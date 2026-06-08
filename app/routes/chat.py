from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from collections import deque

from app.services.access_policy import (
    describe_access,
    describe_restricted_access,
    has_module_access,
    normalize_role,
)
from app.services.llm_service import classify_query, format_answer, generate_answer, refine_question, try_direct_answer
from app.services.smart_query_service import get_relevant_templates, execute_smart_query
from app.services.embedder import get_embedding
from app.services.qdrant_service import search_data_filtered
from app.services.sql_fallback_service import (
    run_exam_sql_fallback, run_trainee_sql_fallback, run_hostel_sql_fallback, run_course_sql_fallback,
    run_attendance_sql_fallback, run_timetable_sql_fallback, run_faculty_vl_sql_fallback,
    run_feedback_sql_fallback, run_complaint_sql_fallback, run_library_sql_fallback,
    run_mess_sql_fallback, run_vehicle_sql_fallback, run_meeting_sql_fallback,
    run_seminar_sql_fallback, run_inspection_sql_fallback, run_sports_sql_fallback,
    run_pass_eq_sql_fallback, run_field_study_tour_sql_fallback, run_master_admin_sql_fallback
)
from app.services.response_mode_service import detect_response_mode
from app.services.report_service import generate_report, get_report_ttl
from app.services.action_intent_service import detect_action_intent
from app.services.action_field_extractor import extract_action_fields
from app.services.action_confirmation_service import create_confirmation
from app.services.action_permission_service import can_execute_action

router = APIRouter()

# Conversation history store: keyed by office_id, stores last 2 exchanges
# Each exchange = {"question": str, "answer": str}
conversation_history: dict[int, deque] = {}

# Keywords to detect data questions (exam, hostel, trainee, course topics)
DATA_KEYWORDS = {
    "exam", "marks", "mark", "result", "pass", "passed", "fail", "failed",
    "score", "scores", "subject", "subjects", "grade", "grades",
    "hostel", "room", "warden", "bed", "allocation",
    "trainee", "trainees", "student", "students",
    "traine", "trianee", "trainne", "taines", "trainnes", "studens", "studnts",
    "attendance", "present", "absent", "leave",
    "top", "highest", "lowest", "average", "total", "count", "performance",
    "performer", "percentage", "occupancy", "complaint", "schedule",
    "joined", "joining", "course", "courses", "department", "designation",
    "nominee", "calendar", "re-exam", "reexam", "test", "paper", "topper", "toppers",
    "building", "overcrowded", "vacant", "available", "empty", "unused",
    "male", "female", "ladies", "gender",
    "compare", "comparison", "vs", "versus", "improvement",
    "how many", "who", "which", "list", "show", "what", "detail", "details",
    "name", "email", "phone", "contact",
    "batch", "batches", "program", "promotion", "refresher", "initial",
}

ACCESS_KEYWORDS = {"access", "permission", "permissions", "allowed", "role"}

# Keywords to detect exam-specific questions (for SQL fallback routing)
EXAM_KEYWORDS = {
    "exam", "marks", "mark", "result", "results", "pass", "passed", "fail", "failed",
    "score", "scores", "subject", "subjects", "grade", "grades", "percentage",
    "performer", "performers", "performance",
    "re-exam", "reexam", "re exam", "schedule", "test", "paper", "topper", "toppers",
    # Trainee/student words (including common typos)
    "trainee", "trainees", "student", "students",
    "traine", "trianee", "trainne", "taines", "trainnes", "studens", "studnts",
}

# Combined patterns: if BOTH sides match, treat as exam question
_EXAM_COMBINED_PATTERNS = [
    # (any of group A) + (any of group B) → exam
    ({"subject", "subjects"}, {"fail", "failed", "pass", "passed", "mark", "marks", "result", "score"}),
    ({"marks", "mark", "result", "results"}, {"trainee", "trainees", "student", "students", "taines", "trainne", "trianee"}),
    ({"fail", "failed", "pass", "passed"}, {"trainee", "trainees", "student", "students", "taines", "trainne", "trianee", "count", "wise", "total"}),
    ({"subject", "subjects"}, {"wise", "count", "total", "average", "highest", "lowest"}),
]

# Keywords to detect trainee-specific questions
TRAINEE_KEYWORDS = {
    "trainee", "trainees", "student", "students", "participant", "participants",
    "learner", "learners", "candidate", "candidates",
    # Common typos
    "traine", "trianee", "trainne", "taines", "trainnes", "studens", "studnts",
    # Trainee-related actions/concepts
    "joined", "joining", "admission", "approved", "pending approval",
    "enrollment", "enrolled", "nomination", "nominee", "nominees",
    "certificate", "linen", "field training",
    "course wise trainee", "batch trainee", "gender wise trainee",
    "zone wise trainee", "division wise trainee",
}

# Keywords to detect hostel-specific questions
HOSTEL_KEYWORDS = {
    "hostel", "room", "rooms", "bed", "beds", "building", "buildings",
    "occupancy", "occupied", "available room", "available bed",
    "checkin", "check-in", "checkout", "check-out",
    "stay", "staying", "allotment", "alloted", "allotted",
    "mess", "hostel complaint", "room complaint", "dues",
    "overstay", "overcrowded", "vacant",
    # Common typos
    "hostal", "hostle", "rom",
}

# Hostel-only words (not shared with other modules) for disambiguation
_HOSTEL_ONLY_WORDS = {
    "hostel", "hostal", "hostle", "room", "rooms", "rom",
    "bed", "beds", "building", "buildings",
    "occupancy", "occupied", "checkin", "check-in", "checkout", "check-out",
    "allotment", "alloted", "allotted", "overstay", "overcrowded",
    "vacant", "mess", "staying",
}

# Trainee-only words for disambiguation (not exam or hostel)
_TRAINEE_ONLY_WORDS = {
    "trainee", "trainees", "taines", "trainne", "trianee", "traine", "trainnes",
    "student", "students", "studens", "studnts",
    "participant", "participants", "learner", "learners",
    "candidate", "candidates",
    "joined", "joining", "admission", "enrolled", "enrollment",
    "nomination", "nominee", "nominees", "certificate", "linen",
}

# Keywords to detect attendance-specific questions
ATTENDANCE_KEYWORDS = {
    "attendance", "present", "absent", "punch", "biometric", "punch time",
    "who is present", "who is absent", "attendance count", "attendance percentage"
}

# Keywords to detect timetable-specific questions
TIMETABLE_KEYWORDS = {
    "timetable", "time table", "lecture", "schedule", "session", "class room",
    "topic", "today's lecture", "tomorrow's lecture", "weekly schedule"
}

# Keywords to detect faculty/VL-specific questions
FACULTY_VL_KEYWORDS = {
    "faculty", "visiting lecturer", "vl", "lecturer", "speaker", "guest faculty"
}

# Keywords to detect feedback-specific questions
FEEDBACK_KEYWORDS = {
    "feedback", "rating", "review", "response", "question feedback", "course feedback"
}

# Keywords to detect complaint-specific questions
COMPLAINT_KEYWORDS = {
    "complaint", "complain", "pending complaint", "closed complaint", "category complaint",
    "grievance", "issue ticket"
}

# Keywords to detect library-specific questions
LIBRARY_KEYWORDS = {
    "library", "book", "books", "issue book", "return book", "fine", "overdue"
}

# Keywords to detect mess-specific questions
MESS_KEYWORDS = {
    "mess", "bill", "receipt", "dues", "food", "meal", "item price", "material",
    "mess bill", "mess receipt", "pending dues"
}

# Keywords to detect vehicle-specific questions
VEHICLE_KEYWORDS = {
    "vehicle", "bus", "driver", "trip", "booking", "km", "kilometer", "pnr", "travel"
}

# Keywords to detect meeting-specific questions
MEETING_KEYWORDS = {
    "meeting", "agenda", "mom", "minutes", "chairman", "invitee", "schedule meeting"
}

# Keywords to detect seminar-specific questions
SEMINAR_KEYWORDS = {
    "seminar", "speaker", "judge", "seminar topic", "presentation"
}

# Keywords to detect inspection-specific questions
INSPECTION_KEYWORDS = {
    "inspection", "inspection note", "inspection description", "audit"
}

# Keywords to detect sports-specific questions
SPORTS_KEYWORDS = {
    "sport", "sports", "team", "participant", "sport item", "game", "tournament"
}

# Keywords to detect pass/EQ-specific questions
PASS_EQ_KEYWORDS = {
    "pass", "privilege pass", "eq", "railway pass", "ticket", "pnr", "train class"
}

# Keywords to detect field study tour-specific questions
FIELD_STUDY_TOUR_KEYWORDS = {
    "field training", "study tour", "tour", "outdoor training", "filled training"
}

# Keywords to detect master admin-specific questions
MASTER_ADMIN_KEYWORDS = {
    "user", "role", "permission", "department", "designation", "grade", "service",
    "zone", "division", "depot", "station", "bank", "company", "holiday", "place"
}

# Keywords to detect course-specific questions
COURSE_KEYWORDS = {
    "course", "courses",
    "training course", "training",
    "batch", "batches",
    "course group", "course for",
    "department wise course", "category wise course",
    "promotion course", "refresher course", "initial course",
    "ongoing course", "upcoming course", "completed course", "running course",
    "recent course", "latest course", "current course",  # Critical: course batch timing
    "recent batch", "latest batch", "current batch",      # Critical: course batch timing
    "course duration", "course code",
    "certificate course", "online exam course",
    "hostel facility course", "mess facility course", "library facility course",
    "seat capacity", "program",
    # Common typos
    "coures", "cors", "traning", "trainig",
}

# Course-only words for disambiguation
_COURSE_ONLY_WORDS = {
    "course", "courses", "coures", "cors",
    "batch", "batches",
    "program",
    "course group", "course for",
    "promotion", "refresher", "initial",
    "seat capacity",
}


def _is_exam_question(message: str) -> bool:
    """Check if the question is related to the Exam module."""
    text = message.lower()

    # 1. Direct keyword match
    exam_specific = {
        "exam", "marks", "mark", "result", "results", "score", "scores",
        "subject", "subjects", "grade", "grades", "percentage",
        "pass", "passed", "fail", "failed", "performance",
        "performer", "performers", "re-exam", "reexam", "re exam", "paper",
        "topper", "toppers",
    }
    if any(kw in text for kw in exam_specific):
        print(f"[Chat] Is exam question: True (keyword match)")
        return True

    # 2. Combined pattern match
    for group_a, group_b in _EXAM_COMBINED_PATTERNS:
        if any(w in text for w in group_a) and any(w in text for w in group_b):
            print(f"[Chat] Is exam question: True (combined pattern match)")
            return True

    return False


def _is_trainee_question(message: str) -> bool:
    """Check if the question is related to the Trainee module.
    
    Excludes questions that are actually about recent/latest course batches
    which should go to Course module.
    """
    text = message.lower()
    
    # If question is about "recent course", "latest course", "current course"
    # it should go to Course module, NOT Trainee module
    course_batch_indicators = {
        "recent course", "latest course", "current course",
        "recent batch", "latest batch", "current batch"
    }
    if any(ind in text for ind in course_batch_indicators):
        print(f"[Chat] Is trainee question: False (course batch indicator found)")
        return False

    # Direct keyword match
    if any(kw in text for kw in TRAINEE_KEYWORDS):
        print(f"[Chat] Is trainee question: True (keyword match)")
        return True

    return False


def _is_hostel_question(message: str) -> bool:
    """Check if the question is related to the Hostel module."""
    text = message.lower()

    # Direct keyword match
    if any(kw in text for kw in HOSTEL_KEYWORDS):
        print(f"[Chat] Is hostel question: True (keyword match)")
        return True

    return False


def _is_course_question(message: str) -> bool:
    """Check if the question is related to the Course module.
    
    Priority logic:
    - If message includes exam/marks/result keywords -> NOT course (prefer exam)
    - If message includes trainee/student + NOT course-specific -> NOT course (prefer trainee)
    - If message includes hostel/room/bed -> NOT course (prefer hostel)
    - Otherwise if course/batch/program keywords -> YES course
    """
    text = message.lower()

    # If clearly an exam question, don't treat as course
    exam_indicators = {"exam", "marks", "mark", "result", "pass", "fail", "score", "subject", "grade", "percentage"}
    if any(kw in text for kw in exam_indicators):
        return False

    # If clearly feedback or complaint question, don't treat as course
    feedback_complaint_indicators = {"feedback", "rating", "review", "complaint", "complain", "grievance"}
    if any(kw in text for kw in feedback_complaint_indicators):
        return False

    # If clearly a trainee question (trainee-specific words), don't treat as course
    if any(kw in text for kw in _TRAINEE_ONLY_WORDS):
        # Unless it also has strong course indicators
        course_indicators = {"course", "batch", "program"}
        if not any(kw in text for kw in course_indicators):
            return False

    # If clearly a hostel question, don't treat as course
    if any(kw in text for kw in _HOSTEL_ONLY_WORDS):
        return False

    # Direct keyword match for course
    if any(kw in text for kw in COURSE_KEYWORDS):
        print(f"[Chat] Is course question: True (keyword match)")
        return True

    return False


def _is_attendance_question(message: str) -> bool:
    """Check if the question is related to the Attendance module."""
    text = message.lower()
    if any(kw in text for kw in ATTENDANCE_KEYWORDS):
        print(f"[Chat] Is attendance question: True (keyword match)")
        return True
    return False


def _is_timetable_question(message: str) -> bool:
    """Check if the question is related to the Timetable module."""
    text = message.lower()
    if any(kw in text for kw in TIMETABLE_KEYWORDS):
        print(f"[Chat] Is timetable question: True (keyword match)")
        return True
    return False


def _is_faculty_vl_question(message: str) -> bool:
    """Check if the question is related to the Faculty/VL module."""
    text = message.lower()
    if any(kw in text for kw in FACULTY_VL_KEYWORDS):
        print(f"[Chat] Is faculty_vl question: True (keyword match)")
        return True
    return False


def _is_feedback_question(message: str) -> bool:
    """Check if the question is related to the Feedback module."""
    text = message.lower()
    if any(kw in text for kw in FEEDBACK_KEYWORDS):
        print(f"[Chat] Is feedback question: True (keyword match)")
        return True
    return False


def _is_complaint_question(message: str) -> bool:
    """Check if the question is related to the Complaint module."""
    text = message.lower()
    if any(kw in text for kw in COMPLAINT_KEYWORDS):
        print(f"[Chat] Is complaint question: True (keyword match)")
        return True
    return False


def _is_library_question(message: str) -> bool:
    """Check if the question is related to the Library module."""
    text = message.lower()
    if any(kw in text for kw in LIBRARY_KEYWORDS):
        print(f"[Chat] Is library question: True (keyword match)")
        return True
    return False


def _is_mess_question(message: str) -> bool:
    """Check if the question is related to the Mess module."""
    text = message.lower()
    if any(kw in text for kw in MESS_KEYWORDS):
        print(f"[Chat] Is mess question: True (keyword match)")
        return True
    return False


def _is_vehicle_question(message: str) -> bool:
    """Check if the question is related to the Vehicle module."""
    text = message.lower()
    if any(kw in text for kw in VEHICLE_KEYWORDS):
        print(f"[Chat] Is vehicle question: True (keyword match)")
        return True
    return False


def _is_meeting_question(message: str) -> bool:
    """Check if the question is related to the Meeting module."""
    text = message.lower()
    if any(kw in text for kw in MEETING_KEYWORDS):
        print(f"[Chat] Is meeting question: True (keyword match)")
        return True
    return False


def _is_seminar_question(message: str) -> bool:
    """Check if the question is related to the Seminar module."""
    text = message.lower()
    if any(kw in text for kw in SEMINAR_KEYWORDS):
        print(f"[Chat] Is seminar question: True (keyword match)")
        return True
    return False


def _is_inspection_question(message: str) -> bool:
    """Check if the question is related to the Inspection module."""
    text = message.lower()
    if any(kw in text for kw in INSPECTION_KEYWORDS):
        print(f"[Chat] Is inspection question: True (keyword match)")
        return True
    return False


def _is_sports_question(message: str) -> bool:
    """Check if the question is related to the Sports module."""
    text = message.lower()
    if any(kw in text for kw in SPORTS_KEYWORDS):
        print(f"[Chat] Is sports question: True (keyword match)")
        return True
    return False


def _is_pass_eq_question(message: str) -> bool:
    """Check if the question is related to the Pass/EQ module."""
    text = message.lower()
    if any(kw in text for kw in PASS_EQ_KEYWORDS):
        print(f"[Chat] Is pass_eq question: True (keyword match)")
        return True
    return False


def _is_field_study_tour_question(message: str) -> bool:
    """Check if the question is related to the Field Study Tour module."""
    text = message.lower()
    if any(kw in text for kw in FIELD_STUDY_TOUR_KEYWORDS):
        print(f"[Chat] Is field_study_tour question: True (keyword match)")
        return True
    return False


def _is_master_admin_question(message: str) -> bool:
    """Check if the question is related to the Master Admin module."""
    text = message.lower()
    if any(kw in text for kw in MASTER_ADMIN_KEYWORDS):
        print(f"[Chat] Is master_admin question: True (keyword match)")
        return True
    return False


# Sensitive/internal columns that should NEVER be exposed to users
_SENSITIVE_COLUMNS = {
    'id', 'user_id', 'trainee_id', 'tra_master_id', 'office_id', 'hostel_master_id',
    'application_id', 'exam_id', 'subject_id', 'course_id', 'ct_id', 'building_id',
    'room_id', 'complaint_id', 'feedback_id', 'schedule_id', 'template_id',
    'created_by', 'updated_by', 'password', 'hrms_id', 'aadhar', 'uan', 'pf_no',
    'bank_id', 'bank_acc', 'ifsc_code', 'android_id', 'permanent_identity',
    'pass_file', 'user_log', 'room_log', 'attachment', 'signature', 'photo',
    'emergency_numbers', 'office_mobile', 'emg_mobile_no', 'whatsapp_number',
    'present_address', 'permanent_address', 'resi_address', 'city', 'email', 'office_email'
}


def _format_fallback_rows(rows: list, max_rows: int = 15) -> str:
    """Convert SQL result rows (list of dicts) into a readable text context."""
    if not rows:
        return "No data found."
    
    # If it is a single row with a single column (usually a COUNT, SUM, AVG, etc.)
    if len(rows) == 1 and len(rows[0]) == 1:
        k = list(rows[0].keys())[0]
        v = rows[0][k]
        val = "N/A" if v is None else str(v)
        return f"{k}: {val}"

    limited = rows[:max_rows]
    lines = []
    for i, row in enumerate(limited, 1):
        # Filter out sensitive/internal columns and format nicely
        parts = []
        for k, v in row.items():
            if k.lower() not in _SENSITIVE_COLUMNS and v is not None and str(v).strip() != "":
                # Format the key nicely (snake_case -> Title Case)
                label = k.replace('_', ' ').title()
                parts.append(f"{label}: {str(v)}")
        if parts:
            lines.append(f"{i}. " + " | ".join(parts))
    summary = f"Total: {len(rows)} record(s)" + (f" (showing first {max_rows})" if len(rows) > max_rows else "")
    return summary + "\n" + "\n".join(lines)


def _build_report_response(
    report: dict,
    base_url: str,
    user_question: str,
    module_name: str = "data"
) -> dict:
    """
    Build a response dict for report mode.
    
    Args:
        report: Report metadata from generate_report()
        base_url: Base URL for building full report URL
        user_question: Original user question
        module_name: Name of the module
        
    Returns:
        Dict with answer, report_url, row_count, response_mode
    """
    # Build full URL
    full_url = base_url.rstrip("/") + report["url"]
    
    # Calculate expiry time display
    ttl_seconds = report["ttl_seconds"]
    if ttl_seconds < 60:
        expiry_text = f"{ttl_seconds} seconds"
    elif ttl_seconds < 3600:
        ttl_minutes = ttl_seconds // 60
        expiry_text = f"{ttl_minutes} minute{'s' if ttl_minutes != 1 else ''}"
    else:
        ttl_hours = ttl_seconds // 3600
        expiry_text = f"{ttl_hours} hour{'s' if ttl_hours != 1 else ''}"
    
    # Build answer text with plain URL (frontend will auto-link)
    answer = (
        f"Found {report['row_count']} records for your request.\n\n"
        f"Open full report: {full_url}\n\n"
        f"This report link will expire in {expiry_text}."
    )
    
    return {
        "type": "text",
        "message": answer,
        "report_url": full_url,
        "row_count": report["row_count"],
        "response_mode": "report",
        "expires_at": report["expires_at"]
    }


class ChatRequest(BaseModel):
    message: str
    role: str = "principal"
    office_id: int = 1
    session_id: str = None  # Optional session ID for report grouping
    selected_option: dict = None  # For guided flow button clicks


def _is_procedural_question(message: str) -> bool:
    """Check if the question is asking about a process, procedure, rules, guidelines, or instructions."""
    text = message.lower()
    
    # 1. Phrases that strongly indicate procedural queries
    procedural_phrases = [
        "process of", "process for", "process to", "process about",
        "procedure of", "procedure for", "procedure to", "procedure about",
        "how to", "how do i", "how can i", "how we can",
        "step by step", "steps to", "steps for", "steps of",
        "guideline", "guidelines",
        "rulebook", "rule book", "rules for", "rules of",
        "policy for", "policy of", "policies of", "policies for",
        "disciplinary action", "discretionary quota",
        "instruction for", "instructions for", "instruction of", "instructions of",
        "what is the process", "what is process",
        "what is the procedure", "what is procedure"
    ]
    
    if any(phrase in text for phrase in procedural_phrases):
        return True
        
    # 2. Check if it's asking a "how" or "what" question about action verbs without asking for data records/counts
    if ("how" in text or "what" in text) and any(verb in text for verb in ["add", "create", "register", "allot", "assign", "enroll"]):
        if not any(data_kw in text for data_kw in ["how many", "list of", "records", "show", "count"]):
            return True
            
    return False


def _is_data_question(message: str) -> bool:
    """Check if the message is asking about data/analytics (exam, hostel, trainee)."""
    text = message.lower()
    return any(kw in text for kw in DATA_KEYWORDS)


def _is_access_question(message: str) -> bool:
    text = message.lower()
    return any(kw in text for kw in ACCESS_KEYWORDS)


def _check_module_access(message: str, user_role: str) -> str | None:
    """Returns an error message if user lacks access, or None if OK."""
    text = message.lower()
    exam_words = {"exam", "marks", "mark", "result", "pass", "fail", "score", "grade", "subject"}
    hostel_words = {"hostel", "room", "bed", "building", "warden", "allocation"}

    if any(w in text for w in exam_words) and not has_module_access(user_role, "exam"):
        return "You do not have permission to access exam data."
    if any(w in text for w in hostel_words) and not has_module_access(user_role, "hostel"):
        return "You do not have permission to access hostel data."
    return None


def _qdrant_fallback(question: str, office_id: int, user_role: str) -> str | None:
    """Search Qdrant for relevant context and generate an answer.
    Returns the answer string, or None if no relevant results found."""
    import re

    try:
        vector = get_embedding(question)
        results = search_data_filtered(
            vector=vector,
            office_id=office_id,
            user_role=user_role,
            limit=1000,
        )

        if not results:
            return None

        # Keyword-based reranking to solve Vector DB's exact-match flaw
        clean_q = re.sub(r"'s\b", "", question.lower())
        query_words = set(re.findall(r'\b\w{3,}\b', clean_q))

        def score_chunk(r):
            text = r.payload.get("text", "").lower()
            # Use word boundaries so "hey" doesn't match "Radhey"
            return sum(1 for w in query_words if re.search(r'\b' + re.escape(w) + r'\b', text))

        # Sort by keyword match score (descending), then original vector score
        results.sort(key=lambda r: (score_chunk(r), r.score), reverse=True)

        # Take only the top 5 most relevant chunks to prevent LLM context exhaustion (2048 tokens max)
        best_results = results[:5]

        # Check if top result is actually relevant (has keyword overlap)
        top_kw_score = score_chunk(best_results[0]) if best_results else 0
        top_vec_score = best_results[0].score if best_results else 0

        # If no keyword overlap AND low vector similarity, skip
        if top_kw_score == 0 and top_vec_score < 0.70:
            return None

        context = "\n".join([r.payload.get("text", "") for r in best_results])
        
        # Hard limit to ~1000 words to keep Qwen-1.5b safely under 2048 tokens
        if len(context) > 5000:
            context = context[:5000] + "..."
            
        return generate_answer(question, context)
    except Exception:
        return None


def _format_to_html(text: str) -> str:
    """Enforces HTML formatting for the frontend."""
    import re
    # If text already contains HTML table, preserve it as-is
    if '<table' in text.lower():
        return text
    # Convert markdown bold to HTML bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Convert markdown newlines/bullets to HTML breaks
    text = text.replace('\n- ', '<br><b>•</b> ')
    text = text.replace('\n', '<br>')
    # Fix double breaks
    text = text.replace('<br><br>', '<br>')
    return text

@router.post("/chat")
def chat(request: ChatRequest, http_request: Request = None):
    try:
        user_message = request.message.strip()
        # Prevent huge payloads from crashing the context window
        if len(user_message) > 500:
            user_message = user_message[:500]
            
        user_role = normalize_role(request.role)
        office_id = request.office_id
        session_id = request.session_id
        
        # Get base URL for building report links
        base_url = "http://localhost:8000"
        if http_request:
            base_url = str(http_request.base_url).rstrip("/")

        # Generate a unique history key if session_id is missing to prevent crossover
        hist_key = session_id if session_id else f"office_{office_id}_anon"

        # Get or create conversation history for this session
        if hist_key not in conversation_history:
            conversation_history[hist_key] = deque(maxlen=2)
        history = list(conversation_history[hist_key])

        # Helper to store exchange and return response
        def _respond(answer_text: str, extra_fields: dict = None) -> dict:
            conversation_history[hist_key].append({
                "question": user_message,
                "answer": answer_text
            })
            response = {"type": "text", "message": _format_to_html(answer_text)}
            if extra_fields:
                response.update(extra_fields)
            return response
        
        # Helper to process fallback results with report support
        def _process_fallback_result(fallback_result: dict, module_name: str) -> dict:
            """Process SQL fallback result, generating report if needed."""
            row_count = fallback_result.get("row_count", 0)
            rows = fallback_result.get("rows", [])
            
            if row_count == 0:
                return None  # No results
            
            # Detect response mode
            mode = detect_response_mode(
                user_question=user_message,
                result_type="list" if row_count > 1 else "single",
                row_count=row_count
            )
            
            print(f"[Chat] Response mode for {module_name}: {mode} (rows: {row_count})")
            
            if mode == "report" and row_count > 1:
                # Generate report
                report = generate_report(
                    module_name=module_name,
                    title=f"{module_name.title()} Report",
                    user_question=user_message,
                    rows=rows,
                    office_id=office_id,
                    session_id=session_id
                )
                return _build_report_response(report, base_url, user_message, module_name)
            else:
                # Return chat format - use LLM to format the response into a conversational sentence
                formatted_text = _format_fallback_rows(rows)
                # Pass the raw text to the LLM to generate a natural language response
                response_text = format_answer(user_message, formatted_text)
                return _respond(response_text)

        # --- Procedural / Process / Q&A queries (Bypass data/SQL pipeline) ---
        if not request.selected_option and _is_procedural_question(user_message):
            print(f"[Chat] Procedural/Process question detected: '{user_message}'. Bypassing SQL pipeline to Qdrant/RAG...")
            refined = refine_question(user_message)
            qdrant_answer = _qdrant_fallback(refined, office_id, user_role)
            if qdrant_answer:
                return _respond(qdrant_answer)
            return _respond(generate_answer(refined, ""))

        # --- Guided Flow (slot-filling with clickable buttons) ---
        from app.services.guided_flow_service import handle_guided_flow
        guided_result = handle_guided_flow(
            message=user_message,
            role=user_role,
            office_id=office_id,
            session_id=session_id or str(office_id),
            selected_option=request.selected_option,
            base_url=base_url,
        )
        if guided_result is not None:
            # Store in conversation history if it's a text response
            if guided_result.get("type") == "text" and "message" in guided_result:
                guided_result["message"] = _format_to_html(guided_result["message"])
                conversation_history[hist_key].append({
                    "question": user_message,
                    "answer": guided_result["message"]
                })
            return guided_result

        # --- Agentic Action Flow (LangChain) ---
        user_context = {"role": user_role, "office_id": office_id, "session_id": session_id}
        from app.services.langchain_agent_service import run_agentic_planner
        agent_result = run_agentic_planner(user_message, user_context)
        
        if agent_result.get("handled"):
            del agent_result["handled"]
            if agent_result.get("type") == "text" and "message" in agent_result:
                agent_result["message"] = _format_to_html(agent_result["message"])
                conversation_history[hist_key].append({
                    "question": user_message,
                    "answer": agent_result["message"]
                })
            return agent_result

        # --- Access questions (role/permission queries) ---
        if _is_access_question(user_message):
            lowered = user_message.lower()
            if "not access" in lowered or "cannot access" in lowered or "can't access" in lowered:
                return _respond(describe_restricted_access(user_role))
            return _respond(describe_access(user_role))

        # --- General / greeting questions (no data needed) ---
        if not _is_data_question(user_message):
            # Before giving up, check if this is a module question missed by DATA_KEYWORDS
            # (e.g. typo-heavy queries like "failed taines" or "hostal room")
            if _is_exam_question(user_message) or _is_trainee_question(user_message) or _is_hostel_question(user_message):
                print("[Chat] _is_data_question missed this but module detector caught it. Routing to data pipeline...")
                pass  # Fall through to data pipeline + fallback below
            else:
                # Check if this might be a follow-up answer (e.g. user just typed "Transportation")
                # If history exists and last answer was a follow-up question, treat as data question
                is_followup = False
                if history:
                    last_answer = history[-1].get("answer", "").lower()
                    followup_signals = ["which course", "which exam", "please specify", "please provide", "which trainee", "can you provide", "please select", "select one"]
                    if any(sig in last_answer for sig in followup_signals):
                        is_followup = True

                if not is_followup:
                    # ── LLM Gate: let the LLM decide if it can answer directly ──
                    # This catches greetings, identity questions, small talk, etc.
                    # without hardcoding patterns. If the LLM can answer, skip Qdrant entirely.
                    direct = try_direct_answer(user_message)
                    if direct:
                        return _respond(direct)

                    # LLM said NEEDS_DATA but DATA_KEYWORDS didn't match —
                    # try Qdrant as a last resort for procedural/document queries
                    qdrant_answer = _qdrant_fallback(user_message, office_id, user_role)
                    if qdrant_answer:
                        return _respond(qdrant_answer)
                    return _respond(generate_answer(user_message, ""))

        # --- Direct trainee selection handler (bypass AI) ---
        # If the previous answer was a TRAINEE_SELECT prompt and user clicked a name with Code
        if history:
            import re
            last_answer_raw = history[-1].get("answer", "")
            if "please select one" in last_answer_raw.lower():
                # Try to extract user_code first (e.g. "Alpa Mayank Talati (Code: U00939)" or just "U00939")
                code_match = re.search(r'\b([A-Z]\d{3,})\b', user_message.upper())
                if code_match:
                    user_code = code_match.group(1)
                    result = execute_smart_query("MARKS_OF_ONE_TRAINEE", {"user_code": user_code}, office_id)
                    if result and not result.startswith("Error"):
                        # If result contains HTML table, bypass format_answer to preserve it
                        if result.strip().startswith("<") and "<table" in result.lower():
                            return _respond(result)
                        formatted = format_answer(f"exam marks for trainee code {user_code}", result)
                        return _respond(formatted)
                # Fallback: try to extract numeric trainee_id
                id_match = re.search(r'\b(\d+)\b', user_message)
                if id_match:
                    trainee_id = int(id_match.group(1))
                    result = execute_smart_query("MARKS_OF_ONE_TRAINEE", {"trainee_id": trainee_id}, office_id)
                    if result and not result.startswith("Error"):
                        # If result contains HTML table, bypass format_answer to preserve it
                        if result.strip().startswith("<") and "<table" in result.lower():
                            return _respond(result)
                        formatted = format_answer(f"exam marks for trainee ID {trainee_id}", result)
                        return _respond(formatted)


        # --- Data question: 3-stage LLM pipeline ---

        # Access control check BEFORE calling LLM
        access_err = _check_module_access(user_message, user_role)
        if access_err:
            return {"type": "text", "message": access_err}

        # Stage 1: Refine question (spell correct + clarify)
        refined = refine_question(user_message)

        # Stage 2: Classify query + extract params (with conversation history)
        allowed_queries = get_relevant_templates(refined)
        route = classify_query(refined, allowed_query_ids=allowed_queries, history=history)
        qid = route.get("query_id")
        params = route.get("params") or {}

        if qid and qid != "NONE":
            print(f"[Chat] Trying predefined query...")
            print(f"[Chat] Predefined query found: {qid}")
            # Stage 2.5: Execute SQL
            result = execute_smart_query(qid, params, office_id)

            if result and not result.startswith("Error"):
                # Check if the result is a trainee selection prompt (multiple matches)
                if result.startswith("TRAINEE_SELECT\n"):
                    trainee_text = result.replace("TRAINEE_SELECT\n", "")
                    return _respond(trainee_text)

                # If result already contains HTML (like tables), skip LLM formatting to preserve it
                if result.strip().startswith("<") and "<table" in result.lower():
                    return _respond(result)

                # Check if this should be a report (list-type queries with multiple rows)
                # User asked for "list" and result has many lines -> generate report
                result_lines = [l for l in result.strip().split('\n') if l.strip()]
                is_list_query = "list" in user_message.lower() or "show" in user_message.lower()
                has_many_results = len(result_lines) > 3
                
                if is_list_query and has_many_results and detect_response_mode(user_message, result_type="list", row_count=len(result_lines)) == "report":
                    # Convert formatted text lines to structured rows for report
                    rows = []
                    for line in result_lines:
                        if '|' in line:
                            # Parse structured lines like "ID:10971 | GEETANJALEE | Room 4"
                            parts = line.replace('• ', '').replace('- ', '').split('|')
                            row = {f"Column {i+1}": p.strip() for i, p in enumerate(parts)}
                            rows.append(row)
                        else:
                            rows.append({"Info": line.replace('• ', '').replace('- ', '').strip()})
                    
                    if rows:
                        module = qid.split('_')[0].lower() if '_' in qid else "data"
                        report = generate_report(
                            module_name=module,
                            title=f"Report",
                            user_question=user_message,
                            rows=rows,
                            office_id=office_id,
                            session_id=session_id
                        )
                        return _build_report_response(report, base_url, user_message, module)

                # Stage 3: LLM formats the answer
                formatted = format_answer(refined, result)

                # Only enrich with Qdrant for specific trainee profile queries where SQL data might be shallow
                if qid in ("HOSTEL_TRAINEE_DETAILS", "HOSTEL_SEARCH_TRAINEE_BY_NAME") and len(formatted) <= 80:
                    qdrant_answer = _qdrant_fallback(refined, office_id, user_role)
                    if qdrant_answer and len(qdrant_answer) > len(formatted):
                        return _respond(qdrant_answer)
                
                return _respond(formatted)

        # --- Module-specific SQL Fallback ---
        # Strategy: Try matched modules sequentially until results are found.
        print(f"[Chat] No predefined query found. Checking module fallback...")

        # 1. Exam SQL Fallback
        if _is_exam_question(user_message) or _is_exam_question(refined):
            print(f"[Chat] Trying Exam SQL fallback...")
            fallback = run_exam_sql_fallback(refined, office_id)
            if fallback.get("row_count", -1) >= 0:
                result = _process_fallback_result(fallback, "exam")
                if result:
                    return result
            elif fallback.get("error"):
                print(f"[Chat] Exam SQL fallback error: {fallback['error']}")

        # 2. Trainee SQL Fallback
        if _is_trainee_question(user_message) or _is_trainee_question(refined):
            print(f"[Chat] Trying Trainee SQL fallback...")
            fallback = run_trainee_sql_fallback(refined, office_id)
            if fallback.get("row_count", -1) >= 0:
                result = _process_fallback_result(fallback, "trainee")
                if result:
                    return result
            elif fallback.get("error"):
                print(f"[Chat] Trainee SQL fallback error: {fallback['error']}")

        # 3. Hostel SQL Fallback
        if _is_hostel_question(user_message) or _is_hostel_question(refined):
            print(f"[Chat] Trying Hostel SQL fallback...")
            fallback = run_hostel_sql_fallback(refined, office_id)
            if fallback.get("row_count", -1) >= 0:
                result = _process_fallback_result(fallback, "hostel")
                if result:
                    return result
            elif fallback.get("error"):
                print(f"[Chat] Hostel SQL fallback error: {fallback['error']}")

        # 4. Course SQL Fallback
        if _is_course_question(user_message) or _is_course_question(refined):
            print(f"[Chat] Trying Course SQL fallback...")
            fallback = run_course_sql_fallback(refined, office_id)
            if fallback.get("row_count", -1) >= 0:
                result = _process_fallback_result(fallback, "course")
                if result:
                    return result
            elif fallback.get("error"):
                print(f"[Chat] Course SQL fallback error: {fallback['error']}")

        # 5. Attendance SQL Fallback
        if _is_attendance_question(user_message) or _is_attendance_question(refined):
            print(f"[Chat] Trying Attendance SQL fallback...")
            fallback = run_attendance_sql_fallback(refined, office_id)
            if fallback.get("row_count", -1) >= 0:
                result = _process_fallback_result(fallback, "attendance")
                if result:
                    return result
            elif fallback.get("error"):
                print(f"[Chat] Attendance SQL fallback error: {fallback['error']}")

        # 6. Timetable SQL Fallback
        if _is_timetable_question(user_message) or _is_timetable_question(refined):
            print(f"[Chat] Trying Timetable SQL fallback...")
            fallback = run_timetable_sql_fallback(refined, office_id)
            if fallback.get("row_count", -1) >= 0:
                result = _process_fallback_result(fallback, "timetable")
                if result:
                    return result
            elif fallback.get("error"):
                print(f"[Chat] Timetable SQL fallback error: {fallback['error']}")

        # 7. Complaint SQL Fallback
        if _is_complaint_question(user_message) or _is_complaint_question(refined):
            print(f"[Chat] Trying Complaint SQL fallback...")
            fallback = run_complaint_sql_fallback(refined, office_id)
            if fallback.get("row_count", -1) >= 0:
                result = _process_fallback_result(fallback, "complaint")
                if result:
                    return result
            elif fallback.get("error"):
                print(f"[Chat] Complaint SQL fallback error: {fallback['error']}")

        # 8. Feedback SQL Fallback
        if _is_feedback_question(user_message) or _is_feedback_question(refined):
            print(f"[Chat] Trying Feedback SQL fallback...")
            fallback = run_feedback_sql_fallback(refined, office_id)
            if fallback.get("row_count", -1) >= 0:
                result = _process_fallback_result(fallback, "feedback")
                if result:
                    return result
            elif fallback.get("error"):
                print(f"[Chat] Feedback SQL fallback error: {fallback['error']}")

        # 9. Faculty VL SQL Fallback
        if _is_faculty_vl_question(user_message) or _is_faculty_vl_question(refined):
            print(f"[Chat] Trying Faculty VL SQL fallback...")
            fallback = run_faculty_vl_sql_fallback(refined, office_id)
            if fallback.get("row_count", -1) >= 0:
                result = _process_fallback_result(fallback, "faculty_vl")
                if result:
                    return result
            elif fallback.get("error"):
                print(f"[Chat] Faculty VL SQL fallback error: {fallback['error']}")

        # 10. Library SQL Fallback
        if _is_library_question(user_message) or _is_library_question(refined):
            print(f"[Chat] Trying Library SQL fallback...")
            fallback = run_library_sql_fallback(refined, office_id)
            if fallback.get("row_count", -1) >= 0:
                result = _process_fallback_result(fallback, "library")
                if result:
                    return result
            elif fallback.get("error"):
                print(f"[Chat] Library SQL fallback error: {fallback['error']}")

        # 11. Mess SQL Fallback
        if _is_mess_question(user_message) or _is_mess_question(refined):
            print(f"[Chat] Trying Mess SQL fallback...")
            fallback = run_mess_sql_fallback(refined, office_id)
            if fallback.get("row_count", -1) >= 0:
                result = _process_fallback_result(fallback, "mess")
                if result:
                    return result
            elif fallback.get("error"):
                print(f"[Chat] Mess SQL fallback error: {fallback['error']}")

        # 12. Vehicle SQL Fallback
        if _is_vehicle_question(user_message) or _is_vehicle_question(refined):
            print(f"[Chat] Trying Vehicle SQL fallback...")
            fallback = run_vehicle_sql_fallback(refined, office_id)
            if fallback.get("row_count", -1) >= 0:
                result = _process_fallback_result(fallback, "vehicle")
                if result:
                    return result
            elif fallback.get("error"):
                print(f"[Chat] Vehicle SQL fallback error: {fallback['error']}")

        # 13. Meeting SQL Fallback
        if _is_meeting_question(user_message) or _is_meeting_question(refined):
            print(f"[Chat] Trying Meeting SQL fallback...")
            fallback = run_meeting_sql_fallback(refined, office_id)
            if fallback.get("row_count", -1) >= 0:
                result = _process_fallback_result(fallback, "meeting")
                if result:
                    return result
            elif fallback.get("error"):
                print(f"[Chat] Meeting SQL fallback error: {fallback['error']}")

        # 14. Seminar SQL Fallback
        if _is_seminar_question(user_message) or _is_seminar_question(refined):
            print(f"[Chat] Trying Seminar SQL fallback...")
            fallback = run_seminar_sql_fallback(refined, office_id)
            if fallback.get("row_count", -1) >= 0:
                result = _process_fallback_result(fallback, "seminar")
                if result:
                    return result
            elif fallback.get("error"):
                print(f"[Chat] Seminar SQL fallback error: {fallback['error']}")

        # 15. Inspection SQL Fallback
        if _is_inspection_question(user_message) or _is_inspection_question(refined):
            print(f"[Chat] Trying Inspection SQL fallback...")
            fallback = run_inspection_sql_fallback(refined, office_id)
            if fallback.get("row_count", -1) >= 0:
                result = _process_fallback_result(fallback, "inspection")
                if result:
                    return result
            elif fallback.get("error"):
                print(f"[Chat] Inspection SQL fallback error: {fallback['error']}")

        # 16. Sports SQL Fallback
        if _is_sports_question(user_message) or _is_sports_question(refined):
            print(f"[Chat] Trying Sports SQL fallback...")
            fallback = run_sports_sql_fallback(refined, office_id)
            if fallback.get("row_count", -1) >= 0:
                result = _process_fallback_result(fallback, "sports")
                if result:
                    return result
            elif fallback.get("error"):
                print(f"[Chat] Sports SQL fallback error: {fallback['error']}")

        # 17. Pass EQ SQL Fallback
        if _is_pass_eq_question(user_message) or _is_pass_eq_question(refined):
            print(f"[Chat] Trying Pass EQ SQL fallback...")
            fallback = run_pass_eq_sql_fallback(refined, office_id)
            if fallback.get("row_count", -1) >= 0:
                result = _process_fallback_result(fallback, "pass_eq")
                if result:
                    return result
            elif fallback.get("error"):
                print(f"[Chat] Pass EQ SQL fallback error: {fallback['error']}")

        # 18. Field Study Tour SQL Fallback
        if _is_field_study_tour_question(user_message) or _is_field_study_tour_question(refined):
            print(f"[Chat] Trying Field Study Tour SQL fallback...")
            fallback = run_field_study_tour_sql_fallback(refined, office_id)
            if fallback.get("row_count", -1) >= 0:
                result = _process_fallback_result(fallback, "field_study_tour")
                if result:
                    return result
            elif fallback.get("error"):
                print(f"[Chat] Field Study Tour SQL fallback error: {fallback['error']}")

        # 19. Master Admin SQL Fallback
        if _is_master_admin_question(user_message) or _is_master_admin_question(refined):
            print(f"[Chat] Trying Master Admin SQL fallback...")
            fallback = run_master_admin_sql_fallback(refined, office_id)
            if fallback.get("row_count", -1) >= 0:
                result = _process_fallback_result(fallback, "master_admin")
                if result:
                    return result
            elif fallback.get("error"):
                print(f"[Chat] Master Admin SQL fallback error: {fallback['error']}")

        # --- Fallback: Vector search (Qdrant) ---
        qdrant_answer = _qdrant_fallback(refined, office_id, user_role)
        if qdrant_answer:
            return _respond(qdrant_answer)

        # --- Final fallback: LLM with no context ---
        return _respond(generate_answer(refined, ""))

    except HTTPException as exc:
        return {"type": "text", "message": f"Error: {exc.detail if hasattr(exc, 'detail') else str(exc)}"}
    except Exception as exc:
        import traceback; traceback.print_exc(); return {"type": "text", "message": f"Error: {exc}"}