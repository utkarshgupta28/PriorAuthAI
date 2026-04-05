"""
CMS database helpers for prior authorization rules and timeframes.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.cms_real_data import (
    STATS,
    get_documentation_requirements,
    get_new_2026_codes,
    get_regulatory_rules,
    lookup_cms_pa_requirement,
    search_pa_codes,
)


def cms_search_tool(search_term: str) -> str:
    search_term = search_term.strip().strip("'\"")

    result = lookup_cms_pa_requirement(search_term.upper())
    if result["found"]:
        data = result["data"]
        return (
            f"=== CMS PA REQUIREMENT: {search_term.upper()} ===\n"
            f"Description: {data['description']}\n"
            f"Category: {data['category']}\n"
            f"Program: {data['program']}\n"
            f"Effective Date: {data['effective_date']}\n"
            f"Status: REQUIRES PRIOR AUTHORIZATION under CMS Medicare program\n\n"
            f"Note: This code is on the official CMS prior authorization list. "
            f"Medicare Advantage plans and applicable Medicaid programs must process "
            f"PA decisions within 7 calendar days (standard) or 72 hours (expedited) per CMS-0057-F."
        )

    matches = search_pa_codes(search_term)
    if matches:
        lines = [
            f"=== CMS PA CODE SEARCH: '{search_term}' ===",
            f"Found {len(matches)} matching codes:\n",
        ]
        for match in matches[:10]:
            lines.append(f"  [{match['program']}] {match['code']}: {match['description'][:80]}...")
        if len(matches) > 10:
            lines.append(f"  ... and {len(matches) - 10} more results")
        lines += [
            "",
            f"Database contains {STATS['total_codes_in_database']} total PA codes "
            f"({STATS['dmepos_codes']} DMEPOS, {STATS['opd_codes']} OPD).",
        ]
        return "\n".join(lines)

    return (
        f"No CMS PA codes found matching '{search_term}'.\n"
        f"The CMS mandatory PA list covers DMEPOS and selected OPD services.\n"
        f"For clinical procedures like 27447, 96413, and 72148, commercial plan policies still control authorization requirements."
    )


def cms_regulatory_tool(query: str) -> str:
    rules = get_regulatory_rules()
    doc_reqs = get_documentation_requirements()
    new_codes = get_new_2026_codes()

    lines = [
        "=== CMS PRIOR AUTHORIZATION REGULATORY REQUIREMENTS ===",
        f"Rule: {rules['rule']}",
        f"Effective Date: {rules['effective_date']}",
        f"PA API Deadline: {rules['api_deadline']}",
        "",
        "DECISION TIMEFRAMES:",
        f"  Standard decisions: {rules['standard_decision_timeframe']}",
        f"  Expedited decisions: {rules['expedited_decision_timeframe']}",
        "",
        "AFFECTED PAYERS:",
    ]
    for payer in rules["affected_payers"]:
        lines.append(f"  - {payer}")

    lines += [
        "",
        "KEY PROVISIONS:",
    ]
    for provision in rules["key_provisions"]:
        lines.append(f"  - {provision}")

    lines += [
        "",
        "REQUIRED PUBLIC REPORTING METRICS:",
    ]
    for metric in rules["required_public_metrics"]:
        lines.append(f"  - {metric}")

    lines += [
        "",
        f"DMEPOS DOCUMENTATION REQUIREMENTS ({doc_reqs['source']}):",
    ]
    for req in doc_reqs["requirements"]:
        lines.append(f"  - {req}")

    lines += [
        "",
        f"NEW CODES EFFECTIVE APRIL 13, 2026 ({len(new_codes)} codes):",
    ]
    for code, data in new_codes.items():
        lines.append(f"  {code}: {data['description'][:70]}...")

    lines += [
        "",
        "INDUSTRY STATISTICS:",
        f"  - AMA Survey: {STATS['ama_survey_pa_requests_per_physician_per_week']} PA requests per physician per week",
        f"  - CAQH Estimate: ${STATS['caqh_annual_cost_billions']}B annual PA processing cost",
        f"  - Average cost per manual PA: ${STATS['caqh_cost_per_manual_pa']}",
        f"  - AMA Benchmark: {STATS['ama_benchmark_manual_pa_minutes']} minutes per manual PA",
    ]
    return "\n".join(lines)
