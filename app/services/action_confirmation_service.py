import uuid
import time

# In-memory storage for confirmations (TTL 10 minutes)
_CONFIRMATIONS = {}
TTL_SECONDS = 600

def create_confirmation(action: str, module: str, fields: dict, user_context: dict) -> dict:
    """Creates a new confirmation request and stores it."""
    confirmation_id = str(uuid.uuid4())
    now = time.time()
    
    confirmation = {
        "confirmation_id": confirmation_id,
        "action": action,
        "module": module,
        "fields": fields,
        "user_context": user_context,
        "created_at": now,
        "expires_at": now + TTL_SECONDS
    }
    
    _CONFIRMATIONS[confirmation_id] = confirmation
    
    return {
        "type": "confirmation_required",
        "confirmation_id": confirmation_id,
        "action": action,
        "module": module,
        "message": "Please confirm this action.",
        "summary": fields
    }

def get_confirmation(confirmation_id: str) -> dict | None:
    """Retrieves a pending confirmation if it exists and hasn't expired."""
    confirmation = _CONFIRMATIONS.get(confirmation_id)
    if not confirmation:
        return None
        
    if time.time() > confirmation["expires_at"]:
        delete_confirmation(confirmation_id)
        return None
        
    return confirmation

def delete_confirmation(confirmation_id: str):
    """Deletes a confirmation request."""
    if confirmation_id in _CONFIRMATIONS:
        del _CONFIRMATIONS[confirmation_id]

def cleanup_expired_confirmations():
    """Removes all expired confirmations."""
    now = time.time()
    expired = [cid for cid, c in _CONFIRMATIONS.items() if now > c["expires_at"]]
    for cid in expired:
        delete_confirmation(cid)
