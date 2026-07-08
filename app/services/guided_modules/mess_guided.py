import re
from typing import Optional, Dict

MESS_FLOWS = {
    "mess_dues_by_trainee": {
        "flow_id": "mess_dues_by_trainee",
        "module": "mess",
        "slots_order": ["trainee_name", "user_id"],
        "requires_name": True
    },
    "mess_receipt_report": {
        "flow_id": "mess_receipt_report",
        "module": "mess",
        "slots_order": ["course_id", "user_id", "from_date", "to_date"],
        "requires_name": False
    },
    "mess_gst_report": {
        "flow_id": "mess_gst_report",
        "module": "mess",
        "slots_order": ["from_date", "to_date"],
        "requires_name": False
    },
    "mess_bill_summary": {
        "flow_id": "mess_bill_summary",
        "module": "mess",
        "slots_order": ["month", "year", "course_id"],
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
        "slots_order": [],
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
    },
    "mess_rate_card": {
        "flow_id": "mess_rate_card",
        "module": "mess",
        "slots_order": [],
        "requires_name": False
    },
    "mess_item_rate": {
        "flow_id": "mess_item_rate",
        "module": "mess",
        "slots_order": ["meal_item_name"],
        "requires_name": False
    }
}

# ── Month name → number mapping ──
_MONTH_MAP = {
    "january": 1, "jan": 1,
    "february": 2, "feb": 2,
    "march": 3, "mar": 3,
    "april": 4, "apr": 4,
    "may": 5,
    "june": 6, "jun": 6,
    "july": 7, "jul": 7,
    "august": 8, "aug": 8,
    "september": 9, "sep": 9, "sept": 9,
    "october": 10, "oct": 10,
    "november": 11, "nov": 11,
    "december": 12, "dec": 12,
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
        r"\brecipts\b": "receipts",
        r"\breciepts\b": "receipts",
        r"\brecipt\b": "receipt",
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
        r"\bconsumtion\b": "consumption",
        r"\bbreakfst\b": "breakfast",
        r"\bbreakfast\b": "breakfast",
        r"\blnch\b": "lunch",
        r"\bdinnr\b": "dinner",
        r"\bdinr\b": "dinner",
        r"\bchargs\b": "charges",
        r"\bcharges\b": "charges",
    }
    for pat, repl in replacements.items():
        text = re.sub(pat, repl, text)
    return text


def _extract_month_year(text: str) -> tuple:
    """Extract month (as int) and year (as int) from text."""
    month = None
    year = None

    # "May 2025", "jan 2024", "december"
    m = re.search(r"\b(january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|sept|october|oct|november|nov|december|dec)\s*(\d{4})?\b", text)
    if m:
        month_str = m.group(1).lower()
        month = _MONTH_MAP.get(month_str)
        if m.group(2):
            year = int(m.group(2))

    # "this month" / "last month"
    if not month:
        from datetime import datetime, timedelta
        if "this month" in text:
            now = datetime.now()
            month = now.month
            year = year or now.year
        elif "last month" in text:
            now = datetime.now()
            last = now.replace(day=1) - timedelta(days=1)
            month = last.month
            year = year or last.year

    # standalone year "2025"
    if not year:
        y = re.search(r"\b(20\d{2})\b", text)
        if y:
            year = int(y.group(1))

    return month, year


def _extract_dues_status(text: str) -> str:
    """Extract dues status from text. Default: pending."""
    if re.search(r"\b(paid|cleared)\b", text):
        return "paid"
    if re.search(r"\ball\b", text):
        return "all"
    return "pending"


def detect_mess_guided_flow(message: str) -> Optional[Dict]:
    text = normalize_mess_message(message)
    print(f"[Mess Guided] Message: {message}")

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
        "dues_status": None,
        "limit": None,
        "meal_item_name": None
    }

    has_mess_word = bool(re.search(r"\b(mess|messs|mes)\b", text))

    # ── Negative guards ──
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
        print(f"[Mess Guided] Flow: {flow_id}")
        print(f"[Mess Guided] Slots: {slots}")
        return {
            "flow_id": flow_id,
            "module": "mess",
            "slots": slots,
            "reason": reason
        }

    # ── Extract common slots ──
    # limit
    m_limit = re.search(r"\b(?:top|last)\s+(\d+)\b", text)
    if m_limit:
        slots["limit"] = int(m_limit.group(1))

    # month/year
    month, year = _extract_month_year(text)
    if month:
        slots["month"] = month
    if year:
        slots["year"] = year

    # dues status
    slots["dues_status"] = _extract_dues_status(text)

    # ── mess_rate_card / mess_item_rate (check EARLY — before bill/stock patterns) ──
    _MEAL_ITEMS = ["breakfast", "lunch", "dinner", "full day meal", "full day", "hq administration", "administration charges", "gio"]
    has_rate_word = bool(re.search(r"\b(rate|rates|price|prices|charge|charges|cost|tariff)\b", text))
    has_meal_word = any(m in text for m in _MEAL_ITEMS)

    if has_rate_word and (has_mess_word or has_meal_word):
        # Check for specific meal item
        matched_meal = None
        for meal in _MEAL_ITEMS:
            if meal in text:
                matched_meal = meal
                break
        if matched_meal:
            slots["meal_item_name"] = matched_meal
            return _build_result("mess_item_rate", "matched specific meal item rate")
        else:
            return _build_result("mess_rate_card", "matched mess rate card")

    # "mess rate card" / "current mess rates" / "what are mess charges" / "mess charges"
    if re.search(r"\bmess rate card\b|\bcurrent mess rates\b|\bmess rates\b|\bmess charges\b|\bmess tariff\b", text):
        return _build_result("mess_rate_card", "matched mess rate card")

    # "what is lunch rate" / "breakfast price" / "dinner cost" without explicit "mess"
    if has_meal_word and has_rate_word:
        matched_meal = None
        for meal in _MEAL_ITEMS:
            if meal in text:
                matched_meal = meal
                break
        if matched_meal:
            slots["meal_item_name"] = matched_meal
            return _build_result("mess_item_rate", "matched meal item rate")

    # ── recent_mess_transactions (check early — "recent/last/latest" patterns) ──
    if re.search(r"\brecent mess transactions\b|\blast \d+ mess receipts\b|\blatest mess payments\b|\brecent mess bills\b|\blast \d+ mess payments\b|\blast \d+ mess bills\b|\blast \d+ mess transactions\b|\blatest mess receipts\b|\blatest mess transactions\b|\brecent mess receipts\b|\brecent mess payments\b", text):
        return _build_result("recent_mess_transactions", "matched recent mess transactions")

    # ── mess_bill_count (check before bill summary) ──
    if re.search(r"\bhow many mess bills\b|\btotal mess bills\b|\bmess bill count\b", text):
        return _build_result("mess_bill_count", "matched mess bill count")

    # ── mess_gst_report ──
    if re.search(r"\bmess gst\b|\bgst report\b|\btaxable amount\b|\bmess tax\b", text):
        return _build_result("mess_gst_report", "matched mess gst report")

    # ── mess_receipt_report ──
    if re.search(r"\breceipt report\b|\bmess receipt report\b|\bcollection report\b|\bdetailed receipt report\b", text):
        return _build_result("mess_receipt_report", "matched mess receipt report")

    # ── mess_dues_by_trainee ──
    if re.search(r"mess dues\b|\bmess pending amount\b", text) and not re.search(r"\bhow many\b|\bshow pending\b|\blist\b|\btrainees with\b", text):
        m = re.search(r"([A-Za-z\s]+) mess dues|pending mess dues for ([A-Za-z\s]+)|does ([A-Za-z\s]+) have mess dues|([A-Za-z\s]+) mess pending amount", text)
        if m:
            extracted = m.group(1) or m.group(2) or m.group(3) or m.group(4)
            if extracted:
                clean_name = re.sub(r"\b(mess|dues|pending|amount|for|does|have|how|many|of)\b", "", extracted.lower()).strip()
                if clean_name:
                    slots["trainee_name"] = clean_name
        if slots["trainee_name"]:
            return _build_result("mess_dues_by_trainee", "matched mess dues by trainee")
        elif "mess dues" in text and not re.search(r"pending mess dues", text):
            # Generic "mess dues" without trainee — still route here
            pass

    # ── pending_mess_dues ──
    if re.search(r"\bpending mess dues\b|\bhow many mess dues\b|\bpending mess payment list\b|\btrainees with pending mess dues\b|\bpending mess payment\b|\bmess dues are pending\b|\bpending mess\b", text):
        return _build_result("pending_mess_dues", "matched pending mess dues")

    # ── mess_bill_summary ──
    if re.search(r"\bmess bill summary\b|\bmonthly mess bill\b|\bmess bill for\b|\bcourse wise mess bill\b|\bmess bill\b", text):
        # Extract course name if present
        c_match = re.search(r"course wise mess bill\s+([A-Za-z\s]+)", text)
        if c_match:
            slots["course_name"] = c_match.group(1).strip()
        return _build_result("mess_bill_summary", "matched mess bill summary")

    # ── mess_receipts_by_trainee ──
    if re.search(r"\bmess receipts?\b|\bmess payment history\b|\bmess paid bills\b|\bmess receipt\b", text):
        m = re.search(r"(?:mess receipts? of|mess payment history of|mess receipt of)\s+([A-Za-z\s]+)|([A-Za-z\s]+)\s+mess paid bills|([A-Za-z\s]+)\s+mess receipts?", text)
        if m:
            extracted = m.group(1) or m.group(2) or m.group(3)
            if extracted:
                clean_name = re.sub(r"\b(mess|receipts?|of|payment|history|paid|bills|show)\b", "", extracted.lower()).strip()
                if clean_name:
                    slots["trainee_name"] = clean_name
        return _build_result("mess_receipts_by_trainee", "matched mess receipts by trainee")

    # ── mess_material_stock (check BEFORE item_summary — "mess material stock" overlaps "mess material") ──
    if re.search(r"\bmess material stock\b|\bavailable mess items\b|\bitem prices\b|\bmess stock report\b|\bmess stock\b", text):
        m = re.search(r"([A-Za-z\s]+)\s+stock|available\s+([A-Za-z\s]+)|\bprice\s+([A-Za-z\s]+)", text)
        if m:
            extracted = m.group(1) or m.group(2) or m.group(3)
            if extracted:
                clean_item = re.sub(r"\b(mess|item|items|material|stock|available|prices|report|show)\b", "", extracted.lower()).strip()
                if clean_item:
                    slots["item_name"] = clean_item
        return _build_result("mess_material_stock", "matched mess material stock")

    # ── mess_party_summary (check BEFORE item_summary — "vendor wise mess material" overlaps "mess material") ──
    if re.search(r"\bparty wise mess\b|\bvendor wise mess\b|\bsupplier payments\b|\bparty payment summary\b", text):
        m = re.search(r"(?:vendor|party|supplier)\s+([A-Za-z\s]+)|([A-Za-z\s]+)\s+(?:vendor|party|supplier)", text)
        if m:
            extracted = m.group(1) or m.group(2)
            if extracted:
                clean_party = re.sub(r"\b(wise|mess|bills|material|payments|summary|vendor|party|supplier|show)\b", "", extracted.lower()).strip()
                if clean_party:
                    slots["party_name"] = clean_party
        return _build_result("mess_party_summary", "matched mess party summary")

    # Also catch vendor/party/supplier + mess keyword combos
    if re.search(r"\b(vendor|party|supplier)\b", text) and has_mess_word:
        m = re.search(r"(?:vendor|party|supplier)\s+([A-Za-z\s]+)|([A-Za-z\s]+)\s+(?:vendor|party|supplier)", text)
        if m:
            extracted = m.group(1) or m.group(2)
            if extracted:
                clean_party = re.sub(r"\b(wise|mess|bills|material|payments|summary|vendor|party|supplier|show)\b", "", extracted.lower()).strip()
                if clean_party:
                    slots["party_name"] = clean_party
        return _build_result("mess_party_summary", "matched mess party summary")

    # ── mess_item_summary ──
    if re.search(r"\bmess item summary\b|\bitem wise mess material\b|\bmess material usage\b|\bmess item\b|\bmess material\b", text) and has_mess_word:
        m = re.search(r"([A-Za-z\s]+)\s+consumption|\bmess material\s+([A-Za-z\s]+)|\bitem price\s+([A-Za-z\s]+)", text)
        if m:
            extracted = m.group(1) or m.group(2) or m.group(3)
            if extracted:
                clean_item = re.sub(r"\b(mess|item|material|stock|available|price|consumption|usage|summary|show|wise)\b", "", extracted.lower()).strip()
                if clean_item:
                    slots["item_name"] = clean_item
        return _build_result("mess_item_summary", "matched mess item summary")

    # consumption pattern without explicit "mess" — e.g. "Rice consumption"
    if re.search(r"\bconsumption\b", text):
        m = re.search(r"([A-Za-z\s]+)\s+consumption", text)
        if m:
            clean_item = re.sub(r"\b(mess|item|material|consumption|usage|summary|show)\b", "", m.group(1).lower()).strip()
            if clean_item:
                slots["item_name"] = clean_item
        return _build_result("mess_item_summary", "matched mess item consumption")

    # ── mess_refund_summary ──
    if re.search(r"\bmess refund summary\b|\brefunds issued\b|\bmess refund\b", text):
        m = re.search(r"([A-Za-z\s]+)\s+mess refund|\bmess refund of\s+([A-Za-z\s]+)", text)
        if m:
            extracted = m.group(1) or m.group(2)
            if extracted:
                clean_name = re.sub(r"\b(mess|refund|of|summary|issued|show)\b", "", extracted.lower()).strip()
                if clean_name:
                    slots["trainee_name"] = clean_name
        return _build_result("mess_refund_summary", "matched mess refund summary")

    # ── Catch-all for "mess dues" without trainee name ──
    if re.search(r"\bmess dues\b", text):
        return _build_result("mess_dues_by_trainee", "matched generic mess dues")

    return None

