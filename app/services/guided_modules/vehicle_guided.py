import re
from typing import Optional, Dict

VEHICLE_FLOWS = {
    "vehicle_list": {
        "flow_id": "vehicle_list",
        "module": "vehicle",
        "slots_order": [],
        "requires_name": False
    },
    "vehicle_availability": {
        "flow_id": "vehicle_availability",
        "module": "vehicle",
        "slots_order": [],
        "requires_name": False
    },
    "vehicle_usage_summary": {
        "flow_id": "vehicle_usage_summary",
        "module": "vehicle",
        "slots_order": [],
        "requires_name": False
    },
    "vehicle_register_history": {
        "flow_id": "vehicle_register_history",
        "module": "vehicle",
        "slots_order": [],
        "requires_name": False
    },
    "study_tour_vehicle_usage": {
        "flow_id": "study_tour_vehicle_usage",
        "module": "vehicle",
        "slots_order": ["course_id"],
        "requires_name": False
    },
    "field_training_vehicle_usage": {
        "flow_id": "field_training_vehicle_usage",
        "module": "vehicle",
        "slots_order": ["course_id"],
        "requires_name": False
    },
    "vehicle_by_driver": {
        "flow_id": "vehicle_by_driver",
        "module": "vehicle",
        "slots_order": [],
        "requires_name": False
    },
    "vehicle_count": {
        "flow_id": "vehicle_count",
        "module": "vehicle",
        "slots_order": [],
        "requires_name": False
    },
    "vehicle_maintenance": {
        "flow_id": "vehicle_maintenance",
        "module": "vehicle",
        "slots_order": [],
        "requires_name": False
    },
    "recent_vehicle_activity": {
        "flow_id": "recent_vehicle_activity",
        "module": "vehicle",
        "slots_order": [],
        "requires_name": False
    }
}


# ── Typo normalization map ──
_TYPO_MAP = {
    r"\bvehical\b": "vehicle",
    r"\bvehicl\b": "vehicle",
    r"\bvechile\b": "vehicle",
    r"\bvechicle\b": "vehicle",
    r"\bvehcile\b": "vehicle",
    r"\bavailble\b": "available",
    r"\bavilable\b": "available",
    r"\bavalab[le]+\b": "available",
    r"\btripps\b": "trips",
    r"\bdrivr\b": "driver",
    r"\bdriveer\b": "driver",
    r"\bmaintanance\b": "maintenance",
    r"\bmaintainance\b": "maintenance",
    r"\bmaintenace\b": "maintenance",
    r"\brepar\b": "repair",
    r"\btranspot\b": "transport",
    r"\btrasport\b": "transport",
    r"\bregistter\b": "register",
    r"\bregistary\b": "register",
    r"\bregistar\b": "register",
}

# ── Vehicle-related keywords for positive matching ──
_VEHICLE_KEYWORDS = re.compile(
    r"\b(vehicles?|transport|trips?|drivers?|buses|bus|cars?|jeeps?|vans?|trucks?|"
    r"vehicle_masters|vehicle_registers|fleet|automobiles?)\b", re.I
)


def normalize_vehicle_message(message: str) -> str:
    """Normalize typos in vehicle-related messages."""
    text = message
    for pattern, replacement in _TYPO_MAP.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def detect_vehicle_guided_flow(message: str) -> Optional[Dict]:
    """Detect if a message matches a vehicle guided flow.

    Returns dict with flow_id, module, slots, reason — or None.
    """
    text = normalize_vehicle_message(message)
    lower = text.lower().strip()

    print(f"[Vehicle Guided] Message: {text}")

    # ── Build default slots ──
    slots = {
        "vehicle_number": None,
        "vehicle_id": None,
        "vehicle_type": None,
        "driver_name": None,
        "driver_id": None,
        "course_name": None,
        "course_id": None,
        "tour_name": None,
        "tour_id": None,
        "field_training_id": None,
        "date": None,
        "from_date": None,
        "to_date": None,
        "date_range": None,
        "status": None,
        "limit": None,
    }

    has_vehicle_word = bool(_VEHICLE_KEYWORDS.search(lower))

    # ── Negative guards ──
    # If other modules' keywords present WITHOUT any vehicle/transport word → skip
    if re.search(r"\b(marks|result|exam|pass|fail|grade)\b", lower) and not has_vehicle_word:
        return None
    if re.search(r"\b(attendance|present|absent|absent)\b", lower) and not has_vehicle_word:
        return None
    if re.search(r"\b(hostel|room|bed|staying)\b", lower) and not has_vehicle_word:
        return None
    if re.search(r"\b(mess|library|book|complaint|timetable|faculty)\b", lower) and not has_vehicle_word:
        return None
    # study tour / field training without vehicle/transport word → let study_tour module handle
    if re.search(r"\b(study tour|field training)\b", lower) and not has_vehicle_word:
        return None

    def _build_result(flow_id: str, reason: str) -> Dict:
        result = {
            "flow_id": flow_id,
            "module": "vehicle",
            "slots": slots,
            "reason": reason
        }
        print(f"[Vehicle Guided] Flow: {flow_id}")
        print(f"[Vehicle Guided] Slots: {slots}")
        return result

    # ── Slot extraction ──

    # Extract limit
    m_limit = re.search(r"\b(?:top|last|recent)\s+(\d+)\b", lower)
    if m_limit:
        slots["limit"] = int(m_limit.group(1))

    # Extract date
    if re.search(r"\btoday\b", lower):
        slots["date"] = "today"
    elif re.search(r"\btomorrow\b", lower):
        slots["date"] = "tomorrow"
    elif re.search(r"\byesterday\b", lower):
        slots["date"] = "yesterday"
    m_date = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", lower)
    if m_date:
        slots["date"] = m_date.group(1)

    # Extract vehicle number (patterns like GJ01, GJ-01, RJ27-PX-1427, MH12AB1234)
    m_vnum = re.search(r"\b([A-Z]{2}[\s-]?\d{1,2}[\s-]?[A-Z]{0,3}[\s-]?\d{0,4})\b", text, re.I)
    if m_vnum:
        raw = m_vnum.group(1).strip()
        # Clean: keep alphanumeric and hyphen
        cleaned = re.sub(r"[^A-Za-z0-9\-]", "", raw).upper()
        if len(cleaned) >= 4:  # At least state+district code
            slots["vehicle_number"] = cleaned

    # Extract vehicle type
    m_type = re.search(r"\b(bus|car|jeep|van|truck)\b", lower)
    if m_type:
        slots["vehicle_type"] = m_type.group(1).lower()

    # Extract driver name
    m_driver = re.search(r"(?:driver|drivr|driveer)\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)", text, re.I)
    if m_driver:
        name = m_driver.group(1).strip()
        name = re.sub(r"\b(vehicle|trip|trips|history|usage|wise|by)\b", "", name, flags=re.I).strip()
        if name:
            slots["driver_name"] = name.lower()

    # Also catch "trips by driver Ramesh" pattern
    if not slots["driver_name"]:
        m_driver2 = re.search(r"(?:trips?\s+by|by)\s+(?:driver\s+)?([A-Za-z]+(?:\s+[A-Za-z]+)?)", text, re.I)
        if m_driver2 and has_vehicle_word:
            name = m_driver2.group(1).strip()
            name = re.sub(r"\b(vehicle|trip|trips|history|usage|wise|by|driver)\b", "", name, flags=re.I).strip()
            if name:
                slots["driver_name"] = name.lower()

    # Extract course name (for study tour / field training)
    m_course = re.search(r"(?:study tour|field training|tour)\s+(?:of|for)\s+(.+?)(?:\s+vehicle|\s+transport|$)", text, re.I)
    if m_course:
        cname = m_course.group(1).strip()
        cname = re.sub(r"\b(vehicle|transport|details|trip|trips)\b", "", cname, flags=re.I).strip()
        if cname:
            slots["course_name"] = cname

    # Extract status
    m_status = re.search(r"\b(active|inactive|available|busy|pending|approved|completed|rejected)\b", lower)
    if m_status:
        slots["status"] = m_status.group(1)

    # ═══════════════════════════════════════════════
    # ── Flow matching (order matters) ──
    # ═══════════════════════════════════════════════

    # 1. vehicle_count — must be before vehicle_list
    if re.search(r"\b(how many|total|count)\b", lower) and re.search(r"\b(vehicles?|buses|bus|cars?|jeeps?|vans?|trucks?)\b", lower):
        return _build_result("vehicle_count", "matched vehicle count")

    # 2. vehicle_maintenance
    if re.search(r"\b(maintenance|repair|service|servicing)\b", lower) and has_vehicle_word:
        return _build_result("vehicle_maintenance", "matched vehicle maintenance")

    # 3. vehicle_availability
    if re.search(r"\b(availab\w*|free)\b", lower) and re.search(r"\b(vehicles?|buses|bus|cars?|transport|jeeps?|vans?|trucks?)\b", lower):
        if not slots["date"]:
            slots["date"] = "today"
        return _build_result("vehicle_availability", "matched vehicle availability")

    # 4. study_tour_vehicle_usage
    if re.search(r"\bstudy\s*tour\b", lower) and has_vehicle_word:
        return _build_result("study_tour_vehicle_usage", "matched study tour vehicle usage")

    # 5. field_training_vehicle_usage
    if re.search(r"\bfield\s*training\b", lower) and has_vehicle_word:
        return _build_result("field_training_vehicle_usage", "matched field training vehicle usage")

    # 6. vehicle_by_driver
    if slots.get("driver_name"):
        return _build_result("vehicle_by_driver", "matched vehicle by driver")
    if re.search(r"\bdriver\s*wise\b", lower) and has_vehicle_word:
        return _build_result("vehicle_by_driver", "matched driver wise vehicle usage")

    # 7. vehicle_usage_summary
    if re.search(r"\b(usage\s*summary|used\s*most|trip\s*count|vehicle\s*wise|usage\s*report)\b", lower) and has_vehicle_word:
        return _build_result("vehicle_usage_summary", "matched vehicle usage summary")

    # 8. vehicle_register_history — specific vehicle trips
    if re.search(r"\b(register\s*history|trip\s*history|trips?\s+of)\b", lower) and has_vehicle_word:
        return _build_result("vehicle_register_history", "matched vehicle register history")
    if slots.get("vehicle_number") and re.search(r"\b(history|trips?|register|details)\b", lower):
        return _build_result("vehicle_register_history", "matched vehicle register history by number")

    # 9. recent_vehicle_activity
    if re.search(r"\b(recent|latest|last)\b", lower) and re.search(r"\b(vehicle|trip|trips|transport|register|activity)\b", lower):
        if not slots["limit"]:
            slots["limit"] = 10
        return _build_result("recent_vehicle_activity", "matched recent vehicle activity")

    # 10. vehicle_list — broad catch-all for vehicle queries
    if re.search(r"\b(show|list|all|active|display)\b", lower) and re.search(r"\b(vehicles?|buses|bus|cars?|jeeps?|vans?|trucks?)\b", lower):
        return _build_result("vehicle_list", "matched vehicle list")

    # 11. Bare "vehicle" / "vehicles" or "vehicle details"
    if re.search(r"\bvehicles?\b", lower) and re.search(r"\b(details?|info|information|data|records?)\b", lower):
        return _build_result("vehicle_list", "matched vehicle details")

    return None
