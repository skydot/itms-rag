"""Per-module guided intent parsers.

Each module gets its own focused prompt with ONLY its own flows,
so the LLM has fewer options and picks more accurately.

Usage:
    parse_guided_intent(message, module_hint)
    → dispatches to the right module-specific parser
"""

import json
import logging
from typing import Dict, Any, Optional

from app.services.llm_service import call_llm

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════
# Shared response format (appended to every module prompt)
# ═══════════════════════════════════════════════════════════════════

_RESPONSE_FORMAT = """
Return JSON:
{"matches_guided_flow":true,"flow_id":"...","confidence":0.9,"slots":{...},"reason":"..."}
If unsure: {"matches_guided_flow":false,"flow_id":null,"confidence":0,"slots":{},"reason":"..."}

JSON only. No markdown. No explanation.
"""

_SYSTEM_BASE = """You are a TRMS guided-flow intent parser.
Return valid JSON only. No markdown. No explanation.
Do not generate SQL. Do not answer the user.
Your job: map a question to one guided flow and extract slots.
"""


# ═══════════════════════════════════════════════════════════════════
# Exam module prompt (12 flows)
# ═══════════════════════════════════════════════════════════════════

_EXAM_PROMPT = _SYSTEM_BASE + """
Guided flows (EXAM module only):

1. exam_marks_by_trainee — marks/score of a specific trainee
Examples: "Mayank marks", "marks of Mayank", "mayank marks in recent exam"
Slots: trainee_name, course_name, exam_filter, exam_type_name, subject_name, year

2. exam_result_by_trainee — did trainee pass or fail
Examples: "Did Mayank pass?", "Mayank pass or fail?", "result of Mayank"
Slots: trainee_name, course_name, exam_filter, year

3. failed_trainees — list/count of failed trainees (NO trainee name needed)
Examples: "Show failed trainees", "How many failed?", "failed students in exam"
Slots: course_name, exam_type_name, subject_name, year

4. failed_trainees_by_subject — which subject has most failures
Examples: "Which subject has highest failed trainees?", "subject wise fail count"
Slots: course_name, exam_type_name, year

5. passed_trainees — list/count of passed trainees
Examples: "Show passed trainees", "How many passed?"
Slots: course_name, exam_type_name, subject_name, year

6. not_appeared_trainees — who did not appear / absent in exam
Examples: "Who did not appear?", "absent in exam", "not appeared trainees"
Slots: course_name, exam_type_name, subject_name, year

7. top_performers — highest marks / topper (NO trainee name needed)
Examples: "Who got highest marks?", "top 5 performers", "exam topper"
Slots: course_name, exam_type_name, subject_name, year, limit

8. lowest_performers — lowest marks (NO trainee name needed)
Examples: "Who got lowest marks?", "bottom 5 performers"
Slots: course_name, exam_type_name, subject_name, year, limit

9. subject_wise_marks_summary — average marks per subject
Examples: "Subject wise average marks", "subject wise performance"
Slots: course_name, exam_type_name, year

10. course_exam_summary — course wise pass/fail summary
Examples: "Course wise exam result", "pass fail summary by course"
Slots: year, course_name

11. re_exam_trainees — trainees in re-exam
Examples: "Show re-exam trainees", "re exam students"
Slots: course_name, year

12. pass_percentage — pass rate / percentage
Examples: "What is pass percentage?", "course pass percentage"
Slots: course_name, exam_type_name, subject_name, year

exam_filter values: recent/latest/current/last/all/final/phase_1/phase_2/re_exam
""" + _RESPONSE_FORMAT


# ═══════════════════════════════════════════════════════════════════
# Trainee module prompt (10 flows)
# ═══════════════════════════════════════════════════════════════════

_TRAINEE_PROMPT = _SYSTEM_BASE + """
Guided flows (TRAINEE module only):

1. trainee_profile_by_name — basic details of a specific trainee
Examples: "Show Mayank details", "Mayank trainee profile", "Mayank details"
Slots: trainee_name

2. active_trainee_count — count of active trainees
Examples: "How many active trainees are there?", "Active trainees count"
Slots: (none)

3. trainee_joined_by_year — trainees joined in a specific year
Examples: "How many trainees joined in 2025?", "Show trainees joined in 2025"
Slots: year

4. recent_course_trainees — trainees in recent/latest/current course
Examples: "How many students joined recent course?", "Trainees in latest course"
Slots: recent_filter (recent/latest/current/ongoing)

5. course_wise_trainee_count — trainee count per course
Examples: "Show course wise trainee count", "Course wise students"
Slots: (none)

6. batch_wise_trainee_count — trainee count per batch
Examples: "Show batch wise trainee count", "Batch wise students"
Slots: (none)

7. gender_wise_trainee_count — count of male and female trainees
Examples: "Gender wise trainee count", "How many male and female students?"
Slots: (none)

8. approved_trainees — approved trainees
Examples: "Show approved trainees", "How many approved trainees?"
Slots: (none)

9. pending_approval_trainees — trainees pending approval
Examples: "Show pending approval trainees", "How many trainees pending approval?"
Slots: (none)

10. outstay_trainees — trainees overstaying
Examples: "Show outstay trainees", "How many outstay students?"
Slots: (none)
""" + _RESPONSE_FORMAT


# ═══════════════════════════════════════════════════════════════════
# Hostel module prompt (10 flows)
# ═══════════════════════════════════════════════════════════════════

_HOSTEL_PROMPT = _SYSTEM_BASE + """
Guided flows (HOSTEL module only):

1. hostel_availability_occupency — available/occupied rooms/beds in hostel
Examples: "How many rooms are available?", "Available beds in gents hostel", "Show available rooms"
Slots: hostel_type (gents/ladies), availability_type (rooms/beds)

2. hostel_full_rooms — fully occupied rooms
Examples: "Which rooms are full?", "Show full rooms in gents hostel"
Slots: hostel_type (gents/ladies)

3. hostel_room_by_trainee — which room a trainee is staying in
Examples: "Which room is Mayank staying in?", "Mayank hostel room", "Where is Mayank staying?"
Slots: trainee_name

4. hostel_trainees_by_room — who is staying in a specific room
Examples: "Who is staying in room 101?", "Occupants of room 101"
Slots: room_number

5. hostel_trainees_by_building — trainees in a hostel building
Examples: "Show trainees in Gents Hostel", "Students in ladies hostel"
Slots: hostel_type (gents/ladies), building_name

6. hostel_building_summary — building wise room/bed summary
Examples: "Hostel building summary", "Building wise rooms and beds"
Slots: hostel_type (gents/ladies)

7. hostel_vacant_beds_by_building — vacant beds per building
Examples: "Building wise vacant beds", "Which hostel has most available beds?"
Slots: hostel_type (gents/ladies)

8. hostel_dues_by_trainee — hostel dues of a specific trainee
Examples: "Mayank hostel dues", "Pending hostel dues for Mayank"
Slots: trainee_name, dues_status (pending/paid/all)

9. hostel_complaints — hostel complaints
Examples: "Show hostel complaints", "Pending hostel complaints"
Slots: complaint_status (pending/resolved/all), hostel_type (gents/ladies)

10. hostel_allocation_summary — hostel occupancy/allocation summary
Examples: "Hostel allocation summary", "How many students are staying in hostel?"
Slots: hostel_type (gents/ladies)
""" + _RESPONSE_FORMAT


# ═══════════════════════════════════════════════════════════════════
# Attendance module prompt (10 flows)
# ═══════════════════════════════════════════════════════════════════

_ATTENDANCE_PROMPT = _SYSTEM_BASE + """
Guided flows (ATTENDANCE module only):

1. attendance_by_trainee — attendance records of a specific trainee
Examples: "Mayank attendance", "Attendance of Mayank", "Show Mayank attendance"
Slots: trainee_name, course_name, date, date_range

2. attendance_percentage_by_trainee — attendance percentage of a trainee
Examples: "Mayank attendance percentage", "What is Mayank attendance percent?"
Slots: trainee_name, course_name, date_range

3. absent_trainees — list/count of absent trainees
Examples: "Who is absent today?", "Show absent trainees today", "How many absent today?"
Slots: date, course_name

4. present_trainees — list/count of present trainees
Examples: "Who is present today?", "Show present trainees today"
Slots: date, course_name

5. course_attendance_summary — course/batch wise attendance summary
Examples: "Course wise attendance summary", "Batch wise attendance summary"
Slots: course_name, date_range

6. low_attendance_trainees — trainees with attendance below threshold
Examples: "Show low attendance trainees", "Trainees below 75 attendance"
Slots: threshold, course_name

7. date_wise_attendance — attendance on a specific date
Examples: "Attendance on 2025-05-20", "Attendance today", "Date wise attendance"
Slots: date, course_name

8. trainee_absent_count — count of absent days for a trainee
Examples: "How many days Mayank was absent?", "Mayank absent count"
Slots: trainee_name, course_name

9. trainee_present_count — count of present days for a trainee
Examples: "How many days Mayank was present?", "Mayank present count"
Slots: trainee_name, course_name

10. batch_attendance_report — attendance report for a batch/course
Examples: "Attendance report for latest batch", "Show batch attendance report"
Slots: course_name, recent_filter (latest/current/ongoing)
""" + _RESPONSE_FORMAT


# ═══════════════════════════════════════════════════════════════════
# Dues module prompt (kept small, only 1 flow)
# ═══════════════════════════════════════════════════════════════════

_DUES_PROMPT = _SYSTEM_BASE + """
Guided flows (DUES module only):

1. pending_dues_by_person — dues of a person
Examples: "Mayank dues", "Pending dues of Mayank", "Show Mayank hostel dues"
Slots: trainee_name, dues_type (hostel/mess/library/ALL), year
""" + _RESPONSE_FORMAT


# ═══════════════════════════════════════════════════════════════════
# Course module prompt (10 flows)
# ═══════════════════════════════════════════════════════════════════

_COURSE_PROMPT = _SYSTEM_BASE + """
Guided flows (COURSE module only):

1. current_courses — currently running courses
Examples: "Which courses are running now?", "Show current courses"
Slots: status (current)

2. latest_course — the most recently started course
Examples: "What is the latest course?", "Latest batch"
Slots: recent_filter (latest)

3. upcoming_courses — future courses
Examples: "Show upcoming courses", "Future batches"
Slots: status (upcoming), month, year

4. completed_courses — finished courses
Examples: "Show completed courses", "Past courses"
Slots: status (completed), year

5. course_details_by_name — specific course details
Examples: "Show HR-LDCE course details", "Details of OS/S&W refresher"
Slots: course_name, recent_filter (latest/current/ongoing)

6. course_trainee_count — number of trainees in a specific course
Examples: "How many trainees in HR-LDCE?", "Student count in latest course"
Slots: course_name, recent_filter

7. course_wise_trainee_count — summary of trainees per course
Examples: "Course wise trainee count", "Batch wise student strength"
Slots: year, status

8. course_duration_summary — course start and end dates
Examples: "Course start and end dates", "Start date and end date of HR-LDCE"
Slots: course_name, recent_filter

9. batch_details — specific batch details
Examples: "Show latest batch details", "Batch details of HR-LDCE"
Slots: course_name, recent_filter

10. course_calendar_summary — month/year wise course calendar
Examples: "Course calendar summary", "Month wise courses"
Slots: year, month, status (current/upcoming/completed/all)
""" + _RESPONSE_FORMAT


# ═══════════════════════════════════════════════════════════════════
# Complaint module prompt (10 flows)
# ═══════════════════════════════════════════════════════════════════

_COMPLAINT_PROMPT = _SYSTEM_BASE + """
Guided flows (COMPLAINT module only):

1. pending_complaints — pending or open complaints
Examples: "Show pending complaints", "Open complaints"
Slots: complaint_category, complaint_status (pending)

2. resolved_complaints — completed or closed complaints
Examples: "Show resolved complaints", "Closed complaints"
Slots: complaint_category, complaint_status (resolved)

3. complaint_status_summary — summary of open vs closed
Examples: "Complaint status summary", "Open vs closed complaints"
Slots: complaint_category, year

4. complaints_by_category — complaints for specific category (hostel, electrical, etc.)
Examples: "Show hostel complaints", "Electrical complaints"
Slots: complaint_category, complaint_status

5. complaints_by_trainee — complaints raised by specific trainee
Examples: "Mayank complaints", "Complaints raised by Mayank"
Slots: trainee_name, complaint_status

6. complaint_details_by_id — details of a specific complaint id
Examples: "Show complaint 123 details", "Complaint id 123"
Slots: complaint_id

7. department_wise_complaints — complaint count by department
Examples: "Department wise complaints", "Which department has most complaints?"
Slots: complaint_status, year

8. recent_complaints — latest or recent complaints
Examples: "Show latest complaints", "Last 10 complaints"
Slots: limit, complaint_status

9. overdue_complaints — complaints pending for a long time
Examples: "Show overdue complaints", "Complaints older than 7 days"
Slots: days, complaint_category

10. complaint_count — total number of complaints
Examples: "How many complaints?", "Total hostel complaints"
Slots: complaint_category, complaint_status, year
""" + _RESPONSE_FORMAT


# ═══════════════════════════════════════════════════════════════════
# Timetable module prompt (10 flows)
# ═══════════════════════════════════════════════════════════════════

_TIMETABLE_PROMPT = _SYSTEM_BASE + """
Guided flows (TIMETABLE module only):

1. today_timetable — today's schedule/timetable
Examples: "Today timetable", "What lectures are today?"
Slots: course_id, course_name, date (today)

2. tomorrow_timetable — tomorrow's schedule/timetable
Examples: "Tomorrow timetable", "What lectures are tomorrow?"
Slots: course_id, course_name, date (tomorrow)

3. date_wise_timetable — timetable on a specific date
Examples: "Timetable on 2025-05-20", "Schedule on 2025-05-20"
Slots: date, course_id, course_name

4. course_timetable — full timetable for a specific course/batch
Examples: "Show timetable of HR-LDCE", "Latest batch timetable"
Slots: course_id, course_name, recent_filter

5. faculty_timetable — schedule of a specific faculty/teacher
Examples: "Show schedule of faculty Sharma", "What lectures does Sharma have today?"
Slots: faculty_name, user_id, date

6. subject_timetable — schedule of a specific subject
Examples: "When is Electrical subject scheduled?", "OS subject schedule"
Slots: subject_name, subject_id, date

7. classroom_timetable — schedule for a specific classroom
Examples: "Show classroom 101 timetable", "What is scheduled in room 101 today?"
Slots: classroom_name, classroom_id, date

8. session_timetable — timetable for a specific session
Examples: "Morning session timetable", "Show lectures in session 1"
Slots: session_name, session_id, date

9. timetable_summary — count or summary of lectures
Examples: "Timetable summary", "How many lectures today?", "Course wise lecture count today"
Slots: date, group_by

10. free_slots — availability of slots/classrooms
Examples: "Which slots are free today?", "Available classroom slots"
Slots: date, classroom_id, faculty_name
""" + _RESPONSE_FORMAT


# ═══════════════════════════════════════════════════════════════════
# Faculty / VL module prompt (10 flows)
# ═══════════════════════════════════════════════════════════════════

_FACULTY_PROMPT = _SYSTEM_BASE + """
Guided flows (FACULTY module only):

1. faculty_profile_by_name — faculty/VL profile details
Examples: "Show faculty Sharma details", "VL Sharma profile"
Slots: faculty_name, faculty_id, faculty_type

2. faculty_schedule — faculty timetable/schedule
Examples: "Faculty Sharma schedule", "What lectures does Sharma have today?"
Slots: faculty_name, faculty_id, date

3. faculty_courses — courses assigned to a faculty
Examples: "Which courses are assigned to Sharma?", "Sharma assigned courses"
Slots: faculty_name, faculty_id

4. faculty_subjects — subjects taught by a faculty
Examples: "Which subjects does Sharma teach?", "Subjects handled by Patel"
Slots: faculty_name, faculty_id

5. faculty_workload_summary — faculty-wise lecture count / ranking
Examples: "Faculty wise lecture count", "Who has most lectures?"
Slots: date, faculty_type

6. visiting_lecturers — list/count of visiting lecturers
Examples: "Show visiting lecturers", "How many VL?"
Slots: (none required)

7. faculty_feedback_summary — faculty feedback/rating
Examples: "Feedback of faculty Sharma", "Faculty rating"
Slots: faculty_name, faculty_id

8. faculty_by_subject — who teaches a subject
Examples: "Who teaches Electrical?", "Faculty for Electrical subject"
Slots: subject_name, subject_id

9. faculty_by_course — faculty assigned to a course
Examples: "Faculty assigned to HR-LDCE", "Teachers for latest batch"
Slots: course_name, course_id, recent_filter

10. faculty_availability — is faculty free/available
Examples: "Which faculty is free today?", "Is Sharma free today?"
Slots: faculty_name, date
""" + _RESPONSE_FORMAT


# ═══════════════════════════════════════════════════════════════════
# Module → prompt mapping
# ═══════════════════════════════════════════════════════════════════

_MODULE_PROMPTS = {
    "exam": _EXAM_PROMPT,
    "trainee": _TRAINEE_PROMPT,
    "hostel": _HOSTEL_PROMPT,
    "attendance": _ATTENDANCE_PROMPT,
    "dues": _DUES_PROMPT,
    "course": _COURSE_PROMPT,
    "complaint": _COMPLAINT_PROMPT,
    "timetable": _TIMETABLE_PROMPT,
    "faculty": _FACULTY_PROMPT,
}


# ═══════════════════════════════════════════════════════════════════
# Core parser
# ═══════════════════════════════════════════════════════════════════

def _parse_llm_response(response_text: str) -> Dict[str, Any]:
    """Clean and parse LLM JSON response."""
    text = response_text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    parsed = json.loads(text)

    # Handle smaller model quirks
    if "flow_id" in parsed and parsed["flow_id"]:
        if "matches_guided_flow" not in parsed:
            parsed["matches_guided_flow"] = True
        if "confidence" not in parsed:
            parsed["confidence"] = 1.0

    return parsed


def _parse_for_module(message: str, module: str) -> Dict[str, Any]:
    """Parse intent using a module-specific prompt."""
    default_fallback = {
        "matches_guided_flow": False,
        "flow_id": None,
        "confidence": 0,
        "slots": {},
        "reason": "Not a guided flow question"
    }

    prompt = _MODULE_PROMPTS.get(module)
    if not prompt:
        return default_fallback

    try:
        response_text = call_llm(
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": message}
            ],
            temperature=0,
            max_tokens=300
        )

        parsed = _parse_llm_response(response_text)
        print(f"[Intent Parser/{module}] Message: {message}")
        print(f"[Intent Parser/{module}] Parsed: {parsed}")

        confidence = parsed.get("confidence", 0)
        if not parsed.get("matches_guided_flow") or confidence < 0.70:
            return default_fallback

        return parsed
    except Exception as e:
        logger.error(f"[Intent Parser/{module}] Error: {e}")
        return default_fallback


# ═══════════════════════════════════════════════════════════════════
# Public API
# ═══════════════════════════════════════════════════════════════════

def parse_guided_intent(message: str, module_hint: Optional[str] = None) -> Dict[str, Any]:
    """Parse guided intent using module-specific prompts.

    Args:
        message:      The user question (ideally already spell-corrected).
        module_hint:  Module detected by the refiner (exam/trainee/hostel/attendance).
                      If provided, ONLY that module's prompt is used.
                      If None or 'unknown', tries all modules in order.

    Returns:
        Dict with matches_guided_flow, flow_id, confidence, slots, reason.
    """
    default_fallback = {
        "matches_guided_flow": False,
        "flow_id": None,
        "confidence": 0,
        "slots": {},
        "reason": "Not a guided flow question"
    }

    # If we know the module, use only that module's prompt (fast, focused)
    if module_hint and module_hint in _MODULE_PROMPTS:
        print(f"[Intent Parser] Using focused {module_hint} prompt")
        return _parse_for_module(message, module_hint)

    # If module is unknown, try each module in order until one matches
    print("[Intent Parser] Module unknown, trying all modules in order")
    for module in ["exam", "trainee", "hostel", "attendance", "dues"]:
        result = _parse_for_module(message, module)
        if result.get("matches_guided_flow") and result.get("confidence", 0) >= 0.70:
            print(f"[Intent Parser] Matched via {module} module")
            return result

    return default_fallback
