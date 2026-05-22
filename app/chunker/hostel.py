import logging
from app.services.db_service import get_connection

logger = logging.getLogger(__name__)


def get_hostel_chunks():
    chunks = []
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 1. hostel_buildings - all buildings
        cursor.execute("SELECT * FROM hostel_buildings WHERE office_id = 1")
        buildings = cursor.fetchall()
        for row in buildings:
            text = f"""HOSTEL BUILDING
Building ID: {row.get('id')}
Building Name: {row.get('building_name')}
Building Code: {row.get('building_code') or 'N/A'}
Location: {row.get('location') or 'N/A'}
Total Floors: {row.get('total_floors') or 'N/A'}
Office ID: {row.get('office_id')}
Status: {row.get('status') or 'Active'}"""
            chunks.append({
                "text": text,
                "building_name": row.get('building_name', '').lower(),
                "building_id": str(row.get('id')),
                "office_id": 1,
                "module": "hostel",
                "allowed_roles": ["principal", "admin", "hostel_staff", "hostel_warden"]
            })

        # 2. hostel_rooms - all rooms with building info
        cursor.execute("""
            SELECT 
                hr.*,
                hb.building_name
            FROM hostel_rooms hr
            LEFT JOIN hostel_buildings hb ON hr.building_id = hb.id
            WHERE hr.office_id = 1 OR hb.office_id = 1
        """)
        rooms = cursor.fetchall()
        for row in rooms:
            building = row.get('building_name') or f"Building_{row.get('building_id')}"
            room_beds = row.get('room_beds') or 0
            occupied = row.get('r_category') or 0  # r_category seems to be occupancy count
            available = room_beds - occupied if room_beds > occupied else 0
            # Check building name for ladies/gents classification
            building_lower = building.lower()
            is_ladies = 'ladies' in building_lower or 'female' in building_lower or 'women' in building_lower
            is_gents = 'gents' in building_lower or 'male' in building_lower or 'men' in building_lower
            room_type = "Ladies" if is_ladies else ("Gents" if is_gents else "Mixed")
            
            text = f"""HOSTEL ROOM
Room ID: {row.get('id')}
Room Name/Number: {row.get('room_name')}
Building: {building}
Building ID: {row.get('building_id')}
Floor: {row.get('floor') if row.get('floor') is not None else 'Ground'}
Room Type: {room_type}
Total Beds: {room_beds}
Occupied: {occupied}
Available Beds: {available}
AC: {'Yes' if row.get('ac') and str(row.get('ac')) != '00000000000' else 'No'}
Status: {'Active' if row.get('status') == 1 else 'Inactive'}
Office ID: {row.get('office_id')}"""
            chunks.append({
                "text": text,
                "room_name": str(row.get('room_name', '')).lower(),
                "building_name": building.lower(),
                "room_type": room_type.lower(),
                "office_id": 1,
                "module": "hostel",
                "allowed_roles": ["principal", "admin", "hostel_staff", "hostel_warden"]
            })

        # 3. hostel_masters - all allocations with trainee details
        cursor.execute("""
            SELECT 
                hm.*,
                u.name AS trainee_name,
                u.email,
                u.mobile,
                hb.building_name,
                hr.room_name
            FROM hostel_masters hm
            LEFT JOIN users u ON hm.user_id = u.id
            LEFT JOIN hostel_buildings hb ON hm.building_id = hb.id
            LEFT JOIN hostel_rooms hr ON hm.room_id = hr.id
            WHERE hm.office_id = 1 AND hm.user_id IS NOT NULL
        """)
        allocations = cursor.fetchall()
        for row in allocations:
            name = row.get("trainee_name") or f"Trainee_{row.get('user_id')}"
            building = row.get('building_name') or f"Building_{row.get('building_id')}"
            room = row.get('room_name') or f"Room_{row.get('room_id')}"
            
            text = f"""HOSTEL ALLOCATION
Trainee: {name}
Email: {row.get('email') or 'N/A'}
Phone: {row.get('mobile') or 'N/A'}
Building: {building}
Room: {room}
Beds Allocated: {row.get('beds') or 1}
Check In Date: {row.get('in_date')}
Check Out Date: {row.get('out_date')}
Duration: {row.get('days')} days
Status: {row.get('h_status') or 'Active'}
Remarks: {row.get('remark') or 'None'}
Allocation ID: {row.get('id')}"""
            
            chunks.append({
                "text": text,
                "trainee_name": name.lower(),
                "room_name": room.lower(),
                "building_name": building.lower(),
                "office_id": 1,
                "module": "hostel",
                "allowed_roles": ["principal", "admin", "hostel_staff", "hostel_warden"]
            })

        # 4. hostel_complaint - all complaints
        try:
            cursor.execute("""
                SELECT 
                    hc.*,
                    u.name AS trainee_name,
                    hb.building_name
                FROM hostel_complaint hc
                LEFT JOIN users u ON hc.user_id = u.id
                LEFT JOIN hostel_buildings hb ON hc.building_id = hb.id
                WHERE hc.office_id = 1
            """)
            complaints = cursor.fetchall()
            for row in complaints:
                name = row.get("trainee_name") or f"Trainee_{row.get('user_id')}"
                building = row.get('building_name') or f"Building_{row.get('building_id')}"
                
                text = f"""HOSTEL COMPLAINT
Complaint ID: {row.get('id')}
Trainee: {name}
Building: {building}
Category: {row.get('category') or 'General'}
Description: {row.get('description') or 'N/A'}
Priority: {row.get('priority') or 'Normal'}
Status: {row.get('status') or 'Pending'}
Created: {row.get('created_at')}
Resolved: {row.get('resolved_at') or 'Not resolved'}
Office ID: {row.get('office_id')}"""
                
                chunks.append({
                    "text": text,
                    "trainee_name": name.lower(),
                    "building_name": building.lower(),
                    "office_id": 1,
                    "module": "hostel",
                    "allowed_roles": ["principal", "admin", "hostel_staff", "hostel_warden"]
                })
        except Exception as e:
            logger.warning(f"hostel_complaint table error: {e}")

        # Summary statistics
        cursor.execute("SELECT COUNT(*) as cnt FROM hostel_buildings WHERE office_id = 1")
        building_count = cursor.fetchone().get('cnt', 0)

        cursor.execute("SELECT COUNT(*) as cnt FROM hostel_rooms WHERE office_id = 1")
        room_count = cursor.fetchone().get('cnt', 0)

        cursor.execute("SELECT COUNT(*) as cnt FROM hostel_masters WHERE office_id = 1 AND user_id IS NOT NULL")
        allocation_count = cursor.fetchone().get('cnt', 0)

        # Handle missing hostel_complaint table gracefully
        try:
            cursor.execute("SELECT COUNT(*) as cnt FROM hostel_complaint WHERE office_id = 1")
            complaint_count = cursor.fetchone().get('cnt', 0)
        except Exception:
            complaint_count = 0

        summary = f"""HOSTEL MODULE SUMMARY - Office 1
Total Buildings: {building_count}
Total Rooms: {room_count}
Total Active Allocations: {allocation_count}
Total Complaints: {complaint_count}

All hostel data is now available including buildings, rooms, allocations, and complaints."""

        chunks.append({
            "text": summary,
            "office_id": 1,
            "module": "hostel",
            "allowed_roles": ["principal", "admin", "hostel_staff", "hostel_warden"],
            "trainee_name": "",
            "room_name": "",
            "building_name": ""
        })

        conn.close()
    except Exception as e:
        logger.error(f"Hostel chunker error: {e}")
        if conn:
            conn.close()

    return chunks