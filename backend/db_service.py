"""
SQLite database setup and seed data for PriorAuth AI (DB Service).
"""
import json
import os
import sqlite3
from datetime import datetime, timezone
from demo_data import DEMO_SCENARIOS

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prior_auth.db")


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables and seed demo data if empty."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            patient_dob TEXT,
            patient_id TEXT,
            insurance_plan TEXT,
            insurance_id TEXT,
            diagnosis_code TEXT,
            diagnosis_description TEXT,
            proposed_treatment TEXT,
            treatment_cpt_code TEXT,
            clinical_notes TEXT,
            lab_results TEXT,
            status TEXT DEFAULT 'intake',
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS agent_outputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER NOT NULL,
            agent_name TEXT NOT NULL,
            output_type TEXT NOT NULL,
            output_data TEXT NOT NULL,
            execution_time_seconds REAL,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (case_id) REFERENCES cases(id)
        );

        CREATE TABLE IF NOT EXISTS status_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER NOT NULL,
            old_status TEXT,
            new_status TEXT NOT NULL,
            notes TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (case_id) REFERENCES cases(id)
        );

        CREATE TABLE IF NOT EXISTS case_insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER NOT NULL UNIQUE,
            approval_probability INTEGER,
            risk_flags TEXT,
            suggestions TEXT,
            strength_score INTEGER,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (case_id) REFERENCES cases(id)
        );
    """)
    conn.commit()

    # Seed demo cases if empty, otherwise refresh the core sample cases
    cursor.execute("SELECT COUNT(*) FROM cases")
    count = cursor.fetchone()[0]
    if count == 0:
        _seed_demo_cases(cursor)
        conn.commit()
    else:
        _sync_demo_cases(cursor)
        conn.commit()

    conn.close()


DEMO_CASES = [
    {**{k: v for k, v in DEMO_SCENARIOS["approved"].items() if not k.startswith("_")}, "status": "intake"},
    {**{k: v for k, v in DEMO_SCENARIOS["missing_info"].items() if not k.startswith("_")}, "status": "intake"},
    {**{k: v for k, v in DEMO_SCENARIOS["denied_appeal"].items() if not k.startswith("_")}, "status": "intake"},
    {
        "patient_name": "Robert Williams",
        "patient_dob": "1955-01-30",
        "patient_id": "RW-20240130",
        "insurance_plan": "Medicare Advantage (Humana Gold Plus)",
        "insurance_id": "HUM-112233445",
        "diagnosis_code": "I25.10",
        "diagnosis_description": "Atherosclerotic heart disease of native coronary artery",
        "proposed_treatment": "Cardiac CT Angiography (CCTA)",
        "treatment_cpt_code": "75574",
        "clinical_notes": (
            "71yo male with atypical chest pain, intermediate pre-test probability for CAD. "
            "Calcium score 342. Unable to perform exercise stress test due to severe osteoarthritis. "
            "Pharmacologic stress test was inconclusive. Need CCTA for definitive evaluation before "
            "considering invasive angiography."
        ),
        "lab_results": (
            "Troponin negative x2. BNP 89. Lipid panel: LDL 145, HDL 38, TG 210. HbA1c 6.8%. eGFR 62."
        ),
        "status": "intake",
    },
    {
        "patient_name": "Aisha Patel",
        "patient_dob": "1988-09-12",
        "patient_id": "AP-20240912",
        "insurance_plan": "Blue Cross Blue Shield PPO",
        "insurance_id": "BCBS-993344221",
        "diagnosis_code": "M54.5",
        "diagnosis_description": "Low back pain, unspecified",
        "proposed_treatment": "Lumbar MRI without contrast",
        "treatment_cpt_code": "72148",
        "clinical_notes": (
            "36yo female with 8 weeks of progressive low back pain radiating to left leg. Positive "
            "straight leg raise on left. Decreased sensation L5 dermatome. Failed 6 weeks conservative "
            "management including PT and NSAIDs. Red flags: progressive neurological deficit."
        ),
        "lab_results": (
            "X-ray lumbar spine: mild disc space narrowing L4-L5. ESR 12. CRP 0.4."
        ),
        "status": "intake",
    },
]

DEMO_PATIENT_IDS = {case["patient_id"] for case in DEMO_CASES}


def is_demo_case(case_like: dict | sqlite3.Row) -> bool:
    """Return True when a case belongs to the preloaded demo dataset."""
    patient_id = dict(case_like).get("patient_id")
    return patient_id in DEMO_PATIENT_IDS


def _seed_demo_cases(cursor: sqlite3.Cursor) -> None:
    """Insert demo cases and their initial status history."""
    now = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
    for case in DEMO_CASES:
        cursor.execute(
            """
            INSERT INTO cases (
                patient_name, patient_dob, patient_id, insurance_plan, insurance_id,
                diagnosis_code, diagnosis_description, proposed_treatment, treatment_cpt_code,
                clinical_notes, lab_results, status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                case["patient_name"], case["patient_dob"], case["patient_id"],
                case["insurance_plan"], case["insurance_id"],
                case["diagnosis_code"], case["diagnosis_description"],
                case["proposed_treatment"], case["treatment_cpt_code"],
                case["clinical_notes"], case["lab_results"],
                case["status"], now, now,
            ),
        )
        case_id = cursor.lastrowid
        cursor.execute(
            """
            INSERT INTO status_history (case_id, old_status, new_status, notes, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (case_id, None, "intake", "Case created — awaiting analysis", now),
        )


def _sync_demo_cases(cursor: sqlite3.Cursor) -> None:
    """Refresh the core sample patients so existing workspaces match the latest demo storylines."""
    now = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
    for case in DEMO_CASES[:3]:
        cursor.execute("SELECT id FROM cases WHERE patient_id = ?", (case["patient_id"],))
        existing = cursor.fetchone()
        if not existing:
            continue
        cursor.execute(
            """
            UPDATE cases
            SET patient_name = ?, patient_dob = ?, insurance_plan = ?, insurance_id = ?,
                diagnosis_code = ?, diagnosis_description = ?, proposed_treatment = ?, treatment_cpt_code = ?,
                clinical_notes = ?, lab_results = ?, updated_at = ?
            WHERE patient_id = ?
            """,
            (
                case["patient_name"],
                case["patient_dob"],
                case["insurance_plan"],
                case["insurance_id"],
                case["diagnosis_code"],
                case["diagnosis_description"],
                case["proposed_treatment"],
                case["treatment_cpt_code"],
                case["clinical_notes"],
                case["lab_results"],
                now,
                case["patient_id"],
            ),
        )


def record_status_change(case_id: int, old_status: str, new_status: str, notes: str = "") -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
    cursor.execute(
        "UPDATE cases SET status = ?, updated_at = ? WHERE id = ?",
        (new_status, now, case_id),
    )
    cursor.execute(
        "INSERT INTO status_history (case_id, old_status, new_status, notes, created_at) VALUES (?, ?, ?, ?, ?)",
        (case_id, old_status, new_status, notes, now),
    )
    conn.commit()
    conn.close()


def save_single_agent_output(case_id: int, agent_name: str, raw: str, parsed: dict, elapsed: float) -> None:
    """Persist a single agent output immediately (used by task_callback for real-time updates)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
    output_data = json.dumps({"raw": raw, "parsed": parsed})
    cursor.execute(
        "INSERT INTO agent_outputs (case_id, agent_name, output_type, output_data, execution_time_seconds, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (case_id, agent_name, "analysis", output_data, elapsed, now),
    )
    conn.commit()
    conn.close()


def save_case_insights(
    case_id: int,
    approval_probability: int,
    risk_flags: list,
    suggestions: list,
    strength_score: int,
) -> None:
    """Upsert case intelligence insights."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
    cursor.execute(
        """
        INSERT INTO case_insights (case_id, approval_probability, risk_flags, suggestions, strength_score, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(case_id) DO UPDATE SET
            approval_probability=excluded.approval_probability,
            risk_flags=excluded.risk_flags,
            suggestions=excluded.suggestions,
            strength_score=excluded.strength_score,
            updated_at=excluded.updated_at
        """,
        (
            case_id,
            approval_probability,
            json.dumps(risk_flags or []),
            json.dumps(suggestions or []),
            strength_score,
            now,
            now,
        ),
    )
    conn.commit()
    conn.close()


def get_case_insights(case_id: int) -> dict | None:
    """Retrieve insights for a case, or None if not yet available."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM case_insights WHERE case_id = ?", (case_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    data = dict(row)
    try:
        data["risk_flags"] = json.loads(data["risk_flags"] or "[]")
    except Exception:
        data["risk_flags"] = []
    try:
        data["suggestions"] = json.loads(data["suggestions"] or "[]")
    except Exception:
        data["suggestions"] = []
    return data


def save_agent_outputs(case_id: int, task_outputs: list, elapsed_seconds: float) -> None:
    """Persist agent outputs to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()

    for output in task_outputs:
        agent_name = output.get("agent_name", "Unknown Agent")
        raw = output.get("raw_output", "")
        parsed = output.get("parsed_output", {})
        output_data = json.dumps({"raw": raw, "parsed": parsed})

        cursor.execute(
            """
            INSERT INTO agent_outputs (case_id, agent_name, output_type, output_data, execution_time_seconds, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (case_id, agent_name, "analysis", output_data, elapsed_seconds, now),
        )
    conn.commit()
    conn.close()
