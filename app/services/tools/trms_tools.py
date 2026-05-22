from langchain_core.tools import tool
from typing import Optional, Dict, Any
from app.services.action_confirmation_service import create_confirmation
from app.services.action_permission_service import can_execute_action
from app.services.redirect_service import build_redirect_url
# In a real scenario, these would call actual db_service functions. 
# Here we mock them for safety as instructed.

@tool
def search_trainee_by_name(name: str, office_id: int) -> dict:
    """Find a trainee/user record safely by their name."""
    # Mocking database search
    return {
        "found": True,
        "user_id": 1234,
        "name": name,
        "course_id": 56,
        "course_batch": "Batch 2025"
    }

@tool
def search_room_by_name(room_name: str, office_id: int) -> dict:
    """Find a hostel room safely by its name."""
    # Mocking database search
    return {
        "found": True,
        "room_id": 432,
        "room_name": room_name,
        "building_id": 12,
        "room_beds": 3
    }

@tool
def check_room_availability(room_id: int, office_id: int) -> dict:
    """Check current room occupancy and available beds."""
    # Mocking availability check
    return {
        "available": True,
        "room_id": room_id,
        "total_beds": 3,
        "occupied_beds": 1,
        "available_beds": 2
    }

@tool
def prepare_room_allotment_confirmation(trainee_name: str, room_name: str, office_id: int, role: str) -> dict:
    """Search trainee, search room, check availability, then create confirmation_required."""
    trainee = search_trainee_by_name.invoke({"name": trainee_name, "office_id": office_id})
    if not trainee["found"]:
        return {"error": f"Trainee '{trainee_name}' not found."}
        
    room = search_room_by_name.invoke({"room_name": room_name, "office_id": office_id})
    if not room["found"]:
        return {"error": f"Room '{room_name}' not found."}
        
    avail = check_room_availability.invoke({"room_id": room["room_id"], "office_id": office_id})
    if not avail["available"]:
        return {"error": f"Room '{room_name}' has no available beds."}
        
    if not can_execute_action(role, "allot_hostel_room", "hostel_allotment"):
        return {"error": "Permission denied for room allotment."}

    fields = {
        "trainee_name": trainee["name"],
        "room_name": room["room_name"]
    }
    user_context = {"role": role, "office_id": office_id}
    
    return create_confirmation("allot_hostel_room", "hostel_allotment", fields, user_context)

@tool
def prepare_complaint_confirmation(description: str, office_id: int, role: str, room_name: Optional[str] = None, building_name: Optional[str] = None, user_name: Optional[str] = None) -> dict:
    """Prepare confirmation for complaint creation."""
    if not can_execute_action(role, "create_complaint", "complaint"):
        return {"error": "Permission denied for creating complaints."}
        
    fields = {"description": description}
    if room_name: fields["room_name"] = room_name
    if building_name: fields["building_name"] = building_name
    if user_name: fields["user_name"] = user_name
    
    user_context = {"role": role, "office_id": office_id}
    return create_confirmation("create_complaint", "complaint", fields, user_context)

@tool
def prepare_icard_confirmation(trainee_name: str, office_id: int, role: str) -> dict:
    """Prepare confirmation for I-card generation."""
    trainee = search_trainee_by_name.invoke({"name": trainee_name, "office_id": office_id})
    if not trainee["found"]:
        return {"error": f"Trainee '{trainee_name}' not found."}
        
    if not can_execute_action(role, "generate_icard", "icard"):
        return {"error": "Permission denied for generating I-cards."}
        
    fields = {"trainee_name": trainee["name"]}
    user_context = {"role": role, "office_id": office_id}
    
    return create_confirmation("generate_icard", "icard", fields, user_context)

@tool
def get_redirect_url(module_name: str, record_id: int) -> str:
    """Return exact TRMS page URL using existing redirect_service.py."""
    url = build_redirect_url(module_name, record_id)
    return url if url else "URL not found"

# Expose available tools
TRMS_TOOLS = [
    search_trainee_by_name,
    search_room_by_name,
    check_room_availability,
    prepare_room_allotment_confirmation,
    prepare_complaint_confirmation,
    prepare_icard_confirmation,
    get_redirect_url
]
