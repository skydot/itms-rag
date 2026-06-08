import re
from typing import Optional, Dict

FIELD_STUDY_TOUR_FLOWS = {
    "field_training_list": {"flow_id": "field_training_list", "module": "field_study_tour", "slots_order": ["course_id"], "requires_name": False},
    "field_training_by_course": {"flow_id": "field_training_by_course", "module": "field_study_tour", "slots_order": ["course_id"], "requires_name": False},
    "study_tour_list": {"flow_id": "study_tour_list", "module": "field_study_tour", "slots_order": ["course_id"], "requires_name": False},
    "study_tour_by_course": {"flow_id": "study_tour_by_course", "module": "field_study_tour", "slots_order": ["course_id"], "requires_name": False},
    "trainee_field_training": {"flow_id": "trainee_field_training", "module": "field_study_tour", "slots_order": ["trainee_name", "user_id"], "requires_name": True},
    "trainee_study_tour": {"flow_id": "trainee_study_tour", "module": "field_study_tour", "slots_order": ["trainee_name", "user_id"], "requires_name": True},
    "field_training_attendance": {"flow_id": "field_training_attendance", "module": "field_study_tour", "slots_order": ["field_training_id"], "requires_name": False},
    "tour_vehicle_details": {"flow_id": "tour_vehicle_details", "module": "field_study_tour", "slots_order": ["tour_id"], "requires_name": False},
    "field_study_summary": {"flow_id": "field_study_summary", "module": "field_study_tour", "slots_order": ["year"], "requires_name": False},
    "recent_field_study_activity": {"flow_id": "recent_field_study_activity", "module": "field_study_tour", "slots_order": ["limit"], "requires_name": False},
}

_FST_KEYWORDS = re.compile(r"\b(field|study tour|tour)\b", re.I)

def normalize_field_study_tour_message(message: str) -> str:
    return message

def detect_field_study_tour_guided_flow(message: str) -> Optional[Dict]:
    text = normalize_field_study_tour_message(message)
    lower = text.lower().strip()
    
    if not _FST_KEYWORDS.search(lower): return None
    
    slots = {"course_id": None, "course_name": None, "trainee_name": None, "user_id": None, "date": None, "year": None, "tour_id": None, "field_training_id": None, "limit": None, "recent_filter": None}
    
    m_limit = re.search(r"\b(?:last|recent|top)\s+(\d+)\b", lower)
    if m_limit: slots["limit"] = int(m_limit.group(1))
    
    if re.search(r"\b(recent|latest)\b", lower): slots["recent_filter"] = "latest"
    
    def _b(f, r): return {"flow_id": f, "module": "field_study_tour", "slots": slots, "reason": r}
    
    if re.search(r"\b(vehicle|transport|bus|car)\b", lower) and re.search(r"\b(study tour|tour)\b", lower): return _b("tour_vehicle_details", "tour vehicle")
    if re.search(r"\b(summary|dashboard)\b", lower): return _b("field_study_summary", "summary")
    if re.search(r"\b(attendance|attended)\b", lower): return _b("field_training_attendance", "attendance")
    
    if re.search(r"\b(study tour|tour)\b", lower):
        if re.search(r"\b(course|batch)\b", lower) or slots["recent_filter"]: return _b("study_tour_by_course", "tour course")
        if re.search(r"\b(recent|last|latest)\b", lower): return _b("recent_field_study_activity", "recent")
        if re.search(r"\b(trainee|student)\b", lower): return _b("trainee_study_tour", "trainee tour")
        return _b("study_tour_list", "tour list")
        
    if re.search(r"\b(field training|field visit|field)\b", lower):
        if re.search(r"\b(course|batch)\b", lower) or slots["recent_filter"]: return _b("field_training_by_course", "field course")
        if re.search(r"\b(recent|last|latest)\b", lower): return _b("recent_field_study_activity", "recent")
        if re.search(r"\b(trainee|student)\b", lower): return _b("trainee_field_training", "trainee field")
        return _b("field_training_list", "field list")
        
    return None
