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
    if re.search(r"\bbooks?\b|\bborrowed\b", text) and not re.search(r"dues\b", text):
        return None

    if re.search(r"dues|pending\b.*dues", text) and not re.search(r"\bmess\b", text):
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

def _get_guided_flow_definition(flow_id: str) -> Optional[dict]:
    """Helper to look up a flow definition across all guided modules."""
    from app.services.guided_modules.trainee_guided import TRAINEE_FLOWS
    from app.services.guided_modules.hostel_guided import HOSTEL_FLOWS
    from app.services.guided_modules.attendance_guided import ATTENDANCE_FLOWS
    from app.services.guided_modules.course_guided import COURSE_FLOWS
    from app.services.guided_modules.complaint_guided import COMPLAINT_FLOWS
    from app.services.guided_modules.timetable_guided import TIMETABLE_FLOWS
    from app.services.guided_modules.faculty_guided import FACULTY_FLOWS
    from app.services.guided_modules.library_guided import LIBRARY_FLOWS
    from app.services.guided_modules.mess_guided import MESS_FLOWS
    from app.services.guided_modules.vehicle_guided import VEHICLE_FLOWS
    from app.services.guided_modules.meeting_guided import MEETING_FLOWS
    from app.services.guided_modules.seminar_guided import SEMINAR_FLOWS
    from app.services.guided_modules.inspection_guided import INSPECTION_FLOWS
    from app.services.guided_modules.sports_guided import SPORTS_FLOWS
    from app.services.guided_modules.pass_eq_guided import PASS_EQ_FLOWS
    from app.services.guided_modules.field_study_tour_guided import FIELD_STUDY_TOUR_FLOWS
    from app.services.guided_modules.master_admin_guided import MASTER_ADMIN_FLOWS
    
    return (
        GUIDED_FLOWS.get(flow_id) or TRAINEE_FLOWS.get(flow_id) or HOSTEL_FLOWS.get(flow_id) or
        ATTENDANCE_FLOWS.get(flow_id) or COURSE_FLOWS.get(flow_id) or COMPLAINT_FLOWS.get(flow_id) or
        TIMETABLE_FLOWS.get(flow_id) or FACULTY_FLOWS.get(flow_id) or LIBRARY_FLOWS.get(flow_id) or
        MESS_FLOWS.get(flow_id) or VEHICLE_FLOWS.get(flow_id) or MEETING_FLOWS.get(flow_id) or
        SEMINAR_FLOWS.get(flow_id) or INSPECTION_FLOWS.get(flow_id) or SPORTS_FLOWS.get(flow_id) or
        PASS_EQ_FLOWS.get(flow_id) or FIELD_STUDY_TOUR_FLOWS.get(flow_id) or MASTER_ADMIN_FLOWS.get(flow_id)
    )

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
        
        # Intercept legacy reports that LLM mistakenly mapped to guided flows
        if flow_module == "attendance" and re.search(r"\bmonth\b|\bmonthly\b|\byear\b|\byearly\b|\bannual\b|\bdepartment\b|\bdesignation\b|\boffice\b|\bgender\b", guided_message.lower()):
            print(f"[Refiner] Bypassing '{flow_id}' because query '{guided_message}' is a legacy report.")
            return None
            
        if flow_module == "library" and flow_id == "book_search" and re.search(r"\bshow\b|\blist\b|\ball\b", guided_message.lower()):
            print(f"[Refiner] Bypassing '{flow_id}' because query '{guided_message}' is a library report.")
            return None
            
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

        elif flow_module == "mess":
            from app.services.guided_modules.mess_guided import detect_mess_guided_flow
            mess_match = detect_mess_guided_flow(guided_message)
            if mess_match:
                m_slots = mess_match.get("slots", {})
                for k, v in m_slots.items():
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
                                extracted_name = slots.get("trainee_name")
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
                                    else:
                                        # Try Library rules
                                        from app.services.guided_modules.library_guided import detect_library_guided_flow
                                        library_match = detect_library_guided_flow(guided_message)
                                        if library_match:
                                            flow_id = library_match["flow_id"]
                                            l_slots = library_match.get("slots", {})
                                            for k, v in l_slots.items():
                                                if k not in slots or not slots[k]:
                                                    slots[k] = v
                                            flow_module = "library"
                                            print(f"[Library Guided] Rule-matched flow: {flow_id}")
                                        else:
                                            # Try Mess rules
                                            from app.services.guided_modules.mess_guided import detect_mess_guided_flow
                                            mess_match = detect_mess_guided_flow(guided_message)
                                            if mess_match:
                                                flow_id = mess_match["flow_id"]
                                                m_slots = mess_match.get("slots", {})
                                                for k, v in m_slots.items():
                                                    if k not in slots or not slots[k]:
                                                        slots[k] = v
                                                flow_module = "mess"
                                                print(f"[Mess Guided] Rule-matched flow: {flow_id}")
                                            else:
                                                # Try Vehicle rules
                                                from app.services.guided_modules.vehicle_guided import detect_vehicle_guided_flow
                                                vehicle_match = detect_vehicle_guided_flow(guided_message)
                                                if vehicle_match:
                                                    flow_id = vehicle_match["flow_id"]
                                                    v_slots = vehicle_match.get("slots", {})
                                                    for k, v in v_slots.items():
                                                        if k not in slots or not slots[k]:
                                                            slots[k] = v
                                                    flow_module = "vehicle"
                                                    print(f"[Vehicle Guided] Rule-matched flow: {flow_id}")
                                                else:
                                                    from app.services.guided_modules.meeting_guided import detect_meeting_guided_flow
                                                    meeting_match = detect_meeting_guided_flow(guided_message)
                                                    if meeting_match:
                                                        flow_id, m_slots = meeting_match["flow_id"], meeting_match.get("slots", {})
                                                        for k, v in m_slots.items():
                                                            if k not in slots or not slots[k]: slots[k] = v
                                                        flow_module = "meeting"
                                                    else:
                                                        from app.services.guided_modules.seminar_guided import detect_seminar_guided_flow
                                                        seminar_match = detect_seminar_guided_flow(guided_message)
                                                        if seminar_match:
                                                            flow_id, s_slots = seminar_match["flow_id"], seminar_match.get("slots", {})
                                                            for k, v in s_slots.items():
                                                                if k not in slots or not slots[k]: slots[k] = v
                                                            flow_module = "seminar"
                                                        else:
                                                            from app.services.guided_modules.inspection_guided import detect_inspection_guided_flow
                                                            inspection_match = detect_inspection_guided_flow(guided_message)
                                                            if inspection_match:
                                                                flow_id, i_slots = inspection_match["flow_id"], inspection_match.get("slots", {})
                                                                for k, v in i_slots.items():
                                                                    if k not in slots or not slots[k]: slots[k] = v
                                                                flow_module = "inspection"
                                                            else:
                                                                from app.services.guided_modules.sports_guided import detect_sports_guided_flow
                                                                sports_match = detect_sports_guided_flow(guided_message)
                                                                if sports_match:
                                                                    flow_id, sp_slots = sports_match["flow_id"], sports_match.get("slots", {})
                                                                    for k, v in sp_slots.items():
                                                                        if k not in slots or not slots[k]: slots[k] = v
                                                                    flow_module = "sports"
                                                                else:
                                                                    from app.services.guided_modules.pass_eq_guided import detect_pass_eq_guided_flow
                                                                    pass_match = detect_pass_eq_guided_flow(guided_message)
                                                                    if pass_match:
                                                                        flow_id, pa_slots = pass_match["flow_id"], pass_match.get("slots", {})
                                                                        for k, v in pa_slots.items():
                                                                            if k not in slots or not slots[k]: slots[k] = v
                                                                        flow_module = "pass_eq"
                                                                    else:
                                                                        from app.services.guided_modules.field_study_tour_guided import detect_field_study_tour_guided_flow
                                                                        fst_match = detect_field_study_tour_guided_flow(guided_message)
                                                                        if fst_match:
                                                                            flow_id, fs_slots = fst_match["flow_id"], fst_match.get("slots", {})
                                                                            for k, v in fs_slots.items():
                                                                                if k not in slots or not slots[k]: slots[k] = v
                                                                            flow_module = "field_study_tour"
                                                                        else:
                                                                            from app.services.guided_modules.master_admin_guided import detect_master_admin_guided_flow
                                                                            ma_match = detect_master_admin_guided_flow(guided_message)
                                                                            if ma_match:
                                                                                flow_id, ma_slots = ma_match["flow_id"], ma_match.get("slots", {})
                                                                                for k, v in ma_slots.items():
                                                                                    if k not in slots or not slots[k]: slots[k] = v
                                                                                flow_module = "master_admin"

    # ── CASE 5: LLM fallback if rules didn't match ──
    # Trust the refiner: if it already classified as "unknown" with low confidence,
    # skip the expensive multi-module intent parser (saves 5 LLM calls for greetings)
    refiner_module = refined.get("module") if refined.get("module") != "unknown" else None
    refiner_confidence = refined.get("confidence", 0)

    if not flow_id and refiner_module:
        from app.services.guided_intent_parser import parse_guided_intent
        # Refiner identified a module — use focused single-module parser (1 LLM call)
        parsed = parse_guided_intent(guided_message, module_hint=refiner_module)
    elif not flow_id:
        # Refiner said "unknown" — skip the multi-module intent parser entirely
        print(f"[Guided Flow] Refiner classified as 'unknown' (confidence={refiner_confidence}). Skipping intent parser.")
        return None
    else:
        parsed = None

    if parsed and parsed.get("matches_guided_flow"):
        flow_id = parsed.get("flow_id")
        from app.services.guided_modules.trainee_guided import TRAINEE_FLOWS
        from app.services.guided_modules.hostel_guided import HOSTEL_FLOWS
        from app.services.guided_modules.attendance_guided import ATTENDANCE_FLOWS
        from app.services.guided_modules.course_guided import COURSE_FLOWS
        from app.services.guided_modules.complaint_guided import COMPLAINT_FLOWS
        from app.services.guided_modules.timetable_guided import TIMETABLE_FLOWS
        from app.services.guided_modules.faculty_guided import FACULTY_FLOWS
        from app.services.guided_modules.mess_guided import MESS_FLOWS as _MESS_FLOWS_INTENT
        from app.services.guided_modules.vehicle_guided import VEHICLE_FLOWS as _VEHICLE_FLOWS_INTENT
        if flow_id in GUIDED_FLOWS or flow_id in TRAINEE_FLOWS or flow_id in HOSTEL_FLOWS or flow_id in ATTENDANCE_FLOWS or flow_id in COURSE_FLOWS or flow_id in COMPLAINT_FLOWS or flow_id in TIMETABLE_FLOWS or flow_id in FACULTY_FLOWS or flow_id in _MESS_FLOWS_INTENT or flow_id in _VEHICLE_FLOWS_INTENT:
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
            elif flow_id in _MESS_FLOWS_INTENT:
                flow_module = "mess"
            elif flow_id in _VEHICLE_FLOWS_INTENT:
                flow_module = "vehicle"
            else:
                flow_module = TRAINEE_FLOWS[flow_id]["module"]
            
            # Copy relevant slots
            for k, v in llm_slots.items():
                if k in ["exam_filter", "dues_type", "limit", "year", "recent_filter", "course_name",
                         "hostel_type", "availability_type", "complaint_status", "dues_status",
                         "room_number", "building_name", "complaint_category", "complaint_id", "days",
                         "faculty_name", "subject_name", "classroom_name", "session_name", "group_by",
                         "date", "threshold", "date_range", "from_date", "to_date", "faculty_type",
                         "item_name", "party_name", "month", "meal_item_name",
                         "vehicle_number", "vehicle_type", "driver_name"]:
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

    flow_def = _get_guided_flow_definition(flow_id)
    if not flow_def:
        print(f"[Guided Flow] Warning: flow definition not found for flow_id '{flow_id}'")
        return None

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
    elif flow_module == "mess":
        # Mess slots already extracted by detect_mess_guided_flow
        if flow_def["requires_name"] and not extracted_name:
            extracted_name = _extract_name(normalized_msg)
    elif flow_module == "vehicle":
        # Vehicle slots already extracted by detect_vehicle_guided_flow
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
        elif flow_module == "mess":
            from app.services.guided_modules.mess_options import search_mess_trainees_by_name
            trainees = search_mess_trainees_by_name(extracted_name, office_id)
        else:
            trainees = search_trainees_by_name(extracted_name, office_id, flow_id)

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
                        trainees = search_trainees_by_name(extracted_name, office_id, flow_id)

            if not trainees:
                return None

        if len(trainees) == 1:
            slots["user_id"] = trainees[0]["value"]
            slot_labels["user_id"] = trainees[0]["label"]
        else:
            slots["trainee_name"] = extracted_name
            state = create_or_update_state(session_id, {
                "flow_id": flow_id,
                "module": flow_def["module"],
                "original_question": message,
                "collected_slots": slots,
                "slot_labels": {},
                "missing_slots": flow_def["slots_order"][:],
            })
            options = trainees[:10]
            if len(trainees) > 10:
                options.append({"value": "LOAD_MORE_OPTIONS", "label": "➡️ Show Next 10"})
            options.append({"_pagination": {"total_count": len(trainees), "limit": 10, "offset": 0}})
            
            return {
                "type": "follow_up",
                "message": f'I found multiple people matching "{extracted_name}". Which one do you mean?',
                "session_id": session_id,
                "flow_id": flow_id,
                "slot_key": "user_id",
                "options": options,
                "search_term": extracted_name,
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
    from app.services.guided_modules.library_guided import LIBRARY_FLOWS
    from app.services.guided_modules.mess_guided import MESS_FLOWS
    from app.services.guided_modules.vehicle_guided import VEHICLE_FLOWS
    flow_def = _get_guided_flow_definition(flow_id)
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

    if value in ("LOAD_MORE_OPTIONS", "LOAD_PREV_OPTIONS", "LOAD_PAGE_OPTIONS"):
        slots = state.get("collected_slots", {})
        # Recover trainee_name from selected_option or original question if state was cleared
        if slot_key == "user_id" and not slots.get("trainee_name"):
            search_term = selected_option.get("search_term", "")
            if search_term:
                slots["trainee_name"] = search_term
            else:
                orig_q = state.get("original_question", "")
                recovered_name = _extract_name(orig_q) if orig_q else None
                if recovered_name:
                    slots["trainee_name"] = recovered_name
        if value == "LOAD_PAGE_OPTIONS":
            # Direct page navigation: page_offset is the target offset sent from frontend
            slots[f"{slot_key}_offset"] = int(selected_option.get("page_offset", 0))
        elif value == "LOAD_MORE_OPTIONS":
            slots[f"{slot_key}_offset"] = slots.get(f"{slot_key}_offset", 0) + 10
        else:
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

        # Strip _pagination metadata entry and nav-only buttons for selection logic
        real_options = [o for o in options if "value" in o and o["value"] not in ("LOAD_MORE_OPTIONS", "LOAD_PREV_OPTIONS")]

        if len(real_options) == 0:
            continue
        if len(real_options) == 1:
            slots[slot_key] = real_options[0]["value"]
            slot_labels[slot_key] = real_options[0]["label"]
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
            "search_term": slots.get("trainee_name", "") if slot_key == "user_id" else "",
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
    elif flow_def.get("module") == "library":
        try:
            from app.services.guided_access_policy import can_access_guided_flow
            if not can_access_guided_flow(role, "library", flow_id, slots, office_id):
                return {"type": "text", "message": "You do not have permission to access this library information."}
        except ImportError:
            pass
            
        print(f"[Library Guided] Executing: {flow_id} with slots: {slots}")
        from app.services.guided_modules.library_executor import execute_library_guided_query
        result = execute_library_guided_query(
            flow_id=flow_id, slots=slots, office_id=office_id,
            role=role, session_id=session_id,
            user_question=original_question, base_url=base_url,
        )
    elif flow_def.get("module") == "mess":
        try:
            from app.services.guided_access_policy import can_access_guided_flow
            allowed = can_access_guided_flow(role, "mess", flow_id, slots, office_id)
            if not allowed:
                return {"type": "text", "message": "You do not have permission to access this mess information.", "response_mode": "chat", "rows": [], "row_count": 0}
        except ImportError:
            pass
            
        print(f"[Mess Guided] Executing: {flow_id} with slots: {slots}")
        from app.services.guided_modules.mess_executor import execute_mess_guided_query
        result = execute_mess_guided_query(
            flow_id=flow_id, slots=slots, office_id=office_id,
            role=role, session_id=session_id,
            user_question=original_question, base_url=base_url,
        )
    elif flow_def.get("module") == "vehicle":
        try:
            from app.services.guided_access_policy import can_access_guided_flow
            allowed = can_access_guided_flow(role, "vehicle", flow_id, slots, office_id)
            if not allowed:
                return {"type": "text", "message": "You do not have permission to access vehicle information.", "response_mode": "chat", "rows": [], "row_count": 0}
        except ImportError:
            pass
            
        print(f"[Vehicle Guided] Executing: {flow_id} with slots: {slots}")
        from app.services.guided_modules.vehicle_executor import execute_vehicle_guided_query
        result = execute_vehicle_guided_query(
            flow_id=flow_id, slots=slots, office_id=office_id,
            role=role, session_id=session_id,
            user_question=original_question, base_url=base_url,
        )
    elif flow_def.get("module") == "meeting":
        try:
            from app.services.guided_access_policy import can_access_guided_flow
            allowed = can_access_guided_flow(role, "meeting", flow_id, slots, office_id)
            if not allowed:
                return {"type": "text", "message": "You do not have permission to access meeting information.", "response_mode": "chat", "rows": [], "row_count": 0}
        except ImportError:
            pass
        print(f"[Meeting Guided] Executing: {flow_id} with slots: {slots}")
        from app.services.guided_modules.meeting_executor import execute_meeting_guided_query
        result = execute_meeting_guided_query(flow_id=flow_id, slots=slots, office_id=office_id, role=role, session_id=session_id, user_question=original_question, base_url=base_url)

    elif flow_def.get("module") == "seminar":
        try:
            from app.services.guided_access_policy import can_access_guided_flow
            allowed = can_access_guided_flow(role, "seminar", flow_id, slots, office_id)
            if not allowed:
                return {"type": "text", "message": "You do not have permission to access seminar information.", "response_mode": "chat", "rows": [], "row_count": 0}
        except ImportError:
            pass
        print(f"[Seminar Guided] Executing: {flow_id} with slots: {slots}")
        from app.services.guided_modules.seminar_executor import execute_seminar_guided_query
        result = execute_seminar_guided_query(flow_id=flow_id, slots=slots, office_id=office_id, role=role, session_id=session_id, user_question=original_question, base_url=base_url)

    elif flow_def.get("module") == "inspection":
        try:
            from app.services.guided_access_policy import can_access_guided_flow
            allowed = can_access_guided_flow(role, "inspection", flow_id, slots, office_id)
            if not allowed:
                return {"type": "text", "message": "You do not have permission to access inspection information.", "response_mode": "chat", "rows": [], "row_count": 0}
        except ImportError:
            pass
        print(f"[Inspection Guided] Executing: {flow_id} with slots: {slots}")
        from app.services.guided_modules.inspection_executor import execute_inspection_guided_query
        result = execute_inspection_guided_query(flow_id=flow_id, slots=slots, office_id=office_id, role=role, session_id=session_id, user_question=original_question, base_url=base_url)

    elif flow_def.get("module") == "sports":
        try:
            from app.services.guided_access_policy import can_access_guided_flow
            allowed = can_access_guided_flow(role, "sports", flow_id, slots, office_id)
            if not allowed:
                return {"type": "text", "message": "You do not have permission to access sports information.", "response_mode": "chat", "rows": [], "row_count": 0}
        except ImportError:
            pass
        print(f"[Sports Guided] Executing: {flow_id} with slots: {slots}")
        from app.services.guided_modules.sports_executor import execute_sports_guided_query
        result = execute_sports_guided_query(flow_id=flow_id, slots=slots, office_id=office_id, role=role, session_id=session_id, user_question=original_question, base_url=base_url)

    elif flow_def.get("module") == "pass_eq":
        try:
            from app.services.guided_access_policy import can_access_guided_flow
            allowed = can_access_guided_flow(role, "pass_eq", flow_id, slots, office_id)
            if not allowed:
                return {"type": "text", "message": "You do not have permission to access pass/EQ information.", "response_mode": "chat", "rows": [], "row_count": 0}
        except ImportError:
            pass
        print(f"[PassEQ Guided] Executing: {flow_id} with slots: {slots}")
        from app.services.guided_modules.pass_eq_executor import execute_pass_eq_guided_query
        result = execute_pass_eq_guided_query(flow_id=flow_id, slots=slots, office_id=office_id, role=role, session_id=session_id, user_question=original_question, base_url=base_url)

    elif flow_def.get("module") == "field_study_tour":
        try:
            from app.services.guided_access_policy import can_access_guided_flow
            allowed = can_access_guided_flow(role, "field_study_tour", flow_id, slots, office_id)
            if not allowed:
                return {"type": "text", "message": "You do not have permission to access field/study tour information.", "response_mode": "chat", "rows": [], "row_count": 0}
        except ImportError:
            pass
        print(f"[FieldStudyTour Guided] Executing: {flow_id} with slots: {slots}")
        from app.services.guided_modules.field_study_tour_executor import execute_field_study_tour_guided_query
        result = execute_field_study_tour_guided_query(flow_id=flow_id, slots=slots, office_id=office_id, role=role, session_id=session_id, user_question=original_question, base_url=base_url)

    elif flow_def.get("module") == "master_admin":
        try:
            from app.services.guided_access_policy import can_access_guided_flow
            allowed = can_access_guided_flow(role, "master_admin", flow_id, slots, office_id)
            if not allowed:
                return {"type": "text", "message": "You do not have permission to access master admin information.", "response_mode": "chat", "rows": [], "row_count": 0}
        except ImportError:
            pass
        print(f"[MasterAdmin Guided] Executing: {flow_id} with slots: {slots}")
        from app.services.guided_modules.master_admin_executor import execute_master_admin_guided_query
        result = execute_master_admin_guided_query(flow_id=flow_id, slots=slots, office_id=office_id, role=role, session_id=session_id, user_question=original_question, base_url=base_url)

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
    from app.services.guided_modules.library_guided import LIBRARY_FLOWS
    is_trainee_flow = flow_id in TRAINEE_FLOWS
    is_hostel_flow = flow_id in HOSTEL_FLOWS
    is_attendance_flow = flow_id in ATTENDANCE_FLOWS
    is_course_flow = flow_id in COURSE_FLOWS
    is_complaint_flow = flow_id in COMPLAINT_FLOWS
    is_timetable_flow = flow_id in TIMETABLE_FLOWS
    is_faculty_flow = flow_id in FACULTY_FLOWS
    is_library_flow = flow_id in LIBRARY_FLOWS

    user_id = slots.get("user_id")

    if slot_key == "user_id":
        tname = slots.get("trainee_name") or slots.get("faculty_name") or ""
        if tname:
            offset = slots.get("user_id_offset", 0)
            trainees = []
            if is_hostel_flow:
                from app.services.guided_modules.hostel_options import search_hostel_trainees_by_name
                trainees = search_hostel_trainees_by_name(tname, office_id)
            elif is_attendance_flow:
                from app.services.guided_modules.attendance_options import search_attendance_trainees_by_name
                trainees = search_attendance_trainees_by_name(tname, office_id)
            elif is_trainee_flow:
                from app.services.guided_modules.trainee_options import search_trainees_by_name as tr_search
                trainees = tr_search(tname, office_id)
            elif flow_id in ("mess_dues_by_trainee", "mess_bill_summary", "pending_mess_dues", "mess_receipts_by_trainee", "mess_item_summary", "mess_party_summary", "mess_refund_summary"):
                from app.services.guided_modules.mess_options import search_mess_trainees_by_name
                trainees = search_mess_trainees_by_name(tname, office_id, flow_id=flow_id)
            elif is_library_flow:
                from app.services.guided_modules.library_options import search_library_trainees_by_name
                trainees = search_library_trainees_by_name(tname, office_id)
            elif is_timetable_flow:
                from app.services.guided_modules.timetable_options import search_faculty_by_name
                trainees = search_faculty_by_name(tname, office_id)
            elif is_faculty_flow:
                from app.services.guided_modules.faculty_options import search_faculty_all
                trainees = search_faculty_all(tname, office_id)
            else:
                from app.services.option_resolver_service import search_trainees_by_name
                trainees = search_trainees_by_name(tname, office_id, flow_id)
                
            if trainees:
                options = trainees[offset:offset+10]
                if offset > 0:
                    options.insert(0, {"value": "LOAD_PREV_OPTIONS", "label": "⬅️ Show Previous 10"})
                if len(trainees) > offset + 10:
                    options.append({"value": "LOAD_MORE_OPTIONS", "label": "➡️ Show Next 10"})
                options.append({"_pagination": {"total_count": len(trainees), "limit": 10, "offset": offset}})
                return options

    if is_library_flow:
        if slot_key == "book_id" or slot_key == "book_title":
            title = slots.get("book_title") or ""
            from app.services.guided_modules.library_options import search_books_by_title
            return search_books_by_title(title, office_id)
        if slot_key == "user_id" or slot_key == "trainee_name":
            name = slots.get("trainee_name") or ""
            from app.services.guided_modules.library_options import search_library_trainees_by_name
            return search_library_trainees_by_name(name, office_id)
        if slot_key == "book_type":
            from app.services.guided_modules.library_options import get_book_types
            return get_book_types(office_id)
        if slot_key == "status":
            from app.services.guided_modules.library_options import get_library_status_options
            return get_library_status_options()
        return None

    if flow_id in ("mess_dues_by_trainee", "mess_bill_summary", "pending_mess_dues", "mess_receipts_by_trainee", "mess_item_summary", "mess_party_summary", "mess_refund_summary", "mess_material_stock", "mess_bill_count", "recent_mess_transactions", "mess_rate_card", "mess_item_rate"):
        if slot_key == "user_id" or slot_key == "trainee_name":
            name = slots.get("trainee_name") or ""
            from app.services.guided_modules.mess_options import search_mess_trainees_by_name
            return search_mess_trainees_by_name(name, office_id, flow_id=flow_id)
        if slot_key == "course_id":
            course_name = slots.get("course_name") or ""
            from app.services.guided_modules.mess_options import search_mess_courses
            return search_mess_courses(course_name, office_id)
        if slot_key == "item_id" or slot_key == "item_name":
            item_name = slots.get("item_name") or ""
            from app.services.guided_modules.mess_options import search_mess_items
            return search_mess_items(item_name, office_id)
        if slot_key == "party_id" or slot_key == "party_name":
            party_name = slots.get("party_name") or ""
            from app.services.guided_modules.mess_options import search_mess_parties
            return search_mess_parties(party_name, office_id)
        if slot_key == "month":
            from app.services.guided_modules.mess_options import get_mess_month_options
            return get_mess_month_options()
        if slot_key == "dues_status":
            from app.services.guided_modules.mess_options import get_mess_due_status_options
            return get_mess_due_status_options()
        if slot_key == "meal_item_name":
            meal_name = slots.get("meal_item_name") or ""
            from app.services.guided_modules.mess_options import search_mess_meal_items
            return search_mess_meal_items(meal_name, office_id)
        return None

    # ── Vehicle options ──
    from app.services.guided_modules.vehicle_guided import VEHICLE_FLOWS
    if flow_id in VEHICLE_FLOWS:
        if slot_key == "vehicle_id" or slot_key == "vehicle_number":
            vnum = slots.get("vehicle_number") or ""
            from app.services.guided_modules.vehicle_options import search_vehicles_by_number
            return search_vehicles_by_number(vnum, office_id)
        if slot_key == "driver_id" or slot_key == "driver_name":
            dname = slots.get("driver_name") or ""
            from app.services.guided_modules.vehicle_options import search_vehicle_drivers
            return search_vehicle_drivers(dname, office_id)
        if slot_key == "course_id":
            cname = slots.get("course_name") or ""
            from app.services.guided_modules.vehicle_options import search_vehicle_courses
            return search_vehicle_courses(cname, office_id)
        if slot_key == "tour_id":
            from app.services.guided_modules.vehicle_options import search_study_tours
            return search_study_tours("", office_id)
        if slot_key == "vehicle_type":
            from app.services.guided_modules.vehicle_options import get_vehicle_type_options
            return get_vehicle_type_options(office_id)
        if slot_key == "status":
            from app.services.guided_modules.vehicle_options import get_vehicle_status_options
            return get_vehicle_status_options()
        return None

    # ── Master Admin options ──
    from app.services.guided_modules.master_admin_guided import MASTER_ADMIN_FLOWS
    if flow_id in MASTER_ADMIN_FLOWS:
        if slot_key == "department_id":
            from app.services.guided_modules.meeting_options import search_departments
            return search_departments("", office_id)
        if slot_key == "zone_id":
            from app.services.guided_modules.master_admin_options import search_zones
            return search_zones("", office_id)
        if slot_key == "division_id":
            from app.services.guided_modules.master_admin_options import search_divisions
            return search_divisions("", office_id)
        if slot_key == "role_id":
            from app.services.guided_modules.master_admin_options import search_roles
            return search_roles("", office_id)

    # ── Field Study Tour options ──
    from app.services.guided_modules.field_study_tour_guided import FIELD_STUDY_TOUR_FLOWS
    if flow_id in FIELD_STUDY_TOUR_FLOWS:
        if slot_key == "course_id":
            from app.services.guided_modules.field_study_tour_options import search_field_training_courses
            cname = slots.get("course_name") or ""
            return search_field_training_courses(cname, office_id)
        if slot_key == "tour_id":
            from app.services.guided_modules.field_study_tour_options import search_tours
            return search_tours("", office_id)
        if slot_key == "user_id":
            tname = slots.get("trainee_name") or ""
            from app.services.guided_modules.trainee_options import search_trainees
            return search_trainees(tname, office_id)

    # ── Pass EQ options ──
    from app.services.guided_modules.pass_eq_guided import PASS_EQ_FLOWS
    if flow_id in PASS_EQ_FLOWS:
        if slot_key == "user_id":
            tname = slots.get("trainee_name") or ""
            from app.services.guided_modules.pass_eq_options import search_pass_trainees
            return search_pass_trainees(tname, office_id)

    # ── Sports options ──
    from app.services.guided_modules.sports_guided import SPORTS_FLOWS
    if flow_id in SPORTS_FLOWS:
        if slot_key == "sport_id":
            sname = slots.get("sport_name") or ""
            from app.services.guided_modules.sports_options import search_sports
            return search_sports(sname, office_id)
        if slot_key == "item_id":
            iname = slots.get("item_name") or ""
            from app.services.guided_modules.sports_options import search_sport_items
            return search_sport_items(iname, office_id)

    # ── Inspection options ──
    from app.services.guided_modules.inspection_guided import INSPECTION_FLOWS
    if flow_id in INSPECTION_FLOWS:
        if slot_key == "inspection_id":
            from app.services.guided_modules.inspection_options import search_inspections
            return search_inspections("", office_id)
        if slot_key == "department_id":
            from app.services.guided_modules.meeting_options import search_departments
            return search_departments("", office_id)

    # ── Seminar options ──
    from app.services.guided_modules.seminar_guided import SEMINAR_FLOWS
    if flow_id in SEMINAR_FLOWS:
        if slot_key == "seminar_id":
            from app.services.guided_modules.seminar_options import search_seminars
            return search_seminars(slots.get("seminar_title") or "", office_id)
        if slot_key == "department_id":
            from app.services.guided_modules.meeting_options import search_departments
            return search_departments("", office_id)

    # ── Meeting options ──
    from app.services.guided_modules.meeting_guided import MEETING_FLOWS
    if flow_id in MEETING_FLOWS:
        if slot_key == "meeting_id":
            from app.services.guided_modules.meeting_options import search_meetings
            return search_meetings(slots.get("meeting_title") or "", office_id)
        if slot_key == "department_id":
            from app.services.guided_modules.meeting_options import search_departments
            dname = slots.get("department_name") or ""
            return search_departments(dname, office_id)

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
            return get_recent_timetable_courses(office_id, offset=slots.get(f"{slot_key}_offset", 0))
            
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
            return get_recent_faculty_courses(office_id, offset=slots.get(f"{slot_key}_offset", 0))
            
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
        return options

    # ── Non-trainee exam flows: course selection ──
    if slot_key == "course_id" and not user_id:
        options = get_recent_courses_for_exam(office_id, limit=10, offset=slots.get(f"{slot_key}_offset", 0), flow_id=flow_id)
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
        ("hostel_full_rooms", "building_id"): "Which hostel building?",
        ("hostel_trainees_by_building", "building_id"): "Which hostel building?",
        ("hostel_building_summary", "building_id"): "Which hostel building?",
        ("hostel_vacant_beds_by_building", "building_id"): "Which hostel building?",
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
        # Library guided module
        ("book_search", "book_title"): "Which book do you want to search?",
        ("book_search", "book_id"): "I found multiple matching books. Please select one:",
        ("book_availability", "book_title"): "Which book's availability do you want to check?",
        ("book_availability", "book_id"): "I found multiple matching books. Please select one:",
        ("issued_books_by_trainee", "trainee_name"): "Whose issued books do you want to see?",
        ("issued_books_by_trainee", "user_id"): "I found multiple trainees. Please select one:",
        ("book_issue_history", "book_title"): "Which book's issue history do you want?",
        ("book_issue_history", "book_id"): "I found multiple matching books. Please select one:",
        ("overdue_books", "user_id"): "I found multiple trainees with that name. Please select one:",
        ("pending_book_returns", "user_id"): "I found multiple trainees with that name. Please select one:",
        # Mess guided module
        ("mess_dues_by_trainee", "user_id"): "I found multiple trainees with that name. Please select one:",
        ("mess_dues_by_trainee", "trainee_name"): "Whose mess dues do you want to check?",
        ("mess_receipts_by_trainee", "user_id"): "I found multiple trainees with that name. Please select one:",
        ("mess_receipts_by_trainee", "trainee_name"): "Whose mess receipts do you want to see?",
        ("mess_refund_summary", "user_id"): "I found multiple trainees with that name. Please select one:",
        ("mess_refund_summary", "trainee_name"): "Whose mess refund do you want to check?",
        ("mess_bill_summary", "course_id"): "Which course or batch?",
        ("mess_bill_summary", "month"): "Which month?",
        ("mess_bill_summary", "year"): "Which year?",
        ("pending_mess_dues", "course_id"): "Which course or batch?",
        ("mess_item_summary", "item_id"): "Which mess item?",
        ("mess_item_summary", "item_name"): "Which mess item?",
        ("mess_party_summary", "party_id"): "Which vendor/party?",
        ("mess_party_summary", "party_name"): "Which vendor/party?",
        ("mess_material_stock", "item_id"): "Which mess item?",
        ("mess_material_stock", "item_name"): "Which mess item?",
        ("mess_rate_card", "meal_item_name"): "Which meal item do you want the rate for?",
        ("mess_item_rate", "meal_item_name"): "Which meal item do you want the rate for?",
        # Vehicle guided module
        ("vehicle_register_history", "vehicle_number"): "Which vehicle?",
        ("vehicle_register_history", "vehicle_id"): "Which vehicle?",
        ("vehicle_maintenance", "vehicle_number"): "Which vehicle's maintenance records?",
        ("vehicle_maintenance", "vehicle_id"): "Which vehicle?",
        ("vehicle_by_driver", "driver_name"): "Which driver?",
        ("vehicle_by_driver", "driver_id"): "Which driver?",
        ("study_tour_vehicle_usage", "course_id"): "Which course/batch?",
        ("study_tour_vehicle_usage", "tour_id"): "Which study tour?",
        ("field_training_vehicle_usage", "course_id"): "Which course/batch?",
        ("field_training_vehicle_usage", "field_training_id"): "Which field training?",
        ("vehicle_list", "vehicle_type"): "Which type of vehicle?",
        ("vehicle_list", "status"): "Which booking status?",
        ("vehicle_availability", "vehicle_type"): "Which type of vehicle?",
        ("vehicle_count", "vehicle_type"): "Which type of vehicle?",
        
        # Meeting Guided Module
        ("meeting_details_by_id", "meeting_id"): "Which meeting?",
        ("meeting_agenda", "meeting_id"): "Which meeting agenda?",
        ("meeting_participants", "meeting_id"): "Which meeting participants?",
        ("upcoming_meetings", "department_id"): "Which department?",
        ("meeting_by_department", "department_id"): "Which department?",
        
        # Seminar Guided Module
        ("seminar_details", "seminar_id"): "Which seminar?",
        ("seminar_topics", "seminar_id"): "Which seminar topics?",
        ("seminar_participants", "seminar_id"): "Which seminar participants?",
        ("upcoming_seminars", "department_id"): "Which department?",
        ("department_wise_seminars", "department_id"): "Which department?",
        
        # Inspection Guided Module
        ("inspection_details", "inspection_id"): "Which inspection note?",
        ("inspection_notes", "department_id"): "Which department?",
        ("pending_inspections", "department_id"): "Which department?",
        ("resolved_inspections", "department_id"): "Which department?",
        ("inspection_by_department", "department_id"): "Which department?",
        ("inspection_action_items", "department_id"): "Which department?",
        
        # Sports Guided Module
        ("sports_events", "sport_id"): "Which sport?",
        ("sports_participants", "sport_id"): "Which sport?",
        ("sports_team_details", "team_id"): "Which team?",
        ("sports_item_stock", "item_id"): "Which sports item?",
        ("sports_material_summary", "item_id"): "Which sports item?",
        ("sports_item_issues", "user_id"): "Which user/trainee?",
        ("sports_by_course", "course_id"): "Which course?",
        ("sports_winners", "sport_id"): "Which sport?",
        
        # Pass EQ Guided Module
        ("pass_by_trainee", "user_id"): "Which trainee?",
        ("eq_by_trainee", "user_id"): "Which trainee?",
        ("pending_passes", "course_id"): "Which course?",
        ("issued_passes", "course_id"): "Which course?",
        ("pending_eqs", "course_id"): "Which course?",
        
        # Field Study Tour Guided Module
        ("field_training_list", "course_id"): "Which course?",
        ("field_training_by_course", "course_id"): "Which course?",
        ("study_tour_list", "course_id"): "Which course?",
        ("study_tour_by_course", "course_id"): "Which course?",
        ("trainee_field_training", "user_id"): "Which trainee?",
        ("trainee_study_tour", "user_id"): "Which trainee?",
        ("tour_vehicle_details", "tour_id"): "Which study tour?",
        
        # Master Admin Guided Module
        ("designation_list", "department_id"): "Which department?",
        ("division_list", "zone_id"): "Which railway zone?",
        ("station_list", "division_id"): "Which division?",
        ("user_role_summary", "role_id"): "Which role?",
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
    elif flow_id in ("issued_books_by_trainee", "overdue_books", "pending_book_returns") and slot_key == "user_id":
        t_name = slots.get("trainee_name")
        if t_name:
            question = f"I found multiple trainees matching '{t_name}'. Please select one:"
    elif flow_id in ("book_search", "book_availability", "book_issue_history") and slot_key == "book_id":
        b_title = slots.get("book_title")
        if b_title:
            question = f"I found multiple books matching '{b_title}'. Please select one:"
    elif flow_id in ("mess_dues_by_trainee", "mess_receipts_by_trainee", "mess_refund_summary") and slot_key == "user_id":
        t_name = slots.get("trainee_name")
        if t_name:
            question = f"I found multiple trainees matching '{t_name}'. Please select one:"
    elif flow_id in ("mess_item_summary", "mess_material_stock") and slot_key in ("item_id", "item_name"):
        i_name = slots.get("item_name")
        if i_name:
            question = f"I found multiple mess items matching '{i_name}'. Please select one:"
    elif flow_id == "mess_party_summary" and slot_key in ("party_id", "party_name"):
        p_name = slots.get("party_name")
        if p_name:
            question = f"I found multiple vendors/parties matching '{p_name}'. Please select one:"
    elif flow_id in ("vehicle_register_history", "vehicle_maintenance") and slot_key in ("vehicle_number", "vehicle_id"):
        v_num = slots.get("vehicle_number")
        if v_num:
            question = f"I found multiple vehicles matching '{v_num}'. Please select one:"
    elif flow_id == "vehicle_by_driver" and slot_key in ("driver_name", "driver_id"):
        d_name = slots.get("driver_name")
        if d_name:
            question = f"I found multiple drivers matching '{d_name}'. Please select one:"
    elif flow_id in ("study_tour_vehicle_usage", "field_training_vehicle_usage") and slot_key == "course_id":
        c_name = slots.get("course_name")
        if c_name:
            question = f"I found multiple courses matching '{c_name}'. Please select one:"
    
    return question
