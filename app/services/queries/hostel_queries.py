"""Hostel module query templates and dispatcher."""
from app.services.queries import hostel_building_room, hostel_occupancy_trainee, hostel_checkin_stats

TEMPLATES = [
    # --- Building & Room Info ---
    {
        "id": "HOSTEL_ACTIVE_BUILDINGS",
        "module": "hostel",
        "description": "List all active hostel buildings",
        "example_questions": ["Active hostel buildings?", "Which hostels are active?", "List all hostels"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_ALL_BUILDINGS",
        "module": "hostel",
        "description": "List all buildings active and inactive",
        "example_questions": ["All hostel buildings?", "List all buildings with status"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_BUILDING_DETAILS",
        "module": "hostel",
        "description": "Details of a specific building",
        "example_questions": ["Building details?", "Tell me about a hostel building"],
        "required_params": ["building_id"],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "detail",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_ROOMS_IN_BUILDING",
        "module": "hostel",
        "description": "List rooms in a building",
        "example_questions": ["Rooms in building?", "What rooms are in hostel?"],
        "required_params": ["building_id"],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_ROOMS_BY_BUILDING_NAME",
        "module": "hostel",
        "description": "Rooms by building name",
        "example_questions": ["Rooms in Geetanjali?", "How many rooms in Chetak hostel?"],
        "required_params": [],
        "optional_params": ["building_name", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_TOTAL_ROOMS",
        "module": "hostel",
        "description": "Total number of hostel rooms",
        "example_questions": ["Total rooms?", "How many rooms in hostel?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_TOTAL_BEDS",
        "module": "hostel",
        "description": "Total beds across all rooms",
        "example_questions": ["Total beds?", "How many beds in hostel?", "Hostel capacity"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_TOTAL_BED_CAPACITY",
        "module": "hostel",
        "description": "Total bed capacity across all buildings",
        "example_questions": ["Total bed capacity?", "Building capacity"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_BED_CAPACITY_PER_BUILDING",
        "module": "hostel",
        "description": "Bed capacity per building",
        "example_questions": ["Bed capacity per building?", "Capacity of each hostel"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_BEDS_IN_SPECIFIC_BUILDING",
        "module": "hostel",
        "description": "Total beds/capacity in a specific building",
        "example_questions": ["Beds in Geetanjali?", "Capacity of Chetak hostel?"],
        "required_params": ["building_name"],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_AC_ROOMS",
        "module": "hostel",
        "description": "List all AC rooms",
        "example_questions": ["AC rooms?", "Rooms with AC"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_ROOMS_WITH_TOILET",
        "module": "hostel",
        "description": "Rooms with attached toilet",
        "example_questions": ["Rooms with toilet?", "Attached bathroom rooms"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_LADIES_ROOMS",
        "module": "hostel",
        "description": "Ladies hostel room stats",
        "example_questions": ["Ladies hostel rooms?", "Female hostel stats"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    # --- Occupancy & Availability ---
    {
        "id": "HOSTEL_OCCUPANCY",
        "module": "hostel",
        "description": "Overall hostel occupancy rate/percentage",
        "example_questions": ["Hostel occupancy?", "How full is the hostel?", "Occupancy rate"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_OCCUPANCY_PERCENTAGE",
        "module": "hostel",
        "description": "Overall occupancy percentage",
        "example_questions": ["Occupancy percentage?", "What percent of hostel is occupied?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_OCCUPANCY_PER_BUILDING",
        "module": "hostel",
        "description": "Occupancy per building",
        "example_questions": ["Occupancy per building?", "How full is each hostel?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_OCCUPANCY_PER_ROOM",
        "module": "hostel",
        "description": "Occupancy per room",
        "example_questions": ["Occupancy per room?", "Which rooms are occupied?"],
        "required_params": ["building_id"],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_VACANT_ROOMS_NOW",
        "module": "hostel",
        "description": "Vacant rooms right now",
        "example_questions": ["Vacant rooms?", "Available rooms now", "Empty rooms"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_AVAILABLE_ROOMS",
        "module": "hostel",
        "description": "Available rooms with free beds",
        "example_questions": ["Available rooms?", "Rooms with space", "Vacant beds"],
        "required_params": [],
        "optional_params": ["building_name", "gender", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_AVAILABLE_ROOMS_BY_BUILDING",
        "module": "hostel",
        "description": "Available rooms by building",
        "example_questions": ["Available rooms by building?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_FULL_ROOMS",
        "module": "hostel",
        "description": "Which rooms are completely full",
        "example_questions": ["Full rooms?", "Completely occupied rooms"],
        "required_params": [],
        "optional_params": ["building_name", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_UNUSED_ROOMS",
        "module": "hostel",
        "description": "Rooms with zero occupants",
        "example_questions": ["Unused rooms?", "Empty unused rooms"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_OCCUPIED_ROOMS",
        "module": "hostel",
        "description": "Count of occupied rooms",
        "example_questions": ["Occupied rooms count?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_FULL_ROOM_LIST_STATUS",
        "module": "hostel",
        "description": "Full room list with status",
        "example_questions": ["Room list with status?", "All rooms status"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_OCCUPANCY_SUMMARY",
        "module": "hostel",
        "description": "Occupancy summary",
        "example_questions": ["Occupancy summary?", "Hostel summary"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    # --- Trainee Occupancy ---
    {
        "id": "HOSTEL_CURRENT_STAYING_COUNT",
        "module": "hostel",
        "description": "How many trainees currently staying",
        "example_questions": ["How many trainees staying?", "Current hostel count"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_TRAINEES_STAYING",
        "module": "hostel",
        "description": "All trainees staying with room and course details",
        "example_questions": ["List trainees in hostel?", "Who is staying in hostel?", "Trainees in Geetanjali"],
        "required_params": [],
        "optional_params": ["building_name", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_FULL_ALLOTMENT_LIST",
        "module": "hostel",
        "description": "Full allotment list with trainee and course details",
        "example_questions": ["Full allotment list?", "All current allotments"],
        "required_params": [],
        "optional_params": ["building_name", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_GENDER_WISE_OCCUPANCY",
        "module": "hostel",
        "description": "Gender-wise occupancy with count and beds",
        "example_questions": ["Gender-wise occupancy?", "Male female hostel count"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_TRAINEES_FOR_COURSE",
        "module": "hostel",
        "description": "Hostel trainees for a course with room details",
        "example_questions": ["Trainees for course?", "Who from course 75 is in hostel?"],
        "required_params": ["course_id"],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_COURSE_WISE_OCCUPANCY",
        "module": "hostel",
        "description": "Course-wise occupancy",
        "example_questions": ["Course-wise occupancy?", "How many per course in hostel?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_TRAINEES_NO_ROOM",
        "module": "hostel",
        "description": "Trainees without a room assigned",
        "example_questions": ["Trainees without room?", "Who needs room allotment?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_PH_TRAINEES",
        "module": "hostel",
        "description": "PH trainees in hostel",
        "example_questions": ["PH trainees?", "Physically handicapped trainees"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    # --- Room Occupants ---
    {
        "id": "HOSTEL_WHO_IN_BUILDING",
        "module": "hostel",
        "description": "Who is staying in a building",
        "example_questions": ["Who is in Geetanjali?", "Trainees in Chetak hostel"],
        "required_params": ["building_id"],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_WHO_IN_ROOM",
        "module": "hostel",
        "description": "Who is in a specific room",
        "example_questions": ["Who is in room 5?", "Room occupants"],
        "required_params": ["room_id"],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_ROOM_OCCUPANTS",
        "module": "hostel",
        "description": "Who stays in a specific room by name",
        "example_questions": ["Occupants of room?", "Who stays in room 101?"],
        "required_params": ["room_name"],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    # --- Search & Details ---
    {
        "id": "HOSTEL_TRAINEE_DETAILS",
        "module": "hostel",
        "description": "Find hostel details for a trainee by name",
        "example_questions": ["Hostel details for trainee?", "Where is Ramesh staying?"],
        "required_params": ["search_name"],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_SEARCH_TRAINEE_BY_NAME",
        "module": "hostel",
        "description": "Search trainee by name",
        "example_questions": ["Find trainee?", "Search hostel for name"],
        "required_params": ["search_name"],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_FIND_TRAINEE_ROOM",
        "module": "hostel",
        "description": "Find trainee room",
        "example_questions": ["Find room for trainee?", "Where is user staying?"],
        "required_params": ["user_id"],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "detail",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_IS_TRAINEE_IN_HOSTEL",
        "module": "hostel",
        "description": "Is trainee in hostel",
        "example_questions": ["Is trainee in hostel?", "Check if staying in hostel"],
        "required_params": ["user_id"],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "boolean",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_TRAINEE_BUILDING_ROOM",
        "module": "hostel",
        "description": "Trainee building and room",
        "example_questions": ["Building and room for trainee?"],
        "required_params": ["user_id"],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "detail",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_TRAINEE_STAY_HISTORY",
        "module": "hostel",
        "description": "Stay history for a trainee",
        "example_questions": ["Stay history?", "Past hostel stays"],
        "required_params": ["user_id"],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    # --- Check-in / Check-out ---
    {
        "id": "HOSTEL_RECENT_CHECKINS",
        "module": "hostel",
        "description": "Recent hostel check-ins",
        "example_questions": ["Recent check-ins?", "Who checked in recently?"],
        "required_params": [],
        "optional_params": ["limit", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_CHECKINS_TODAY",
        "module": "hostel",
        "description": "Trainees checking in today",
        "example_questions": ["Check-ins today?", "Who is checking in today?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_CHECKOUTS_TODAY",
        "module": "hostel",
        "description": "Trainees checking out today",
        "example_questions": ["Checkouts today?", "Who is leaving today?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_CHECKOUTS_UPCOMING",
        "module": "hostel",
        "description": "Checkouts in next N days",
        "example_questions": ["Upcoming checkouts?", "Who is leaving this week?"],
        "required_params": [],
        "optional_params": ["days_ahead", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_CHECKINS_DATE_RANGE",
        "module": "hostel",
        "description": "Check-ins in date range",
        "example_questions": ["Check-ins in date range?", "Who checked in between dates?"],
        "required_params": [],
        "optional_params": ["from_date", "to_date", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_MONTHLY_CHECKINS",
        "module": "hostel",
        "description": "Month-wise check-ins",
        "example_questions": ["Monthly check-ins?", "Check-ins by month"],
        "required_params": [],
        "optional_params": ["year", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_AVG_STAY_PER_BUILDING",
        "module": "hostel",
        "description": "Average stay duration per building",
        "example_questions": ["Average stay per building?", "How long do trainees stay?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_OVERSTAY",
        "module": "hostel",
        "description": "Trainees past checkout date",
        "example_questions": ["Overstays?", "Trainees past checkout"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    # --- Complaints ---
    {
        "id": "HOSTEL_PENDING_COMPLAINTS",
        "module": "hostel",
        "description": "Pending hostel complaints",
        "example_questions": ["Pending complaints?", "Unresolved hostel issues"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_MOST_COMPLAINTS",
        "module": "hostel",
        "description": "Building with most complaints",
        "example_questions": ["Which building has most complaints?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "detail",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_COMPLAINTS_COUNT",
        "module": "hostel",
        "description": "Total complaints count",
        "example_questions": ["Total complaints?", "How many complaints?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_COMPLAINTS_BY_STATUS",
        "module": "hostel",
        "description": "Complaints by status",
        "example_questions": ["Complaints by status?", "Status-wise complaints"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    # --- Financial ---
    {
        "id": "HOSTEL_TOTAL_REVENUE",
        "module": "hostel",
        "description": "Total hostel charges collected",
        "example_questions": ["Total revenue?", "Hostel income"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "count",
        "security_level": "medium"
    },
    {
        "id": "HOSTEL_REVENUE_PER_BUILDING",
        "module": "hostel",
        "description": "Revenue per building",
        "example_questions": ["Revenue per building?", "Income by hostel"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "HOSTEL_DUES_PENDING",
        "module": "hostel",
        "description": "Trainees with dues pending",
        "example_questions": ["Pending dues?", "Who owes hostel charges?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "HOSTEL_TRAINEE_CHARGES",
        "module": "hostel",
        "description": "Trainee charges",
        "example_questions": ["Charges for trainee?", "How much does trainee owe?"],
        "required_params": ["user_id"],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "detail",
        "security_level": "medium"
    },
    # --- Mess ---
    {
        "id": "HOSTEL_MESS_TRAINEES",
        "module": "hostel",
        "description": "Trainees who opted for mess",
        "example_questions": ["Mess trainees?", "Who opted for mess?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_MESS_COUNT_PER_BUILDING",
        "module": "hostel",
        "description": "Mess count per building",
        "example_questions": ["Mess count per building?", "Mess strength per hostel"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_TOTAL_MESS_STRENGTH",
        "module": "hostel",
        "description": "Total mess strength today",
        "example_questions": ["Total mess strength?", "How many in mess today?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    # --- Search ---
    {
        "id": "HOSTEL_FIND_BY_RECEIPT",
        "module": "hostel",
        "description": "Find by receipt number",
        "example_questions": ["Find by receipt?", "Search by receipt number"],
        "required_params": ["receipt_no"],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "detail",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_FIND_BY_ALLOTMENT_ID",
        "module": "hostel",
        "description": "Find by allotment ID",
        "example_questions": ["Find by allotment ID?", "Search by HM ID"],
        "required_params": ["hm_id"],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "detail",
        "security_level": "low"
    },
    {
        "id": "HOSTEL_EXTRA_ROOM_ALLOTMENTS",
        "module": "hostel",
        "description": "Extra room allotments",
        "example_questions": ["Extra room allotments?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    # --- Other ---
    {
        "id": "HOSTEL_ROOMS_BY_FLOOR",
        "module": "hostel",
        "description": "Rooms on a specific floor",
        "example_questions": ["Rooms on first floor?", "Ground floor rooms"],
        "required_params": ["floor"],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
]

# Ordered list of sub-handler modules
_HANDLERS = [hostel_building_room, hostel_occupancy_trainee, hostel_checkin_stats]


def execute(query_id, params, cur, office_id):
    """Dispatch to the appropriate hostel sub-handler."""
    for handler in _HANDLERS:
        result = handler.execute(query_id, params, cur, office_id)
        if result is not None:
            return result
    return None
