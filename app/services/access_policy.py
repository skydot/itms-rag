ROLE_MODULE_ACCESS = {
    "principal": {"exam", "hostel", "attendance", "trainee", "trainee_leave", "course_nominee"},
    "admin": {"exam", "hostel", "attendance", "trainee", "trainee_leave", "course_nominee"},
    "exam_staff": {"exam"},
    "hostel_warden": {"hostel"},
    "attendance_staff": {"attendance"},
    "hr_staff": {"trainee", "trainee_leave"},
    "training_staff": {"course_nominee", "trainee"},
    "unknown": set(),  # No access for unrecognized roles
}

IMPLEMENTED_MODULES = {"exam", "hostel", "attendance", "trainee", "trainee_leave", "course_nominee"}

ALL_KNOWN_ROLES = set(ROLE_MODULE_ACCESS.keys())


def normalize_role(role: str) -> str:
    normalized = (role or "").strip().lower()
    
    # Role aliases for common variations
    ROLE_ALIASES = {
        "warden": "hostel_warden",
        "hostel_staff": "hostel_warden",
        "hostel": "hostel_warden",
        "exam": "exam_staff",
        "attendance": "attendance_staff",
        "hr": "hr_staff",
        "training": "training_staff",
        "trainer": "training_staff",
    }
    
    # Check if it's a known role
    if normalized in ALL_KNOWN_ROLES:
        return normalized
    
    # Check if it's an alias
    if normalized in ROLE_ALIASES:
        return ROLE_ALIASES[normalized]
    
    # Unknown role = NO ACCESS (security fix!)
    return "unknown"


def allowed_modules_for_role(role: str) -> list[str]:
    normalized = normalize_role(role)
    return sorted(ROLE_MODULE_ACCESS.get(normalized, set()))


def has_module_access(role: str, module: str) -> bool:
    normalized = normalize_role(role)
    return module in ROLE_MODULE_ACCESS.get(normalized, set())


def is_module_implemented(module: str) -> bool:
    return module in IMPLEMENTED_MODULES


def describe_access(role: str) -> str:
    normalized = normalize_role(role)
    modules = allowed_modules_for_role(normalized)
    if not modules:
        return f"Your role is {normalized}. No data modules are configured for this role."

    module_list = ", ".join(modules)
    return (
        f"Your role is {normalized}. You are allowed to access these modules: {module_list}. "
        
    )


def describe_restricted_access(role: str) -> str:
    normalized = normalize_role(role)
    denied_modules = sorted({"exam", "hostel", "attendance"} - set(allowed_modules_for_role(normalized)))
    if not denied_modules:
        return f"Your role is {normalized}. No configured modules are restricted for you."

    return (
        f"Your role is {normalized}. You do not have access to these modules: "
        f"{', '.join(denied_modules)}."
    )
