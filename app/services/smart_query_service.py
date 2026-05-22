"""Smart query service - dispatches to module-specific query handlers."""
import traceback
from typing import Any, Dict
from app.services.db_service import get_connection
from app.services.queries import (
    exam_queries, hostel_queries, trainee_queries, course_queries,
    attendance_queries, timetable_queries, faculty_vl_queries, feedback_queries,
    complaint_queries, library_queries, mess_queries, vehicle_queries,
    meeting_queries, seminar_queries, inspection_queries, sports_queries,
    pass_eq_queries, field_study_tour_queries, master_admin_queries
)

# Aggregate all templates from module files
QUERY_TEMPLATES = (
    exam_queries.TEMPLATES +
    hostel_queries.TEMPLATES +
    trainee_queries.TEMPLATES +
    course_queries.TEMPLATES +
    attendance_queries.TEMPLATES +
    timetable_queries.TEMPLATES +
    faculty_vl_queries.TEMPLATES +
    feedback_queries.TEMPLATES +
    complaint_queries.TEMPLATES +
    library_queries.TEMPLATES +
    mess_queries.TEMPLATES +
    vehicle_queries.TEMPLATES +
    meeting_queries.TEMPLATES +
    seminar_queries.TEMPLATES +
    inspection_queries.TEMPLATES +
    sports_queries.TEMPLATES +
    pass_eq_queries.TEMPLATES +
    field_study_tour_queries.TEMPLATES +
    master_admin_queries.TEMPLATES
)

# Ordered list of module handlers to try
_MODULE_HANDLERS = [
    exam_queries, hostel_queries, trainee_queries, course_queries,
    attendance_queries, timetable_queries, faculty_vl_queries, feedback_queries,
    complaint_queries, library_queries, mess_queries, vehicle_queries,
    meeting_queries, seminar_queries, inspection_queries, sports_queries,
    pass_eq_queries, field_study_tour_queries, master_admin_queries
]


def get_relevant_templates(question: str) -> list:
    """Filter templates based on keywords to avoid exceeding LLM context limits."""
    text = question.lower()
    exam_words = {"exam", "marks", "mark", "result", "pass", "fail", "score", "grade", "subject", "percentage", "top", "bottom", "lowest", "highest", "performers"}
    hostel_words = {"hostel", "room", "bed", "building", "warden", "allocation", "checkin", "checkout", "occupancy", "vacant", "complaint", "feedback"}
    trainee_words = {"trainee", "student", "attendance", "present", "absent", "leave", "department", "designation", "nominee", "linen", "field"}
    course_words = {"course", "courses", "batch", "batches", "program", "course group", "course for", "promotion course", "refresher course", "initial course", "upcoming course", "ongoing course", "completed course", "seat capacity", "certificate course", "online exam course"}
    attendance_words = {"attendance", "present", "absent", "punch", "biometric"}
    timetable_words = {"timetable", "time table", "lecture", "schedule", "session", "class room", "topic"}
    faculty_vl_words = {"faculty", "visiting lecturer", "vl", "lecturer", "speaker"}
    feedback_words = {"feedback", "rating", "review", "response", "question feedback"}
    complaint_words = {"complaint", "complain", "pending complaint", "closed complaint", "category complaint"}
    library_words = {"library", "book", "books", "issue book", "return book", "fine"}
    mess_words = {"mess", "bill", "receipt", "dues", "food", "meal", "item price", "material"}
    vehicle_words = {"vehicle", "bus", "driver", "trip", "booking", "km", "kilometer", "pnr", "travel"}
    meeting_words = {"meeting", "agenda", "mom", "minutes", "chairman", "invitee"}
    seminar_words = {"seminar", "speaker", "judge", "seminar topic"}
    inspection_words = {"inspection", "inspection note", "inspection description"}
    sports_words = {"sport", "sports", "team", "participant", "sport item", "game"}
    pass_eq_words = {"pass", "privilege pass", "eq", "railway pass", "ticket", "pnr", "train class"}
    field_study_tour_words = {"field training", "study tour", "tour", "outdoor training", "filled training"}
    master_admin_words = {"user", "role", "permission", "department", "designation", "grade", "service", "zone", "division", "depot", "station", "bank", "company", "holiday", "place"}
    
    active_templates = []
    if any(w in text for w in exam_words):
        active_templates.extend(exam_queries.TEMPLATES)
    if any(w in text for w in hostel_words):
        active_templates.extend(hostel_queries.TEMPLATES)
    if any(w in text for w in trainee_words):
        active_templates.extend(trainee_queries.TEMPLATES)
    if any(w in text for w in course_words):
        active_templates.extend(course_queries.TEMPLATES)
    if any(w in text for w in attendance_words):
        active_templates.extend(attendance_queries.TEMPLATES)
    if any(w in text for w in timetable_words):
        active_templates.extend(timetable_queries.TEMPLATES)
    if any(w in text for w in faculty_vl_words):
        active_templates.extend(faculty_vl_queries.TEMPLATES)
    if any(w in text for w in feedback_words):
        active_templates.extend(feedback_queries.TEMPLATES)
    if any(w in text for w in complaint_words):
        active_templates.extend(complaint_queries.TEMPLATES)
    if any(w in text for w in library_words):
        active_templates.extend(library_queries.TEMPLATES)
    if any(w in text for w in mess_words):
        active_templates.extend(mess_queries.TEMPLATES)
    if any(w in text for w in vehicle_words):
        active_templates.extend(vehicle_queries.TEMPLATES)
    if any(w in text for w in meeting_words):
        active_templates.extend(meeting_queries.TEMPLATES)
    if any(w in text for w in seminar_words):
        active_templates.extend(seminar_queries.TEMPLATES)
    if any(w in text for w in inspection_words):
        active_templates.extend(inspection_queries.TEMPLATES)
    if any(w in text for w in sports_words):
        active_templates.extend(sports_queries.TEMPLATES)
    if any(w in text for w in pass_eq_words):
        active_templates.extend(pass_eq_queries.TEMPLATES)
    if any(w in text for w in field_study_tour_words):
        active_templates.extend(field_study_tour_queries.TEMPLATES)
    if any(w in text for w in master_admin_words):
        active_templates.extend(master_admin_queries.TEMPLATES)
        
    if not active_templates:
        return QUERY_TEMPLATES
        
    return active_templates


def execute_smart_query(query_id: str, params: Dict[str, Any], office_id: int) -> str:
    conn = get_connection()
    try:
        cur = conn.cursor()
        # Try each module handler in order
        for module in _MODULE_HANDLERS:
            result = module.execute(query_id, params or {}, cur, office_id)
            if result is not None:
                return result
        return None
    except Exception as e:
        print(f"Error executing smart query {query_id}: {traceback.format_exc()}")
        return f"Error processing request: {str(e)}"
    finally:
        conn.close()
