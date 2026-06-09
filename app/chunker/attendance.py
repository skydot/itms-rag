import logging
from app.services.db_service import get_connection
from app.chunker.utils import (
    table_exists,
    get_existing_columns,
    build_office_filter,
    limit_clause,
    make_chunk,
    safe_run,
    safe_text
)

logger = logging.getLogger(__name__)

def get_attendance_chunks(office_id: int | None = None, limit: int | None = None):
    chunks = []
    conn = get_connection()
    if not conn:
        logger.warning("[Chunker] No DB connection for module=attendance")
        return chunks

    try:
        cursor = conn.cursor()
        module = "attendance"

        if table_exists(cursor, "attendances"):
            cols = get_existing_columns(cursor, "attendances")
            where_office, params = build_office_filter(cols, alias="", office_id=office_id)
            sql = f"SELECT * FROM `attendances` WHERE 1=1 {where_office} {limit_clause(limit)}"
            rows = safe_run(cursor, sql, params)

            for row in rows:
                row_office = row.get("office_id") or office_id
                eid = row.get("id")

                text = f"ATTENDANCE RECORD\n"
                for col in ["trainee_id", "course_id", "att_date", "punch_in", "punch_out", "status", "attendance_type", "remark"]:
                    if col in row and row[col] is not None:
                        text += f"{col.replace('_', ' ').title()}: {safe_text(row[col])}\n"

                chunks.append(make_chunk(
                    text=text,
                    module=module,
                    office_id=row_office,
                    allowed_roles=["principal", "admin", "training_staff", "trainer"],
                    entity_id=eid,
                    entity_type="attendances"
                ))
        else:
            logger.warning("[Chunker] table missing module=%s table=%s", module, "attendances")

        logger.info("[Chunker] module=%s office_id=%s chunks=%s", module, office_id, len(chunks))

    except Exception as e:
        logger.error(f"[Chunker] module=attendance error: {e}")
    finally:
        conn.close()

    return chunks
