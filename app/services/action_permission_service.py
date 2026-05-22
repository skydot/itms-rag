import random
from app.services.redirect_service import build_redirect_url
from app.services.action_audit_service import log_action

def can_execute_action(role: str, action: str, module: str) -> bool:
    """Checks if the user role has permission to execute the given action."""
    # Base normalization
    r = role.lower().strip()
    
    if r in ["principal", "admin", "master_admin"]:
        return True
        
    if r == "hostel_warden":
        return action in ["allot_hostel_room", "create_complaint", "close_complaint"]
        
    if r == "exam_admin":
        return action in ["generate_certificate", "generate_icard"]
        
    if r == "course_admin":
        return action in ["create_meeting", "create_vehicle_booking", "mark_attendance", "update_attendance"]

    # Default deny for all other roles/actions
    return False
