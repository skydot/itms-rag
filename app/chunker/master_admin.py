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

def get_master_admin_chunks(office_id: int | None = None, limit: int | None = None):
    chunks = []
    conn = get_connection()
    if not conn:
        logger.warning("[Chunker] No DB connection for module=master_admin")
        return chunks

    try:
        cursor = conn.cursor()
        module = "master_admin"
        roles = ["principal", "admin"]

        tables_to_check = [
            ("departments", "DEPARTMENT MASTER RECORD"),
            ("designations", "DESIGNATION MASTER RECORD"),
            ("rail_zones", "RAILWAY ZONE MASTER RECORD"),
            ("divisions", "DIVISION MASTER RECORD"),
            ("rail_stations", "RAILWAY STATION MASTER RECORD"),
            ("services", "SERVICE MASTER RECORD"),
            ("grades", "GRADE MASTER RECORD"),
            ("pay_level", "PAY LEVEL MASTER RECORD"),
            ("holidays", "HOLIDAY MASTER RECORD"),
            ("states", "STATE MASTER RECORD"),
            ("places", "PLACE MASTER RECORD"),
            ("qualification", "QUALIFICATION MASTER RECORD"),
            ("sessions", "SESSION MASTER RECORD"),
            ("class_rooms", "CLASSROOM MASTER RECORD"),
            ("company", "COMPANY INFO RECORD"),
            ("site_info", "SITE INFO RECORD")
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
                    # Include standard master fields, avoiding passwords, tokens, API keys
                    safe_fields = [
                        "department_name", "desi_name", "zone_name", "division", "st_name", "service_name", "grade_name", "level_name", 
                        "holiday_name", "holiday_date", "state_name", "place_name", "qualification_name", "session_name", "class_room", 
                        "company_name", "site_name", "address", "city", "status", "sort_no"
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
        logger.error(f"[Chunker] module=master_admin error: {e}")
    finally:
        conn.close()

    return chunks
