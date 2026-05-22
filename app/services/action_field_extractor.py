import re

def extract_action_fields(action: str, message: str) -> dict:
    """Extracts required and optional fields from the message for the given action."""
    text = message.lower()
    fields = {}
    missing_fields = []
    
    # Simple rule-based extraction for MVP.
    # In a real scenario, this could use an LLM for structured extraction.
    
    if action == "create_customer":
        # extract name and mobile
        name_match = re.search(r'customer\s+([a-zA-Z\s]+?)(?:\s+mobile|\s+email|$)', text, re.IGNORECASE)
        if name_match:
            fields["name"] = name_match.group(1).strip()
        else:
            # Fallback naive name extraction
            words = message.split()
            idx = -1
            if "customer" in text:
                idx = text.split().index("customer")
            if idx != -1 and len(words) > idx + 1:
                fields["name"] = words[idx + 1].capitalize()
        
        mobile_match = re.search(r'mobile\s+(\d{10})', text, re.IGNORECASE)
        if mobile_match:
            fields["mobile"] = mobile_match.group(1)
            
        if "name" not in fields or not fields["name"]:
            missing_fields.append("name")

    elif action == "allot_hostel_room":
        room_match = re.search(r'room\s+(\w+)', text, re.IGNORECASE)
        if room_match:
            fields["room_name"] = room_match.group(1)
        else:
            missing_fields.append("room_name or room_id")
            
        # Extract trainee name (naive: word after "to" or before "room")
        to_match = re.search(r'to\s+([a-zA-Z\s]+)', text, re.IGNORECASE)
        if to_match:
            fields["trainee_name"] = to_match.group(1).strip()
        else:
            missing_fields.append("trainee_name")

    elif action == "create_complaint":
        desc_match = re.search(r'complaint(?:\s+(?:about|regarding|for|that|is))?\s+(.+)', text, re.IGNORECASE)
        if desc_match:
            fields["description"] = desc_match.group(1).strip()
        else:
            missing_fields.append("description")

    elif action in ["generate_icard", "generate_certificate"]:
        name_match = re.search(r'(?:for)\s+([a-zA-Z\s]+)', text, re.IGNORECASE)
        if name_match:
            fields["trainee_name"] = name_match.group(1).strip()
        else:
            missing_fields.append("trainee_name or user_id")
            
    elif action == "mark_attendance":
        name_match = re.search(r'(?:for)\s+([a-zA-Z\s]+)', text, re.IGNORECASE)
        if name_match:
            fields["trainee_name"] = name_match.group(1).strip()
        else:
            missing_fields.append("trainee_name")
            
        if "present" in text:
            fields["attendance_status"] = "present"
        elif "absent" in text:
            fields["attendance_status"] = "absent"
        else:
            missing_fields.append("attendance_status")

    elif action == "create_vehicle_booking":
        purpose_match = re.search(r'(?:for)\s+(.+)', text, re.IGNORECASE)
        if purpose_match:
            fields["purpose"] = purpose_match.group(1).strip()
        else:
            missing_fields.append("purpose/date or course_name")

    is_complete = len(missing_fields) == 0

    return {
        "fields": fields,
        "missing_fields": missing_fields,
        "is_complete": is_complete
    }
