from app.services.db_service import get_connection
conn = get_connection()
try:
    c = conn.cursor()
    c.execute("SELECT id, comp_name FROM complaint_cat WHERE status=1 AND cat_id=0")
    for r in c.fetchall():
        print(f"{r['id']}: {r['comp_name']}")
finally:
    conn.close()
