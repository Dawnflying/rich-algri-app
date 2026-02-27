from fastapi import APIRouter, HTTPException, Query
from typing import Optional

router = APIRouter()

# 巡田报告 mock 数据
reports_store = [
    {
        "id": 1,
        "type": "drone",
        "title": "无人机巡田_棉田#01_20260615",
        "provider": "蓝天无人机服务",
        "orderNo": "NO20260615001",
        "plotName": "棉田#01",
        "datetime": "2026-06-15 14:20",
        "serviceTime": "2026-06-20 09:00-10:00",
        "plot": "棉田#01",
        "batchPlots": ["棉田#01", "棉田#02", "棉田#03"],
        "reportDate": "2026-06-20",
        "dataSource": None,
        "updateFreq": None,
        "packageCycle": None,
        "chartDesc": "该图展示了棉田#01的作物长势分布情况。绿色区域表示长势良好，黄色区域表示长势一般，红色区域表示长势较差。",
    },
    {
        "id": 2,
        "type": "satellite",
        "title": "卫星遥感巡田_棉田#01_20260610_第4期",
        "provider": "星空遥感服务",
        "orderNo": "NO20260615003",
        "plotName": "棉田#01",
        "datetime": "2026-06-10 09:15",
        "reportDate": "2026-06-20",
        "plot": "棉田#01",
        "batchPlots": ["棉田#01", "棉田#02", "棉田#03"],
        "dataSource": "哨兵-2卫星",
        "updateFreq": "5天/次",
        "packageCycle": "年度套餐",
        "currentPeriod": 4,
        "totalPeriods": 12,
        "chartDesc": "该图展示了棉田#01的作物长势分布情况。基于哨兵-2卫星数据生成，分辨率为10米。绿色区域表示长势良好，黄色区域表示长势一般，红色区域表示长势较差。",
        "legend": [
            {"label": "长势优", "percent": "63.01%", "color": "#4CAF50"},
            {"label": "长势良好", "percent": "23.87%", "color": "#8BC34A"},
            {"label": "长势中", "percent": "10.75%", "color": "#FFEB3B"},
            {"label": "长势差", "percent": "2.37%", "color": "#F44336"},
        ],
    },
    {
        "id": 3,
        "type": "drone",
        "title": "无人机巡田_棉田#01_20260605",
        "provider": "绿源农机服务",
        "orderNo": "NO20260605001",
        "plotName": "棉田#01",
        "datetime": "2026-06-05 16:40",
        "serviceTime": "2026-06-05 16:00-17:00",
        "plot": "棉田#01",
        "batchPlots": ["棉田#01"],
        "reportDate": "2026-06-05",
        "chartDesc": "该图展示了棉田#01的作物长势分布情况。绿色区域表示长势良好，黄色区域表示长势一般，红色区域表示长势较差。",
    },
]


@router.get("")
def list_reports(
    q: Optional[str] = Query(None),
    source: Optional[str] = Query(None, description="all|drone|satellite"),
    timeRange: Optional[str] = Query(None, description="month|3month|year|custom"),
    plot: Optional[str] = Query(None),
):
    items = reports_store
    if q:
        ql = q.lower()
        items = [r for r in items if ql in (r.get("title") or "").lower() or ql in (r.get("orderNo") or "").lower()]
    if source and source != "all":
        items = [r for r in items if r.get("type") == source]
    return items


@router.get("/{report_id}")
def get_report(report_id: int):
    r = next((x for x in reports_store if x["id"] == report_id), None)
    if not r:
        raise HTTPException(status_code=404, detail="报告不存在")
    return r
