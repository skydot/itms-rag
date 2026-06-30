from dotenv import load_dotenv
load_dotenv()
from app.services.query_registry import select_query_and_extract_params

res = select_query_and_extract_params("show all library books?", "library")
print(res)
res2 = select_query_and_extract_params("how many books in library!", "library")
print(res2)
