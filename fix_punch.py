import os
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Replacements
    content = content.replace("a.a_b = 0", "a.punch = '4'")
    content = content.replace("a.a_b = 1", "a.punch = '5'")
    content = content.replace("a_b = 0", "punch = '4'")
    content = content.replace("a_b = 1", "punch = '5'")
    
    content = content.replace("a.a_b=0", "a.punch='4'")
    content = content.replace("a.a_b=1", "a.punch='5'")
    content = content.replace("a_b=0", "punch='4'")
    content = content.replace("a_b=1", "punch='5'")
    
    # Specific CASE statements
    content = content.replace("CASE a_b WHEN 0 THEN 'Present' WHEN 1 THEN 'Absent' END", 
                              "CASE punch WHEN '4' THEN 'Present' WHEN '5' THEN 'Absent' WHEN '1' THEN 'CL' WHEN '2' THEN 'LAP' WHEN '3' THEN 'SL' ELSE 'Unknown' END")
    content = content.replace("CASE WHEN a.a_b = 0 THEN 'Present' ELSE 'Absent' END",
                              "CASE a.punch WHEN '4' THEN 'Present' WHEN '5' THEN 'Absent' WHEN '1' THEN 'CL' WHEN '2' THEN 'LAP' WHEN '3' THEN 'SL' ELSE 'Absent' END")
    
    # Also fix dictionary access
    content = content.replace("r['a_b'] == 0", "r['punch'] == '4'")
    
    # Select clause: we don't need a_b
    content = content.replace("a.a_b,", "")
    content = content.replace("a.a_b", "a.punch")
    
    with open(filepath, 'w') as f:
        f.write(content)

base = "/home/erpuser/rag-server/app/services/queries/"
fix_file(os.path.join(base, "attendance_queries.py"))
fix_file(os.path.join(base, "trainee_queries.py"))
print("Done fixing punch values.")
