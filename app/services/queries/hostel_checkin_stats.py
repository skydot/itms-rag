"""Hostel checkin/out, stats, financial, mess, and search handlers."""


def execute(query_id, params, cur, office_id):
    p = params or {}

    # --- Check-in/out ---
    if query_id == "HOSTEL_CHECKINS_TODAY":
        cur.execute("""SELECT u.name, u.user_code, hb.building_name, hr.room_name, hm.in_date, hm.beds
            FROM hostel_masters hm JOIN users u ON u.id=hm.user_id JOIN hostel_buildings hb ON hb.id=hm.building_id
            JOIN hostel_rooms hr ON hr.id=hm.room_id WHERE hm.office_id=%s AND DATE(hm.in_date)=CURDATE()
            ORDER BY hm.in_date""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No check-ins today."
        lines = [f"- {r['name']} ({r['user_code'] or 'N/A'}) -> {r['building_name']} Room {r['room_name']}" for r in rows]
        return f"Today's Check-ins ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_CHECKOUTS_TODAY":
        cur.execute("""SELECT u.name, u.user_code, hb.building_name, hr.room_name, hm.in_date, hm.out_date, hm.days
            FROM hostel_masters hm JOIN users u ON u.id=hm.user_id JOIN hostel_buildings hb ON hb.id=hm.building_id
            JOIN hostel_rooms hr ON hr.id=hm.room_id WHERE hm.office_id=%s AND DATE(hm.out_date)=CURDATE()
            ORDER BY hm.out_date""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No check-outs today."
        lines = [f"- {r['name']} | {r['building_name']} Room {r['room_name']} | {r['days']} days" for r in rows]
        return f"Today's Check-outs ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_CHECKOUTS_UPCOMING":
        days = int(p.get("days_ahead", 7))
        cur.execute("""SELECT u.name, u.user_code, hb.building_name, hr.room_name, hm.out_date,
            DATEDIFF(hm.out_date, NOW()) AS days_remaining
            FROM hostel_masters hm JOIN users u ON u.id=hm.user_id JOIN hostel_buildings hb ON hb.id=hm.building_id
            JOIN hostel_rooms hr ON hr.id=hm.room_id WHERE hm.office_id=%s AND hm.h_status=1
            AND hm.out_date BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL %s DAY) ORDER BY hm.out_date""", (office_id, days))
        rows = cur.fetchall()
        if not rows: return f"No check-outs in next {days} days."
        lines = [f"- {r['name']} | {r['building_name']} Room {r['room_name']} | Out: {r['out_date']} ({r['days_remaining']}d left)" for r in rows]
        return f"Upcoming Check-outs ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_TRAINEE_STAY_HISTORY":
        uid = p.get("user_id")
        if not uid: return "Please specify user_id."
        cur.execute("""SELECT hb.building_name, hr.room_name, hm.in_date, hm.out_date, hm.days, hm.beds, hm.total_charges,
            CASE hm.h_status WHEN 1 THEN 'Staying' ELSE 'Checked Out' END AS status
            FROM hostel_masters hm JOIN hostel_buildings hb ON hb.id=hm.building_id
            JOIN hostel_rooms hr ON hr.id=hm.room_id WHERE hm.user_id=%s AND hm.office_id=%s
            ORDER BY hm.in_date DESC""", (uid, office_id))
        rows = cur.fetchall()
        if not rows: return f"No stay history for user {uid}."
        lines = [f"- {r['building_name']} Room {r['room_name']} | {r['in_date']} to {r['out_date']} | {r['days']}d | Charges: {r['total_charges'] or 0} | {r['status']}" for r in rows]
        return f"Stay History ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_CHECKINS_DATE_RANGE":
        fd = p.get("from_date")
        td = p.get("to_date")
        if not fd or not td: return "Please specify from_date and to_date."
        cur.execute("""SELECT u.name, u.user_code, hb.building_name, hr.room_name, hm.in_date, hm.out_date, hm.days
            FROM hostel_masters hm JOIN users u ON u.id=hm.user_id JOIN hostel_buildings hb ON hb.id=hm.building_id
            JOIN hostel_rooms hr ON hr.id=hm.room_id WHERE hm.office_id=%s AND hm.in_date BETWEEN %s AND %s
            ORDER BY hm.in_date""", (office_id, fd, td))
        rows = cur.fetchall()
        if not rows: return f"No check-ins between {fd} and {td}."
        lines = [f"- {r['name']} | {r['building_name']} Room {r['room_name']} | In: {r['in_date']}" for r in rows[:50]]
        return f"Check-ins {fd} to {td} ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_OVERSTAY":
        cur.execute("""SELECT u.name, u.mobile, hb.building_name, hr.room_name, hm.out_date,
            DATEDIFF(NOW(), hm.out_date) AS days_overdue
            FROM hostel_masters hm JOIN users u ON u.id=hm.user_id JOIN hostel_buildings hb ON hb.id=hm.building_id
            JOIN hostel_rooms hr ON hr.id=hm.room_id WHERE hm.office_id=%s AND hm.h_status=1 AND hm.out_date < NOW()
            ORDER BY days_overdue DESC""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No overstaying trainees."
        lines = [f"- {r['name']} ({r['mobile'] or 'N/A'}) | {r['building_name']} Room {r['room_name']} | {r['days_overdue']}d overdue" for r in rows]
        return f"Overstaying Trainees ({len(rows)}):\n" + "\n".join(lines)

    # --- Stats ---
    elif query_id == "HOSTEL_MONTHLY_CHECKINS":
        year = p.get("year")
        if not year:
            cur.execute("SELECT YEAR(CURDATE()) AS y")
            year = cur.fetchone().get("y", 2025)
        cur.execute("""SELECT MONTH(hm.in_date) AS month_no, MONTHNAME(hm.in_date) AS month,
            COUNT(*) AS checkins, SUM(hm.days) AS total_days_stayed
            FROM hostel_masters hm WHERE hm.office_id=%s AND YEAR(hm.in_date)=%s
            GROUP BY MONTH(hm.in_date) ORDER BY month_no""", (office_id, year))
        rows = cur.fetchall()
        if not rows: return f"No check-in data for {year}."
        lines = [f"- {r['month']}: {r['checkins']} check-ins, {r['total_days_stayed'] or 0} total days" for r in rows]
        return f"Monthly Check-ins ({year}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_COURSE_WISE_OCCUPANCY":
        cur.execute("""SELECT c.course_name, COUNT(hm.id) AS trainees, SUM(hm.beds) AS beds_used
            FROM hostel_masters hm JOIN courses c ON c.id=hm.course_id
            WHERE hm.office_id=%s AND hm.h_status=1 AND (hm.out_date IS NULL OR hm.out_date > NOW())
            GROUP BY hm.course_id, c.course_name ORDER BY trainees DESC""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No course-wise data."
        lines = [f"- {r['course_name']}: {r['trainees']} trainees, {r['beds_used'] or 0} beds" for r in rows]
        return "Course-wise Occupancy:\n" + "\n".join(lines)

    elif query_id == "HOSTEL_AVG_STAY_PER_BUILDING":
        cur.execute("""SELECT hb.building_name, COUNT(hm.id) AS total_allotments,
            ROUND(AVG(hm.days),1) AS avg_stay_days, MAX(hm.days) AS max_stay_days
            FROM hostel_masters hm JOIN hostel_buildings hb ON hb.id=hm.building_id
            WHERE hm.office_id=%s GROUP BY hm.building_id, hb.building_name ORDER BY avg_stay_days DESC""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No stay data."
        lines = [f"- {r['building_name']}: Avg {r['avg_stay_days']}d, Max {r['max_stay_days']}d ({r['total_allotments']} allotments)" for r in rows]
        return "Avg Stay per Building:\n" + "\n".join(lines)

    elif query_id == "HOSTEL_PH_TRAINEES":
        cur.execute("""SELECT u.name, u.user_code, hb.building_name, hr.room_name, hm.in_date, hm.out_date
            FROM hostel_masters hm JOIN users u ON u.id=hm.user_id JOIN hostel_buildings hb ON hb.id=hm.building_id
            JOIN hostel_rooms hr ON hr.id=hm.room_id WHERE hm.office_id=%s AND hm.ph=1 AND hm.h_status=1""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No PH trainees in hostel."
        lines = [f"- {r['name']} | {r['building_name']} Room {r['room_name']}" for r in rows]
        return f"PH Trainees ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_COMPLAINTS_COUNT":
        cur.execute("SELECT COUNT(*) AS total_complaints FROM hostel_complaint WHERE office_id=%s", (office_id,))
        r = cur.fetchone()
        return f"Total complaints: {r['total_complaints'] if r else 0}"

    elif query_id == "HOSTEL_PENDING_COMPLAINTS":
        cur.execute("""SELECT hb.building_name, hc.description FROM hostel_complaint hc
            LEFT JOIN hostel_buildings hb ON hb.id=hc.building_id WHERE hc.office_id=%s AND hc.status!=1""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No pending complaints."
        lines = [f"- {r['building_name'] or 'Unknown'}: {r['description']}" for r in rows]
        return f"Pending complaints ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_COMPLAINTS_BY_STATUS":
        cur.execute("SELECT status, COUNT(*) AS total FROM hostel_complaint WHERE office_id=%s GROUP BY status", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No complaint data."
        lines = [f"- Status {r['status']}: {r['total']}" for r in rows]
        return "Complaints by Status:\n" + "\n".join(lines)

    elif query_id == "HOSTEL_MOST_COMPLAINTS":
        cur.execute("""SELECT hb.building_name, COUNT(hc.id) as cnt FROM hostel_complaint hc
            LEFT JOIN hostel_buildings hb ON hb.id=hc.building_id GROUP BY hc.building_id ORDER BY cnt DESC LIMIT 1""")
        r = cur.fetchone()
        if not r: return "No complaint data."
        return f"Most complaints: {r['building_name'] or 'Unknown'} ({r['cnt']} complaints)"

    # --- Financial ---
    elif query_id == "HOSTEL_TOTAL_REVENUE":
        cur.execute("""SELECT SUM(hm.total_charges) AS total_revenue, SUM(hm.charge) AS total_daily_charges,
            COUNT(hm.id) AS total_allotments FROM hostel_masters hm WHERE hm.office_id=%s""", (office_id,))
        r = cur.fetchone()
        return f"Total Revenue: {r['total_revenue'] or 0}\nDaily Charges: {r['total_daily_charges'] or 0}\nTotal Allotments: {r['total_allotments'] or 0}"

    elif query_id == "HOSTEL_DUES_PENDING":
        cur.execute("""SELECT u.name, u.user_code, u.mobile, hb.building_name, hr.room_name,
            hm.total_charges, hm.amount, (hm.total_charges - hm.amount) AS due_amount
            FROM hostel_masters hm JOIN users u ON u.id=hm.user_id JOIN hostel_buildings hb ON hb.id=hm.building_id
            JOIN hostel_rooms hr ON hr.id=hm.room_id WHERE hm.office_id=%s AND hm.hostel_dues=1
            ORDER BY due_amount DESC""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No pending dues."
        lines = [f"- {r['name']}: Due ₹{r['due_amount'] or 0} | {r['building_name']} Room {r['room_name']}" for r in rows]
        return f"Dues Pending ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_TRAINEE_CHARGES":
        uid = p.get("user_id")
        if not uid: return "Please specify user_id."
        cur.execute("""SELECT hm.in_date, hm.out_date, hm.days, hm.beds, hm.charge AS daily_charge,
            hm.total_charges, hm.amount AS paid, (hm.total_charges - hm.amount) AS balance, hm.receipt_no
            FROM hostel_masters hm WHERE hm.user_id=%s AND hm.office_id=%s ORDER BY hm.in_date DESC""", (uid, office_id))
        rows = cur.fetchall()
        if not rows: return f"No charges for user {uid}."
        lines = [f"- {r['in_date']} to {r['out_date']} | {r['days']}d | Charge: {r['total_charges'] or 0} | Paid: {r['paid'] or 0} | Balance: {r['balance'] or 0} | Receipt: {r['receipt_no'] or 'N/A'}" for r in rows]
        return f"Charges for User {uid}:\n" + "\n".join(lines)

    elif query_id == "HOSTEL_REVENUE_PER_BUILDING":
        cur.execute("""SELECT hb.building_name, COUNT(hm.id) AS total_stays, SUM(hm.total_charges) AS total_revenue,
            SUM(hm.amount) AS amount_collected, SUM(hm.total_charges - hm.amount) AS pending
            FROM hostel_masters hm JOIN hostel_buildings hb ON hb.id=hm.building_id
            WHERE hm.office_id=%s GROUP BY hm.building_id, hb.building_name ORDER BY total_revenue DESC""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No revenue data."
        lines = [f"- {r['building_name']}: Revenue ₹{r['total_revenue'] or 0} | Collected ₹{r['amount_collected'] or 0} | Pending ₹{r['pending'] or 0}" for r in rows]
        return "Revenue per Building:\n" + "\n".join(lines)

    # --- Mess ---
    elif query_id == "HOSTEL_MESS_TRAINEES":
        cur.execute("""SELECT u.name, u.user_code, hb.building_name, hr.room_name, hm.in_date, hm.out_date
            FROM hostel_masters hm JOIN users u ON u.id=hm.user_id JOIN hostel_buildings hb ON hb.id=hm.building_id
            JOIN hostel_rooms hr ON hr.id=hm.room_id WHERE hm.office_id=%s AND hm.mess=1 AND hm.h_status=1
            AND (hm.out_date IS NULL OR hm.out_date > NOW()) ORDER BY hb.building_name""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No trainees opted for mess."
        lines = [f"- {r['name']} | {r['building_name']} Room {r['room_name']}" for r in rows]
        return f"Mess Trainees ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_MESS_COUNT_PER_BUILDING":
        cur.execute("""SELECT hb.building_name, SUM(IF(hm.mess=1,1,0)) AS mess_count,
            SUM(IF(hm.food=1,1,0)) AS food_count, COUNT(hm.id) AS total_trainees
            FROM hostel_masters hm JOIN hostel_buildings hb ON hb.id=hm.building_id
            WHERE hm.office_id=%s AND hm.h_status=1 AND (hm.out_date IS NULL OR hm.out_date > NOW())
            GROUP BY hm.building_id, hb.building_name""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No mess data."
        lines = [f"- {r['building_name']}: Mess {r['mess_count']}, Food {r['food_count']}, Total {r['total_trainees']}" for r in rows]
        return "Mess Count per Building:\n" + "\n".join(lines)

    elif query_id == "HOSTEL_TOTAL_MESS_STRENGTH":
        cur.execute("""SELECT COUNT(*) AS total_staying, SUM(IF(hm.mess=1,1,0)) AS mess_opted,
            SUM(IF(hm.food=1,1,0)) AS food_opted FROM hostel_masters hm
            WHERE hm.office_id=%s AND hm.h_status=1 AND (hm.out_date IS NULL OR hm.out_date > NOW())""", (office_id,))
        r = cur.fetchone()
        return f"Total Staying: {r['total_staying'] or 0}\nMess Opted: {r['mess_opted'] or 0}\nFood Opted: {r['food_opted'] or 0}"

    # --- Search ---
    elif query_id == "HOSTEL_FIND_BY_RECEIPT":
        rno = p.get("receipt_no")
        if not rno: return "Please specify receipt_no."
        cur.execute("""SELECT u.name, u.user_code, hb.building_name, hr.room_name, hm.in_date, hm.out_date,
            hm.total_charges, hm.receipt_no FROM hostel_masters hm JOIN users u ON u.id=hm.user_id
            JOIN hostel_buildings hb ON hb.id=hm.building_id JOIN hostel_rooms hr ON hr.id=hm.room_id
            WHERE hm.receipt_no=%s AND hm.office_id=%s""", (rno, office_id))
        r = cur.fetchone()
        if not r: return f"No record for receipt {rno}."
        return f"Receipt {rno}:\n{r['name']} ({r['user_code'] or 'N/A'})\n{r['building_name']} Room {r['room_name']}\nIn: {r['in_date']} Out: {r['out_date']}\nCharges: {r['total_charges'] or 0}"

    elif query_id == "HOSTEL_FIND_BY_ALLOTMENT_ID":
        hid = p.get("hm_id")
        if not hid: return "Please specify hm_id."
        cur.execute("""SELECT hm.*, u.name, u.user_code, u.mobile, hb.building_name, hr.room_name
            FROM hostel_masters hm JOIN users u ON u.id=hm.user_id JOIN hostel_buildings hb ON hb.id=hm.building_id
            JOIN hostel_rooms hr ON hr.id=hm.room_id WHERE hm.id=%s""", (hid,))
        r = cur.fetchone()
        if not r: return f"No allotment with ID {hid}."
        return f"Allotment {hid}:\n{r['name']} ({r['user_code'] or 'N/A'}) | Mobile: {r['mobile'] or 'N/A'}\n{r['building_name']} Room {r['room_name']}\nIn: {r['in_date']} Out: {r['out_date']}"

    elif query_id == "HOSTEL_EXTRA_ROOM_ALLOTMENTS":
        cur.execute("""SELECT u.name, u.user_code, hb.building_name, hr.room_name, hm.in_date, hm.out_date
            FROM hostel_masters hm JOIN users u ON u.id=hm.user_id JOIN hostel_buildings hb ON hb.id=hm.building_id
            JOIN hostel_rooms hr ON hr.id=hm.room_id WHERE hm.office_id=%s AND hm.extra_room=1 AND hm.h_status=1""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No extra room allotments."
        lines = [f"- {r['name']} | {r['building_name']} Room {r['room_name']}" for r in rows]
        return f"Extra Room Allotments ({len(rows)}):\n" + "\n".join(lines)

    return None
