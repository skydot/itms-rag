"""Role-based access control for guided flows."""

from typing import Dict, Any


def can_access_guided_flow(role: str, module: str, flow_id: str, slots: Dict[str, Any], office_id: int) -> bool:
    """Check if the current role is allowed to execute the specific guided flow."""
    
    # ── Default allow for other modules since access control might be implemented directly inside them ──
    if module not in ["timetable", "faculty"]:
        return True
        
    role = role.lower().strip()

    # ── Faculty Role Matrix ──
    if module == "faculty":
        if role in ["admin", "principal", "course_coordinator"]:
            return True
            
        if role == "faculty":
            # For now, allow faculty to see all faculty schedules and workloads
            # since we don't have authenticated user context to restrict to own
            return True
            
        if role == "attendance_staff":
            allowed = {"faculty_schedule", "faculty_by_course", "faculty_by_subject"}
            return flow_id in allowed
            
        if role == "trainee" or role == "student":
            allowed = {"faculty_by_course", "faculty_by_subject"}
            return flow_id in allowed
            
        if role == "hostel_warden":
            return False
            
        if role == "exam_staff":
            allowed = {"faculty_by_subject", "faculty_by_course"}
            return flow_id in allowed
            
        return False
        
    # ── Timetable Role Matrix ──
    role = role.lower().strip()
    
    if role in ["admin", "principal", "course_coordinator"]:
        return True
        
    if role == "faculty":
        allowed = {
            "today_timetable", "tomorrow_timetable", "date_wise_timetable",
            "faculty_timetable", "subject_timetable", "timetable_summary",
            "course_timetable", "classroom_timetable", "session_timetable", "free_slots"
        }
        return flow_id in allowed
        
    if role == "attendance_staff":
        allowed = {
            "today_timetable", "tomorrow_timetable", "course_timetable", "date_wise_timetable"
        }
        return flow_id in allowed
        
    if role == "trainee" or role == "student":
        # Trainees only allowed to see their course timetable
        # In a real implementation we would check if slots["course_id"] == trainee's active course
        # For now, allow course-specific or general today/tomorrow flows
        allowed = {
            "today_timetable", "tomorrow_timetable", "course_timetable", "date_wise_timetable"
        }
        return flow_id in allowed
        
    if role == "hostel_warden":
        return False
        
    if role == "exam_staff":
        allowed = {"course_timetable", "today_timetable"}
        return flow_id in allowed

    # Default deny for timetable if role is unknown or not explicitly allowed
    return False
