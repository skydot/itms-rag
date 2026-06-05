import re
from typing import Optional, Dict

LIBRARY_FLOWS = {
    "book_search": {
        "flow_id": "book_search",
        "module": "library",
        "slots_order": ["book_title"],
        "requires_name": False
    },
    "book_availability": {
        "flow_id": "book_availability",
        "module": "library",
        "slots_order": [],
        "requires_name": False
    },
    "issued_books_by_trainee": {
        "flow_id": "issued_books_by_trainee",
        "module": "library",
        "slots_order": ["trainee_name", "user_id"],
        "requires_name": True
    },
    "overdue_books_by_trainee": {
        "flow_id": "overdue_books_by_trainee",
        "module": "library",
        "slots_order": ["trainee_name", "user_id"],
        "requires_name": True
    },
    "overdue_books": {
        "flow_id": "overdue_books",
        "module": "library",
        "slots_order": [],
        "requires_name": False
    },
    "pending_returns_by_trainee": {
        "flow_id": "pending_returns_by_trainee",
        "module": "library",
        "slots_order": ["trainee_name", "user_id"],
        "requires_name": True
    },
    "book_issue_history": {
        "flow_id": "book_issue_history",
        "module": "library",
        "slots_order": ["book_title", "book_id"],
        "requires_name": False
    },
    "library_book_count": {
        "flow_id": "library_book_count",
        "module": "library",
        "slots_order": [],
        "requires_name": False
    },
    "book_type_summary": {
        "flow_id": "book_type_summary",
        "module": "library",
        "slots_order": [],
        "requires_name": False
    },
    "most_issued_books": {
        "flow_id": "most_issued_books",
        "module": "library",
        "slots_order": [],
        "requires_name": False
    },
    "recent_book_issues": {
        "flow_id": "recent_book_issues",
        "module": "library",
        "slots_order": [],
        "requires_name": False
    },
    "pending_book_returns": {
        "flow_id": "pending_book_returns",
        "module": "library",
        "slots_order": [],
        "requires_name": False
    }
}

def normalize_library_message(message: str) -> str:
    text = message.lower().strip()
    # Strip common punctuation that breaks LIKE queries
    text = re.sub(r"[?!.,;:\'\"()\[\]{}]", "", text)
    replacements = {
        r"\blibary\b": "library",
        r"\blibrery\b": "library",
        r"\blibraray\b": "library",
        r"\bbok\b": "book",
        r"\bboook\b": "book",
        r"\bbooks\b": "book",
        r"\bavailble\b": "available",
        r"\bavilable\b": "available",
        r"\bissed\b": "issued",
        r"\bisued\b": "issued",
        r"\bretrun\b": "return",
        r"\bretun\b": "return",
        r"\boverdu\b": "overdue",
        r"\bpendng\b": "pending",
        r"\bhistroy\b": "history",
    }
    for pat, repl in replacements.items():
        text = re.sub(pat, repl, text)
    return text

def detect_library_guided_flow(message: str) -> Optional[Dict]:
    text = normalize_library_message(message)
    slots = {
        "book_title": None,
        "book_id": None,
        "book_type": None,
        "trainee_name": None,
        "user_id": None,
        "date": None,
        "from_date": None,
        "to_date": None,
        "limit": None,
        "status": None
    }

    has_book_word = bool(re.search(r"\b(book|library)\b", text))

    # Negative guards
    if re.search(r"\bmess\b", text):
        return None
    if re.search(r"\b(marks|result|exam|pass|fail)\b", text) and not has_book_word:
        return None
    if re.search(r"\b(attendance|present|absent)\b", text) and not has_book_word:
        return None
    if re.search(r"\b(hostel|room|bed|staying)\b", text) and not has_book_word:
        return None
    if re.search(r"\b(complaint|issue|problem)\b", text) and not has_book_word:
        return None
    if re.search(r"\b(faculty|timetable|schedule)\b", text) and not has_book_word:
        return None

    def _build_result(flow_id: str, reason: str) -> Dict:
        return {
            "flow_id": flow_id,
            "module": "library",
            "slots": slots,
            "reason": reason
        }

    # Extract limit
    m_limit = re.search(r"\b(top|last)\s+(\d+)\b", text)
    if m_limit:
        slots["limit"] = int(m_limit.group(2))

    # ── issued_books_by_trainee ──
    if re.search(r"issued\s+to\b|borrowed\s+by\b|issue\s+of\b", text) or (re.search(r"\blibrary\b", text) and re.search(r"\b(book)\b", text) and re.search(r"\b(issued|borrowed)\b", text)):
        m = re.search(r"(?:issued to|borrowed by|issue of|returns of)\s+([A-Za-z\s]+)", text)
        if m:
            clean_name = re.sub(r"\b(book|issued|to|library|pending|returns|of|overdue|how|many)\b", "", m.group(1).lower()).strip()
            if clean_name:
                slots["trainee_name"] = clean_name
        return _build_result("issued_books_by_trainee", "matched issued books by trainee")
        
    if re.search(r"pending returns of\s+([A-Za-z\s]+)", text):
        m = re.search(r"pending returns of\s+([A-Za-z\s]+)", text)
        if m:
            clean_name = re.sub(r"\b(book|issued|to|library|pending|returns|of|overdue|how|many)\b", "", m.group(1).lower()).strip()
            if clean_name:
                slots["trainee_name"] = clean_name
        return _build_result("pending_returns_by_trainee", "matched pending book returns by trainee")

    # ── overdue_books_by_trainee ──
    if re.search(r"\boverdue\b.*(?:of|for|by)\s+([A-Za-z\s]+)", text):
        m = re.search(r"\boverdue\b.*(?:of|for|by)\s+([A-Za-z\s]+)", text)
        if m:
            clean_name = re.sub(r"\b(book|books|library|of|for|overdue|how|many|by)\b", "", m.group(1).lower()).strip()
            if clean_name:
                slots["trainee_name"] = clean_name
        return _build_result("overdue_books_by_trainee", "matched overdue books by trainee")

    # ── pending_returns_by_trainee ──
    if re.search(r"\bpending returns\b.*(?:of|for|by)\s+([A-Za-z\s]+)", text):
        m = re.search(r"\bpending returns\b.*(?:of|for|by)\s+([A-Za-z\s]+)", text)
        if m:
            clean_name = re.sub(r"\b(book|books|library|of|for|pending|returns|how|many|by)\b", "", m.group(1).lower()).strip()
            if clean_name:
                slots["trainee_name"] = clean_name
        return _build_result("pending_returns_by_trainee", "matched pending returns by trainee")

    # ── overdue_books ──
    if re.search(r"\boverdue\b|\bnot returned after due\b|\bdue date\b", text):
        return _build_result("overdue_books", "matched overdue books")

    # ── pending_book_returns ──
    if re.search(r"\bpending returns\b|\bnot returned yet\b|\bwho has not returned\b", text):
        return _build_result("pending_book_returns", "matched pending book returns")

    # ── book_issue_history ──
    if re.search(r"\bissue history\b|\bhistory of\b|\bwho borrowed\b", text):
        m = re.search(r"(?:history of|who borrowed)\s+([A-Za-z0-9\s]+)", text)
        if m:
            clean_title = re.sub(r"\b(search|find|book|library|available|availability|issue|history|of|is|do|we|have)\b", "", m.group(1).lower()).strip()
            if clean_title:
                slots["book_title"] = clean_title
        return _build_result("book_issue_history", "matched book issue history")

    # ── most_issued_books ──
    if re.search(r"\bmost issued\b|\bpopular\b|\btop borrowed\b|\btop \d+ (?:issued|borrowed)\b", text):
        return _build_result("most_issued_books", "matched most issued books")

    # ── recent_book_issues ──
    if re.search(r"\brecent book issue\b|\blast \d+ book issue\b|\blatest issued book\b", text):
        return _build_result("recent_book_issues", "matched recent book issues")

    # ── library_book_count ──
    if re.search(r"\bhow many book.*in library\b|\btotal book\b|\blibrary book count\b|\bhow many \w+ book\b", text):
        return _build_result("library_book_count", "matched library book count")

    # ── book_type_summary ──
    if re.search(r"\btype wise count\b|\bcategory wise book\b|\bsubject wise book\b|\bbook category summary\b|\bbook type wise\b", text):
        return _build_result("book_type_summary", "matched book type summary")

    # ── book_availability ──
    if re.search(r"\bavailable\b|\bavailability\b|\bin library\b", text):
        m = re.search(r"(?:available|availability|in library)\s*(?:on|for)?\s*([A-Za-z0-9\s]+)", text)
        if m:
            clean_title = re.sub(r"\b(search|find|book|books|library|available|availability|issue|history|of|is|do|we|have|are|many|how|on|for)\b", "", text).strip()
            if clean_title:
                slots["book_title"] = clean_title
        return _build_result("book_availability", "matched book availability")

    # ── book_search ──
    if re.search(r"\bsearch\b|\bfind\b|\bdo we have\b", text) and has_book_word:
        clean_title = re.sub(r"\b(search|find|book|books|library|available|availability|issue|history|of|is|do|we|have|are)\b", "", text).strip()
        if clean_title:
            slots["book_title"] = clean_title
        return _build_result("book_search", "matched book search")

    return None
