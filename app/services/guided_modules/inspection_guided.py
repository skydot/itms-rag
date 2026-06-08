import re
from typing import Optional, Dict

INSPECTION_FLOWS = {
    "inspection_notes": {"flow_id": "inspection_notes", "module": "inspection", "slots_order": ["department_id"], "requires_name": False},
    "inspection_details": {"flow_id": "inspection_details", "module": "inspection", "slots_order": ["inspection_id"], "requires_name": False},
    "pending_inspections": {"flow_id": "pending_inspections", "module": "inspection", "slots_order": ["department_id"], "requires_name": False},
    "resolved_inspections": {"flow_id": "resolved_inspections", "module": "inspection", "slots_order": ["department_id"], "requires_name": False},
    "inspection_by_department": {"flow_id": "inspection_by_department", "module": "inspection", "slots_order": ["department_id"], "requires_name": False},
    "inspection_by_user": {"flow_id": "inspection_by_user", "module": "inspection", "slots_order": ["user_id"], "requires_name": False},
    "inspection_summary": {"flow_id": "inspection_summary", "module": "inspection", "slots_order": ["year"], "requires_name": False},
    "inspection_count": {"flow_id": "inspection_count", "module": "inspection", "slots_order": ["year"], "requires_name": False},
    "recent_inspections": {"flow_id": "recent_inspections", "module": "inspection", "slots_order": ["limit"], "requires_name": False},
    "inspection_action_items": {"flow_id": "inspection_action_items", "module": "inspection", "slots_order": ["department_id"], "requires_name": False},
}

_INSP_KEYWORDS = re.compile(r"\b(inspection|inspections|observations?|notes?)\b", re.I)

def normalize_inspection_message(message: str) -> str:
    text = message
    text = re.sub(r"\binspec\w*\b", "inspection", text, flags=re.I)
    return text

def detect_inspection_guided_flow(message: str) -> Optional[Dict]:
    text = normalize_inspection_message(message)
    lower = text.lower().strip()
    
    if not _INSP_KEYWORDS.search(lower): return None
    if re.search(r"\b(complaint|meeting|seminar|course|exam|attendance)\b", lower) and not re.search(r"\binspection\b", lower): return None
        
    slots = {"inspection_id": None, "department_name": None, "department_id": None, "user_name": None, "user_id": None, "date": None, "year": None, "month": None, "limit": None}
    
    m_limit = re.search(r"\b(?:last|recent|top)\s+(\d+)\b", lower)
    if m_limit: slots["limit"] = int(m_limit.group(1))
    
    m_id = re.search(r"\binspection\s*(?:id|note|no)?\s*(\d+)\b", lower)
    if m_id: slots["inspection_id"] = int(m_id.group(1))
    
    def _b(f, r): return {"flow_id": f, "module": "inspection", "slots": slots, "reason": r}
    
    if re.search(r"\b(how many|count|total)\b", lower): return _b("inspection_count", "count")
    if re.search(r"\b(recent|latest|last)\b", lower): return _b("recent_inspections", "recent")
    if re.search(r"\b(pending|open)\b", lower): return _b("pending_inspections", "pending")
    if re.search(r"\b(resolved|closed|completed)\b", lower): return _b("resolved_inspections", "resolved")
    if re.search(r"\b(action|points?)\b", lower): return _b("inspection_action_items", "action")
    if re.search(r"\b(department|dept)\b", lower): return _b("inspection_by_department", "department")
    if re.search(r"\b(by|created by)\b", lower): return _b("inspection_by_user", "user")
    if re.search(r"\b(summary|dashboard|report)\b", lower): return _b("inspection_summary", "summary")
    if slots["inspection_id"] or re.search(r"\b(detail|info|show)\b", lower): return _b("inspection_details", "details")
    
    if re.search(r"\b(notes?)\b", lower): return _b("inspection_notes", "notes")
    
    if re.search(r"\binspections?\b", lower): return _b("inspection_notes", "default")
    return None
