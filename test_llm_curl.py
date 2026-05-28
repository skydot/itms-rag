import json
import requests
from app.services.guided_query_refiner import refine_guided_query

g = refine_guided_query("How many trainees joined past 4 months?")
print("Result:", g)
