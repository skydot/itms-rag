"""Complaint guided flow — rule-based detection, typo normalization, slot extraction.

Returns a flow detection dict or None if no complaint flow matched.
"""

import re
from typing import Optional, Dict, Any
from datetime import datetime


# ═══════════════════════════════════════════════════════════════════
# Complaint-specific typo normalization
# ═══════════════════════════════════════════════════════════════════

_COMPLAINT_TYPO_MAP = {
    r"\bcomplent\b": "complaint",
    r"\bcompaint\b": "complaint",
    r"\bcomplain\b": "complaint",
    r"\bcomplains\b": "complaints",
    r"\bpendingg\b": "pending",
    r"\bpendng\b": "pending",
    r"\bresolve\b": "resolved",
    r"\bresloved\b": "resolved",
    r"\bclosed\b": "resolved",
    r"\bclose\b": "resolved",
    r"\bopen\b": "pending",
    r"\bmaintanance\b": "maintenance",
    r"\bmaintainance\b": "maintenance",
    r"\belectic\b": "electrical",
    r"\beletrical\b": "electrical",
    r"\bhostal\b": "hostel",
    r"\bhostle\b": "hostel",
}


def normalize_complaint_message(message: str) -> str:
    """Apply complaint-specific typo corrections."""
    text = message
    for pattern, replacement in _COMPLAINT_TYPO_MAP.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


# ═══════════════════════════════════════════════════════════════════
# Complaint flow definitions (used by guided_flow_service)
# ═══════════════════════════════════════════════════════════════════

COMPLAINT_FLOWS = {
    "pending_complaints": {
        "module": "complaint",
        "requires_name": False,
        "slots_order": [],
    },
    "resolved_complaints": {
        "module": "complaint",
        "requires_name": False,
        "slots_order": [],
    },
    "complaint_status_summary": {
        "module": "complaint",
        "requires_name": False,
        "slots_order": [],
    },
    "complaints_by_category": {
        "module": "complaint",
        "requires_name": False,
        "slots_order": ["complaint_category"],
    },
    "complaints_by_trainee": {
        "module": "complaint",
        "requires_name": True,
        "slots_order": ["user_id"],
    },
    "complaint_details_by_id": {
        "module": "complaint",
        "requires_name": False,
        "slots_order": ["complaint_id"],
    },
    "department_wise_complaints": {
        "module": "complaint",
        "requires_name": False,
        "slots_order": [],
    },
    "recent_complaints": {
        "module": "complaint",
        "requires_name": False,
        "slots_order": [],
    },
    "overdue_complaints": {
        "module": "complaint",
        "requires_name": False,
        "slots_order": [],
    },
    "complaint_count": {
        "module": "complaint",
        "requires_name": False,
        "slots_order": [],
    },
}


# ═══════════════════════════════════════════════════════════════════
# Slot extraction helpers
# ═══════════════════════════════════════════════════════════════════

def _extract_complaint_id(message: str) -> Optional[int]:
    """Extract complaint id from numbers after complaint/id."""
    m = re.search(r"complaint(?:s)?\s+(?:id\s+)?(\d+)", message, re.IGNORECASE)
    if m:
        return int(m.group(1))
    m = re.search(r"(?:id|details\s+of)\s+(\d+)", message, re.IGNORECASE)
    if m:
        return int(m.group(1))
    return None


def _extract_complaint_status(message: str) -> Optional[str]:
    """Extract complaint status filter."""
    text = message.lower()
    if re.search(r"\b(pending|open|unresolved)\b", text):
        return "pending"
    if re.search(r"\b(resolved|closed|done)\b", text):
        return "resolved"
    if re.search(r"\ball\b", text):
        return "all"
    return None


def _extract_complaint_category(message: str) -> Optional[str]:
    """Extract category words. Now disabled so we always prompt for options."""
    return None


def _extract_limit(message: str) -> Optional[int]:
    """Extract limit like last 10, latest 5."""
    m = re.search(r"(?:last|latest|top|recent)\s+(\d+)", message.lower())
    if m:
        return int(m.group(1))
    return None


def _extract_days(message: str) -> Optional[int]:
    """Extract days like older than 7 days."""
    m = re.search(r"(?:older\s+than|not\s+resolved\s+for|overdue\s+by)\s+(\d+)\s+days?", message.lower())
    if m:
        return int(m.group(1))
    return None


def _extract_year(message: str) -> Optional[int]:
    """Extract 4-digit year."""
    m = re.search(r"\b(20[1-3]\d)\b", message)
    if m:
        return int(m.group(1))
    text = message.lower()
    if re.search(r"\bthis\s+year\b", text):
        return datetime.now().year
    if re.search(r"\blast\s+year\b|\bprevious\s+year\b", text):
        return datetime.now().year - 1
    return None


MONTH_NAME_MAP = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
    "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
}


def _extract_month(message: str) -> Optional[int]:
    """Extract month number from a month name in the message."""
    text = message.lower()
    for name, num in MONTH_NAME_MAP.items():
        if re.search(r"\b" + name + r"\b", text):
            return num
    return None



def _extract_trainee_name(message: str) -> Optional[str]:
    """Extract trainee name for complaint queries."""
    # Remove common words related to complaints
    stop_words = {"complaint", "complaints", "complain", "complains", "compaint", "complent", "pending", "resolved", "raised", "by", "of", "history", "show", "list", "get", "what", "how", "many", "is", "are", "the", "for", "in", "a", "an", "and", "to", "from", "with", "my", "me", "i", "please", "tell", "give", "details", "detail", "about", "total", "count", "number", "check", "hostel", "mess", "room", "bed", "water", "electrical", "maintenance", "food", "cleaning", "toilet", "bathroom", "fan", "light", "civil", "academic", "block", "others"}
    text = re.sub(r'[?!.,;:\'\"()\[\]{}]', ' ', message.strip())
    words = text.split()
    name_parts = []
    for word in words:
        if word.lower() in stop_words:
            continue
        if word.isdigit():
            continue
        if len(word) <= 1:
            continue
        name_parts.append(word)
    if name_parts:
        return " ".join(name_parts)
    return None


# ═══════════════════════════════════════════════════════════════════
# Rule-based complaint flow detection
# ═══════════════════════════════════════════════════════════════════

def detect_complaint_guided_flow(message: str) -> Optional[Dict[str, Any]]:
    """Detect if message matches a complaint guided flow."""
    text = normalize_complaint_message(message.lower().strip())

    print(f"[Complaint Guided] Message: {message}")

    # ── DISAMBIGUATION ──
    if re.search(r"marks|result\b|exam\b|pass\b|fail|subject\b|score\b|grade\b|topper|re-exam|reexam", text):
        print("[Complaint Guided] Skipped — exam context detected")
        return None
    if re.search(r"attendance|present\b|absent\b|punch|biometric", text):
        print("[Complaint Guided] Skipped — attendance context detected")
        return None
    if re.search(r"books?\b|library\b|issued\s+to\b|borrowed\b", text) and not re.search(r"complaint", text):
        print("[Complaint Guided] Skipped — library context detected")
        return None
    
    has_complaint_word = bool(re.search(r"complaint|issue|problem", text))
    
    if re.search(r"hostel\b|room\b|bed\b|staying|dues\b", text) and not has_complaint_word:
        print("[Complaint Guided] Skipped — hostel context without complaint word")
        return None
        
    # If it's a pure trainee question without complaint word
    if not has_complaint_word:
        # We only process if complaint word is present, except maybe edge cases, 
        # but prompt says: "If message contains only trainee details/profile and no complaint word -> return None"
        print("[Complaint Guided] Skipped — no complaint word found")
        return None

    # Build common slots
    slots: Dict[str, Any] = {
        "trainee_name": None,
        "user_id": None,
        "complaint_id": _extract_complaint_id(text),
        "complaint_category": _extract_complaint_category(text),
        "complaint_status": _extract_complaint_status(text),
        "department_name": None,
        "building_name": None,
        "year": _extract_year(text),
        "month": _extract_month(text),
        "limit": _extract_limit(text),
        "days": _extract_days(text),
    }

    trainee_name = _extract_trainee_name(message)
    if trainee_name:
        slots["trainee_name"] = trainee_name

    # 1. complaint_details_by_id
    if slots["complaint_id"] or re.search(r"complaint(?:s)?\s+(?:id\s+)?\d+|details\s+of\s+complaint", text):
        return _build_result("complaint_details_by_id", slots, "matched complaint id pattern")

    # 2. complaint_status_summary
    if re.search(r"complaint\s+status\s+summary|open\s+vs\s+closed|complaint\s+dashboard|complaint\s+summary", text):
        return _build_result("complaint_status_summary", slots, "matched complaint status summary")

    # 3. department_wise_complaints
    if re.search(r"department\s+wise|by\s+department|department", text):
        return _build_result("department_wise_complaints", slots, "matched department wise complaints")

    # 4. recent_complaints
    if re.search(r"recent|latest|new\s+complaint|last\s+\d+\s+complaint", text):
        if not slots["limit"]:
            slots["limit"] = 10
        return _build_result("recent_complaints", slots, "matched recent complaints")

    # 5. overdue_complaints
    if re.search(r"overdue|older\s+than|not\s+resolved\s+for", text):
        if not slots["days"]:
            slots["days"] = 7
        return _build_result("overdue_complaints", slots, "matched overdue complaints")

    # 6. pending_complaints
    if re.search(r"pending|open|unresolved", text) and re.search(r"complaint|issue", text):
        if not slots["complaint_status"]:
            slots["complaint_status"] = "pending"
        return _build_result("pending_complaints", slots, "matched pending complaints")

    # 7. resolved_complaints
    if re.search(r"resolved|closed|done", text) and re.search(r"complaint|issue", text):
        if not slots["complaint_status"]:
            slots["complaint_status"] = "resolved"
        return _build_result("resolved_complaints", slots, "matched resolved complaints")

    # 8. complaint_count
    if re.search(r"how\s+many|total|count", text):
        return _build_result("complaint_count", slots, "matched complaint count")

    # 9. complaints_by_category
    if slots["complaint_category"]:
        return _build_result("complaints_by_category", slots, "matched complaint category")

    # 10. complaints_by_trainee
    if slots["trainee_name"] and len(slots["trainee_name"]) > 2:
        return _build_result("complaints_by_trainee", slots, "matched complaint by trainee")

    # Fallback to category selection so user gets options for any broad query
    if re.search(r"(?:show|list|get|fetch|find|view).*?complaints?", text):
        slots["complaint_status"] = slots["complaint_status"] or "all"
        return _build_result("complaints_by_category", slots, "fallback to category selection")

    print("[Complaint Guided] No flow matched")
    return None


def _build_result(flow_id: str, slots: dict, reason: str) -> dict:
    """Build standard detection result dict."""
    print(f"[Complaint Guided] Flow: {flow_id}")
    print(f"[Complaint Guided] Slots: {slots}")
    return {
        "flow_id": flow_id,
        "module": "complaint",
        "slots": slots,
        "reason": reason,
    }
