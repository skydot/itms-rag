"""Attendance guided flow — rule-based detection, typo normalization, slot extraction.

Returns a flow detection dict or None if no attendance flow matched.
"""

import re
from datetime import datetime
from typing import Optional, Dict, Any


# ═══════════════════════════════════════════════════════════════════
# Attendance-specific typo normalization
# ═══════════════════════════════════════════════════════════════════

_ATTENDANCE_TYPO_MAP = {
    r"\battendence\b": "attendance",
    r"\battandance\b": "attendance",
    r"\battendace\b": "attendance",
    r"\battendanc\b": "attendance",
    r"\battandence\b": "attendance",
    r"\babscent\b": "absent",
    r"\babesent\b": "absent",
    r"\babsnt\b": "absent",
    r"\bpresnt\b": "present",
    r"\bpersent\b": "present",
    r"\bpresant\b": "present",
    r"\bpercantage\b": "percentage",
    r"\bpercentge\b": "percentage",
    r"\bpercntage\b": "percentage",
    r"\btaines\b": "trainees",
    r"\btaine\b": "trainee",
    r"\btrainnes\b": "trainees",
    r"\bstudnts\b": "students",
    r"\bstdent\b": "student",
    r"\bstdents\b": "students",
    r"\bcorse\b": "course",
    r"\bbatch\b": "batch",
}


def normalize_attendance_message(message: str) -> str:
    """Apply attendance-specific typo corrections."""
    text = message
    for pattern, replacement in _ATTENDANCE_TYPO_MAP.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


# ═══════════════════════════════════════════════════════════════════
# Attendance flow definitions (used by guided_flow_service)
# ═══════════════════════════════════════════════════════════════════

ATTENDANCE_FLOWS = {
    "attendance_by_trainee": {
        "module": "attendance",
        "requires_name": True,
        "slots_order": ["user_id", "course_id"],
    },
    "attendance_percentage_by_trainee": {
        "module": "attendance",
        "requires_name": True,
        "slots_order": ["user_id", "course_id"],
    },
    "absent_trainees": {
        "module": "attendance",
        "requires_name": False,
        "slots_order": ["course_id"],
    },
    "present_trainees": {
        "module": "attendance",
        "requires_name": False,
        "slots_order": ["course_id"],
    },
    "course_attendance_summary": {
        "module": "attendance",
        "requires_name": False,
        "slots_order": ["course_id"],
    },
    "low_attendance_trainees": {
        "module": "attendance",
        "requires_name": False,
        "slots_order": ["threshold", "course_id"],
    },
    "date_wise_attendance": {
        "module": "attendance",
        "requires_name": False,
        "slots_order": ["course_id"],
    },
    "trainee_absent_count": {
        "module": "attendance",
        "requires_name": True,
        "slots_order": ["user_id"],
    },
    "trainee_present_count": {
        "module": "attendance",
        "requires_name": True,
        "slots_order": ["user_id"],
    },
    "batch_attendance_report": {
        "module": "attendance",
        "requires_name": False,
        "slots_order": ["course_id"],
    },
}


# ═══════════════════════════════════════════════════════════════════
# Slot extraction helpers
# ═══════════════════════════════════════════════════════════════════

_ATTENDANCE_STOP_WORDS = {
    "show", "list", "get", "find", "what", "which", "who", "how",
    "many", "is", "are", "the", "of", "for", "in", "a", "an", "and",
    "to", "from", "with", "by", "on", "at", "all", "my", "me", "i",
    "attendance", "present", "absent", "punch", "biometric",
    "trainee", "trainees", "student", "students", "trainee's",
    "course", "courses", "batch", "batches",
    "please", "tell", "give", "details", "detail", "about",
    "total", "count", "number", "check", "summary", "wise",
    "percentage", "percent", "ratio", "rate",
    "days", "day", "date", "today", "yesterday",
    "recent", "latest", "current", "ongoing", "last",
    "report", "low", "below", "less", "than",
    "do", "does", "has", "have", "been", "was", "were", "did",
    "or", "not", "there", "will", "would", "can", "much",
    "we", "us", "our", "this", "that", "those", "these",
}


def _extract_attendance_trainee_name(message: str) -> Optional[str]:
    """Extract a potential person name from an attendance context message."""
    text = re.sub(r'[?!.,;:\'\"()\[\]{}]', ' ', message.strip())
    words = text.split()
    name_parts = []
    for word in words:
        if word.lower() in _ATTENDANCE_STOP_WORDS:
            continue
        if word.isdigit():
            continue
        if len(word) <= 1:
            continue
        # Skip date-like tokens
        if re.match(r"^\d{4}-\d{2}-\d{2}$", word):
            continue
        name_parts.append(word)
    if name_parts:
        return " ".join(name_parts)
    return None


def _extract_threshold(message: str) -> Optional[int]:
    """Extract attendance threshold from patterns like 'below 75', 'less than 80%'."""
    m = re.search(r"(?:below|less\s+than|under|<)\s*(\d{1,3})\s*%?", message, re.IGNORECASE)
    if m:
        return int(m.group(1))
    m = re.search(r"(\d{1,3})\s*%?\s*(?:attendance|percent|percentage)", message, re.IGNORECASE)
    if m:
        val = int(m.group(1))
        if val <= 100:
            return val
    return None


def _extract_date(message: str) -> Optional[str]:
    """Extract date from message. Returns YYYY-MM-DD, 'today', or 'yesterday'."""
    # Explicit date
    m = re.search(r"(\d{4}-\d{2}-\d{2})", message)
    if m:
        return m.group(1)
    # DD/MM/YYYY or DD-MM-YYYY
    m = re.search(r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})", message)
    if m:
        day, month, year = m.group(1), m.group(2), m.group(3)
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

    text = message.lower()
    if re.search(r"\btoday\b", text):
        return "today"
    if re.search(r"\byesterday\b", text):
        return "yesterday"
    return None


def _extract_recent_filter(message: str) -> Optional[str]:
    """Extract recent/latest/current/ongoing filter."""
    text = message.lower()
    if re.search(r"\blatest\b", text):
        return "latest"
    if re.search(r"\bcurrent\b|\bongoing\b", text):
        return "current"
    if re.search(r"\brecent\b", text):
        return "recent"
    return None


def _extract_course_name(message: str) -> Optional[str]:
    """Extract course name from 'for/in/of <COURSE>' patterns."""
    m = re.search(r"(?:for|in|of)\s+([A-Z][A-Z0-9\-]+(?:\s+\d+)?)", message)
    if m:
        candidate = m.group(1)
        if candidate not in {"ALL", "AND", "NOT", "FOR", "THE"}:
            return candidate
    return None


# ═══════════════════════════════════════════════════════════════════
# Rule-based attendance flow detection
# ═══════════════════════════════════════════════════════════════════

def detect_attendance_guided_flow(message: str) -> Optional[Dict[str, Any]]:
    """Detect if message matches an attendance guided flow.

    Returns a detection dict or None if no match.
    """
    text = normalize_attendance_message(message.lower().strip())

    print(f"[Attendance Guided] Message: {message}")

    # ── DISAMBIGUATION: Do NOT capture exam / hostel / pure trainee profile ──
    if re.search(r"marks|result|exam|pass\b|fail|subject|score|grade|topper|re-exam|reexam", text):
        print("[Attendance Guided] Skipped — exam/marks context detected")
        return None
    if re.search(r"hostel|room\b|bed\b|staying|dues\b", text):
        print("[Attendance Guided] Skipped — hostel context detected")
        return None

    # Must have attendance context
    has_attendance_context = bool(re.search(
        r"attendance|present\b|absent\b|punch|biometric",
        text
    ))
    if not has_attendance_context:
        print("[Attendance Guided] Skipped — no attendance context found")
        return None

    # Build common slots
    slots: Dict[str, Any] = {
        "trainee_name": None,
        "user_id": None,
        "course_id": None,
        "course_name": None,
        "date": None,
        "from_date": None,
        "to_date": None,
        "date_range": None,
        "threshold": None,
        "recent_filter": None,
    }

    # Extract slots
    date = _extract_date(message)
    if date:
        slots["date"] = date

    threshold = _extract_threshold(message)
    if threshold:
        slots["threshold"] = threshold

    recent_filter = _extract_recent_filter(message)
    if recent_filter:
        slots["recent_filter"] = recent_filter

    course_name = _extract_course_name(message)
    if course_name:
        slots["course_name"] = course_name

    # ── Flow matching (order matters: specific before generic) ──

    # 1. person + attendance + percentage/percent/ratio
    if re.search(r"percentage|percent\b|ratio", text) and re.search(r"attendance", text):
        name = _extract_attendance_trainee_name(message)
        if name:
            slots["trainee_name"] = name
            return _build_result("attendance_percentage_by_trainee", slots,
                                 "matched trainee attendance percentage pattern")

    # 2. person + absent + days/count
    if re.search(r"absent", text) and re.search(r"day|count|how\s+many", text):
        name = _extract_attendance_trainee_name(message)
        if name:
            slots["trainee_name"] = name
            return _build_result("trainee_absent_count", slots,
                                 "matched trainee absent count pattern")

    # 3. person + present + days/count
    if re.search(r"present", text) and re.search(r"day|count|how\s+many", text):
        name = _extract_attendance_trainee_name(message)
        if name:
            slots["trainee_name"] = name
            return _build_result("trainee_present_count", slots,
                                 "matched trainee present count pattern")

    # 4. low attendance / below / less than
    if re.search(r"low\s+attendance|below\s+\d|less\s+than\s+\d|under\s+\d|irregular", text):
        return _build_result("low_attendance_trainees", slots,
                             "matched low attendance pattern")

    # 5. absent + trainees/students/today/date (no person needed)
    if re.search(r"absent", text) and re.search(r"trainee|student|today|yesterday|\d{4}-\d{2}-\d{2}|who|how\s+many|show|list", text):
        if not slots["date"]:
            slots["date"] = "today"  # default
        return _build_result("absent_trainees", slots,
                             "matched absent trainees pattern")

    # 6. present + trainees/students/today/date (no person needed)
    if re.search(r"present", text) and re.search(r"trainee|student|today|yesterday|\d{4}-\d{2}-\d{2}|who|how\s+many|show|list", text):
        if not slots["date"]:
            slots["date"] = "today"  # default
        return _build_result("present_trainees", slots,
                             "matched present trainees pattern")

    # 7. course wise / batch wise + attendance + summary/report
    if re.search(r"(course|batch)\s*wise", text) and re.search(r"attendance", text):
        return _build_result("course_attendance_summary", slots,
                             "matched course attendance summary pattern")

    # 8. attendance report + latest/current/batch/course
    if re.search(r"attendance\s+report|report\s+.*attendance", text):
        if re.search(r"latest|current|batch|course", text):
            return _build_result("batch_attendance_report", slots,
                                 "matched batch attendance report pattern")
        return _build_result("batch_attendance_report", slots,
                             "matched attendance report pattern")

    # 9. attendance + specific date/today/yesterday/date wise
    if re.search(r"date\s*wise", text) and re.search(r"attendance", text):
        return _build_result("date_wise_attendance", slots,
                             "matched date wise attendance pattern")

    if re.search(r"attendance", text) and date:
        return _build_result("date_wise_attendance", slots,
                             "matched attendance on specific date")

    if re.search(r"attendance\s+(today|yesterday)", text):
        if not slots["date"]:
            if "today" in text:
                slots["date"] = "today"
            elif "yesterday" in text:
                slots["date"] = "yesterday"
        return _build_result("date_wise_attendance", slots,
                             "matched attendance today/yesterday")

    # 10. person + attendance (generic — must be after specific patterns)
    if re.search(r"attendance", text):
        name = _extract_attendance_trainee_name(message)
        if name:
            slots["trainee_name"] = name
            return _build_result("attendance_by_trainee", slots,
                                 "matched trainee attendance pattern")

    # 11. course attendance summary (broader fallback)
    if re.search(r"attendance\s+summary", text):
        return _build_result("course_attendance_summary", slots,
                             "matched attendance summary pattern")

    print("[Attendance Guided] No flow matched")
    return None


def _build_result(flow_id: str, slots: dict, reason: str) -> dict:
    """Build standard detection result dict."""
    print(f"[Attendance Guided] Flow: {flow_id}")
    print(f"[Attendance Guided] Slots: {slots}")
    return {
        "flow_id": flow_id,
        "module": "attendance",
        "slots": slots,
        "reason": reason,
    }
