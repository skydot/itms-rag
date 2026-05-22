import random
from app.services.redirect_service import build_redirect_url
from app.services.action_audit_service import log_action
from app.services.action_permission_service import can_execute_action

def execute_action(action: str, fields: dict, user_context: dict) -> dict:
    """Executes the action safely. Returns the result dict."""
    module = None
    
    # Simple mapping to get module name for redirect
    if "customer" in action:
        module = "customer"
    elif "trainee" in action:
        module = "trainee"
    elif "hostel" in action:
        module = "hostel_allotment"
    elif "complaint" in action:
        module = "complaint"
    elif "icard" in action:
        module = "icard"
    elif "certificate" in action:
        module = "certificate"
    elif "attendance" in action:
        module = "attendance"
    elif "meeting" in action:
        module = "meeting"
    elif "vehicle" in action:
        module = "vehicle_booking"
    elif "library" in action:
        module = "library_issue"
    else:
        module = "unknown"

    role = user_context.get("role", "default")
    if not can_execute_action(role, action, module):
        return {
            "type": "action_result",
            "status": "denied",
            "message": "You do not have permission to perform this action.",
            "action": action,
            "module": module,
            "record_id": None,
            "redirect_url": None
        }

    # Simulate DB operation and get a dummy record ID
    record_id = random.randint(100, 999)
    
    success_message = f"Action '{action}' executed successfully."
    if action == "create_customer":
        name = fields.get("name", "Unknown")
        success_message = f"Customer {name} created successfully."
    elif action == "allot_hostel_room":
        room = fields.get("room_name", "")
        trainee = fields.get("trainee_name", "")
        success_message = f"Room {room} allotted to {trainee} successfully."
        
    redirect_url = build_redirect_url(module, record_id)
    
    log_action(
        action=action,
        module=module,
        user_context=user_context,
        fields=fields,
        status="success",
        record_id=record_id
    )

    return {
        "type": "action_result",
        "status": "success",
        "action": action,
        "module": module,
        "message": success_message,
        "record_id": record_id,
        "redirect_url": redirect_url
    }
