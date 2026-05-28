"""Faculty / VL guided flow — rule-based detection, typo normalization, slot extraction.

Returns a flow detection dict or None if no faculty flow matched.
"""

import re
from typing import Optional, Dict, Any


# ═══════════════════════════════════════════════════════════════════
# Faculty-specific typo normalization
# ═══════════════════════════════════════════════════════════════════

_FACULTY_TYPO_MAP = {
    r"\bfacalty\b": "faculty",
    r"\bfaculity\b": "faculty",
    r"\bfacuty\b": "faculty",
    r"\bteachr\b": "teacher",
    r"\btecher\b": "teacher",
    r"\binstrctor\b": "instructor",
    r"\binstructer\b": "instructor",
    r"\blecturerer\b": "lecturer",
    r"\blecturar\b": "lecturer",
    r"\bvissiting\b": "visiting",
    r"\bvising\b": "visiting",
    r"\bschedul\b": "schedule",
    r"\bshedule\b": "schedule",
    r"\btimtable\b": "timetable",
    r"\btymetable\b": "timetable",
    r"\bsubjectt\b": "subject",
    r"\bcours\b": "course",
    r"\bfeedbak\b": "feedback",
}


def normalize_faculty_message(message: str) -> str:
    """Apply faculty-specific typo corrections."""
    text = message.lower()
    for pattern, replacement in _FACULTY_TYPO_MAP.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


# ═══════════════════════════════════════════════════════════════════
# Faculty flow definitions
# ═══════════════════════════════════════════════════════════════════

FACULTY_FLOWS = {
    "faculty_profile_by_name": {
        "module": "faculty",
        "requires_name": False,
        "slots_order": ["faculty_id"],
    },
    "faculty_schedule": {
        "module": "faculty",
        "requires_name": False,
        "slots_order": ["faculty_id"],
    },
    "faculty_courses": {
        "module": "faculty",
        "requires_name": False,
        "slots_order": ["faculty_id"],
    },
    "faculty_subjects": {
        "module": "faculty",
        "requires_name": False,
        "slots_order": ["faculty_id"],
    },
    "faculty_workload_summary": {
        "module": "faculty",
        "requires_name": False,
        "slots_order": [],
    },
    "visiting_lecturers": {
        "module": "faculty",
        "requires_name": False,
        "slots_order": [],
    },
    "faculty_feedback_summary": {
        "module": "faculty",
        "requires_name": False,
        "slots_order": [],
    },
    "faculty_by_subject": {
        "module": "faculty",
        "requires_name": False,
        "slots_order": ["subject_id"],
    },
    "faculty_by_course": {
        "module": "faculty",
        "requires_name": False,
        "slots_order": ["course_id"],
    },
    "faculty_availability": {
        "module": "faculty",
        "requires_name": False,
        "slots_order": [],
    },
}


# ═══════════════════════════════════════════════════════════════════
# Slot extraction helpers
# ═══════════════════════════════════════════════════════════════════

def _extract_date(text: str) -> Optional[str]:
    if re.search(r"\btoday\b", text): return "today"
    if re.search(r"\btomorrow\b", text): return "tomorrow"
    if re.search(r"\byesterday\b", text): return "yesterday"
    m = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", text)
    if m: return m.group(1)
    return None


def _extract_faculty_type(text: str) -> Optional[str]:
    if re.search(r"\bvisiting\s+lectur|\bvisiting\s+facul|\bvl\b", text):
        return "vl"
    if re.search(r"\binternal\s+facul", text):
        return "internal"
    return None


def _extract_recent_filter(text: str) -> Optional[str]:
    if re.search(r"\b(latest|recent|last\s+started)\b", text): return "latest"
    if re.search(r"\b(current|ongoing|running)\b", text): return "current"
    return None


def _extract_year(text: str) -> Optional[int]:
    m = re.search(r"\b(20\d{2})\b", text)
    if m: return int(m.group(1))
    return None


_FACULTY_KEYWORDS = re.compile(
    r"\bfaculty\b|\bteacher\b|\binstructor\b|\blecturer\b|\bvl\b|\bvisiting\b"
)

_STOP_WORDS = {
    "faculty", "teacher", "instructor", "vl", "visiting", "lecturer", "lecturers",
    "schedule", "timetable", "lecture", "show", "list", "details", "profile",
    "feedback", "course", "courses", "subject", "subjects", "assigned",
    "teaches", "teach", "topics", "rating", "ratings", "summary", "workload",
    "count", "batch", "batches", "handled", "for", "of", "the", "a",
    "is", "in", "to", "by", "what", "which", "who", "how", "many",
    "does", "have", "has", "today", "tomorrow", "yesterday", "current",
    "latest", "ongoing", "internal", "report", "free", "available",
    "availability", "wise", "most",
}


def _extract_faculty_name(text: str) -> Optional[str]:
    """Extract a faculty name from the message."""
    # Pattern: faculty/instructor/teacher <Name>
    m = re.search(
        r"(?:faculty|instructor|teacher|lecturer|vl)\s+([A-Za-z][A-Za-z\s]{1,30}?)(?:\s+(?:details|profile|schedule|timetable|lecture|courses|subjects|feedback|rating|workload|assigned|free|available)|$)",
        text
    )
    if m:
        raw = m.group(1).strip()
        parts = [w for w in raw.split() if w.lower() not in _STOP_WORDS]
        if parts:
            return " ".join(parts)

    # Pattern: <Name> + faculty context word
    m = re.search(
        r"(?:show|list|details|profile|schedule|feedback|rating|courses|subjects|timetable|lectures|assigned)\s+(?:of\s+)?(?:faculty|instructor|teacher|vl)?\s*([A-Za-z][A-Za-z\s]{1,25})",
        text
    )
    if m:
        raw = m.group(1).strip()
        parts = [w for w in raw.split() if w.lower() not in _STOP_WORDS]
        if parts:
            return " ".join(parts)

    # Pattern: <Name> schedule/timetable/feedback etc
    m = re.search(
        r"([A-Za-z][A-Za-z]{2,})\s+(?:schedule|timetable|lecture|courses|subjects|feedback|rating|workload|assigned|free)",
        text
    )
    if m:
        raw = m.group(1).strip()
        if raw.lower() not in _STOP_WORDS:
            return raw

    return None


def _extract_subject_name(text: str) -> Optional[str]:
    m = re.search(r"(?:who\s+teaches|faculty\s+for|teacher\s+for|vl\s+for)\s+([A-Za-z/&\s]+?)(?:\s+subject|\s*$)", text)
    if m:
        raw = m.group(1).strip()
        parts = [w for w in raw.split() if w.lower() not in _STOP_WORDS]
        if parts: return " ".join(parts)
    m = re.search(r"(?:teaches|for)\s+([A-Za-z/&]+)\s+subject", text)
    if m: return m.group(1).strip()
    return None


def _extract_course_name(text: str) -> Optional[str]:
    m = re.search(r"(?:assigned\s+to|teachers\s+for|faculty\s+of|faculty\s+for)\s+([A-Za-z/&\s\-]+?)(?:\s+course|\s+batch|\s*$)", text)
    if m:
        raw = m.group(1).strip()
        parts = [w for w in raw.split() if w.lower() not in _STOP_WORDS]
        if parts: return " ".join(parts)
    return None


# ═══════════════════════════════════════════════════════════════════
# Rule-based faculty flow detection
# ═══════════════════════════════════════════════════════════════════

def detect_faculty_guided_flow(message: str, allow_weak_intent: bool = False) -> Optional[Dict[str, Any]]:
    """Detect if message matches a faculty guided flow."""
    text = normalize_faculty_message(message.strip())

    print(f"[Faculty Guided] Message: {message}")

    # ── DISAMBIGUATION ──
    if re.search(r"marks|result\b|exam\b|pass\b|fail|percentage", text) and not _FACULTY_KEYWORDS.search(text):
        print("[Faculty Guided] Skipped — exam context detected")
        return None
    if re.search(r"attendance|present\b|absent\b|punch|biometric", text) and not _FACULTY_KEYWORDS.search(text):
        print("[Faculty Guided] Skipped — attendance context detected")
        return None
    if re.search(r"hostel\b|room\b|bed\b|staying|dues\b", text):
        print("[Faculty Guided] Skipped — hostel context detected")
        return None
    if re.search(r"complaint|issue|problem", text) and not re.search(r"feedback", text):
        print("[Faculty Guided] Skipped — complaint context detected")
        return None

    # Must have faculty/teacher/instructor/VL intent
    has_faculty_intent = bool(_FACULTY_KEYWORDS.search(text))
    # Also catch: "who teaches", "who has most lectures"
    has_who_teaches = bool(re.search(r"who\s+teach", text))
    has_workload_pattern = bool(re.search(r"who\s+has\s+most\s+lecture|faculty\s+wise|teacher\s+wise|vl\s+workload", text))

    if not has_faculty_intent and not has_who_teaches and not has_workload_pattern and not allow_weak_intent:
        print("[Faculty Guided] Skipped — no faculty intent found")
        return None

    # Build slots
    slots: Dict[str, Any] = {
        "faculty_name": _extract_faculty_name(text),
        "faculty_id": None,
        "faculty_type": _extract_faculty_type(text),
        "course_name": _extract_course_name(text),
        "course_id": None,
        "subject_name": _extract_subject_name(text),
        "subject_id": None,
        "date": _extract_date(text),
        "from_date": None, "to_date": None, "date_range": None,
        "recent_filter": _extract_recent_filter(text),
        "year": _extract_year(text),
        "status": None,
        "group_by": None,
    }

    # ── visiting_lecturers ──
    if re.search(r"visiting\s+lectur|visiting\s+facul|vl\s+list|vl\s+details|list\s+vl|show\s+vl\b|how\s+many\s+vl|how\s+many\s+visiting", text):
        if not slots["faculty_name"]:
            return _build_result("visiting_lecturers", slots, "matched visiting lecturer pattern")

    # ── faculty_availability ──
    if re.search(r"free|available|availability", text) and (has_faculty_intent or allow_weak_intent):
        return _build_result("faculty_availability", slots, "matched faculty availability")

    # ── faculty_workload_summary ──
    if re.search(r"workload|faculty\s+wise\s+lecture|teacher\s+wise|vl\s+workload|who\s+has\s+most\s+lecture|lecture\s+count\s+faculty|session\s+count\s+faculty", text):
        return _build_result("faculty_workload_summary", slots, "matched faculty workload")

    # ── faculty_feedback_summary ──
    if re.search(r"feedback|rating", text) and (has_faculty_intent or allow_weak_intent):
        return _build_result("faculty_feedback_summary", slots, "matched faculty feedback")

    # ── faculty_by_subject ──
    if re.search(r"who\s+teach|faculty\s+for\s+\w+\s+subject|teacher\s+for\s+\w+|vl\s+for\s+\w+", text):
        if not slots["subject_name"]:
            # Try to extract from remaining text
            m = re.search(r"(?:teaches|teach)\s+([A-Za-z/&]+)", text)
            if m: slots["subject_name"] = m.group(1)
        return _build_result("faculty_by_subject", slots, "matched faculty by subject")

    # ── faculty_by_course ──
    if re.search(r"(?:faculty|teacher|instructor)\s+(?:assigned|of|for)\s+|teachers\s+for\s+|faculty\s+of\s+", text) or (allow_weak_intent and re.search(r"assigned\s+to", text) and slots["course_name"]):
        return _build_result("faculty_by_course", slots, "matched faculty by course")

    # ── faculty_profile_by_name ──
    if re.search(r"profile|details", text) and (has_faculty_intent or allow_weak_intent):
        return _build_result("faculty_profile_by_name", slots, "matched faculty profile")

    # ── faculty_schedule ──
    if re.search(r"schedule|timetable|lecture", text) and (has_faculty_intent or allow_weak_intent):
        return _build_result("faculty_schedule", slots, "matched faculty schedule")

    # ── faculty_courses ──
    if re.search(r"courses|batches|assigned", text) and (has_faculty_intent or allow_weak_intent):
        return _build_result("faculty_courses", slots, "matched faculty courses")

    # ── faculty_subjects ──
    if re.search(r"subjects|topics", text) and (has_faculty_intent or allow_weak_intent):
        return _build_result("faculty_subjects", slots, "matched faculty subjects")

    # Fallback: if faculty keyword is present and a name is extracted
    if slots["faculty_name"] and (has_faculty_intent or allow_weak_intent):
        return _build_result("faculty_profile_by_name", slots, "fallback to faculty profile")

    print("[Faculty Guided] No flow matched")
    return None


def _build_result(flow_id: str, slots: dict, reason: str) -> dict:
    print(f"[Faculty Guided] Flow: {flow_id}")
    print(f"[Faculty Guided] Slots: {slots}")
    return {
        "flow_id": flow_id,
        "module": "faculty",
        "slots": slots,
        "reason": reason,
    }
