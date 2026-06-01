import requests

base_url = "http://localhost:8000/api/chat"
headers = {"Content-Type": "application/json"}

queries = [
    "Search all about roses book",
    "Find all about roses book",
    "Do we have all about roses book?",
    "Is all about roses book available?",
    "Available books on all about roses",
    "How many books are available?",
    "Books issued to Mayank",
    "Mayank library books",
    "Which books are issued to Mayank?",
    "Show overdue books",
    "How many books are overdue?",
    "Overdue books of Mayank",
    "Issue history of all about roses book",
    "Who borrowed all about roses book?",
    "How many books are in library?",
    "Total books",
    "Book type wise count",
    "Category wise books",
    "Most issued books",
    "Top 10 borrowed books",
    "Show recent book issues",
    "Last 10 book issues",
    "Books not returned yet",
    "Pending book returns",
    "Pending returns of Mayank"
]

print(f"Running {len(queries)} tests...\n")
for idx, q in enumerate(queries, 1):
    payload = {"message": q, "role": "principal", "office_id": 1}
    try:
        resp = requests.post(base_url, headers=headers, json=payload).json()
        print(f"[{idx}] Q: {q}")
        if resp.get("type") == "follow_up":
            flow = resp.get('flow_id')
            slot = resp.get('slot_key')
            opts = len(resp.get('options', []))
            print(f"    --> FLOW: {flow} | SLOT: {slot} | OPTIONS: {opts}")
        else:
            mode = resp.get("response_mode", "chat")
            if mode == "report":
                print(f"    --> REPORT GENERATED ({resp.get('row_count')} rows)")
            else:
                msg = resp.get("message", "").replace("\n", " ")[:150]
                print(f"    --> CHAT: {msg}")
    except Exception as e:
        print(f"[{idx}] Q: {q} --> ERROR: {e}")
print("\nDone.")
