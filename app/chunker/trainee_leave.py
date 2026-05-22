import logging
from app.services.db_service import get_connection

logger = logging.getLogger(__name__)


def get_trainee_leave_chunks():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                tl.id AS entity_id,
                u.name AS trainee_name,
                tl.office_id,
                tl.from_date,
                tl.to_date,
                tl.reason,
                tl.leave_approve AS status,
                tl.remarks_forward AS remarks
            FROM trainee_leave tl
            LEFT JOIN users u ON tl.user_id = u.id
            WHERE tl.office_id IS NOT NULL AND tl.user_id > 0
            LIMIT 200
        """)
        rows = cursor.fetchall()
        chunks = []
        for row in rows:
            name = row.get("trainee_name") or "Unknown trainee"
            from_date = row.get("from_date") or "N/A"
            to_date = row.get("to_date") or "N/A"
            reason = row.get("reason") or ""
            status = row.get("status") or 0
            remarks = row.get("remarks") or ""
            status_text = "Approved" if status == 1 else "Pending" if status == 0 else "Rejected"
            
            text = f"""Trainee: {name}
Leave From: {from_date}
Leave To: {to_date}
Status: {status_text}
Reason: {reason}
Remarks: {remarks}"""
            
            chunks.append({
                "text": text,
                "office_id": row.get("office_id"),
                "module": "trainee_leave",
                "allowed_roles": ["principal", "admin", "hr_staff", "trainer"],
                "entity_id": row.get("entity_id"),
                "entity_type": "trainee_leave",
                "trainee_name": name.lower()
            })
        conn.close()
        return chunks
    except Exception as e:
        logger.warning(f"Trainee leave sync skipped: {e}")
        return []
