from fastapi import APIRouter

from app.store import ndvi_data

router = APIRouter()


@router.get("/{field_key}")
def get_ndvi(field_key: str):
    key = field_key.upper()
    if key not in ndvi_data:
        return {"error": "地块不存在"}
    return ndvi_data[key]
