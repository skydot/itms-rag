import requests
import json

base_url = "http://localhost:8000/api/chat"
headers = {"Content-Type": "application/json"}

queries = [
    "Search Python book",
    "Is Python book available?",
    "Books issued to Mayank",
    "Show overdue books",
    "Issue history of Python book",
    "How many books are in library?",
    "Book type wise count",
    "Most issued books",
    "Show recent book issues",
    "Books not returned yet",
    "Mayank marks",
    "Mayank hostel room"
]

for q in queries:
    payload = {"message": q, "role": "principal", "office_id": 1}
    resp = requests.post(base_url, headers=headers, json=payload).json()
    print(f"Q: {q}")
    if resp.get("type") == "follow_up":
        print(f"Flow: {resp.get('flow_id')} | Follow-up: {resp.get('message')}")
    else:
        msg = resp.get("message", "")[:200].replace("\n", " ")
        print(f"Answer: {msg}")
    print("-" * 50)
