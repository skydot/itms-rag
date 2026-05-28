"""Hostel guided flow — rule-based detection, typo normalization, slot extraction.

Returns a flow detection dict or None if no hostel flow matched.
"""

import re
from typing import Optional, Dict, Any


# ═══════════════════════════════════════════════════════════════════
# Hostel-specific typo normalization
# ═══════════════════════════════════════════════════════════════════

_HOSTEL_TYPO_MAP = {
    r"\bhostal\b": "hostel",
    r"\bhostle\b": "hostel",
    r"\brom\b": "room",
    r"\brum\b": "room",
    r"\bavailble\b": "available",
    r"\bavilable\b": "available",
    r"\bavailabel\b": "available",
    r"\bvaccant\b": "vacant",
    r"\bvacent\b": "vacant",
    r"\bvacant\b": "vacant",
    r"\bgent\b": "gents",
    r"\bladis\b": "ladies",
    r"\bcomplent\b": "complaint",
    r"\bcompaint\b": "complaint",
    r"\bcomplain\b": "complaint",
    r"\bcomplains\b": "complaints",
    r"\bcomplaints\b": "complaints",
    r"\boccupncy\b": "occupancy",
    r"\boccupency\b": "occupancy",
    r"\ballotmnt\b": "allotment",
    r"\ballottment\b": "allotment",
    r"\bsummry\b": "summary",
    r"\bbilding\b": "building",
    r"\bbulding\b": "building",
    r"\bstaying\b": "staying",
    r"\bstayng\b": "staying",
}


def normalize_hostel_message(message: str) -> str:
    """Apply hostel-specific typo corrections."""
    text = message
    for pattern, replacement in _HOSTEL_TYPO_MAP.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


# ═══════════════════════════════════════════════════════════════════
# Hostel flow definitions
# ═══════════════════════════════════════════════════════════════════

HOSTEL_FLOWS = {
    "hostel_availability_occupency": {
        "module": "hostel",
        "requires_name": False,
        "slots_order": ["building_id"],
    },
    "hostel_full_rooms": {
        "module": "hostel",
        "requires_name": False,
        "slots_order": [],
    },
    "hostel_room_by_trainee": {
        "module": "hostel",
        "requires_name": True,
        "slots_order": ["user_id"],
    },
    "hostel_trainees_by_room": {
        "module": "hostel",
        "requires_name": False,
        "slots_order": [],
    },
    "hostel_trainees_by_building": {
        "module": "hostel",
        "requires_name": False,
        "slots_order": [],
    },
    "hostel_building_summary": {
        "module": "hostel",
        "requires_name": False,
        "slots_order": [],
    },
    "hostel_vacant_beds_by_building": {
        "module": "hostel",
        "requires_name": False,
        "slots_order": [],
    },
    "hostel_dues_by_trainee": {
        "module": "hostel",
        "requires_name": True,
        "slots_order": ["user_id"],
    },
    "hostel_allocation_summary": {
        "module": "hostel",
        "requires_name": False,
        "slots_order": [],
    },
}


# ═══════════════════════════════════════════════════════════════════
# Slot extraction helpers
# ═══════════════════════════════════════════════════════════════════

_HOSTEL_STOP_WORDS = {
    "show", "list", "get", "find", "what", "which", "who", "how",
    "many", "is", "are", "the", "of", "for", "in", "a", "an", "and",
    "to", "from", "with", "by", "on", "at", "all", "my", "me", "i",
    "hostel", "room", "rooms", "bed", "beds", "building", "buildings",
    "stay", "staying", "available", "vacant", "empty", "availability",
    "full", "occupied", "occupancy", "allocation", "allotment", "allotted",
    "trainee", "trainees", "student", "students", "occupants",
    "please", "tell", "give", "details", "detail", "about",
    "total", "count", "number", "check", "summary", "wise",
    "current", "pending", "resolved", "paid", "unpaid", "due", "dues",
    "complaint", "complaints", "gents", "ladies", "boys", "girls",
    "male", "female", "does", "have", "has", "do", "there",
    "we", "us", "our", "much", "any", "some",
}


def _extract_hostel_trainee_name(message: str) -> Optional[str]:
    """Extract a potential person name from hostel context messages."""
    text = re.sub(r'[?!.,;:\'\"()\[\]{}]', ' ', message.strip())
    words = text.split()
    name_parts = []
    for word in words:
        if word.lower() in _HOSTEL_STOP_WORDS:
            continue
        if word.isdigit():
            continue
        if len(word) <= 1:
            continue
        name_parts.append(word)
    if name_parts:
        return " ".join(name_parts)
    return None


def _extract_room_number(message: str) -> Optional[str]:
    """Extract room number from patterns like room 101, room no 101, 101 room."""
    # Match "room 101", "room no 101", "room no. 101", "room number 101"
    m = re.search(r"room\s+(?:no\.?\s+|number\s+)?(\d+)", message, re.IGNORECASE)
    if m:
        return m.group(1)
    # Match "101 room"
    m = re.search(r"(\d+)\s+room", message, re.IGNORECASE)
    if m:
        return m.group(1)
    # Match standalone room numbers in "who is staying in 101", "occupants of 101"
    m = re.search(r"(?:in|of)\s+(\d{2,4})\b", message, re.IGNORECASE)
    if m:
        return m.group(1)
    return None


def _extract_hostel_type(message: str) -> Optional[str]:
    """Extract hostel type: gents or ladies."""
    text = message.lower()
    if re.search(r"\b(gents|boys|male)\b", text):
        return "gents"
    if re.search(r"\b(ladies|girls|female)\b", text):
        return "ladies"
    return None


def _extract_complaint_status(message: str) -> Optional[str]:
    """Extract complaint status filter."""
    text = message.lower()
    if re.search(r"\b(pending|open)\b", text):
        return "pending"
    if re.search(r"\b(resolved|closed|done)\b", text):
        return "resolved"
    if re.search(r"\ball\b", text):
        return "all"
    return None


def _extract_dues_status(message: str) -> Optional[str]:
    """Extract dues status filter."""
    text = message.lower()
    if re.search(r"\b(pending|unpaid|due)\b", text):
        return "pending"
    if re.search(r"\b(paid|cleared)\b", text):
        return "paid"
    if re.search(r"\ball\b", text):
        return "all"
    return None


def _extract_availability_type(message: str) -> Optional[str]:
    """Extract whether user asks about rooms or beds."""
    text = message.lower()
    if re.search(r"\bbed", text):
        return "beds"
    if re.search(r"\broom", text):
        return "rooms"
    return None


# ═══════════════════════════════════════════════════════════════════
# Rule-based hostel flow detection
# ═══════════════════════════════════════════════════════════════════

def detect_hostel_guided_flow(message: str) -> Optional[Dict[str, Any]]:
    """Detect if message matches a hostel guided flow.

    Returns a detection dict or None if no match.
    """
    text = normalize_hostel_message(message.lower().strip())

    print(f"[Hostel Guided] Message: {message}")

    # ── DISAMBIGUATION: Do NOT capture exam / attendance / pure trainee questions ──
    if re.search(r"marks|result|exam|pass\b|fail|subject|score|grade|topper|re-exam|reexam", text):
        print("[Hostel Guided] Skipped — exam/marks context detected")
        return None
    if re.search(r"attendance|present\b|absent\b|punch|biometric", text):
        print("[Hostel Guided] Skipped — attendance context detected")
        return None
    if re.search(r"complain|complaint|complaints|issue|compaint|complent", text):
        print("[Hostel Guided] Skipped — complaint context detected")
        return None

    # Pure trainee profile questions without hostel context
    has_hostel_context = bool(re.search(
        r"hostel|room\b|bed\b|building|stay|staying|vacant|available|occupan|allot|dues.*hostel|hostel.*dues",
        text
    ))
    if not has_hostel_context:
        print("[Hostel Guided] Skipped — no hostel context found")
        return None

    # Build common slots
    slots: Dict[str, Any] = {
        "trainee_name": None,
        "building_name": None,
        "building_id": None,
        "room_number": None,
        "hostel_type": None,
        "availability_type": None,
        "complaint_status": None,
        "dues_status": None,
    }

    # Extract slots from message
    room_number = _extract_room_number(message)
    if room_number:
        slots["room_number"] = room_number

    hostel_type = _extract_hostel_type(message)
    if hostel_type:
        slots["hostel_type"] = hostel_type

    complaint_status = _extract_complaint_status(message)
    if complaint_status:
        slots["complaint_status"] = complaint_status

    dues_status = _extract_dues_status(message)
    if dues_status:
        slots["dues_status"] = dues_status

    availability_type = _extract_availability_type(message)
    if availability_type:
        slots["availability_type"] = availability_type

    # ── hostel_dues_by_trainee ──
    if re.search(r"hostel\s+dues|dues.*hostel", text):
        name = _extract_hostel_trainee_name(message)
        if name:
            slots["trainee_name"] = name
            return _build_result("hostel_dues_by_trainee", slots, "matched hostel dues by trainee pattern")

    # ── hostel_room_by_trainee (person + room/staying/stay/allocation/hostel) ──
    if re.search(r"which\s+room|room\s+of\b|hostel\s+room|hostel\s+allocation|where\s+is\s+\w+\s+staying", text):
        name = _extract_hostel_trainee_name(message)
        if name:
            slots["trainee_name"] = name
            return _build_result("hostel_room_by_trainee", slots, "matched hostel room by trainee pattern")

    # ── hostel_trainees_by_room (room number + who/students/trainees/occupants) ──
    if room_number and re.search(r"who|student|trainee|occupant|staying|list|show", text):
        return _build_result("hostel_trainees_by_room", slots, "matched trainees by room pattern")

    # ── hostel_availability_occupency (available/vacant + room/bed/hostel OR occupied + room/bed/hostel) ──
    if re.search(r"available|vacant|empty|availability|occupied", text) and re.search(r"room|bed|hostel", text):
        # Check if it's specifically about vacant beds by building
        if re.search(r"building\s+wise|by\s+building|per\s+building|by\s+hostel", text):
            return _build_result("hostel_vacant_beds_by_building", slots, "matched vacant beds by building pattern")
        return _build_result("hostel_availability_occupency", slots, "matched hostel availability pattern")

    # ── hostel_full_rooms ──
    if re.search(r"full\s+room|room.*full|full\s+hostel|fully\s+occupied", text):
        return _build_result("hostel_full_rooms", slots, "matched full rooms pattern")

    # ── hostel_vacant_beds_by_building ──
    if re.search(r"vacant\s+beds?\s+(?:by|per|building|wise)|most\s+available\s+beds?|building\s+wise\s+vacant", text):
        return _build_result("hostel_vacant_beds_by_building", slots, "matched vacant beds by building pattern")

    # ── hostel_building_summary ──
    if re.search(r"building\s+summary|hostel\s+summary|room\s+summary|bed\s+summary", text):
        return _build_result("hostel_building_summary", slots, "matched building summary pattern")

    # ── hostel_allocation_summary ──
    if re.search(r"allocation\s+summary|occupancy\s+summary|total\s+hostel\s+student|how\s+many|hostel\s+occupancy|count|wise", text) and re.search(r"building|hostel|trainee|student|staying", text):
        return _build_result("hostel_allocation_summary", slots, "matched allocation summary pattern")

    # ── hostel_trainees_by_building ──
    if re.search(r"trainee|student|staying|list|show", text) and re.search(r"building|hostel", text):
        # Avoid capturing summary queries
        if not re.search(r"summary|count|how\s+many|wise|total", text):
            return _build_result("hostel_trainees_by_building", slots, "matched trainees by building pattern")

    # ── hostel_dues_by_trainee (fallback for dues with name) ──
    if re.search(r"dues", text):
        name = _extract_hostel_trainee_name(message)
        if name:
            slots["trainee_name"] = name
            return _build_result("hostel_dues_by_trainee", slots, "matched hostel dues pattern with name")

    # ── Broader hostel room by trainee (name + hostel context) ──
    if re.search(r"hostel", text):
        name = _extract_hostel_trainee_name(message)
        if name and re.search(r"room|stay|staying|allot|allocation", text):
            slots["trainee_name"] = name
            return _build_result("hostel_room_by_trainee", slots, "matched broad hostel room by trainee")

    print("[Hostel Guided] No flow matched")
    return None


def _build_result(flow_id: str, slots: dict, reason: str) -> dict:
    """Build standard detection result dict."""
    print(f"[Hostel Guided] Flow: {flow_id}")
    print(f"[Hostel Guided] Slots: {slots}")
    return {
        "flow_id": flow_id,
        "module": "hostel",
        "slots": slots,
        "reason": reason,
    }
