"""Role-based access control for guided flows."""

from typing import Dict, Any


def can_access_guided_flow(role: str, module: str, flow_id: str, slots: Dict[str, Any], office_id: int) -> bool:
    """Check if the current role is allowed to execute the specific guided flow."""
    
    # ── Default allow for other modules since access control might be implemented directly inside them ──
    if module not in ["timetable", "faculty", "library", "mess"]:
        return True
        
    role = role.lower().strip()

    # ── Mess Role Matrix ──
    if module == "mess":
        if role in ["admin", "principal", "mess_staff"]:
            return True
        
        if role == "hostel_warden":
            allowed = {"mess_dues_by_trainee", "pending_mess_dues", "mess_bill_summary", "mess_receipts_by_trainee", "mess_refund_summary"}
            return flow_id in allowed
            
        if role == "course_coordinator":
            allowed = {"mess_bill_summary", "pending_mess_dues"}
            return flow_id in allowed
            
        if role in ["trainee", "student"]:
            allowed = {"mess_dues_by_trainee", "mess_receipts_by_trainee", "mess_refund_summary"}
            # Business logic allows trainees to see their own dues only.
            # In a fully authenticated setup, we would verify the requested user_id matches the session user.
            return flow_id in allowed
            
        # library_staff, exam_staff, attendance_staff etc. default deny
        return False


    # ── Library Role Matrix ──
    if module == "library":
        if role in ["admin", "principal", "library_staff"]:
            return True
            
        if role == "course_coordinator":
            allowed = {"book_search", "book_availability", "library_book_count", "book_type_summary", "issued_books_by_trainee"}
            return flow_id in allowed
            
        if role in ["trainee", "student"]:
            allowed = {"book_search", "book_availability", "issued_books_by_trainee", "pending_book_returns", "overdue_books"}
            # In real system, verify slots["user_id"] == logged in user
            return flow_id in allowed
            
        if role in ["hostel_warden", "exam_staff", "attendance_staff"]:
            allowed = {"book_search", "book_availability"}
            return flow_id in allowed
            
        return False
        
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
