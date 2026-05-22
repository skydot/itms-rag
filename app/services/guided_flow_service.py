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
    "hostel_availability": {
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
    if re.search(r"which\s+room|room\s+.*staying|hostel\s+room|staying\s+in|room\s+of\b|room\s+allot", text):
        if _extract_name(message):
            return "hostel_room_of_trainee"

    if re.search(r"available\s+room|available\s+bed|hostel\s+availability|vacant\s+room|vacant\s+bed|empty\s+room", text):
        return "hostel_availability"

    if re.search(r"dues|pending\b.*dues|hostel\b.*dues|mess\b.*dues|library\b.*dues", text):
        if _extract_name(message):
            return "pending_dues_by_person"

    if re.search(r"attendance", text):
        if _extract_name(message):
            return "attendance_by_trainee"

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

    # ── CASE 3: Rule-based detection first (fast) ──
    normalized_msg = _normalize_typos(message)
    flow_id = _match_flow_rules(normalized_msg)
    slots = {}
    extracted_name = None

    print(f"[Exam Guided] Message: {message}")
    print(f"[Exam Guided] Rule-matched flow: {flow_id}")

    # ── CASE 4: LLM fallback if rules didn't match ──
    if not flow_id:
        from app.services.guided_intent_parser import parse_guided_intent
        parsed = parse_guided_intent(message)
        if parsed.get("matches_guided_flow"):
            flow_id = parsed.get("flow_id")
            if flow_id in GUIDED_FLOWS:
                llm_slots = parsed.get("slots", {})
                extracted_name = llm_slots.get("trainee_name")
                if llm_slots.get("exam_filter"):
                    slots["exam_filter"] = llm_slots["exam_filter"]
                if llm_slots.get("dues_type"):
                    slots["dues_type"] = llm_slots["dues_type"]
                if llm_slots.get("limit"):
                    try:
                        slots["limit"] = int(llm_slots["limit"])
                    except (ValueError, TypeError):
                        pass
            else:
                flow_id = None

    if not flow_id:
        return None

    print(f"[Exam Guided] Flow: {flow_id}")

    flow_def = GUIDED_FLOWS[flow_id]

    # Extract slots from message
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

    print(f"[Exam Guided] Slots: {slots}")

    slot_labels = {}

    # ── For name-based flows: resolve trainee first ──
    if flow_def["requires_name"] and extracted_name:
        trainees = search_trainees_by_name(extracted_name, office_id)

        if not trainees:
            from app.services.guided_intent_parser import parse_guided_intent
            parsed = parse_guided_intent(message)
            if parsed.get("matches_guided_flow"):
                llm_slots = parsed.get("slots", {})
                new_name = llm_slots.get("trainee_name")
                if new_name and new_name.lower() != extracted_name.lower():
                    extracted_name = new_name
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

    # ── For hostel_availability: check building ──
    if flow_id == "hostel_availability":
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

    # ── For pending_dues: check if dues type already specified ──
    if flow_id == "pending_dues_by_person":
        detected_type = _detect_dues_type(message)
        if detected_type:
            slots["dues_type"] = detected_type
            slot_labels["dues_type"] = detected_type.title() + " dues"

    # ── Now check next missing slot ──
    return _check_next_slot(
        flow_id, flow_def, slots, slot_labels, office_id,
        session_id, message, base_url
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

    flow_def = GUIDED_FLOWS.get(flow_id)
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

    update_slot(session_id, slot_key, value, label)
    state = get_state(session_id)

    slots = state.get("collected_slots", {})
    slot_labels = state.get("slot_labels", {})
    original_question = state.get("original_question", message)

    return _check_next_slot(
        flow_id, flow_def, slots, slot_labels, office_id,
        session_id, original_question, base_url
    )


def _check_next_slot(
    flow_id: str, flow_def: dict, slots: dict, slot_labels: dict,
    office_id: int, session_id: str, original_question: str, base_url: str,
) -> Optional[dict]:
    """Check which slot is next to fill, ask follow-up, or execute query."""
    slots_order = flow_def["slots_order"]

    for slot_key in slots_order:
        if slot_key in slots:
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
            print(f"[Exam Guided] Auto-resolved {slot_key} to {matched_option['value']} from text match")
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

        question_text = _get_follow_up_question(flow_id, slot_key)
        print(f"[Exam Guided] Next follow-up: {slot_key}")
        return {
            "type": "follow_up",
            "message": question_text,
            "session_id": session_id,
            "flow_id": flow_id,
            "slot_key": slot_key,
            "options": options[:15],
        }

    # ── All slots filled — execute query ──
    clear_state(session_id)
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
    user_id = slots.get("user_id")

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


def _get_follow_up_question(flow_id: str, slot_key: str) -> str:
    """Get the human-readable follow-up question for a slot."""
    questions = {
        # Trainee-specific
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
        ("hostel_availability", "building_id"): "Which hostel building?",
        ("attendance_by_trainee", "user_id"): "Which trainee do you mean?",
        ("attendance_by_trainee", "course_id"): "Which course/batch?",
    }
    return questions.get((flow_id, slot_key), f"Please select {slot_key.replace('_', ' ')}:")
