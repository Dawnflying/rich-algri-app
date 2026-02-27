from fastapi import APIRouter

from app.store import valves

router = APIRouter()


@router.get("/valves")
def list_valves():
    return valves


@router.post("/valves/{valve_id}/toggle")
def toggle_valve(valve_id: int):
    import random
    v = next((x for x in valves if x["id"] == valve_id), None)
    if not v:
        return {"success": False}
    v["open"] = not v["open"]
    v["flow"] = round(1.5 + random.random(), 1) if v["open"] else 0
    return {"success": True, "valve": v}
