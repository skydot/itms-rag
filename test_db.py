from app.services.db_service import get_connection

conn = get_connection()
cur = conn.cursor()

def show_table(t):
    try:
        cur.execute(f"DESCRIBE {t}")
        print(f"--- {t} ---")
        for r in cur.fetchall():
            print(f"{r['Field']} : {r['Type']}")
    except Exception as e:
        pass

for t in ['bills', 'bill_details', 'bill_receipts', 'bill_receipts_refund', 'mess_bill_format', 'mess_material', 'items', 'item_prices', 'partys']:
    show_table(t)

