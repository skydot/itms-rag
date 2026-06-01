import re
from typing import Optional, Dict

MESS_FLOWS = {
    "mess_dues_by_trainee": {
        "flow_id": "mess_dues_by_trainee",
        "module": "mess",
        "slots_order": ["trainee_name", "user_id"],
        "requires_name": True
    },
    "mess_bill_summary": {
        "flow_id": "mess_bill_summary",
        "module": "mess",
        "slots_order": [],
        "requires_name": False
    },
    "pending_mess_dues": {
        "flow_id": "pending_mess_dues",
        "module": "mess",
        "slots_order": [],
        "requires_name": False
    },
    "mess_receipts_by_trainee": {
        "flow_id": "mess_receipts_by_trainee",
        "module": "mess",
        "slots_order": ["trainee_name", "user_id"],
        "requires_name": True
    },
    "mess_item_summary": {
        "flow_id": "mess_item_summary",
        "module": "mess",
        "slots_order": ["item_name", "item_id"],
        "requires_name": False
    },
    "mess_party_summary": {
        "flow_id": "mess_party_summary",
        "module": "mess",
        "slots_order": ["party_name", "party_id"],
        "requires_name": False
    },
    "mess_refund_summary": {
        "flow_id": "mess_refund_summary",
        "module": "mess",
        "slots_order": [],
        "requires_name": False
    },
    "mess_material_stock": {
        "flow_id": "mess_material_stock",
        "module": "mess",
        "slots_order": ["item_name", "item_id"],
        "requires_name": False
    },
    "mess_bill_count": {
        "flow_id": "mess_bill_count",
        "module": "mess",
        "slots_order": [],
        "requires_name": False
    },
    "recent_mess_transactions": {
        "flow_id": "recent_mess_transactions",
        "module": "mess",
        "slots_order": [],
        "requires_name": False
    }
}

def normalize_mess_message(message: str) -> str:
    text = message.lower().strip()
    text = re.sub(r"[?!.,;:\'\"()\[\]{}]", "", text)
    replacements = {
        r"\bmes\b": "mess",
        r"\bmesss\b": "mess",
        r"\bdue\b": "dues",
        r"\bduess\b": "dues",
        r"\bpendng\b": "pending",
        r"\bbil\b": "bill",
        r"\bbilll\b": "bill",
        r"\breciept\b": "receipt",
        r"\brecipt\b": "receipt",
        r"\bpaymnt\b": "payment",
        r"\bpyment\b": "payment",
        r"\brefnd\b": "refund",
        r"\bmatirial\b": "material",
        r"\bmateral\b": "material",
        r"\bstok\b": "stock",
        r"\bavilable\b": "available",
        r"\bavailble\b": "available",
        r"\btransction\b": "transaction",
    }
    for pat, repl in replacements.items():
        text = re.sub(pat, repl, text)
    return text

def detect_mess_guided_flow(message: str) -> Optional[Dict]:
    text = normalize_mess_message(message)
    slots = {
        "trainee_name": None,
        "user_id": None,
        "month": None,
        "year": None,
        "course_name": None,
        "course_id": None,
        "item_name": None,
        "item_id": None,
        "party_name": None,
        "party_id": None,
        "dues_status": "pending",
        "limit": None
    }

    has_mess_word = bool(re.search(r"\b(mess|messs|mes)\b", text))

    # Negative guards
    if re.search(r"\b(hostel|room|bed)\b.*dues", text) and not has_mess_word:
        return None
    if re.search(r"\b(library|book|books)\b.*dues", text) and not has_mess_word:
        return None
    if re.search(r"\b(marks|result|exam|pass|fail)\b", text) and not has_mess_word:
        return None
    if re.search(r"\b(attendance|present|absent)\b", text) and not has_mess_word:
        return None
    if re.search(r"\b(complaint|room|timetable|faculty)\b", text) and not has_mess_word:
        return None

    def _build_result(flow_id: str, reason: str) -> Dict:
        return {
            "flow_id": flow_id,
            "module": "mess",
            "slots": slots,
            "reason": reason
        }

    # Extract limit
    m_limit = re.search(r"\b(?:top|last)\s+(\d+)\b", text)
    if m_limit:
        slots["limit"] = int(m_limit.group(1))

    # ── mess_dues_by_trainee ──
    if re.search(r"mess dues\b|\bmess pending amount\b", text) and not re.search(r"\bhow many\b|\bshow pending\b|\blist\b|\btrainees with\b", text):
        m = re.search(r"([A-Za-z\s]+) mess dues|pending mess dues for ([A-Za-z\s]+)|does ([A-Za-z\s]+) have mess dues|([A-Za-z\s]+) mess pending amount", text)
        if m:
            extracted = m.group(1) or m.group(2) or m.group(3) or m.group(4)
            if extracted:
                clean_name = re.sub(r"\b(mess|dues|pending|amount|for|does|have|how|many)\b", "", extracted.lower()).strip()
                if clean_name:
                    slots["trainee_name"] = clean_name
        # Note: If no trainee_name is found, but the user explicitly specifies a trainee in "Mayank mess dues", we capture it.
        # Otherwise, if they just say "mess dues", we can still route to it and let the slots logic ask for trainee_name.
        if slots["trainee_name"]:
            return _build_result("mess_dues_by_trainee", "matched mess dues by trainee")
        elif "mess dues" in text and not re.search(r"pending mess dues", text):
            # Let it fall through or route
            pass

    # ── pending_mess_dues ──
    if re.search(r"\bpending mess dues\b|\bhow many mess dues\b|\bpending mess payment list\b|\btrainees with pending mess dues\b", text):
        return _build_result("pending_mess_dues", "matched pending mess dues")

    # ── mess_bill_summary ──
    if re.search(r"\bmess bill summary\b|\bmonthly mess bill\b|\bmess bill for\b|\bcourse wise mess bill\b", text):
        return _build_result("mess_bill_summary", "matched mess bill summary")

    # ── mess_receipts_by_trainee ──
    if re.search(r"\bmess receipts of\b|\bmess payment history of\b|\bmess paid bills\b", text):
        m = re.search(r"(?:mess receipts of|mess payment history of)\s+([A-Za-z\s]+)|([A-Za-z\s]+)\s+mess paid bills", text)
        if m:
            extracted = m.group(1) or m.group(2)
            if extracted:
                clean_name = re.sub(r"\b(mess|receipts|of|payment|history|paid|bills)\b", "", extracted.lower()).strip()
                if clean_name:
                    slots["trainee_name"] = clean_name
        return _build_result("mess_receipts_by_trainee", "matched mess receipts by trainee")

    # ── mess_item_summary ──
    if re.search(r"\bmess item summary\b|\bitem wise mess material\b|\bconsumption\b|\bmess material usage\b", text):
        m = re.search(r"([A-Za-z\s]+)\s+consumption|\bmess material\s+([A-Za-z\s]+)", text)
        if m:
            extracted = m.group(1) or m.group(2)
            if extracted:
                clean_item = re.sub(r"\b(mess|item|material|stock|available|price|consumption|usage)\b", "", extracted.lower()).strip()
                if clean_item:
                    slots["item_name"] = clean_item
        return _build_result("mess_item_summary", "matched mess item summary")

    # ── mess_party_summary ──
    if re.search(r"\bparty wise mess bills\b|\bvendor wise mess material\b|\bsupplier payments\b|\bparty payment summary\b|\bvendor\b|\bparty\b|\bsupplier\b", text) and has_mess_word:
        m = re.search(r"(?:vendor|party|supplier)\s+([A-Za-z\s]+)|([A-Za-z\s]+)\s+(?:vendor|party|supplier)", text)
        if m:
            extracted = m.group(1) or m.group(2)
            if extracted:
                clean_party = re.sub(r"\b(wise|mess|bills|material|payments|summary|vendor|party|supplier)\b", "", extracted.lower()).strip()
                if clean_party:
                    slots["party_name"] = clean_party
        return _build_result("mess_party_summary", "matched mess party summary")

    # ── mess_refund_summary ──
    if re.search(r"\bmess refund summary\b|\brefunds issued\b|\bmess refund\b", text):
        m = re.search(r"([A-Za-z\s]+)\s+mess refund|\bmess refund of\s+([A-Za-z\s]+)", text)
        if m:
            extracted = m.group(1) or m.group(2)
            if extracted:
                clean_name = re.sub(r"\b(mess|refund|of|summary|issued)\b", "", extracted.lower()).strip()
                if clean_name:
                    slots["trainee_name"] = clean_name
        return _build_result("mess_refund_summary", "matched mess refund summary")

    # ── mess_material_stock ──
    if re.search(r"\bmess material stock\b|\bavailable mess items\b|\bitem prices\b|\bmess stock report\b", text):
        m = re.search(r"([A-Za-z\s]+)\s+stock|available\s+([A-Za-z\s]+)|\bprice\s+([A-Za-z\s]+)", text)
        if m:
            extracted = m.group(1) or m.group(2) or m.group(3)
            if extracted:
                clean_item = re.sub(r"\b(mess|item|material|stock|available|prices|report)\b", "", extracted.lower()).strip()
                if clean_item:
                    slots["item_name"] = clean_item
        return _build_result("mess_material_stock", "matched mess material stock")

    # ── mess_bill_count ──
    if re.search(r"\bhow many mess bills\b|\btotal mess bills\b|\bmess bill count\b", text):
        return _build_result("mess_bill_count", "matched mess bill count")

    # ── recent_mess_transactions ──
    if re.search(r"\brecent mess transactions\b|\blast \d+ mess receipts\b|\blatest mess payments\b|\brecent mess bills\b", text):
        return _build_result("recent_mess_transactions", "matched recent mess transactions")

    # Catch-all for mess dues if trainee name is specified in a generic way
    if re.search(r"\bmess dues\b", text):
        return _build_result("mess_dues_by_trainee", "matched generic mess dues")

    return None
