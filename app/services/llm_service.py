"""Generic OpenAI-compatible LLM service for TRMS chatbot.

All LLM calls are routed through call_llm().
Model and endpoint are configured via environment variables only —
no model name is hardcoded beyond the default fallback.

To switch models or endpoints, update .env:
    LLM_BASE_URL=http://<host>:<port>/v1
    LLM_MODEL=qwen2.5-14b          # or any OpenAI-compatible model
    LLM_API_KEY=<key>

Manual connectivity test:
    curl http://148.135.137.141:11434/v1/models

Chat completions test:
    curl http://148.135.137.141:11434/v1/chat/completions \\
      -H "Content-Type: application/json" \\
      -d '{
        "model": "qwen2.5-1.5b",
        "messages": [
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "Say hi"}
        ],
        "temperature": 0
      }'
"""

import os
import json
import logging

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration — read from env, never hardcode beyond these defaults
# ---------------------------------------------------------------------------

LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "http://148.135.137.141:11434/v1")
LLM_MODEL: str    = os.getenv("LLM_MODEL",    "qwen2.5-1.5b")
LLM_API_KEY: str  = os.getenv("LLM_API_KEY",  "ollama")

# Log config at import time (never log the API key)
print("[LLM] Base URL:", LLM_BASE_URL)
print("[LLM] Model:", LLM_MODEL)

_client = OpenAI(
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY,
)


# ---------------------------------------------------------------------------
# Core call — all other functions delegate here
# ---------------------------------------------------------------------------

def call_llm(
    messages: list,
    temperature: float = 0,
    max_tokens: int = 800,
    timeout: int = 60,
) -> str:
    """Call the configured OpenAI-compatible /chat/completions endpoint.

    Args:
        messages:    List of {"role": ..., "content": ...} dicts.
        temperature: Sampling temperature (0 = deterministic).
        max_tokens:  Maximum tokens in the response.
        timeout:     HTTP timeout in seconds.

    Returns:
        Response text string, or empty string on error.
    """
    try:
        response = _client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        # Log error without exposing the API key
        logger.error("[LLM] call_llm error (model=%s, base_url=%s): %s", LLM_MODEL, LLM_BASE_URL, e)
        raise


# ---------------------------------------------------------------------------
# High-level helpers (imported by chat.py and groq_service.py)
# ---------------------------------------------------------------------------

def classify_query(question: str, allowed_query_ids: list, history: list = None) -> dict:
    """Route a user question to the best matching predefined query ID.

    Returns:
        {"query_id": "<id>", "params": {...}} or {"query_id": "NONE", "params": {}}
    """
    import datetime

    current_year = datetime.datetime.now().year

    history_context = ""
    if history:
        history_lines = []
        for h in history:
            history_lines.append(f"User: {h['question']}")
            answer = h['answer'][:200] + "..." if len(h['answer']) > 200 else h['answer']
            history_lines.append(f"Assistant: {answer}")
        history_context = (
            f"\nConversation History (last {len(history)} exchange(s)):\n"
            + "\n".join(history_lines)
            + "\n"
        )

    prompt = f"""You are a query router for TRMS (TRAINING RESOURCE MANAGEMENT SYSTEM).
Current Date/Year Context: {datetime.datetime.now().strftime('%Y-%m-%d')}

Task: Choose exactly ONE query_id from the allowed list and extract parameters from the user's question.
IMPORTANT: If the user's current question is a follow-up or continuation of the conversation history, combine context from the history with the current question to determine the correct query_id and parameters. For example, if the previous question was "top performers" and the AI asked "which exam?" and the user now says "Transportation", extract course_name: "Transportation" and use the query_id from the previous context.

Allowed queries (each has id and description with expected params):
{json.dumps(allowed_query_ids)}

Return STRICT JSON ONLY:
{{"query_id": "...", "params": {{...}} }}
{history_context}
Parameter extraction rules:
- year: Extract any 4-digit year mentioned (e.g. "in 2025" → "year": 2025). Do NOT hallucinate a year if not explicitly stated, except when calculating relative to the current year.
- month: Extract month number (1-12) ONLY if a TEXT NAME of a month (like January, December) is explicitly used. NEVER extract this if the user says "last 12 months" or similar.
- start_month: Extract starting month number if a range is given (e.g. "between January..." -> 1).
- end_month: Extract ending month number if a range is given (e.g. "...to December" -> 12).
- last_months: Extract number of months if user says "last X months" (e.g. "last 4 months" -> 4, "last 12 months" -> 12).
- last_years: Extract number of years if user says "last X years" or "last year" (e.g. "last year" -> 1). NEVER extract this if the user uses the word "months".
- limit: Extract count if user says "top 5" or "top 20" etc (default 10)
- threshold_pct: Extract percentage if user says "below 50%" (default 40)
- search_name: Extract trainee name if mentioned
- building_name: Extract building/hostel name if mentioned
- room_name: Extract room number if mentioned
- gender: Extract "male" or "female" if mentioned
- trainee_id: Extract numeric ID if mentioned
- min_failures: Extract minimum failure count if mentioned (default 2)
- course_name: Extract ONLY the actual training course or program name if mentioned (e.g. "Establishment exam" -> "Establishment", "Cabinman course" -> "Cabinman"). NEVER extract generic words like "exam", "performers", "marks", "course", "top", "highest", "lowest" as course_name. If no specific course/program name is mentioned, do NOT include course_name at all.
- year1, year2: Extract two years for comparison queries

Rules:
1) Match if the user's intent clearly corresponds to the meaning. Even if the phrasing is different (e.g. "how many" vs "total"), pick the most relevant query_id. If the user asks for unstructured details NOT related to these queries (like "remarks", "building codes", "phone numbers", or broad "summaries"), you MUST return: {{"query_id": "NONE", "params": {{}}}}
2) If you are unsure, always default to {{"query_id": "NONE", "params": {{}}}}
3) Do NOT include explanations, only JSON.
4) Extract ALL relevant parameters from the question.

User question:
{question}
"""

    try:
        content = call_llm(
            messages=[
                {"role": "system", "content": "Return strict JSON only. No markdown. No explanation."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=200,
        )
        content = content.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            return {"query_id": "NONE", "params": {}}

        query_id = parsed.get("query_id")
        params   = parsed.get("params")

        allowed_set = set()
        for item in allowed_query_ids:
            if isinstance(item, dict):
                allowed_set.add(item.get("id"))
            else:
                allowed_set.add(item)

        if query_id not in allowed_set.union({"NONE"}):
            return {"query_id": "NONE", "params": {}}
        if not isinstance(params, dict):
            params = {}
        return {"query_id": query_id, "params": params}
    except Exception:
        return {"query_id": "NONE", "params": {}}


def refine_question(question: str) -> str:
    """Correct spelling and rewrite the question in standard English.

    Preserves original intent, numbers, names, and constraints.
    Returns the original question on any error.
    """
    prompt = f"""You are a text-only question refiner.

Task:
- Correct spelling and rewrite the question into a clear, standard English query.
- Preserve the original intent exactly.
- Keep all specific numbers, years, dates, names, and constraints mentioned in the original question.
- Do NOT add new constraints, names, numbers, years, or assumptions.
- Do NOT answer the question.

Output rules:
- Return ONLY the refined question as plain text.
- No quotes, no markdown, no explanations.

User question:
{question}

Refined question:
"""

    try:
        content = call_llm(
            messages=[
                {"role": "system", "content": "Return only the refined question as plain text."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=200,
        )
        return content.strip() or question
    except Exception:
        return question


def try_direct_answer(question: str) -> str | None:
    """LLM gate: decide if the question can be answered directly without any data lookup.

    Uses a small, fast prompt to ask the LLM:
    - Greetings, identity questions, small talk → answer directly
    - Questions needing TRMS data (trainees, exams, etc.) → return None so caller goes to RAG/Qdrant

    Returns:
        The direct answer string, or None if data lookup is needed.
    """
    system_msg = (
        "You are the TRMS AI Assistant chatbot. Your job is to decide:\n"
        "Can you answer this question directly, or does it need a database/document lookup?\n\n"
        "If you can answer it directly, JUST reply with your natural conversational answer. Do NOT prefix your answer with anything. Answer directly for:\n"
        "- Greetings (hi, hello, hey, good morning, etc.)\n"
        "- Identity questions (who are you, what are you, what can you do)\n"
        "- Small talk (how are you, thank you, bye, etc.)\n"
        "- General TRMS info (what is TRMS, what modules does TRMS have)\n\n"
        "If you need database/document data, SAY EXACTLY 'NEEDS_DATA' (nothing else) for:\n"
        "- Any question about specific trainees, exams, marks, hostels, rooms, courses, attendance, complaints, etc.\n"
        "- Any question that needs real numbers, names, counts, or records from a database\n"
        "- Any data query even if vaguely worded\n\n"
        "CRITICAL: NEVER invent or hallucinate any data like names, IDs, dates, numbers, or records.\n"
        "If in doubt, say NEEDS_DATA."
    )

    try:
        content = call_llm(
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user",   "content": question},
            ],
            temperature=0.3,
            max_tokens=200,
            timeout=15,
        )
        answer = (content or "").strip()

        # If the LLM decided it needs data, return None
        if "NEEDS_DATA" in answer.upper():
            print(f"[LLM Gate] '{question}' → NEEDS_DATA")
            return None

        # Safety net: if the answer contains suspicious data patterns, reject it
        import re
        # Reject if it mentions specific IDs, allocation IDs, or trainee records
        if re.search(r'\b(allocation|id|ID)\s*(is|for|of)\s*\d+', answer, re.IGNORECASE):
            print(f"[LLM Gate] '{question}' → Rejected (contains suspicious data pattern)")
            return None
        if re.search(r'\b\d{4,}\b', answer):  # 4+ digit numbers = likely DB IDs
            print(f"[LLM Gate] '{question}' → Rejected (contains large numbers)")
            return None

        print(f"[LLM Gate] '{question}' → Direct answer")
        return answer

    except Exception as e:
        print(f"[LLM Gate] Error: {e}")
        return None


def generate_answer(question: str, context: str) -> str:
    """Generate a conversational TRMS answer from Qdrant/RAG context.

    Uses two prompt modes depending on whether context has data:
    - Empty context  → simple conversational prompt (greetings, identity, general chat)
    - Has context    → strict data-only prompt (SQL/RAG results)

    Small models (1.5b–7b) cannot reliably follow "block off-topic BUT greet naturally"
    in a single complex prompt — they over-fire the domain restriction.
    Splitting into two modes solves this without hardcoding patterns.
    """
    import datetime

    has_data = bool(context and context.strip() and context.strip() != "No data found.")

    if not has_data:
        # ---------------------------------------------------------------
        # CONVERSATIONAL MODE — no data context
        # Simple prompt so small models can handle greetings naturally.
        # Only block clearly off-topic requests (coding, recipes, etc.).
        # ---------------------------------------------------------------
        system_msg = (
            "You are TRMS AI Assistant — a friendly chatbot for TRMS (Training Resource Management System), "
            "a software platform used by railway training centres in India to manage trainees, exams, "
            "hostels, attendance, courses, and reports. "
            "Answer greetings, small talk, and identity questions naturally and warmly. "
            "When asked 'who are you' or 'what are you', introduce yourself as the TRMS AI Assistant. "
            "If someone asks about TRMS data (trainees, exams, marks, hostels, courses, attendance) "
            "but you have no data available, say: \"I don't have that specific data available right now. "
            "Please try a more specific question.\" "
            "Only if the question is completely unrelated to TRMS and is not a greeting "
            "(e.g. coding homework, recipes, weather forecast), reply: "
            "\"I'm the TRMS AI Assistant and can only help with training management questions.\""
        )
        user_msg = question

        try:
            content = call_llm(
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user",   "content": user_msg},
                ],
                temperature=0.5,   # slightly warmer for natural conversation
                max_tokens=300,
            )
            return content.strip() or "Hello! How can I help you with TRMS today?"
        except Exception as e:
            return f"Error generating answer: {str(e)}"

    # ---------------------------------------------------------------
    # DATA MODE — context contains actual SQL/RAG results
    # Use the strict data prompt.
    # ---------------------------------------------------------------
    if len(context) > 14000:
        context = context[:14000] + "\n...[truncated]"

    prompt = f"""You are TRMS (TRAINING RESOURCE MANAGEMENT SYSTEM) AI Assistant. Give DIRECT, CONCISE answers based on the provided data.
Current Date/Year Context: {datetime.datetime.now().strftime('%Y-%m-%d')}

CRITICAL RULES:
1. ONLY use information explicitly in the Context below. DO NOT hallucinate numbers, names, or facts.
2. Count ONLY what is in the context — do not guess totals.
3. NEVER say "To find this..." or "Based on data..." — just answer directly.
4. FORMATTING IS CRITICAL: The frontend requires HTML. NEVER use markdown (** or -). Use <b> for keys (e.g., <b>Name:</b> Value). Use <br> for every line break.
5. Return ONLY the answer text. NEVER prefix with "Response:", "Answer:", or any label.
6. Start the answer immediately with the content.

Context:
{context}

User question:
{question}

Direct Answer:
"""

    try:
        content = call_llm(
            messages=[
                {"role": "system", "content": "You are a TRMS data assistant. Answer using only the provided context. Use HTML formatting."},
                {"role": "user",   "content": prompt},
            ],
            temperature=0.3,
            max_tokens=800,
        )
        return content.strip() or "I do not have access to that specific data at the moment."
    except Exception as e:
        return f"Error generating answer: {str(e)}"


def format_answer(question: str, result_context: str) -> str:
    """Format raw SQL result text into a natural-language TRMS response.

    Enforces HTML formatting rules required by the frontend.
    """
    if len(result_context) > 2500:
        result_context = result_context[:2500] + "\n...[truncated]"

    import datetime

    prompt = f"""You are TRMS (TRAINING RESOURCE MANAGEMENT SYSTEM) AI Assistant.
Current Date/Year Context: {datetime.datetime.now().strftime('%Y-%m-%d')}

You will be given a User question and a RESULT CONTEXT produced by SQL.

CRITICAL RULES:
1) Use ONLY the RESULT CONTEXT. Do not add any new facts.
2) Do NOT change numbers, names, dates, or counts. Repeat them exactly as in RESULT CONTEXT.
3) If RESULT CONTEXT indicates no data or counts are zero, just state that there are no records matching the criteria. NEVER invent or hallucinate a reason. NEVER filter records out based on the date or time (e.g. if the user asks for 'recent' or 'latest', treat all provided records as the correct recent ones).
4) Keep it concise but conversational.
5) Return ONLY the answer text. NEVER prefix the response with "Response:", "Answer:", or any other label.
6) Start the answer immediately with the content.
7) NEVER use introductory filler phrases like "Based on the RESULT CONTEXT" or "It appears that".
8) NEVER analyze the completeness of the data. If the RESULT CONTEXT contains ANY records matching the user's criteria, simply list them exactly as provided.
9) If the RESULT CONTEXT provides a 'Total' count AND a list, you MUST include BOTH the total count and the list in your final answer. Do NOT drop the count.
10) NEVER include internal database IDs like user_id, trainee_id, application_id, office_id, etc. Only show human-readable information like name, marks, course name, dates.
11) ALWAYS format the answer as a complete, natural sentence. NEVER output raw key-value pairs like 'student_count: 1319'. Instead, say 'There are 1,319 students whose names start with A.'

RESULT CONTEXT:
{result_context}

User question:
{question}

Final Answer:
"""

    try:
        content = call_llm(
            messages=[
                {"role": "system", "content": "Format the SQL result into a short user-facing TRMS answer. No new facts."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=800,
        )
        return content.strip() or result_context
    except Exception as e:
        return f"Error generating answer: {str(e)}"


def generate_suggested_followups(user_message: str, answer_message: str) -> list[str]:
    """Generate 3 contextual follow-up questions for the user based on the chat.
    
    Returns a list of 3 strings. If generation fails, returns an empty list.
    """
    prompt = f"""You are a suggestion engine for the TRMS AI Chatbot.
Based on the current conversation, suggest up to 3 short, relevant follow-up questions the user might want to ask next.

CRITICAL RULES:
1. ONLY suggest queries that a database can answer (e.g., about attendance, marks, hostels, courses, trainees, exams).
2. DO NOT suggest meta-questions about the chatbot itself, reports, expiration dates, links, or PDF downloads.
3. If the user asked about a specific person, suggest asking for their other details (e.g. if they asked for marks, suggest "What is their attendance?" or "Show their hostel details").
4. If the user just said "hi" or the topic is generic, suggest standard queries like: "Show top performers", "Available hostel rooms", "Recent exam results".
5. Keep suggestions under 6 words.
6. Return ONLY a JSON list of strings.

User question: {user_message}
Answer snippet: {answer_message[:300]}
"""
    try:
        content = call_llm(
            messages=[
                {"role": "system", "content": "Return strict JSON list of strings only."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
            max_tokens=100,
        )
        if not content:
            return []
        content = content.replace("```json", "").replace("```", "").strip()
        import json
        suggestions = json.loads(content)
        if isinstance(suggestions, list):
            return suggestions[:3]
        return []
    except Exception as e:
        logger.error(f"[Suggestions Error] {e}")
        return []
