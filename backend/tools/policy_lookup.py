"""
Policy lookup helper for prior authorization requirements.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.policy_kb import get_all_cpt_codes, get_policy_rules


def policy_lookup_tool(cpt_code: str) -> str:
    cpt_code = cpt_code.strip().strip("'\"")

    rules = get_policy_rules(cpt_code)
    if not rules:
        available = ", ".join(get_all_cpt_codes())
        return (
            f"CPT code {cpt_code} not found in policy knowledge base.\n"
            f"Available codes: {available}\n"
            f"For codes not in the KB, assume prior authorization is required by major commercial payers."
        )

    lines = [
        f"=== PRIOR AUTHORIZATION POLICY: CPT {cpt_code} ===",
        f"Procedure: {rules['procedure']}",
        f"Prior Auth Required: {'YES' if rules['requires_prior_auth'] else 'NO'}",
        f"Plans Requiring PA: {', '.join(rules['plans_requiring'])}",
        "",
        "APPROVAL CRITERIA:",
    ]
    for i, criterion in enumerate(rules["criteria"], 1):
        lines.append(f"  {i}. {criterion}")

    lines += [
        "",
        "REQUIRED DOCUMENTATION:",
    ]
    for i, doc in enumerate(rules["required_documentation"], 1):
        lines.append(f"  {i}. {doc}")

    lines += [
        "",
        f"Typical Turnaround: {rules['typical_turnaround']}",
        f"Historical Appeal Success Rate: {rules['appeal_success_rate']}",
    ]
    return "\n".join(lines)
