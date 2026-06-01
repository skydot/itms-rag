import asyncio
import json
from app.services.guided_query_refiner import _quick_classify
print(json.dumps(_quick_classify("how to add a trainee")))
