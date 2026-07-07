"""
TRMS Redirect Service

Generates MakeMyTrip Myra-style deep links that redirect users from the chatbot 
to specific TRMS pages with their requested filters pre-filled.
"""

from typing import Dict, Optional, Any
from urllib.parse import urlencode

# Base URL for TRMS PHP Application
# Hardcoded to the production domain for testing
TRMS_BASE_URL = "http://trms.zrtiudaipur.in" 

# Mapping of Guided Flow IDs -> TRMS Pages and Parameters
REDIRECT_MAP = {
    # ── Hostel Flows ──
    "hostel_availability_occupency": {
        "page": "hostel_current_booking",
        "params": {
            "building_id": "building_id",
            "from_date": "from_date",
            "to_date": "to_date",
            "course_id": "course_id"
        }
    },
    "hostel_full_rooms": {
        "page": "hostel_current_booking",
        "params": { "building_id": "building_id" }
    },
    "hostel_trainees_by_building": {
        "page": "hostel_current_booking",
        "params": { "building_id": "building_id" }
    },
    "hostel_room_by_trainee": {
        "page": "hostel_current_booking",
        "params": { "user_id": "trainee_id" }
    },
    "hostel_vacant_beds_by_building": {
        "page": "hostel_current_booking",
        "params": { "building_id": "building_id" }
    },
    "hostel_building_summary": {
        "page": "hostel_current_booking",
        "params": { "building_id": "building_id" }
    },
    "hostel_allocation_summary": {
        "page": "hostel_current_booking",
        "params": {}
    },
    "hostel_past_booking": {
        "page": "hostel_booking_history",
        "params": {
            "building_id": "building_id",
            "from_date": "from_date",
            "to_date": "to_date",
            "course_id": "course_id",
            "year": "year"
        }
    },
    "hostel_daily_occupancy": {
        "page": "daily_position",
        "params": { "daily_date": "date" }
    },

    # ── Attendance Flows ──
    "attendance_by_trainee": {
        "page": "attendance",
        "params": { "course_id": "course_id", "dates": "date" }
    },
    "attendance_percentage_by_trainee": {
        "page": "attendance",
        "params": { "course_id": "course_id" }
    },
    "absent_trainees": {
        "page": "attendance",
        "params": { "course_id": "course_id" }
    },
    "present_trainees": {
        "page": "attendance",
        "params": { "course_id": "course_id" }
    },
    "course_attendance_summary": {
        "page": "attendance",
        "params": { "course_id": "course_id" }
    },
    "date_wise_attendance": {
        "page": "attendance",
        "params": { "course_id": "course_id", "dates": "date" }
    },
    "batch_attendance_report": {
        "page": "attendance",
        "params": { "course_id": "course_id" }
    },

    # ── Trainee Flows ──
    "trainees_by_course": {
        "page": "trainee_list",
        "params": { "course_id": "course_id" }
    },
    "trainee_profile_by_name": {
        "page": "trainee_list",
        "params": { "user_id": "user_id" }
    },
    "trainee_joined_by_year": {
        "page": "trainee_list",
        "params": { "year": "year" }
    },
    "all_trainees_list": {
        "page": "trainee_list",
        "params": {}
    },
    "approved_trainees": {
        "page": "trainee_list",
        "params": {}
    },
    "recent_course_trainees": {
        "page": "trainee_list",
        "params": {}
    },

    # ── Exam Flows ──
    "exam_marks_report": {
        "page": "exam_marks",
        "params": { "course_id": "course_id", "year": "year" }
    },
    "exam_failure_report": {
        "page": "exam_marks_failure",
        "params": { "course_id": "course_id", "year": "year" }
    },

    # ── Complaint Flows ──
    "pending_complaints": {
        "page": "complaint_register",
        "params": {
            "from_date": "from_date",
            "to_date": "to_date",
            "cm_status": "complaint_status"
        }
    },
    "resolved_complaints": {
        "page": "complaint_register",
        "params": {
            "from_date": "from_date",
            "to_date": "to_date",
            "cm_status": "complaint_status"
        }
    },
    "all_complaints": {
        "page": "complaint_register",
        "params": {
            "from_date": "from_date",
            "to_date": "to_date",
            "cm_status": "complaint_status"
        }
    },
    "recent_complaints": {
        "page": "complaint_register",
        "params": {}
    },
    "complaint_status_summary": {
        "page": "complaint_register",
        "params": {}
    },

    # ── Mess Flows ──
    "mess_bill_summary": {
        "page": "mess_bill_list",
        "params": {
            "course_id": "course_id",
            "from_date": "from_date",
            "to_date": "to_date"
        }
    },
    "mess_receipts_by_course": {
        "page": "mess_receipt_list",
        "params": { "course_id": "course_id" }
    },

    # ── Other General Flows ──
    "meeting_list": {
        "page": "meeting_list",
        "params": {
            "from_date": "from_date",
            "to_date": "to_date",
            "m_status": "meeting_status"
        }
    },
    "seminar_list": {
        "page": "seminar",
        "params": {
            "from_date": "from_date",
            "to_date": "to_date",
            "se_status": "seminar_status"
        }
    },
    "study_tour_list": {
        "page": "study_tour_list",
        "params": {
            "from_date": "from_date",
            "to_date": "to_date"
        }
    },
    "field_training_list": {
        "page": "field_training",
        "params": {
            "from_date": "from_date",
            "to_date": "to_date"
        }
    },
    "inspection_notes": {
        "page": "inspection_note_list",
        "params": {
            "from_date": "from_date",
            "to_date": "to_date"
        }
    },
    "book_search": {
        "page": "books",
        "params": {
            "title": "book_title",
            "author": "author"
        }
    },
    "book_issue_list": {
        "page": "book_issue_list",
        "params": {
            "from_date": "from_date",
            "to_date": "to_date"
        }
    },
    "vehicle_register": {
        "page": "vehicle_register",
        "params": {
            "from_date": "from_date",
            "to_date": "to_date"
        }
    },
    "pass_pto_list": {
        "page": "pass_pto_list",
        "params": {
            "from_date": "from_date",
            "to_date": "to_date"
        }
    },
    "no_dues_status": {
        "page": "all_dues",
        "params": {
            "course_id": "course_id",
            "year": "year"
        }
    },
    "daily_position": {
        "page": "daily_position",
        "params": {
            "daily_date": "daily_date"
        }
    }
}

def generate_redirect_url(flow_id: str, slots: Dict[str, Any]) -> Optional[str]:
    """
    Generates a deep-link URL for the TRMS PHP application based on the active flow and collected slots.
    Since the PHP app primarily uses POST -> Session for filters, this URL includes GET parameters 
    that the PHP side can intercept (or a JS snippet on the TRMS side can read) to auto-fill the form.
    """
    if flow_id not in REDIRECT_MAP:
        return None
        
    mapping = REDIRECT_MAP[flow_id]
    page = mapping["page"]
    param_map = mapping["params"]
    
    query_params = {}
    for php_param, slot_key in param_map.items():
        if slot_key in slots and slots[slot_key]:
            # Format dates to d-m-Y if they look like Y-m-d (basic heuristic)
            val = str(slots[slot_key])
            query_params[php_param] = val
            
    # Always include a flag so the PHP app knows this came from the chatbot
    query_params["_from_bot"] = "1"
    query_params["_auto_submit"] = "1"
    
    query_string = urlencode(query_params)
    return f"{TRMS_BASE_URL}/{page}?{query_string}"

def attach_redirect_metadata(guided_result: dict, flow_id: str, slots: dict):
    """
    Attaches the redirect URL and page name to the guided_result payload.
    """
    url = generate_redirect_url(flow_id, slots)
    if url:
        page_name = REDIRECT_MAP[flow_id]["page"].replace("_", " ").title()
        
        # Determine the button label based on the flow
        label = f"View in {page_name}"
        if "hostel" in flow_id:
            label = "Open Hostel Booking"
        elif "complaint" in flow_id:
            label = "View Complaint Register"
        elif "mess" in flow_id:
            label = "View Mess Bills"
        
        guided_result["redirect"] = {
            "url": url,
            "label": label
        }
    return guided_result
