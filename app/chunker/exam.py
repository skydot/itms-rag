import logging
from app.services.db_service import get_connection
from app.chunker.utils import (
    table_exists,
    get_existing_columns,
    build_office_filter,
    limit_clause,
    make_chunk,
    safe_run,
    safe_text,
    pick_column
)

logger = logging.getLogger(__name__)

def get_exam_chunks(office_id: int | None = None, limit: int | None = None):
    chunks = []
    conn = get_connection()
    if not conn:
        logger.warning("[Chunker] No DB connection for module=exam")
        return chunks

    try:
        cursor = conn.cursor()
        module = "exam"

        if table_exists(cursor, "exam_marks"):
            cols = get_existing_columns(cursor, "exam_marks")
            where_office, params = build_office_filter(cols, alias="", office_id=office_id)
            sql = f"SELECT * FROM `exam_marks` WHERE 1=1 {where_office} {limit_clause(limit)}"
            rows = safe_run(cursor, sql, params)

            for row in rows:
                row_office = row.get("office_id") or office_id
                eid = row.get("id")
                
                # Result mapping: 1 = PASSED, 2 = FAILED, 0 = NOT APPEARED
                res_val = row.get("result")
                result_text = "UNKNOWN"
                if res_val == 1 or res_val == "1":
                    result_text = "PASSED"
                elif res_val == 2 or res_val == "2":
                    result_text = "FAILED"
                elif res_val == 0 or res_val == "0":
                    result_text = "NOT APPEARED"
                else:
                    result_text = safe_text(res_val)

                text = f"EXAM MARK RECORD\n"
                if "course_id" in row: text += f"Course ID: {safe_text(row.get('course_id'))}\n"
                if "trainee_id" in row: text += f"Trainee ID: {safe_text(row.get('trainee_id'))}\n"
                if "subject_id" in row: text += f"Subject ID: {safe_text(row.get('subject_id'))}\n"
                if "marks" in row: text += f"Marks: {safe_text(row.get('marks'))}\n"
                text += f"Result: {result_text}\n"

                chunks.append(make_chunk(
                    text=text,
                    module=module,
                    office_id=row_office,
                    allowed_roles=["principal", "admin", "training_staff", "trainer"],
                    entity_id=eid,
                    entity_type="exam_marks"
                ))
        else:
            logger.warning("[Chunker] table missing module=%s table=%s", module, "exam_marks")

        if table_exists(cursor, "exam_type"):
            cols = get_existing_columns(cursor, "exam_type")
            where_office, params = build_office_filter(cols, alias="", office_id=office_id)
            sql = f"SELECT * FROM `exam_type` WHERE 1=1 {where_office} {limit_clause(limit)}"
            rows = safe_run(cursor, sql, params)

            for row in rows:
                row_office = row.get("office_id") or office_id
                eid = row.get("id")
                name_col = pick_column(cols, ["name", "type_name", "exam_type_name"])
                
                text = f"EXAM TYPE RECORD\n"
                if name_col:
                    text += f"Name: {safe_text(row.get(name_col))}\n"

                chunks.append(make_chunk(
                    text=text,
                    module=module,
                    office_id=row_office,
                    allowed_roles=["principal", "admin", "training_staff", "trainer"],
                    entity_id=eid,
                    entity_type="exam_type"
                ))
        else:
            logger.warning("[Chunker] table missing module=%s table=%s", module, "exam_type")

        logger.info("[Chunker] module=%s office_id=%s chunks=%s", module, office_id, len(chunks))

    except Exception as e:
        logger.error(f"[Chunker] module=exam error: {e}")
    finally:
        conn.close()

    return chunks