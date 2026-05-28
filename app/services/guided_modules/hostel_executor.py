"""Hostel query executor — runs final parameterized SQL for hostel guided flows.

Uses existing response_mode_service and report_service for output formatting.
"""

from typing import Dict, Optional
from app.services.db_service import get_connection
from app.services.response_mode_service import detect_response_mode
from app.services.report_service import generate_report
from app.services.llm_service import format_answer


_SENSITIVE_COLS = {
    'id', 'user_id', 'trainee_id', 'course_id', 'office_id', 'password',
    'created_by', 'updated_by', 'created_at', 'updated_at', 'status',
    'aadhar', 'uan', 'pf_no', 'bank_acc', 'ifsc_code', 'android_id',
    'permanent_identity', 'photo', 'signature', 'email', 'office_email',
    'whatsapp_number', 'emergency_numbers', 'office_mobile', 'emg_mobile_no',
    'present_address', 'permanent_address', 'resi_address', 'pass_file',
    'user_log', 'room_log', 'attachment', 'hrms_id',
}


def _format_rows_for_chat(rows: list, max_rows: int = 5, total_count: Optional[int] = None) -> str:
    if not rows:
        return "No data found."
    if len(rows) == 1 and len(rows[0]) == 1:
        k = list(rows[0].keys())[0]
        v = rows[0][k]
        return f"{k}: {'N/A' if v is None else str(v)}"
    limited = rows[:max_rows]
    lines = []
    for i, row in enumerate(limited, 1):
        parts = []
        for k, v in row.items():
            if k.lower() not in _SENSITIVE_COLS and v is not None and str(v).strip() != "":
                label = k.replace('_', ' ').title()
                parts.append(f"{label}: {str(v)}")
        if parts:
            lines.append(f"{i}. " + " | ".join(parts))
    actual_total = total_count if total_count is not None else len(rows)
    summary = f"Total count: {actual_total}"
    if actual_total > max_rows:
        summary += f"\n(showing top {max_rows} to avoid text overload. Use 'show list' for full report)"
    return summary + "\n" + "\n".join(lines)


def execute_hostel_guided_query(
    flow_id: str,
    slots: dict,
    office_id: int,
    role: str,
    session_id: str = None,
    user_question: str = "",
    base_url: str = "http://localhost:8000",
) -> dict:
    """Execute the final guided query and return formatted result."""
    try:
        print(f"[Hostel Guided] Executing: {flow_id} with slots: {slots}")
        handler = {
            "hostel_availability_occupency": _exec_hostel_availability_occupency,
            "hostel_full_rooms": _exec_hostel_full_rooms,
            "hostel_room_by_trainee": _exec_hostel_room_by_trainee,
            "hostel_trainees_by_room": _exec_hostel_trainees_by_room,
            "hostel_trainees_by_building": _exec_hostel_trainees_by_building,
            "hostel_building_summary": _exec_hostel_building_summary,
            "hostel_vacant_beds_by_building": _exec_hostel_vacant_beds_by_building,
            "hostel_dues_by_trainee": _exec_hostel_dues_by_trainee,
            "hostel_allocation_summary": _exec_hostel_allocation_summary,
        }.get(flow_id)
        if not handler:
            return None
        return handler(slots, office_id, user_question, session_id, base_url)
    except Exception as e:
        print(f"[Hostel Guided] Error executing {flow_id}: {e}")
        return {"type": "text", "message": f"Error retrieving hostel data: {str(e)}"}


def _build_response(rows, question, office_id, session_id, base_url,
                     force_report=False, force_chat=False, total_count=None):
    row_count = len(rows)
    actual_count = total_count if total_count is not None else row_count
    if actual_count == 0:
        return {"type": "text", "message": "No matching hostel data found for your request."}
    if force_chat:
        mode = "chat"
    elif force_report:
        mode = "report"
    else:
        mode = detect_response_mode(
            user_question=question,
            result_type="list" if actual_count > 1 else "single",
            row_count=actual_count,
        )
    if mode == "report" and row_count > 1:
        report = generate_report(
            module_name="hostel", title="Hostel Report",
            user_question=question, rows=rows,
            office_id=office_id, session_id=session_id,
        )
        full_url = base_url.rstrip("/") + report["url"]
        ttl = report["ttl_seconds"]
        if ttl < 60: exp = f"{ttl} seconds"
        elif ttl < 3600: exp = f"{ttl // 60} minute{'s' if ttl // 60 != 1 else ''}"
        else: exp = f"{ttl // 3600} hour{'s' if ttl // 3600 != 1 else ''}"
        if total_count and total_count > row_count:
            count_msg = f"Found {total_count} records (showing {report['row_count']} in report)."
        else:
            count_msg = f"Found {report['row_count']} records for your request."
        answer = f"{count_msg}\n\nOpen full report: {full_url}\n\nThis report link will expire in {exp}."
        return {
            "type": "text", "message": answer,
            "report_url": full_url, "row_count": report["row_count"],
            "response_mode": "report", "expires_at": report["expires_at"],
        }
    else:
        formatted_text = _format_rows_for_chat(rows, total_count=total_count)
        answer = format_answer(question, formatted_text)
        return {"type": "text", "message": answer}


def _get_building_filter(slots, text_param="hb"):
    """Build SQL fragment + params for building/hostel_type filtering."""
    sql_parts = []
    params = []
    bid = slots.get("building_id")
    if bid and bid != "ALL":
        sql_parts.append(f" AND {text_param}.id = %s")
        params.append(bid)
    # Note: hostel_type (gents/ladies) is ignored because building names
    # (e.g. ARAVALI, CHETAK) don't contain gender keywords.
    # All buildings are shown when no specific building_id is selected.
    return "".join(sql_parts), params


# ═══════════════════════════════════════════════════════════════════
# Individual executor handlers
# ═══════════════════════════════════════════════════════════════════

def _exec_hostel_availability_occupency(slots, office_id, question, session_id, base_url):
    conn = get_connection()
    try:
        cur = conn.cursor()
        bfilter, bparams = _get_building_filter(slots)
        sql = f"""
            SELECT hb.building_name,
                   COUNT(hr.id) AS total_rooms,
                   SUM(hr.room_beds) AS total_beds,
                   COALESCE(occ.occupied_beds, 0) AS occupied_beds,
                   (SUM(hr.room_beds) - COALESCE(occ.occupied_beds, 0)) AS available_beds,
                   COALESCE(occ.occupied_rooms, 0) AS occupied_rooms,
                   (COUNT(hr.id) - COALESCE(occ.occupied_rooms, 0)) AS available_rooms
            FROM hostel_buildings hb
            LEFT JOIN hostel_rooms hr ON hr.building_id = hb.id AND hr.status = 1
            LEFT JOIN (
                SELECT hm.building_id,
                       COUNT(DISTINCT hm.room_id) AS occupied_rooms,
                       SUM(hm.beds) AS occupied_beds
                FROM hostel_masters hm
                WHERE hm.office_id = %s AND hm.h_status = 1
                  AND (hm.out_date IS NULL OR hm.out_date > NOW())
                GROUP BY hm.building_id
            ) occ ON occ.building_id = hb.id
            WHERE hb.office_id = %s AND hb.status = 1{bfilter}
            GROUP BY hb.id, hb.building_name, occ.occupied_beds, occ.occupied_rooms
            ORDER BY hb.building_name
        """
        cur.execute(sql, [office_id, office_id] + bparams)
        rows = cur.fetchall()
        
        force_chat = detect_response_mode(question) == "chat"
        if force_chat:
            total_rooms = sum(r["total_rooms"] for r in rows if r["total_rooms"])
            total_beds = sum(r["total_beds"] for r in rows if r["total_beds"])
            occ_rooms = sum(r["occupied_rooms"] for r in rows if r["occupied_rooms"])
            avail_rooms = sum(r["available_rooms"] for r in rows if r["available_rooms"])
            occ_beds = sum(r["occupied_beds"] for r in rows if r["occupied_beds"])
            avail_beds = sum(r["available_beds"] for r in rows if r["available_beds"])
            
            q_lower = question.lower()
            if "occupied" in q_lower or "occupy" in q_lower or "fill" in q_lower:
                total_msg = f"Overall Occupancy: {occ_rooms} occupied rooms out of {total_rooms} total rooms ({avail_rooms} completely available). {occ_beds} occupied beds out of {total_beds} total beds."
            elif "available" in q_lower or "vacant" in q_lower or "empty" in q_lower or "free" in q_lower:
                total_msg = f"Overall Availability: {avail_rooms} fully available rooms out of {total_rooms} total rooms ({occ_rooms} occupied). {avail_beds} available beds out of {total_beds} total beds."
            else:
                total_msg = f"Overall Summary: {avail_rooms} available rooms, {occ_rooms} occupied rooms. {avail_beds} available beds, {occ_beds} occupied beds."
                
            if not rows:
                return {"type": "text", "message": format_answer(question, total_msg)}
            formatted = _format_rows_for_chat(rows)
            return {"type": "text", "message": format_answer(question, f"{total_msg}\n\n{formatted}")}
            
        return _build_response(rows, question, office_id, session_id, base_url, force_chat=force_chat)
    finally:
        conn.close()


def _exec_hostel_full_rooms(slots, office_id, question, session_id, base_url):
    conn = get_connection()
    try:
        cur = conn.cursor()
        bfilter, bparams = _get_building_filter(slots)
        sql = f"""
            SELECT hb.building_name, hr.room_name, hr.room_beds, COUNT(hm.id) AS occupants
            FROM hostel_rooms hr
            JOIN hostel_buildings hb ON hb.id = hr.building_id
            LEFT JOIN hostel_masters hm ON hm.room_id = hr.id AND hm.h_status = 1
              AND (hm.out_date IS NULL OR hm.out_date > NOW())
            WHERE hr.office_id = %s AND hr.status = 1{bfilter}
            GROUP BY hr.id, hb.building_name, hr.room_name, hr.room_beds
            HAVING occupants >= hr.room_beds AND hr.room_beds > 0
            ORDER BY hb.building_name, hr.room_name
        """
        cur.execute(sql, [office_id] + bparams)
        rows = cur.fetchall()
        force_chat = detect_response_mode(question) == "chat"
        return _build_response(rows, question, office_id, session_id, base_url, force_chat=force_chat)
    finally:
        conn.close()


def _exec_hostel_room_by_trainee(slots, office_id, question, session_id, base_url):
    user_id = slots.get("user_id")
    stay_filter = slots.get("stay_filter", "all")
    if not user_id:
        return {"type": "text", "message": "Please specify which trainee you mean."}
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = """
            SELECT u.name AS trainee_name, u.user_code,
                   hb.building_name, hr.room_name, hm.in_date, hm.out_date,
                   hm.beds, hm.days,
                   CASE hm.h_status WHEN 1 THEN 'Active' ELSE 'Checked Out' END AS stay_status
            FROM hostel_masters hm
            JOIN users u ON u.id = hm.user_id
            JOIN hostel_buildings hb ON hb.id = hm.building_id
            JOIN hostel_rooms hr ON hr.id = hm.room_id
            WHERE hm.user_id = %s AND hm.office_id = %s
        """
        params = [user_id, office_id]
        if stay_filter == "current":
            sql += " AND hm.h_status = 1 AND (hm.out_date IS NULL OR hm.out_date >= CURDATE())"
        sql += " ORDER BY hm.in_date DESC LIMIT 20"
        cur.execute(sql, params)
        rows = cur.fetchall()
        return _build_response(rows, question, office_id, session_id, base_url, force_chat=True)
    finally:
        conn.close()


def _exec_hostel_trainees_by_room(slots, office_id, question, session_id, base_url):
    room_number = slots.get("room_number")
    room_id = slots.get("room_id")
    if not room_number and not room_id:
        return {"type": "text", "message": "Please specify a room number."}
    conn = get_connection()
    try:
        cur = conn.cursor()
        if room_id:
            sql = """
                SELECT u.name AS trainee_name, u.user_code, u.gender,
                       hb.building_name, hr.room_name, hm.in_date, hm.out_date, hm.beds
                FROM hostel_masters hm
                JOIN users u ON u.id = hm.user_id
                JOIN hostel_buildings hb ON hb.id = hm.building_id
                JOIN hostel_rooms hr ON hr.id = hm.room_id
                WHERE hm.room_id = %s AND hm.office_id = %s AND hm.h_status = 1
                  AND (hm.out_date IS NULL OR hm.out_date >= CURDATE())
                ORDER BY u.name
            """
            cur.execute(sql, [room_id, office_id])
        else:
            bfilter, bparams = _get_building_filter(slots)
            sql = f"""
                SELECT u.name AS trainee_name, u.user_code, u.gender,
                       hb.building_name, hr.room_name, hm.in_date, hm.out_date, hm.beds
                FROM hostel_masters hm
                JOIN users u ON u.id = hm.user_id
                JOIN hostel_buildings hb ON hb.id = hm.building_id
                JOIN hostel_rooms hr ON hr.id = hm.room_id
                WHERE hr.room_name = %s AND hm.office_id = %s AND hm.h_status = 1
                  AND (hm.out_date IS NULL OR hm.out_date >= CURDATE()){bfilter}
                ORDER BY u.name
            """
            cur.execute(sql, [room_number, office_id] + bparams)
        rows = cur.fetchall()
        force_chat = detect_response_mode(question) == "chat"
        return _build_response(rows, question, office_id, session_id, base_url, force_chat=force_chat)
    finally:
        conn.close()


def _exec_hostel_trainees_by_building(slots, office_id, question, session_id, base_url):
    conn = get_connection()
    try:
        cur = conn.cursor()
        bfilter, bparams = _get_building_filter(slots)

        count_sql = f"""
            SELECT COUNT(DISTINCT hm.user_id) AS cnt
            FROM hostel_masters hm
            JOIN hostel_buildings hb ON hb.id = hm.building_id
            WHERE hm.office_id = %s AND hm.h_status = 1
              AND (hm.out_date IS NULL OR hm.out_date >= CURDATE()){bfilter}
        """
        cur.execute(count_sql, [office_id] + bparams)
        total_count = cur.fetchone()["cnt"]

        sql = f"""
            SELECT u.name AS trainee_name, u.user_code, u.gender,
                   hb.building_name, hr.room_name, hm.in_date
            FROM hostel_masters hm
            JOIN users u ON u.id = hm.user_id
            JOIN hostel_buildings hb ON hb.id = hm.building_id
            JOIN hostel_rooms hr ON hr.id = hm.room_id
            WHERE hm.office_id = %s AND hm.h_status = 1
              AND (hm.out_date IS NULL OR hm.out_date >= CURDATE()){bfilter}
            ORDER BY hb.building_name, hr.room_name, u.name
            LIMIT 500
        """
        cur.execute(sql, [office_id] + bparams)
        rows = cur.fetchall()
        force_chat = detect_response_mode(question) == "chat"
        return _build_response(rows, question, office_id, session_id, base_url,
                               force_chat=force_chat, total_count=total_count)
    finally:
        conn.close()


def _exec_hostel_building_summary(slots, office_id, question, session_id, base_url):
    conn = get_connection()
    try:
        cur = conn.cursor()
        bfilter, bparams = _get_building_filter(slots)
        sql = f"""
            SELECT hb.building_name,
                   hb.bed_capacity AS building_capacity,
                   COUNT(hr.id) AS total_rooms,
                   SUM(hr.room_beds) AS total_beds,
                   COALESCE(occ.occupied_rooms, 0) AS occupied_rooms,
                   (COUNT(hr.id) - COALESCE(occ.occupied_rooms, 0)) AS available_rooms,
                   COALESCE(occ.occupied_beds, 0) AS occupied_beds,
                   (SUM(hr.room_beds) - COALESCE(occ.occupied_beds, 0)) AS available_beds
            FROM hostel_buildings hb
            LEFT JOIN hostel_rooms hr ON hr.building_id = hb.id AND hr.status = 1
            LEFT JOIN (
                SELECT hm.building_id,
                       COUNT(DISTINCT hm.room_id) AS occupied_rooms,
                       SUM(hm.beds) AS occupied_beds
                FROM hostel_masters hm
                WHERE hm.office_id = %s AND hm.h_status = 1
                  AND (hm.out_date IS NULL OR hm.out_date > NOW())
                GROUP BY hm.building_id
            ) occ ON occ.building_id = hb.id
            WHERE hb.office_id = %s AND hb.status = 1{bfilter}
            GROUP BY hb.id, hb.building_name, hb.bed_capacity, occ.occupied_rooms, occ.occupied_beds
            ORDER BY hb.building_name
        """
        cur.execute(sql, [office_id, office_id] + bparams)
        rows = cur.fetchall()
        
        force_chat = detect_response_mode(question) == "chat"
        if force_chat:
            total_rooms = sum(r["total_rooms"] for r in rows if r["total_rooms"])
            total_beds = sum(r["total_beds"] for r in rows if r["total_beds"])
            occ_beds = sum(r["occupied_beds"] for r in rows if r["occupied_beds"])
            avail_beds = sum(r["available_beds"] for r in rows if r["available_beds"])
            total_msg = f"Overall Summary: {occ_beds} occupied beds, {avail_beds} available beds (Total: {total_beds})."
            if not rows:
                return {"type": "text", "message": format_answer(question, total_msg)}
            formatted = _format_rows_for_chat(rows)
            return {"type": "text", "message": format_answer(question, f"{total_msg}\n\n{formatted}")}

        return _build_response(rows, question, office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_hostel_vacant_beds_by_building(slots, office_id, question, session_id, base_url):
    conn = get_connection()
    try:
        cur = conn.cursor()
        bfilter, bparams = _get_building_filter(slots)
        sql = f"""
            SELECT hb.building_name,
                   SUM(hr.room_beds) AS total_beds,
                   COALESCE(occ.occupied_beds, 0) AS occupied_beds,
                   (SUM(hr.room_beds) - COALESCE(occ.occupied_beds, 0)) AS vacant_beds
            FROM hostel_buildings hb
            LEFT JOIN hostel_rooms hr ON hr.building_id = hb.id AND hr.status = 1
            LEFT JOIN (
                SELECT hm.building_id, SUM(hm.beds) AS occupied_beds
                FROM hostel_masters hm
                WHERE hm.office_id = %s AND hm.h_status = 1
                  AND (hm.out_date IS NULL OR hm.out_date > NOW())
                GROUP BY hm.building_id
            ) occ ON occ.building_id = hb.id
            WHERE hb.office_id = %s AND hb.status = 1{bfilter}
            GROUP BY hb.id, hb.building_name, occ.occupied_beds
            ORDER BY vacant_beds DESC
        """
        cur.execute(sql, [office_id, office_id] + bparams)
        rows = cur.fetchall()
        
        force_chat = detect_response_mode(question) == "chat"
        if force_chat:
            total_beds = sum(r["total_beds"] for r in rows if r["total_beds"])
            vacant_beds = sum(r["vacant_beds"] for r in rows if r["vacant_beds"])
            total_msg = f"Overall: {vacant_beds} vacant beds across all queried buildings."
            if not rows:
                return {"type": "text", "message": format_answer(question, total_msg)}
            formatted = _format_rows_for_chat(rows, max_rows=20)
            return {"type": "text", "message": format_answer(question, f"{total_msg}\n\n{formatted}")}

        return _build_response(rows, question, office_id, session_id, base_url, force_chat=True)
    finally:
        conn.close()


def _exec_hostel_dues_by_trainee(slots, office_id, question, session_id, base_url):
    user_id = slots.get("user_id")
    if not user_id:
        return {"type": "text", "message": "Please specify which trainee you mean."}
    dues_status = slots.get("dues_status", "pending")
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = """
            SELECT u.name AS trainee_name, u.user_code,
                   hb.building_name, hr.room_name,
                   hm.total_charges, hm.amount AS paid_amount,
                   (hm.total_charges - hm.amount) AS due_amount,
                   hm.in_date, hm.out_date, hm.hostel_dues
            FROM hostel_masters hm
            JOIN users u ON u.id = hm.user_id
            JOIN hostel_buildings hb ON hb.id = hm.building_id
            JOIN hostel_rooms hr ON hr.id = hm.room_id
            WHERE hm.user_id = %s AND hm.office_id = %s
        """
        params = [user_id, office_id]
        if dues_status == "pending":
            sql += " AND hm.hostel_dues = 1"
        elif dues_status == "paid":
            sql += " AND (hm.hostel_dues = 0 OR hm.hostel_dues IS NULL)"
        sql += " ORDER BY hm.in_date DESC LIMIT 50"
        cur.execute(sql, params)
        rows = cur.fetchall()
        if not rows:
            return {"type": "text", "message": "No hostel dues records found for this trainee."}
        force_chat = detect_response_mode(question) == "chat"
        return _build_response(rows, question, office_id, session_id, base_url, force_chat=force_chat)
    finally:
        conn.close()



def _exec_hostel_allocation_summary(slots, office_id, question, session_id, base_url):
    conn = get_connection()
    try:
        cur = conn.cursor()
        bfilter, bparams = _get_building_filter(slots)
        sql = f"""
            SELECT hb.building_name,
                   COUNT(DISTINCT hm.user_id) AS trainees_staying,
                   COUNT(hm.id) AS total_allotments,
                   SUM(hm.beds) AS beds_used
            FROM hostel_masters hm
            JOIN hostel_buildings hb ON hb.id = hm.building_id
            WHERE hm.office_id = %s AND hm.h_status = 1
              AND (hm.out_date IS NULL OR hm.out_date >= CURDATE()){bfilter}
            GROUP BY hb.id, hb.building_name
            ORDER BY trainees_staying DESC
        """
        cur.execute(sql, [office_id] + bparams)
        rows = cur.fetchall()
        # Also get grand total
        total_sql = f"""
            SELECT COUNT(DISTINCT hm.user_id) AS total_trainees,
                   COUNT(hm.id) AS total_allotments
            FROM hostel_masters hm
            JOIN hostel_buildings hb ON hb.id = hm.building_id
            WHERE hm.office_id = %s AND hm.h_status = 1
              AND (hm.out_date IS NULL OR hm.out_date >= CURDATE()){bfilter}
        """
        cur.execute(total_sql, [office_id] + bparams)
        total_row = cur.fetchone()
        force_chat = detect_response_mode(question) == "chat"
        if force_chat and total_row:
            # For count questions, prepend total
            total_info = f"Total trainees staying in hostel: {total_row['total_trainees']}"
            if rows:
                formatted = _format_rows_for_chat(rows, max_rows=20)
                answer = format_answer(question, f"{total_info}\n\n{formatted}")
            else:
                answer = format_answer(question, total_info)
            return {"type": "text", "message": answer}
        return _build_response(rows, question, office_id, session_id, base_url, force_chat=force_chat)
    finally:
        conn.close()
