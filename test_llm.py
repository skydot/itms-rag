import sys
from app.services.llm_service import format_answer
import traceback

try:
    context = "Total count: 10\n1. Building: ARAVALI | Total Rooms: 32"
    format_answer("How many available beds?", context)
    print("Done")
except Exception as e:
    print(e)
    traceback.print_exc()
