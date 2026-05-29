"""LLM-generated SQL fallback for Exam, Trainee, Hostel, and Course modules.

Flow:
1. Build prompt with module-specific schema (no credentials/raw data).
2. Call the configured OpenAI-compatible LLM to generate a SELECT-only SQL query.
3. Validate SQL strictly before execution.
4. Execute against DB and return result dict.
"""

import re
import logging

from app.services.schema.exam_schema import EXAM_SCHEMA
from app.services.schema.trainee_schema import TRAINEE_SCHEMA
from app.services.schema.hostel_schema import HOSTEL_SCHEMA
from app.services.schema.course_schema import COURSE_SCHEMA
from app.services.schema.attendance_schema import ATTENDANCE_SCHEMA
from app.services.schema.timetable_schema import TIMETABLE_SCHEMA
from app.services.schema.faculty_vl_schema import FACULTY_VL_SCHEMA
from app.services.schema.feedback_schema import FEEDBACK_SCHEMA
from app.services.schema.complaint_schema import COMPLAINT_SCHEMA
from app.services.schema.library_schema import LIBRARY_SCHEMA
from app.services.schema.mess_schema import MESS_SCHEMA
from app.services.schema.vehicle_schema import VEHICLE_SCHEMA
from app.services.schema.meeting_schema import MEETING_SCHEMA
from app.services.schema.seminar_schema import SEMINAR_SCHEMA
from app.services.schema.inspection_schema import INSPECTION_SCHEMA
from app.services.schema.sports_schema import SPORTS_SCHEMA
from app.services.schema.pass_eq_schema import PASS_EQ_SCHEMA
from app.services.schema.field_study_tour_schema import FIELD_STUDY_TOUR_SCHEMA
from app.services.schema.master_admin_schema import MASTER_ADMIN_SCHEMA
from app.services.db_service import get_connection
from app.services.llm_service import call_llm

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Allowed tables per module and shared blocked keywords
# ---------------------------------------------------------------------------

ALLOWED_EXAM_TABLES = [
    "courses",
    "et_design",
    "exam_design",
    "exam_marks",
    "exam_type",
    "subjects",
    "users",
    "training_calendars",
]

ALLOWED_TRAINEE_TABLES = [
    "tra_masters",
    "users",
    "training_calendars",
    "rail_zones",  # For zone name lookups (NWR, WCR, etc.)
    "divisions",  # For division name lookups
    "depots",  # For depot name lookups
    "courses",
    "course_for",
    "cs_designs",
    "hostel_buildings",  # For hostel building name lookups (Geetanjali, Chetak, etc.)
    "hostel_masters",    # For trainee hostel allotment records
    "hostel_rooms",      # For room details
]

ALLOWED_HOSTEL_TABLES = [
    "hostel_buildings",
    "hostel_rooms",
    "hostel_masters",
    "all_dues",
    "complaints",
    "users",
    "tra_masters",
    "training_calendars",  # Required for course name lookups via ct_id -> courses.id
    "courses",             # Required for course_name
]

ALLOWED_COURSE_TABLES = [
    "courses",
    "course_for",
    "course_groups",
    "training_calendars",
    "cs_designs",
    "degree",
    "departments",
]

ALLOWED_ATTENDANCE_TABLES = [
    "attendances", "users", "tra_masters", "training_calendars",
    "courses", "departments", "designations", "rail_zones", "divisions"
]

ALLOWED_TIMETABLE_TABLES = [
    "time_masters", "tt_designs", "tt_designs_daywise", "training_calendars",
    "courses", "subjects", "topics", "sessions", "class_rooms",
    "users", "designations", "vl_management"
]

ALLOWED_FACULTY_VL_TABLES = [
    "vl_management", "vl_description", "feed_que_vls", "users",
    "designations", "subjects", "courses", "training_calendars", "departments"
]

ALLOWED_FEEDBACK_TABLES = [
    "feed_master", "feed_que", "feed_section", "feed_forwards", "feed_que_vls",
    "users", "courses", "training_calendars", "subjects", "vl_management"
]

ALLOWED_COMPLAINT_TABLES = [
    "complaints", "complaints_files", "complaint_cat", "complaint_subcat",
    "comp_categories", "users", "hostel_buildings", "departments", "designations"
]

ALLOWED_LIBRARY_TABLES = [
    "books", "book_issue", "book_type", "users", "courses", "training_calendars"
]

ALLOWED_MESS_TABLES = [
    "bills", "bill_details", "bill_receipts", "bill_receipts_refund",
    "mess_bill_format", "mess_material", "items", "item_prices", "partys",
    "users", "courses", "training_calendars", "hostel_masters"
]

ALLOWED_VEHICLE_TABLES = [
    "vehicle_masters", "vehicle_registers", "study_tour", "field_training",
    "users", "courses", "training_calendars", "tra_masters"
]

ALLOWED_MEETING_TABLES = [
    "meeting_create", "meeting_master", "meet_agenda", "mdl_calenders",
    "users", "departments", "designations"
]

ALLOWED_SEMINAR_TABLES = [
    "seminars", "seminars_topic", "topics", "users",
    "vl_management", "subjects", "departments"
]

ALLOWED_INSPECTION_TABLES = [
    "inspection_notes", "inspection_description", "users", "departments", "designations"
]

ALLOWED_SPORTS_TABLES = [
    "sport", "sport_team", "sport_item", "sportitem_issue", "sport_material",
    "sports_photos", "srec_sport", "particpants", "partys",
    "users", "courses", "training_calendars"
]

ALLOWED_PASS_EQ_TABLES = [
    "pass", "pass_type", "eqs", "users", "train_class", "rail_stations",
    "tra_masters", "courses", "training_calendars"
]

ALLOWED_FIELD_STUDY_TOUR_TABLES = [
    "field_training", "filled_training_data", "study_tour", "vehicle_registers",
    "users", "courses", "training_calendars", "tra_masters", "rail_zones", "divisions"
]

ALLOWED_MASTER_ADMIN_TABLES = [
    "users", "roles", "permissions", "perm_types", "accesses", "services",
    "departments", "designations", "grades", "grade_pay", "pay_level", "pay_scale",
    "rail_zones", "divisions", "depots", "rail_stations", "states", "places",
    "company", "bank", "holidays", "site_info"
]

ALL_ALLOWED_TABLES = set(
    ALLOWED_EXAM_TABLES +
    ALLOWED_TRAINEE_TABLES +
    ALLOWED_HOSTEL_TABLES +
    ALLOWED_COURSE_TABLES +
    ALLOWED_ATTENDANCE_TABLES +
    ALLOWED_TIMETABLE_TABLES +
    ALLOWED_FACULTY_VL_TABLES +
    ALLOWED_FEEDBACK_TABLES +
    ALLOWED_COMPLAINT_TABLES +
    ALLOWED_LIBRARY_TABLES +
    ALLOWED_MESS_TABLES +
    ALLOWED_VEHICLE_TABLES +
    ALLOWED_MEETING_TABLES +
    ALLOWED_SEMINAR_TABLES +
    ALLOWED_INSPECTION_TABLES +
    ALLOWED_SPORTS_TABLES +
    ALLOWED_PASS_EQ_TABLES +
    ALLOWED_FIELD_STUDY_TOUR_TABLES +
    ALLOWED_MASTER_ADMIN_TABLES
)

CONCISE_ATTENDANCE_SCHEMA = """
Table: attendances (stores trainee attendance/punch records)
Columns:
- id
- user_id (joins with users.id)
- course_id (joins with training_calendars.id)
- punch_time (datetime)
- punch (status: 4=Present, 5=Absent(AB), 1=CL, 2=LAP, 3=SL)
"""

CONCISE_EXAM_SCHEMA = """
Table: exam_marks (stores trainee marks)
Columns:
- id
- user_id (joins with users.id)
- course_id (joins with training_calendars.id)
- mark_obtained (VARCHAR, cast to numeric for sorting/averages)
- result (1=Pass, 2=Fail, 0=Not Appeared)
- status (1=active)

Table: et_design (stores exam schedules/dates)
Columns:
- id
- course_id (joins with training_calendars.id)
- exam_date (date)
- status (1=active)
"""

CONCISE_HOSTEL_SCHEMA = """
Table: hostel_masters (stores trainee hostel stay records)
Columns:
- id
- user_id (joins with users.id)
- building_id (joins with hostel_buildings.id)
- room_id (joins with hostel_rooms.id)
- in_date (date)
- out_date (date)
- h_status (stay status: 1=currently staying)

Table: hostel_buildings (stores hostel building names)
Columns:
- id
- building_name
"""

CONCISE_FEEDBACK_SCHEMA = """
Table: feed_master (stores feedback responses)
Columns:
- id
- user_id (joins with users.id)
- course_id (joins with training_calendars.id)
- response (VARCHAR rating value)
- status (1=active)
"""

CONCISE_COMPLAINT_SCHEMA = """
Table: complaints (stores user complaints)
Columns:
- id
- user_id (joins with users.id)
- category_id
- complaint_by
- complaint_date
- status (1=active)
"""

CONCISE_TRAINEE_SCHEMA = """
Table: tra_masters (stores trainee course enrollments)
Columns:
- id
- user_id (joins with users.id)
- course_id (joins with training_calendars.id)
- status (1=active)
- is_approved (1=approved)
"""

def get_dynamic_schemas(user_question: str, base_schema: str, base_schema_name: str) -> str:
    """Dynamically append other schemas if keywords from their modules are present in the question."""
    text = user_question.lower()
    combined = base_schema
    
    # 1. Exam
    if "exam" in text or "marks" in text or "result" in text or "score" in text or "topper" in text:
        if base_schema_name != "exam":
            combined += "\n\nCross-Module Table Info:\n" + CONCISE_EXAM_SCHEMA
            
    # 2. Trainee
    if "trainee" in text or "student" in text:
        if base_schema_name != "trainee":
            combined += "\n\nCross-Module Table Info:\n" + CONCISE_TRAINEE_SCHEMA
            
    # 3. Hostel
    if "hostel" in text or "room" in text or "building" in text or "block" in text:
        if base_schema_name != "hostel":
            combined += "\n\nCross-Module Table Info:\n" + CONCISE_HOSTEL_SCHEMA
            
    # 5. Attendance
    if "attendance" in text or "punch" in text or "present" in text or "absent" in text:
        if base_schema_name != "attendance":
            combined += "\n\nCross-Module Table Info:\n" + CONCISE_ATTENDANCE_SCHEMA
            
    # 7. Feedback
    if "feedback" in text or "rating" in text or "review" in text:
        if base_schema_name != "feedback":
            combined += "\n\nCross-Module Table Info:\n" + CONCISE_FEEDBACK_SCHEMA
            
    # 8. Complaint
    if "complaint" in text or "grievance" in text:
        if base_schema_name != "complaint":
            combined += "\n\nCross-Module Table Info:\n" + CONCISE_COMPLAINT_SCHEMA
            
    return combined

BLOCKED_SQL_WORDS = [
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "truncate",
    "create",
    "replace",
    "grant",
    "revoke",
    "load_file",
    "outfile",
    "dumpfile",
    "infile",
]


# ===========================================================================
# Generic helpers (shared across modules)
# ===========================================================================

def clean_llm_sql(sql: str) -> str:
    """Strip markdown fences, whitespace, and extract the SELECT query."""
    if not sql:
        return "UNSUPPORTED_QUERY"

    sql = sql.strip()

    # Remove markdown code fences
    sql = sql.replace("```sql", "").replace("```", "").strip()

    # Check for unsupported marker
    if "UNSUPPORTED_QUERY" in sql.upper():
        return "UNSUPPORTED_QUERY"

    # If LLM added explanation around SQL, try to extract the SELECT statement
    match = re.search(r"(SELECT\s.+)", sql, re.IGNORECASE | re.DOTALL)
    if match:
        sql = match.group(1).strip()

    # Remove trailing semicolons for uniform handling (validator re-checks)
    sql = sql.rstrip(";").strip()

    # Dynamic fix for LLM forgetting to JOIN users when querying module tables
    if "users.office_id" in sql.lower() and "join users" not in sql.lower():
        sql = re.sub(r'(FROM\s+attendances)(?!\s+join)', r'\1 JOIN users ON users.id = attendances.user_id', sql, flags=re.IGNORECASE)
        sql = re.sub(r'(FROM\s+srec_sport)(?!\s+join)', r'\1 JOIN users ON users.id = srec_sport.user_id', sql, flags=re.IGNORECASE)
        sql = re.sub(r'(FROM\s+pass_eq)(?!\s+join)', r'\1 JOIN users ON users.id = pass_eq.user_id', sql, flags=re.IGNORECASE)
        sql = re.sub(r'(FROM\s+library)(?!\s+join)', r'\1 JOIN users ON users.id = library.user_id', sql, flags=re.IGNORECASE)

    return sql


def _validate_sql(sql: str, office_id: int, allowed_tables: list, module_label: str) -> str:
    """Validate LLM-generated SQL for any module. Returns safe SQL or raises ValueError."""

    if not sql or sql.strip().upper() == "UNSUPPORTED_QUERY":
        raise ValueError(f"LLM returned UNSUPPORTED_QUERY — question cannot be answered with {module_label} schema.")

    sql = sql.strip()

    # Must start with SELECT
    if not sql.upper().startswith("SELECT"):
        raise ValueError("SQL must start with SELECT.")

    # Block dangerous keywords (word-boundary check)
    sql_lower = sql.lower()
    for word in BLOCKED_SQL_WORDS:
        # Use word boundary so "updated_at" doesn't match "update"
        if re.search(r'\b' + re.escape(word) + r'\b', sql_lower):
            raise ValueError(f"Blocked SQL keyword detected: {word}")

    # Reject multiple statements
    # Allow zero or one semicolon (only at the very end)
    stripped = sql.rstrip(";").strip()
    if ";" in stripped:
        raise ValueError("Multiple SQL statements detected.")

    # Reject SQL comments
    if re.search(r'--', sql) or re.search(r'/\*', sql) or re.search(r'#', sql):
        raise ValueError("SQL comments are not allowed.")

    # Check that only allowed tables are referenced
    # Extract table-like identifiers after FROM / JOIN keywords
    table_refs = re.findall(r'(?:FROM|JOIN)\s+(\w+)', sql, re.IGNORECASE)
    for tbl in table_refs:
        tbl_lower = tbl.lower()
        if tbl_lower not in allowed_tables and tbl_lower not in ALL_ALLOWED_TABLES:
            raise ValueError(f"Table '{tbl}' is not in allowed database tables.")

    # Must contain the office_id value somewhere (as a number)
    if str(office_id) not in sql:
        raise ValueError(f"SQL must contain office_id = {office_id} for security filtering.")

    # Append LIMIT 50 if not present
    if not re.search(r'\bLIMIT\b', sql, re.IGNORECASE):
        sql = sql.rstrip(";").strip() + " LIMIT 50"

    return sql


def _generate_sql(prompt: str, module_label: str) -> str:
    """Call the configured LLM with a strict SQL prompt and return cleaned SQL."""
    try:
        raw = call_llm(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You generate safe MySQL SELECT queries only. "
                        "Return only one MySQL SELECT query. No markdown. No explanation. "
                        "No comments. If unsure, return exactly UNSUPPORTED_QUERY. "
                        "Use only the provided schema. Always include the required office_id filter. "
                        "Add LIMIT 50 for list/detail queries."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=300,
        )
        return clean_llm_sql(raw)
    except Exception as e:
        logger.error(f"[SQL Fallback/{module_label}] LLM call failed: {e}")
        return "UNSUPPORTED_QUERY"


def _run_fallback(user_question: str, office_id: int, prompt: str,
                  allowed_tables: list, module_label: str) -> dict:
    """End-to-end fallback: generate → validate → execute. Never crashes the API."""
    print(f"[SQL Fallback/{module_label}] No predefined query found. Using {module_label} SQL fallback...")
    logger.info(f"[SQL Fallback/{module_label}] No predefined query found. Using {module_label} SQL fallback...")

    try:
        # Append cross-module join instructions and enforce office_id format
        extra_rules = f"""
CRITICAL SQL GENERATION RULES:
- ALWAYS include a WHERE clause filter for office_id = {office_id} (e.g. `users.office_id = {office_id}`, `training_calendars.office_id = {office_id}`, or `courses.office_id = {office_id}`).
- DO NOT join the same table (like users, courses, or training_calendars) twice in the FROM/JOIN clause without unique aliases. Reuse existing table joins if they are already in the query.
- When joining attendances: use `JOIN attendances ON attendances.user_id = users.id` and filter by punch.
- When joining exam_marks: use `JOIN exam_marks ON exam_marks.user_id = users.id`.
- MySQL ONLY_FULL_GROUP_BY: When using GROUP BY, every column in the SELECT list MUST either be part of an aggregate function (e.g. MAX, MIN, SUM, AVG, COUNT) or be listed in the GROUP BY clause.
- MySQL WHERE vs HAVING: You MUST NOT use aggregate functions (like SUM, AVG, COUNT, MAX, MIN) in the WHERE clause. Any condition filtering aggregated values (e.g. `COUNT(attendances.id) < 75` or `AVG(...) > 90`) MUST be placed in the HAVING clause.
- DO NOT use correlated subqueries inside the WHERE clause on large tables like attendances (e.g. `(SELECT COUNT(*) FROM attendances ...) < 0.75`). Instead, join the table and use GROUP BY with a HAVING clause.
- Ensure all table names and column names match the provided schemas exactly.
"""
        full_prompt = prompt + "\n" + extra_rules
        
        # Step 1: Generate
        raw_sql = _generate_sql(full_prompt, module_label)
        print(f"[SQL Fallback/{module_label}] Generated fallback SQL: {raw_sql}")
        logger.info(f"[SQL Fallback/{module_label}] Generated fallback SQL: {raw_sql}")

        # Step 2: Validate
        safe_sql = _validate_sql(raw_sql, office_id, allowed_tables, module_label)
        print(f"[SQL Fallback/{module_label}] Validated fallback SQL: {safe_sql}")
        logger.info(f"[SQL Fallback/{module_label}] Validated fallback SQL: {safe_sql}")

        # Step 3: Execute (follows db_service pattern)
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(safe_sql)
            rows = cur.fetchall()
        finally:
            conn.close()

        return {
            "source": f"llm_sql_fallback_{module_label.lower()}",
            "sql": safe_sql,
            "rows": rows,
            "row_count": len(rows),
        }

    except ValueError as ve:
        print(f"[SQL Fallback/{module_label}] Fallback SQL blocked: {ve}")
        logger.warning(f"[SQL Fallback/{module_label}] Fallback SQL blocked: {ve}")
        return {
            "source": f"llm_sql_fallback_{module_label.lower()}",
            "error": str(ve),
            "rows": [],
            "row_count": 0,
        }
    except Exception as e:
        print(f"[SQL Fallback/{module_label}] Unexpected error: {e}")
        logger.error(f"[SQL Fallback/{module_label}] Unexpected error: {e}")
        return {
            "source": f"llm_sql_fallback_{module_label.lower()}",
            "error": str(e),
            "rows": [],
            "row_count": 0,
        }


# ===========================================================================
# EXAM module
# ===========================================================================

def build_exam_sql_prompt(user_question: str, office_id: int) -> str:
    """Build an LLM prompt that includes only schema — never credentials."""
    return f"""You are a MySQL SQL generator for TRMS Exam module.

Generate exactly one SQL query.

Rules:
- Generate SELECT query only.
- Use only the provided Exam schema below.
- Do not use INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, REPLACE, GRANT, REVOKE.
- Do not use LOAD_FILE, INTO OUTFILE, INTO DUMPFILE, or INFILE.
- Do not generate multiple statements.
- ALWAYS include a filter for office_id = {office_id} in your WHERE clause (e.g. users.office_id = {office_id}, training_calendars.office_id = {office_id}, or courses.office_id = {office_id}).
- CRITICAL: Since exam_marks, et_design, and exam_design do not have office_id directly, you MUST join training_calendars, courses, or users to filter by office_id.
  - To join from exam_marks: JOIN training_calendars tc ON tc.id = exam_marks.course_id JOIN courses c ON c.id = tc.ct_id WHERE c.office_id = {office_id}
  - To join from et_design: JOIN training_calendars tc ON tc.id = et_design.course_id JOIN courses c ON c.id = tc.ct_id WHERE c.office_id = {office_id}
  - To join from exam_design: JOIN courses c ON c.id = exam_design.cs_id WHERE c.office_id = {office_id}
  Never filter by office_id directly on tables that do not have it!
- Use status = 1 for active records where applicable.
- Add LIMIT 50 for list/detail queries.
- Return SQL only.
- No markdown.
- No explanation.
- If the question cannot be answered using the provided schema, return exactly: UNSUPPORTED_QUERY

SQL behavior:
- For trainee name search, use: LOWER(users.name) LIKE LOWER('%name%')
- For pass count, use exam_marks.result = 1.
- For fail count, use exam_marks.result = 2.
- For not appeared count, use exam_marks.result = 0.
- For year filtering, use YEAR(training_calendars.from_date) or YEAR(et_design.exam_date), depending on question.
- For month filtering, use MONTH(training_calendars.from_date) or MONTH(et_design.exam_date), depending on question.
- CRITICAL: exam_marks table does NOT have an exam_date column. To filter exam marks by date/year/month, you must join training_calendars tc ON tc.id = exam_marks.course_id and use tc.from_date (e.g. YEAR(tc.from_date) = YEAR(CURDATE())).
- CRITICAL: exam_marks.mark_obtained is VARCHAR. When sorting by marks (highest/lowest/toppers), ALWAYS use: ORDER BY CAST(exam_marks.mark_obtained AS UNSIGNED) DESC (or ASC). If you do not CAST, alphabetical sorting will put non-numeric marks like 'Q' (Qualified) at the top.

Schema:
{get_dynamic_schemas(user_question, EXAM_SCHEMA, "exam")}

User question:
{user_question}

SQL:
"""


def generate_exam_sql(user_question: str, office_id: int) -> str:
    """Call the configured LLM with the exam schema prompt and return cleaned SQL."""
    prompt = build_exam_sql_prompt(user_question, office_id)
    return _generate_sql(prompt, "Exam")


def validate_exam_sql(sql: str, office_id: int) -> str:
    """Validate LLM-generated SQL for Exam module."""
    return _validate_sql(sql, office_id, ALLOWED_EXAM_TABLES, "Exam")


def run_exam_sql_fallback(user_question: str, office_id: int) -> dict:
    """Exam module fallback pipeline."""
    prompt = build_exam_sql_prompt(user_question, office_id)
    return _run_fallback(user_question, office_id, prompt, ALLOWED_EXAM_TABLES, "Exam")


# ===========================================================================
# TRAINEE module
# ===========================================================================

def build_trainee_sql_prompt(user_question: str, office_id: int) -> str:
    """Build an LLM prompt for Trainee module — only schema, never credentials."""
    return f"""You are a MySQL SQL generator for TRMS Trainee module.

Generate exactly one SQL query.

Rules:
- Generate SELECT query only.
- Use only the provided Trainee schema below.
- Do not use INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, REPLACE, GRANT, REVOKE.
- Do not use LOAD_FILE, INTO OUTFILE, INTO DUMPFILE, or INFILE.
- Do not generate multiple statements.
- Always include office filtering.
- Prefer tra_masters.office_id = {office_id} for trainee records.
- Also use training_calendars.office_id = {office_id} or courses.office_id = {office_id} when applicable.
- Use status = 1 for active records where applicable.
- Add LIMIT 50 for list/detail queries.
- Do NOT select password column from users table.
- Return SQL only.
- No markdown.
- No explanation.
- If the question cannot be answered using the provided schema, return exactly: UNSUPPORTED_QUERY

SQL behavior:
- For trainee name search, use: LOWER(users.name) LIKE LOWER('%name%')
- For ongoing training: training_calendars.from_date <= CURDATE() AND training_calendars.to_date >= CURDATE()
- For completed training: training_calendars.to_date < CURDATE()
- For upcoming training: training_calendars.from_date > CURDATE()
- For approved trainees: tra_masters.is_approved = 1
- For gender-wise count: GROUP BY users.gender
- For year filtering: YEAR(tra_masters.created_at) or YEAR(training_calendars.from_date)

CRITICAL - RECENT/LATEST/CURRENT COURSE RULES:
- "recent course", "latest course", "current course", "recent batch", "latest batch" = LATEST by training_calendars.from_date DESC, NOT current year.
- For "recent/latest course trainees": ORDER BY training_calendars.from_date DESC LIMIT 1, then COUNT tra_masters.
- For "current course" (ongoing/running NOW): training_calendars.from_date <= CURDATE() AND training_calendars.to_date >= CURDATE().
- For "this year" / "2026": use YEAR(training_calendars.from_date) = year_value.
- DO NOT use YEAR(CURDATE()) for "recent course" - it means latest batch by date.

Example - "how many student join recent course?":
SELECT tc.course_batch, c.course_name, tc.from_date, COUNT(tm.user_id) AS trainee_count
FROM training_calendars tc
JOIN courses c ON c.id = tc.ct_id
LEFT JOIN tra_masters tm ON tm.course_id = tc.id AND tm.status = 1
WHERE tc.office_id = {office_id} AND tc.status = 1
GROUP BY tc.id, tc.course_batch, c.course_name, tc.from_date
ORDER BY tc.from_date DESC
LIMIT 1;

Schema:
{get_dynamic_schemas(user_question, TRAINEE_SCHEMA, "trainee")}

User question:
{user_question}

SQL:
"""


def generate_trainee_sql(user_question: str, office_id: int) -> str:
    """Call the configured LLM with the trainee schema prompt and return cleaned SQL."""
    prompt = build_trainee_sql_prompt(user_question, office_id)
    return _generate_sql(prompt, "Trainee")


def validate_trainee_sql(sql: str, office_id: int) -> str:
    """Validate LLM-generated SQL for Trainee module."""
    return _validate_sql(sql, office_id, ALLOWED_TRAINEE_TABLES, "Trainee")


def run_trainee_sql_fallback(user_question: str, office_id: int) -> dict:
    """Trainee module fallback pipeline."""
    prompt = build_trainee_sql_prompt(user_question, office_id)
    return _run_fallback(user_question, office_id, prompt, ALLOWED_TRAINEE_TABLES, "Trainee")


# ===========================================================================
# HOSTEL module
# ===========================================================================

def build_hostel_sql_prompt(user_question: str, office_id: int) -> str:
    """Build an LLM prompt for Hostel module — only schema, never credentials."""
    return f"""You are a MySQL SQL generator for TRMS Hostel module.

Generate exactly one SQL query.

Rules:
- Generate SELECT query only.
- Use only the provided Hostel schema below.
- Do not use INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, REPLACE, GRANT, REVOKE.
- Do not use LOAD_FILE, INTO OUTFILE, INTO DUMPFILE, or INFILE.
- Do not generate multiple statements.
- Always include office filtering.
- Prefer hostel_masters.office_id = {office_id} for allotment/stay queries.
- Use hostel_buildings.office_id = {office_id} for building queries.
- Use hostel_rooms.office_id = {office_id} for room queries.
- For "currently staying" / "occupancy" queries, use: (h_status = 1 OR h_status = '1') AND (out_date IS NULL OR out_date >= CURDATE())
- Use status = 1 for active records where applicable.
- Add LIMIT 50 for list/detail queries.
- Return SQL only.
- No markdown.
- No explanation.
- If the question cannot be answered using the provided schema, return exactly: UNSUPPORTED_QUERY

SQL behavior:
- For trainee name search, use: LOWER(users.name) LIKE LOWER('%name%')
- For building name search, use: LOWER(hostel_buildings.building_name) LIKE LOWER('%name%')
- For count of occupied rooms: COUNT(DISTINCT room_id) in hostel_masters with (h_status = 1 OR h_status = '1') and active dates. (Do not count total rows/allotments as rooms, since multiple trainees share the same room).
- For count of occupied beds / staying trainees: count of rows (COUNT(*)) in hostel_masters with (h_status = 1 OR h_status = '1') and active dates.
- For vacant/available rooms: rooms NOT IN (SELECT room_id FROM hostel_masters WHERE h_status = 1 AND (out_date IS NULL OR out_date >= CURDATE()))
- For full rooms: WHERE occupied_count >= room_beds
- For check-in today: DATE(hostel_masters.in_date) = CURDATE()
- For check-out today: DATE(hostel_masters.out_date) = CURDATE()
- For overstay: (h_status = 1 OR h_status = '1') AND out_date < CURDATE()
- For ladies hostel: building_name LIKE '%ladies%'
- For AC rooms: hostel_rooms.ac = 'Y'
- For rooms with toilet: hostel_rooms.toilet = 'Y'
- For female/male rooms (no direct gender column on rooms):
  - A room is occupied by female trainees if it has an active allotment (h_status = 1 and (out_date IS NULL OR out_date >= CURDATE())) where the user is female (users.gender = 'F').
  - Active rooms available for female trainees (rooms NOT occupied by females): count of active rooms (hostel_rooms.status = 1) that are NOT occupied by female trainees. E.g., SELECT COUNT(*) FROM hostel_rooms WHERE status = 1 AND id NOT IN (SELECT room_id FROM hostel_masters JOIN users ON users.id = hostel_masters.user_id WHERE users.gender = 'F' AND h_status = 1 AND (out_date IS NULL OR out_date >= CURDATE())).
  - Similar logic applies for males using gender = 'M'.
- When counting available/vacant rooms or beds, DO NOT JOIN hostel_masters in the main FROM clause. Instead, select from hostel_rooms and use NOT IN (subquery on hostel_masters) or LEFT JOIN with a WHERE hm.id IS NULL condition. Joining hostel_masters directly in the FROM clause will incorrectly exclude completely empty rooms that have no history in hostel_masters.

Schema:
{get_dynamic_schemas(user_question, HOSTEL_SCHEMA, "hostel")}

User question:
{user_question}

SQL:
"""


def generate_hostel_sql(user_question: str, office_id: int) -> str:
    """Call the configured LLM with the hostel schema prompt and return cleaned SQL."""
    prompt = build_hostel_sql_prompt(user_question, office_id)
    return _generate_sql(prompt, "Hostel")


def validate_hostel_sql(sql: str, office_id: int) -> str:
    """Validate LLM-generated SQL for Hostel module."""
    return _validate_sql(sql, office_id, ALLOWED_HOSTEL_TABLES, "Hostel")


def run_hostel_sql_fallback(user_question: str, office_id: int) -> dict:
    """Hostel module fallback pipeline."""
    prompt = build_hostel_sql_prompt(user_question, office_id)
    return _run_fallback(user_question, office_id, prompt, ALLOWED_HOSTEL_TABLES, "Hostel")


# ===========================================================================
# COURSE module
# ===========================================================================

def build_course_sql_prompt(user_question: str, office_id: int) -> str:
    """Build an LLM prompt for Course module — only schema, never credentials."""
    return f"""You are a MySQL SQL generator for TRMS Course module.

Generate exactly one SQL query.

Rules:
- Generate SELECT query only.
- Use only the provided Course schema below.
- Do not use INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, REPLACE, GRANT, REVOKE.
- Do not use LOAD_FILE, INTO OUTFILE, INTO DUMPFILE, or INFILE.
- Do not generate multiple statements.
- Always include office filtering.
- Prefer courses.office_id = {office_id} for course master queries.
- For batch/calendar questions, use training_calendars.office_id = {office_id}.
- Use status = 1 for active records where applicable.
- Add LIMIT 50 for list/detail queries.
- Return SQL only.
- No markdown.
- No explanation.
- If the question cannot be answered using the provided schema, return exactly: UNSUPPORTED_QUERY

SQL behavior:
- For course name search, use: LOWER(courses.course_name) LIKE LOWER('%name%') OR LOWER(courses.cs_code) LIKE LOWER('%name%')
- If question asks "course wise", group by courses.course_name.
- If question asks "course for wise/category wise/department wise", join course_for and group by course_for.course_for.
- If question asks "course group wise", join course_groups and group by course_groups.course_group.
- If question asks "promotion/refresher/initial", use course_groups.course_group LIKE '%promotion%' etc.
- If question asks "upcoming", use training_calendars.from_date > CURDATE().
- If question asks "ongoing/current/running", use training_calendars.from_date <= CURDATE() AND training_calendars.to_date >= CURDATE().
- If question asks "completed", use training_calendars.to_date < CURDATE().
- If question asks "hostel/mess/library facility", join cs_designs and use cs_designs.hostel = 1, cs_designs.mess = 1, cs_designs.library = 1.
- For year filtering on training calendars: YEAR(training_calendars.from_date) = year_value.
- For month filtering on training calendars: MONTH(training_calendars.from_date) = month_value.

CRITICAL - RECENT/LATEST/CURRENT COURSE RULES:
- "recent course", "latest course", "current course", "recent batch", "latest batch" = LATEST by training_calendars.from_date DESC, NOT current year.
- For "recent/latest course": ORDER BY training_calendars.from_date DESC LIMIT 1.
- For "current course" (ongoing NOW): training_calendars.from_date <= CURDATE() AND training_calendars.to_date >= CURDATE().
- For "this year" / "2026": use YEAR(training_calendars.from_date) = year_value.
- For "recent course trainees": join training_calendars with tra_masters, ORDER BY tc.from_date DESC LIMIT 1, count trainees.
- DO NOT use YEAR(CURDATE()) for "recent course" - it means latest batch by date.

Example - "show recent course details":
SELECT tc.course_batch, c.course_name, tc.from_date, tc.to_date, tc.seat
FROM training_calendars tc
JOIN courses c ON c.id = tc.ct_id
WHERE tc.office_id = {office_id} AND tc.status = 1
ORDER BY tc.from_date DESC
LIMIT 1;

Schema:
{get_dynamic_schemas(user_question, COURSE_SCHEMA, "course")}

User question:
{user_question}

SQL:
"""


def generate_course_sql(user_question: str, office_id: int) -> str:
    """Call the configured LLM with the course schema prompt and return cleaned SQL."""
    prompt = build_course_sql_prompt(user_question, office_id)
    return _generate_sql(prompt, "Course")


def validate_course_sql(sql: str, office_id: int) -> str:
    """Validate LLM-generated SQL for Course module."""
    return _validate_sql(sql, office_id, ALLOWED_COURSE_TABLES, "Course")


def run_course_sql_fallback(user_question: str, office_id: int) -> dict:
    """Course module fallback pipeline."""
    prompt = build_course_sql_prompt(user_question, office_id)
    return _run_fallback(user_question, office_id, prompt, ALLOWED_COURSE_TABLES, "Course")


# ===========================================================================
# ATTENDANCE module
# ===========================================================================

def build_attendance_sql_prompt(user_question: str, office_id: int) -> str:
    return f"""You are a MySQL SQL generator for TRMS Attendance module.
Generate exactly one SELECT query.
Rules:
- Use only the provided Attendance schema.
- CRITICAL: You MUST use "JOIN users ON users.id = attendances.user_id" and filter by "users.office_id = {office_id}". Never use users.office_id without the JOIN.
- Use status = 1 for active records.
- Add LIMIT 50 for list queries.
- Return SQL only, no markdown, no explanation.
- If cannot answer, return: UNSUPPORTED_QUERY
Schema:
{get_dynamic_schemas(user_question, ATTENDANCE_SCHEMA, "attendance")}
User question:
{user_question}
SQL:
"""

def run_attendance_sql_fallback(user_question: str, office_id: int) -> dict:
    prompt = build_attendance_sql_prompt(user_question, office_id)
    return _run_fallback(user_question, office_id, prompt, ALLOWED_ATTENDANCE_TABLES, "Attendance")


# ===========================================================================
# TIMETABLE module
# ===========================================================================

def build_timetable_sql_prompt(user_question: str, office_id: int) -> str:
    return f"""You are a MySQL SQL generator for TRMS Timetable module.
Generate exactly one SELECT query.
Rules:
- Use only the provided Timetable schema.
- Always include office filtering.
- CRITICAL: Since time_masters, tt_designs, and tt_designs_daywise do not have office_id directly, you MUST join training_calendars (or courses) to filter by office_id.
  - To join from tt_designs: JOIN training_calendars tc ON tc.id = tt_designs.course_id WHERE tc.office_id = {office_id}
  - To join from tt_designs_daywise: JOIN training_calendars tc ON tc.id = tt_designs_daywise.course_id WHERE tc.office_id = {office_id}
  - To join from time_masters: JOIN training_calendars tc ON tc.id = time_masters.course_id WHERE tc.office_id = {office_id}
  Never filter by office_id directly on these tables without joining training_calendars or users!
- Use status = 1 for active records.
- Add LIMIT 50 for list queries.
- Return SQL only, no markdown, no explanation.
- If cannot answer, return: UNSUPPORTED_QUERY
Schema:
{get_dynamic_schemas(user_question, TIMETABLE_SCHEMA, "timetable")}
User question:
{user_question}
SQL:
"""

def run_timetable_sql_fallback(user_question: str, office_id: int) -> dict:
    prompt = build_timetable_sql_prompt(user_question, office_id)
    return _run_fallback(user_question, office_id, prompt, ALLOWED_TIMETABLE_TABLES, "Timetable")


# ===========================================================================
# FACULTY_VL module
# ===========================================================================

def build_faculty_vl_sql_prompt(user_question: str, office_id: int) -> str:
    return f"""You are a MySQL SQL generator for TRMS Faculty/VL module.
Generate exactly one SELECT query.
Rules:
- Use only the provided Faculty VL schema.
- Always include vl_management.office_id = {office_id} for security.
- Use status = 1 for active records.
- Add LIMIT 50 for list queries.
- Return SQL only, no markdown, no explanation.
- If cannot answer, return: UNSUPPORTED_QUERY
Schema:
{FACULTY_VL_SCHEMA}
User question:
{user_question}
SQL:
"""

def run_faculty_vl_sql_fallback(user_question: str, office_id: int) -> dict:
    prompt = build_faculty_vl_sql_prompt(user_question, office_id)
    return _run_fallback(user_question, office_id, prompt, ALLOWED_FACULTY_VL_TABLES, "Faculty_VL")


# ===========================================================================
# FEEDBACK module
# ===========================================================================

def build_feedback_sql_prompt(user_question: str, office_id: int) -> str:
    return f"""You are a MySQL SQL generator for TRMS Feedback module.
Generate exactly one SELECT query.
Rules:
- Use only the provided Feedback schema.
- Always include office filtering.
- CRITICAL: Since feed_master and feed_forwards do not have office_id directly, you MUST join training_calendars, courses, or users to filter by office_id.
  - To join from feed_master: JOIN training_calendars tc ON tc.id = feed_master.course_id WHERE tc.office_id = {office_id} (or JOIN users ON users.id = feed_master.user_id WHERE users.office_id = {office_id})
  - To join from feed_forwards: JOIN training_calendars tc ON tc.id = feed_forwards.course_id WHERE tc.office_id = {office_id}
  Never filter by office_id directly on these tables without the correct JOINs!
- Use status = 1 for active records where applicable.
- Add LIMIT 50 for list queries.
- Return SQL only, no markdown, no explanation.
- If cannot answer, return: UNSUPPORTED_QUERY
Schema:
{get_dynamic_schemas(user_question, FEEDBACK_SCHEMA, "feedback")}
User question:
{user_question}
SQL:
"""

def run_feedback_sql_fallback(user_question: str, office_id: int) -> dict:
    prompt = build_feedback_sql_prompt(user_question, office_id)
    return _run_fallback(user_question, office_id, prompt, ALLOWED_FEEDBACK_TABLES, "Feedback")


# ===========================================================================
# COMPLAINT module
# ===========================================================================

def build_complaint_sql_prompt(user_question: str, office_id: int) -> str:
    return f"""You are a MySQL SQL generator for TRMS Complaint module.
Generate exactly one SELECT query.
Rules:
- Use only the provided Complaint schema.
- Always include complaints.office_id = {office_id} for security.
- Use status = 1 for active records.
- Add LIMIT 50 for list queries.
- Return SQL only, no markdown, no explanation.
- If cannot answer, return: UNSUPPORTED_QUERY
Schema:
{get_dynamic_schemas(user_question, COMPLAINT_SCHEMA, "complaint")}
User question:
{user_question}
SQL:
"""

def run_complaint_sql_fallback(user_question: str, office_id: int) -> dict:
    prompt = build_complaint_sql_prompt(user_question, office_id)
    return _run_fallback(user_question, office_id, prompt, ALLOWED_COMPLAINT_TABLES, "Complaint")


# ===========================================================================
# LIBRARY module
# ===========================================================================

def build_library_sql_prompt(user_question: str, office_id: int) -> str:
    return f"""You are a MySQL SQL generator for TRMS Library module.
Generate exactly one SELECT query.
Rules:
- Use only the provided Library schema.
- Always include office_id = {office_id} for security.
- Use status = 1 for active records.
- Add LIMIT 50 for list queries.
- Return SQL only, no markdown, no explanation.
- If cannot answer, return: UNSUPPORTED_QUERY
Schema:
{LIBRARY_SCHEMA}
User question:
{user_question}
SQL:
"""

def run_library_sql_fallback(user_question: str, office_id: int) -> dict:
    prompt = build_library_sql_prompt(user_question, office_id)
    return _run_fallback(user_question, office_id, prompt, ALLOWED_LIBRARY_TABLES, "Library")


# ===========================================================================
# MESS module
# ===========================================================================

def build_mess_sql_prompt(user_question: str, office_id: int) -> str:
    return f"""You are a MySQL SQL generator for TRMS Mess module.
Generate exactly one SELECT query.
Rules:
- Use only the provided Mess schema.
- Always include office_id = {office_id} for security.
- Use status = 1 for active records.
- Add LIMIT 50 for list queries.
- Return SQL only, no markdown, no explanation.
- If cannot answer, return: UNSUPPORTED_QUERY
Schema:
{MESS_SCHEMA}
User question:
{user_question}
SQL:
"""

def run_mess_sql_fallback(user_question: str, office_id: int) -> dict:
    prompt = build_mess_sql_prompt(user_question, office_id)
    return _run_fallback(user_question, office_id, prompt, ALLOWED_MESS_TABLES, "Mess")


# ===========================================================================
# VEHICLE module
# ===========================================================================

def build_vehicle_sql_prompt(user_question: str, office_id: int) -> str:
    return f"""You are a MySQL SQL generator for TRMS Vehicle module.
Generate exactly one SELECT query.
Rules:
- Use only the provided Vehicle schema.
- Always include training_calendars.office_id = {office_id} for security.
- Use status = 1 for active records.
- Add LIMIT 50 for list queries.
- Return SQL only, no markdown, no explanation.
- If cannot answer, return: UNSUPPORTED_QUERY
Schema:
{VEHICLE_SCHEMA}
User question:
{user_question}
SQL:
"""

def run_vehicle_sql_fallback(user_question: str, office_id: int) -> dict:
    prompt = build_vehicle_sql_prompt(user_question, office_id)
    return _run_fallback(user_question, office_id, prompt, ALLOWED_VEHICLE_TABLES, "Vehicle")


# ===========================================================================
# MEETING module
# ===========================================================================

def build_meeting_sql_prompt(user_question: str, office_id: int) -> str:
    return f"""You are a MySQL SQL generator for TRMS Meeting module.
Generate exactly one SELECT query.
Rules:
- Use only the provided Meeting schema.
- Always include office_id = {office_id} for security.
- Use status = 1 for active records.
- Add LIMIT 50 for list queries.
- Return SQL only, no markdown, no explanation.
- If cannot answer, return: UNSUPPORTED_QUERY
Schema:
{MEETING_SCHEMA}
User question:
{user_question}
SQL:
"""

def run_meeting_sql_fallback(user_question: str, office_id: int) -> dict:
    prompt = build_meeting_sql_prompt(user_question, office_id)
    return _run_fallback(user_question, office_id, prompt, ALLOWED_MEETING_TABLES, "Meeting")


# ===========================================================================
# SEMINAR module
# ===========================================================================

def build_seminar_sql_prompt(user_question: str, office_id: int) -> str:
    return f"""You are a MySQL SQL generator for TRMS Seminar module.
Generate exactly one SELECT query.
Rules:
- Use only the provided Seminar schema.
- Always include office_id = {office_id} for security.
- Use status = 1 for active records.
- Add LIMIT 50 for list queries.
- Return SQL only, no markdown, no explanation.
- If cannot answer, return: UNSUPPORTED_QUERY
Schema:
{SEMINAR_SCHEMA}
User question:
{user_question}
SQL:
"""

def run_seminar_sql_fallback(user_question: str, office_id: int) -> dict:
    prompt = build_seminar_sql_prompt(user_question, office_id)
    return _run_fallback(user_question, office_id, prompt, ALLOWED_SEMINAR_TABLES, "Seminar")


# ===========================================================================
# INSPECTION module
# ===========================================================================

def build_inspection_sql_prompt(user_question: str, office_id: int) -> str:
    return f"""You are a MySQL SQL generator for TRMS Inspection module.
Generate exactly one SELECT query.
Rules:
- Use only the provided Inspection schema.
- Always include inspection_notes.office_id = {office_id} for security.
- Use status = 1 for active records.
- Add LIMIT 50 for list queries.
- Return SQL only, no markdown, no explanation.
- If cannot answer, return: UNSUPPORTED_QUERY
Schema:
{INSPECTION_SCHEMA}
User question:
{user_question}
SQL:
"""

def run_inspection_sql_fallback(user_question: str, office_id: int) -> dict:
    prompt = build_inspection_sql_prompt(user_question, office_id)
    return _run_fallback(user_question, office_id, prompt, ALLOWED_INSPECTION_TABLES, "Inspection")


# ===========================================================================
# SPORTS module
# ===========================================================================

def build_sports_sql_prompt(user_question: str, office_id: int) -> str:
    return f"""You are a MySQL SQL generator for TRMS Sports module.
Generate exactly one SELECT query.
Rules:
- Use only the provided Sports schema.
- Always include users.office_id = {office_id} for security via joins.
- Use status = 1 for active records.
- Add LIMIT 50 for list queries.
- Return SQL only, no markdown, no explanation.
- If cannot answer, return: UNSUPPORTED_QUERY
Schema:
{SPORTS_SCHEMA}
User question:
{user_question}
SQL:
"""

def run_sports_sql_fallback(user_question: str, office_id: int) -> dict:
    prompt = build_sports_sql_prompt(user_question, office_id)
    return _run_fallback(user_question, office_id, prompt, ALLOWED_SPORTS_TABLES, "Sports")


# ===========================================================================
# PASS_EQ module
# ===========================================================================

def build_pass_eq_sql_prompt(user_question: str, office_id: int) -> str:
    return f"""You are a MySQL SQL generator for TRMS Pass/EQ module.
Generate exactly one SELECT query.
Rules:
- Use only the provided Pass/EQ schema.
- Always include users.office_id = {office_id} for security via joins.
- Use status = 1 for active records.
- Add LIMIT 50 for list queries.
- Return SQL only, no markdown, no explanation.
- If cannot answer, return: UNSUPPORTED_QUERY
Schema:
{PASS_EQ_SCHEMA}
User question:
{user_question}
SQL:
"""

def run_pass_eq_sql_fallback(user_question: str, office_id: int) -> dict:
    prompt = build_pass_eq_sql_prompt(user_question, office_id)
    return _run_fallback(user_question, office_id, prompt, ALLOWED_PASS_EQ_TABLES, "Pass_EQ")


# ===========================================================================
# FIELD_STUDY_TOUR module
# ===========================================================================

def build_field_study_tour_sql_prompt(user_question: str, office_id: int) -> str:
    return f"""You are a MySQL SQL generator for TRMS Field Training/Study Tour module.
Generate exactly one SELECT query.
Rules:
- Use only the provided Field Study Tour schema.
- Always include training_calendars.office_id = {office_id} for security.
- Use status = 1 for active records.
- Add LIMIT 50 for list queries.
- Return SQL only, no markdown, no explanation.
- If cannot answer, return: UNSUPPORTED_QUERY
Schema:
{FIELD_STUDY_TOUR_SCHEMA}
User question:
{user_question}
SQL:
"""

def run_field_study_tour_sql_fallback(user_question: str, office_id: int) -> dict:
    prompt = build_field_study_tour_sql_prompt(user_question, office_id)
    return _run_fallback(user_question, office_id, prompt, ALLOWED_FIELD_STUDY_TOUR_TABLES, "Field_Study_Tour")


# ===========================================================================
# MASTER_ADMIN module
# ===========================================================================

def build_master_admin_sql_prompt(user_question: str, office_id: int) -> str:
    return f"""You are a MySQL SQL generator for TRMS Master Admin module.
Generate exactly one SELECT query.
Rules:
- Use only the provided Master Admin schema.
- Always include office_id = {office_id} where applicable.
- Use status = 1 for active records.
- Add LIMIT 50 for list queries.
- Return SQL only, no markdown, no explanation.
- If cannot answer, return: UNSUPPORTED_QUERY
Schema:
{MASTER_ADMIN_SCHEMA}
User question:
{user_question}
SQL:
"""

def run_master_admin_sql_fallback(user_question: str, office_id: int) -> dict:
    prompt = build_master_admin_sql_prompt(user_question, office_id)
    return _run_fallback(user_question, office_id, prompt, ALLOWED_MASTER_ADMIN_TABLES, "Master_Admin")
