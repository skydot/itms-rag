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

def get_course_nominee_chunks(office_id: int | None = None, limit: int | None = None):
    chunks = []
    conn = get_connection()
    if not conn:
        logger.warning("[Chunker] No DB connection for module=course_nominee")
        return chunks

    try:
        cursor = conn.cursor()
        module = "course_nominee"

        # Check for both possible table names
        table_to_use = None
        if table_exists(cursor, "tra_masters_nominee"):
            table_to_use = "tra_masters_nominee"
        elif table_exists(cursor, "courses_nominee"):
            table_to_use = "courses_nominee"

        if table_to_use:
            cols = get_existing_columns(cursor, table_to_use)
            where_office, params = build_office_filter(cols, alias="", office_id=office_id)
            sql = f"SELECT * FROM `{table_to_use}` WHERE 1=1 {where_office} {limit_clause(limit)}"
            rows = safe_run(cursor, sql, params)

            for row in rows:
                row_office = row.get("office_id") or office_id
                eid = row.get("id")

                text = f"COURSE NOMINEE RECORD\n"
                safe_fields = ["nominee", "trainee_id", "course_id", "ct_id", "tc_id", "created_at", "status", "approved_by"]
                for col in safe_fields:
                    if col in row and row[col] is not None:
                        text += f"{col.replace('_', ' ').title()}: {safe_text(row[col])}\n"

                chunks.append(make_chunk(
                    text=text,
                    module=module,
                    office_id=row_office,
                    allowed_roles=["principal", "admin", "training_staff", "trainer", "course_coordinator"],
                    entity_id=eid,
                    entity_type=table_to_use
                ))
        else:
            logger.warning("[Chunker] table missing module=%s tables=tra_masters_nominee/courses_nominee", module)

        logger.info("[Chunker] module=%s office_id=%s chunks=%s", module, office_id, len(chunks))

    except Exception as e:
        logger.error(f"[Chunker] module=course_nominee error: {e}")
    finally:
        conn.close()

    return chunks
