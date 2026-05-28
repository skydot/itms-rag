"""Course guided flow — rule-based detection, typo normalization, slot extraction.

Returns a flow detection dict or None if no course flow matched.
"""

import re
from datetime import datetime
from typing import Optional, Dict, Any


# ═══════════════════════════════════════════════════════════════════
# Course-specific typo normalization
# ═══════════════════════════════════════════════════════════════════

_COURSE_TYPO_MAP = {
    r"\bcoures\b": "course",
    r"\bcoursee\b": "course",
    r"\bcources\b": "courses",
    r"\btraning\b": "training",
    r"\btrainig\b": "training",
    r"\bbatchh\b": "batch",
    r"\bcurent\b": "current",
    r"\bcurrnt\b": "current",
    r"\blattest\b": "latest",
    r"\bletest\b": "latest",
    r"\bupcomming\b": "upcoming",
    r"\bupcomng\b": "upcoming",
    r"\bcompletedd\b": "completed",
    r"\bfinshed\b": "finished",
    r"\bfinishd\b": "finished",
    r"\bplaned\b": "planned",
    r"\brunning\b": "running",
    r"\bruning\b": "running",
    r"\bschedule\b": "schedule",
    r"\bschdule\b": "schedule",
    r"\bstudnts\b": "students",
    r"\bstudnet\b": "student",
    r"\btaines\b": "trainees",
    r"\btaine\b": "trainee",
    r"\btrainnes\b": "trainees",
    r"\bstrenth\b": "strength",
    r"\bstrenght\b": "strength",
    r"\bduration\b": "duration",
    r"\bduraton\b": "duration",
    r"\bcalender\b": "calendar",
    r"\bcalendar\b": "calendar",
    r"\bsummery\b": "summary",
    r"\bsummry\b": "summary",
}


def normalize_course_message(message: str) -> str:
    """Apply course-specific typo corrections."""
    text = message
    for pattern, replacement in _COURSE_TYPO_MAP.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


# ═══════════════════════════════════════════════════════════════════
# Course flow definitions (used by guided_flow_service)
# ═══════════════════════════════════════════════════════════════════

COURSE_FLOWS = {
    "current_courses": {
        "module": "course",
        "requires_name": False,
        "slots_order": [],
    },
    "latest_course": {
        "module": "course",
        "requires_name": False,
        "slots_order": [],
    },
    "upcoming_courses": {
        "module": "course",
        "requires_name": False,
        "slots_order": [],
    },
    "completed_courses": {
        "module": "course",
        "requires_name": False,
        "slots_order": [],
    },
    "course_details_by_name": {
        "module": "course",
        "requires_name": False,
        "slots_order": ["course_id"],
    },
    "course_trainee_count": {
        "module": "course",
        "requires_name": False,
        "slots_order": ["course_id"],
    },
    "course_wise_trainee_count": {
        "module": "course",
        "requires_name": False,
        "slots_order": [],
    },
    "course_duration_summary": {
        "module": "course",
        "requires_name": False,
        "slots_order": ["course_id"],
    },
    "batch_details": {
        "module": "course",
        "requires_name": False,
        "slots_order": ["course_id"],
    },
    "course_calendar_summary": {
        "module": "course",
        "requires_name": False,
        "slots_order": [],
    },
}


# ═══════════════════════════════════════════════════════════════════
# Slot extraction helpers
# ═══════════════════════════════════════════════════════════════════

_COURSE_STOP_WORDS = {
    "show", "list", "get", "find", "what", "which", "who", "how",
    "many", "is", "are", "the", "of", "for", "in", "a", "an", "and",
    "to", "from", "with", "by", "on", "at", "all", "my", "me", "i",
    "course", "courses", "batch", "batches", "training", "program",
    "programs", "current", "ongoing", "running", "latest", "recent",
    "upcoming", "future", "planned", "completed", "finished", "past",
    "details", "detail", "about", "information", "info",
    "trainee", "trainees", "student", "students", "strength",
    "count", "number", "total", "how", "much",
    "please", "tell", "give", "show", "check",
    "calendar", "schedule", "summary", "wise", "report",
    "duration", "start", "end", "date", "dates",
    "year", "month", "week", "this", "that",
    "do", "does", "has", "have", "been", "was", "were",
    "or", "not", "there", "will", "would", "can",
}

_MONTH_MAP = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
    "jun": 6, "jul": 7, "aug": 8, "sep": 9,
    "oct": 10, "nov": 11, "dec": 12,
}


def _extract_year(message: str) -> Optional[int]:
    """Extract 4-digit year from message."""
    m = re.search(r"\b(20[1-3]\d)\b", message)
    if m:
        return int(m.group(1))
    text = message.lower()
    if re.search(r"\bthis\s+year\b", text):
        return datetime.now().year
    if re.search(r"\blast\s+year\b|\bprevious\s+year\b", text):
        return datetime.now().year - 1
    return None


def _extract_month(message: str) -> Optional[int]:
    """Extract month number from message."""
    text = message.lower()
    for name, num in _MONTH_MAP.items():
        if re.search(rf"\b{name}\b", text):
            return num
    return None


def _extract_recent_filter(message: str) -> Optional[str]:
    """Extract recent/latest/current/ongoing filter."""
    text = message.lower()
    if re.search(r"\blatest\b|\brecent\b|\blast\s+started\b", text):
        return "latest"
    if re.search(r"\bcurrent\b|\bongoing\b|\brunning\b", text):
        return "current"
    return None


def _extract_status(message: str) -> Optional[str]:
    """Extract course status filter."""
    text = message.lower()
    if re.search(r"\bcurrent\b|\bongoing\b|\brunning\b", text):
        return "current"
    if re.search(r"\bupcoming\b|\bfuture\b|\bplanned\b", text):
        return "upcoming"
    if re.search(r"\bcompleted\b|\bfinished\b|\bpast\b", text):
        return "completed"
    return None


def _extract_course_name(message: str) -> Optional[str]:
    """Extract course name from the message.
    Looks for patterns like:
    - 'details of HR-LDCE'
    - 'HR-LDCE course details'
    - 'students in OS/S&W refresher'
    - 'duration of HR-LDCE'
    """
    # Pattern: preposition + course name (e.g. "details of HR-LDCE", "in OS/S&W")
    m = re.search(
        r"(?:of|in|for|about)\s+([A-Z][A-Za-z0-9/&\-\s]+?)(?:\s+(?:course|batch|training|details|duration|students|trainees|count)|$|\?)",
        message,
        re.IGNORECASE,
    )
    if m:
        candidate = m.group(1).strip().rstrip("?.,;:! ")
        if candidate.lower() not in _COURSE_STOP_WORDS and len(candidate) > 1:
            return candidate

    # Pattern: course name at start + course/batch/details (e.g. "HR-LDCE course details")
    m = re.search(
        r"^(?:show\s+|list\s+|get\s+)?([A-Z][A-Za-z0-9/&\-]+(?:\s+[A-Za-z0-9/&\-]+)*?)\s+(?:course|batch|training)\s+(?:details|information|info|duration)",
        message,
        re.IGNORECASE,
    )
    if m:
        candidate = m.group(1).strip()
        if candidate.lower() not in _COURSE_STOP_WORDS and len(candidate) > 1:
            return candidate

    return None


# ═══════════════════════════════════════════════════════════════════
# Rule-based course flow detection
# ═══════════════════════════════════════════════════════════════════

def detect_course_guided_flow(message: str) -> Optional[Dict[str, Any]]:
    """Detect if message matches a course guided flow.

    Returns a detection dict or None if no match.
    """
    text = normalize_course_message(message.lower().strip())

    print(f"[Course Guided] Message: {message}")

    # ── DISAMBIGUATION: Do NOT capture exam / attendance / hostel / pure trainee ──
    if re.search(r"marks|result\b|exam\b|pass\b|fail|subject\b|score\b|grade\b|topper|re-exam|reexam", text):
        print("[Course Guided] Skipped — exam/marks context detected")
        return None
    if re.search(r"attendance|present\b|absent\b|punch|biometric", text):
        print("[Course Guided] Skipped — attendance context detected")
        return None
    if re.search(r"hostel\b|room\b|bed\b|staying|dues\b|allot", text):
        print("[Course Guided] Skipped — hostel context detected")
        return None

    # Must have course/batch/training context
    has_course_context = bool(re.search(
        r"course|batch|training\s+program|training\s+calendar|duration|schedule",
        text
    ))
    if not has_course_context:
        print("[Course Guided] Skipped — no course context found")
        return None

    # Build common slots
    slots: Dict[str, Any] = {
        "course_name": None,
        "course_id": None,
        "recent_filter": None,
        "year": None,
        "month": None,
        "status": None,
    }

    # Extract slots
    year = _extract_year(message)
    if year:
        slots["year"] = year

    month = _extract_month(message)
    if month:
        slots["month"] = month

    recent_filter = _extract_recent_filter(message)
    if recent_filter:
        slots["recent_filter"] = recent_filter

    status = _extract_status(message)
    if status:
        slots["status"] = status

    course_name = _extract_course_name(message)
    if course_name:
        slots["course_name"] = course_name

    # ── Flow matching (order matters: specific before generic) ──

    # 1. course calendar / training calendar / month wise / year wise courses
    if re.search(r"(course|training)\s+calendar|month\s+wise\s+course|year\s+wise\s+course|how\s+many\s+courses?\s+in\s+\d{4}", text):
        return _build_result("course_calendar_summary", slots,
                             "matched course calendar summary pattern")

    # 2. course wise / batch wise + trainee/student/count/strength
    if re.search(r"(course|batch)\s+wise\s+(trainee|student|count|strength|trainees|students)", text):
        return _build_result("course_wise_trainee_count", slots,
                             "matched course wise trainee count pattern")

    # 3. duration / start date / end date
    if re.search(r"duration|start\s+date|end\s+date|from\s+date|to\s+date|start\s+and\s+end", text):
        if re.search(r"course|batch|training", text):
            return _build_result("course_duration_summary", slots,
                                 "matched course duration summary pattern")

    # 4. batch details / batch information
    if re.search(r"batch\s+details|batch\s+information|batch\s+info", text):
        return _build_result("batch_details", slots,
                             "matched batch details pattern")

    # 5. course details / details of / tell me about + course/batch
    if re.search(r"course\s+details|details\s+of\b|tell\s+me\s+about|course\s+information|course\s+info", text):
        if re.search(r"course|batch|training", text):
            return _build_result("course_details_by_name", slots,
                                 "matched course details pattern")

    # 6. how many trainees/students + in + course/batch
    if re.search(r"(?:how\s+many|count|number\s+of|total)\s+(?:trainee|student|trainees|students)", text):
        if re.search(r"(?:in|of|for)\s+", text) and re.search(r"course|batch|training", text):
            return _build_result("course_trainee_count", slots,
                                 "matched course trainee count pattern")
        if re.search(r"latest|current|recent", text):
            return _build_result("course_trainee_count", slots,
                                 "matched course trainee count with recent filter")

    # 7. student/trainee + count/strength + in course/batch
    if re.search(r"(trainee|student)\s+(count|strength|number)", text):
        if re.search(r"latest|current|recent|course|batch", text):
            return _build_result("course_trainee_count", slots,
                                 "matched trainee count in course/batch pattern")

    # 8. current / ongoing / running + course/batch/training
    if re.search(r"current|ongoing|running", text) and re.search(r"course|batch|training", text):
        # But not if asking details of current course
        if re.search(r"details|information|info", text):
            slots["recent_filter"] = "current"
            return _build_result("course_details_by_name", slots,
                                 "matched current course details")
        return _build_result("current_courses", slots,
                             "matched current courses pattern")

    # 9. upcoming / future / planned + course/batch/training
    if re.search(r"upcoming|future|planned", text) and re.search(r"course|batch|training", text):
        return _build_result("upcoming_courses", slots,
                             "matched upcoming courses pattern")

    # 10. completed / finished / past + course/batch
    if re.search(r"completed|finished|past", text) and re.search(r"course|batch|training", text):
        return _build_result("completed_courses", slots,
                             "matched completed courses pattern")

    # 11. latest / recent / last started + course/batch
    if re.search(r"latest|recent|last\s+started", text) and re.search(r"course|batch|training", text):
        # But not if asking details of latest course
        if re.search(r"details|information|info", text):
            slots["recent_filter"] = "latest"
            return _build_result("course_details_by_name", slots,
                                 "matched latest course details")
        return _build_result("latest_course", slots,
                             "matched latest course pattern")

    print("[Course Guided] No flow matched")
    return None


def _build_result(flow_id: str, slots: dict, reason: str) -> dict:
    """Build standard detection result dict."""
    print(f"[Course Guided] Flow: {flow_id}")
    print(f"[Course Guided] Slots: {slots}")
    return {
        "flow_id": flow_id,
        "module": "course",
        "slots": slots,
        "reason": reason,
    }
