"""Trainee guided flow — rule-based detection, typo normalization, slot extraction.

Returns a flow detection dict or None if no trainee flow matched.
"""

import re
from datetime import datetime
from typing import Optional, Dict, Any


# ═══════════════════════════════════════════════════════════════════
# Trainee-specific typo normalization
# ═══════════════════════════════════════════════════════════════════

_TRAINEE_TYPO_MAP = {
    r"\bstudnts\b": "students",
    r"\bstdent\b": "student",
    r"\bstdents\b": "students",
    r"\btaines\b": "trainees",
    r"\btaine\b": "trainee",
    r"\btraine\b": "trainee",
    r"\btrainnes\b": "trainees",
    r"\btraning\b": "training",
    r"\btrainig\b": "training",
    r"\baproved\b": "approved",
    r"\baprove\b": "approve",
    r"\bpendng\b": "pending",
    r"\bjoind\b": "joined",
    r"\bjoinig\b": "joining",
    r"\bgender\b": "gender",
    r"\bgendr\b": "gender",
    r"\boutsty\b": "outstay",
    r"\bcorse\b": "course",
    r"\bcourses\b": "courses",
    r"\bbatch\b": "batch",
}


def normalize_trainee_message(message: str) -> str:
    """Apply trainee-specific typo corrections."""
    text = message
    for pattern, replacement in _TRAINEE_TYPO_MAP.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


# ═══════════════════════════════════════════════════════════════════
# Trainee flow definitions (used by guided_flow_service)
# ═══════════════════════════════════════════════════════════════════

TRAINEE_FLOWS = {
    "trainee_profile_by_name": {
        "module": "trainee",
        "requires_name": True,
        "slots_order": ["user_id"],
    },
    "active_trainee_count": {
        "module": "trainee",
        "requires_name": False,
        "slots_order": [],
    },
    "total_trainee_count": {
        "module": "trainee",
        "requires_name": False,
        "slots_order": [],
    },
    "all_trainees_list": {
        "module": "trainee",
        "requires_name": False,
        "slots_order": [],
    },
    "trainee_joined_by_year": {
        "module": "trainee",
        "requires_name": False,
        "slots_order": ["year"],
    },
    "trainees_by_course": {
        "module": "trainee",
        "requires_name": False,
        "slots_order": ["course_id"],
    },
    "recent_course_trainees": {
        "module": "trainee",
        "requires_name": False,
        "slots_order": [],
    },
    "course_wise_trainee_count": {
        "module": "trainee",
        "requires_name": False,
        "slots_order": [],
    },
    "batch_wise_trainee_count": {
        "module": "trainee",
        "requires_name": False,
        "slots_order": [],
    },
    "gender_wise_trainee_count": {
        "module": "trainee",
        "requires_name": False,
        "slots_order": [],
    },
    "approved_trainees": {
        "module": "trainee",
        "requires_name": False,
        "slots_order": [],
    },
    "pending_approval_trainees": {
        "module": "trainee",
        "requires_name": False,
        "slots_order": [],
    },
    "outstay_trainees": {
        "module": "trainee",
        "requires_name": False,
        "slots_order": [],
    },
}


# ═══════════════════════════════════════════════════════════════════
# Slot extraction helpers
# ═══════════════════════════════════════════════════════════════════

_TRAINEE_STOP_WORDS = {
    "show", "list", "get", "find", "what", "which", "who", "how",
    "many", "is", "are", "the", "of", "for", "in", "a", "an", "and",
    "to", "from", "with", "by", "on", "at", "all", "my", "me", "i",
    "trainee", "trainees", "student", "students", "course", "courses",
    "batch", "batches", "please", "tell", "give", "details", "detail",
    "about", "total", "count", "number", "check", "profile", "info",
    "information", "active", "joined", "joining", "approved", "pending",
    "approval", "outstay", "out", "stay", "gender", "male", "female",
    "wise", "recent", "latest", "current", "ongoing", "this", "year",
    "years", "do", "does", "has", "have", "been", "or", "not",
    "there", "were", "was", "will", "would", "can", "much",
    "we", "us", "our", "total", "last", "previous", "prev", "next", "month", "months", "days", "past"
}


def _extract_trainee_name(message: str) -> Optional[str]:
    """Extract a potential person name from the message (trainee context)."""
    text = re.sub(r'[?!.,;:\'\"()\[\]{}]', ' ', message.strip())
    words = text.split()
    name_parts = []
    for word in words:
        if word.lower() in _TRAINEE_STOP_WORDS:
            continue
        if word.isdigit():
            continue
        if len(word) <= 1:
            continue
        name_parts.append(word)
    if name_parts:
        return " ".join(name_parts)
    return None


def _extract_year(message: str) -> Optional[int]:
    """Extract a 4-digit year from the message."""
    m = re.search(r"\b(20\d{2})\b", message)
    if m:
        return int(m.group(1))
    # Handle relative year phrases
    text = message.lower()
    current_year = datetime.now().year
    if re.search(r"this\s+year|current\s+year", text):
        return current_year
    if re.search(r"last\s+year|previous\s+year|prev\s+year", text):
        return current_year - 1
    return None


def _extract_recent_filter(message: str) -> Optional[str]:
    """Extract recent/latest/current/ongoing filter."""
    text = message.lower()
    if re.search(r"\brecent\b", text):
        return "recent"
    if re.search(r"\blatest\b", text):
        return "latest"
    if re.search(r"\bcurrent\b|\bongoing\b", text):
        return "current"
    return None


def _extract_course_name(message: str) -> Optional[str]:
    """Extract a course name reference (e.g. HR-LDCE, Cabinman)."""
    # Look for course-like patterns (alphanumeric with hyphens)
    m = re.search(r"\b([A-Z][A-Z0-9\-]+(?:\s+\d+)?)\b", message)
    if m:
        candidate = m.group(1)
        # Exclude common non-course tokens
        if candidate not in {"ALL", "AND", "NOT", "FOR", "THE"}:
            return candidate
    return None


def _extract_date_range(message: str) -> Optional[str]:
    """Extract past/last month/months date range."""
    text = message.lower()
    m = re.search(r"((last|past)\s+(\d+\s+)?month[s]?|last\s+30\s+days)", text)
    if m:
        return m.group(1).strip()
    m = re.search(r"((last|past|this|current)\s+year)", text)
    if m:
        return m.group(1).strip()
    return None


# ═══════════════════════════════════════════════════════════════════
# Rule-based trainee flow detection
# ═══════════════════════════════════════════════════════════════════

def detect_trainee_guided_flow(message: str) -> Optional[Dict[str, Any]]:
    """Detect if message matches a trainee guided flow.

    Returns a detection dict or None if no match.
    """
    text = normalize_trainee_message(message.lower().strip())

    # ── DISAMBIGUATION: Do NOT capture exam / hostel / attendance questions ──
    if re.search(r"exam|marks|result|pass\b|fail|subject|score|grade|topper|re-exam|reexam", text):
        return None
    if re.search(r"hostel|room\b|bed\b|building", text):
        return None
    if re.search(r"attendance|present\b|absent\b|punch|biometric", text):
        return None
    if re.search(r"dues\b|mess\b|library\b|sports\b", text):
        return None

    # Build common slots dict
    slots: Dict[str, Any] = {}

    year = _extract_year(message)
    if year:
        slots["year"] = year

    recent_filter = _extract_recent_filter(message)
    if recent_filter:
        slots["recent_filter"] = recent_filter

    date_range = _extract_date_range(message)
    if date_range:
        slots["date_range"] = date_range

    course_name = _extract_course_name(message)
    if course_name:
        slots["course_name"] = course_name

    # ── outstay trainees ──
    if re.search(r"outstay|out\s+stay", text):
        return _build_result("outstay_trainees", slots, "matched outstay pattern")

    # ── pending approval (check BEFORE standalone "approved") ──
    if re.search(r"pending\s+approv|pending\s+for\s+approv|not\s+approv|unapproved", text):
        return _build_result("pending_approval_trainees", slots, "matched pending approval pattern")

    # ── approved trainees ──
    if re.search(r"approved", text):
        return _build_result("approved_trainees", slots, "matched approved pattern")

    # ── gender wise ──
    if re.search(r"gender|male\s+(and\s+)?female|female\s+(and\s+)?male|gender\s*wise", text):
        return _build_result("gender_wise_trainee_count", slots, "matched gender pattern")

    # ── batch wise ──
    if re.search(r"batch\s*wise|per\s+batch", text):
        return _build_result("batch_wise_trainee_count", slots, "matched batch wise pattern")

    # ── course wise ──
    if re.search(r"course\s*wise|per\s+course", text):
        return _build_result("course_wise_trainee_count", slots, "matched course wise pattern")

    # ── recent / latest / current / ongoing course trainees ──
    if re.search(r"(recent|latest|current|ongoing)\s+(course|batch|training)", text):
        if not slots.get("recent_filter"):
            slots["recent_filter"] = _extract_recent_filter(message) or "recent"
        return _build_result("recent_course_trainees", slots, "matched recent course pattern")

    if re.search(r"(trainee|student)s?\s+in\s+(recent|latest|current|ongoing)", text):
        if not slots.get("recent_filter"):
            slots["recent_filter"] = _extract_recent_filter(message) or "recent"
        return _build_result("recent_course_trainees", slots, "matched recent course pattern")

    # ── trainees by course ──
    if re.search(r"course\s+(trainee|student)s?|batch\s+(trainee|student)s?|(trainee|student)s?\s+(in|of|for)\s+(course|batch)", text):
        return _build_result("trainees_by_course", slots, "matched trainees by course pattern")

    # ── trainees joined by year ──
    if re.search(r"(joined|joining|admission|admitted|enrolled|intake)", text):
        if not _extract_trainee_name(message):
            return _build_result("trainee_joined_by_year", slots, "matched joined by year pattern")

    # ── list of ALL trainees (explicit list/show all request) ──
    if re.search(r"(list|show|display|get)\s+(of\s+)?(all|every)\s+(trainee|student)s?", text):
        return _build_result("all_trainees_list", slots, "matched list-all trainees pattern")
    if re.search(r"(trainee|student)s?\s+list", text) and re.search(r"\ball\b", text):
        return _build_result("all_trainees_list", slots, "matched all trainees list pattern")

    # ── active trainee count (must NOT match if 'total' is in query) ──
    if not re.search(r"\btotal\b", text):
        if re.search(r"active\s+(trainee|student|trainees|students)", text):
            return _build_result("active_trainee_count", slots, "matched active trainee pattern")
        if re.search(r"(trainee|student)s?\s+(active|currently\s+active)", text):
            return _build_result("active_trainee_count", slots, "matched active trainee pattern")
        
    # ── total trainee count ──
    if re.search(r"total\s+(trainee|student)s?|(trainee|student)s?\s+total", text) or (re.search(r"how\s+many\s+(total\s+)?(trainee|student)s?", text) and not re.search(r"per\s+(course|batch)", text)):
        return _build_result("total_trainee_count", slots, "matched total trainee pattern")

    # ── trainee profile by name (must be last — broadest match) ──
    name = _extract_trainee_name(message)
    if name:
        if re.search(r"(detail|profile|info|information|course|batch|enrolled|status|admission|joined)", text):
            slots["trainee_name"] = name
            return _build_result("trainee_profile_by_name", slots, "matched trainee name + context")
            
        # Fallback for just name + trainee/student
        if re.search(r"(trainee|student)", text):
            slots["trainee_name"] = name
            return _build_result("trainee_profile_by_name", slots, "matched trainee name + trainee")

    return None


def _build_result(flow_id: str, slots: dict, reason: str) -> dict:
    """Build standard detection result dict."""
    return {
        "flow_id": flow_id,
        "module": "trainee",
        "slots": slots,
        "reason": reason,
    }
