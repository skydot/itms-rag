"""Hostel building, room, and basic occupancy handlers."""


def _find_building(cur, office_id, search_name):
    import difflib
    cur.execute("SELECT id, building_name FROM hostel_buildings WHERE office_id=%s AND status=1", (office_id,))
    buildings = cur.fetchall()
    matches = []
    for b in buildings:
        name = b['building_name'].split('(')[0].strip().lower()
        ratio = difflib.SequenceMatcher(None, search_name.lower(), name).ratio()
        if search_name.lower() in name or ratio > 0.6:
            matches.append((ratio, b))
    if matches:
        matches.sort(key=lambda x: x[0], reverse=True)
        return matches[0][1]
    return None

def execute(query_id, params, cur, office_id):
    p = params or {}

    if query_id == "HOSTEL_TOTAL_ROOMS":
        cur.execute("SELECT COUNT(*) as cnt FROM hostel_rooms WHERE office_id=%s AND status=1", (office_id,))
        r = cur.fetchone()
        return f"Total hostel rooms: {r['cnt'] if r else 0}"

    elif query_id == "HOSTEL_TOTAL_BEDS":
        cur.execute("SELECT SUM(room_beds) AS total_beds FROM hostel_rooms WHERE office_id=%s AND status=1", (office_id,))
        r = cur.fetchone()
        return f"Total beds/capacity: {r['total_beds'] or 0}"

    elif query_id == "HOSTEL_ACTIVE_BUILDINGS":
        cur.execute("SELECT id, building_name, bed_capacity, location FROM hostel_buildings WHERE office_id=%s AND status=1 ORDER BY sort_no, building_name", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No active buildings found."
        lines = [f"- {r['building_name']} (Capacity: {r['bed_capacity'] or 'N/A'}, Location: {r['location'] or 'N/A'})" for r in rows]
        return f"Active Buildings ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_ALL_BUILDINGS":
        cur.execute("SELECT id, building_name, bed_capacity, location, CASE status WHEN 1 THEN 'Active' ELSE 'Inactive' END AS status FROM hostel_buildings WHERE office_id=%s ORDER BY status DESC, building_name", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No buildings found."
        lines = [f"- {r['building_name']} [{r['status']}] (Capacity: {r['bed_capacity'] or 'N/A'})" for r in rows]
        return f"All Buildings ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_TOTAL_BED_CAPACITY":
        cur.execute("SELECT SUM(bed_capacity) AS total_bed_capacity, COUNT(*) AS total_buildings FROM hostel_buildings WHERE office_id=%s AND status=1", (office_id,))
        r = cur.fetchone()
        return f"Total bed capacity: {r['total_bed_capacity'] or 0} across {r['total_buildings'] or 0} buildings"

    elif query_id == "HOSTEL_BEDS_IN_SPECIFIC_BUILDING":
        bname = p.get("building_name") or p.get("hostel_name")
        if not bname: return "Please specify a building name."
        b = _find_building(cur, office_id, bname)
        if not b: return f"No building found matching '{bname}'."
        
        cur.execute("SELECT SUM(room_beds) AS total_beds FROM hostel_rooms WHERE office_id=%s AND building_id=%s AND status=1", (office_id, b['id']))
        r = cur.fetchone()
        return f"Total Beds in Building {b['building_name']}:\n- {r['total_beds'] or 0} beds"

    elif query_id == "HOSTEL_BED_CAPACITY_PER_BUILDING":
        cur.execute("SELECT building_name, bed_capacity, location FROM hostel_buildings WHERE office_id=%s AND status=1 ORDER BY bed_capacity DESC", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No building data."
        lines = [f"- {r['building_name']}: {r['bed_capacity'] or 0} beds ({r['location'] or 'N/A'})" for r in rows]
        return "Bed Capacity per Building:\n" + "\n".join(lines)

    elif query_id == "HOSTEL_BUILDING_DETAILS":
        bid = p.get("building_id")
        if not bid: return "Please specify building_id."
        cur.execute("""SELECT hb.id, hb.building_name, hb.bed_capacity, hb.location, hb.status,
            COUNT(hr.id) AS total_rooms, SUM(hr.room_beds) AS total_room_beds
            FROM hostel_buildings hb LEFT JOIN hostel_rooms hr ON hr.building_id=hb.id
            WHERE hb.id=%s AND hb.office_id=%s GROUP BY hb.id""", (bid, office_id))
        r = cur.fetchone()
        if not r: return f"Building {bid} not found."
        return f"Building: {r['building_name']}\nCapacity: {r['bed_capacity'] or 'N/A'}\nLocation: {r['location'] or 'N/A'}\nStatus: {'Active' if r['status']==1 else 'Inactive'}\nTotal Rooms: {r['total_rooms']}\nTotal Room Beds: {r['total_room_beds'] or 0}"

    elif query_id == "HOSTEL_ROOMS_IN_BUILDING":
        bid = p.get("building_id")
        if not bid: return "Please specify building_id."
        cur.execute("""SELECT hr.id, hr.room_name, hr.room_beds,
            CASE hr.floor WHEN 0 THEN 'Ground' ELSE CONCAT('Floor ',hr.floor) END AS floor,
            IF(hr.ac='Y','Yes','No') AS ac, IF(hr.toilet='Y','Yes','No') AS toilet, hr.status
            FROM hostel_rooms hr WHERE hr.building_id=%s AND hr.office_id=%s ORDER BY hr.floor, hr.sort_no""", (bid, office_id))
        rows = cur.fetchall()
        if not rows: return f"No rooms in building {bid}."
        lines = [f"- {r['room_name']} | {r['floor']} | Beds: {r['room_beds']} | AC: {r['ac']} | Toilet: {r['toilet']}" for r in rows]
        return f"Rooms in Building ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_ROOMS_BY_BUILDING_NAME":
        hname = p.get("building_name") or p.get("hostel_name", "")
        if hname:
            b = _find_building(cur, office_id, hname)
            if not b: return f"No building found matching '{hname}'."
            cur.execute("SELECT COUNT(id) AS total_rooms FROM hostel_rooms WHERE office_id=%s AND building_id=%s AND status=1", (office_id, b['id']))
            r = cur.fetchone()
            return f"Rooms by Building:\n- {b['building_name']}: {r['total_rooms']} rooms"
        else:
            cur.execute("""SELECT hb.building_name, COUNT(hr.id) AS total_rooms FROM hostel_buildings hb
                LEFT JOIN hostel_rooms hr ON hr.building_id=hb.id AND hr.office_id=hb.office_id
                WHERE hb.office_id=%s GROUP BY hb.id, hb.building_name""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No data found."
        lines = [f"- {r['building_name']}: {r['total_rooms']} rooms" for r in rows]
        return "Rooms by Building:\n" + "\n".join(lines)

    elif query_id == "HOSTEL_AC_ROOMS":
        cur.execute("""SELECT hr.room_name, hb.building_name,
            CASE hr.floor WHEN 0 THEN 'Ground' ELSE CONCAT('Floor ',hr.floor) END AS floor, hr.room_beds
            FROM hostel_rooms hr JOIN hostel_buildings hb ON hb.id=hr.building_id
            WHERE hr.office_id=%s AND hr.ac='Y' AND hr.status=1 ORDER BY hb.building_name, hr.room_name""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No AC rooms found."
        lines = [f"- {r['room_name']} | {r['building_name']} | {r['floor']} | Beds: {r['room_beds']}" for r in rows]
        return f"AC Rooms ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_ROOMS_WITH_TOILET":
        cur.execute("""SELECT hr.room_name, hb.building_name, hr.room_beds, IF(hr.ac='Y','AC','Non-AC') AS ac_type
            FROM hostel_rooms hr JOIN hostel_buildings hb ON hb.id=hr.building_id
            WHERE hr.office_id=%s AND hr.toilet='Y' AND hr.status=1""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No rooms with attached toilet."
        lines = [f"- {r['room_name']} | {r['building_name']} | {r['ac_type']} | Beds: {r['room_beds']}" for r in rows]
        return f"Rooms with Toilet ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_ROOMS_BY_FLOOR":
        floor = p.get("floor", 0)
        cur.execute("""SELECT hr.room_name, hb.building_name, hr.room_beds, IF(hr.ac='Y','AC','Non-AC') AS ac_type,
            IF(hr.toilet='Y','Yes','No') AS toilet FROM hostel_rooms hr
            JOIN hostel_buildings hb ON hb.id=hr.building_id
            WHERE hr.office_id=%s AND hr.floor=%s AND hr.status=1""", (office_id, floor))
        rows = cur.fetchall()
        fl = "Ground" if int(floor)==0 else f"Floor {floor}"
        if not rows: return f"No rooms on {fl}."
        lines = [f"- {r['room_name']} | {r['building_name']} | {r['ac_type']} | Toilet: {r['toilet']}" for r in rows]
        return f"Rooms on {fl} ({len(rows)}):\n" + "\n".join(lines)

    elif query_id == "HOSTEL_ROOM_SUMMARY_PER_BUILDING":
        cur.execute("""SELECT hb.building_name, COUNT(hr.id) AS total_rooms, SUM(hr.room_beds) AS total_beds,
            SUM(IF(hr.ac='Y',1,0)) AS ac_rooms, SUM(IF(hr.toilet='Y',1,0)) AS rooms_with_toilet
            FROM hostel_buildings hb LEFT JOIN hostel_rooms hr ON hr.building_id=hb.id AND hr.status=1
            WHERE hb.office_id=%s AND hb.status=1 GROUP BY hb.id, hb.building_name ORDER BY total_beds DESC""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No data."
        lines = [f"- {r['building_name']}: {r['total_rooms']} rooms, {r['total_beds'] or 0} beds, {r['ac_rooms']} AC, {r['rooms_with_toilet']} with toilet" for r in rows]
        return "Room Summary per Building:\n" + "\n".join(lines)

    elif query_id == "HOSTEL_OCCUPIED_ROOMS":
        cur.execute("SELECT COUNT(DISTINCT room_id) AS occupied_rooms FROM hostel_masters WHERE office_id=%s AND room_id IS NOT NULL AND h_status=1", (office_id,))
        r = cur.fetchone()
        return f"Occupied rooms: {r['occupied_rooms'] if r else 0}"

    elif query_id == "HOSTEL_AVAILABLE_ROOMS_BY_BUILDING":
        cur.execute("""SELECT hb.building_name, COUNT(hr.id) AS available_rooms FROM hostel_rooms hr
            JOIN hostel_buildings hb ON hb.id=hr.building_id WHERE hr.office_id=%s
            AND hr.id NOT IN (SELECT DISTINCT room_id FROM hostel_masters WHERE office_id=%s AND room_id IS NOT NULL AND h_status=1)
            GROUP BY hb.building_name""", (office_id, office_id))
        rows = cur.fetchall()
        if not rows: return "No available rooms."
        lines = [f"- {r['building_name']}: {r['available_rooms']} available" for r in rows]
        return "Available Rooms by Building:\n" + "\n".join(lines)

    elif query_id == "HOSTEL_OCCUPANCY_SUMMARY":
        cur.execute("""SELECT COUNT(DISTINCT hr.id) AS total_rooms, COUNT(DISTINCT hm.room_id) AS occupied_rooms,
            COUNT(DISTINCT hr.id)-COUNT(DISTINCT hm.room_id) AS available_rooms
            FROM hostel_rooms hr LEFT JOIN hostel_masters hm ON hm.room_id=hr.id AND hm.office_id=hr.office_id AND hm.h_status=1
            WHERE hr.office_id=%s""", (office_id,))
        r = cur.fetchone()
        if not r: return "No data."
        return f"Occupancy Summary:\nTotal Rooms: {r['total_rooms']}\nOccupied: {r['occupied_rooms']}\nAvailable: {r['available_rooms']}"

    elif query_id == "HOSTEL_FULL_ROOM_LIST_STATUS":
        cur.execute("""SELECT hr.room_name, hb.building_name, hr.room_beds,
            CASE WHEN hm.room_id IS NULL THEN 'Available' ELSE 'Occupied' END AS room_status
            FROM hostel_rooms hr LEFT JOIN hostel_buildings hb ON hb.id=hr.building_id
            LEFT JOIN hostel_masters hm ON hm.room_id=hr.id AND hm.office_id=hr.office_id AND hm.h_status=1
            WHERE hr.office_id=%s GROUP BY hr.id, hr.room_name, hb.building_name, hr.room_beds, hm.room_id""", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No rooms."
        lines = [f"- {r['room_name']} | {r['building_name']} | Beds: {r['room_beds']} | {r['room_status']}" for r in rows]
        return f"Room List ({len(rows)}):\n" + "\n".join(lines)

    return None
