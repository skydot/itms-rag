import re
from typing import Optional, Dict

MEETING_FLOWS = {
    "upcoming_meetings": {"flow_id": "upcoming_meetings", "module": "meeting", "slots_order": ["department_name", "department_id"], "requires_name": False},
    "today_meetings": {"flow_id": "today_meetings", "module": "meeting", "slots_order": [], "requires_name": False},
    "meeting_details_by_id": {"flow_id": "meeting_details_by_id", "module": "meeting", "slots_order": ["meeting_id"], "requires_name": False},
    "meeting_agenda": {"flow_id": "meeting_agenda", "module": "meeting", "slots_order": ["meeting_id"], "requires_name": False},
    "meeting_by_department": {"flow_id": "meeting_by_department", "module": "meeting", "slots_order": ["department_name", "department_id"], "requires_name": False},
    "meeting_participants": {"flow_id": "meeting_participants", "module": "meeting", "slots_order": ["meeting_id"], "requires_name": False},
    "past_meetings": {"flow_id": "past_meetings", "module": "meeting", "slots_order": ["year", "month"], "requires_name": False},
    "meeting_count": {"flow_id": "meeting_count", "module": "meeting", "slots_order": ["year", "month", "department_id"], "requires_name": False},
    "recent_meetings": {"flow_id": "recent_meetings", "module": "meeting", "slots_order": ["limit"], "requires_name": False},
    "meeting_calendar_summary": {"flow_id": "meeting_calendar_summary", "module": "meeting", "slots_order": ["year", "month"], "requires_name": False},
}

_MEETING_KEYWORDS = re.compile(r"\b(meeting|meetings|meet|agenda|chairman|invitee)\b", re.I)

def normalize_meeting_message(message: str) -> str:
    text = message
    text = re.sub(r"\bmeting\b", "meeting", text, flags=re.I)
    text = re.sub(r"\bmeating\b", "meeting", text, flags=re.I)
    return text

def detect_meeting_guided_flow(message: str) -> Optional[Dict]:
    text = normalize_meeting_message(message)
    lower = text.lower().strip()
    
    if not _MEETING_KEYWORDS.search(lower):
        return None
        
    if re.search(r"\b(timetable|complaint|seminar|course|attendance|exam)\b", lower) and not re.search(r"\b(meeting)\b", lower):
        return None
        
    slots = {"meeting_id": None, "meeting_title": None, "department_name": None, "department_id": None, "date": None, "year": None, "month": None, "limit": None}
    
    m_limit = re.search(r"\b(?:last|recent|top)\s+(\d+)\b", lower)
    if m_limit: slots["limit"] = int(m_limit.group(1))
    
    if re.search(r"\btoday\b", lower): slots["date"] = "today"
    
    m_id = re.search(r"\bmeeting\s*(?:id|no|number)?\s*(\d+)\b", lower)
    if m_id: slots["meeting_id"] = int(m_id.group(1))
    
    def _b(f, r): return {"flow_id": f, "module": "meeting", "slots": slots, "reason": r}
    
    if re.search(r"\b(how many|count|total)\b", lower): return _b("meeting_count", "count")
    if re.search(r"\bagenda\b", lower): return _b("meeting_agenda", "agenda")
    if re.search(r"\b(participant|attendee|who attended|invitee)\b", lower): return _b("meeting_participants", "participants")
    if re.search(r"\b(today|today'?s)\b", lower): return _b("today_meetings", "today")
    if re.search(r"\b(recent|latest|last)\b", lower): return _b("recent_meetings", "recent")
    if re.search(r"\b(past|completed|history)\b", lower): return _b("past_meetings", "past")
    if re.search(r"\b(upcoming|future|planned|scheduled)\b", lower): return _b("upcoming_meetings", "upcoming")
    if re.search(r"\b(department|dept)\b", lower): return _b("meeting_by_department", "department")
    if re.search(r"\b(summary|dashboard|calendar)\b", lower): return _b("meeting_calendar_summary", "summary")
    if slots["meeting_id"] or re.search(r"\b(detail|info|show)\b", lower): return _b("meeting_details_by_id", "details")
    
    if re.search(r"\bmeetings?\b", lower): return _b("upcoming_meetings", "default")
    return None
