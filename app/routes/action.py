from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.action_confirmation_service import get_confirmation, delete_confirmation
from app.services.action_executor_service import execute_action
from app.services.action_audit_service import log_action

router = APIRouter()

class ConfirmRequest(BaseModel):
    confirmation_id: str
    confirm: bool

@router.post("/action/confirm")
def confirm_action(request: ConfirmRequest):
    confirmation = get_confirmation(request.confirmation_id)
    
    if not confirmation:
        return {
            "type": "action_result",
            "status": "expired",
            "message": "Confirmation expired or invalid."
        }

    action = confirmation["action"]
    module = confirmation["module"]
    fields = confirmation["fields"]
    user_context = confirmation["user_context"]
    
    if not request.confirm:
        delete_confirmation(request.confirmation_id)
        
        log_action(
            action=action,
            module=module,
            user_context=user_context,
            fields=fields,
            status="cancelled"
        )
        
        return {
            "type": "action_result",
            "status": "cancelled",
            "message": "Action cancelled."
        }

    # Execute action
    result = execute_action(action, fields, user_context)
    
    # Delete confirmation regardless of success/fail to prevent double submission
    delete_confirmation(request.confirmation_id)
    
    return result
