from app.services.db_service import get_connection
conn = get_connection()
cur = conn.cursor()
cur.execute("SELECT hr.id, hr.building_id, hr.room_name, hr.room_beds, COUNT(hm.id) AS occupants FROM hostel_rooms hr LEFT JOIN hostel_masters hm ON hm.room_id = hr.id AND hm.h_status = 1 WHERE hr.building_id = (SELECT id FROM hostel_buildings WHERE building_name LIKE 'ARAVALI%' LIMIT 1) GROUP BY hr.id LIMIT 10;")
print(cur.fetchall())
