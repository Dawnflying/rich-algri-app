from fastapi import APIRouter

from app.store import alerts

router = APIRouter()


@router.get("")
def list_alerts(filter_type: str = "all"):
    if filter_type == "all":
        return alerts
    return [a for a in alerts if a["type"] == filter_type]


@router.post("/{alert_id}/read")
def read_alert(alert_id: int):
    a = next((x for x in alerts if x["id"] == alert_id), None)
    if a:
        a["read"] = True
    return {"success": True}


@router.post("/read-all")
def mark_all_read():
    for a in alerts:
        a["read"] = True
    return {"success": True}
