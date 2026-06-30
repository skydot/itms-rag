import re
from datetime import datetime, timedelta

def parse_loose_date(date_str: str):
    if not date_str:
        return None
        
    date_str = str(date_str).strip()
    if date_str.lower() in ("today", "yesterday", "last_7_days", "last_30_days", "all"):
        return date_str

    # Clean up ordinals
    clean_date = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str.lower())
    clean_date = clean_date.replace(',', '')

    formats = [
        "%Y-%m-%d",
        "%d %B %Y", 
        "%d %b %Y", 
        "%B %d %Y", 
        "%b %d %Y",
        "%d %B",
        "%B %d",
        "%d/%m/%Y", 
        "%m/%d/%Y", 
        "%d-%m-%Y",
        "%Y/%m/%d"
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(clean_date, fmt)
            if dt.year == 1900:
                dt = dt.replace(year=datetime.now().year)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            pass
            
    # For just months, return a special tuple or string so queries know it's a month
    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    for i, m in enumerate(months, 1):
        if date_str.lower() == m or date_str.lower() == m[:3]:
            # Return YYYY-MM-01 format for the first day of that month for the current year
            yr = datetime.now().year
            return f"{yr}-{i:02d}-01"
            
    return date_str
