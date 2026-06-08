import re
from typing import Optional, Dict

SEMINAR_FLOWS = {
    "upcoming_seminars": {"flow_id": "upcoming_seminars", "module": "seminar", "slots_order": ["department_id"], "requires_name": False},
    "seminar_details": {"flow_id": "seminar_details", "module": "seminar", "slots_order": ["seminar_id"], "requires_name": False},
    "seminar_topics": {"flow_id": "seminar_topics", "module": "seminar", "slots_order": ["seminar_id"], "requires_name": False},
    "seminar_by_faculty": {"flow_id": "seminar_by_faculty", "module": "seminar", "slots_order": ["faculty_id"], "requires_name": False},
    "seminar_by_subject": {"flow_id": "seminar_by_subject", "module": "seminar", "slots_order": ["subject_name"], "requires_name": False},
    "seminar_participants": {"flow_id": "seminar_participants", "module": "seminar", "slots_order": ["seminar_id"], "requires_name": False},
    "seminar_count": {"flow_id": "seminar_count", "module": "seminar", "slots_order": ["year", "month"], "requires_name": False},
    "recent_seminars": {"flow_id": "recent_seminars", "module": "seminar", "slots_order": ["limit"], "requires_name": False},
    "department_wise_seminars": {"flow_id": "department_wise_seminars", "module": "seminar", "slots_order": ["department_id"], "requires_name": False},
    "seminar_summary": {"flow_id": "seminar_summary", "module": "seminar", "slots_order": ["year"], "requires_name": False},
}

_SEMINAR_KEYWORDS = re.compile(r"\b(seminar|seminars|topics?)\b", re.I)

def normalize_seminar_message(message: str) -> str:
    text = message
    text = re.sub(r"\bseminr\b", "seminar", text, flags=re.I)
    return text

def detect_seminar_guided_flow(message: str) -> Optional[Dict]:
    text = normalize_seminar_message(message)
    lower = text.lower().strip()
    
    if not _SEMINAR_KEYWORDS.search(lower): return None
    if re.search(r"\b(meeting)\b", lower) and not re.search(r"\bseminar\b", lower): return None
    if re.search(r"\b(timetable|course|exam|attendance)\b", lower): return None
        
    slots = {"seminar_id": None, "seminar_title": None, "faculty_name": None, "faculty_id": None, "subject_name": None, "department_name": None, "department_id": None, "date": None, "year": None, "month": None, "limit": None}
    
    m_limit = re.search(r"\b(?:last|recent|top)\s+(\d+)\b", lower)
    if m_limit: slots["limit"] = int(m_limit.group(1))
    
    m_id = re.search(r"\bseminar\s*(?:id|no|number)?\s*(\d+)\b", lower)
    if m_id: slots["seminar_id"] = int(m_id.group(1))
    
    def _b(f, r): return {"flow_id": f, "module": "seminar", "slots": slots, "reason": r}
    
    if re.search(r"\b(how many|count|total)\b", lower): return _b("seminar_count", "count")
    if re.search(r"\btopics?\b", lower): return _b("seminar_topics", "topics")
    if re.search(r"\b(participant|attendee|who attended)\b", lower): return _b("seminar_participants", "participants")
    if re.search(r"\b(recent|latest|last)\b", lower): return _b("recent_seminars", "recent")
    if re.search(r"\b(upcoming|future|planned|scheduled)\b", lower): return _b("upcoming_seminars", "upcoming")
    if re.search(r"\b(department|dept)\b", lower): return _b("department_wise_seminars", "department")
    if re.search(r"\b(faculty|teacher|speaker)\b", lower) or slots["faculty_name"]: return _b("seminar_by_faculty", "faculty")
    if re.search(r"\bsubject\b", lower) or slots["subject_name"]: return _b("seminar_by_subject", "subject")
    if re.search(r"\b(summary|dashboard|report)\b", lower): return _b("seminar_summary", "summary")
    if slots["seminar_id"] or re.search(r"\b(detail|info|show)\b", lower): return _b("seminar_details", "details")
    
    if re.search(r"\bseminars?\b", lower): return _b("upcoming_seminars", "default")
    return None
