def _build_exam_date_filter(slots, alias="em"):
    """
    Build date filter from slots: year, date_range, from_date, to_date, date.
    Returns (sql_where, params)
    """
    date = slots.get("date")
    year = slots.get("year")
    date_range = slots.get("date_range")
    
    # Try year first (e.g. '2023')
    if year:
        return f" AND YEAR({alias}.created_at) = %s", [year]
        
    # Try date range (e.g. 'last year', 'last month', 'past 4 months')
    if date_range:
        dr = str(date_range).lower()
        if "last year" in dr or "past year" in dr or "previous year" in dr:
            return f" AND YEAR({alias}.created_at) = YEAR(CURDATE()) - 1", []
        if "this year" in dr or "current year" in dr:
            return f" AND YEAR({alias}.created_at) = YEAR(CURDATE())", []
        if "last month" in dr or "past month" in dr or "previous month" in dr:
            return f" AND {alias}.created_at >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)", []
        import re
        m = re.search(r"past\s+(\d+)\s+month", dr)
        if m:
            return f" AND {alias}.created_at >= DATE_SUB(CURDATE(), INTERVAL %s MONTH)", [int(m.group(1))]
        if "last 30 days" in dr:
            return f" AND {alias}.created_at >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)", []
            
    # Explicit from/to
    from_date = slots.get("from_date")
    to_date = slots.get("to_date")
    if from_date and to_date:
        return f" AND DATE({alias}.created_at) BETWEEN %s AND %s", [from_date, to_date]
    if from_date:
        return f" AND DATE({alias}.created_at) >= %s", [from_date]
    if to_date:
        return f" AND DATE({alias}.created_at) <= %s", [to_date]
        
    # Explicit single date
    if date:
        return f" AND DATE({alias}.created_at) = %s", [date]
        
    return "", []
