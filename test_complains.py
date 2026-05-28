from app.services.guided_query_refiner import refine_guided_query
from app.services.guided_flow_service import process_guided_flow

print("Refiner:")
print(refine_guided_query("show complains"))

print("\nGuided Flow:")
print(process_guided_flow("show complains", 1, "admin"))
