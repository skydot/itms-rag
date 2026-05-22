import logging
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchAny,
    MatchValue,
    PointStruct,
    VectorParams,
)
from fastapi import HTTPException

client = QdrantClient("localhost", port=6333)

COLLECTION_NAME = "trms_data"


def create_collection():
    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if COLLECTION_NAME not in names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )


def insert_data(point_id: int, vector, payload: dict):
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=point_id,
                vector=vector,
                payload=payload
            )
        ],
    )

def get_all_points(limit=200):
    result = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=limit,
        with_payload=True,
        with_vectors=False
    )
    return result[0]
def search_data(vector, limit=5):
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        limit=limit,
    )


    return results.points


def search_data_filtered(vector, office_id, user_role, module=None, limit=10):
    must_conditions = [
        FieldCondition(
            key="office_id",
            match=MatchValue(value=office_id),
        ),
        FieldCondition(
            key="allowed_roles",
            match=MatchAny(any=[user_role]),
        ),
    ]
    
    # Add module filter if specified
    if module:
        must_conditions.append(
            FieldCondition(
                key="module",
                match=MatchValue(value=module),
            )
        )

    query_filter = Filter(must=must_conditions)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        query_filter=query_filter,
        limit=limit,
    )

    return results.points


# Module ID offsets for stable point IDs
MODULE_ID_OFFSETS = {
    "exam": 1_000_000,
    "hostel": 2_000_000,
    "attendance": 3_000_000,
    "trainee": 4_000_000,
    "trainee_leave": 5_000_000,
    "course_nominee": 6_000_000,
}


def upsert_data_stable_id(module: str, index: int, vector, payload: dict):
    """Upsert with stable integer ID based on module offset"""
    offset = MODULE_ID_OFFSETS.get(module, 9_000_000)
    point_id = offset + index
    
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=point_id,
                vector=vector,
                payload=payload
            )
        ],
    )
    return point_id


def delete_by_module(module: str):
    """Delete all points for a module using module filter"""
    try:
        client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=Filter(
                must=[
                    FieldCondition(key="module", match=MatchValue(value=module))
                ]
            )
        )
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.warning(f"Delete by module failed (may be empty): {e}")


def delete_by_office(office_id: int):
    """Delete all points for an office"""
    try:
        client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=Filter(
                must=[
                    FieldCondition(key="office_id", match=MatchValue(value=office_id))
                ]
            )
        )
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.warning(f"Delete by office failed (may be empty): {e}")


def delete_by_module_and_office(module: str, office_id: int):
    """Delete points for specific module and office"""
    try:
        client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=Filter(
                must=[
                    FieldCondition(key="module", match=MatchValue(value=module)),
                    FieldCondition(key="office_id", match=MatchValue(value=office_id))
                ]
            )
        )
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.warning(f"Delete by module/office failed (may be empty): {e}")


def get_collection_info():
    """Get collection statistics"""
    info = client.get_collection(COLLECTION_NAME)
    return {
        "name": COLLECTION_NAME,
        "vectors_count": info.vectors_count,
        "points_count": info.points_count,
        "status": info.status
    }