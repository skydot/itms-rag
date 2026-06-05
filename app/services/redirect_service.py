import os

TRMS_BASE_URL = os.environ.get("TRMS_BASE_URL", "http://192.168.1.42")

ROUTE_MAP = {
    "customer": "/customers/view.php?id={id}",
    "trainee": "/trainees/view.php?id={id}",
    "hostel_allotment": "/hostel/allotment/view.php?id={id}",
    "complaint": "/complaints/view.php?id={id}",
    "icard": "/icard/view.php?id={id}",
    "certificate": "/certificates/view.php?id={id}",
    "attendance": "/attendance/view.php?id={id}",
    "meeting": "/meetings/view.php?id={id}",
    "vehicle_booking": "/vehicle/bookings/view.php?id={id}",
    "library_issue": "/library/issue/view.php?id={id}"
}

def build_redirect_url(module_name: str, record_id: int) -> str | None:
    """Builds a full redirect URL for a given module and record ID."""
    if module_name not in ROUTE_MAP:
        return None
        
    route = ROUTE_MAP[module_name].format(id=record_id)
    return f"{TRMS_BASE_URL}{route}"
