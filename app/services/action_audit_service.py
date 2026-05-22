import json
from datetime import datetime
import os

AUDIT_LOG_FILE = "logs/action_audit.log"

def log_action(action: str, module: str, user_context: dict, fields: dict, status: str, record_id: int = None, error: str = None):
    """Logs action execution details."""
    os.makedirs(os.path.dirname(AUDIT_LOG_FILE), exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "role": user_context.get("role", "unknown"),
        "office_id": user_context.get("office_id"),
        "action": action,
        "module": module,
        "fields_summary": str(fields),
        "status": status,
        "record_id": record_id,
        "error": error
    }
    
    try:
        with open(AUDIT_LOG_FILE, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"[Audit] Failed to write audit log: {e}")
