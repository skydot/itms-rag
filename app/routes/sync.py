from fastapi import APIRouter, HTTPException, Query
import logging

from app.services.embedder import get_embedding
from app.services.qdrant_service import (
    create_collection,
    upsert_data_stable_id,
    delete_by_module,
    delete_by_office,
    delete_by_module_and_office,
    get_collection_info,
    recreate_collection as qdrant_recreate_collection
)

from app.chunker.exam import get_exam_chunks
from app.chunker.hostel import get_hostel_chunks
from app.chunker.attendance import get_attendance_chunks
from app.chunker.trainee import get_trainee_chunks
from app.chunker.trainee_leave import get_trainee_leave_chunks
from app.chunker.course_nominee import get_course_nominee_chunks
from app.chunker.course import get_course_chunks
from app.chunker.complaint import get_complaint_chunks
from app.chunker.timetable import get_timetable_chunks
from app.chunker.faculty import get_faculty_chunks
from app.chunker.library import get_library_chunks
from app.chunker.mess import get_mess_chunks
from app.chunker.vehicle import get_vehicle_chunks
from app.chunker.meeting import get_meeting_chunks
from app.chunker.seminar import get_seminar_chunks
from app.chunker.inspection import get_inspection_chunks
from app.chunker.sports import get_sports_chunks
from app.chunker.pass_eq import get_pass_eq_chunks
from app.chunker.field_study_tour import get_field_study_tour_chunks
from app.chunker.master_admin import get_master_admin_chunks

router = APIRouter()
logger = logging.getLogger(__name__)

CHUNKER_REGISTRY = {
    "exam": get_exam_chunks,
    "hostel": get_hostel_chunks,
    "attendance": get_attendance_chunks,
    "trainee": get_trainee_chunks,
    "trainee_leave": get_trainee_leave_chunks,
    "course_nominee": get_course_nominee_chunks,
    "course": get_course_chunks,
    "complaint": get_complaint_chunks,
    "timetable": get_timetable_chunks,
    "faculty": get_faculty_chunks,
    "library": get_library_chunks,
    "mess": get_mess_chunks,
    "vehicle": get_vehicle_chunks,
    "meeting": get_meeting_chunks,
    "seminar": get_seminar_chunks,
    "inspection": get_inspection_chunks,
    "sports": get_sports_chunks,
    "pass_eq": get_pass_eq_chunks,
    "field_study_tour": get_field_study_tour_chunks,
    "master_admin": get_master_admin_chunks,
}

def _validate_chunk(chunk):
    if not chunk.get("text"):
        return False
    if not chunk.get("module"):
        return False
    if "allowed_roles" not in chunk or not isinstance(chunk["allowed_roles"], list):
        return False
    return True

def _sync_module(module: str, office_id: int | None = None, limit: int | None = None):
    logger.info("[Sync] starting module=%s office_id=%s limit=%s", module, office_id, limit)
    if module not in CHUNKER_REGISTRY:
        raise HTTPException(status_code=400, detail=f"Unknown module: {module}")

    if office_id:
        delete_by_module_and_office(module, office_id)
    else:
        delete_by_module(module)

    chunks = CHUNKER_REGISTRY[module](office_id=office_id, limit=limit)
    
    upserted = 0
    for i, chunk in enumerate(chunks):
        if not _validate_chunk(chunk):
            logger.warning("[Sync] skipping invalid chunk module=%s index=%s", module, i)
            continue
            
        vector = get_embedding(chunk["text"])
        upsert_data_stable_id(module, i, vector, chunk)
        upserted += 1

    logger.info("[Sync] completed module=%s chunks=%s upserted=%s", module, len(chunks), upserted)
    return {"chunks": len(chunks), "upserted": upserted}

@router.post("/sync/all")
def sync_all(office_id: int | None = Query(None), limit: int | None = Query(None)):
    create_collection()
    modules_result = {}

    for module in CHUNKER_REGISTRY:
        try:
            res = _sync_module(module, office_id=office_id, limit=limit)
            modules_result[module] = res
        except Exception as e:
            logger.error(f"Failed to sync {module}: {e}")
            modules_result[module] = {"error": str(e)}

    return {
        "status": "success",
        "modules": modules_result
    }

@router.post("/sync/recreate-collection")
def recreate_collection():
    try:
        qdrant_recreate_collection()
        return {"status": "success", "message": "Collection recreated"}
    except Exception as e:
        logger.error(f"Failed to recreate collection: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sync/{module_name}")
def sync_module(module_name: str, office_id: int | None = Query(None), limit: int | None = Query(None)):
    if module_name == "all" or module_name == "recreate-collection":
        raise HTTPException(status_code=400, detail="Invalid module name")
        
    create_collection()
    res = _sync_module(module_name, office_id=office_id, limit=limit)
    return {
        "status": "success",
        "modules": {
            module_name: res
        }
    }

@router.get("/sync/modules")
def list_modules():
    return {"modules": list(CHUNKER_REGISTRY.keys())}

@router.get("/sync/status")
def sync_status():
    try:
        info = get_collection_info()
        return {"status": "ok", "collection": info}
    except Exception as e:
        return {"status": "error", "message": str(e)}