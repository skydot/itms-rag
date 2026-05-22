from fastapi import APIRouter, HTTPException
import logging

from app.services.embedder import get_embedding
from app.services.qdrant_service import (
    create_collection,
    upsert_data_stable_id,
    delete_by_module,
    delete_by_office,
    delete_by_module_and_office,
    get_collection_info
)
from app.chunker.exam import get_exam_chunks
from app.chunker.hostel import get_hostel_chunks
from app.chunker.attendance import get_attendance_chunks
from app.chunker.trainee import get_trainee_chunks
from app.chunker.trainee_leave import get_trainee_leave_chunks
from app.chunker.course_nominee import get_course_nominee_chunks

router = APIRouter()
logger = logging.getLogger(__name__)

# Registry of all available chunkers
CHUNKER_REGISTRY = {
    "exam": get_exam_chunks,
    "hostel": get_hostel_chunks,
    "attendance": get_attendance_chunks,
    "trainee": get_trainee_chunks,
    "trainee_leave": get_trainee_leave_chunks,
    "course_nominee": get_course_nominee_chunks,
}


def _sync_module(module: str, delete_existing: bool = True, office_id: int = None):
    """Internal: sync a single module"""
    if module not in CHUNKER_REGISTRY:
        raise HTTPException(status_code=400, detail=f"Unknown module: {module}")

    if delete_existing:
        if office_id:
            delete_by_module_and_office(module, office_id)
        else:
            delete_by_module(module)

    chunks = CHUNKER_REGISTRY[module]()
    if office_id:
        chunks = [c for c in chunks if c.get("office_id") == office_id]

    logger.info(f"[{module}] Retrieved {len(chunks)} chunks")

    for i, chunk in enumerate(chunks):
        vector = get_embedding(chunk["text"])
        point_id = upsert_data_stable_id(module, i, vector, chunk)

    return {"module": module, "chunks_synced": len(chunks), "office_id": office_id}


@router.post("/sync/all")
def sync_all():
    """Sync all modules for all offices"""
    create_collection()
    results = []
    total = 0

    for module in CHUNKER_REGISTRY:
        try:
            result = _sync_module(module, delete_existing=True)
            results.append(result)
            total += result["chunks_synced"]
        except Exception as e:
            logger.error(f"Failed to sync {module}: {e}")
            results.append({"module": module, "error": str(e)})

    return {
        "status": "ok",
        "message": f"Synced {total} total records across {len(CHUNKER_REGISTRY)} modules",
        "details": results
    }


@router.post("/sync/module/{module}")
def sync_module(module: str, office_id: int = None):
    """Sync a specific module (optionally filtered by office)"""
    create_collection()
    result = _sync_module(module, delete_existing=True, office_id=office_id)
    return {"status": "ok", **result}


@router.post("/sync/office/{office_id}")
def sync_office(office_id: int):
    """Sync all modules for a specific office"""
    create_collection()
    results = []
    total = 0

    for module in CHUNKER_REGISTRY:
        try:
            result = _sync_module(module, delete_existing=False, office_id=office_id)
            results.append(result)
            total += result["chunks_synced"]
        except Exception as e:
            logger.error(f"Failed to sync {module} for office {office_id}: {e}")
            results.append({"module": module, "office_id": office_id, "error": str(e)})

    return {
        "status": "ok",
        "message": f"Synced {total} records for office {office_id}",
        "details": results
    }


@router.post("/sync/module/{module}/office/{office_id}")
def sync_module_office(module: str, office_id: int):
    """Sync specific module for specific office"""
    create_collection()
    result = _sync_module(module, delete_existing=True, office_id=office_id)
    return {"status": "ok", **result}


@router.get("/sync/modules")
def list_modules():
    """List all available sync modules"""
    return {"modules": list(CHUNKER_REGISTRY.keys())}


@router.get("/sync/status")
def sync_status():
    """Get collection status"""
    try:
        info = get_collection_info()
        return {"status": "ok", "collection": info}
    except Exception as e:
        return {"status": "error", "message": str(e)}