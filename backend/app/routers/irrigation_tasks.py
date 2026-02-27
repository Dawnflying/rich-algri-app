from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter()

tasks_store = [
    {
        "id": 1,
        "name": "夏灌",
        "farmPlot": "东区果园",
        "createDate": "2024-06-01",
        "subTaskCount": 3,
        "duration": "2h20m",
        "totalFlow": "640m³",
        "instantFlow": "300m³/h",
        "status": "pending",
        "statusText": "未开始",
        "subTasks": [
            {"id": 1, "duration": "2h20m", "totalFlow": "640m³", "instantFlow": "300m³/h", "valves": "1支管/2支管/3支管/4支管", "status": "completed", "statusText": "完成"},
            {"id": 2, "duration": "2h20m", "totalFlow": "640m³", "instantFlow": "300m³/h", "valves": "1支管/2支管/3支管/4支管", "status": "running", "statusText": "暂停"},
            {"id": 3, "duration": "2h20m", "totalFlow": "640m³", "instantFlow": "300m³/h", "valves": "1支管/2支管/3支管/4支管", "status": "pending", "statusText": "执行"},
        ],
        "pipeNodes": {"1": {"A": ["completed"]*7, "B": ["completed"]*5+["pending"]*2}, "2": {"A": ["pending"]*7, "B": ["pending"]*7}, "3": {"A": ["pending"]*7, "B": ["pending"]*7}},
    },
    {
        "id": 2,
        "name": "苗期补水",
        "farmPlot": "西区棉田",
        "createDate": "2024-05-28",
        "subTaskCount": 2,
        "duration": "2h20m",
        "totalFlow": "640m³",
        "instantFlow": "300m³/h",
        "status": "running",
        "statusText": "进行中",
        "subTasks": [
            {"id": 1, "duration": "2h20m", "totalFlow": "640m³", "instantFlow": "300m³/h", "valves": "1支管/A", "status": "running", "statusText": "暂停"},
            {"id": 2, "duration": "1h30m", "totalFlow": "450m³", "instantFlow": "300m³/h", "valves": "2支管/B", "status": "pending", "statusText": "执行"},
        ],
        "pipeNodes": {"1": {"A": ["completed"]*7, "B": ["completed"]*5+["pending"]*2}, "2": {"A": ["irrigating"]*7, "B": ["pending"]*7}, "3": {"A": ["pending"]*7, "B": ["pending"]*7}},
    },
    {
        "id": 3,
        "name": "春季灌溉",
        "farmPlot": "南区果园",
        "createDate": "2024-04-15",
        "subTaskCount": 4,
        "duration": "2h20m",
        "totalFlow": "640m³",
        "instantFlow": "300m³/h",
        "status": "completed",
        "statusText": "已完成",
        "subTasks": [
            {"id": 1, "duration": "2h20m", "totalFlow": "640m³", "instantFlow": "300m³/h", "valves": "1支管/A", "status": "completed", "statusText": "完成"},
            {"id": 2, "duration": "2h20m", "totalFlow": "640m³", "instantFlow": "300m³/h", "valves": "2支管/A", "status": "completed", "statusText": "完成"},
            {"id": 3, "duration": "2h20m", "totalFlow": "640m³", "instantFlow": "300m³/h", "valves": "3支管/A", "status": "completed", "statusText": "完成"},
            {"id": 4, "duration": "2h20m", "totalFlow": "640m³", "instantFlow": "300m³/h", "valves": "1支管/B", "status": "completed", "statusText": "完成"},
        ],
        "pipeNodes": {"1": {"A": ["completed"]*7, "B": ["completed"]*7}, "2": {"A": ["completed"]*7, "B": ["completed"]*7}, "3": {"A": ["completed"]*7, "B": ["completed"]*7}},
    },
]


class TaskCreate(BaseModel):
    name: str
    farmPlot: str
    date: str
    subTasks: List[dict]


@router.get("")
def list_tasks(farm: Optional[str] = None, plot: Optional[str] = None):
    items = tasks_store
    if farm and farm != "all":
        items = [t for t in items if t.get("farmPlot", "").startswith(farm)]
    return items


@router.get("/{task_id}")
def get_task(task_id: int):
    t = next((x for x in tasks_store if x["id"] == task_id), None)
    if not t:
        raise HTTPException(status_code=404, detail="任务不存在")
    return t


@router.post("")
def create_task(req: TaskCreate):
    new_id = max((x["id"] for x in tasks_store), default=0) + 1
    task = {
        "id": new_id,
        "name": req.name or "新灌溉任务",
        "farmPlot": req.farmPlot,
        "createDate": req.date or datetime.now().strftime("%Y-%m-%d"),
        "subTaskCount": len(req.subTasks),
        "duration": "2h20m",
        "totalFlow": "640m³",
        "instantFlow": "300m³/h",
        "status": "pending",
        "statusText": "未开始",
        "subTasks": [{"id": i+1, "duration": st.get("duration", "2h20m"), "totalFlow": st.get("totalFlow", "640m³"), "instantFlow": st.get("instantFlow", "300m³/h"), "valves": st.get("valves", "1支管/A"), "status": "pending", "statusText": "执行"} for i, st in enumerate(req.subTasks)],
        "pipeNodes": {"1": {"A": ["pending"]*7, "B": ["pending"]*7}, "2": {"A": ["pending"]*7, "B": ["pending"]*7}, "3": {"A": ["pending"]*7, "B": ["pending"]*7}},
    }
    tasks_store.append(task)
    return {"success": True, "task": task}


@router.delete("/{task_id}")
def delete_task(task_id: int):
    global tasks_store
    tasks_store = [t for t in tasks_store if t["id"] != task_id]
    return {"success": True}
