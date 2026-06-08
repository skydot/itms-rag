import re
from typing import Optional, Dict

MASTER_ADMIN_FLOWS = {
    "department_list": {"flow_id": "department_list", "module": "master_admin", "slots_order": [], "requires_name": False},
    "designation_list": {"flow_id": "designation_list", "module": "master_admin", "slots_order": ["department_id"], "requires_name": False},
    "role_list": {"flow_id": "role_list", "module": "master_admin", "slots_order": [], "requires_name": False},
    "user_role_summary": {"flow_id": "user_role_summary", "module": "master_admin", "slots_order": ["role_id"], "requires_name": False},
    "railway_zone_list": {"flow_id": "railway_zone_list", "module": "master_admin", "slots_order": [], "requires_name": False},
    "division_list": {"flow_id": "division_list", "module": "master_admin", "slots_order": ["zone_id"], "requires_name": False},
    "station_list": {"flow_id": "station_list", "module": "master_admin", "slots_order": ["division_id"], "requires_name": False},
    "holiday_list": {"flow_id": "holiday_list", "module": "master_admin", "slots_order": ["year"], "requires_name": False},
    "company_info": {"flow_id": "company_info", "module": "master_admin", "slots_order": [], "requires_name": False},
    "master_count_summary": {"flow_id": "master_count_summary", "module": "master_admin", "slots_order": ["entity_type"], "requires_name": False},
}

_MASTER_KEYWORDS = re.compile(r"\b(department|designation|role|zone|division|station|holiday|company|master data|admin|organization)\b", re.I)

def normalize_master_admin_message(message: str) -> str:
    return message

def detect_master_admin_guided_flow(message: str) -> Optional[Dict]:
    text = normalize_master_admin_message(message)
    lower = text.lower().strip()
    
    if not _MASTER_KEYWORDS.search(lower): return None
    
    # Negative guards for trainee profile
    if re.search(r"\b(trainee|student|details of|profile)\b", lower): return None
        
    slots = {"department_name": None, "department_id": None, "role_name": None, "role_id": None, "zone_name": None, "zone_id": None, "division_name": None, "division_id": None, "year": None, "entity_type": None}
    
    def _b(f, r): return {"flow_id": f, "module": "master_admin", "slots": slots, "reason": r}
    
    if re.search(r"\b(company|organization|site info)\b", lower): return _b("company_info", "company")
    if re.search(r"\b(count summary|how many)\b", lower): return _b("master_count_summary", "count")
    if re.search(r"\b(holiday)\b", lower): return _b("holiday_list", "holiday")
    if re.search(r"\b(station)\b", lower): return _b("station_list", "station")
    if re.search(r"\b(division)\b", lower): return _b("division_list", "division")
    if re.search(r"\b(zone)\b", lower): return _b("railway_zone_list", "zone")
    if re.search(r"\b(role summary)\b", lower): return _b("user_role_summary", "role summary")
    if re.search(r"\b(role|roles)\b", lower): return _b("role_list", "role")
    if re.search(r"\b(designation)\b", lower): return _b("designation_list", "designation")
    if re.search(r"\b(department|dept)\b", lower): return _b("department_list", "department")
    
    return None
