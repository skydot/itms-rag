import re
text = "pending returns of mayank"
m = re.search(r"\bpending returns\b.*(?:of|for|by)\s+([A-Za-z\s]+)", text)
print(m.group(1))
