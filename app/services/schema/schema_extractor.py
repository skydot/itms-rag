"""Schema extraction utility for TRMS MySQL dump files.

Parses SQL CREATE TABLE statements to extract table and column names.
Uses regex to avoid heavy dependencies.
"""

import re
from typing import Dict, List


def extract_schema_from_dump(dump_path: str) -> Dict[str, List[str]]:
    """Parse MySQL dump file and extract table names with their columns.
    
    Args:
        dump_path: Path to the SQL dump file
        
    Returns:
        Dictionary mapping table_name -> list of column names
    """
    schema = {}
    
    try:
        with open(dump_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"[SchemaExtractor] Error reading dump: {e}")
        return schema
    
    # Pattern to match CREATE TABLE blocks
    # Matches: CREATE TABLE `table_name` ( ... )
    create_pattern = re.compile(
        r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?`?(\w+)`?\s*\((.*?)\)\s*(?:ENGINE|DEFAULT|PRIMARY|UNIQUE|KEY|CONSTRAINT|\Z)',
        re.DOTALL | re.IGNORECASE
    )
    
    # Pattern to extract column names from CREATE TABLE body
    # Matches: `column_name` TYPE ...
    column_pattern = re.compile(
        r'^\s*`(\w+)`\s+\w+',
        re.MULTILINE
    )
    
    matches = create_pattern.findall(content)
    
    for table_name, table_body in matches:
        columns = column_pattern.findall(table_body)
        if columns:
            schema[table_name] = columns
            
    print(f"[SchemaExtractor] Extracted {len(schema)} tables from dump")
    return schema


def get_columns(table_name: str, dump_path: str = None, cached_schema: Dict = None) -> List[str]:
    """Get columns for a specific table.
    
    Args:
        table_name: Name of the table
        dump_path: Path to dump file (if no cached schema)
        cached_schema: Pre-loaded schema dictionary
        
    Returns:
        List of column names
    """
    if cached_schema is not None:
        return cached_schema.get(table_name, [])
    
    if dump_path:
        schema = extract_schema_from_dump(dump_path)
        return schema.get(table_name, [])
    
    return []


def get_tables_with_prefix(prefix: str, dump_path: str = None, cached_schema: Dict = None) -> Dict[str, List[str]]:
    """Get all tables matching a prefix.
    
    Args:
        prefix: Table name prefix to match
        dump_path: Path to dump file
        cached_schema: Pre-loaded schema dictionary
        
    Returns:
        Dictionary of matching tables and their columns
    """
    if cached_schema is None and dump_path:
        cached_schema = extract_schema_from_dump(dump_path)
    
    if cached_schema is None:
        return {}
    
    return {
        name: cols for name, cols in cached_schema.items()
        if name.lower().startswith(prefix.lower())
    }


# Module-to-tables mapping for TRMS
MODULE_TABLES = {
    "attendance": [
        "attendances", "users", "tra_masters", "training_calendars", 
        "courses", "departments", "designations", "rail_zones", "divisions"
    ],
    "timetable": [
        "time_masters", "tt_designs", "tt_designs_daywise", "training_calendars",
        "courses", "subjects", "topics", "sessions", "class_rooms",
        "users", "designations", "vl_management"
    ],
    "faculty_vl": [
        "vl_management", "vl_description", "feed_que_vls", "users",
        "designations", "subjects", "courses", "training_calendars", "departments"
    ],
    "feedback": [
        "feed_master", "feed_que", "feed_section", "feed_forwards", "feed_que_vls",
        "users", "courses", "training_calendars", "subjects", "vl_management"
    ],
    "complaint": [
        "complaints", "complaints_files", "complaint_cat", "complaint_subcat",
        "comp_categories", "users", "hostel_buildings", "departments", "designations"
    ],
    "library": [
        "books", "book_issue", "book_type", "users", "courses", "training_calendars"
    ],
    "mess": [
        "bills", "bill_details", "bill_receipts", "bill_receipts_refund",
        "mess_bill_format", "mess_material", "items", "item_prices", "partys",
        "users", "courses", "training_calendars", "hostel_masters"
    ],
    "vehicle": [
        "vehicle_masters", "vehicle_registers", "study_tour", "field_training",
        "users", "courses", "training_calendars", "tra_masters"
    ],
    "meeting": [
        "meeting_create", "meeting_master", "meet_agenda", "meeting_agenda",
        "mdl_calenders", "users", "departments", "designations"
    ],
    "seminar": [
        "seminars", "seminars_topic", "topics", "users",
        "vl_management", "subjects", "departments"
    ],
    "inspection": [
        "inspection_notes", "inspection_description", "users", "departments", "designations"
    ],
    "sports": [
        "sport", "sport_team", "sport_item", "sportitem_issue", "sport_material",
        "sports_photos", "srec_sport", "particpants", "partys",
        "users", "courses", "training_calendars"
    ],
    "pass_eq": [
        "pass", "pass_type", "eqs", "users", "train_class", "rail_stations",
        "tra_masters", "courses", "training_calendars"
    ],
    "field_study_tour": [
        "field_training", "filled_training_data", "study_tour", "vehicle_registers",
        "users", "courses", "training_calendars", "tra_masters", "rail_zones", "divisions"
    ],
    "master_admin": [
        "users", "roles", "permissions", "perm_types", "accesses", "services",
        "departments", "designations", "grades", "grade_pay", "pay_level", "pay_scale",
        "rail_zones", "divisions", "depots", "rail_stations", "states", "places",
        "company", "bank", "holidays", "site_info"
    ],
}


def extract_module_schema(module_name: str, dump_path: str) -> Dict[str, List[str]]:
    """Extract schema for a specific module.
    
    Args:
        module_name: Name of the module (must be in MODULE_TABLES)
        dump_path: Path to SQL dump file
        
    Returns:
        Dictionary of tables and columns for the module
    """
    if module_name not in MODULE_TABLES:
        print(f"[SchemaExtractor] Unknown module: {module_name}")
        return {}
    
    full_schema = extract_schema_from_dump(dump_path)
    module_tables = MODULE_TABLES[module_name]
    
    result = {}
    for table in module_tables:
        if table in full_schema:
            result[table] = full_schema[table]
        else:
            print(f"[SchemaExtractor] Warning: Table '{table}' not found in dump for module '{module_name}'")
    
    return result


if __name__ == "__main__":
    # Test extraction
    import json
    dump_file = "/home/erpuser/rag-server/trms_dump.txt"
    
    print("Testing schema extraction...")
    schema = extract_schema_from_dump(dump_file)
    print(f"Total tables: {len(schema)}")
    
    # Test module extraction
    for module in ["attendance", "library", "mess"]:
        mod_schema = extract_module_schema(module, dump_file)
        print(f"\n{module}: {len(mod_schema)} tables")
        for table, cols in list(mod_schema.items())[:2]:
            print(f"  - {table}: {len(cols)} columns")
