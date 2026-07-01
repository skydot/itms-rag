"""Timetable guided flow — rule-based detection, typo normalization, slot extraction.

Returns a flow detection dict or None if no timetable flow matched.
"""

import re
from typing import Optional, Dict, Any
from datetime import datetime


# ═══════════════════════════════════════════════════════════════════
# Timetable-specific typo normalization
# ═══════════════════════════════════════════════════════════════════

_TIMETABLE_TYPO_MAP = {
    r"\btimtable\b": "timetable",
    r"\btime table\b": "timetable",
    r"\btymetable\b": "timetable",
    r"\bschedul\b": "schedule",
    r"\bshedule\b": "schedule",
    r"\blectur\b": "lecture",
    r"\bleacture\b": "lecture",
    r"\bfacalty\b": "faculty",
    r"\bfaculity\b": "faculty",
    r"\bteachr\b": "teacher",
    r"\binstrctor\b": "instructor",
    r"\bclass room\b": "classroom",
    r"\bclasroom\b": "classroom",
    r"\bsesson\b": "session",
    r"\bcurent\b": "current",
    r"\blattest\b": "latest",
    r"\bletest\b": "latest",
}


def normalize_timetable_message(message: str) -> str:
    """Apply timetable-specific typo corrections."""
    text = message.lower()
    for pattern, replacement in _TIMETABLE_TYPO_MAP.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


# ═══════════════════════════════════════════════════════════════════
# Timetable flow definitions (used by guided_flow_service)
# ═══════════════════════════════════════════════════════════════════

TIMETABLE_FLOWS = {
    "today_timetable": {
        "module": "timetable",
        "requires_name": False,
        "slots_order": [],
    },
    "tomorrow_timetable": {
        "module": "timetable",
        "requires_name": False,
        "slots_order": [],
    },
    "date_wise_timetable": {
        "module": "timetable",
        "requires_name": False,
        "slots_order": ["date"],
    },
    "course_timetable": {
        "module": "timetable",
        "requires_name": False,
        "slots_order": ["course_id"],
    },
    "faculty_timetable": {
        "module": "timetable",
        "requires_name": False,
        "slots_order": ["user_id"],
    },
    "subject_timetable": {
        "module": "timetable",
        "requires_name": False,
        "slots_order": ["subject_id"],
    },
    "classroom_timetable": {
        "module": "timetable",
        "requires_name": False,
        "slots_order": ["classroom_id"],
    },
    "session_timetable": {
        "module": "timetable",
        "requires_name": False,
        "slots_order": ["session_id"],
    },
    "timetable_summary": {
        "module": "timetable",
        "requires_name": False,
        "slots_order": [],
    },
    "free_slots": {
        "module": "timetable",
        "requires_name": False,
        "slots_order": [],
    },
}


# ═══════════════════════════════════════════════════════════════════
# Slot extraction helpers
# ═══════════════════════════════════════════════════════════════════

def _extract_date(message: str) -> Optional[str]:
    if re.search(r"\btoday\b", message): return "today"
    if re.search(r"\btomorrow\b", message): return "tomorrow"
    if re.search(r"\byesterday\b", message): return "yesterday"
    # YYYY-MM-DD
    m = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", message)
    if m: return m.group(1)
    return None

def _extract_recent_filter(message: str) -> Optional[str]:
    if re.search(r"\b(latest|recent|last\s+started)\b", message): return "latest"
    if re.search(r"\b(current|ongoing|running)\b", message): return "current"
    return None

def _extract_group_by(message: str) -> Optional[str]:
    if re.search(r"\bcourse\s+wise\b", message): return "course"
    if re.search(r"\bfaculty\s+wise\b", message): return "faculty"
    if re.search(r"\bsubject\s+wise\b", message): return "subject"
    if re.search(r"\bclassroom\s+wise\b", message): return "classroom"
    if re.search(r"\bsession\s+wise\b", message): return "session"
    return None

def _extract_classroom_name(message: str) -> Optional[str]:
    m = re.search(r"(?:classroom|room|class\s+room)\s+([A-Za-z0-9]+)", message)
    if m: return m.group(1)
    return None

def _extract_entity_name(message: str) -> Optional[str]:
    """Generic name extraction for faculty, course, subject"""
    stop_words = {"timetable", "schedule", "lecture", "show", "list", "today", "tomorrow", "current", "latest", "course", "batch", "subject", "faculty", "classroom", "session", "when", "is", "scheduled", "for", "of", "the", "in", "what", "which", "how", "many"}
    text = re.sub(r'[?!.,;:\'\"()\[\]{}]', ' ', message)
    words = text.split()
    name_parts = []
    for word in words:
        if word in stop_words: continue
        if len(word) <= 2 and not word.isdigit(): continue
        name_parts.append(word)
    if name_parts:
        return " ".join(name_parts)
    return None


# ═══════════════════════════════════════════════════════════════════
# Rule-based timetable flow detection
# ═══════════════════════════════════════════════════════════════════

def detect_timetable_guided_flow(message: str) -> Optional[Dict[str, Any]]:
    """Detect if message matches a timetable guided flow."""
    text = normalize_timetable_message(message.strip())

    print(f"[Timetable Guided] Message: {message}")

    # ── DISAMBIGUATION ──
    # "exam schedule" / "exam date" refers to exam scheduling (et_design), NOT lecture timetables
    if re.search(r"exams?\s+schedule|exams?\s+date|exams?\s+schedul", text) and not re.search(r"timetable|\blecture\b|\blectures\b", text):
        print("[Timetable Guided] Skipped — exam schedule context detected (not timetable)")
        return None
    # If message contains marks/result/exam/pass/fail/result/percentage and NOT timetable/schedule/lecture
    if re.search(r"marks|result\b|exams?\b|pass\b|fail|percentage", text) and not re.search(r"timetable|schedule|\blecture\b|\blectures\b", text):
        print("[Timetable Guided] Skipped — exam context detected")
        return None
    # If message contains attendance/present/absent and NOT timetable/schedule
    if re.search(r"attendance|present\b|absent\b|punch|biometric", text) and not re.search(r"timetable|schedule|\blecture\b|\blectures\b", text):
        print("[Timetable Guided] Skipped — attendance context detected")
        return None
    # If message contains hostel/room/bed/staying/dues and NOT classroom
    if re.search(r"hostel\b|room\b|bed\b|staying|dues\b", text) and not re.search(r"classroom|class\s+room", text):
        print("[Timetable Guided] Skipped — hostel context detected without classroom")
        return None
    # If message contains complaint/issue/problem
    if re.search(r"complaint|issue|problem", text):
        print("[Timetable Guided] Skipped — complaint context detected")
        return None

    # Base intent required
    has_timetable_intent = bool(re.search(r"timetable|schedule|\blecture\b|\blectures\b|free\s+slot|available\s+slot", text))
    if not has_timetable_intent:
        print("[Timetable Guided] Skipped — no timetable intent found")
        return None

    slots: Dict[str, Any] = {
        "course_name": None, "course_id": None,
        "faculty_name": None, "user_id": None,
        "subject_name": None, "subject_id": None,
        "classroom_name": _extract_classroom_name(text), "classroom_id": None,
        "session_name": None, "session_id": None,
        "date": _extract_date(text),
        "from_date": None, "to_date": None, "date_range": None,
        "recent_filter": _extract_recent_filter(text),
        "group_by": _extract_group_by(text)
    }

    extracted = _extract_entity_name(text)

    # 1. free_slots
    if re.search(r"free\s+slot|available\s+slot|free\s+classroom|free\s+faculty|is\s+free", text):
        return _build_result("free_slots", slots, "matched free slots")

    # 2. timetable_summary
    if re.search(r"summary|count|how\s+many\s+lecture|how\s+many\s+session|total\s+lecture", text) or slots["group_by"]:
        if not slots["date"]:
            slots["date"] = "today"
        return _build_result("timetable_summary", slots, "matched timetable summary")

    # 3. today_timetable
    if re.search(r"\btoday\b", text) and re.search(r"timetable|schedule|\blecture\b|\blectures\b", text):
        # Could be course timetable today, etc. Check if faculty/subject/classroom etc are present.
        if re.search(r"faculty|instructor|teacher", text):
            slots["faculty_name"] = extracted
            return _build_result("faculty_timetable", slots, "matched faculty timetable today")
        if re.search(r"subject", text):
            slots["subject_name"] = extracted
            return _build_result("subject_timetable", slots, "matched subject timetable today")
        if slots["classroom_name"]:
            return _build_result("classroom_timetable", slots, "matched classroom timetable today")
        if re.search(r"session|morning|afternoon", text):
            slots["session_name"] = extracted
            return _build_result("session_timetable", slots, "matched session timetable today")
            
        slots["date"] = "today"
        if extracted:
            slots["course_name"] = extracted
        return _build_result("today_timetable", slots, "matched today timetable")

    # 4. tomorrow_timetable
    if re.search(r"\btomorrow\b", text) and re.search(r"timetable|schedule|\blecture\b|\blectures\b", text):
        if re.search(r"faculty|instructor|teacher", text):
            slots["faculty_name"] = extracted
            return _build_result("faculty_timetable", slots, "matched faculty timetable tomorrow")
        slots["date"] = "tomorrow"
        if extracted:
            slots["course_name"] = extracted
        return _build_result("tomorrow_timetable", slots, "matched tomorrow timetable")

    # 5. classroom_timetable
    if slots["classroom_name"] or re.search(r"classroom|class\s+room", text):
        if not slots["classroom_name"] and extracted:
            slots["classroom_name"] = extracted
        return _build_result("classroom_timetable", slots, "matched classroom timetable")

    # 6. faculty_timetable
    if re.search(r"faculty|instructor|teacher", text):
        slots["faculty_name"] = extracted
        return _build_result("faculty_timetable", slots, "matched faculty timetable")

    # 7. subject_timetable
    if re.search(r"subject|when\s+is\s+.*scheduled", text):
        slots["subject_name"] = extracted
        return _build_result("subject_timetable", slots, "matched subject timetable")

    # 8. session_timetable
    if re.search(r"session|morning|afternoon", text):
        slots["session_name"] = extracted
        return _build_result("session_timetable", slots, "matched session timetable")

    # 9. date_wise_timetable
    if re.search(r"date|yesterday", text) or (slots["date"] and slots["date"] not in ("today", "tomorrow")):
        if extracted:
            slots["course_name"] = extracted
        return _build_result("date_wise_timetable", slots, "matched date wise timetable")

    # 10. course_timetable
    if re.search(r"course|batch|timetable\s+of|schedule\s+of", text) or slots["recent_filter"]:
        slots["course_name"] = extracted
        return _build_result("course_timetable", slots, "matched course timetable")
        
    # If just "timetable" -> default to course timetable
    if re.search(r"timetable|schedule|\blecture\b|\blectures\b", text):
        slots["course_name"] = extracted
        return _build_result("course_timetable", slots, "fallback to course timetable")

    print("[Timetable Guided] No flow matched")
    return None


def _build_result(flow_id: str, slots: dict, reason: str) -> dict:
    """Build standard detection result dict."""
    print(f"[Timetable Guided] Flow: {flow_id}")
    print(f"[Timetable Guided] Slots: {slots}")
    return {
        "flow_id": flow_id,
        "module": "timetable",
        "slots": slots,
        "reason": reason,
    }
