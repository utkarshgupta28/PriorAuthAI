"""
Policy knowledge base for prior authorization rules and clinical guidelines.
"""

POLICY_RULES = {
    "27447": {
        "procedure": "Total Knee Arthroplasty",
        "clinical_goal": "Authorize TKA only when advanced symptomatic knee osteoarthritis has failed appropriate conservative management.",
        "requires_prior_auth": True,
        "plans_requiring": ["Aetna", "UnitedHealthcare", "Cigna", "BCBS", "Humana", "Medicare"],
        "criteria": [
            "Kellgren-Lawrence Grade III or IV on weight-bearing X-ray",
            "Documented failure of conservative treatment >= 3 months (PT, NSAIDs, injections)",
            "Significant functional limitation documented (WOMAC or KOOS score)",
            "BMI < 40 preferred (some plans hard requirement)",
            "Medical optimization of comorbidities (diabetes, cardiac)",
        ],
        "required_documentation": [
            "Weight-bearing knee X-rays (AP, lateral, sunrise views)",
            "Clinical notes documenting conservative treatment history",
            "Physical therapy records (minimum 6 weeks)",
            "Pre-operative medical clearance",
            "CBC, BMP, HbA1c (if diabetic), coagulation studies",
        ],
        "common_denial_reasons": [
            "Insufficient documentation of failed conservative treatment duration",
            "Severity of osteoarthritis not clearly documented on weight-bearing imaging",
            "Functional limitation not described in the orthopedic assessment",
        ],
        "documentation_examples": [
            "Orthopedic note documents 3 years of progressive knee pain limiting ambulation and stairs",
            "X-ray impression states bone-on-bone medial compartment narrowing with Kellgren-Lawrence Grade IV changes",
            "Treatment history lists NSAIDs, physical therapy, corticosteroid injections, and hyaluronic acid injection failure",
        ],
        "typical_turnaround": "5-15 business days",
        "appeal_success_rate": "65-75%",
    },
    "96413": {
        "procedure": "Chemotherapy/Immunotherapy Infusion (Pembrolizumab/Keytruda)",
        "clinical_goal": "Authorize immune checkpoint therapy when diagnosis, biomarker status, prior treatment line, and organ function support use.",
        "requires_prior_auth": True,
        "plans_requiring": ["Aetna", "UnitedHealthcare", "Cigna", "BCBS", "Humana", "Medicare"],
        "criteria": [
            "FDA-approved indication for the diagnosis",
            "PD-L1 expression testing performed and documented",
            "ECOG performance status 0-2",
            "Adequate organ function (liver, kidney, bone marrow)",
            "No active autoimmune disease requiring systemic treatment",
            "No prior severe immune-related adverse events",
            "NCCN Category 1 recommendation for this line of therapy",
        ],
        "required_documentation": [
            "Pathology report confirming cancer type and stage",
            "PD-L1 TPS testing results",
            "Molecular/genomic profiling (EGFR, ALK, ROS1 for NSCLC)",
            "Prior treatment records and response documentation",
            "ECOG performance status documentation",
            "Current labs: CBC, CMP, thyroid function",
        ],
        "common_denial_reasons": [
            "Missing PD-L1 or molecular testing documentation",
            "Line of therapy or prior regimen history not clearly documented",
            "Current organ function labs not included",
        ],
        "documentation_examples": [
            "Oncology note states stage, histology, biomarker profile, and current line of therapy",
            "Lab section includes CBC, CMP, and thyroid function results within the current review window",
            "Treatment response note documents progression or partial response after prior systemic therapy",
        ],
        "typical_turnaround": "3-7 business days",
        "appeal_success_rate": "70-80%",
    },
    "96372": {
        "procedure": "Erenumab (Aimovig) 140mg Subcutaneous Injection",
        "clinical_goal": "Authorize CGRP biologic therapy after migraine diagnosis and step-therapy failure are documented.",
        "requires_prior_auth": True,
        "plans_requiring": ["Aetna", "UnitedHealthcare", "Cigna", "BCBS", "Humana"],
        "criteria": [
            "Diagnosis of chronic migraine (>= 15 headache days/month) OR episodic migraine (>= 4 migraine days/month)",
            "Failed at least 2 oral preventive medications from different drug classes",
            "Classes include: beta-blockers, tricyclics, anticonvulsants, calcium channel blockers, ACE inhibitors",
            "Documented headache diary or neurologist assessment of frequency",
            "No contraindications to CGRP pathway inhibition",
        ],
        "required_documentation": [
            "Neurology evaluation confirming migraine diagnosis",
            "Headache diary or documented frequency/severity",
            "Documentation of 2+ failed preventive medications (drug, dose, duration, reason stopped)",
            "Current migraine medications and frequency of acute treatment use",
            "MRI/CT head results to rule out secondary causes",
        ],
        "common_denial_reasons": [
            "Headache frequency threshold not clearly documented",
            "Failed preventive medication trials missing dose, duration, or discontinuation reason",
            "Neurology evaluation absent or incomplete",
        ],
        "documentation_examples": [
            "Headache diary documents 18 headache days per month with 8 migraine days",
            "Medication history lists topiramate and propranolol failures with duration and adverse effects",
            "Neurology assessment confirms chronic migraine and lack of adequate control with standard preventives",
        ],
        "typical_turnaround": "3-7 business days",
        "appeal_success_rate": "60-70%",
    },
    "75574": {
        "procedure": "Cardiac CT Angiography (CCTA)",
        "clinical_goal": "Authorize CCTA when chest pain evaluation supports noninvasive coronary imaging over stress testing or invasive angiography.",
        "requires_prior_auth": True,
        "plans_requiring": ["Aetna", "UnitedHealthcare", "Cigna", "BCBS", "Humana", "Medicare"],
        "criteria": [
            "Intermediate pre-test probability of CAD (10-90%)",
            "Non-diagnostic stress test OR inability to perform stress test",
            "Stable chest pain syndrome evaluation",
            "Assessment before revascularization decision",
            "Contraindication to invasive coronary angiography",
        ],
        "required_documentation": [
            "Clinical notes documenting chest pain symptoms",
            "Pre-test probability calculation",
            "Prior non-diagnostic or uninterpretable stress test results",
            "Documentation of reason exercise stress test not feasible",
            "Coronary calcium score (if available)",
            "Current medications and cardiovascular risk factors",
        ],
        "common_denial_reasons": [
            "Pre-test probability not documented",
            "No explanation for why stress testing is non-diagnostic or not feasible",
            "Symptoms and CAD risk profile not sufficiently characterized",
        ],
        "documentation_examples": [
            "Cardiology note documents stable exertional chest pain with intermediate CAD risk",
            "Prior stress test report is attached and marked non-diagnostic",
            "The chart explains inability to complete exercise testing because of functional limitation",
        ],
        "typical_turnaround": "3-5 business days",
        "appeal_success_rate": "55-65%",
    },
    "72148": {
        "procedure": "Lumbar MRI Without Contrast",
        "clinical_goal": "Authorize lumbar MRI when red flags, neurological findings, or conservative treatment failure justify advanced imaging.",
        "requires_prior_auth": True,
        "plans_requiring": ["Aetna", "UnitedHealthcare", "Cigna", "BCBS", "Humana"],
        "criteria": [
            "Symptoms >= 6 weeks despite conservative management (PT, NSAIDs, activity modification)",
            "Presence of red flags: progressive neurological deficit, bowel/bladder dysfunction, fever, weight loss",
            "Positive clinical signs of nerve root compression (straight leg raise, dermatomal deficit)",
            "Prior to surgical or interventional procedure",
            "Failure to respond to initial conservative therapy",
        ],
        "required_documentation": [
            "Clinical notes documenting symptom duration and character",
            "Physical exam findings including straight leg raise, neurological deficits",
            "Documentation of failed conservative treatment (PT records, medication trials)",
            "Prior imaging results if available",
            "Specific clinical indication for MRI over other imaging",
        ],
        "common_denial_reasons": [
            "Symptoms have not met the usual duration threshold for imaging",
            "Neurological deficits or red flags are not documented clearly",
            "Conservative treatment trial is missing or too vague",
        ],
        "documentation_examples": [
            "Primary care note documents 8 weeks of radicular pain despite NSAIDs and physical therapy",
            "Exam section includes positive straight leg raise and dermatomal sensory loss",
            "MRI request states planned interventional or surgical decision-making",
        ],
        "typical_turnaround": "1-3 business days",
        "appeal_success_rate": "70-80%",
    },
}

CLINICAL_GUIDELINES = {
    "M17.11": {
        "diagnosis": "Primary osteoarthritis, right knee",
        "chart_signals": [
            "Progressive knee pain with impaired walking, stairs, or activities of daily living",
            "Weight-bearing X-ray showing advanced degenerative joint disease",
            "Failure of PT, NSAIDs, corticosteroid injections, or hyaluronic acid injections",
        ],
        "guidelines": [
            {
                "organization": "AAOS",
                "title": "Clinical Practice Guideline for the Diagnosis and Treatment of Osteoarthritis of the Knee",
                "year": 2021,
                "recommendations": [
                    "Strong evidence supports TKA for moderate-to-severe osteoarthritis with functional limitation",
                    "Conservative treatment failure (PT, NSAIDs, injections) is prerequisite for surgical consideration",
                    "Kellgren-Lawrence Grade III-IV on weight-bearing radiograph indicates surgical candidacy",
                    "Patient should have tried and failed at least 3 months of non-surgical management",
                ],
            },
            {
                "organization": "ACR",
                "title": "Guideline for the Management of Osteoarthritis of the Hand, Hip, and Knee",
                "year": 2020,
                "recommendations": [
                    "Exercise and physical therapy are first-line treatments",
                    "Intra-articular corticosteroids and hyaluronic acid may provide temporary relief",
                    "TKA is conditionally recommended for patients with moderate-to-severe functional limitation",
                    "Preoperative optimization of BMI, HbA1c, and cardiac status improves outcomes",
                ],
            },
        ],
    },
    "C34.11": {
        "diagnosis": "Malignant neoplasm of upper lobe, right bronchus or lung",
        "chart_signals": [
            "Pathology-confirmed NSCLC stage and histology",
            "PD-L1 TPS and molecular profile documented",
            "Prior systemic therapy history and current ECOG status available",
        ],
        "guidelines": [
            {
                "organization": "NCCN",
                "title": "NCCN Clinical Practice Guidelines in Oncology: Non-Small Cell Lung Cancer",
                "year": 2024,
                "recommendations": [
                    "Pembrolizumab is Category 1 recommendation for NSCLC with PD-L1 TPS >= 1% after progression on chemotherapy",
                    "PD-L1 testing is required before initiating checkpoint inhibitor therapy",
                    "Comprehensive molecular profiling (EGFR, ALK, ROS1, KRAS, MET) required for adenocarcinoma",
                    "Pembrolizumab maintenance after platinum-based chemotherapy extends PFS and OS",
                ],
            },
            {
                "organization": "ASCO",
                "title": "Systemic Therapy for Stage IV Non-Small-Cell Lung Cancer: ASCO Clinical Practice Guideline",
                "year": 2023,
                "recommendations": [
                    "Immune checkpoint inhibitor therapy is standard of care for eligible NSCLC patients",
                    "ECOG PS 0-2 required for checkpoint inhibitor candidacy",
                    "PD-L1 high expression (TPS >= 50%) predicts superior response to pembrolizumab monotherapy",
                    "Biomarker testing guides selection between chemotherapy, immunotherapy, and targeted therapy",
                ],
            },
        ],
    },
    "G43.909": {
        "diagnosis": "Migraine, unspecified, not intractable",
        "chart_signals": [
            "Headache days per month documented",
            "Two or more failed preventive medication trials listed with reason stopped",
            "Neurology assessment confirms migraine subtype and severity burden",
        ],
        "guidelines": [
            {
                "organization": "AHS",
                "title": "American Headache Society Consensus Statement: Integrating New Migraine Treatments",
                "year": 2021,
                "recommendations": [
                    "CGRP monoclonal antibodies (erenumab, fremanezumab, galcanezumab) are effective for chronic migraine prevention",
                    "Step therapy requiring 2+ failed oral preventives from different drug classes before CGRP biologics",
                    "Erenumab 140mg shown superior efficacy to 70mg dose in chronic migraine",
                    "CGRP antagonists indicated when conventional preventives are contraindicated or not tolerated",
                ],
            },
            {
                "organization": "AAN",
                "title": "Practice Guideline Update Summary: Acute Treatment of Migraine in Adults",
                "year": 2023,
                "recommendations": [
                    "Preventive therapy indicated for >= 4 migraine days/month or >= 15 headache days/month",
                    "Failed preventive medications must be documented with drug, dose, duration, and reason for discontinuation",
                    "Medication overuse headache (10+ acute treatment days/month) supports need for effective prophylaxis",
                    "CGRP pathway inhibition represents first mechanistically targeted migraine prevention",
                ],
            },
        ],
    },
    "I25.10": {
        "diagnosis": "Atherosclerotic heart disease of native coronary artery",
        "chart_signals": [
            "Intermediate CAD risk profile documented",
            "Stress testing limitation or non-diagnostic result present",
            "Symptoms support chest pain evaluation pathway",
        ],
        "guidelines": [
            {
                "organization": "ACC/AHA",
                "title": "2021 Chest Pain: A Guideline for the Evaluation and Diagnosis of Chest Pain",
                "year": 2021,
                "recommendations": [
                    "CCTA is preferred for intermediate-risk patients who cannot perform exercise stress testing",
                    "Coronary artery calcium score guides risk stratification and imaging decisions",
                    "CCTA has class I recommendation (Level A evidence) for intermediate pre-test probability CAD",
                    "CCTA can rule out significant CAD with high negative predictive value, avoiding invasive procedures",
                ],
            },
            {
                "organization": "SCCT",
                "title": "Society of Cardiovascular CT Appropriate Use Criteria for Cardiac CT",
                "year": 2022,
                "recommendations": [
                    "CCTA is appropriate for symptomatic patients with intermediate pre-test probability",
                    "Non-diagnostic pharmacologic stress test supports CCTA indication",
                    "CCTA provides anatomic assessment superior to functional stress testing for plaque characterization",
                    "Results directly guide revascularization decisions and risk factor management",
                ],
            },
        ],
    },
    "M54.5": {
        "diagnosis": "Low back pain, unspecified",
        "chart_signals": [
            "Persistent radicular or red-flag symptoms documented",
            "Physical exam supports nerve root involvement",
            "Conservative therapy failure is described with duration",
        ],
        "guidelines": [
            {
                "organization": "ACP",
                "title": "Noninvasive Treatments for Acute, Subacute, and Chronic Low Back Pain: ACP Clinical Practice Guideline",
                "year": 2022,
                "recommendations": [
                    "Imaging indicated for red flags: progressive neurological deficit, bowel/bladder dysfunction",
                    "MRI preferred over CT for evaluation of soft tissue, disc pathology, and nerve compression",
                    "Imaging after 6 weeks of conservative treatment failure is appropriate for radicular symptoms",
                    "Positive straight leg raise and dermatomal sensory deficit indicate nerve root involvement",
                ],
            },
            {
                "organization": "NASS",
                "title": "Evidence-Based Clinical Guidelines for Multidisciplinary Spine Care",
                "year": 2023,
                "recommendations": [
                    "MRI without contrast is the imaging modality of choice for lumbar radiculopathy",
                    "Progressive neurological symptoms are an urgent indication for MRI",
                    "Clinical correlation with imaging essential: disc herniation common in asymptomatic patients",
                    "MRI findings guide surgical planning and epidural steroid injection level selection",
                ],
            },
        ],
    },
}


def get_policy_rules(cpt_code: str) -> dict:
    """Get policy rules for a CPT code."""
    return POLICY_RULES.get(cpt_code, {})


def get_clinical_guidelines(icd10_code: str) -> dict:
    """Get clinical guidelines for an ICD-10 diagnosis code."""
    return CLINICAL_GUIDELINES.get(icd10_code, {})


def get_all_cpt_codes() -> list:
    """Get all CPT codes in the knowledge base."""
    return list(POLICY_RULES.keys())


def get_all_icd10_codes() -> list:
    """Get all ICD-10 codes in the knowledge base."""
    return list(CLINICAL_GUIDELINES.keys())
