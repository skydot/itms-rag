"""Hostel occupancy and trainee query handlers."""


def execute(query_id, params, cur, office_id):
    p = params or {}

    if query_id == "HOSTEL_OCCUPANCY":
        cur.execute("""SELECT SUM(hr.room_beds) as cap,
            (SELECT COUNT(*) FROM hostel_masters hm WHERE hm.office_id=%s AND hm.h_status=1 AND hm.room_id IS NOT NULL) as occ
            FROM hostel_rooms hr WHERE hr.office_id=%s""", (office_id, office_id))
        r = cur.fetchone()
        if not r or not r["cap"]: return "No hostel capacity data."
        occ, cap = r["occ"] or 0, r["cap"]
        pct = round((occ/cap)*100, 2) if cap > 0 else 0
        return f"Hostel Occupancy: {pct}% ({occ} occupied / {cap} total beds)\nFree beds: {cap - occ}"

    elif query_id == "HOSTEL_CURRENT_STAYING_COUNT":
        cur.execute("""SELECT COUNT(*) AS currently_staying, SUM(hm.beds) AS beds_occupied
            FROM hostel_masters hm WHERE hm.office_id=%s AND hm.h_status=1
            AND (hm.out_date IS NULL OR hm.out_date > NOW())""", (office_id,))
        r = cur.fetchone()
        return f"Currently staying: {r['currently_staying'] or 0} trainees\nBeds occupied: {r['beds_occupied'] or 0}"

    elif query_id == "HOSTEL_OCCUPANCY_PER_BUILDING":
        cur.execute("""SELECT hb.building_name, hb.bed_capacity, COUNT(hm.id) AS trainees_staying,
            SUM(hm.beds) AS beds_used, (hb.bed_capacity - COALESCE(SUM(hm.beds),0)) AS beds_vacant
            FROM hostel_buildings hb LEFT JOIN hostel_masters hm ON hm.building_id=hb.id AND hm.office_id=%s
            AND hm.h_status=1 AND (hm.out_date IS NULL OR hm.out_date > NOW())
            WHERE hb.office_id=%s AND hb.status=1 GROUP BY hb.id, hb.building_name, hb.bed_capacity
            ORDER BY trainees_staying DESC""", (office_id, office_id))
        rows = cur.fetchall()
        if not rows: return "No occupancy data."
        lines = [f"- {r['building_name']}: {r['trainees_staying']} staying, {r['beds_used'] or 0} beds used, {r['beds_vacant'] or 0} vacant (cap: {r['bed_capacity'] or 0})" for r in rows]
        return "Occupancy per Building:\n" + "\n".join(lines)

    elif query_id == "HOSTEL_OCCUPANCY_PER_ROOM":
        bid = p.get("building_id")
        if not bid: return "Please specify building_id."
        cur.execute("""SELECT hr.room_name, hr.room_beds, COUNT(hm.id) AS trainees_in_room,
            SUM(hm.beds) AS beds_used, (hr.room_beds - COALESCE(SUM(hm.beds),0)) AS beds_vacant,
            IF(hr.ac='Y','AC','Non-AC') AS type FROM hostel_rooms hr
            LEFT JOIN hostel_masters hm ON hm.room_id=hr.id AND hm.h_status=1 AND (hm.out_date IS NULL OR hm.out_date > NOW())
            WHERE hr.building_id=%s AND hr.office_id=%s AND hr.status=1
            GROUP BY hr.id, hr.room_name, hr.room_beds ORDER BY beds_vacant DESC""", (bid, office_id))
        rows = cur.fetchall()
        if not rows: return f"No rooms in building {bid}."
        lines = [f"- {r['room_name']} [{r['type']}]: {r['trainees_in_room']} in room, {r['beds_used'] or 0}/{r['room_beds']} beds, {r['beds_vacant'] or 0} vacant" for r in rows]
        return f"Occupancy per Room ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_VACANT_ROOMS_NOW":
        cur.execute("""SELECT hr.room_name, hb.building_name, hr.room_beds, IF(hr.ac='Y','AC','Non-AC') AS type,
            CASE hr.floor WHEN 0 THEN 'Ground' ELSE CONCAT('Floor ',hr.floor) END AS floor
            FROM hostel_rooms hr JOIN hostel_buildings hb ON hb.id=hr.building_id
            WHERE hr.office_id=%s AND hr.status=1 AND hr.id NOT IN (
            SELECT room_id FROM hostel_masters WHERE h_status=1 AND (out_date IS NULL OR out_date > NOW()) AND office_id=%s)
            ORDER BY hb.building_name, hr.room_name""", (office_id, office_id))
        rows = cur.fetchall()
        if not rows: return "No vacant rooms right now."
        lines = [f"- {r['room_name']} | {r['building_name']} | {r['floor']} | {r['type']} | Beds: {r['room_beds']}" for r in rows]
        return f"Vacant Rooms ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_OCCUPANCY_PERCENTAGE":
        cur.execute("""SELECT SUM(hb.bed_capacity) AS total_capacity, COALESCE(SUM(occ.beds_used),0) AS beds_occupied,
            ROUND(COALESCE(SUM(occ.beds_used),0)*100.0/SUM(hb.bed_capacity),1) AS occupancy_pct
            FROM hostel_buildings hb LEFT JOIN (SELECT building_id, SUM(beds) AS beds_used FROM hostel_masters
            WHERE h_status=1 AND (out_date IS NULL OR out_date > NOW()) AND office_id=%s GROUP BY building_id) occ
            ON occ.building_id=hb.id WHERE hb.office_id=%s AND hb.status=1""", (office_id, office_id))
        r = cur.fetchone()
        if not r or not r["total_capacity"]: return "No capacity data."
        return f"Occupancy: {r['occupancy_pct'] or 0}%\nBeds Occupied: {r['beds_occupied']}\nTotal Capacity: {r['total_capacity']}"

    elif query_id == "HOSTEL_FULL_ROOMS":
        cur.execute("""SELECT hb.building_name, hr.room_name, hr.room_beds, COUNT(hm.id) as occ
            FROM hostel_rooms hr LEFT JOIN hostel_buildings hb ON hb.id=hr.building_id
            LEFT JOIN hostel_masters hm ON hm.room_id=hr.id AND hm.h_status=1
            WHERE hr.office_id=%s GROUP BY hr.id HAVING occ>=hr.room_beds AND hr.room_beds>0""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No fully occupied rooms."
        lines = [f"- {r['building_name']} Room {r['room_name']} ({r['occ']}/{r['room_beds']})" for r in rows]
        return f"Fully occupied rooms ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_AVAILABLE_ROOMS":
        gender = p.get("gender")
        gf = ""
        if gender and gender.lower() in ("female", "f", "ladies"):
            gf = " AND LOWER(hb.building_name) LIKE '%ladies%'"
        cur.execute(f"""SELECT hb.building_name, hr.room_name, hr.room_beds, COUNT(hm.id) as occ
            FROM hostel_rooms hr LEFT JOIN hostel_buildings hb ON hb.id=hr.building_id
            LEFT JOIN hostel_masters hm ON hm.room_id=hr.id AND hm.h_status=1
            WHERE hr.office_id=%s{gf} GROUP BY hr.id HAVING occ<hr.room_beds OR hr.room_beds IS NULL""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No available rooms."
        lines = [f"- {r['building_name']} Room {r['room_name']} (Free: {(r['room_beds'] or 0)-r['occ']})" for r in rows[:20]]
        return f"Available rooms ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_UNUSED_ROOMS":
        cur.execute("""SELECT hb.building_name, hr.room_name FROM hostel_rooms hr
            LEFT JOIN hostel_buildings hb ON hb.id=hr.building_id
            LEFT JOIN hostel_masters hm ON hm.room_id=hr.id AND hm.h_status=1
            WHERE hr.office_id=%s GROUP BY hr.id HAVING COUNT(hm.id)=0""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No unused rooms."
        lines = [f"- {r['building_name']} Room {r['room_name']}" for r in rows]
        return f"Unused rooms ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_OVERCROWDED_ROOMS":
        cur.execute("""SELECT hb.building_name, hr.room_name, hr.room_beds, COUNT(hm.id) as occ
            FROM hostel_rooms hr LEFT JOIN hostel_buildings hb ON hb.id=hr.building_id
            LEFT JOIN hostel_masters hm ON hm.room_id=hr.id AND hm.h_status=1
            WHERE hr.office_id=%s GROUP BY hr.id HAVING occ>hr.room_beds""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No overcrowded rooms."
        lines = [f"- {r['building_name']} Room {r['room_name']} ({r['occ']}/{r['room_beds']})" for r in rows]
        return "Overcrowded rooms:\n" + "\n".join(lines)

    elif query_id == "HOSTEL_LADIES_ROOMS":
        cur.execute("""SELECT hr.room_name, hr.room_beds, COUNT(hm.id) as occ
            FROM hostel_rooms hr LEFT JOIN hostel_buildings hb ON hb.id=hr.building_id
            LEFT JOIN hostel_masters hm ON hm.room_id=hr.id AND hm.h_status=1
            WHERE hr.office_id=%s AND LOWER(hb.building_name) LIKE '%%ladies%%' GROUP BY hr.id""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No ladies hostel data."
        total = len(rows)
        free = sum(1 for r in rows if (r["room_beds"] or 0) - r["occ"] > 0)
        return f"Ladies hostel: {total} rooms total, {free} with free beds"

    elif query_id == "HOSTEL_IS_TRAINEE_IN_HOSTEL":
        uid = p.get("user_id")
        if not uid: return "Please specify user_id."
        cur.execute("""SELECT hm.id, u.name, hb.building_name, hr.room_name, hm.in_date, hm.out_date, hm.beds, hm.days,
            CASE hm.h_status WHEN 1 THEN 'Staying' ELSE 'Checked Out' END AS status
            FROM hostel_masters hm JOIN users u ON u.id=hm.user_id JOIN hostel_buildings hb ON hb.id=hm.building_id
            JOIN hostel_rooms hr ON hr.id=hm.room_id WHERE hm.user_id=%s AND hm.office_id=%s
            ORDER BY hm.in_date DESC LIMIT 1""", (uid, office_id))
        r = cur.fetchone()
        if not r: return f"Trainee {uid} has no hostel record."
        return f"Trainee: {r['name']}\nBuilding: {r['building_name']}\nRoom: {r['room_name']}\nCheck-in: {r['in_date']}\nCheck-out: {r['out_date']}\nBeds: {r['beds']}\nDays: {r['days']}\nStatus: {r['status']}"

    elif query_id == "HOSTEL_TRAINEE_BUILDING_ROOM":
        uid = p.get("user_id")
        if not uid: return "Please specify user_id."
        cur.execute("""SELECT u.name, u.user_code, hb.building_name, hr.room_name, hm.beds, hm.in_date, hm.out_date
            FROM hostel_masters hm JOIN users u ON u.id=hm.user_id JOIN hostel_buildings hb ON hb.id=hm.building_id
            JOIN hostel_rooms hr ON hr.id=hm.room_id WHERE hm.user_id=%s AND hm.office_id=%s AND hm.h_status=1
            AND (hm.out_date IS NULL OR hm.out_date > NOW())""", (uid, office_id))
        r = cur.fetchone()
        if not r: return f"Trainee {uid} not currently in hostel."
        return f"{r['name']} ({r['user_code'] or 'N/A'})\nBuilding: {r['building_name']}\nRoom: {r['room_name']}\nBeds: {r['beds']}\nIn: {r['in_date']} | Out: {r['out_date']}"

    elif query_id == "HOSTEL_WHO_IN_ROOM":
        rid = p.get("room_id")
        if not rid: return "Please specify room_id."
        cur.execute("""SELECT u.name, u.user_code, u.mobile, u.designation, hm.in_date, hm.out_date, hm.beds, hm.days
            FROM hostel_masters hm JOIN users u ON u.id=hm.user_id
            WHERE hm.room_id=%s AND hm.office_id=%s AND hm.h_status=1 AND (hm.out_date IS NULL OR hm.out_date > NOW())
            ORDER BY u.name""", (rid, office_id))
        rows = cur.fetchall()
        if not rows: return f"No one in room {rid}."
        lines = [f"- {r['name']} ({r['user_code'] or 'N/A'}) | {r['mobile'] or 'N/A'} | In: {r['in_date']}" for r in rows]
        return f"Room {rid} Occupants ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_WHO_IN_BUILDING":
        bid = p.get("building_id")
        if not bid: return "Please specify building_id."
        cur.execute("""SELECT u.name, u.user_code, u.gender, u.mobile, hr.room_name, hm.in_date, hm.out_date, hm.beds
            FROM hostel_masters hm JOIN users u ON u.id=hm.user_id JOIN hostel_rooms hr ON hr.id=hm.room_id
            WHERE hm.building_id=%s AND hm.office_id=%s AND hm.h_status=1 AND (hm.out_date IS NULL OR hm.out_date > NOW())
            ORDER BY hr.room_name, u.name""", (bid, office_id))
        rows = cur.fetchall()
        if not rows: return f"No one in building {bid}."
        lines = [f"- {r['name']} | Room {r['room_name']} | {r['gender'] or 'N/A'} | In: {r['in_date']}" for r in rows]
        return f"Building {bid} Occupants ({len(rows)}):\n" + "\n".join(lines)


    elif query_id == "HOSTEL_ROOM_OCCUPANTS":
        room = p.get("room_name", "")
        if not room: return "Please specify a room name/number."
        cur.execute("""SELECT u.name FROM hostel_masters hm
            JOIN hostel_rooms hr ON hr.id=hm.room_id LEFT JOIN users u ON u.id=hm.user_id
            WHERE hm.office_id=%s AND hm.h_status=1 AND hr.room_name=%s AND u.name IS NOT NULL""", (office_id, room))
        rows = cur.fetchall()
        if not rows: return f"No occupants in room {room}."
        return f"Room {room} occupants:\n- " + "\n- ".join([r["name"] for r in rows])

    elif query_id == "HOSTEL_TRAINEES_NO_ROOM":
        cur.execute("""SELECT DISTINCT u.name FROM tra_masters tm
            JOIN users u ON u.id=tm.user_id LEFT JOIN hostel_masters hm ON hm.user_id=tm.user_id AND hm.h_status=1
            WHERE tm.office_id=%s AND hm.id IS NULL AND u.name IS NOT NULL""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "All trainees have rooms."
        lines = [f"- {r['name']}" for r in rows[:30]]
        res = f"Trainees without room ({len(rows)}):\n" + "\n".join(lines)
        if len(rows) > 30: res += "\n...and more."
        return res


    elif query_id == "HOSTEL_FULL_ALLOTMENT_LIST":
        # Get optional building filter
        bname = p.get("building_name", "")
        bid = None
        if bname:
            import difflib
            cur.execute("SELECT id, building_name FROM hostel_buildings WHERE office_id=%s AND status=1", (office_id,))
            buildings = cur.fetchall()
            matches = []
            for b in buildings:
                name_clean = b['building_name'].split('(')[0].strip().lower()
                ratio = difflib.SequenceMatcher(None, bname.lower(), name_clean).ratio()
                if bname.lower() in name_clean or ratio > 0.6:
                    matches.append((ratio, b))
            if matches:
                matches.sort(key=lambda x: x[0], reverse=True)
                bid = matches[0][1]['id']
        
        sql = """SELECT u.name, u.user_code, u.gender, u.designation, hb.building_name, hr.room_name,
            hm.in_date, hm.out_date, hm.days, hm.beds, IF(hm.food=1,'Yes','No') AS food, IF(hm.mess=1,'Yes','No') AS mess,
            tc.course_batch, c.course_name
            FROM hostel_masters hm JOIN users u ON u.id=hm.user_id JOIN hostel_buildings hb ON hb.id=hm.building_id
            JOIN hostel_rooms hr ON hr.id=hm.room_id
            LEFT JOIN training_calendars tc ON tc.id=hm.course_id
            LEFT JOIN courses c ON c.id=tc.ct_id
            WHERE hm.office_id=%s AND hm.h_status=1 AND (hm.out_date IS NULL OR hm.out_date > NOW())"""
        params = [office_id]
        if bid:
            sql += " AND hm.building_id=%s"
            params.append(bid)
        sql += " ORDER BY hb.building_name, hr.room_name, u.name"
        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
        if not rows: 
            if bname:
                return f"No current allotments in {bname}."
            return "No current allotments."
        lines = []
        for r in rows[:50]:
            course_info = f" | {r['course_batch'] or 'N/A'}: {r['course_name'] or 'N/A'}" if r['course_name'] else ""
            lines.append(f"- {r['name']} | {r['building_name']} Room {r['room_name']}{course_info} | In: {r['in_date'][:10]}")
        return f"Current Allotments ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_GENDER_WISE_OCCUPANCY":
        cur.execute("""SELECT u.gender, COUNT(hm.id) AS count, SUM(hm.beds) AS beds_used
            FROM hostel_masters hm JOIN users u ON u.id=hm.user_id
            WHERE hm.office_id=%s AND hm.h_status=1 AND (hm.out_date IS NULL OR hm.out_date > NOW())
            GROUP BY u.gender""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No occupancy data."
        lines = [f"- {r['gender'] or 'Unknown'}: {r['count']} trainees, {r['beds_used'] or 0} beds" for r in rows]
        return "Gender-wise Occupancy:\n" + "\n".join(lines)

    elif query_id == "HOSTEL_TRAINEES_FOR_COURSE":
        cid = p.get("course_id")
        if not cid: return "Please specify course_id."
        cur.execute("""SELECT u.name, u.user_code, u.designation, hb.building_name, hr.room_name, hm.in_date, hm.out_date, hm.beds
            FROM hostel_masters hm JOIN users u ON u.id=hm.user_id JOIN hostel_buildings hb ON hb.id=hm.building_id
            JOIN hostel_rooms hr ON hr.id=hm.room_id WHERE hm.course_id=%s AND hm.office_id=%s AND hm.h_status=1
            ORDER BY hb.building_name, hr.room_name""", (cid, office_id))
        rows = cur.fetchall()
        if not rows: return f"No hostel trainees for course {cid}."
        lines = [f"- {r['name']} | {r['building_name']} Room {r['room_name']} | In: {r['in_date']}" for r in rows]
        return f"Hostel Trainees for Course ({len(rows)}):\n" + "\n".join(lines)

    elif query_id in ("HOSTEL_SEARCH_TRAINEE_BY_NAME", "HOSTEL_TRAINEE_DETAILS"):
        name = p.get("search_name", "")
        if not name: return "Please specify a trainee name."
        cur.execute("""SELECT u.name, u.user_code, u.mobile, hb.building_name, hr.room_name, hm.in_date, hm.out_date,
            CASE hm.h_status WHEN 1 THEN 'Staying' ELSE 'Checked Out' END AS status
            FROM hostel_masters hm JOIN users u ON u.id=hm.user_id JOIN hostel_buildings hb ON hb.id=hm.building_id
            JOIN hostel_rooms hr ON hr.id=hm.room_id WHERE u.name LIKE %s AND hm.office_id=%s
            ORDER BY hm.in_date DESC""", (f"%{name}%", office_id))
        rows = cur.fetchall()
        if not rows: return f"No hostel records for '{name}'."
        lines = [f"- {r['name']}: {r['building_name']} Room {r['room_name']} | In: {r['in_date']} Out: {r['out_date']} | {r['status']}" for r in rows]
        return f"Hostel Details for '{name}':\n" + "\n".join(lines)

    elif query_id in ("HOSTEL_TRAINEES_STAYING", "HOSTEL_FIND_TRAINEE_ROOM"):
        uid = p.get("user_id")
        # Get optional building filter
        bname = p.get("building_name", "")
        bid = None
        if bname:
            import difflib
            cur.execute("SELECT id, building_name FROM hostel_buildings WHERE office_id=%s AND status=1", (office_id,))
            buildings = cur.fetchall()
            matches = []
            for b in buildings:
                name_clean = b['building_name'].split('(')[0].strip().lower()
                ratio = difflib.SequenceMatcher(None, bname.lower(), name_clean).ratio()
                if bname.lower() in name_clean or ratio > 0.6:
                    matches.append((ratio, b))
            if matches:
                matches.sort(key=lambda x: x[0], reverse=True)
                bid = matches[0][1]['id']
        
        if query_id == "HOSTEL_FIND_TRAINEE_ROOM" and uid:
            cur.execute("""SELECT u.name, hr.room_name, hb.building_name, hm.in_date, hm.out_date, hm.h_status
                FROM hostel_masters hm LEFT JOIN hostel_rooms hr ON hr.id=hm.room_id
                LEFT JOIN hostel_buildings hb ON hb.id=hm.building_id
                JOIN users u ON u.id=hm.user_id
                WHERE hm.office_id=%s AND hm.user_id=%s ORDER BY hm.id DESC LIMIT 1""", (office_id, uid))
            r = cur.fetchone()
            if not r: return f"No hostel record for user {uid}."
            return f"Trainee: {r['name']}\nBuilding: {r['building_name']}\nRoom: {r['room_name']}\nIn: {r['in_date']}\nOut: {r['out_date']}\nStatus: {'Active' if r['h_status']==1 else 'Inactive'}"
        else:
            # Query with building filter and course info
            sql = """SELECT u.name, u.user_code, u.gender, u.designation, 
                hb.building_name, hr.room_name, hm.in_date, hm.out_date, hm.beds,
                tc.course_batch, c.course_name
                FROM hostel_masters hm 
                JOIN users u ON u.id=hm.user_id 
                JOIN hostel_buildings hb ON hb.id=hm.building_id
                JOIN hostel_rooms hr ON hr.id=hm.room_id
                LEFT JOIN training_calendars tc ON tc.id=hm.course_id
                LEFT JOIN courses c ON c.id=tc.ct_id
                WHERE hm.office_id=%s AND hm.h_status=1 AND (hm.out_date IS NULL OR hm.out_date > NOW())"""
            params = [office_id]
            if bid:
                sql += " AND hm.building_id=%s"
                params.append(bid)
            sql += " ORDER BY hb.building_name, hr.room_name, u.name"
            cur.execute(sql, tuple(params))
            rows = cur.fetchall()
            if not rows: 
                if bname:
                    return f"No trainees currently staying in {bname}."
                return "No trainees currently staying."
            lines = []
            for r in rows[:50]:
                course_info = f" | {r['course_batch'] or 'N/A'}: {r['course_name'] or 'N/A'}" if r['course_name'] else ""
                lines.append(f"- {r['name']} | {r['building_name']} Room {r['room_name']}{course_info} | In: {r['in_date'][:10]}")
            return f"Trainees Staying ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_RECENT_CHECKINS":
        limit = int(p.get("limit", 10))
        cur.execute("""SELECT hm.in_date, u.name, hb.building_name, hr.room_name
            FROM hostel_masters hm JOIN users u ON u.id=hm.user_id JOIN hostel_buildings hb ON hb.id=hm.building_id
            JOIN hostel_rooms hr ON hr.id=hm.room_id WHERE hm.office_id=%s AND hm.h_status=1 AND hm.in_date IS NOT NULL
            ORDER BY hm.in_date DESC LIMIT %s""", (office_id, limit))
        rows = cur.fetchall()
        if not rows: return "No recent check-ins found."
        lines = [f"- {r['in_date']}: {r['name']} -> {r['building_name']} Room {r['room_name']}" for r in rows]
        return f"Recent {limit} check-ins:\n" + "\n".join(lines)

    return None
