from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from collections import deque

from app.services.access_policy import (
    describe_access,
    describe_restricted_access,
    has_module_access,
    normalize_role,
)
from app.services.llm_service import classify_query, format_answer, generate_answer, refine_question, try_direct_answer
from app.services.smart_query_service import get_relevant_templates, execute_smart_query
from app.services.embedder import get_embedding
from app.services.qdrant_service import search_data_filtered
from app.services.query_registry import select_query_and_extract_params, validate_parameters
from app.services.sql_builder import build_and_execute_fallback
from app.services.response_mode_service import detect_response_mode
from app.services.report_service import generate_report, get_report_ttl
from app.services.action_intent_service import detect_action_intent
from app.services.action_field_extractor import extract_action_fields
from app.services.action_confirmation_service import create_confirmation
from app.services.action_permission_service import can_execute_action

router = APIRouter()

# Conversation history store: keyed by office_id, stores last 2 exchanges
# Each exchange = {"question": str, "answer": str}
conversation_history: dict[int, deque] = {}

# Sensitive/internal columns that should NEVER be exposed to users
_SENSITIVE_COLUMNS = {
    'id', 'user_id', 'trainee_id', 'tra_master_id', 'office_id', 'hostel_master_id',
    'application_id', 'exam_id', 'subject_id', 'course_id', 'ct_id', 'building_id',
    'room_id', 'complaint_id', 'feedback_id', 'schedule_id', 'template_id',
    'created_by', 'updated_by', 'password', 'hrms_id', 'aadhar', 'uan', 'pf_no',
    'bank_id', 'bank_acc', 'ifsc_code', 'android_id', 'permanent_identity',
    'pass_file', 'user_log', 'room_log', 'attachment', 'signature', 'photo',
    'emergency_numbers', 'office_mobile', 'emg_mobile_no', 'whatsapp_number',
    'present_address', 'permanent_address', 'resi_address', 'city', 'email', 'office_email'
}


def _format_fallback_rows(rows: list, max_rows: int = 15) -> str:
    """Convert SQL result rows (list of dicts) into a readable text context."""
    if not rows:
        return "No data found."
    
    # If it is a single row with a single column (usually a COUNT, SUM, AVG, etc.)
    if len(rows) == 1 and len(rows[0]) == 1:
        k = list(rows[0].keys())[0]
        v = rows[0][k]
        val = "N/A" if v is None else str(v)
        return f"{k}: {val}"

    limited = rows[:max_rows]
    lines = []
    for i, row in enumerate(limited, 1):
        # Filter out sensitive/internal columns and format nicely
        parts = []
        for k, v in row.items():
            if k.lower() not in _SENSITIVE_COLUMNS and v is not None and str(v).strip() != "":
                # Format the key nicely (snake_case -> Title Case)
                label = k.replace('_', ' ').title()
                parts.append(f"{label}: {str(v)}")
        if parts:
            lines.append(f"{i}. " + " | ".join(parts))
    summary = f"Total: {len(rows)} record(s)" + (f" (showing first {max_rows})" if len(rows) > max_rows else "")
    return summary + "\n" + "\n".join(lines)


def _build_report_response(
    report: dict,
    base_url: str,
    user_question: str,
    module_name: str = "data",
    total_count: int = None
) -> dict:
    """
    Build a response dict for report mode.
    
    Args:
        report: Report metadata from generate_report()
        base_url: Base URL for building full report URL
        user_question: Original user question
        module_name: Name of the module
        total_count: Optional actual total count to show when rows are limited
        
    Returns:
        Dict with answer, report_url, row_count, response_mode
    """
    # Build full URL
    full_url = base_url.rstrip("/") + report["url"]
    
    # Calculate expiry time display
    ttl_seconds = report["ttl_seconds"]
    if ttl_seconds < 60:
        expiry_text = f"{ttl_seconds} seconds"
    elif ttl_seconds < 3600:
        ttl_minutes = ttl_seconds // 60
        expiry_text = f"{ttl_minutes} minute{'s' if ttl_minutes != 1 else ''}"
    else:
        ttl_hours = ttl_seconds // 3600
        expiry_text = f"{ttl_hours} hour{'s' if ttl_hours != 1 else ''}"
    
    if total_count and total_count > report['row_count']:
        count_msg = f"Found {total_count} total records (showing {report['row_count']} in report)."
    else:
        count_msg = f"Found {report['row_count']} records for your request."
        
    # Build answer text with plain URL (frontend will auto-link)
    answer = (
        f"{count_msg}\n\n"
        f"Open full report: {full_url}\n\n"
        f"This report link will expire in {expiry_text}."
    )
    
    return {
        "type": "text",
        "message": answer,
        "report_url": full_url,
        "row_count": report["row_count"],
        "response_mode": "report",
        "expires_at": report["expires_at"]
    }


class ChatRequest(BaseModel):
    message: str
    role: str = "principal"
    office_id: int = 1
    session_id: str = None  # Optional session ID for report grouping
    selected_option: dict = None  # For guided flow button clicks


def _qdrant_fallback(question: str, office_id: int, user_role: str) -> str | None:
    """Search Qdrant for relevant context and generate an answer.
    Returns the answer string, or None if no relevant results found."""
    import re

    try:
        vector = get_embedding(question)
        results = search_data_filtered(
            vector=vector,
            office_id=office_id,
            user_role=user_role,
            limit=1000,
        )

        if not results:
            return None

        # Keyword-based reranking to solve Vector DB's exact-match flaw
        clean_q = re.sub(r"'s\b", "", question.lower())
        query_words = set(re.findall(r'\b\w{3,}\b', clean_q))

        def score_chunk(r):
            text = r.payload.get("text", "").lower()
            # Use word boundaries so "hey" doesn't match "Radhey"
            return sum(1 for w in query_words if re.search(r'\b' + re.escape(w) + r'\b', text))

        # Sort by keyword match score (descending), then original vector score
        results.sort(key=lambda r: (score_chunk(r), r.score), reverse=True)

        # Take only the top 5 most relevant chunks to prevent LLM context exhaustion (2048 tokens max)
        best_results = results[:5]

        # Check if top result is actually relevant (has keyword overlap)
        top_kw_score = score_chunk(best_results[0]) if best_results else 0
        top_vec_score = best_results[0].score if best_results else 0

        # If no keyword overlap AND low vector similarity, skip
        if top_kw_score == 0 and top_vec_score < 0.70:
            return None

        context = "\n".join([r.payload.get("text", "") for r in best_results])
        
        # Hard limit to ~1000 words to keep Qwen-1.5b safely under 2048 tokens
        if len(context) > 5000:
            context = context[:5000] + "..."
            
        return generate_answer(question, context)
    except Exception:
        return None


def _format_to_html(text: str) -> str:
    """Enforces HTML formatting for the frontend."""
    import re
    # If text already contains HTML table, preserve it as-is
    if '<table' in text.lower():
        return text
    # Convert markdown bold to HTML bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Convert markdown newlines/bullets to HTML breaks
    text = text.replace('\n- ', '<br><b>•</b> ')
    text = text.replace('\n', '<br>')
    # Fix double breaks
    text = text.replace('<br><br>', '<br>')
    return text

@router.post("/chat")
def chat(request: ChatRequest, http_request: Request = None):
    try:
        user_message = request.message.strip()
        # Prevent huge payloads from crashing the context window
        if len(user_message) > 500:
            user_message = user_message[:500]
            
        user_role = normalize_role(request.role)
        office_id = request.office_id
        session_id = request.session_id
        
        # Get base URL for building report links
        base_url = "http://localhost:8000"
        if http_request:
            base_url = str(http_request.base_url).rstrip("/")

        # Generate a unique history key if session_id is missing to prevent crossover
        hist_key = session_id if session_id else f"office_{office_id}_anon"

        # Get or create conversation history for this session
        if hist_key not in conversation_history:
            conversation_history[hist_key] = deque(maxlen=3)
        history = list(conversation_history[hist_key])

        def _add_suggestions(resp: dict) -> dict:
            if not resp or resp.get("type") != "text":
                return resp
            if "suggestions" in resp and resp["suggestions"]:
                return resp
            msg = resp.get("message", "")
            if not msg:
                return resp
            # Skip suggestions for simple requests for clarification
            if "Could you please clarify" in msg:
                return resp
            from app.services.llm_service import generate_suggested_followups
            sugs = generate_suggested_followups(user_message, msg)
            if sugs:
                resp["suggestions"] = sugs
            return resp

        # Helper to store exchange and return response
        def _respond(answer_text: str, extra_fields: dict = None) -> dict:
            conversation_history[hist_key].append({
                "question": user_message,
                "answer": answer_text
            })
            response = {"type": "text", "message": _format_to_html(answer_text)}
            if extra_fields:
                response.update(extra_fields)
            return _add_suggestions(response)
        
        # Helper to process fallback results with report support
        def _process_fallback_result(fallback_result: dict, module_name: str) -> dict:
            """Process SQL fallback result, generating report if needed."""
            row_count = fallback_result.get("row_count", 0)
            rows = fallback_result.get("rows", [])
            
            if row_count == 0:
                return None  # No results
            
            # Detect response mode
            mode = detect_response_mode(
                user_question=user_message,
                result_type="list" if row_count > 1 else "single",
                row_count=row_count
            )
            
            print(f"[Chat] Response mode for {module_name}: {mode} (rows: {row_count})")
            
            if mode == "report" and row_count > 1:
                # Generate report
                report = generate_report(
                    module_name=module_name,
                    title=f"{module_name.title()} Report",
                    user_question=user_message,
                    rows=rows,
                    office_id=office_id,
                    session_id=session_id
                )
                return _add_suggestions(_build_report_response(report, base_url, user_message, module_name))
            else:
                # Return chat format - use LLM to format the response into a conversational sentence
                formatted_text = _format_fallback_rows(rows)
                # Pass the raw text to the LLM to generate a natural language response
                response_text = format_answer(user_message, formatted_text)
                return _respond(response_text)


        # Prioritize active guided flow session or button option clicks
        from app.services.conversation_state_service import get_state
        has_active_guided_flow = get_state(session_id) is not None if session_id else False

        if request.selected_option or has_active_guided_flow:
            from app.services.guided_flow_service import handle_guided_flow
            guided_result = handle_guided_flow(
                message=user_message,
                role=user_role,
                office_id=office_id,
                session_id=session_id or str(office_id),
                selected_option=request.selected_option,
                base_url=base_url,
            )
            if guided_result is not None:
                if guided_result.get("type") == "text" and "message" in guided_result:
                    guided_result["message"] = _format_to_html(guided_result["message"])
                    conversation_history[hist_key].append({
                        "question": user_message,
                        "answer": guided_result["message"]
                    })
                return _add_suggestions(guided_result)

        # ── Pre-screen: catch obvious nonsense before wasting LLM calls ──
        import re as _re
        _msg_stripped = user_message.strip()
        _is_pure_junk = False
        # Pure math/symbols (e.g. "1-1", "2+2", "!!@@", "###")
        if _re.fullmatch(r'[\d\s\+\-\*\/\=\(\)\^\%\.\!\?\@\#\$\&\~\`\|\<\>\{\}\[\]\_\,\;]+', _msg_stripped):
            _is_pure_junk = True
        # Very short with no alpha (e.g. "1-1", "?!")
        elif len(_re.findall(r'[a-zA-Z]', _msg_stripped)) < 2 and len(_msg_stripped) <= 10:
            _is_pure_junk = True
        if _is_pure_junk:
            return _respond("I'm the TRMS AI Assistant! I can help you with training management queries like trainee details, exam results, hostel info, attendance, and more. How can I help you?")

        # ── Hardcoded security blocker: catch attempts to extract DB/system internals ──
        _msg_lower = user_message.lower()
        _BLOCKED_PATTERNS = [
            # Database schema probing
            r"\b(table|tables)\b.*\b(name|list|show|all|column|schema|structure|database|db)\b",
            r"\b(column|columns)\b.*\b(name|list|show|all|table|schema|database|db)\b",
            r"\b(database|db)\b.*\b(schema|structure|table|column|name|list|show|design|model|erd)\b",
            r"\b(schema|structure|erd|entity)\b.*\b(database|db|table|column|show|list|diagram)\b",
            r"\bshow\b.*\b(tables|columns|schema|database|db\s+structure)\b",
            r"\blist\b.*\b(tables|columns|schema|database|db\s+structure)\b",
            r"\bdescribe\b.*\b(table|database|schema)\b",
            # SQL injection / raw SQL attempts
            r"\b(select|insert|update|delete|drop|alter|create|truncate|exec|execute)\b.*\b(from|into|table|where|set)\b",
            r"\binformation_schema\b",
            r"\bsys\.(tables|columns|objects)\b",
            r"\bpg_catalog\b",
            r"\bsqlite_master\b",
            # API / system internals
            r"\b(api|endpoint|route|url)\b.*\b(list|show|all|structure|internal)\b",
            r"\b(source\s*code|backend|server\s*config|env|environment\s*variable|\.env)\b",
            r"\b(password|secret|key|token|credential)\b.*\b(show|list|tell|what|give)\b",
            # Primary key / foreign key probing
            r"\b(primary\s*key|foreign\s*key|index|constraint)\b",
        ]
        if any(_re.search(pat, _msg_lower) for pat in _BLOCKED_PATTERNS):
            print(f"[Chat] BLOCKED security-sensitive question: '{user_message}'")
            return _respond("I'm the TRMS AI Assistant and I can only help with training management queries like trainee details, exam results, hostel info, attendance, complaints, and more. I cannot share database or system technical details. How can I help you with TRMS?")


        # New LLM Intent Router Integration
        from app.services.intent_router import route_intent
        intent_response = route_intent(user_message, history=history)

        if intent_response.intent_type == "unclear":
            return _respond("Could you please clarify what you are looking for?")

        # 1. Casual Chat
        if intent_response.intent_type == "casual_chat":
            direct = try_direct_answer(user_message)
            if direct:
                return _respond(direct)
            return _respond(generate_answer(user_message, ""))

        # 2. Try Guided Flow first for multiple potential data intents
        if intent_response.intent_type in ("guided_query", "report_query", "procedural_help", "action_query"):
            from app.services.guided_flow_service import handle_guided_flow
            guided_result = handle_guided_flow(
                message=user_message,
                role=user_role,
                office_id=office_id,
                session_id=session_id or str(office_id),
                selected_option=request.selected_option,
                base_url=base_url,
            )
            if guided_result is not None:
                if guided_result.get("type") == "text" and "message" in guided_result:
                    guided_result["message"] = _format_to_html(guided_result["message"])
                    conversation_history[hist_key].append({
                        "question": user_message,
                        "answer": guided_result["message"]
                    })
                return _add_suggestions(guided_result)

        # 3. Procedural Help (if Guided Flow didn't catch it)
        if intent_response.intent_type == "procedural_help" and not request.selected_option:
            print(f"[Chat] Procedural/Process question detected: '{user_message}'. Bypassing SQL pipeline to Qdrant/RAG...")
            refined = refine_question(user_message)
            qdrant_answer = _qdrant_fallback(refined, office_id, user_role)
            if qdrant_answer:
                return _respond(qdrant_answer)
            return _respond(generate_answer(refined, ""))

        # 4. Action Query (if Guided Flow didn't catch it)
        if intent_response.intent_type == "action_query":
            user_context = {"role": user_role, "office_id": office_id, "session_id": session_id}
            from app.services.langchain_agent_service import run_agentic_planner
            agent_result = run_agentic_planner(user_message, user_context)
            
            if agent_result.get("handled"):
                del agent_result["handled"]
                if agent_result.get("type") == "text" and "message" in agent_result:
                    agent_result["message"] = _format_to_html(agent_result["message"])
                    conversation_history[hist_key].append({
                        "question": user_message,
                        "answer": agent_result["message"]
                    })
                return _add_suggestions(agent_result)

        # 5. Report / Data Query (fallback to SQL pipeline)

        # --- Direct trainee selection handler (bypass AI) ---
        # If the previous answer was a TRAINEE_SELECT prompt and user clicked a name with Code
        if history:
            import re
            last_answer_raw = history[-1].get("answer", "")
            if "please select a course" in last_answer_raw.lower():
                # Extract course code (e.g. "(Code: HR-02(C))" -> "HR-02(C)")
                code_match = re.search(r'\(Code:\s*(.+)\)', user_message)
                if not code_match:
                    code_match = re.search(r'\b([A-Z0-9-/&]+)\b', user_message.upper())
                if code_match:
                    cs_code = code_match.group(1).strip()
                    result = execute_smart_query("COURSE_DETAILS_BY_NAME", {"cs_code": cs_code}, office_id)
                    if result and not result.startswith("Error"):
                        if result.strip().startswith("<") and "<table" in result.lower():
                            return _respond(result)
                        formatted = format_answer(f"details for course {cs_code}", result)
                        return _respond(formatted)
                        
            elif "please select one" in last_answer_raw.lower():
                # Try to extract user_code first (e.g. "Alpa Mayank Talati (Code: U00939)" or just "U00939")
                code_match = re.search(r'\b([A-Z]\d{3,})\b', user_message.upper())
                if code_match:
                    user_code = code_match.group(1)
                    result = execute_smart_query("MARKS_OF_ONE_TRAINEE", {"user_code": user_code}, office_id)
                    if result and not result.startswith("Error"):
                        # If result contains HTML table, bypass format_answer to preserve it
                        if result.strip().startswith("<") and "<table" in result.lower():
                            return _respond(result)
                        formatted = format_answer(f"exam marks for trainee code {user_code}", result)
                        return _respond(formatted)
                # Fallback: try to extract numeric trainee_id
                id_match = re.search(r'\b(\d+)\b', user_message)
                if id_match:
                    trainee_id = int(id_match.group(1))
                    result = execute_smart_query("MARKS_OF_ONE_TRAINEE", {"trainee_id": trainee_id}, office_id)
                    if result and not result.startswith("Error"):
                        # If result contains HTML table, bypass format_answer to preserve it
                        if result.strip().startswith("<") and "<table" in result.lower():
                            return _respond(result)
                        formatted = format_answer(f"exam marks for trainee ID {trainee_id}", result)
                        return _respond(formatted)


        # --- Data question: 3-stage LLM pipeline ---


        # Access control check BEFORE calling LLM
        module = intent_response.module.lower() if intent_response.module else ""
        if module == "exam" and not has_module_access(user_role, "exam"):
            return {"type": "text", "message": "You do not have permission to access exam data."}
        if module == "hostel" and not has_module_access(user_role, "hostel"):
            return {"type": "text", "message": "You do not have permission to access hostel data."}


        # Stage 1: Refine question (spell correct + clarify)
        refined = refine_question(user_message)

        # Stage 2: Classify query + extract params (with conversation history)
        qid, params, confidence = select_query_and_extract_params(refined, intent_response.module, history)

        if qid and qid != "NONE":
            # Stage 2.1: Validate Required Parameters
            missing_params = validate_parameters(qid, params)
            if missing_params:
                # If required parameters are missing, prompt the user for them
                missing_str = ", ".join(missing_params)
                return _respond(f"Could you please specify the following missing information: {missing_str}?")
                
            if confidence < 0.70:
                # Force clarification for low confidence matches to prevent hallucination
                return _respond("I'm not completely sure what you're asking. Could you please clarify your request?")

        if qid and qid != "NONE":
            print(f"[Chat] Trying predefined query...")
            print(f"[Chat] Predefined query found: {qid}")
            # Stage 2.5: Execute SQL
            result = execute_smart_query(qid, params, office_id)

            if result and not result.startswith("Error"):
                # Check if the result is a trainee selection prompt (multiple matches)
                if result.startswith("TRAINEE_SELECT\n"):
                    trainee_text = result.replace("TRAINEE_SELECT\n", "")
                    options = [line[2:].strip() for line in trainee_text.split("\n") if line.startswith("- ")]
                    return _respond(trainee_text, extra_fields={"suggestions": options})
                    
                if result.startswith("COURSE_SELECT\n"):
                    course_text = result.replace("COURSE_SELECT\n", "")
                    options = [line[2:].strip() for line in course_text.split("\n") if line.startswith("- ")]
                    return _respond(course_text, extra_fields={"suggestions": options})

                # If result already contains HTML (like tables), skip LLM formatting to preserve it
                if result.strip().startswith("<") and "<table" in result.lower():
                    return _respond(result)

                # Check if this should be a report (list-type queries with multiple rows)
                # User asked for "list" and result has many lines -> generate report
                result_lines = [l for l in result.strip().split('\n') if l.strip()]
                is_list_query = "list" in user_message.lower() or "show" in user_message.lower()
                has_many_results = len(result_lines) > 3
                
                if is_list_query and has_many_results and detect_response_mode(user_message, result_type="list", row_count=len(result_lines)) == "report":
                    # Convert formatted text lines to structured rows for report
                    rows = []
                    extracted_total = None
                    import re
                    
                    for line in result_lines:
                        clean_line = line.strip()
                        
                        m = re.search(r"Total:?\s*(\d+)", clean_line, re.IGNORECASE)
                        if m:
                            extracted_total = int(m.group(1))
                            
                        # Skip header, title, or summary lines
                        if clean_line.endswith(":") or clean_line.lower().startswith("total"):
                            continue
                        if '|' in line:
                            # Parse structured lines like "ID:10971 | GEETANJALEE | Room 4"
                            parts = line.replace('• ', '').replace('- ', '').split('|')
                            row = {f"Column {i+1}": p.strip() for i, p in enumerate(parts)}
                            rows.append(row)
                        else:
                            rows.append({"Info": line.replace('• ', '').replace('- ', '').strip()})
                    
                    if rows:
                        module = qid.split('_')[0].lower() if '_' in qid else "data"
                        report = generate_report(
                            module_name=module,
                            title=f"Report",
                            user_question=user_message,
                            rows=rows,
                            office_id=office_id,
                            session_id=session_id
                        )
                        return _build_report_response(report, base_url, user_message, module, total_count=extracted_total)

                # Stage 3: LLM formats the answer
                formatted = format_answer(refined, result)

                # Only enrich with Qdrant for specific trainee profile queries where SQL data might be shallow
                if qid in ("HOSTEL_TRAINEE_DETAILS", "HOSTEL_SEARCH_TRAINEE_BY_NAME") and len(formatted) <= 80:
                    qdrant_answer = _qdrant_fallback(refined, office_id, user_role)
                    if qdrant_answer and len(qdrant_answer) > len(formatted):
                        return _respond(qdrant_answer)
                
                return _respond(formatted)

        # --- Module-specific SQL Fallback ---
        print(f"[Chat] No predefined query found. Checking template fallback...")
        
        fallback = build_and_execute_fallback(intent_response.module, intent_response.operation, params, office_id)
        if fallback.get("row_count", -1) >= 0:
            result = _process_fallback_result(fallback, intent_response.module or "data")
            if result:
                return result
        elif fallback.get("error"):
            print(f"[Chat] Template SQL fallback error: {fallback['error']}")

        # --- Fallback: Vector search (Qdrant) ---
        qdrant_answer = _qdrant_fallback(refined, office_id, user_role)
        if qdrant_answer:
            return _respond(qdrant_answer)

        # --- Final fallback: LLM with no context ---
        return _respond(generate_answer(refined, ""))

    except HTTPException as exc:
        return {"type": "text", "message": f"Error: {exc.detail if hasattr(exc, 'detail') else str(exc)}"}
    except Exception as exc:
        import traceback; traceback.print_exc(); return {"type": "text", "message": f"Error: {exc}"}