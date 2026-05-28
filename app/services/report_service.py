"""
Report Generation Service

Generates temporary HTML reports for list/detail queries.
"""

import os
import json
import html
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

# Configuration
REPORTS_DIR = Path("app/static/reports")
DEFAULT_TTL_SECONDS = int(os.getenv("REPORT_TTL_SECONDS", "180"))  # 3 minutes for testing
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

# Sensitive columns to exclude from reports (IDs, internal fields, status codes, PII)
_SENSITIVE_COLUMNS = {
    # IDs (primary keys, foreign keys)
    'id', 'user_id', 'trainee_id', 'course_id', 'exam_id', 'subject_id',
    'tra_master_id', 'hostel_master_id', 'complaint_id', 'feedback_id',
    'schedule_id', 'template_id', 'meeting_id', 'seminar_id',
    # Internal/system fields
    'created_at', 'updated_at', 'created_by', 'updated_by', 'deleted_at',
    'office_id', 'role_id', 'department_id', 'designation_id',
    # Status/result codes (numeric codes that expose internal data)
    'status', 'user_status', 'course_status', 'trainee_status',
    'result', 're_exam_result',  # Exam result codes (0,1,2)
    'is_active', 'is_deleted', 'is_verified', 'is_approved',
    # Internal flags/codes
    'sort_order', 'priority', 'type', 'user_type', 'course_type',
    # Sensitive PII
    'password', 'pass_file', 'user_log', 'room_log', 'attachment',
    'signature', 'photo', 'emergency_numbers', 'office_mobile',
    'emg_mobile_no', 'whatsapp_number', 'present_address',
    'permanent_address', 'resi_address', 'email', 'office_email',
    'bank_acc', 'ifsc_code', 'aadhar', 'uan', 'pf_no', 'permanent_identity',
    'android_id', 'hrms_id'
}


def _generate_filename(module_name: str) -> str:
    """Generate a safe, unique filename for the report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_suffix = secrets.token_hex(4)
    return f"{module_name}_{timestamp}_{random_suffix}"


def _sanitize_value(value) -> str:
    """Sanitize a value for safe HTML display."""
    if value is None:
        return ""
    if isinstance(value, (bytes,)):
        return "[BINARY]"
    # Escape HTML entities
    return html.escape(str(value))


def _format_column_header(col_name: str) -> str:
    """Convert column name to human-readable header."""
    # Remove common suffixes
    clean = col_name.lower()
    
    # Common replacements
    replacements = {
        'holiday_name': 'Holiday',
        'holiday_date': 'Date',
        'trainee_name': 'Trainee Name',
        'student_name': 'Student Name',
        'user_name': 'Name',
        'full_name': 'Full Name',
        'course_name': 'Course',
        'exam_name': 'Exam',
        'subject_name': 'Subject',
        'marks': 'Marks',
        'total_marks': 'Total Marks',
        'obtained_marks': 'Obtained',
        'percentage': 'Percentage',
        'result': 'Result',
        'grade': 'Grade',
        'attendance_date': 'Date',
        'attendance_status': 'Status',
        'complaint_type': 'Type',
        'complaint_description': 'Description',
        'feedback_rating': 'Rating',
        'feedback_comments': 'Comments',
        'meeting_title': 'Meeting',
        'seminar_title': 'Seminar',
        'vehicle_number': 'Vehicle No',
        'vehicle_type': 'Type',
        'library_name': 'Library',
        'book_name': 'Book',
        'hostel_name': 'Hostel',
        'room_number': 'Room',
        'designation_name': 'Designation',
        'department_name': 'Department',
    }
    
    if clean in replacements:
        return replacements[clean]
    
    # Default: convert snake_case to Title Case
    return clean.replace('_', ' ').title()


def _filter_columns(rows: List[Dict]) -> List[str]:
    """Filter out sensitive columns from report."""
    if not rows:
        return []
    
    all_columns = list(rows[0].keys())
    safe_columns = [
        col for col in all_columns
        if col.lower() not in _SENSITIVE_COLUMNS and not col.lower().endswith('_id')
    ]
    return safe_columns


def _generate_html_report(
    title: str,
    user_question: str,
    module_name: str,
    office_id: int,
    rows: List[Dict],
    safe_columns: List[str],
    created_at: datetime,
    expires_at: datetime
) -> str:
    """Generate HTML report content."""
    
    row_count = len(rows)
    
    # Build table headers
    headers_html = "".join([f"<th>{_sanitize_value(col)}</th>" for col in safe_columns])
    
    # Build table rows
    rows_html = ""
    for row in rows:
        row_html = "<tr>"
        for col in safe_columns:
            value = row.get(col, "")
            row_html += f"<td>{_sanitize_value(value)}</td>"
        row_html += "</tr>"
        rows_html += row_html
    
    # Debug info (only if DEBUG_MODE is true)
    debug_section = ""
    if DEBUG_MODE:
        debug_section = f"""
        <div class="debug-info">
            <h3>Debug Info</h3>
            <p><strong>Module:</strong> {module_name}</p>
            <p><strong>Office ID:</strong> {office_id}</p>
            <p><strong>Generated At:</strong> {created_at.isoformat()}</p>
        </div>
        """
    
    # Build table headers with human-readable names
    headers_html = "".join([f"<th>{_sanitize_value(_format_column_header(col))}</th>" for col in safe_columns])
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Report</title>
    <style>
        * {{
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .query-box {{
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 15px 20px;
            margin-bottom: 20px;
            border-radius: 0 5px 5px 0;
        }}
        .query-box .label {{
            font-weight: bold;
            color: #1976d2;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .query-box .question {{
            color: #333;
            font-size: 16px;
            margin-top: 5px;
        }}
        .timestamp {{
            color: #666;
            font-size: 12px;
            margin-bottom: 20px;
        }}
        .expiry-warning {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            color: #856404;
            padding: 10px 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 13px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            font-size: 14px;
        }}
        thead {{
            background: #f5f5f5;
            border-bottom: 2px solid #ddd;
        }}
        th {{
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #555;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #e0e0e0;
            vertical-align: top;
        }}
        tr:nth-child(even) {{
            background: #fafafa;
        }}
        tr:hover {{
            background: #f5f5f5;
        }}
        .empty-state {{
            text-align: center;
            padding: 50px;
            color: #666;
        }}
        @media print {{
            body {{
                background: white;
            }}
            .container {{
                box-shadow: none;
                max-width: none;
            }}
            .expiry-warning {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="query-box">
            <div class="label">Question</div>
            <div class="question">{_sanitize_value(user_question)}</div>
        </div>
        
        <div class="timestamp">Generated: {created_at.strftime('%Y-%m-%d %H:%M:%S')}</div>
        
        <div class="expiry-warning">
            ⚠️ This report link will expire at {expires_at.strftime('%Y-%m-%d %H:%M:%S')} ({DEFAULT_TTL_SECONDS // 3600} hour{'s' if DEFAULT_TTL_SECONDS != 3600 else ''})
        </div>
        
        {f'''
        <div class="empty-state">
            <h3>No records found</h3>
            <p>The query did not return any matching records.</p>
        </div>
        ''' if row_count == 0 else f'''
        <table>
            <thead>
                <tr>{headers_html}</tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
        '''}
    </div>
</body>
</html>"""
    
    return html_content


def generate_report(
    module_name: str,
    title: str,
    user_question: str,
    rows: List[Dict],
    office_id: int,
    session_id: Optional[str] = None,
    file_type: str = "html"
) -> Dict:
    """
    Generate a temporary HTML report and return report metadata.
    
    Args:
        module_name: Name of the module (e.g., "attendance", "exam")
        title: Report title
        user_question: Original user question
        rows: List of dicts (query results)
        office_id: User's office ID
        session_id: Optional session identifier for grouping reports
        file_type: Report format (currently only "html" supported)
        
    Returns:
        Dict with report_id, title, row_count, url, file_path, expires_at, ttl_seconds
    """
    # Validate module name (prevent path traversal)
    safe_module = "".join(c for c in module_name if c.isalnum() or c == "_")
    
    # Generate unique filename
    base_filename = _generate_filename(safe_module)
    html_filename = f"{base_filename}.html"
    json_filename = f"{base_filename}.json"
    
    # Determine directory path
    if session_id:
        # Sanitize session_id
        safe_session_id = "".join(c for c in session_id if c.isalnum() or c in "-_")
        reports_subdir = REPORTS_DIR / safe_session_id
    else:
        reports_subdir = REPORTS_DIR / "temp"
    
    # Create directories if needed
    reports_subdir.mkdir(parents=True, exist_ok=True)
    
    # Calculate timestamps
    created_at = datetime.now()
    expires_at = created_at + timedelta(seconds=DEFAULT_TTL_SECONDS)
    
    # Filter sensitive columns
    safe_columns = _filter_columns(rows)
    
    # Generate HTML report
    html_content = _generate_html_report(
        title=title,
        user_question=user_question,
        module_name=safe_module,
        office_id=office_id,
        rows=rows,
        safe_columns=safe_columns,
        created_at=created_at,
        expires_at=expires_at
    )
    
    # Write HTML file
    html_path = reports_subdir / html_filename
    html_path.write_text(html_content, encoding="utf-8")
    
    # Generate metadata JSON
    metadata = {
        "file": html_filename,
        "created_at": created_at.isoformat(),
        "expires_at": expires_at.isoformat(),
        "ttl_seconds": DEFAULT_TTL_SECONDS,
        "session_id": session_id or None,
        "module_name": safe_module,
        "row_count": len(rows),
        "office_id": office_id,
        "user_question": user_question
    }
    
    # Write JSON metadata file
    json_path = reports_subdir / json_filename
    json_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    
    # Build URL path
    if session_id:
        url_path = f"/reports/{safe_session_id}/{html_filename}"
    else:
        url_path = f"/reports/temp/{html_filename}"
    
    return {
        "report_id": base_filename,
        "title": title,
        "row_count": len(rows),
        "url": url_path,
        "file_path": str(html_path.relative_to("app")),
        "expires_at": expires_at.isoformat(),
        "ttl_seconds": DEFAULT_TTL_SECONDS
    }


def get_report_ttl() -> int:
    """Get the current report TTL setting."""
    return DEFAULT_TTL_SECONDS
