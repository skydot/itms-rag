import logging

logger = logging.getLogger(__name__)


def safe_text(value, default="N/A"):
    if value is None:
        return default
    value = str(value).strip()
    return value if value else default


def safe_lower(value):
    if value is None:
        return ""
    return str(value).strip().lower()


def safe_int(value, default=0):
    try:
        if value is None or value == "":
            return default
        return int(value)
    except Exception:
        return default


def safe_float(value, default=0.0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except Exception:
        return default


def table_exists(cursor, table_name: str) -> bool:
    try:
        cursor.execute("SHOW TABLES LIKE %s", (table_name,))
        return cursor.fetchone() is not None
    except Exception as e:
        logger.warning("table_exists failed for %s: %s", table_name, e)
        return False


def get_existing_columns(cursor, table_name: str) -> set:
    try:
        cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
        rows = cursor.fetchall()
        return {row.get("Field") for row in rows if row.get("Field")}
    except Exception as e:
        logger.warning("get_existing_columns failed for %s: %s", table_name, e)
        return set()


def column_exists(cursor, table_name: str, column_name: str) -> bool:
    return column_name in get_existing_columns(cursor, table_name)


def pick_column(existing_columns: set, candidates: list[str]):
    for col in candidates:
        if col in existing_columns:
            return col
    return None


def build_office_filter(existing_columns: set, alias: str = "", office_id=None):
    if office_id is None:
        return "", []
    if "office_id" not in existing_columns:
        return "", []
    prefix = f"{alias}." if alias else ""
    return f" AND {prefix}`office_id` = %s ", [office_id]


def build_status_filter(existing_columns: set, alias: str = ""):
    if "status" not in existing_columns:
        return ""
    prefix = f"{alias}." if alias else ""
    return f" AND ({prefix}`status` = 1 OR {prefix}`status` IS NULL) "


def limit_clause(limit=None):
    if not limit:
        return ""
    return f" LIMIT {int(limit)} "


def make_chunk(
    text: str,
    module: str,
    office_id=None,
    allowed_roles=None,
    entity_id=None,
    entity_type=None,
    extra=None
):
    payload = {
        "text": text.strip(),
        "module": module,
        "office_id": office_id,
        "allowed_roles": allowed_roles or ["principal", "admin"]
    }

    if entity_id is not None:
        payload["entity_id"] = entity_id

    if entity_type:
        payload["entity_type"] = entity_type

    if extra:
        payload.update(extra)

    return payload


def safe_run(cursor, sql: str, params=None):
    params = params or []
    cursor.execute(sql, params)
    return cursor.fetchall()
