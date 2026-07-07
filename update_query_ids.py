import json
import re

def get_module_prefix(page_name):
    # Remove .php, .inc etc
    page = page_name.replace('.php', '').replace('.inc', '')
    
    # Common mappings
    mapping = {
        'attendance': 'ATT',
        'trainee': 'TRN',
        'hostel': 'HST',
        'exam': 'EXM',
        'complaint': 'CMP',
        'daily_position': 'DPO',
        'mess': 'MES',
        'meeting': 'MTG',
        'seminar': 'SEM',
        'study_tour': 'STR',
        'field_training': 'FLD',
        'inspection': 'INS',
        'book': 'LIB',
        'library': 'LIB',
        'sport': 'SPT',
        'vehicle': 'VEH',
        'pass': 'PAS',
        'eq': 'PAS',
        'faculty': 'FAC',
        'feedback': 'FDB',
        'feed': 'FDB',
        'training_calendar': 'TCA',
        'dues': 'DUE',
        'dashboard': 'DSH',
        'admission': 'ADM',
        'bill': 'MES',
        'receipt': 'MES',
    }
    
    for key, prefix in mapping.items():
        if key in page:
            return prefix
            
    # Fallback to first 3 consonants or letters
    cleaned = re.sub(r'[^a-zA-Z]', '', page).upper()
    if len(cleaned) >= 3:
        return cleaned[:3]
    return "GEN"

def get_action_name(description, sql):
    # Try to extract tables from description
    # "Retrieves data from rail_stations, training_calendars, divisions for..."
    match = re.search(r'Retrieves data from (.*?)(?: filtered by| joined with| for the)', description)
    if match:
        tables = match.group(1).split(', ')
        first_table = tables[0].replace(' ', '_').upper()
        if len(tables) > 1:
            return f"GET_{first_table}_AND_MORE"
        return f"GET_{first_table}"
        
    return "GET_DATA"

def main():
    path = "/home/erpuser/rag-server/app/static/trms_all_real_queries.json"
    with open(path, 'r') as f:
        data = json.load(f)
        
    counters = {}
    
    for item in data:
        page = item.get("page_name", "")
        prefix = get_module_prefix(page)
        
        if prefix not in counters:
            counters[prefix] = 1
        else:
            counters[prefix] += 1
            
        action = get_action_name(item.get("description", ""), item.get("complete_sql", ""))
        
        new_id = f"{prefix}_Q{counters[prefix]}: {action}"
        item["query_id"] = new_id
        
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
        
    print(f"Updated {len(data)} queries.")

if __name__ == '__main__':
    main()
