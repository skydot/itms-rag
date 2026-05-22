from app.services.action_field_extractor import extract_action_fields
from app.services.action_intent_service import detect_action_intent, SUPPORTED_ACTIONS
from app.services.tools.trms_tools import (
    prepare_complaint_confirmation,
    prepare_icard_confirmation,
    prepare_room_allotment_confirmation,
)


def run_agentic_planner(message: str, user_context: dict) -> dict:
    """Handle supported write-action intents without a provider-specific LLM."""
    intent = detect_action_intent(message)

    if not intent.get("is_action"):
        return {"handled": False}

    action = intent["action"]
    if action not in ["create_complaint", "allot_hostel_room", "generate_icard"]:
        return {"handled": False}

    extracted = extract_action_fields(action, message)
    if not extracted.get("is_complete"):
        missing = ", ".join(extracted.get("missing_fields") or [])
        return {
            "handled": True,
            "type": "text",
            "message": f"Please provide {missing} to continue.",
        }

    fields = extracted.get("fields") or {}
    office_id = user_context.get("office_id", 1)
    role = user_context.get("role", "default")
    module = SUPPORTED_ACTIONS[action][0]

    try:
        if action == "allot_hostel_room":
            result = prepare_room_allotment_confirmation.invoke({
                "trainee_name": fields["trainee_name"],
                "room_name": fields["room_name"],
                "office_id": office_id,
                "role": role,
            })
        elif action == "create_complaint":
            result = prepare_complaint_confirmation.invoke({
                "description": fields["description"],
                "office_id": office_id,
                "role": role,
            })
        elif action == "generate_icard":
            result = prepare_icard_confirmation.invoke({
                "trainee_name": fields["trainee_name"],
                "office_id": office_id,
                "role": role,
            })
        else:
            return {"handled": False}

        if isinstance(result, dict) and result.get("type") == "confirmation_required":
            result["handled"] = True
            result.setdefault("module", module)
            return result

        if isinstance(result, dict) and "error" in result:
            return {
                "handled": True,
                "type": "action_result",
                "status": "failed",
                "message": result["error"],
            }

        return {
            "handled": True,
            "type": "text",
            "message": "I processed your request but could not finalize the action. Could you please provide more details?",
        }

    except Exception as exc:
        print(f"[Agent] Error in action planner: {exc}")
        return {"handled": False}
