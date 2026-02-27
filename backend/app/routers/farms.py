from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.store import farms as store_farms

router = APIRouter()


class FarmCreate(BaseModel):
    province: str = ""
    city: str = ""
    county: str = ""
    town: str = ""
    isEnterprise: bool = False
    enterpriseName: str = ""
    enterpriseAddress: str = ""
    contact: str = ""
    phone: str = ""
    name: str = ""


@router.get("")
def list_farms():
    return store_farms


@router.get("/{farm_id}")
def get_farm(farm_id: int):
    f = next((x for x in store_farms if x["id"] == farm_id), None)
    if not f:
        raise HTTPException(status_code=404, detail="农场不存在")
    return f


@router.post("")
def create_farm(req: FarmCreate):
    if not req.name.strip():
        return {"success": False, "message": "请输入农场名称"}
    region = " ".join(filter(None, [req.province, req.city, req.county, req.town]))
    new_id = max((x["id"] for x in store_farms), default=0) + 1
    new_farm = {
        "id": new_id,
        "name": req.name.strip(),
        "region": region or "未设置",
        "province": req.province,
        "city": req.city,
        "county": req.county,
        "town": req.town,
        "isEnterprise": req.isEnterprise,
        "enterpriseName": req.enterpriseName,
        "enterpriseAddress": req.enterpriseAddress,
        "contact": req.contact,
        "phone": req.phone,
        "cropType": "棉花农场",
        "fieldCount": 0,
        "totalArea": 0,
        "cropVariety": 0,
        "location": region or "未设置",
        "fields": [],
    }
    store_farms.append(new_farm)
    return {"success": True, "farm": new_farm}
