from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List, Any

from app.store import fields as store_fields, farms as store_farms

router = APIRouter()


class FieldCreate(BaseModel):
    name: str
    area: float = 0
    crop: str
    location: str = ""
    planting: str = "常规种植"
    supervisor: str = ""
    farmId: Optional[int] = None
    cropSeed: str = ""
    boundary: Optional[List[dict]] = None
    plantHoleCount: Optional[int] = None
    dripFlow: Optional[float] = None
    holeSpacing: str = ""
    waterSource: str = ""
    trenchMeter: Optional[float] = None
    trenchCm: Optional[float] = None
    soilType: str = ""


@router.get("")
def list_fields():
    return store_fields


@router.get("/{field_id}")
def get_field(field_id: int):
    f = next((x for x in store_fields if x["id"] == field_id), None)
    if not f:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="地块不存在")
    return f


@router.post("")
def add_field(f: FieldCreate):
    if not f.name or not f.crop:
        return {"success": False, "message": "请填写完整地块信息"}
    farm_name = "示范农场"
    if f.farmId:
        farm = next((x for x in store_farms if x["id"] == f.farmId), None)
        if farm:
            farm_name = farm["name"]
    area = f.area if f.area and f.area > 0 else 0
    new_id = max((x["id"] for x in store_fields), default=0) + 1
    new_field = {
        "id": new_id,
        "name": f.name,
        "area": area,
        "crop": f.crop,
        "planting": f.planting or "常规种植",
        "status": "pending_irrigate",
        "statusText": "待灌溉",
        "statusDuration": "",
        "supervisor": f.supervisor or "",
        "farm": farm_name,
        "location": f.location or "待定",
        "boundary": f.boundary,
        "cropSeed": f.cropSeed or "",
        "plantHoleCount": f.plantHoleCount,
        "dripFlow": f.dripFlow,
        "holeSpacing": f.holeSpacing or "",
        "waterSource": f.waterSource or "",
        "soilType": f.soilType or "",
    }
    store_fields.append(new_field)
    # 若指定了 farmId，同步到农场的 fields 列表
    if f.farmId:
        farm = next((x for x in store_farms if x["id"] == f.farmId), None)
        if farm:
            farm["fields"] = farm.get("fields") or []
            farm["fields"].append({
                "id": new_id,
                "name": f.name,
                "area": area,
                "crop": f.crop,
                "updatedAt": __import__("datetime").datetime.now().strftime("%Y-%m-%d"),
            })
            farm["fieldCount"] = len(farm["fields"])
            farm["totalArea"] = sum(x.get("area", 0) for x in farm["fields"])
    return {"success": True, "field": new_field}
