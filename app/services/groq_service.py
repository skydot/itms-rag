"""Backward-compatibility shim — Groq is no longer used.

All LLM calls are now routed through app.services.llm_service (OpenAI-compatible).
This file is kept only so that any stale imports do not break; it simply
re-exports the same functions from llm_service.

Do NOT add new logic here.  Import directly from llm_service instead.
"""

from app.services.llm_service import (  # noqa: F401
    call_llm,
    classify_query,
    refine_question,
    generate_answer,
    format_answer,
)