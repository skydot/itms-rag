import re
from typing import Optional, Dict

SPORTS_FLOWS = {
    "sports_events": {"flow_id": "sports_events", "module": "sports", "slots_order": ["sport_id"], "requires_name": False},
    "sports_participants": {"flow_id": "sports_participants", "module": "sports", "slots_order": ["sport_id"], "requires_name": False},
    "sports_team_details": {"flow_id": "sports_team_details", "module": "sports", "slots_order": ["team_id"], "requires_name": False},
    "sports_item_stock": {"flow_id": "sports_item_stock", "module": "sports", "slots_order": ["item_id"], "requires_name": False},
    "sports_item_issues": {"flow_id": "sports_item_issues", "module": "sports", "slots_order": ["user_id"], "requires_name": False},
    "sports_material_summary": {"flow_id": "sports_material_summary", "module": "sports", "slots_order": ["item_id"], "requires_name": False},
    "sports_by_course": {"flow_id": "sports_by_course", "module": "sports", "slots_order": ["course_id"], "requires_name": False},
    "sports_count": {"flow_id": "sports_count", "module": "sports", "slots_order": ["count_type"], "requires_name": False},
    "recent_sports_activity": {"flow_id": "recent_sports_activity", "module": "sports", "slots_order": ["limit"], "requires_name": False},
    "sports_winners": {"flow_id": "sports_winners", "module": "sports", "slots_order": ["sport_id"], "requires_name": False},
}

_SPORTS_KEYWORDS = re.compile(r"\b(sports?|games?|cricket|volleyball|football|badminton|bat|ball|team|winner)\b", re.I)

def normalize_sports_message(message: str) -> str:
    return message

def detect_sports_guided_flow(message: str) -> Optional[Dict]:
    text = normalize_sports_message(message)
    lower = text.lower().strip()
    
    if not _SPORTS_KEYWORDS.search(lower): return None
    if re.search(r"\b(exam|attendance|faculty)\b", lower) and not re.search(r"\bsport\b", lower): return None
        
    slots = {"sport_id": None, "sport_name": None, "team_id": None, "item_name": None, "item_id": None, "user_id": None, "trainee_name": None, "course_name": None, "course_id": None, "count_type": None, "limit": None}
    
    m_limit = re.search(r"\b(?:last|recent|top)\s+(\d+)\b", lower)
    if m_limit: slots["limit"] = int(m_limit.group(1))
    
    def _b(f, r): return {"flow_id": f, "module": "sports", "slots": slots, "reason": r}
    
    if re.search(r"\b(how many|count|total)\b", lower): return _b("sports_count", "count")
    if re.search(r"\b(recent|latest|last)\b", lower): return _b("recent_sports_activity", "recent")
    if re.search(r"\b(winner)\b", lower): return _b("sports_winners", "winner")
    if re.search(r"\b(participant|who participated|played)\b", lower): return _b("sports_participants", "participants")
    if re.search(r"\b(team)\b", lower): return _b("sports_team_details", "team")
    if re.search(r"\b(stock|available|inventory)\b", lower): return _b("sports_item_stock", "stock")
    if re.search(r"\b(issue|issued)\b", lower): return _b("sports_item_issues", "issue")
    if re.search(r"\b(material|summary)\b", lower): return _b("sports_material_summary", "material")
    if re.search(r"\b(course|batch)\b", lower): return _b("sports_by_course", "course")
    if re.search(r"\b(detail|info|event)\b", lower): return _b("sports_events", "events")
    
    if re.search(r"\bsports?\b", lower): return _b("sports_events", "default")
    return None
