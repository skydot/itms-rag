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

def get_pass_eq_chunks(office_id: int | None = None, limit: int | None = None):
    chunks = []
    conn = get_connection()
    if not conn:
        logger.warning("[Chunker] No DB connection for module=pass_eq")
        return chunks

    try:
        cursor = conn.cursor()
        module = "pass_eq"
        roles = ["principal", "admin", "pass_staff"]

        tables_to_check = [
            ("pass", "RAILWAY PASS RECORD"),
            ("pass_type", "PASS TYPE RECORD"),
            ("eqs", "EQ REQUEST RECORD"),
            ("train_class", "TRAIN CLASS RECORD")
        ]

        for table_name, record_type in tables_to_check:
            if table_exists(cursor, table_name):
                cols = get_existing_columns(cursor, table_name)
                # Many pass tables don't have office_id directly, they link to users. If office_id missing, we ingest for all.
                where_office, params = build_office_filter(cols, alias="", office_id=office_id)
                sql = f"SELECT * FROM `{table_name}` WHERE 1=1 {where_office} {limit_clause(limit)}"
                rows = safe_run(cursor, sql, params)

                for row in rows:
                    row_office = row.get("office_id") or office_id
                    eid = row.get("id")

                    text = f"{record_type}\n"
                    safe_fields = [
                        "pass_type", "out_from", "out_to", "out_via", "out_break", "return_from", "return_to", "user_id", "course_id", "journey_date", "dep_time", "train_no", "from_place", "to_place", "pnr", "tos", "train_class", "status"
                    ]
                    for col in safe_fields:
                        if col in row and row[col] is not None:
                            text += f"{col.replace('_', ' ').title()}: {safe_text(row[col])}\n"

                    chunks.append(make_chunk(
                        text=text,
                        module=module,
                        office_id=row_office,
                        allowed_roles=roles,
                        entity_id=eid,
                        entity_type=table_name
                    ))
            else:
                logger.warning("[Chunker] table missing module=%s table=%s", module, table_name)

        logger.info("[Chunker] module=%s office_id=%s chunks=%s", module, office_id, len(chunks))

    except Exception as e:
        logger.error(f"[Chunker] module=pass_eq error: {e}")
    finally:
        conn.close()

    return chunks
