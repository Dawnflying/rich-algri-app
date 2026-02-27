from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any, Optional

from app.store import farmlogs, fields as store_fields

router = APIRouter()


class FarmlogCreate(BaseModel):
    fieldId: int
    farmId: Optional[int] = None
    date: str
    time: str = ""
    type: str
    data: dict[str, Any]
    photos: list[str] = []
    notes: str = ""


@router.get("")
def list_farmlogs(
    type_filter: str = "all",
    search: str = "",
    start_date: str = "",
    end_date: str = "",
    field_id: str = "",
    crop: str = "",
):
    result = farmlogs
    if type_filter != "all":
        result = [r for r in result if r["type"] == type_filter]
    if search:
        def match(r):
            s = search.lower()
            if s in (r.get("fieldName") or "").lower(): return True
            if s in (r.get("recorder") or "").lower(): return True
            if s in (r.get("notes") or "").lower(): return True
            d = r.get("data") or {}
            if isinstance(d.get("content"), str) and s in d["content"].lower(): return True
            return False
        result = [r for r in result if match(r)]
    if start_date:
        result = [r for r in result if (r.get("date") or "") >= start_date]
    if end_date:
        result = [r for r in result if (r.get("date") or "") <= end_date]
    if field_id:
        fid = int(field_id) if field_id.isdigit() else None
        if fid is not None:
            result = [r for r in result if r.get("fieldId") == fid]
    if crop:
        result = [r for r in result if (r.get("crop") or "") == crop]
    return sorted(result, key=lambda x: (x.get("date") or "", x.get("time") or ""), reverse=True)


@router.get("/{log_id}")
def get_farmlog(log_id: int):
    r = next((x for x in farmlogs if x["id"] == log_id), None)
    if not r:
        return {"error": "记录不存在"}
    return r


@router.post("")
def create_farmlog(req: FarmlogCreate):
    field = next((f for f in store_fields if f["id"] == req.fieldId), None)
    if not field:
        return {"success": False, "message": "地块不存在"}
    new_id = max((x["id"] for x in farmlogs), default=0) + 1
    new_log = {
        "id": new_id,
        "type": req.type,
        "fieldId": req.fieldId,
        "fieldName": field["name"],
        "farm": field.get("farm", "示范农场"),
        "farmId": req.farmId or field.get("farmId"),
        "crop": field["crop"],
        "date": req.date,
        "time": req.time,
        "recorder": "王农户",
        "data": req.data,
        "photos": req.photos,
        "notes": req.notes,
    }
    farmlogs.insert(0, new_log)
    return {"success": True, "farmlog": new_log}


@router.put("/{log_id}")
def update_farmlog(log_id: int, req: FarmlogCreate):
    field = next((f for f in store_fields if f["id"] == req.fieldId), None)
    if not field:
        return {"success": False, "message": "地块不存在"}
    r = next((x for x in farmlogs if x["id"] == log_id), None)
    if not r:
        return {"success": False, "message": "记录不存在"}
    r.update({
        "type": req.type,
        "fieldId": req.fieldId,
        "fieldName": field["name"],
        "farm": field.get("farm", "示范农场"),
        "crop": field["crop"],
        "date": req.date,
        "data": req.data,
        "photos": req.photos,
        "notes": req.notes,
    })
    return {"success": True, "farmlog": r}


@router.delete("/{log_id}")
def delete_farmlog(log_id: int):
    global farmlogs
    farmlogs = [r for r in farmlogs if r["id"] != log_id]
    return {"success": True}
