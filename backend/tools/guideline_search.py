"""
Clinical guideline lookup helper for an ICD-10 code.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.policy_kb import get_all_icd10_codes, get_clinical_guidelines


def guideline_search_tool(diagnosis_code: str) -> str:
    diagnosis_code = diagnosis_code.strip().strip("'\"")

    guidelines_data = get_clinical_guidelines(diagnosis_code)
    if not guidelines_data:
        available = ", ".join(get_all_icd10_codes())
        return (
            f"ICD-10 code {diagnosis_code} not found in clinical guidelines database.\n"
            f"Available codes: {available}\n"
            f"Recommend using UpToDate, NCCN, or relevant specialty society guidelines for this diagnosis."
        )

    lines = [
        f"=== CLINICAL GUIDELINES: {diagnosis_code} - {guidelines_data['diagnosis']} ===",
        "",
    ]
    for gl in guidelines_data["guidelines"]:
        lines += [
            f"GUIDELINE: {gl['title']}",
            f"Organization: {gl['organization']} | Year: {gl['year']}",
            "Key Recommendations:",
        ]
        for i, rec in enumerate(gl["recommendations"], 1):
            lines.append(f"  {i}. {rec}")
        lines.append("")

    lines.append(
        "CITATION GUIDANCE: Cite these guidelines in the medical necessity letter by "
        "organization name, guideline title, and year to maximize credibility with insurance medical directors."
    )
    return "\n".join(lines)
