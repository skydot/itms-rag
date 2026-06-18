import logging
from typing import Dict, Any
from app.services.db_service import get_connection

logger = logging.getLogger(__name__)

# Basic fallback templates for standard modules
FALLBACK_TEMPLATES = {
    "complaint": {
        "list": "SELECT id, cm_no, description, created_at FROM complaints WHERE status = 1 AND office_id = %(office_id)s {filter_clause} ORDER BY created_at DESC LIMIT 50",
        "count": "SELECT COUNT(*) as total FROM complaints WHERE status = 1 AND office_id = %(office_id)s {filter_clause}"
    },
    "exam": {
        "list": "SELECT em.id, u.name, em.mark_obtained FROM exam_marks em JOIN users u ON u.id = em.user_id JOIN training_calendars tc ON tc.id = em.course_id JOIN courses c ON c.id = tc.ct_id WHERE c.office_id = %(office_id)s {filter_clause} LIMIT 50",
        "count": "SELECT COUNT(*) as total FROM exam_marks em JOIN training_calendars tc ON tc.id = em.course_id JOIN courses c ON c.id = tc.ct_id WHERE c.office_id = %(office_id)s {filter_clause}"
    },
    "hostel": {
        "list": "SELECT hm.id, u.name, hb.building_name, hr.room_no FROM hostel_masters hm JOIN users u ON u.id = hm.user_id JOIN hostel_buildings hb ON hb.id = hm.building_id JOIN hostel_rooms hr ON hr.id = hm.room_id WHERE hm.h_status = 1 AND hb.office_id = %(office_id)s {filter_clause} LIMIT 50",
        "count": "SELECT COUNT(*) as total FROM hostel_masters hm JOIN hostel_buildings hb ON hb.id = hm.building_id WHERE hm.h_status = 1 AND hb.office_id = %(office_id)s {filter_clause}"
    },
    "trainee": {
        "list": "SELECT tm.id, u.name, tm.created_at FROM tra_masters tm JOIN users u ON u.id = tm.user_id WHERE tm.status = 1 AND tm.office_id = %(office_id)s {filter_clause} LIMIT 50",
        "count": "SELECT COUNT(*) as total FROM tra_masters tm WHERE tm.status = 1 AND tm.office_id = %(office_id)s {filter_clause}"
    },
    "course": {
        "list": "SELECT c.id, c.course_name, c.cs_code FROM courses c WHERE c.status = 1 AND c.office_id = %(office_id)s {filter_clause} LIMIT 50",
        "count": "SELECT COUNT(*) as total FROM courses c WHERE c.status = 1 AND c.office_id = %(office_id)s {filter_clause}"
    },
    "attendance": {
        "list": "SELECT a.id, u.name, a.punch_time FROM attendances a JOIN users u ON u.id = a.user_id WHERE u.office_id = %(office_id)s {filter_clause} LIMIT 50",
        "count": "SELECT COUNT(*) as total FROM attendances a JOIN users u ON u.id = a.user_id WHERE u.office_id = %(office_id)s {filter_clause}"
    }
}

def build_and_execute_fallback(module: str, operation: str, filters: Dict[str, Any], office_id: int) -> dict:
    """
    Centralized, secure SQL Builder that consumes approved templates.
    Replaces LLM-generated raw SQL.
    """
    module = module.lower() if module else ""
    operation = operation.lower() if operation else "list"
    
    if module not in FALLBACK_TEMPLATES:
        return {"error": f"No fallback templates for module {module}", "rows": [], "row_count": 0}
        
    module_templates = FALLBACK_TEMPLATES[module]
    
    # Map operation to template
    template_key = "list"
    if "count" in operation or "total" in operation:
        template_key = "count"
        
    template = module_templates.get(template_key)
    if not template:
        return {"error": f"No fallback template for operation {operation}", "rows": [], "row_count": 0}
        
    # Build filter clauses safely
    filter_clauses = []
    params = {"office_id": office_id}
    
    # Simple direct equality filters
    for k, v in filters.items():
        if k and v and isinstance(k, str) and k.isalnum():
            # Very basic generic filtering - in a real system this would need column mapping
            if k in ["status", "category_id", "building_id", "month", "year"]:
                # specific mappings would go here
                pass
    
    filter_str = " ".join(filter_clauses)
    sql = template.replace("{filter_clause}", filter_str)
    
    logger.info(f"[SQL BUILDER] Executing fallback template for {module}.{operation}: {sql}")
    
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
        return {
            "source": f"sql_builder_{module}",
            "sql": sql,
            "rows": rows,
            "row_count": len(rows),
        }
    except Exception as e:
        logger.error(f"[SQL BUILDER] Error executing template: {e}")
        return {"error": str(e), "rows": [], "row_count": 0}
    finally:
        conn.close()
