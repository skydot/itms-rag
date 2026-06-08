import os
import sys
from app.services.guided_flow_service import handle_guided_flow, _get_guided_flow_definition, _check_next_slot, detect_seminar_guided_flow

print("Detecting...")
match = detect_seminar_guided_flow("Seminar topics")
print("Match:", match)

flow_def = _get_guided_flow_definition(match["flow_id"])
print("Flow Def:", flow_def)

print("Checking next slot...")
res = _check_next_slot(flow_def, match["slots"], 1, "Seminar topics", "test", "admin", "http://localhost:8000")
print("Result:", res)
