"""
Central configuration for PriorAuth AI.
All agents, tools, and API calls import from here.
"""

import os

from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)


def _get_int_env(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


def _get_float_env(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


# Provider / model configuration
API_KEY = os.getenv("API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("OPENROUTER_API_KEY", "")
API_BASE_URL = os.getenv("API_BASE_URL") or os.getenv("OPENROUTER_BASE_URL", "https://api.mistral.ai/v1")
MODEL = os.getenv("MODEL") or os.getenv("FREE_MODEL") or os.getenv("STRONG_MODEL") or "mistral-small-latest"


# Per-agent token and timeout limits
AGENT_CONFIGS = {
    "policy_engine": {
        "max_tokens": 1500,
        "timeout": 90,
        "max_retries": 2,
        "model": MODEL,
    },
    "case_intelligence": {
        "max_tokens": 4000,
        "timeout": 240,
        "max_retries": 2,
        "model": MODEL,
    },
    "submission_tracker": {
        "max_tokens": 1500,
        "timeout": 90,
        "max_retries": 2,
        "model": MODEL,
    },
}


AGENT_SYSTEM_PROMPTS = {
    "policy_engine": (
        "You are the Policy & Requirements Engine for a healthcare prior authorization platform. "
        "Your job is to review payer criteria, required documentation, and utilization management requirements. "
        "Be conservative, precise, and clinically literate. Ground your answer in the supplied case facts and local policy baseline only. "
        "Do not invent payer rules. If evidence is incomplete, mark it as review required rather than assuming it is met. "
        "Return valid JSON only and preserve the requested schema exactly."
    ),
    "case_intelligence": (
        "You are the Case Intelligence Engine for a healthcare prior authorization platform. "
        "Your job is to assess medical necessity, identify strengths and risks, and draft an insurer-ready justification letter. "
        "Write like an experienced utilization management clinician: specific, evidence-based, and aligned to the supplied policy and guideline context. "
        "Use only the provided case details, policy output, and local baseline. Do not fabricate treatments, dates, labs, or guideline citations. "
        "The medical necessity letter must sound submission-ready, professional, and payer-facing. "
        "Use clean business-letter formatting with short paragraphs. Start with 'To the Medical Director,' and end with 'Sincerely,' followed by the requesting provider name only. "
        "Do not sign the letter with the model name, agent name, placeholders, or bracketed text. "
        "If the case is not fully supportable, say so clearly and explain what documentation is still required before approval. "
        "Return valid JSON only and preserve the requested schema exactly."
    ),
    "submission_tracker": (
        "You are the Submission & Tracker agent for a healthcare prior authorization platform. "
        "Your job is to prepare a clean submission package, identify real missing fields, and produce operational follow-up guidance. "
        "Assume the doctor-approved letter is authoritative. Prefer completeness and operational clarity over creative writing. "
        "Do not mark fields missing if they are present in the provided case context or local baseline. "
        "Follow-up schedules should be realistic for payer operations and internal clinical review. "
        "Return valid JSON only and preserve the requested schema exactly."
    ),
}


# Pipeline settings
PIPELINE_TIMEOUT = _get_int_env("PIPELINE_TIMEOUT", 480)
MANUAL_BENCHMARK_SECONDS = _get_int_env("MANUAL_BENCHMARK_SECONDS", 2700)


# Response cache
RESPONSE_CACHE_TTL = _get_int_env("RESPONSE_CACHE_TTL", 3600)


# Cost estimation
COST_PER_1M_TOKENS = _get_float_env("COST_PER_1M_TOKENS", 0.10)
AVG_TOKENS_PER_AGENT = _get_int_env("AVG_TOKENS_PER_AGENT", 1500)
