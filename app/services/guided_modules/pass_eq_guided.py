import re
from typing import Optional, Dict

PASS_EQ_FLOWS = {
    "pass_by_trainee": {"flow_id": "pass_by_trainee", "module": "pass_eq", "slots_order": ["trainee_name", "user_id"], "requires_name": True},
    "pending_passes": {"flow_id": "pending_passes", "module": "pass_eq", "slots_order": ["course_id"], "requires_name": False},
    "issued_passes": {"flow_id": "issued_passes", "module": "pass_eq", "slots_order": ["course_id"], "requires_name": False},
    "pass_type_summary": {"flow_id": "pass_type_summary", "module": "pass_eq", "slots_order": ["pass_type"], "requires_name": False},
    "eq_by_trainee": {"flow_id": "eq_by_trainee", "module": "pass_eq", "slots_order": ["trainee_name", "user_id"], "requires_name": True},
    "pending_eqs": {"flow_id": "pending_eqs", "module": "pass_eq", "slots_order": ["course_id"], "requires_name": False},
    "train_class_summary": {"flow_id": "train_class_summary", "module": "pass_eq", "slots_order": ["train_class"], "requires_name": False},
    "station_wise_passes": {"flow_id": "station_wise_passes", "module": "pass_eq", "slots_order": ["station_name"], "requires_name": False},
    "pass_count": {"flow_id": "pass_count", "module": "pass_eq", "slots_order": ["status"], "requires_name": False},
    "recent_pass_eq_activity": {"flow_id": "recent_pass_eq_activity", "module": "pass_eq", "slots_order": ["limit"], "requires_name": False},
}

_PASSEQ_KEYWORDS = re.compile(r"\b(pass|passes|eq|eqs|quota|station|railway|train)\b", re.I)

def normalize_pass_eq_message(message: str) -> str:
    return message

def detect_pass_eq_guided_flow(message: str) -> Optional[Dict]:
    text = normalize_pass_eq_message(message)
    lower = text.lower().strip()
    
    if not _PASSEQ_KEYWORDS.search(lower): return None
    # Negative guards for exam
    if re.search(r"\b(marks|result|exam|fail|grade)\b", lower): return None
        
    slots = {"trainee_name": None, "user_id": None, "course_name": None, "course_id": None, "pass_type": None, "train_class": None, "station_name": None, "station_id": None, "status": None, "limit": None}
    
    m_limit = re.search(r"\b(?:last|recent|top)\s+(\d+)\b", lower)
    if m_limit: slots["limit"] = int(m_limit.group(1))
    
    def _b(f, r): return {"flow_id": f, "module": "pass_eq", "slots": slots, "reason": r}
    
    if re.search(r"\b(how many|count|total)\b", lower): return _b("pass_count", "count")
    if re.search(r"\b(recent|latest|last)\b", lower): return _b("recent_pass_eq_activity", "recent")
    if re.search(r"\beq|quota\b", lower):
        if re.search(r"\bpending\b", lower): return _b("pending_eqs", "pending eq")
        return _b("eq_by_trainee", "eq trainee")
        
    if re.search(r"\b(pending)\b", lower): return _b("pending_passes", "pending pass")
    if re.search(r"\b(issued)\b", lower): return _b("issued_passes", "issued pass")
    if re.search(r"\b(type wise|type summary)\b", lower): return _b("pass_type_summary", "pass type")
    if re.search(r"\b(class wise|class summary|sleeper|ac)\b", lower): return _b("train_class_summary", "train class")
    if re.search(r"\b(station)\b", lower): return _b("station_wise_passes", "station")
    
    # Catch all for trainee pass
    if re.search(r"\b(pass|passes|train)\b", lower): return _b("pass_by_trainee", "trainee pass")
    
    return None
