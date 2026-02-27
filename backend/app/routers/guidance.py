from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()

guidance_store = [
    {
        "id": 1,
        "badge": "new",
        "badgeText": "新",
        "time": "今天 09:30",
        "plotName": "地块1",
        "issue": "棉花生长问题",
        "photoCount": 3,
        "status": "unprocessed",
        "statusText": "未处理",
        "expert": "李农师",
        "read": False,
        "farm": "农场A",
        "fieldId": 1,
        "createTime": "2024-01-20 09:30",
        "farmer": "张三",
        "provider": "李四",
        "providerLabel": "农资服务商",
        "messages": [
            {"role": "farmer", "name": "农户 - 张三", "time": "2024-01-20 09:30", "content": "玉米叶片发黄,疑似病虫害,需要专业指导。最近一周天气较热,浇水正常,施肥也按照标准进行的。", "photos": 2, "record": "玉米病虫害防治 (2024-01-18)"},
            {"role": "provider", "name": "服务商 - 李四", "time": "2024-01-20 14:30", "content": "您好,根据您提供的图片和描述,玉米叶片发黄可能是由以下原因导致的:\n1. 病虫害:可能是玉米螟或蚜虫侵害\n2. 营养缺乏:可能是氮元素不足\n3. 水分管理:虽然您说浇水正常,但可能存在浇水不均匀的情况\n\n建议措施:\n1. 使用吡虫啉+戊唑醇混合喷施,防治病虫害\n2. 追施尿素,每亩10-15公斤\n3. 合理灌溉,保持土壤湿润但不过湿\n\n如有其他问题随时联系我们", "photos": 1},
        ],
        "replied": True,
    },
    {
        "id": 2,
        "badge": "read",
        "badgeText": "已读",
        "time": "昨天 14:20",
        "plotName": "棉田#02",
        "issue": "病虫害防治",
        "photoCount": 1,
        "status": "processed",
        "statusText": "已处理",
        "expert": "王技师",
        "read": True,
        "farm": "幸福农场",
        "fieldId": 2,
        "createTime": "2024-01-19 14:20",
        "farmer": "张三",
        "provider": "王技师",
        "messages": [],
        "replied": True,
    },
    {
        "id": 3,
        "badge": "unprocessed",
        "badgeText": "未处理",
        "time": "06-12 10:15",
        "plotName": "棉田#01",
        "issue": "土壤肥力问题",
        "photoCount": 2,
        "status": "unprocessed",
        "statusText": "未处理",
        "expert": "张专家",
        "read": False,
        "farm": "幸福农场",
        "fieldId": 5,
        "createTime": "2024-06-12 10:15",
        "farmer": "张三",
        "provider": "张专家",
        "messages": [],
        "replied": False,
    },
]


class GuidanceCreate(BaseModel):
    farmId: int
    fieldId: int
    farmName: str
    fieldName: str
    guidanceType: str
    personId: str
    personName: str
    problem: str
    photos: List[str] = []
    recordId: Optional[int] = None


@router.get("")
def list_guidance(
    filter_type: Optional[str] = Query(None, description="all|unread|unprocessed"),
):
    items = guidance_store
    if filter_type == "unread":
        items = [g for g in items if not g.get("read")]
    elif filter_type == "unprocessed":
        items = [g for g in items if g.get("status") == "unprocessed"]
    return items


@router.get("/{guidance_id}")
def get_guidance(guidance_id: int):
    g = next((x for x in guidance_store if x["id"] == guidance_id), None)
    if not g:
        raise HTTPException(status_code=404, detail="建议不存在")
    g["read"] = True
    g["badge"] = "read"
    g["badgeText"] = "已读"
    return g


@router.post("")
def create_guidance(req: GuidanceCreate):
    new_id = max((x["id"] for x in guidance_store), default=0) + 1
    g = {
        "id": new_id,
        "badge": "new",
        "badgeText": "新",
        "time": "今天 " + __import__("datetime").datetime.now().strftime("%H:%M"),
        "plotName": req.fieldName,
        "issue": req.guidanceType or "问题咨询",
        "photoCount": len(req.photos),
        "status": "unprocessed",
        "statusText": "未处理",
        "expert": req.personName,
        "read": False,
        "farm": req.farmName,
        "fieldId": req.fieldId,
        "createTime": __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M"),
        "farmer": "张三",
        "provider": req.personName,
        "messages": [{"role": "farmer", "name": "农户 - 张三", "time": __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M"), "content": req.problem, "photos": len(req.photos), "record": None}],
        "replied": False,
    }
    guidance_store.append(g)
    return {"success": True, "guidance": g}
