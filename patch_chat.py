import re

with open("app/routes/chat.py", "r") as f:
    content = f.read()

# 1. Update imports
import_old = """from app.services.sql_fallback_service import (
    run_exam_sql_fallback, run_trainee_sql_fallback, run_hostel_sql_fallback, run_course_sql_fallback,
    run_attendance_sql_fallback, run_timetable_sql_fallback, run_faculty_vl_sql_fallback,
    run_feedback_sql_fallback, run_complaint_sql_fallback, run_library_sql_fallback,
    run_mess_sql_fallback, run_vehicle_sql_fallback, run_meeting_sql_fallback,
    run_seminar_sql_fallback, run_inspection_sql_fallback, run_sports_sql_fallback,
    run_pass_eq_sql_fallback, run_field_study_tour_sql_fallback, run_master_admin_sql_fallback
)
from app.services.response_mode_service import detect_response_mode"""

import_new = """from app.services.query_registry import select_query_and_extract_params, validate_parameters
from app.services.sql_builder import build_and_execute_fallback
from app.services.response_mode_service import detect_response_mode"""

content = content.replace(import_old, import_new)

# 2. Update logic
logic_old_pattern = r"# Stage 1: Refine question \(spell correct \+ clarify\).*?# Fallback to Qdrant if all SQL attempts failed"

logic_new = """# Stage 1: Refine question (spell correct + clarify)
        refined = refine_question(user_message)

        # Stage 2: Query Registry Match & Parameter Extraction
        qid, params, confidence = select_query_and_extract_params(refined, module_hint=module, history=history)

        # Accuracy Scoring Layer: Handle Low Confidence
        if confidence < 0.70 or qid == "NONE":
            print(f"[Chat] Low confidence ({confidence}) or no query match. Triggering clarification or structured fallback.")
            
            # 3. Strict Fallback Architecture: use SQL Builder with (module, operation, slots)
            if intent_response.module and intent_response.operation:
                fallback = build_and_execute_fallback(intent_response.module, intent_response.operation, intent_response.slots, office_id)
                if fallback and fallback.get("row_count", -1) > 0:
                    result = _process_fallback_result(fallback, intent_response.module)
                    if result:
                        return result
                        
            return _respond(f"I couldn't confidently determine exactly what you're looking for. Could you please clarify your question?")

        # Required Parameter Validation Layer
        missing = validate_parameters(qid, params)
        if missing:
            print(f"[Chat] Missing required parameters: {missing}")
            missing_str = ", ".join(missing).replace("_", " ").title()
            return _respond(f"Could you please specify the {missing_str}?", extra_fields={
                "type": "clarification",
                "missing_params": missing
            })

        print(f"[Chat] Predefined query found: {qid} (Confidence: {confidence})")
        
        # Stage 2.5: Execute SQL
        result = execute_smart_query(qid, params, office_id)

        if result and not result.startswith("Error"):
            # Check if the result is a trainee selection prompt (multiple matches)
            if result.startswith("TRAINEE_SELECT\\n"):
                trainee_text = result.replace("TRAINEE_SELECT\\n", "")
                return _respond(trainee_text)

            # If result already contains HTML (like tables), skip LLM formatting to preserve it
            if result.strip().startswith("<") and "<table" in result.lower():
                return _respond(result)

            # Check if this should be a report (list-type queries with multiple rows)
            # User asked for "list" and result has many lines -> generate report
            result_lines = [l for l in result.strip().split('\\n') if l.strip()]
            is_list_query = "list" in user_message.lower() or "show" in user_message.lower()
            has_many_results = len(result_lines) > 3
            
            if is_list_query and has_many_results and detect_response_mode(user_message, result_type="list", row_count=len(result_lines)) == "report":
                # Convert formatted text lines to structured rows for report
                rows = []
                for line in result_lines:
                    if '|' in line:
                        # Parse structured lines like "ID:10971 | GEETANJALEE | Room 4"
                        parts = line.replace('• ', '').replace('- ', '').split('|')
                        row = {f"Column {i+1}": p.strip() for i, p in enumerate(parts)}
                        rows.append(row)
                    else:
                        rows.append({"Info": line.replace('• ', '').replace('- ', '').strip()})
                
                if rows:
                    report_module = qid.split('_')[0].lower() if '_' in qid else "data"
                    report = generate_report(
                        module_name=report_module,
                        title=f"Report",
                        user_question=user_message,
                        rows=rows,
                        office_id=office_id,
                        session_id=session_id
                    )
                    return _build_report_response(report, base_url, user_message, report_module)

            # Stage 3: LLM formats the answer
            formatted = format_answer(refined, result)

            # Only enrich with Qdrant for specific trainee profile queries where SQL data might be shallow
            if qid in ("HOSTEL_TRAINEE_DETAILS", "HOSTEL_SEARCH_TRAINEE_BY_NAME") and len(formatted) <= 80:
                qdrant_answer = _qdrant_fallback(refined, office_id, user_role)
                if qdrant_answer and len(qdrant_answer) > len(formatted):
                    return _respond(qdrant_answer)
            
            return _respond(formatted)
            
        # If execution fails or no result
        return _respond("No records found. Could you please clarify or check if the parameters are correct?")

        # Fallback to Qdrant if all database attempts failed"""

content = re.sub(logic_old_pattern, logic_new, content, flags=re.DOTALL)

with open("app/routes/chat.py", "w") as f:
    f.write(content)
