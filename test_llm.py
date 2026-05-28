import json
import requests
import app.services.guided_query_refiner as g

text = "How many trainees joined past 4 months?"
prompt = g._build_refiner_prompt(text, None)
response = requests.post(
    "http://148.135.137.141:11434/v1/chat/completions",
    json={
        "model": "qwen2.5-1.5b",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0
    }
)
print("RAW RESPONSE:", response.text)
