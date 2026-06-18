import json
from app.services.llm_service import call_llm


def _quick_classify(message: str) -> dict:
    """Ultra-lightweight LLM classifier — decides if a message is a TRMS data query.
    
    Uses a tiny prompt (~200 tokens) so even small models respond in 1-2 seconds.
    Returns {"is_data": bool, "module": str}.
    """
    prompt = f"""Classify this message. Is it asking to fetch/search TRMS database records (exams, trainees, hostel, attendance, courses, complaints, timetable, faculty, dues, library, mess, vehicle/transport, meeting, seminar, inspection, sports, pass/eq, field/study tour, master data/admin)?

Reply JSON only:
{{"is_data": true/false, "module": "exam|trainee|hostel|attendance|course|complaint|timetable|faculty|library|mess|vehicle|meeting|seminar|inspection|sports|pass_eq|field_study_tour|master_admin|unknown"}}

Rules for is_data=false:
- Greetings, small-talk, general chat
- Procedural "how to" questions (e.g. "how to add a trainee", "how to generate report")
- Software usage questions

Message: {message}"""

    try:
        content = call_llm(
            messages=[
                {"role": "system", "content": "Return JSON only. No explanation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=50
        )
        content = content.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(content)
        is_data = parsed.get("is_data", False)
        module = parsed.get("module", "unknown")
        print(f"[Quick Classify] Message: '{message}' -> is_data={is_data}, module={module}")
        return {"is_data": is_data, "module": module}
    except Exception as e:
        print(f"[Quick Classify] Error: {e}")
        # On error, assume it might be data — don't block real queries
        return {"is_data": True, "module": "unknown"}


def refine_guided_query(message: str) -> dict:
    """Two-stage classification + refinement.
    
    Stage 1: Quick classify (tiny prompt, ~1-2s) — is it a data query?
    Stage 2: Full refiner (big prompt, ~5-8s) — only if Stage 1 says yes.
    """
    # Stage 1: Quick classify
    classification = _quick_classify(message)
    
    if not classification.get("is_data"):
        # Not a data query — skip the heavy refiner entirely
        print(f"[Guided Refiner] Skipped (not a data query): '{message}'")
        return {
            "corrected_query": message,
            "module": "unknown",
            "flow_id": None,
            "confidence": 0.0,
            "slots": {},
            "reason": "Not a data query"
        }

    # Stage 2: Full refiner — only for actual data queries
    prompt = """You are a query refinement engine for TRMS AI chatbot.

Your job:
- Correct spelling mistakes.
- Normalize messy natural language.
- Detect module.
- Detect guided flow.
- Extract simple slots.
- Keep person names unchanged as much as possible.
- Do NOT answer the question.
- Do NOT generate SQL.
- Do NOT add facts.
- Return JSON only.

Supported modules:
exam, trainee, hostel, attendance, course, complaint, timetable, faculty, library, mess, vehicle, meeting, seminar, inspection, sports, pass_eq, field_study_tour, master_admin, unknown

Supported Exam flows:
- exam_marks_by_trainee
- exam_result_by_trainee
- failed_trainees
- failed_trainees_by_subject
- passed_trainees
- not_appeared_trainees
- top_performers
- lowest_performers
- subject_wise_marks_summary
- course_exam_summary
- re_exam_trainees
- pass_percentage

Supported Trainee flows:
- trainee_profile_by_name
- active_trainee_count
- trainee_joined_by_year
- recent_course_trainees
- course_wise_trainee_count
- batch_wise_trainee_count
- gender_wise_trainee_count
- approved_trainees
- pending_approval_trainees
- outstay_trainees

Supported Hostel flows:
- hostel_availability_occupency
- hostel_full_rooms
- hostel_room_by_trainee
- hostel_trainees_by_room
- hostel_trainees_by_building
- hostel_building_summary
- hostel_vacant_beds_by_building
- hostel_dues_by_trainee
- hostel_allocation_summary

Supported Attendance flows:
- attendance_by_trainee
- attendance_percentage_by_trainee
- absent_trainees
- present_trainees
- course_attendance_summary
- low_attendance_trainees
- date_wise_attendance
- trainee_absent_count
- trainee_present_count
- batch_attendance_report

Supported Course flows:
- current_courses
- latest_course
- upcoming_courses
- completed_courses
- course_details_by_name
- course_trainee_count
- course_wise_trainee_count
- course_duration_summary
- batch_details
- course_calendar_summary

Supported Complaint flows:
- pending_complaints
- resolved_complaints
- complaint_status_summary
- complaints_by_category
- complaints_by_trainee
- complaint_details_by_id
- department_wise_complaints
- recent_complaints
- overdue_complaints
- complaint_count

Supported Timetable flows:
- today_timetable
- tomorrow_timetable
- date_wise_timetable
- course_timetable
- faculty_timetable
- subject_timetable
- classroom_timetable
- session_timetable
- timetable_summary
- free_slots

Supported Faculty flows:
- faculty_profile_by_name
- faculty_schedule
- faculty_courses
- faculty_subjects
- faculty_workload_summary
- visiting_lecturers
- faculty_feedback_summary
- faculty_by_subject
- faculty_by_course
- faculty_availability

Supported Library flows:
- book_search
- book_availability

- issued_books_by_trainee
- overdue_books
- book_issue_history
- library_book_count
- book_type_summary
- most_issued_books
- recent_book_issues
- pending_book_returns

Supported Mess flows:
- mess_dues_by_trainee
- mess_bill_summary
- pending_mess_dues
- mess_receipts_by_trainee
- mess_item_summary
- mess_party_summary
- mess_refund_summary
- mess_material_stock
- mess_bill_count
- recent_mess_transactions
- mess_rate_card
- mess_item_rate

Supported Vehicle flows:
- vehicle_list
- vehicle_availability
- vehicle_usage_summary
- vehicle_register_history
- study_tour_vehicle_usage
- field_training_vehicle_usage
- vehicle_by_driver
- vehicle_count
- vehicle_maintenance
- recent_vehicle_activity

Supported Meeting flows:
- upcoming_meetings
- today_meetings
- meeting_details_by_id
- meeting_agenda
- meeting_by_department
- meeting_participants
- past_meetings
- meeting_count
- recent_meetings
- meeting_calendar_summary

Supported Seminar flows:
- upcoming_seminars
- seminar_details
- seminar_topics
- seminar_by_faculty
- seminar_by_subject
- seminar_participants
- seminar_count
- recent_seminars
- department_wise_seminars
- seminar_summary

Supported Inspection flows:
- inspection_notes
- inspection_details
- pending_inspections
- resolved_inspections
- inspection_by_department
- inspection_by_user
- inspection_summary
- inspection_count
- recent_inspections
- inspection_action_items

Supported Sports flows:
- sports_events
- sports_participants
- sports_team_details
- sports_item_stock
- sports_item_issues
- sports_material_summary
- sports_by_course
- sports_count
- recent_sports_activity
- sports_winners

Supported Pass/EQ flows:
- pass_by_trainee
- pending_passes
- issued_passes
- pass_type_summary
- eq_by_trainee
- pending_eqs
- train_class_summary
- station_wise_passes
- pass_count
- recent_pass_eq_activity

Supported Field/Study Tour flows:
- field_training_list
- field_training_by_course
- study_tour_list
- study_tour_by_course
- trainee_field_training
- trainee_study_tour
- field_training_attendance
- tour_vehicle_details
- field_study_summary
- recent_field_study_activity

Supported Master/Admin flows:
- department_list
- designation_list
- role_list
- user_role_summary
- railway_zone_list
- division_list
- station_list
- holiday_list
- company_info
- master_count_summary

Return JSON format only:

{
  "corrected_query": "",
  "module": "",
  "flow_id": "",
  "confidence": 0.0,
  "slots": {
    "trainee_name": null,
    "course_name": null,
    "subject_name": null,
    "exam_filter": null,
    "recent_filter": null,
    "complaint_id": null,
    "complaint_category": null,
    "complaint_status": null,
    "days": null,
    "date_range": null,
    "year": null,
    "faculty_name": null,
    "faculty_id": null,
    "subject_id": null,
    "classroom_name": null,
    "classroom_id": null,
    "session_name": null,
    "session_id": null,
    "group_by": null,
    "hostel_type": null,
    "building_name": null,
    "room_number": null,
    "date": null,
    "from_date": null,
    "to_date": null,
    "date_range": null,
    "threshold": null,
    "status": null,
    "limit": null,
    "year": null,
    "month": null,
    "faculty_type": null,
    "book_title": null,
    "book_id": null,
    "book_type": null,
    "item_name": null,
    "party_name": null,
    "dues_status": null,
    "vehicle_number": null,
    "vehicle_type": null,
    "driver_name": null,
    "meeting_id": null,
    "department_name": null,
    "department_id": null,
    "seminar_id": null,
    "inspection_id": null,
    "user_name": null,
    "user_id": null,
    "sport_id": null,
    "team_id": null,
    "pass_type": null,
    "train_class": null,
    "station_name": null,
    "tour_id": null,
    "field_training_id": null,
    "zone_id": null,
    "division_id": null,
    "entity_type": null
  },
  "reason": ""
}

If not sure:
{"corrected_query":"<cleaned>","module":"unknown","flow_id":null,"confidence":0.0,"slots":{},"reason":"Not sure"}

Examples:

Input: "available hostel rooms"
Output: {"corrected_query":"available hostel rooms","module":"hostel","flow_id":"hostel_availability_occupency","confidence":0.95,"slots":{},"reason":"User asks for available rooms in hostel"}

Input: "fully occupied hostel rooms"
Output: {"corrected_query":"fully occupied hostel rooms","module":"hostel","flow_id":"hostel_full_rooms","confidence":0.95,"slots":{},"reason":"User asks for fully occupied rooms in hostel"}

Input: "how many hostel we have?"
Output: {"corrected_query":"how many hostels do we have","module":"hostel","flow_id":"hostel_building_summary","confidence":0.95,"slots":{"building_id":"ALL"},"reason":"User asks for total hostel buildings"}

Input: "how many rooms in each hostel building"
Output: {"corrected_query":"how many rooms in each hostel building","module":"hostel","flow_id":"hostel_building_summary","confidence":0.95,"slots":{"building_id":"ALL"},"reason":"User asks for room count summary per building"}

Input: "mayank mark in recent exm?"
Output: {"corrected_query":"mayank marks in recent exam","module":"exam","flow_id":"exam_marks_by_trainee","confidence":0.95,"slots":{"trainee_name":"mayank","exam_filter":"recent"},"reason":"exam marks"}

Input: "show maynk detials"
Output: {"corrected_query":"show maynk details","module":"trainee","flow_id":"trainee_profile_by_name","confidence":0.9,"slots":{"trainee_name":"maynk"},"reason":"trainee profile"}

Input: "which rom mayank staying?"
Output: {"corrected_query":"which room mayank staying","module":"hostel","flow_id":"hostel_room_by_trainee","confidence":0.9,"slots":{"trainee_name":"mayank"},"reason":"User asks hostel room of trainee"}

Input: "mayank mess due?"
Output: {"corrected_query": "Mayank mess dues","module": "mess","flow_id": "mess_dues_by_trainee","confidence": 0.9,"slots": {"trainee_name": "mayank","dues_status": "pending"},"reason": "User asks pending mess dues of trainee"}

Input: "show pendng mess dues"
Output: {"corrected_query": "show pending mess dues","module": "mess","flow_id": "pending_mess_dues","confidence": 0.9,"slots": {"dues_status": "pending"},"reason": "User asks pending mess dues list"}

Input: "mess bill may 2025"
Output: {"corrected_query": "mess bill May 2025","module": "mess","flow_id": "mess_bill_summary","confidence": 0.9,"slots": {"month": "May","year": 2025},"reason": "User asks mess bill summary for month"}

Input: "rice consumption mess"
Output: {"corrected_query": "rice consumption in mess","module": "mess","flow_id": "mess_item_summary","confidence": 0.9,"slots": {"item_name": "rice"},"reason": "User asks item-wise mess material usage"}

Output: {"corrected_query":"which room is mayank staying in","module":"hostel","flow_id":"hostel_room_by_trainee","confidence":0.95,"slots":{"trainee_name":"mayank"},"reason":"hostel room"}

Input: "abhijeet attendence percentage?"
Output: {"corrected_query":"abhijeet attendance percentage","module":"attendance","flow_id":"attendance_percentage_by_trainee","confidence":0.95,"slots":{"trainee_name":"abhijeet"},"reason":"attendance percentage"}

Input: "pass percentage last year"
Output: {"corrected_query":"pass percentage last year","module":"exam","flow_id":"pass_percentage","confidence":0.95,"slots":{"date_range":"last year"},"reason":"pass percentage with date filter"}

Input: "failed trainees past 4 months"
Output: {"corrected_query":"failed trainees past 4 months","module":"exam","flow_id":"failed_trainees","confidence":0.95,"slots":{"date_range":"past 4 months"},"reason":"failed trainees with date filter"}

Input: "how many students not appeared in exam last year"
Output: {"corrected_query":"how many students not appeared in exam last year","module":"exam","flow_id":"not_appeared_trainees","confidence":0.95,"slots":{"date_range":"last year"},"reason":"not appeared with date filter"}

Input: "passed trainees in 2023"
Output: {"corrected_query":"passed trainees in 2023","module":"exam","flow_id":"passed_trainees","confidence":0.95,"slots":{"year":"2023"},"reason":"passed trainees with year filter"}

Input: "how many trainees joined last year"
Output: {"corrected_query":"how many trainees joined last year","module":"trainee","flow_id":"trainee_joined_by_year","confidence":0.95,"slots":{"date_range":"last year"},"reason":"trainees joined with date filter"}

Input: "which courses are running now?"
Output: {"corrected_query":"which courses are currently running","module":"course","flow_id":"current_courses","confidence":0.9,"slots":{"status":"current"},"reason":"current courses"}

Input: "show pending complents"
Output: {"corrected_query":"show pending complaints","module":"complaint","flow_id":"pending_complaints","confidence":0.9,"slots":{"complaint_status":"pending"},"reason":"pending complaints"}

Input: "todays timtable"
Output: {"corrected_query":"today timetable","module":"timetable","flow_id":"today_timetable","confidence":0.9,"slots":{"date":"today"},"reason":"today timetable"}

Input: "books issued to maynk"
Output: {"corrected_query":"books issued to Mayank","module":"library","flow_id":"issued_books_by_trainee","confidence":0.9,"slots":{"trainee_name":"mayank"},"reason":"User asks books issued to trainee"}

Input: "is python bok availble"
Output: {"corrected_query":"is Python book available","module":"library","flow_id":"book_availability","confidence":0.9,"slots":{"book_title":"python"},"reason":"User asks book availability"}

Input: "show overdu books"
Output: {"corrected_query":"show overdue books","module":"library","flow_id":"overdue_books","confidence":0.9,"slots":{},"reason":"User asks overdue books"}

Input: "top borrowed books"
Output: {"corrected_query":"top borrowed books","module":"library","flow_id":"most_issued_books","confidence":0.9,"slots":{"limit":10},"reason":"User asks most issued books"}

Input: "facalty sharma schedule today"
Output: {"corrected_query":"faculty sharma schedule today","module":"timetable","flow_id":"faculty_timetable","confidence":0.9,"slots":{"faculty_name":"sharma","date":"today"},"reason":"faculty timetable"}

Input: "how many lectures today"
Output: {"corrected_query":"how many lectures today","module":"timetable","flow_id":"timetable_summary","confidence":0.9,"slots":{"date":"today"},"reason":"lecture count"}

Input: "show facalty sharma details"
Output: {"corrected_query":"show faculty sharma details","module":"faculty","flow_id":"faculty_profile_by_name","confidence":0.9,"slots":{"faculty_name":"sharma"},"reason":"faculty profile"}

Input: "which courses are assigned to sharma"
Output: {"corrected_query":"which courses are assigned to sharma","module":"faculty","flow_id":"faculty_courses","confidence":0.9,"slots":{"faculty_name":"sharma"},"reason":"faculty courses"}

Input: "which subjects does sharma teach"
Output: {"corrected_query":"which subjects does sharma teach","module":"faculty","flow_id":"faculty_subjects","confidence":0.9,"slots":{"faculty_name":"sharma"},"reason":"faculty subjects"}

Input: "who teaches electrical"
Output: {"corrected_query":"who teaches electrical","module":"faculty","flow_id":"faculty_by_subject","confidence":0.9,"slots":{"subject_name":"electrical"},"reason":"faculty by subject"}

Input: "show vl list"
Output: {"corrected_query":"show VL list","module":"faculty","flow_id":"visiting_lecturers","confidence":0.9,"slots":{"faculty_type":"vl"},"reason":"visiting lecturers"}

Input: "show upcomming meeting"
Output: {"corrected_query": "show upcoming meetings", "module": "meeting", "flow_id": "upcoming_meetings", "confidence": 0.9, "slots": {}, "reason": "User asks upcoming meetings"}

Input: "show seminr topics"
Output: {"corrected_query": "show seminar topics", "module": "seminar", "flow_id": "seminar_topics", "confidence": 0.9, "slots": {}, "reason": "User asks seminar topics"}

Input: "inspection pending action"
Output: {"corrected_query": "inspection pending action items", "module": "inspection", "flow_id": "inspection_action_items", "confidence": 0.9, "slots": {}, "reason": "User asks pending inspection action items"}

Input: "sport item stock"
Output: {"corrected_query": "sports item stock", "module": "sports", "flow_id": "sports_item_stock", "confidence": 0.9, "slots": {}, "reason": "User asks sports item stock"}

Input: "mayank pass details"
Output: {"corrected_query": "Mayank railway pass details", "module": "pass_eq", "flow_id": "pass_by_trainee", "confidence": 0.9, "slots": {"trainee_name": "mayank"}, "reason": "User asks railway pass details of trainee"}

Input: "latest batch study tour"
Output: {"corrected_query": "latest batch study tour", "module": "field_study_tour", "flow_id": "study_tour_by_course", "confidence": 0.9, "slots": {"recent_filter": "latest"}, "reason": "User asks study tour of latest batch"}

Input: "show dept list"
Output: {"corrected_query": "show department list", "module": "master_admin", "flow_id": "department_list", "confidence": 0.9, "slots": {}, "reason": "User asks department master list"}

Important: Do not over-correct names. Keep person names mostly same.

User query:
""" + message

    try:
        content = call_llm(
            messages=[
                {"role": "system", "content": "Return strict JSON only. No markdown. No explanation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=200
        )
        content = content.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(content)
        
        # Enrich with pre-classifier's module if refiner returned unknown
        if parsed.get("module") == "unknown" and classification.get("module") != "unknown":
            parsed["module"] = classification["module"]
        
        # Add debug logs
        print("[Guided Refiner] Original:", message)
        print("[Guided Refiner] Corrected:", parsed.get("corrected_query"))
        print("[Guided Refiner] Module:", parsed.get("module"))
        print("[Guided Refiner] Flow:", parsed.get("flow_id"))
        print("[Guided Refiner] Confidence:", parsed.get("confidence"))
        print("[Guided Refiner] Slots:", parsed.get("slots"))
        
        return parsed
    except Exception as e:
        print(f"[Guided Refiner] Error: {e}")
        return {
            "corrected_query": message,
            "module": classification.get("module", "unknown"),
            "flow_id": None,
            "confidence": 0.0,
            "slots": {},
            "reason": "Error parsing LLM output"
        }
