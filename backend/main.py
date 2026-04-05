"""
PriorAuth AI - FastAPI backend
"""
import asyncio
import json
import os
import sys
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db_service import (
    init_db,
    get_db_connection,
    record_status_change,
    save_agent_outputs,
    save_case_insights,
    get_case_insights,
)
from pipeline_engine import run_review, run_submission_tracker, _get_submission_defaults
from demo_data import DEMO_SCENARIOS, get_demo_presets

# ── App Setup ─────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="PriorAuth AI", version="2.0.0", lifespan=lifespan)

cors_origins_env = os.getenv("CORS_ORIGINS", "")
allowed_origins = [
    origin.strip()
    for origin in cors_origins_env.split(",")
    if origin.strip()
]
if not allowed_origins:
    allowed_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Pydantic Models ────────────────────────────────────────────────────────────
class CreateCaseRequest(BaseModel):
    patient_name: str
    patient_dob: Optional[str] = None
    patient_id: Optional[str] = None
    insurance_plan: Optional[str] = None
    insurance_id: Optional[str] = None
    diagnosis_code: Optional[str] = None
    diagnosis_description: Optional[str] = None
    proposed_treatment: Optional[str] = None
    treatment_cpt_code: Optional[str] = None
    clinical_notes: Optional[str] = None
    lab_results: Optional[str] = None


class SubmitDraftRequest(BaseModel):
    draft: dict[str, Any]


DEMO_PATIENT_IDS = {
    scenario["patient_id"]
    for scenario in DEMO_SCENARIOS.values()
    if scenario.get("patient_id")
}


def _get_hidden_demo_case_ids(rows: list[Any]) -> set[int]:
    """Hide only the original seeded demo rows, not newer user-created copies."""
    oldest_by_patient: dict[str, int] = {}
    for row in rows:
        item = dict(row)
        patient_id = item.get("patient_id")
        if patient_id not in DEMO_PATIENT_IDS:
            continue
        case_id = item.get("id")
        if patient_id not in oldest_by_patient or case_id < oldest_by_patient[patient_id]:
            oldest_by_patient[patient_id] = case_id
    return set(oldest_by_patient.values())


def _load_case_outputs(case_id: int) -> list[dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM agent_outputs WHERE case_id = ? ORDER BY created_at ASC",
        (case_id,),
    )
    rows = cursor.fetchall()
    conn.close()

    outputs = []
    for row in rows:
        output = dict(row)
        try:
            output["output_data"] = json.loads(output["output_data"])
        except Exception:
            output["output_data"] = {}
        outputs.append(output)
    return outputs


def _find_agent_parsed_output(outputs: list[dict[str, Any]], agent_name: str) -> dict[str, Any]:
    for output in reversed(outputs):
        if output.get("agent_name") == agent_name:
            return output.get("output_data", {}).get("parsed", {}) or {}
    return {}


def _build_follow_up_schedule(case_id: int) -> list[dict[str, Any]]:
    return [
        {
            "day": 7,
            "audience": "insurance",
            "action": "Automated payer status check",
            "contact_method": "Portal message",
            "message": (
                f"Follow-up for Prior Authorization Case #{case_id}: "
                "Please confirm receipt and provide the current review status."
            ),
        },
        {
            "day": 7,
            "audience": "doctor",
            "action": "Physician update reminder",
            "contact_method": "Internal inbox message",
            "message": (
                f"Case #{case_id} is pending with the payer. "
                "Please review whether any additional notes, imaging, or treatment history should be added."
            ),
        },
        {
            "day": 14,
            "audience": "insurance",
            "action": "Second automated status request",
            "contact_method": "Fax or secure message",
            "message": (
                f"Second follow-up for Prior Authorization Case #{case_id}: "
                "Please share any pending documentation needs or utilization review updates."
            ),
        },
        {
            "day": 14,
            "audience": "doctor",
            "action": "Request addendum review",
            "contact_method": "Internal inbox message",
            "message": (
                f"Case #{case_id} remains pending. "
                "Please confirm whether an addendum or peer-to-peer request should be prepared."
            ),
        },
        {
            "day": 21,
            "audience": "insurance",
            "action": "Escalation follow-up",
            "contact_method": "Phone call with written summary",
            "message": (
                f"Escalation follow-up for Prior Authorization Case #{case_id}: "
                "This request remains pending. Please advise on decision timing or any final requirements."
            ),
        },
        {
            "day": 21,
            "audience": "doctor",
            "action": "Escalation planning reminder",
            "contact_method": "Internal inbox message",
            "message": (
                f"Case #{case_id} has been pending for 21 days. "
                "Please review appeal readiness and escalation options."
            ),
        },
    ]


def _build_denial_payload(case_id: int, case_data: dict[str, Any], outputs: list[dict[str, Any]]) -> dict[str, Any]:
    policy_output = _find_agent_parsed_output(outputs, "Policy & Requirements Engine")
    intelligence_output = _find_agent_parsed_output(outputs, "Case Intelligence Engine")
    submission_output = _find_agent_parsed_output(outputs, "Submission & Tracker")

    missing_items = policy_output.get("missing_items") or []
    risk_flags = intelligence_output.get("risk_flags") or []
    suggestions = intelligence_output.get("suggestions") or []
    missing_fields = submission_output.get("missing_fields") or []

    denial_reasons = []
    if missing_items:
        denial_reasons.append(
            "Payer-required supporting documentation was not fully documented in the submission package."
        )
    if risk_flags:
        denial_reasons.append(str(risk_flags[0]))
    if missing_fields:
        denial_reasons.append(
            f"Administrative fields still needed review: {', '.join(missing_fields[:4])}."
        )
    if not denial_reasons:
        denial_reasons.append(
            "Medical necessity criteria were not sufficiently supported for this payer's policy requirements."
        )

    improvement_suggestions = []
    if suggestions:
        improvement_suggestions.extend(suggestions[:3])
    if missing_items:
        improvement_suggestions.append(
            f"Add supporting documentation for: {', '.join(missing_items[:3])}."
        )
    if case_data.get("clinical_notes"):
        improvement_suggestions.append(
            "Strengthen the justification letter with direct references to the documented failed treatments and objective findings."
        )
    if not improvement_suggestions:
        improvement_suggestions = [
            "Add payer-specific documentation and resubmit with a stronger medical necessity narrative.",
            "Request a peer-to-peer review if the payer allows it.",
        ]

    appeal_letter = submission_output.get("appeal_letter")
    follow_up_schedule = _build_follow_up_schedule(case_id)

    return {
        "case_id": case_id,
        "new_status": "denied",
        "denial_reason": " ".join(denial_reasons),
        "denial_reasons": denial_reasons,
        "improvement_suggestions": improvement_suggestions,
        "appeal_deadline": "60 days from denial date",
        "appeal_letter": appeal_letter,
        "follow_up_schedule": follow_up_schedule,
        "automated_follow_up_enabled": True,
        "next_steps": [
            "Review the denial rationale and compare it against the payer criteria.",
            "Update the application with missing documentation or stronger clinical evidence.",
            "Request peer-to-peer review with the insurance medical director.",
            "Submit the appeal package before the deadline.",
        ],
    }


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/api/cases")
def list_cases():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    hidden_demo_case_ids = _get_hidden_demo_case_ids(rows)
    cases = []
    for row in rows:
        case = dict(row)
        case["is_demo_case"] = case["id"] in hidden_demo_case_ids
        cases.append(case)
    return cases


@app.get("/api/demo-presets")
def list_demo_presets():
    return get_demo_presets()


@app.post("/api/cases", status_code=201)
def create_case(body: CreateCaseRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()

    cursor.execute(
        """
        INSERT INTO cases (
            patient_name, patient_dob, patient_id, insurance_plan, insurance_id,
            diagnosis_code, diagnosis_description, proposed_treatment, treatment_cpt_code,
            clinical_notes, lab_results, status, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'intake', ?, ?)
        """,
        (
            body.patient_name, body.patient_dob, body.patient_id,
            body.insurance_plan, body.insurance_id,
            body.diagnosis_code, body.diagnosis_description,
            body.proposed_treatment, body.treatment_cpt_code,
            body.clinical_notes, body.lab_results, now, now,
        ),
    )
    case_id = cursor.lastrowid
    cursor.execute(
        "INSERT INTO status_history (case_id, old_status, new_status, notes, created_at) VALUES (?, ?, ?, ?, ?)",
        (case_id, None, "intake", "Case created", now),
    )
    conn.commit()
    cursor.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row)


@app.delete("/api/cases/{case_id}", status_code=204)
def delete_case(case_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM cases WHERE id = ?", (case_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")

    cursor.execute("DELETE FROM agent_outputs WHERE case_id = ?", (case_id,))
    cursor.execute("DELETE FROM status_history WHERE case_id = ?", (case_id,))
    cursor.execute("DELETE FROM case_insights WHERE case_id = ?", (case_id,))
    cursor.execute("DELETE FROM cases WHERE id = ?", (case_id,))
    conn.commit()
    conn.close()


@app.get("/api/cases/{case_id}")
def get_case(case_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
    case_row = cursor.fetchone()
    if not case_row:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")

    case = dict(case_row)
    case["is_demo_case"] = False

    cursor.execute(
        "SELECT * FROM agent_outputs WHERE case_id = ? ORDER BY created_at ASC",
        (case_id,),
    )
    outputs = _load_case_outputs(case_id)

    cursor.execute(
        "SELECT * FROM status_history WHERE case_id = ? ORDER BY created_at ASC",
        (case_id,),
    )
    history = [dict(r) for r in cursor.fetchall()]
    conn.close()

    return {
        "case": case,
        "provider_context": _get_submission_defaults(case),
        "agent_outputs": outputs,
        "status_history": history,
    }


@app.post("/api/cases/{case_id}/run")
async def run_pipeline(case_id: int, demo: bool = False, scenario: str = ""):
    """Run the physician review stage (agents 1 and 2)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")

    case_data = dict(row)
    old_status = case_data["status"]
    conn.close()

    # Demo mode: substitute pre-baked scenario data but keep the real case_id
    if demo and scenario in DEMO_SCENARIOS:
        scenario_data = {
            k: v for k, v in DEMO_SCENARIOS[scenario].items()
            if not k.startswith("_")
        }
        case_data.update(scenario_data)
        case_data["id"] = case_id  # preserve real case_id for DB writes

    # Clear previous outputs so polling shows fresh data
    conn2 = get_db_connection()
    conn2.execute("DELETE FROM agent_outputs WHERE case_id = ?", (case_id,))
    conn2.commit()
    conn2.close()

    record_status_change(case_id, old_status, "processing", "Clinical review started")

    # Run agents in thread — keeps event loop free for polling requests
    results = await asyncio.to_thread(run_review, case_data)

    if not results.get("outputs_saved"):
        save_agent_outputs(
            case_id,
            results.get("task_outputs", []),
            results.get("elapsed_seconds", 0),
        )

    # Extract and persist Case Intelligence insights
    intel_output = next(
        (o for o in results.get("task_outputs", [])
         if o.get("agent_name") == "Case Intelligence Engine"),
        None,
    )
    if intel_output:
        parsed = intel_output.get("parsed_output", {})
        try:
            save_case_insights(
                case_id,
                approval_probability=parsed.get("approval_probability", 50),
                risk_flags=parsed.get("risk_flags", []),
                suggestions=parsed.get("suggestions", []),
                strength_score=parsed.get("strength_score", 5),
            )
        except Exception as e:
            print(f"[run_pipeline] Failed to save insights: {e}")

    new_status = "analyzed" if results.get("success") else "error"
    record_status_change(
        case_id, "processing", new_status,
        f"Clinical review {'completed' if results['success'] else 'failed'} in {results['elapsed_seconds']}s"
        + (" [fallback mode]" if results.get("fallback_mode") else "")
        + (" [cached]" if results.get("cached") else ""),
    )

    return {
        "case_id": case_id,
        "success": results.get("success"),
        "error": results.get("error"),
        "fallback_mode": results.get("fallback_mode", False),
        "mode": results.get("mode", "ai"),
        "task_outputs": results.get("task_outputs", []),
        "elapsed_seconds": results.get("elapsed_seconds"),
        "manual_benchmark_seconds": results.get("manual_benchmark_seconds", 2700),
        "time_saved_percent": results.get("time_saved_percent"),
        "estimated_cost_manual": results.get("estimated_cost_manual", 31.00),
        "estimated_cost_ai": results.get("estimated_cost_ai", 0.0),
        "new_status": new_status,
    }


@app.post("/api/cases/{case_id}/submit")
async def submit_application(case_id: int, body: SubmitDraftRequest):
    """Submit the doctor-approved application and start submission tracking."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")

    case_data = dict(row)
    old_status = case_data["status"]

    cursor.execute(
        "SELECT * FROM agent_outputs WHERE case_id = ? ORDER BY created_at ASC",
        (case_id,),
    )
    stored_outputs = []
    for output_row in cursor.fetchall():
        output = dict(output_row)
        try:
            output_data = json.loads(output["output_data"])
        except Exception:
            output_data = {}

        agent_name = output.get("agent_name")
        agent_key = (
            "policy_engine" if agent_name == "Policy & Requirements Engine"
            else "case_intelligence" if agent_name == "Case Intelligence Engine"
            else "submission_tracker" if agent_name == "Submission & Tracker"
            else None
        )
        if agent_key:
            stored_outputs.append(
                {
                    "agent_key": agent_key,
                    "agent_name": agent_name,
                    "parsed_output": output_data.get("parsed", {}),
                    "raw_output": output_data.get("raw", ""),
                }
            )
    conn.close()

    prior_outputs = [
        output for output in stored_outputs
        if output.get("agent_key") in {"policy_engine", "case_intelligence"}
    ]
    if len(prior_outputs) < 2:
        raise HTTPException(
            status_code=400,
            detail="Run the clinical review first before submitting to the insurance company.",
        )

    draft = body.draft or {}
    case_data.update({
        "insurance_id": draft.get("insurance_id") or case_data.get("insurance_id"),
        "diagnosis_code": draft.get("diagnosis_code") or case_data.get("diagnosis_code"),
        "diagnosis_description": draft.get("diagnosis_description") or case_data.get("diagnosis_description"),
        "proposed_treatment": draft.get("procedure_description") or case_data.get("proposed_treatment"),
        "treatment_cpt_code": draft.get("cpt_code") or case_data.get("treatment_cpt_code"),
        "clinical_notes": draft.get("clinical_summary") or case_data.get("clinical_notes"),
        "service_date_requested": draft.get("service_date_requested") or case_data.get("service_date_requested"),
        "medical_necessity_letter": draft.get("medical_necessity_letter") or "",
        "review_notes": draft.get("review_notes") or "",
        "submission_method": draft.get("submission_method") or "",
    })

    submission_defaults = _get_submission_defaults(case_data)
    submission_defaults.update({
        "provider_name": draft.get("provider_name") or submission_defaults.get("provider_name"),
        "provider_npi": draft.get("provider_npi") or submission_defaults.get("provider_npi"),
        "provider_phone": draft.get("provider_phone") or submission_defaults.get("provider_phone"),
        "provider_fax": draft.get("provider_fax") or submission_defaults.get("provider_fax"),
        "provider_specialty": draft.get("provider_specialty") or submission_defaults.get("provider_specialty"),
        "facility_name": draft.get("facility_name") or submission_defaults.get("facility_name"),
        "service_location": draft.get("service_location") or submission_defaults.get("service_location"),
        "urgency": draft.get("urgency") or submission_defaults.get("urgency"),
    })
    case_data.update(submission_defaults)

    conn2 = get_db_connection()
    conn2.execute(
        "DELETE FROM agent_outputs WHERE case_id = ? AND agent_name = 'Submission & Tracker'",
        (case_id,),
    )
    conn2.commit()
    conn2.close()

    record_status_change(
        case_id,
        old_status,
        "processing",
        "Doctor approved draft. Submission & tracking started.",
    )

    results = await asyncio.to_thread(run_submission_tracker, case_data, prior_outputs)

    if not results.get("outputs_saved"):
        save_agent_outputs(
            case_id,
            results.get("task_outputs", []),
            results.get("elapsed_seconds", 0),
        )

    new_status = "submitted" if results.get("success") else "error"
    record_status_change(
        case_id,
        "processing",
        new_status,
        f"Submission tracker {'completed' if results['success'] else 'failed'} in {results['elapsed_seconds']}s"
        + (" [fallback mode]" if results.get("fallback_mode") else ""),
    )

    combined_outputs = prior_outputs + (results.get("task_outputs", []) or [])

    return {
        "case_id": case_id,
        "success": results.get("success"),
        "error": results.get("error"),
        "fallback_mode": results.get("fallback_mode", False),
        "mode": results.get("mode", "ai"),
        "task_outputs": combined_outputs,
        "elapsed_seconds": results.get("elapsed_seconds"),
        "manual_benchmark_seconds": results.get("manual_benchmark_seconds", 2700),
        "time_saved_percent": results.get("time_saved_percent"),
        "estimated_cost_manual": results.get("estimated_cost_manual", 31.00),
        "estimated_cost_ai": results.get("estimated_cost_ai", 0.0),
        "new_status": new_status,
    }


@app.get("/api/cases/{case_id}/insights")
def get_insights(case_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cases WHERE id = ?", (case_id,))
    if cursor.fetchone()[0] == 0:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
    conn.close()

    insights = get_case_insights(case_id)
    if not insights:
        raise HTTPException(status_code=404, detail="No insights available for this case yet")
    return insights


@app.get("/api/cases/{case_id}/outputs")
def get_case_outputs(case_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cases WHERE id = ?", (case_id,))
    if cursor.fetchone()[0] == 0:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
    conn.close()

    return _load_case_outputs(case_id)


@app.post("/api/cases/{case_id}/deny")
def simulate_denial(case_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
    old_status = dict(row)["status"]
    conn.close()

    record_status_change(
        case_id, old_status, "denied",
        "Denial simulated — Insurance plan issued denial notice. Appeal rights available within 60 days.",
    )

    outputs = _load_case_outputs(case_id)
    return _build_denial_payload(case_id, dict(row), outputs)


@app.post("/api/cases/{case_id}/approve")
def simulate_approval(case_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
    old_status = dict(row)["status"]
    conn.close()

    record_status_change(
        case_id, old_status, "approved",
        f"Approval simulated — Prior authorization granted. Auth number: PA-{str(case_id).zfill(8)}",
    )
    return {
        "case_id": case_id,
        "new_status": "approved",
        "auth_number": f"PA-{str(case_id).zfill(8)}",
        "valid_for": "90 days from approval date",
        "next_steps": [
            "Communicate authorization to patient",
            "Schedule the procedure/treatment",
            "Retain authorization number for billing",
            "Verify authorization validity before service date",
        ],
    }


@app.get("/api/metrics")
def get_metrics():
    conn = get_db_connection()
    cursor = conn.cursor()
    all_case_rows = cursor.execute("SELECT id, patient_id FROM cases").fetchall()
    demo_case_ids = _get_hidden_demo_case_ids(all_case_rows)

    def count_cases(where_clause: str = "", params: tuple = ()) -> int:
        query = f"SELECT id FROM cases {where_clause}"
        rows = cursor.execute(query, params).fetchall()
        return sum(1 for row in rows if row["id"] not in demo_case_ids)

    total = count_cases()
    approved = count_cases("WHERE status = 'approved'")
    denied = count_cases("WHERE status = 'denied'")
    in_progress = count_cases("WHERE status = 'processing'")
    analyzed = count_cases("WHERE status = 'analyzed'")
    intake = count_cases("WHERE status = 'intake'")

    cursor.execute("SELECT COUNT(*) as cnt FROM agent_outputs")
    total_outputs = cursor.fetchone()["cnt"]

    cursor.execute(
        "SELECT AVG(execution_time_seconds) as avg_time FROM agent_outputs WHERE execution_time_seconds IS NOT NULL"
    )
    avg_row = cursor.fetchone()
    avg_time = round(avg_row["avg_time"], 2) if avg_row["avg_time"] else None

    cursor.execute("SELECT AVG(approval_probability) as avg_prob FROM case_insights")
    prob_row = cursor.fetchone()
    avg_approval_prob = round(prob_row["avg_prob"], 1) if prob_row["avg_prob"] else None

    conn.close()

    approval_rate = round((approved / total * 100), 1) if total > 0 else 0

    return {
        "total_cases": total,
        "approved": approved,
        "denied": denied,
        "in_progress": in_progress,
        "analyzed": analyzed,
        "intake": intake,
        "total_agent_outputs": total_outputs,
        "avg_pipeline_time_seconds": avg_time,
        "avg_approval_probability": avg_approval_prob,
        "approval_rate_percent": approval_rate,
        "manual_benchmark_seconds": 2700,
        "cost_per_manual_pa": 31.00,
        "estimated_annual_savings": round(total * 30.85, 2),
    }
