"""
Demo scenario data for PriorAuth AI.
Three pre-baked cases now map to clear approval, partial support, and low support.
"""

DEMO_PRESET_LABELS = {
    "approved": "Strong Approval",
    "missing_info": "Missing Info",
    "denied_appeal": "Denial + Appeal",
}

DEMO_SCENARIOS = {
    "approved": {
        "patient_name": "Maria Rodriguez",
        "patient_dob": "1978-03-15",
        "patient_id": "MR-20240315",
        "insurance_plan": "Aetna PPO Gold",
        "insurance_id": "AET-889921034",
        "diagnosis_code": "M17.11",
        "diagnosis_description": "Primary osteoarthritis, right knee",
        "proposed_treatment": "Total Knee Arthroplasty (TKA)",
        "treatment_cpt_code": "27447",
        "clinical_notes": (
            "Patient has had progressive right knee pain for 3 years despite exhaustive conservative "
            "treatment. Failed 6 months of physical therapy (3x/week), NSAIDs (naproxen 500mg BID x6 "
            "months, discontinued due to GI side effects), 3 corticosteroid injections (last 4 months "
            "ago with only 2-week relief), and hyaluronic acid injection series. Weight-bearing X-rays "
            "show bone-on-bone changes with complete loss of medial and lateral joint space. "
            "Kellgren-Lawrence Grade IV. BMI 27.4. Functional limitation: unable to climb stairs or "
            "walk more than 1 block without severe pain. WOMAC pain score 18/20. No surgical "
            "contraindications. Pre-op cardiac clearance obtained. HbA1c 5.6%."
        ),
        "lab_results": (
            "CBC: WBC 6.8, Hgb 13.2, Plt 210. BMP: Na 139, K 4.1, Cr 0.9, Glucose 88. "
            "HbA1c 5.6%. PT/INR 1.0. Pre-op cardiac clearance obtained from cardiologist."
        ),
        "_expected_outcome": "approved",
        "_target_approval_probability": 100,
        "_target_strength_score": 10,
        "_target_policy_likelihood": "High",
        "_target_policy_reasoning": "All core payer criteria are clearly documented, including advanced radiographic severity, prolonged conservative treatment failure, and functional limitation.",
        "_target_evidence_summary": "This case is a clear approval candidate because advanced osteoarthritis severity, multiple failed conservative treatments, functional limitation, imaging, and pre-operative readiness are all documented.",
        "_target_risk_flags": [],
        "_target_suggestions": [],
    },
    "missing_info": {
        "patient_name": "Sarah Thompson",
        "patient_dob": "1992-07-08",
        "patient_id": "ST-20240708",
        "insurance_plan": "Cigna Open Access Plus",
        "insurance_id": "CGN-778834521",
        "diagnosis_code": "G43.909",
        "diagnosis_description": "Migraine, unspecified, not intractable",
        "proposed_treatment": "Erenumab (Aimovig) 140mg monthly injection",
        "treatment_cpt_code": "96372",
        "clinical_notes": (
            "32yo female with chronic migraine, averaging 12 headache days per month with 6 migraine days. "
            "Failed topiramate due to cognitive adverse effects and propranolol due to hypotension. "
            "Currently using sumatriptan for acute treatment. PCP note recommends CGRP therapy, but the payer packet "
            "does not yet include a formal neurology assessment or a structured headache diary."
        ),
        "lab_results": "MRI brain: normal. CBC normal. CMP normal.",
        "_expected_outcome": "missing_info",
        "_target_approval_probability": 65,
        "_target_strength_score": 6,
        "_target_policy_likelihood": "Medium",
        "_target_policy_reasoning": "The case is clinically supportable, but payer review is likely to pause until the headache diary and specialist documentation are attached.",
        "_target_evidence_summary": "The patient meets part of the step-therapy story, but approval support is only partial because the packet is missing the strongest migraine-specific supporting records.",
        "_target_risk_flags": [
            "Neurology evaluation is not yet attached",
            "Headache frequency documentation is not yet packaged as a formal diary",
        ],
        "_target_suggestions": [
            "Attach a neurology assessment confirming migraine burden and CGRP rationale",
            "Add a structured headache diary showing monthly headache and migraine day counts",
        ],
    },
    "denied_appeal": {
        "patient_name": "James Chen",
        "patient_dob": "1965-11-22",
        "patient_id": "JC-20241122",
        "insurance_plan": "UnitedHealthcare Choice Plus",
        "insurance_id": "UHC-445567123",
        "diagnosis_code": "C34.11",
        "diagnosis_description": "Malignant neoplasm of upper lobe, right bronchus or lung",
        "proposed_treatment": "Pembrolizumab (Keytruda) immunotherapy",
        "treatment_cpt_code": "96413",
        "clinical_notes": (
            "62yo male with NSCLC referred for pembrolizumab authorization after chemotherapy. "
            "Outside oncology summary mentions prior cisplatin/pemetrexed, but the submitted packet does not clearly document "
            "current line of therapy, formal treatment response, or the oncologist's maintenance treatment rationale. "
            "No autoimmune history is documented. ECOG is listed as 1 in a brief summary note."
        ),
        "lab_results": (
            "PD-L1 TPS: 80%. CBC and CMP are within normal limits. The packet does not include the full oncology progress note, "
            "formal response assessment, or the original pathology and staging documents."
        ),
        "_expected_outcome": "denied_appeal",
        "_target_approval_probability": 30,
        "_target_strength_score": 4,
        "_target_policy_likelihood": "Low",
        "_target_policy_reasoning": "The requested immunotherapy may be clinically reasonable, but the payer packet does not clearly support the requested treatment line or contain the full oncology rationale.",
        "_target_evidence_summary": "This case is low approval because the packet lacks the key oncology records needed to justify why pembrolizumab maintenance should be approved at this point in treatment.",
        "_target_risk_flags": [
            "Current line of therapy is not clearly documented in the packet",
            "Full oncology rationale and treatment response records are not attached",
        ],
        "_target_suggestions": [
            "Attach the full oncology progress note documenting the intended maintenance pathway",
            "Add treatment response records and staging and pathology documents before submission",
        ],
    },
}

DEMO_PRESETS_FRONTEND = {
    key: {k: v for k, v in val.items() if not k.startswith("_")}
    for key, val in DEMO_SCENARIOS.items()
}


def get_demo_presets() -> list[dict]:
    """Return frontend-safe demo presets from the canonical backend scenarios."""
    presets = []
    for scenario_key, data in DEMO_SCENARIOS.items():
        presets.append(
            {
                "key": scenario_key,
                "label": DEMO_PRESET_LABELS.get(scenario_key, scenario_key),
                "data": {k: v for k, v in data.items() if not k.startswith("_")},
            }
        )
    return presets
