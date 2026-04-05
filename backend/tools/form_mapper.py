"""
Simplified prior authorization form mapping helper.
Aligned to the current hackathon submission draft UI.
"""

FORM_SECTIONS = {
    "provider_info": {
        "section_name": "Provider Information",
        "fields": [
            {"name": "provider_name", "label": "Provider Name", "required": True, "placeholder": ""},
            {"name": "provider_npi", "label": "Provider NPI", "required": True, "placeholder": "10-digit NPI"},
            {"name": "provider_phone", "label": "Provider Phone", "required": True, "placeholder": "(555) 555-5555"},
            {"name": "facility_name", "label": "Facility Name", "required": False, "placeholder": ""},
            {"name": "service_date_requested", "label": "Requested Service Date", "required": True, "placeholder": "MM/DD/YYYY"},
            {"name": "submission_method", "label": "Submission Method", "required": False, "placeholder": "Portal or fax"},
        ],
    },
    "clinical_info": {
        "section_name": "Clinical Request Information",
        "fields": [
            {"name": "insurance_id", "label": "Insurance Member ID", "required": True, "placeholder": ""},
            {"name": "diagnosis_code", "label": "Diagnosis Code", "required": True, "placeholder": "e.g. M17.11"},
            {"name": "diagnosis_description", "label": "Diagnosis Description", "required": False, "placeholder": ""},
            {"name": "cpt_code", "label": "CPT Code", "required": False, "placeholder": "e.g. 27447"},
            {"name": "procedure_description", "label": "Procedure Description", "required": True, "placeholder": ""},
            {"name": "clinical_summary", "label": "Clinical Summary", "required": True, "placeholder": "Brief case summary"},
        ],
    },
    "justification": {
        "section_name": "Medical Necessity and Review Notes",
        "fields": [
            {"name": "medical_necessity_letter", "label": "Justification Letter", "required": True, "placeholder": "Medical necessity letter"},
            {"name": "review_notes", "label": "Review Notes", "required": False, "placeholder": "Notes before submission"},
            {"name": "guidelines_cited", "label": "Guidelines Cited", "required": False, "placeholder": "Clinical guidelines referenced"},
            {"name": "supporting_findings", "label": "Supporting Findings", "required": False, "placeholder": "Imaging, labs, and objective findings"},
            {"name": "failed_treatments", "label": "Prior Treatments Documented", "required": False, "placeholder": "Conservative or prior therapies"},
        ],
    },
}


def form_mapper_tool(section: str) -> str:
    section = section.strip().strip("'\"").lower()

    if section == "all":
        sections_to_show = list(FORM_SECTIONS.keys())
    elif section in FORM_SECTIONS:
        sections_to_show = [section]
    else:
        available = ", ".join(list(FORM_SECTIONS.keys()) + ["all"])
        return (
            f"Section '{section}' not found.\n"
            f"Available sections: {available}\n"
            f"Use 'all' to get the complete form template."
        )

    lines = ["=== PRIOR AUTHORIZATION SUBMISSION TEMPLATE ===", ""]
    for sec_key in sections_to_show:
        sec = FORM_SECTIONS[sec_key]
        lines += [sec["section_name"], "-" * len(sec["section_name"])]
        for field in sec["fields"]:
            required_label = "[REQUIRED]" if field["required"] else "[optional]"
            lines.append(f"  {required_label} {field['label']}: {field['placeholder'] or '<fill in>'}")
        lines.append("")

    lines += [
        "COMPLETION GUIDANCE:",
        "- Complete all required fields before submission.",
        "- Keep the medical necessity letter aligned to the clinical summary and supporting findings.",
        "- Use payer-specific follow-up only after the doctor-approved draft is ready.",
    ]
    return "\n".join(lines)
