import os
import glob

files = glob.glob('/home/erpuser/rag-server/app/services/guided_modules/*executor.py')
files.append('/home/erpuser/rag-server/app/services/guided_query_executor.py')
files.append('/home/erpuser/rag-server/app/routes/chat.py')

for filepath in files:
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Fix 1: Single row single column case
    content = content.replace(
        """return f"{k}: {'None / 0' if v is None else str(v)}\"""",
        """return f"{k}: {'N/A' if v is None else str(v)}\""""
    )
    
    # Fix 2: Multi-column case
    content = content.replace(
        """        for k, v in row.items():
            if k.lower() not in _SENSITIVE_COLS:
                val = "None / 0" if v is None else str(v)
                label = k.replace('_', ' ').title()
                parts.append(f"{label}: {val}")""",
        """        for k, v in row.items():
            if k.lower() not in _SENSITIVE_COLS and v is not None and str(v).strip() != "":
                label = k.replace('_', ' ').title()
                parts.append(f"{label}: {str(v)}")"""
    )
    
    # Fix 3: Multi-column case in chat.py where it's dict directly
    content = content.replace(
        """    for k, v in row.items():
        if k.lower() not in _SENSITIVE_COLS:
            val = "None / 0" if v is None else str(v)
            label = k.replace('_', ' ').title()
            parts.append(f"{label}: {val}")""",
        """    for k, v in row.items():
        if k.lower() not in _SENSITIVE_COLS and v is not None and str(v).strip() != "":
            label = k.replace('_', ' ').title()
            parts.append(f"{label}: {str(v)}")"""
    )

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Fixed {filepath}")
