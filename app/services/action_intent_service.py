import re

# Action verbs mapping
CREATE_VERBS = {"create", "add", "register", "generate", "make", "issue", "allot", "assign", "book", "schedule", "mark"}
UPDATE_VERBS = {"update", "change", "edit", "modify", "correct"}
DELETE_VERBS = {"delete", "remove", "cancel", "close"}

# Supported action mappings (action -> (module, operation))
SUPPORTED_ACTIONS = {
    "create_customer": ("customer", "create"),
    "update_customer": ("customer", "update"),
    "create_trainee": ("trainee", "create"),
    "update_trainee": ("trainee", "update"),
    "allot_hostel_room": ("hostel_allotment", "create"),
    "create_complaint": ("complaint", "create"),
    "close_complaint": ("complaint", "update"),
    "generate_icard": ("icard", "create"),
    "generate_certificate": ("certificate", "create"),
    "mark_attendance": ("attendance", "create"),
    "update_attendance": ("attendance", "update"),
    "create_meeting": ("meeting", "create"),
    "create_vehicle_booking": ("vehicle_booking", "create"),
    "issue_library_book": ("library_issue", "create"),
    "return_library_book": ("library_issue", "update"),
}

def detect_action_intent(message: str) -> dict:
    """Detects if a message is an action intent and returns details."""
    text = message.lower()
    
    # Exclude non-action questions
    if any(q in text for q in ["how", "show", "list", "who", "what", "where", "when", "why"]):
        return {"is_action": False, "action": None, "module": None, "operation": None, "confidence": 0.0}

    words = set(re.findall(r'\b\w+\b', text))
    
    verb_found = None
    if words.intersection(CREATE_VERBS):
        verb_found = "create"
    elif words.intersection(UPDATE_VERBS):
        verb_found = "update"
    elif words.intersection(DELETE_VERBS):
        verb_found = "delete"
        
    if not verb_found:
        return {"is_action": False, "action": None, "module": None, "operation": None, "confidence": 0.0}
        
    action_intent = None
    
    if "customer" in text:
        action_intent = f"{verb_found}_customer" if verb_found in ["create", "update"] else None
    elif "trainee" in text or "student" in text:
        action_intent = f"{verb_found}_trainee" if verb_found in ["create", "update"] else None
    elif "room" in text or "hostel" in text:
        if verb_found == "create" and "allot" in text or "assign" in text:
            action_intent = "allot_hostel_room"
    elif "complaint" in text:
        if verb_found == "create":
            action_intent = "create_complaint"
        elif verb_found == "delete" or "close" in text:
            action_intent = "close_complaint"
    elif "icard" in text or "i-card" in text:
        action_intent = "generate_icard" if verb_found == "create" else None
    elif "certificate" in text:
        action_intent = "generate_certificate" if verb_found == "create" else None
    elif "attendance" in text:
        action_intent = f"{verb_found}_attendance" if verb_found in ["create", "update"] else None
        if "mark" in text:
            action_intent = "mark_attendance"
    elif "meeting" in text:
        action_intent = "create_meeting" if verb_found == "create" else None
    elif "vehicle" in text or "booking" in text or "bus" in text:
        action_intent = "create_vehicle_booking" if verb_found == "create" else None
    elif "book" in text or "library" in text:
        if "issue" in text:
            action_intent = "issue_library_book"
        elif "return" in text:
            action_intent = "return_library_book"

    if action_intent and action_intent in SUPPORTED_ACTIONS:
        module, operation = SUPPORTED_ACTIONS[action_intent]
        return {
            "is_action": True,
            "action": action_intent,
            "module": module,
            "operation": operation,
            "confidence": 0.9
        }
        
    return {"is_action": False, "action": None, "module": None, "operation": None, "confidence": 0.0}
