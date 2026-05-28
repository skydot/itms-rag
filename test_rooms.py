from app.services.db_service import get_connection

conn = get_connection()
cur = conn.cursor()

# Query room ID 26
cur.execute("SELECT id as room_id, room_name, building_id FROM hostel_rooms WHERE id = 26")
print("Row with internal room_id = 26:")
print(cur.fetchall())

# Query room NAME '26'
cur.execute("SELECT id as room_id, room_name, building_id FROM hostel_rooms WHERE room_name = '26' AND building_id = 4")
print("\nRow with room_name = '26' in Geetanjali:")
print(cur.fetchall())

conn.close()
