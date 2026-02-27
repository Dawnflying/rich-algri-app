from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter()

# 内存存储
orders_store = []

# 状态映射: pending_quote|pending_confirm|pending_payment|in_progress|pending_acceptance|completed|cancelled
STATUS_MAP = {
    "pending_quote": "待报价",
    "pending_confirm": "待确认",
    "pending_payment": "待付款",
    "in_progress": "作业中",
    "pending_acceptance": "待验收",
    "completed": "已完成",
    "cancelled": "已取消",
}


class OrderCreate(BaseModel):
    packageId: int
    packageName: str
    serviceContent: str
    provider: str
    totalArea: float
    pricePerMu: float
    userPrice: Optional[float] = None
    userSettlement: str = "yearend"
    plotCount: int = 0
    serviceType: str = "drone"  # drone|remote|other
    plotNames: Optional[str] = None
    bookingStartTime: Optional[str] = None
    workRequirements: Optional[str] = None


def _make_order(new_id: int, req: OrderCreate) -> dict:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    order_no = f"DRD{datetime.now().strftime('%Y%m%d')}{str(new_id).zfill(3)}"
    final_price = round(req.totalArea * req.pricePerMu, 2)
    platform_fee = round(final_price * 0.05, 2)  # 5% 平台费
    online_pay = round(final_price * 0.2, 2)  # 线上20%
    return {
        "id": new_id,
        "orderNo": order_no,
        "status": "pending_quote",
        "statusText": "待报价",
        "serviceContent": req.serviceContent,
        "provider": req.provider,
        "providerPhone": "138****1234",
        "orderTime": now,
        "bookingStartTime": req.bookingStartTime or now,
        "totalArea": req.totalArea,
        "pricePerMu": req.pricePerMu,
        "finalPrice": final_price,
        "platformFee": platform_fee,
        "onlinePayAmount": round(online_pay + platform_fee * 0.2, 2),
        "userPrice": req.userPrice,
        "userSettlement": req.userSettlement,
        "providerPrice": None,
        "providerPricePerMu": None,
        "providerSettlement": None,
        "providerMessage": None,
        "packageName": req.packageName,
        "packageId": req.packageId,
        "serviceType": req.serviceType,
        "plotCount": req.plotCount,
        "plotNames": req.plotNames or f"地块1、地块2 共{req.plotCount}个地块",
        "workRequirements": req.workRequirements or "农药使用符合规范，覆盖均匀，无漏喷。",
        "countdown": "6天 23小时 45分",
        "executorName": "张师傅",
        "executorPhone": "135****5555",
        "executorLocation": "阳光农场地块1附近",
        "progressCurrent": 10,
        "progressTotal": 20,
        "elapsedTime": "1小时30分钟",
        "remainingTime": "1小时30分钟",
        "plotProgress": [{"name": "地块1", "status": "completed"}, {"name": "地块2", "status": "in_progress", "percent": 50}],
        "timeline": [
            {"time": "2026-06-20 09:00", "event": "订单确认"},
            {"time": "2026-06-21 08:30", "event": "执行人员到达"},
            {"time": "2026-06-21 09:00", "event": "开始作业"},
            {"time": "2026-06-21 11:00", "event": "预计完成"},
        ],
    }


@router.get("")
def list_orders(
    q: Optional[str] = Query(None, description="搜索订单号、套餐名称或服务商"),
    serviceType: Optional[str] = Query(None, description="all|drone|remote|other"),
    statusGroup: Optional[str] = Query(None, description="pending|progress|acceptance|completed"),
):
    _ensure_seed()
    items = sorted(orders_store, key=lambda x: x.get("orderTime", ""), reverse=True)
    if q:
        ql = q.lower()
        items = [o for o in items if ql in (o.get("orderNo") or "").lower() or ql in (o.get("serviceContent") or "").lower() or ql in (o.get("provider") or "").lower()]
    if serviceType and serviceType != "all":
        items = [o for o in items if o.get("serviceType") == serviceType]
    if statusGroup:
        if statusGroup == "pending":
            items = [o for o in items if o.get("status") in ("pending_quote", "pending_confirm", "pending_payment")]
        elif statusGroup == "progress":
            items = [o for o in items if o.get("status") == "in_progress"]
        elif statusGroup == "acceptance":
            items = [o for o in items if o.get("status") == "pending_acceptance"]
        elif statusGroup == "completed":
            items = [o for o in items if o.get("status") in ("completed", "cancelled")]
    return items


@router.get("/{order_id}")
def get_order(order_id: int):
    o = next((x for x in orders_store if x["id"] == order_id), None)
    if not o:
        raise HTTPException(status_code=404, detail="订单不存在")
    return o


@router.post("")
def create_order(req: OrderCreate):
    new_id = max((x["id"] for x in orders_store), default=0) + 1
    order = _make_order(new_id, req)
    orders_store.append(order)
    return {"success": True, "order": order}


class NewQuoteBody(BaseModel):
    price: float = 1350
    pricePerMu: Optional[float] = None
    settlement: str = "spot"
    message: str = ""


@router.post("/{order_id}/new-quote")
def simulate_new_quote(order_id: int, body: Optional[NewQuoteBody] = None):
    body = body or NewQuoteBody()
    o = next((x for x in orders_store if x["id"] == order_id), None)
    if not o:
        raise HTTPException(status_code=404, detail="订单不存在")
    o["status"] = "pending_confirm"
    o["statusText"] = "待确认"
    o["providerPrice"] = body.price
    o["providerPricePerMu"] = body.pricePerMu or (body.price / o["totalArea"] if o.get("totalArea") else None)
    o["providerSettlement"] = body.settlement
    o["providerMessage"] = body.message or "您好, 这是基于面积的核算价, 考虑了飞手成本和设备损耗, 供您参考。"
    o["platformFee"] = round(o.get("providerPrice", 0) * 0.05, 2)
    o["onlinePayAmount"] = round(o.get("providerPrice", 0) * 0.2 + o["platformFee"] * 0.2, 2)
    return {"success": True, "order": o}


@router.post("/{order_id}/accept")
def accept_order(order_id: int):
    o = next((x for x in orders_store if x["id"] == order_id), None)
    if not o:
        raise HTTPException(status_code=404, detail="订单不存在")
    o["status"] = "pending_payment"
    o["statusText"] = "待付款"
    o["finalPrice"] = o.get("providerPrice") or o["finalPrice"]
    o["platformFee"] = round(o["finalPrice"] * 0.05, 2)
    o["onlinePayAmount"] = round(o["finalPrice"] * 0.2 + o["platformFee"] * 0.2, 2)
    o["providerPrice"] = None
    o["providerPricePerMu"] = None
    o["providerSettlement"] = None
    o["providerMessage"] = None
    o["countdown"] = "6天 23小时 45分"
    return {"success": True, "order": o}


@router.post("/{order_id}/pay")
def pay_order(order_id: int):
    o = next((x for x in orders_store if x["id"] == order_id), None)
    if not o:
        raise HTTPException(status_code=404, detail="订单不存在")
    o["status"] = "in_progress"
    o["statusText"] = "作业中"
    o.setdefault("executorName", "张师傅")
    o.setdefault("executorPhone", "135****5555")
    o.setdefault("executorLocation", "阳光农场地块1附近")
    o.setdefault("progressCurrent", 10)
    o.setdefault("progressTotal", 20)
    o.setdefault("elapsedTime", "1小时30分钟")
    o.setdefault("remainingTime", "1小时30分钟")
    o.setdefault("plotProgress", [{"name": "地块1", "status": "completed"}, {"name": "地块2", "status": "in_progress", "percent": 50}])
    o.setdefault("timeline", [
        {"time": "2026-06-20 09:00", "event": "订单确认"},
        {"time": "2026-06-21 08:30", "event": "执行人员到达"},
        {"time": "2026-06-21 09:00", "event": "开始作业"},
        {"time": "2026-06-21 11:00", "event": "预计完成"},
    ])
    return {"success": True, "order": o}


@router.post("/{order_id}/simulate/{target_status}")
def simulate_status(order_id: int, target_status: str):
    o = next((x for x in orders_store if x["id"] == order_id), None)
    if not o:
        raise HTTPException(status_code=404, detail="订单不存在")
    if target_status in STATUS_MAP:
        o["status"] = target_status
        o["statusText"] = STATUS_MAP[target_status]
        if target_status == "in_progress":
            o.setdefault("executorName", "张师傅")
            o.setdefault("executorPhone", "135****5555")
            o.setdefault("executorLocation", "阳光农场地块1附近")
            o.setdefault("progressCurrent", 10)
            o.setdefault("progressTotal", 20)
            o.setdefault("elapsedTime", "1小时30分钟")
            o.setdefault("remainingTime", "1小时30分钟")
            o.setdefault("plotProgress", [{"name": "地块1", "status": "completed"}, {"name": "地块2", "status": "in_progress", "percent": 50}])
            o.setdefault("timeline", [
                {"time": "2026-06-20 09:00", "event": "订单确认"},
                {"time": "2026-06-21 08:30", "event": "执行人员到达"},
                {"time": "2026-06-21 09:00", "event": "开始作业"},
                {"time": "2026-06-21 11:00", "event": "预计完成"},
            ])
        elif target_status == "pending_acceptance":
            o.setdefault("workCompleteTime", "2026-06-20 11:00")
            o.setdefault("totalWorkDuration", "3小时")
            o.setdefault("actualArea", o.get("totalArea", 20))
            o.setdefault("reportSummary", "本次植保作业已完成，喷洒均匀，覆盖面积20亩，符合作业要求。")
            o.setdefault("reportName", o.get("serviceContent"))
            o.setdefault("traceRecords", [
                {"time": "2026-06-20 10:00", "desc": "开始作业，正在喷洒第一块地。", "images": 2, "source": "服务商"},
                {"time": "2026-06-20 09:00", "desc": "到达作业地点，准备开始作业。", "images": 1, "source": "服务商"},
                {"time": "2026-06-20 08:30", "desc": "执行人员已到达阳光农场。", "images": 0, "source": "服务商"},
            ])
    return {"success": True, "order": o}


@router.post("/{order_id}/confirm-complete")
def confirm_complete(order_id: int):
    o = next((x for x in orders_store if x["id"] == order_id), None)
    if not o:
        raise HTTPException(status_code=404, detail="订单不存在")
    o["status"] = "completed"
    o["statusText"] = "已完成"
    o.setdefault("workCompleteTime", "2026-06-20 11:00")
    o.setdefault("totalWorkDuration", "3小时")
    o.setdefault("actualArea", o.get("totalArea", 20))
    o.setdefault("reportSummary", "本次植保作业已完成，喷洒均匀，覆盖面积20亩，符合作业要求。")
    o.setdefault("reportName", o.get("serviceContent", "玉米植保专业打药"))
    o.setdefault("reportGenTime", "2026-06-16 14:00")
    o.setdefault("completionTimeline", [
        {"label": "下单时间", "value": o.get("orderTime", "2026-06-15 10:30")},
        {"label": "确认时间", "value": "2026-06-15 11:00"},
        {"label": "作业时间", "value": "2026-06-16 08:00-12:00"},
        {"label": "完成时间", "value": "2026-06-16 12:00"},
    ])
    o.setdefault("paymentReminder", "请于12月31日前完成线上20%付款及线下80%结算")
    return {"success": True, "order": o}


@router.get("/{order_id}/trace")
def get_order_trace(order_id: int):
    o = next((x for x in orders_store if x["id"] == order_id), None)
    if not o:
        raise HTTPException(status_code=404, detail="订单不存在")
    trace = o.get("traceRecords") or [
        {"time": "2026-06-20 10:00", "desc": "开始作业，正在喷洒第一块地。", "images": 2, "source": "服务商"},
        {"time": "2026-06-20 09:00", "desc": "到达作业地点，准备开始作业。", "images": 1, "source": "服务商"},
        {"time": "2026-06-20 08:30", "desc": "执行人员已到达阳光农场。", "images": 0, "source": "服务商"},
    ]
    return {
        "orderNo": o.get("orderNo"),
        "status": o.get("status"),
        "statusText": o.get("statusText"),
        "updatedAt": o.get("orderTime"),
        "traceRule": "每1小时留痕一次",
        "records": trace,
    }


@router.post("/{order_id}/cancel")
def cancel_order(order_id: int):
    o = next((x for x in orders_store if x["id"] == order_id), None)
    if not o:
        raise HTTPException(status_code=404, detail="订单不存在")
    o["status"] = "cancelled"
    o["statusText"] = "已取消"
    return {"success": True}


# 初始化种子数据
def _init_seed():
    if orders_store:
        return
    from datetime import timedelta
    base = datetime.now()
    for i, (srv, prov, st, plots) in enumerate([
        ("玉米植保专业打药", "丰农植保服务有限公司", "pending_quote", "2个地块"),
        ("小麦收割服务", "丰收农机合作社", "pending_confirm", "1个地块"),
        ("水稻插秧服务", "绿田农机服务", "pending_payment", "3个地块"),
        ("玉米植保专业打药", "丰农植保服务有限公司", "in_progress", "2个地块"),
        ("小麦巡田监测", "蓝天无人机服务", "pending_acceptance", "1个地块"),
        ("玉米无人机巡田", "河北农机服务有限公司", "completed", "3个地块"),
    ], 1):
        dt = (base - timedelta(days=i)).strftime("%Y-%m-%d %H:%M")
        order_no = f"DRD{(base - timedelta(days=i)).strftime('%Y%m%d')}{str(i).zfill(3)}"
        orders_store.append({
            "id": i,
            "orderNo": order_no,
            "status": st,
            "statusText": STATUS_MAP.get(st, st),
            "serviceContent": srv,
            "provider": prov,
            "providerPhone": "138****1234",
            "orderTime": dt,
            "bookingStartTime": dt,
            "totalArea": 20 if i <= 2 else (19.1 if i == 3 else 10),
            "pricePerMu": 60 if i <= 2 else (45 if i == 3 else 15),
            "finalPrice": 1200 if i <= 2 else (859.28 if i == 3 else 286.5),
            "platformFee": 0 if i == 1 else (4.28 if i == 2 else 9.32),
            "onlinePayAmount": 482.4 if i == 3 else None,
            "userPrice": 40 if i == 2 else None,
            "userSettlement": "spot",
            "providerPrice": 45 if i == 2 else None,
            "providerPricePerMu": 45 if i == 2 else None,
            "providerSettlement": "spot" if i == 2 else None,
            "providerMessage": None,
            "userPricePerMu": 40 if i == 2 else None,
            "packageName": srv,
            "packageId": i,
            "serviceType": "drone" if "植保" in srv or "巡田" in srv else "other",
            "plotCount": 2 if i in (1, 4, 5) else (1 if i == 2 else 3),
            "plotNames": "阳光农场地块1、地块2" if i in (1, 4) else ("阳光农场地块3" if i == 2 else ("阳光农场·地块1、地块2 (2个地块)" if i == 5 else "3个地块") if i == 6 else "阳光农场地块4、地块5、地块6"),
            "workRequirements": "农药使用符合规范，覆盖均匀。" if "植保" in srv else "适时收割，秸秆处理。" if "收割" in srv else "秧苗质量符合要求，插秧密度合理。",
            "countdown": "6天 23小时 45分" if i == 3 else None,
            "executorName": "张师傅" if i == 4 else None,
            "executorPhone": "135****5555" if i == 4 else None,
            "executorLocation": "阳光农场地块1附近" if i == 4 else None,
            "progressCurrent": 10 if i == 4 else None,
            "progressTotal": 20 if i == 4 else None,
            "elapsedTime": "1小时30分钟" if i == 4 else None,
            "remainingTime": "1小时30分钟" if i == 4 else None,
            "plotProgress": [{"name": "地块1", "status": "completed"}, {"name": "地块2", "status": "in_progress", "percent": 50}] if i == 4 else None,
            "timeline": [
                {"time": "2026-06-20 09:00", "event": "订单确认"},
                {"time": "2026-06-21 08:30", "event": "执行人员到达"},
                {"time": "2026-06-21 09:00", "event": "开始作业"},
                {"time": "2026-06-21 11:00", "event": "预计完成"},
            ] if i == 4 else None,
            "workCompleteTime": "2026-06-20 11:00" if i == 5 else None,
            "totalWorkDuration": "3小时" if i == 5 else None,
            "actualArea": 20 if i == 5 else None,
            "reportSummary": "本次植保作业已完成，喷洒均匀，覆盖面积20亩，符合作业要求。" if i == 5 else None,
            "reportName": srv if i in (5, 6) else None,
            "reportGenTime": "2026-06-16 14:00" if i in (5, 6) else None,
            "traceRecords": [
                {"time": "2026-06-20 10:00", "desc": "开始作业，正在喷洒第一块地。", "images": 2, "source": "服务商"},
                {"time": "2026-06-20 09:00", "desc": "到达作业地点，准备开始作业。", "images": 1, "source": "服务商"},
                {"time": "2026-06-20 08:30", "desc": "执行人员已到达阳光农场。", "images": 0, "source": "服务商"},
            ] if i in (4, 5, 6) else None,
            "completionTimeline": [
                {"label": "下单时间", "value": "2026-06-15 10:30"},
                {"label": "确认时间", "value": "2026-06-15 11:00"},
                {"label": "作业时间", "value": "2026-06-16 08:00-12:00"},
                {"label": "完成时间", "value": "2026-06-16 12:00"},
            ] if i == 6 else None,
            "paymentReminder": "请于12月31日前完成线上20%付款及线下80%结算" if i == 6 else None,
        })


# 在首次列表请求时初始化种子
def _ensure_seed():
    if not orders_store:
        _init_seed()
