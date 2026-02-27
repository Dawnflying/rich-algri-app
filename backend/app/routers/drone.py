from fastapi import APIRouter
from pydantic import BaseModel

from app.store import tasks, fields as store_fields

router = APIRouter()


class TaskCreate(BaseModel):
    field: str
    type: str = "多光谱巡田（NDVI）"
    alt: int = 90
    overlap: int = 80


@router.get("/tasks")
def list_tasks(status: str | None = None):
    if status and status != "all":
        return [t for t in tasks if t["status"] == status]
    return tasks


@router.post("/tasks")
def create_task(req: TaskCreate):
    if not req.field:
        return {"success": False, "message": "请选择作业地块"}
    f = next((x for x in store_fields if x["name"] == req.field), None)
    area = f["area"] if f else 0
    from datetime import datetime
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M")
    new_task = {
        "id": max((t["id"] for t in tasks), default=0) + 1,
        "field": req.field,
        "type": req.type,
        "status": "pending",
        "date": date_str,
        "progress": 0,
        "photos": 0,
        "area": area,
    }
    tasks.insert(0, new_task)
    return {"success": True, "task": new_task}
