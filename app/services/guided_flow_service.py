"""Guided flow service — slot-filling layer that sits before SQL fallback.

Detects if user question matches a guided flow, manages multi-turn slot
collection with clickable option buttons, and executes final queries.

Returns None if no guided flow applies (old pipeline continues).
"""

import re
from typing import Optional, Dict

from app.services.conversation_state_service import (
    create_or_update_state, get_state, clear_state, update_slot,
)
from app.services.option_resolver_service import (
    search_trainees_by_name,
    get_courses_for_trainee,
    get_exam_types_for_trainee_course,
    get_recent_courses_for_exam,
    get_exam_types_for_course,
    get_subjects_for_course,
    get_dues_type_options,
    get_hostel_records_for_trainee,
    get_buildings,
)
from app.services.guided_query_executor import execute_guided_query


# ═══════════════════════════════════════════════════════════════════
# Flow definitions
# ═══════════════════════════════════════════════════════════════════

GUIDED_FLOWS = {
    # ── Trainee-specific exam flows ──
    "exam_marks_by_trainee": {
        "module": "exam",
        "requires_name": True,
        "slots_order": ["user_id", "course_id", "exam_type_id"],
    },
    "exam_result_by_trainee": {
        "module": "exam",
        "requires_name": True,
        "slots_order": ["user_id", "course_id", "exam_type_id"],
    },
    # ── Non-trainee exam flows ──
    "failed_trainees": {
        "module": "exam",
        "requires_name": False,
        "slots_order": ["course_id"],
    },
    "failed_trainees_by_subject": {
        "module": "exam",
        "requires_name": False,
        "slots_order": ["course_id"],
    },
    "passed_trainees": {
        "module": "exam",
        "requires_name": False,
        "slots_order": ["course_id"],
    },
    "not_appeared_trainees": {
        "module": "exam",
        "requires_name": False,
        "slots_order": ["course_id"],
    },
    "top_performers": {
        "module": "exam",
        "requires_name": False,
        "slots_order": ["course_id"],
    },
    "lowest_performers": {
        "module": "exam",
        "requires_name": False,
        "slots_order": ["course_id"],
    },
    "subject_wise_marks_summary": {
        "module": "exam",
        "requires_name": False,
        "slots_order": ["course_id"],
    },
    "course_exam_summary": {
        "module": "exam",
        "requires_name": False,
        "slots_order": [],
    },
    "re_exam_trainees": {
        "module": "exam",
        "requires_name": False,
        "slots_order": ["course_id"],
    },
    "pass_percentage": {
        "module": "exam",
        "requires_name": False,
        "slots_order": ["course_id"],
    },
    # ── Non-exam flows ──
    "pending_dues_by_person": {
        "module": "dues",
        "requires_name": True,
        "slots_order": ["user_id", "dues_type"],
    },
    "hostel_room_of_trainee": {
        "module": "hostel",
        "requires_name": True,
        "slots_order": ["user_id", "stay_filter"],
    },
    "hostel_availability_occupency": {
        "module": "hostel",
        "requires_name": False,
        "slots_order": ["building_id"],
    },
    "attendance_by_trainee": {
        "module": "attendance",
        "requires_name": True,
        "slots_order": ["user_id", "course_id"],
    },
}


# ═══════════════════════════════════════════════════════════════════
# Typo normalization
# ═══════════════════════════════════════════════════════════════════

_TYPO_MAP = {
    r"\btaines\b": "trainees", r"\btaine\b": "trainee",
    r"\btrainnes\b": "trainees", r"\btrainee's\b": "trainees",
    r"\bstudnts\b": "students", r"\bstudnet\b": "student",
    r"\bfaild\b": "failed", r"\bfaield\b": "failed",
    r"\bhigest\b": "highest", r"\bheighest\b": "highest",
    r"\bmarksheet\b": "marks", r"\bmark\b": "marks",
    r"\bre exam\b": "re-exam", r"\breexam\b": "re-exam",
    r"\bpercntage\b": "percentage", r"\bpercentge\b": "percentage",
    r"\bapperd\b": "appeared", r"\bapeared\b": "appeared",
    r"\bavrage\b": "average", r"\baverge\b": "average",
}


def _normalize_typos(text: str) -> str:
    for pattern, replacement in _TYPO_MAP.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


# ═══════════════════════════════════════════════════════════════════
# Name extraction (rule-based, no LLM dependency)
# ═══════════════════════════════════════════════════════════════════

_STOP_WORDS = {
    "show", "list", "get", "find", "what", "which", "who", "how",
    "many", "is", "are", "the", "of", "for", "in", "a", "an", "and",
    "to", "from", "with", "by", "on", "at", "all", "my", "me", "i",
    "marks", "mark", "result", "results", "exam", "exams", "score",
    "scores", "subject", "subjects", "grade", "grades", "percentage",
    "attendance", "present", "absent", "punch", "biometric",
    "hostel", "room", "rooms", "bed", "beds", "building", "stay",
    "staying", "allotment", "alloted", "allotted", "current",
    "dues", "pending", "mess", "library", "sports",
    "available", "vacant", "empty", "availability",
    "trainee", "trainees", "student", "students",
    "course", "courses", "batch", "batches",
    "please", "tell", "give", "details", "detail", "about",
    "total", "count", "number", "check",
    "recent", "latest", "last", "final", "phase", "re",
    "this", "month", "week", "year", "today", "yesterday",
    "did", "pass", "fail", "failed", "passed", "not", "appeared",
    "top", "highest", "lowest", "bottom", "topper", "performer",
    "performers", "average", "wise", "summary", "rate",
    "or", "do", "does", "has", "have", "been",
}


def _extract_name(message: str) -> Optional[str]:
    """Extract a potential person name from the message."""
    text = re.sub(r'[?!.,;:\'"()\[\]{}]', ' ', message.strip())
    words = text.split()
    name_parts = []
    for word in words:
        if word.lower() in _STOP_WORDS:
            continue
        if word.isdigit():
            continue
        if len(word) <= 1:
            continue
        name_parts.append(word)
    if name_parts:
        return " ".join(name_parts)
    return None


def _extract_exam_filter(message: str) -> Optional[str]:
    text = message.lower()
    if re.search(r"recent|latest|last", text):
        return "recent"
    if "current" in text:
        return "current"
    if "final" in text:
        return "final"
    if "phase 1" in text or "phase1" in text:
        return "phase_1"
    if "phase 2" in text or "phase2" in text:
        return "phase_2"
    if "re-exam" in text or "re exam" in text:
        return "re_exam"
    return None


def _extract_limit(message: str) -> Optional[int]:
    m = re.search(r"top\s+(\d+)", message.lower())
    if m:
        return int(m.group(1))
    m = re.search(r"bottom\s+(\d+)", message.lower())
    if m:
        return int(m.group(1))
    return None


def _detect_dues_type(message: str) -> Optional[str]:
    text = message.lower()
    if "hostel" in text and "dues" in text:
        return "hostel"
    if "mess" in text and "dues" in text:
        return "mess"
    if "library" in text and "dues" in text:
        return "library"
    return None


# ═══════════════════════════════════════════════════════════════════
# Rule-based flow matching (fast, deterministic)
# ═══════════════════════════════════════════════════════════════════

def _match_flow_rules(message: str) -> Optional[str]:
    """Rule-based matching. Returns flow_id or None."""
    text = _normalize_typos(message.lower().strip())

    # ── Non-exam flows (check first for specificity) ──
    if re.search(r"dues|pending\b.*dues|mess\b.*dues|library\b.*dues", text):
        if _extract_name(message):
            return "pending_dues_by_person"

    # ── Exam flows (order matters: specific before generic) ──

    # re-exam
    if re.search(r"re-exam|re\s+exam", text) and re.search(r"trainee|student|list|show|how many", text):
        return "re_exam_trainees"

    # pass percentage / pass rate
    if re.search(r"pass\s+percentage|pass\s+rate|passing\s+percentage", text):
        return "pass_percentage"

    # course wise exam summary
    if re.search(r"course\s+wise\s+exam|result\s+summary\s+by\s+course|exam\s+result\s+summary|pass\s+fail\s+summary\s+by\s+course", text):
        return "course_exam_summary"

    # subject wise marks / average
    if re.search(r"(subject\s+wise|per\s+subject).*(marks|average|performance|summary)", text):
        if not re.search(r"fail|failed|failure", text):
            return "subject_wise_marks_summary"
    if re.search(r"average\s+marks", text):
        return "subject_wise_marks_summary"

    # failed trainees by subject
    if re.search(r"(fail|failed|failure).*(subject)", text) or re.search(r"subject.*(fail|failed|failure)", text):
        return "failed_trainees_by_subject"
    if re.search(r"(highest|most)\s+(fail|failed|failure)", text):
        return "failed_trainees_by_subject"

    # top performers
    if re.search(r"highest\s+marks|topper|top\s+performer|top\s+\d+\s+performer|exam\s+topper|top\s+\d+", text):
        return "top_performers"

    # lowest performers
    if re.search(r"lowest\s+marks|bottom\s+performer|bottom\s+\d+|lowest\s+performer", text):
        return "lowest_performers"

    # not appeared
    if re.search(r"not\s+appear|did\s+not\s+appear|absent\s+in\s+exam|not\s+appeared", text):
        return "not_appeared_trainees"

    # failed trainees (generic)
    if re.search(r"failed\s+(trainee|student|candidate)|fail\s+(trainee|student)", text):
        return "failed_trainees"
    if re.search(r"(show|list|how\s+many|count).*(fail|failed)", text):
        return "failed_trainees"

    # passed trainees
    if re.search(r"passed\s+(trainee|student|candidate)|pass\s+(trainee|student)", text):
        return "passed_trainees"
    if re.search(r"(show|list|how\s+many|count).*(pass|passed)", text):
        return "passed_trainees"

    # exam result (pass/fail question for specific trainee)
    if re.search(r"(did\s+.+\s+pass|pass\s+or\s+fail|result\s+of\b)", text):
        if _extract_name(message):
            return "exam_result_by_trainee"

    # exam marks (trainee-specific)
    if re.search(r"marks|result|score|exam\b.*result|recent\s+exam|latest\s+exam|last\s+exam|phase\s+\d|final\s+exam|re-exam", text):
        if _extract_name(message):
            return "exam_marks_by_trainee"

    return None


# ═══════════════════════════════════════════════════════════════════
# Main entry point
# ═══════════════════════════════════════════════════════════════════

def handle_guided_flow(
    message: str,
    role: str,
    office_id: int,
    session_id: str,
    selected_option: Optional[Dict] = None,
    base_url: str = "http://localhost:8000",
) -> Optional[dict]:
    """Handle guided query flow. Returns None if no guided flow applies."""

    # ── CASE 1: User clicked an option button (continuing a flow) ──
    if selected_option:
        return _handle_option_selection(
            session_id, selected_option, office_id, role, message, base_url
        )

    # ── CASE 2: Check if existing session state needs continuation ──
    existing_state = get_state(session_id) if session_id else None
    if existing_state:
        clear_state(session_id)

    # ── CASE 3: Pre-processing with LLM Query Refiner ──
    from app.services.guided_query_refiner import refine_guided_query
    refined = refine_guided_query(message)
    
    guided_message = message
    if refined.get("corrected_query"):
        guided_message = refined.get("corrected_query")

    normalized_msg = _normalize_typos(guided_message)
    slots = refined.get("slots", {}) or {}
    extracted_name = slots.get("trainee_name")
    flow_id = None
    flow_module = "exam"

    # Route directly if LLM is confident
    if refined.get("confidence", 0) >= 0.70 and refined.get("module") and refined.get("module") != "unknown" and refined.get("flow_id"):
        flow_id = refined.get("flow_id")
        flow_module = refined.get("module")
        print(f"[Refiner] Confident match for {flow_module} -> {flow_id}")
        
        # For timetable and faculty flows, also run rule-based detection to extract slots
        if flow_module == "timetable":
            from app.services.guided_modules.timetable_guided import detect_timetable_guided_flow
            tt_match = detect_timetable_guided_flow(guided_message)
            if tt_match:
                tt_slots = tt_match.get("slots", {})
                for k, v in tt_slots.items():
                    if v is not None and (k not in slots or not slots[k]):
                        slots[k] = v
                        
        elif flow_module == "faculty":
            from app.services.guided_modules.faculty_guided import detect_faculty_guided_flow
            f_match = detect_faculty_guided_flow(guided_message, allow_weak_intent=True)
            if f_match:
                # Selectively override LLM hallucinations for course vs faculty mappings
                r_flow = f_match.get("flow_id")
                if r_flow in ("faculty_by_course", "faculty_by_subject") and flow_id in ("faculty_courses", "faculty_subjects"):
                    flow_id = r_flow
                    
                f_slots = f_match.get("slots", {})
                for k, v in f_slots.items():
                    if v is not None and (k not in slots or not slots[k]):
                        slots[k] = v
    
    # ── CASE 4: Rule-based detection fallback ──
    if not flow_id:
        flow_id = _match_flow_rules(normalized_msg)
        if flow_id:
            print(f"[Exam Guided] Message: {guided_message}")
            print(f"[Exam Guided] Rule-matched flow: {flow_id}")
            flow_module = "exam"
        else:
            # Try Trainee rules
            from app.services.guided_modules.trainee_guided import detect_trainee_guided_flow
            trainee_match = detect_trainee_guided_flow(guided_message)
            if trainee_match:
                flow_id = trainee_match["flow_id"]
                t_slots = trainee_match.get("slots", {})
                for k, v in t_slots.items():
                    if k not in slots or not slots[k]:
                        slots[k] = v
                extracted_name = slots.get("trainee_name")
                flow_module = "trainee"
                print(f"[Trainee Guided] Message: {guided_message}")
                print(f"[Trainee Guided] Rule-matched flow: {flow_id}")
            else:
                # Try Hostel rules
                from app.services.guided_modules.hostel_guided import detect_hostel_guided_flow
                hostel_match = detect_hostel_guided_flow(guided_message)
                if hostel_match:
                    flow_id = hostel_match["flow_id"]
                    h_slots = hostel_match.get("slots", {})
                    for k, v in h_slots.items():
                        if k not in slots or not slots[k]:
                            slots[k] = v
                    extracted_name = slots.get("trainee_name")
                    flow_module = "hostel"
                    print(f"[Hostel Guided] Rule-matched flow: {flow_id}")
                else:
                    # Try Attendance rules
                    from app.services.guided_modules.attendance_guided import detect_attendance_guided_flow
                    attendance_match = detect_attendance_guided_flow(guided_message)
                    if attendance_match:
                        flow_id = attendance_match["flow_id"]
                        a_slots = attendance_match.get("slots", {})
                        for k, v in a_slots.items():
                            if k not in slots or not slots[k]:
                                slots[k] = v
                        extracted_name = slots.get("trainee_name")
                        flow_module = "attendance"
                        print(f"[Attendance Guided] Rule-matched flow: {flow_id}")
                    else:
                        # Try Course rules
                        from app.services.guided_modules.course_guided import detect_course_guided_flow
                        course_match = detect_course_guided_flow(guided_message)
                        if course_match:
                            flow_id = course_match["flow_id"]
                            c_slots = course_match.get("slots", {})
                            for k, v in c_slots.items():
                                if k not in slots or not slots[k]:
                                    slots[k] = v
                            flow_module = "course"
                            print(f"[Course Guided] Rule-matched flow: {flow_id}")
                        else:
                            # Try Complaint rules
                            from app.services.guided_modules.complaint_guided import detect_complaint_guided_flow
                            complaint_match = detect_complaint_guided_flow(guided_message)
                            if complaint_match:
                                flow_id = complaint_match["flow_id"]
                                co_slots = complaint_match.get("slots", {})
                                for k, v in co_slots.items():
                                    if k not in slots or not slots[k]:
                                        slots[k] = v
                                flow_module = "complaint"
                                print(f"[Complaint Guided] Rule-matched flow: {flow_id}")
                            else:
                                # Try Timetable rules
                                from app.services.guided_modules.timetable_guided import detect_timetable_guided_flow
                                timetable_match = detect_timetable_guided_flow(guided_message)
                                if timetable_match:
                                    flow_id = timetable_match["flow_id"]
                                    t_slots = timetable_match.get("slots", {})
                                    for k, v in t_slots.items():
                                        if k not in slots or not slots[k]:
                                            slots[k] = v
                                    flow_module = "timetable"
                                    print(f"[Timetable Guided] Rule-matched flow: {flow_id}")
                                else:
                                    # Try Faculty rules
                                    from app.services.guided_modules.faculty_guided import detect_faculty_guided_flow
                                    faculty_match = detect_faculty_guided_flow(guided_message)
                                    if faculty_match:
                                        flow_id = faculty_match["flow_id"]
                                        f_slots = faculty_match.get("slots", {})
                                        for k, v in f_slots.items():
                                            if k not in slots or not slots[k]:
                                                slots[k] = v
                                        flow_module = "faculty"
                                        print(f"[Faculty Guided] Rule-matched flow: {flow_id}")

    # ── CASE 5: LLM fallback if rules didn't match ──
    if not flow_id:
        from app.services.guided_intent_parser import parse_guided_intent
        # Pass module hint from refiner so only that module's prompt is used
        refiner_module = refined.get("module") if refined.get("module") != "unknown" else None
        parsed = parse_guided_intent(guided_message, module_hint=refiner_module)
        if parsed.get("matches_guided_flow"):
            flow_id = parsed.get("flow_id")
            from app.services.guided_modules.trainee_guided import TRAINEE_FLOWS
            from app.services.guided_modules.hostel_guided import HOSTEL_FLOWS
            from app.services.guided_modules.attendance_guided import ATTENDANCE_FLOWS
            from app.services.guided_modules.course_guided import COURSE_FLOWS
            from app.services.guided_modules.complaint_guided import COMPLAINT_FLOWS
            from app.services.guided_modules.timetable_guided import TIMETABLE_FLOWS
            from app.services.guided_modules.faculty_guided import FACULTY_FLOWS
            if flow_id in GUIDED_FLOWS or flow_id in TRAINEE_FLOWS or flow_id in HOSTEL_FLOWS or flow_id in ATTENDANCE_FLOWS or flow_id in COURSE_FLOWS or flow_id in COMPLAINT_FLOWS or flow_id in TIMETABLE_FLOWS or flow_id in FACULTY_FLOWS:
                llm_slots = parsed.get("slots", {})
                extracted_name = llm_slots.get("trainee_name")
                if flow_id in GUIDED_FLOWS:
                    flow_module = GUIDED_FLOWS[flow_id]["module"]
                elif flow_id in HOSTEL_FLOWS:
                    flow_module = "hostel"
                elif flow_id in ATTENDANCE_FLOWS:
                    flow_module = "attendance"
                elif flow_id in COURSE_FLOWS:
                    flow_module = "course"
                elif flow_id in COMPLAINT_FLOWS:
                    flow_module = "complaint"
                elif flow_id in TIMETABLE_FLOWS:
                    flow_module = "timetable"
                elif flow_id in FACULTY_FLOWS:
                    flow_module = "faculty"
                else:
                    flow_module = TRAINEE_FLOWS[flow_id]["module"]
                
                # Copy relevant slots
                for k, v in llm_slots.items():
                    if k in ["exam_filter", "dues_type", "limit", "year", "recent_filter", "course_name",
                             "hostel_type", "availability_type", "complaint_status", "dues_status",
                             "room_number", "building_name", "complaint_category", "complaint_id", "days",
                             "faculty_name", "subject_name", "classroom_name", "session_name", "group_by",
                             "date", "threshold", "date_range", "from_date", "to_date", "faculty_type"]:
                        if k == "limit":
                            try:
                                slots["limit"] = int(v)
                            except (ValueError, TypeError):
                                pass
                        elif k == "threshold":
                            try:
                                slots["threshold"] = int(v)
                            except (ValueError, TypeError):
                                pass
                        else:
                            slots[k] = v
            else:
                flow_id = None

    if not flow_id:
        return None

    print(f"[{flow_module.capitalize()} Guided] Flow: {flow_id}")

    from app.services.guided_modules.trainee_guided import TRAINEE_FLOWS
    from app.services.guided_modules.hostel_guided import HOSTEL_FLOWS
    from app.services.guided_modules.attendance_guided import ATTENDANCE_FLOWS
    from app.services.guided_modules.course_guided import COURSE_FLOWS
    from app.services.guided_modules.complaint_guided import COMPLAINT_FLOWS
    from app.services.guided_modules.timetable_guided import TIMETABLE_FLOWS
    from app.services.guided_modules.faculty_guided import FACULTY_FLOWS
    flow_def = GUIDED_FLOWS.get(flow_id) or TRAINEE_FLOWS.get(flow_id) or HOSTEL_FLOWS.get(flow_id) or ATTENDANCE_FLOWS.get(flow_id) or COURSE_FLOWS.get(flow_id) or COMPLAINT_FLOWS.get(flow_id) or TIMETABLE_FLOWS.get(flow_id) or FACULTY_FLOWS.get(flow_id)

    # Extract slots from message
    if flow_module == "hostel":
        # Hostel slots already extracted by detect_hostel_guided_flow
        if flow_def["requires_name"] and not extracted_name:
            extracted_name = _extract_name(normalized_msg)
    elif flow_module == "attendance":
        # Attendance slots already extracted by detect_attendance_guided_flow
        if flow_def["requires_name"] and not extracted_name:
            extracted_name = _extract_name(normalized_msg)
    elif flow_module == "course":
        # Course slots already extracted
        pass
    elif flow_module == "complaint":
        # Complaint slots already extracted by detect_complaint_guided_flow
        pass
    elif flow_module == "timetable":
        # Timetable slots already extracted
        pass
    elif flow_module == "faculty":
        # Faculty slots already extracted
        pass
    elif flow_module != "trainee":
        if flow_def["requires_name"] and not extracted_name:
            extracted_name = _extract_name(normalized_msg)

        if "exam_filter" not in slots:
            ef = _extract_exam_filter(normalized_msg)
            if ef:
                slots["exam_filter"] = ef

        if "limit" not in slots:
            lim = _extract_limit(normalized_msg)
            if lim:
                slots["limit"] = lim

    print(f"[{flow_module.capitalize()} Guided] Slots: {slots}")

    slot_labels = {}

    # ── For name-based flows: resolve trainee first ──
    if flow_def.get("requires_name"):
        if not extracted_name:
            print(f"[{flow_module.capitalize()} Guided] Aborting: Name is required but none was extracted.")
            return None
        if flow_module == "hostel":
            from app.services.guided_modules.hostel_options import search_hostel_trainees_by_name
            trainees = search_hostel_trainees_by_name(extracted_name, office_id)
        elif flow_module == "attendance":
            from app.services.guided_modules.attendance_options import search_attendance_trainees_by_name
            trainees = search_attendance_trainees_by_name(extracted_name, office_id)
        elif flow_module == "trainee":
            from app.services.guided_modules.trainee_options import search_trainees_by_name as tr_search
            trainees = tr_search(extracted_name, office_id)
        else:
            trainees = search_trainees_by_name(extracted_name, office_id)

        if not trainees:
            from app.services.guided_intent_parser import parse_guided_intent
            parsed = parse_guided_intent(message)
            if parsed.get("matches_guided_flow"):
                llm_slots = parsed.get("slots", {})
                new_name = llm_slots.get("trainee_name")
                if new_name and new_name.lower() != extracted_name.lower():
                    extracted_name = new_name
                    if flow_module == "hostel":
                        trainees = search_hostel_trainees_by_name(extracted_name, office_id)
                    elif flow_module == "attendance":
                        trainees = search_attendance_trainees_by_name(extracted_name, office_id)
                    elif flow_module == "trainee":
                        trainees = tr_search(extracted_name, office_id)
                    else:
                        trainees = search_trainees_by_name(extracted_name, office_id)

            if not trainees:
                return None

        if len(trainees) == 1:
            slots["user_id"] = trainees[0]["value"]
            slot_labels["user_id"] = trainees[0]["label"]
        else:
            state = create_or_update_state(session_id, {
                "flow_id": flow_id,
                "module": flow_def["module"],
                "original_question": message,
                "collected_slots": slots,
                "slot_labels": {},
                "missing_slots": flow_def["slots_order"][:],
            })
            return {
                "type": "follow_up",
                "message": f'I found multiple people matching "{extracted_name}". Which one do you mean?',
                "session_id": session_id,
                "flow_id": flow_id,
                "slot_key": "user_id",
                "options": trainees[:10],
            }

    # ── For old hostel_availability_occupency (legacy flow): check building ──
    if flow_id == "hostel_availability_occupency" and flow_module != "hostel":
        buildings = get_buildings(office_id)
        if len(buildings) > 2:
            state = create_or_update_state(session_id, {
                "flow_id": flow_id, "module": flow_def["module"],
                "original_question": message,
                "collected_slots": {}, "slot_labels": {},
                "missing_slots": ["building_id"],
            })
            return {
                "type": "follow_up",
                "message": "Which hostel building do you want to check availability for?",
                "session_id": session_id, "flow_id": flow_id,
                "slot_key": "building_id", "options": buildings,
            }
        else:
            slots["building_id"] = "ALL"

    # ── For hostel_trainees_by_room: check room disambiguation ──
    if flow_id == "hostel_trainees_by_room" and flow_module == "hostel":
        room_number = slots.get("room_number")
        if room_number:
            from app.services.guided_modules.hostel_options import get_rooms_by_number
            room_options = get_rooms_by_number(room_number, office_id)
            if len(room_options) > 1:
                state = create_or_update_state(session_id, {
                    "flow_id": flow_id, "module": "hostel",
                    "original_question": message,
                    "collected_slots": slots, "slot_labels": {},
                    "missing_slots": ["room_id"],
                })
                print(f"[Hostel Guided] Follow-up slot: room_id")
                return {
                    "type": "follow_up",
                    "message": f"Room {room_number} exists in multiple buildings. Which one?",
                    "session_id": session_id, "flow_id": flow_id,
                    "slot_key": "room_id", "options": room_options,
                }
            elif len(room_options) == 1:
                slots["room_id"] = room_options[0]["value"]

    # ── For pending_dues: check if dues type already specified ──
    if flow_id == "pending_dues_by_person":
        detected_type = _detect_dues_type(message)
        if detected_type:
            slots["dues_type"] = detected_type
            slot_labels["dues_type"] = detected_type.title() + " dues"

    # ── Now check next missing slot ──
    return _check_next_slot(
        flow_id, flow_def, slots, slot_labels, office_id,
        session_id, message, base_url, role
    )


def _handle_option_selection(
    session_id: str, selected_option: dict, office_id: int,
    role: str, message: str, base_url: str,
) -> Optional[dict]:
    """Handle when user clicks an option button."""
    flow_id = selected_option.get("flow_id")
    slot_key = selected_option.get("slot_key")
    value = selected_option.get("value")
    label = selected_option.get("label", "")

    if not flow_id or not slot_key:
        return None

    from app.services.guided_modules.trainee_guided import TRAINEE_FLOWS
    from app.services.guided_modules.hostel_guided import HOSTEL_FLOWS
    from app.services.guided_modules.attendance_guided import ATTENDANCE_FLOWS
    from app.services.guided_modules.course_guided import COURSE_FLOWS
    from app.services.guided_modules.complaint_guided import COMPLAINT_FLOWS
    from app.services.guided_modules.timetable_guided import TIMETABLE_FLOWS
    from app.services.guided_modules.faculty_guided import FACULTY_FLOWS
    flow_def = GUIDED_FLOWS.get(flow_id) or TRAINEE_FLOWS.get(flow_id) or HOSTEL_FLOWS.get(flow_id) or ATTENDANCE_FLOWS.get(flow_id) or COURSE_FLOWS.get(flow_id) or COMPLAINT_FLOWS.get(flow_id) or TIMETABLE_FLOWS.get(flow_id) or FACULTY_FLOWS.get(flow_id)
    if not flow_def:
        return None

    state = get_state(session_id)
    if state is None:
        state = create_or_update_state(session_id, {
            "flow_id": flow_id, "module": flow_def["module"],
            "original_question": message,
            "collected_slots": {}, "slot_labels": {},
            "missing_slots": flow_def["slots_order"][:],
        })

    if value == "LOAD_MORE_OPTIONS":
        slots = state.get("collected_slots", {})
        slots[f"{slot_key}_offset"] = slots.get(f"{slot_key}_offset", 0) + 10
        create_or_update_state(session_id, state)
        return _check_next_slot(flow_id, flow_def, slots, state.get("slot_labels", {}), office_id, session_id, state.get("original_question", message), base_url, role)

    if value == "LOAD_PREV_OPTIONS":
        slots = state.get("collected_slots", {})
        slots[f"{slot_key}_offset"] = max(0, slots.get(f"{slot_key}_offset", 0) - 10)
        create_or_update_state(session_id, state)
        return _check_next_slot(flow_id, flow_def, slots, state.get("slot_labels", {}), office_id, session_id, state.get("original_question", message), base_url, role)

    update_slot(session_id, slot_key, value, label)
    state = get_state(session_id)

    slots = state.get("collected_slots", {})
    slot_labels = state.get("slot_labels", {})
    original_question = state.get("original_question", message)

    return _check_next_slot(
        flow_id, flow_def, slots, slot_labels, office_id,
        session_id, original_question, base_url, role
    )


def _check_next_slot(
    flow_id: str, flow_def: dict, slots: dict, slot_labels: dict,
    office_id: int, session_id: str, original_question: str, base_url: str,
    role: str = "principal",
) -> Optional[dict]:
    """Check which slot is next to fill, ask follow-up, or execute query."""
    slots_order = flow_def["slots_order"]

    for slot_key in slots_order:
        if slots.get(slot_key) is not None:
            continue

        if slot_key == "year" and slots.get("date_range"):
            continue

        options = _get_options_for_slot(flow_id, slot_key, slots, office_id)

        if options is None:
            continue
        if len(options) == 0:
            continue
        if len(options) == 1:
            slots[slot_key] = options[0]["value"]
            slot_labels[slot_key] = options[0]["label"]
            continue

        # Check if the user explicitly typed one of the options
        def _clean_for_match(text: str) -> str:
            import re
            return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', text.lower())).strip()

        matched_option = None
        cleaned_q = _clean_for_match(original_question)
        
        # Sort by length descending so longer, more specific course names match first
        for opt in sorted(options, key=lambda x: len(str(x.get("label", ""))), reverse=True):
            cleaned_opt = _clean_for_match(str(opt.get("label", "")))
            if cleaned_opt and len(cleaned_opt) > 3 and cleaned_opt in cleaned_q:
                matched_option = opt
                break
                
        if matched_option:
            module_name = flow_def.get('module', 'exam').capitalize()
            print(f"[{module_name} Guided] Auto-resolved {slot_key} to {matched_option['value']} from text match")
            slots[slot_key] = matched_option["value"]
            slot_labels[slot_key] = matched_option["label"]
            continue

        # Multiple options — ask user
        state = create_or_update_state(session_id, {
            "flow_id": flow_id, "module": flow_def["module"],
            "original_question": original_question,
            "collected_slots": slots, "slot_labels": slot_labels,
            "missing_slots": [s for s in slots_order if s not in slots],
        })

        question_text = _get_follow_up_question(flow_id, slot_key, slots)
        module_name = flow_def.get('module', 'exam').capitalize()
        print(f"[{module_name} Guided] Missing slots: {state.get('missing_slots', [])}")
        print(f"[{module_name} Guided] Follow-up slot: {slot_key}")
        return {
            "type": "follow_up",
            "message": question_text,
            "session_id": session_id,
            "flow_id": flow_id,
            "slot_key": slot_key,
            "options": options,
        }

    # ── All slots filled — execute query ──
    clear_state(session_id)
    if flow_def.get("module") == "hostel":
        print(f"[Hostel Guided] Executing: {flow_id} with slots: {slots}")
        from app.services.guided_modules.hostel_executor import execute_hostel_guided_query
        result = execute_hostel_guided_query(
            flow_id=flow_id, slots=slots, office_id=office_id,
            role="principal", session_id=session_id,
            user_question=original_question, base_url=base_url,
        )
    elif flow_def.get("module") == "attendance":
        print(f"[Attendance Guided] Executing: {flow_id} with slots: {slots}")
        from app.services.guided_modules.attendance_executor import execute_attendance_guided_query
        result = execute_attendance_guided_query(
            flow_id=flow_id, slots=slots, office_id=office_id,
            role="principal", session_id=session_id,
            user_question=original_question, base_url=base_url,
        )
    elif flow_def.get("module") == "course":
        print(f"[Course Guided] Executing: {flow_id} with slots: {slots}")
        from app.services.guided_modules.course_executor import execute_course_guided_query
        result = execute_course_guided_query(
            flow_id=flow_id, slots=slots, office_id=office_id,
            role="principal", session_id=session_id,
            user_question=original_question, base_url=base_url,
        )
    elif flow_def.get("module") == "complaint":
        print(f"[Complaint Guided] Executing: {flow_id} with slots: {slots}")
        from app.services.guided_modules.complaint_executor import execute_complaint_guided_query
        result = execute_complaint_guided_query(
            flow_id=flow_id, slots=slots, office_id=office_id,
            role="principal", session_id=session_id,
            user_question=original_question, base_url=base_url,
        )
    elif flow_def.get("module") == "timetable":
        print(f"[Timetable Guided] Executing: {flow_id} with slots: {slots}")
        from app.services.guided_modules.timetable_executor import execute_timetable_guided_query
        result = execute_timetable_guided_query(
            flow_id=flow_id, slots=slots, office_id=office_id,
            role="principal", session_id=session_id,
            user_question=original_question, base_url=base_url,
        )
    elif flow_def.get("module") == "faculty":
        # Access policy check
        try:
            from app.services.guided_access_policy import can_access_guided_flow
            if not can_access_guided_flow(role, "faculty", flow_id, slots, office_id):
                return {"type": "text", "message": "Permission denied: You do not have access to this faculty information."}
        except ImportError:
            pass
            
        print(f"[Faculty Guided] Executing: {flow_id} with slots: {slots}")
        from app.services.guided_modules.faculty_executor import execute_faculty_guided_query
        result = execute_faculty_guided_query(
            flow_id=flow_id, slots=slots, office_id=office_id,
            role=role, session_id=session_id,
            user_question=original_question, base_url=base_url,
        )
    elif flow_def.get("module") == "trainee":
        print(f"[Trainee Guided] Executing: {flow_id} with slots: {slots}")
        from app.services.guided_modules.trainee_executor import execute_trainee_guided_query
        result = execute_trainee_guided_query(
            flow_id=flow_id, slots=slots, office_id=office_id,
            role="principal", original_question=original_question,
            session_id=session_id, base_url=base_url,
        )
    else:
        print(f"[Exam Guided] Executing flow: {flow_id} with slots: {slots}")
        result = execute_guided_query(
            flow_id=flow_id, slots=slots, office_id=office_id,
            role="principal", original_question=original_question,
            session_id=session_id, base_url=base_url,
        )
    return result


def _get_options_for_slot(
    flow_id: str, slot_key: str, slots: dict, office_id: int
) -> Optional[list]:
    """Fetch options from DB for a specific slot."""
    from app.services.guided_modules.trainee_guided import TRAINEE_FLOWS
    from app.services.guided_modules.hostel_guided import HOSTEL_FLOWS
    from app.services.guided_modules.attendance_guided import ATTENDANCE_FLOWS
    from app.services.guided_modules.course_guided import COURSE_FLOWS
    from app.services.guided_modules.complaint_guided import COMPLAINT_FLOWS
    from app.services.guided_modules.timetable_guided import TIMETABLE_FLOWS
    from app.services.guided_modules.faculty_guided import FACULTY_FLOWS
    is_trainee_flow = flow_id in TRAINEE_FLOWS
    is_hostel_flow = flow_id in HOSTEL_FLOWS
    is_attendance_flow = flow_id in ATTENDANCE_FLOWS
    is_course_flow = flow_id in COURSE_FLOWS
    is_complaint_flow = flow_id in COMPLAINT_FLOWS
    is_timetable_flow = flow_id in TIMETABLE_FLOWS
    is_faculty_flow = flow_id in FACULTY_FLOWS

    user_id = slots.get("user_id")

    if is_hostel_flow:
        if slot_key == "building_id":
            return get_buildings(office_id)
        if slot_key == "stay_filter" and user_id:
            from app.services.guided_modules.hostel_options import get_hostel_records_for_trainee
            options = get_hostel_records_for_trainee(user_id, office_id)
            if not options:
                return None
            return options
        # Hostel flows have no multi-step slot filling via options
        # (room disambiguation handled separately)
        return None

    if is_attendance_flow:
        if slot_key == "course_id":
            user_id_val = slots.get("user_id")
            if user_id_val:
                from app.services.guided_modules.attendance_options import get_attendance_courses_for_trainee
                options = get_attendance_courses_for_trainee(user_id_val, office_id)
            else:
                from app.services.guided_modules.attendance_options import get_recent_attendance_courses
                options = get_recent_attendance_courses(office_id, offset=slots.get(f"{slot_key}_offset", 0))
            if len(options) <= 2:
                return None
            return options
        if slot_key == "threshold":
            from app.services.guided_modules.attendance_options import get_attendance_threshold_options
            return get_attendance_threshold_options()
        # Attendance flows without defined multi-step slots
        return None

    if is_course_flow:
        if slot_key == "course_id":
            from app.services.guided_modules.course_options import search_courses_by_name, get_recent_courses_for_course_module
            c_name = slots.get("course_name")
            if c_name:
                options = search_courses_by_name(c_name, office_id)
                if options:
                    return options
            return get_recent_courses_for_course_module(office_id, offset=slots.get(f"{slot_key}_offset", 0))
        if slot_key == "year":
            from app.services.guided_modules.course_options import get_course_year_options
            return get_course_year_options()
        if slot_key == "status":
            from app.services.guided_modules.course_options import get_course_status_options
            return get_course_status_options()
        return None

    if is_complaint_flow:
        if slot_key == "user_id":
            from app.services.guided_modules.complaint_options import search_complaint_trainees_by_name
            t_name = slots.get("trainee_name")
            if t_name:
                options = search_complaint_trainees_by_name(t_name, office_id)
                if options:
                    return options
            return None
        if slot_key == "complaint_category":
            from app.services.guided_modules.complaint_options import get_complaint_categories
            return get_complaint_categories(office_id, offset=slots.get(f"{slot_key}_offset", 0))
        if slot_key == "complaint_status":
            from app.services.guided_modules.complaint_options import get_complaint_status_options
            return get_complaint_status_options()
        if slot_key == "year":
            from app.services.guided_modules.complaint_options import get_complaint_year_options
            return get_complaint_year_options()
        return None

    if is_timetable_flow:
        if slot_key == "course_id":
            from app.services.guided_modules.timetable_options import search_timetable_courses, get_recent_timetable_courses
            c_name = slots.get("course_name")
            if c_name:
                options = search_timetable_courses(c_name, office_id)
                if options: return options
            return get_recent_timetable_courses(office_id)
            
        if slot_key == "user_id":
            from app.services.guided_modules.timetable_options import search_faculty_by_name
            f_name = slots.get("faculty_name")
            if f_name:
                options = search_faculty_by_name(f_name, office_id)
                if options: return options
            return None
            
        if slot_key == "subject_id":
            from app.services.guided_modules.timetable_options import search_subjects_by_name
            s_name = slots.get("subject_name")
            if s_name:
                options = search_subjects_by_name(s_name, office_id)
                if options: return options
            return None
            
        if slot_key == "classroom_id":
            from app.services.guided_modules.timetable_options import search_classrooms_by_name
            r_name = slots.get("classroom_name")
            if r_name:
                options = search_classrooms_by_name(r_name, office_id)
                if options: return options
            return None
            
        if slot_key == "session_id":
            from app.services.guided_modules.timetable_options import get_sessions
            return get_sessions(office_id)
            
        if slot_key == "date":
            from app.services.guided_modules.timetable_options import get_timetable_date_options
            return get_timetable_date_options()
            
        return None

    if is_faculty_flow:
        if slot_key == "faculty_id":
            from app.services.guided_modules.faculty_options import search_faculty_all, get_faculty_type_options
            f_name = slots.get("faculty_name")
            if f_name:
                options = search_faculty_all(f_name, office_id)
                if options: return options
            return None
            
        if slot_key == "course_id":
            from app.services.guided_modules.faculty_options import search_faculty_courses, get_recent_faculty_courses
            c_name = slots.get("course_name")
            if c_name:
                options = search_faculty_courses(c_name, office_id)
                if options: return options
            return get_recent_faculty_courses(office_id)
            
        if slot_key == "subject_id":
            from app.services.guided_modules.faculty_options import search_faculty_subjects
            s_name = slots.get("subject_name")
            if s_name:
                options = search_faculty_subjects(s_name, office_id)
                if options: return options
            return None
            
        if slot_key == "date":
            from app.services.guided_modules.faculty_options import get_faculty_date_options
            return get_faculty_date_options()

    if is_trainee_flow:
        from app.services.guided_modules.trainee_options import (
            get_recent_trainee_courses, get_year_options, get_courses_for_trainee_module
        )
        if slot_key == "year":
            return get_year_options()
        if slot_key == "course_id":
            return get_courses_for_trainee_module(office_id, offset=slots.get(f"{slot_key}_offset", 0))
        return None

    # ── Trainee-specific course selection ──
    if slot_key == "course_id" and user_id:
        options = get_courses_for_trainee(user_id, office_id)
        if len(options) <= 2:
            return None
        return options

    # ── Non-trainee exam flows: course selection ──
    if slot_key == "course_id" and not user_id:
        options = get_recent_courses_for_exam(office_id, limit=10)
        if len(options) <= 2:
            return None
        return options

    # ── Exam type for trainee ──
    if slot_key == "exam_type_id" and user_id:
        exam_filter = slots.get("exam_filter")
        if exam_filter in ["recent", "latest", "last", "current", "final",
                           "phase_1", "phase_2", "re_exam", "all"]:
            return None
        course_id = slots.get("course_id", "ALL")
        options = get_exam_types_for_trainee_course(user_id, course_id, office_id)
        if not options:
            return None
        return options

    # ── Non-exam slots ──
    if slot_key == "dues_type":
        return get_dues_type_options()

    if slot_key == "stay_filter" and user_id:
        options = get_hostel_records_for_trainee(user_id, office_id)
        if not options:
            return None
        return options

    if slot_key == "building_id":
        return get_buildings(office_id)

    return None


def _get_follow_up_question(flow_id: str, slot_key: str, slots: dict = None) -> str:
    """Get the human-readable follow-up question for a slot."""
    questions = {
        # Trainee Module
        ("trainee_joined_by_year", "year"): "Which year do you want to check?",
        ("trainees_by_course", "course_id"): "Which course or batch do you want to see trainees for?",
        # Exam Trainee-specific
        ("exam_marks_by_trainee", "user_id"): "Which trainee do you mean?",
        ("exam_marks_by_trainee", "course_id"): "Which course/batch?",
        ("exam_marks_by_trainee", "exam_type_id"): "Which exam type/phase?",
        ("exam_result_by_trainee", "user_id"): "Which trainee do you mean?",
        ("exam_result_by_trainee", "course_id"): "Which course/batch?",
        ("exam_result_by_trainee", "exam_type_id"): "Which exam type/phase?",
        # Non-trainee exam
        ("failed_trainees", "course_id"): "For which course do you want to see failed trainees?",
        ("failed_trainees_by_subject", "course_id"): "For which course do you want subject-wise fail count?",
        ("passed_trainees", "course_id"): "For which course do you want to see passed trainees?",
        ("not_appeared_trainees", "course_id"): "For which course?",
        ("top_performers", "course_id"): "For which course do you want top performers?",
        ("lowest_performers", "course_id"): "For which course?",
        ("subject_wise_marks_summary", "course_id"): "For which course do you want subject-wise marks?",
        ("re_exam_trainees", "course_id"): "For which course?",
        ("pass_percentage", "course_id"): "For which course do you want pass percentage?",
        # Non-exam
        ("pending_dues_by_person", "user_id"): "Which person do you mean?",
        ("pending_dues_by_person", "dues_type"): "Which type of dues do you want to check?",
        ("hostel_room_of_trainee", "user_id"): "Which trainee do you mean?",
        ("hostel_room_of_trainee", "stay_filter"): "Which hostel stay record?",
        ("hostel_availability_occupency", "building_id"): "Which hostel building?",
        ("attendance_by_trainee", "user_id"): "Which trainee do you mean?",
        ("attendance_by_trainee", "course_id"): "Which course/batch?",
        # Hostel guided module
        ("hostel_room_by_trainee", "user_id"): "I found multiple trainees with that name. Please select one:",
        ("hostel_room_by_trainee", "stay_filter"): "Do you want current stay or all stays?",
        ("hostel_dues_by_trainee", "user_id"): "I found multiple trainees with that name. Please select one:",
        ("hostel_trainees_by_room", "room_id"): "This room exists in multiple buildings. Which one?",
        # Attendance guided module
        ("attendance_by_trainee", "user_id"): "I found multiple trainees with that name. Please select one:",
        ("attendance_by_trainee", "course_id"): "Do you want attendance for all courses or a specific course?",
        ("attendance_percentage_by_trainee", "user_id"): "I found multiple trainees with that name. Please select one:",
        ("attendance_percentage_by_trainee", "course_id"): "Do you want attendance percentage for all courses or a specific course?",
        ("trainee_absent_count", "user_id"): "I found multiple trainees with that name. Please select one:",
        ("trainee_present_count", "user_id"): "I found multiple trainees with that name. Please select one:",
        ("low_attendance_trainees", "threshold"): "What attendance threshold should I use?",
        ("low_attendance_trainees", "course_id"): "Which course or batch do you want to check?",
        ("course_attendance_summary", "course_id"): "Which course or batch do you want the summary for?",
        ("present_trainees", "course_id"): "Which course or batch?",
        ("absent_trainees", "course_id"): "Which course or batch?",
        ("date_wise_attendance", "course_id"): "Which course or batch?",
        ("batch_attendance_report", "course_id"): "Which course/batch do you want the attendance report for?",
        # Course guided module
        ("course_details_by_name", "course_id"): "Which course or batch do you want?",
        ("course_trainee_count", "course_id"): "Which course or batch do you want the trainee count for?",
        ("course_duration_summary", "course_id"): "Which course or batch do you want the duration for?",
        ("batch_details", "course_id"): "Which batch do you want details for?",
        ("course_calendar_summary", "status"): "Do you want current, upcoming, or completed courses?",
        ("course_calendar_summary", "year"): "Which year do you want to check?",
        # Complaint guided module
        ("complaints_by_trainee", "user_id"): "I found multiple trainees named {}. Please select one:",
        ("complaints_by_category", "complaint_category"): "Which complaint category?",
        ("complaint_details_by_id", "complaint_id"): "Please provide the complaint ID:",
        # Timetable guided module
        ("course_timetable", "course_id"): "Which course or batch do you want?",
        ("faculty_timetable", "user_id"): "Which faculty?",
        ("subject_timetable", "subject_id"): "Which subject?",
        ("classroom_timetable", "classroom_id"): "Which classroom?",
        ("session_timetable", "session_id"): "Which session?",
        ("date_wise_timetable", "date"): "For which date?",
        # Faculty guided module
        ("faculty_profile_by_name", "faculty_id"): "Which faculty?",
        ("faculty_schedule", "faculty_id"): "Which faculty?",
        ("faculty_courses", "faculty_id"): "Which faculty?",
        ("faculty_subjects", "faculty_id"): "Which faculty?",
        ("faculty_feedback_summary", "faculty_id"): "Which faculty?",
        ("faculty_by_subject", "subject_id"): "Which subject?",
        ("faculty_by_course", "course_id"): "Which course or batch?",
    }
    question = questions.get((flow_id, slot_key), f"Please select {slot_key.replace('_', ' ')}:")
    slots = slots or {}
    
    if flow_id == "complaints_by_trainee" and slot_key == "user_id":
        t_name = slots.get("trainee_name", "that")
        question = question.format(t_name)
    elif flow_id in ("course_timetable", "faculty_by_course") and slot_key == "course_id":
        c_name = slots.get("course_name")
        if c_name:
            question = f"I found multiple courses matching '{c_name}'. Please select one:"
    elif flow_id in ("faculty_timetable", "faculty_profile_by_name", "faculty_schedule", "faculty_courses", "faculty_subjects", "faculty_feedback_summary") and slot_key in ("user_id", "faculty_id"):
        f_name = slots.get("faculty_name")
        if f_name:
            question = f"I found multiple faculty matching '{f_name}'. Please select one:"
    elif flow_id in ("subject_timetable", "faculty_by_subject") and slot_key == "subject_id":
        s_name = slots.get("subject_name")
        if s_name:
            question = f"I found multiple subjects matching '{s_name}'. Please select one:"
        
    return question
