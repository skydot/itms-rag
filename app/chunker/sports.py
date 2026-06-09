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

def get_sports_chunks(office_id: int | None = None, limit: int | None = None):
    chunks = []
    conn = get_connection()
    if not conn:
        logger.warning("[Chunker] No DB connection for module=sports")
        return chunks

    try:
        cursor = conn.cursor()
        module = "sports"
        roles = ["principal", "admin", "sports_staff", "course_coordinator"]

        tables_to_check = [
            ("sport", "SPORTS EVENT RECORD"),
            ("sport_team", "SPORTS TEAM RECORD"),
            ("sport_item", "SPORTS ITEM RECORD"),
            ("sportitem_issue", "SPORTS ITEM ISSUE RECORD"),
            ("sport_material", "SPORTS MATERIAL RECORD"),
            ("srec_sport", "SPORTS PAYMENT/RECEIPT RECORD"),
            ("particpants", "SPORTS PARTICIPANT RECORD")
        ]

        for table_name, record_type in tables_to_check:
            if table_exists(cursor, table_name):
                cols = get_existing_columns(cursor, table_name)
                where_office, params = build_office_filter(cols, alias="", office_id=office_id)
                sql = f"SELECT * FROM `{table_name}` WHERE 1=1 {where_office} {limit_clause(limit)}"
                rows = safe_run(cursor, sql, params)

                for row in rows:
                    row_office = row.get("office_id") or office_id
                    eid = row.get("id")

                    text = f"{record_type}\n"
                    safe_fields = [
                        "program", "from_date", "to_date", "start_timing", "end_timing", "team", "team_name", "sport_item", "qty", "issue_date", "return_date", "fine", "item_price", "total_price", "payment_by", "receipt_no", "trainee", "status", "course_id", "user_id"
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
        logger.error(f"[Chunker] module=sports error: {e}")
    finally:
        conn.close()

    return chunks
