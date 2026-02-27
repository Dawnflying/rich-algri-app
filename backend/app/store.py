"""
内存数据存储（演示用，可后续替换为数据库）
"""
from typing import Any

# 用户
user = {"name": "王大明", "phone": "13800138000", "role": "农户端·大总管"}

# 农场
farms = [
    {
        "id": 1,
        "name": "幸福农场",
        "region": "新疆维吾尔自治区 石河子市",
        "province": "新疆维吾尔自治区",
        "city": "石河子市",
        "county": "",
        "town": "",
        "isEnterprise": False,
        "enterpriseName": "",
        "enterpriseAddress": "",
        "contact": "",
        "phone": "",
        "cropType": "棉花农场",
        "fieldCount": 8,
        "totalArea": 500,
        "cropVariety": 1,
        "location": "新疆维吾尔自治区石河子市",
        "fields": [
            {"id": 1, "name": "地块 1", "area": 50, "crop": "棉花", "updatedAt": "2024-06-01"},
            {"id": 2, "name": "地块 2", "area": 30, "crop": "棉花", "updatedAt": "2024-05-28"},
            {"id": 3, "name": "地块 3", "area": 40, "crop": "棉花", "updatedAt": "2024-05-25"},
            {"id": 5, "name": "大本营南", "area": 80, "crop": "棉花", "updatedAt": "2026-06-15"},
        ],
    },
]

# 地块（农户版首页用）
# center: [lng, lat] 高德地图中心点；boundary: [[lng,lat],...] 地块边界多边形（可选）
fields = [
    {"id": 1, "name": "1号地块", "area": 50, "crop": "棉花", "planting": "一膜六行", "status": "pending_irrigate", "statusText": "待灌溉", "statusDuration": "", "supervisor": "张三", "farm": "幸福农场", "location": "新疆维吾尔自治区 石河子市", "ndvi": 0.68, "cropSeed": "新陆早56号", "dripFlow": 0.75, "holeSpacing": "30厘米", "waterSource": "井水", "trenchMeter": 20, "trenchCm": 0, "soilType": "壤土", "saltAlkali": "不含盐碱", "center": [86.0411, 44.3059], "boundary": [[86.035, 44.302], [86.048, 44.302], [86.048, 44.312], [86.035, 44.312]]},
    {"id": 2, "name": "西南地块", "area": 30, "crop": "小麦", "planting": "常规种植", "status": "irrigating", "statusText": "灌溉中", "statusDuration": "2h30m", "supervisor": "李四", "farm": "示范农场", "location": "西南区", "ndvi": 0.72, "center": [86.02, 44.28], "boundary": [[86.015, 44.275], [86.025, 44.275], [86.025, 44.285], [86.015, 44.285]]},
    {"id": 3, "name": "中心地块", "area": 40, "crop": "玉米", "planting": "一膜两行", "status": "working", "statusText": "作业中", "statusDuration": "1h15m", "supervisor": "张三", "farm": "示范农场", "location": "中心区", "ndvi": 0.41, "center": [86.05, 44.32], "boundary": [[86.042, 44.315], [86.058, 44.315], [86.058, 44.325], [86.042, 44.325]]},
    {"id": 4, "name": "南地块", "area": 25, "crop": "番茄", "planting": "常规种植", "status": "pending_irrigate", "statusText": "待灌溉", "statusDuration": "", "supervisor": "王五", "farm": "示范农场", "location": "南区", "ndvi": 0.65, "center": [86.03, 44.26], "boundary": [[86.025, 44.255], [86.035, 44.255], [86.035, 44.265], [86.025, 44.265]]},
    {"id": 5, "name": "大本营南", "area": 80, "crop": "棉花", "planting": "一膜六行", "status": "working", "statusText": "作业中", "statusDuration": "", "supervisor": "王农户", "farm": "幸福农场", "farmId": 1, "location": "121团-大本营", "ndvi": 0.72, "center": [86.08, 44.29], "boundary": [[86.07, 44.28], [86.09, 44.28], [86.09, 44.30], [86.07, 44.30]]},
]

# 无人机任务
tasks = [
    {"id": 1, "field": "A区·小麦", "type": "多光谱巡田", "status": "flying", "date": "2024-01-15 09:30", "progress": 62, "photos": 124, "area": 320},
    {"id": 2, "field": "C区·玉米", "type": "病害检测", "status": "done", "date": "2024-01-14 14:20", "progress": 100, "photos": 210, "area": 410},
    {"id": 3, "field": "B区·水稻", "type": "RGB正射图", "status": "pending", "date": "2024-01-16 08:00", "progress": 0, "photos": 0, "area": 280},
    {"id": 4, "field": "D区·大豆", "type": "多光谱巡田", "status": "done", "date": "2024-01-13 10:15", "progress": 100, "photos": 180, "area": 270},
]

# 预警
alerts = [
    {"id": 1, "type": "warn", "level": "red", "icon": "🌡️", "title": "C区玉米高温预警", "desc": "当前温度 38.2°C，超出警戒值", "time": "10分钟前", "read": False},
    {"id": 2, "type": "warn", "level": "amber", "icon": "💧", "title": "B区水稻灌溉提醒", "desc": "土壤湿度 42%，建议补充灌溉", "time": "1小时前", "read": False},
    {"id": 3, "type": "todo", "level": "blue", "icon": "📸", "title": "M3M 任务待审核", "desc": "B区水稻RGB正射图任务需确认出发", "time": "2小时前", "read": False},
    {"id": 4, "type": "msg", "level": "green", "icon": "✅", "title": "A区小麦NDVI分析完成", "desc": "报告已生成，平均NDVI 0.68", "time": "昨天 16:30", "read": True},
    {"id": 5, "type": "warn", "level": "amber", "icon": "🚁", "title": "M3M 电量提醒", "desc": "电量剩余 24%，建议及时充电", "time": "昨天 14:00", "read": True},
    {"id": 6, "type": "todo", "level": "green", "icon": "📋", "title": "月度报告待确认", "desc": "1月份农事记录汇总待审核", "time": "1月10日", "read": True},
]

# 阀门
valves = [
    {"id": 1, "name": "A区主阀", "zone": "北大沟", "open": True, "flow": 2.4},
    {"id": 2, "name": "B区灌渠阀", "zone": "灌渠南", "open": False, "flow": 0},
    {"id": 3, "name": "C区滴灌阀", "zone": "西坡", "open": True, "flow": 1.8},
    {"id": 4, "name": "D区阀门", "zone": "东南角", "open": False, "flow": 0},
]

# 农事记录（含 2026 示例数据，匹配参考图）
farmlogs = [
    {"id": 1, "type": "growth", "fieldId": 5, "fieldName": "大本营南", "farm": "幸福农场", "farmId": 1, "crop": "棉花", "date": "2026-06-15", "time": "09:30", "recorder": "王农户",
     "data": {"points": [
         {"no": 1, "area": "区域A", "height": 68, "growth": 2.1, "leaves": 14, "stems": 4},
         {"no": 2, "area": "区域B", "height": 62, "growth": 1.8, "leaves": 12, "stems": 3},
         {"no": 3, "area": "区域C", "height": 65, "growth": 2.0, "leaves": 13, "stems": 3},
     ]},
     "photos": ["img1", "img2", "img3"], "notes": "植株长势良好,无病虫害迹象"},
    {"id": 2, "type": "water", "fieldId": 5, "fieldName": "大本营南", "farm": "幸福农场", "farmId": 1, "crop": "棉花", "date": "2026-06-15", "time": "14:20", "recorder": "王农户",
     "data": {"waterAmt": 20, "fertilizers": [{"no": 1, "name": "尿素", "amount": 15, "N": 46, "P": 0, "K": 0}]},
     "photos": [], "notes": ""},
    {"id": 3, "type": "pest", "fieldId": 5, "fieldName": "大本营南", "farm": "幸福农场", "farmId": 1, "crop": "棉花", "date": "2026-06-14", "time": "10:00", "recorder": "王农户",
     "data": {"pesticides": [{"no": 1, "name": "阿维菌素", "effect": "杀虫", "amount": "50ml/亩"}]},
     "photos": [], "notes": ""},
    {"id": 4, "type": "diary", "fieldId": 5, "fieldName": "大本营南", "farm": "幸福农场", "farmId": 1, "crop": "棉花", "date": "2026-06-14", "time": "16:30", "recorder": "王农户",
     "data": {"content": "田间除草完成, 植株长势良好"},
     "photos": [], "notes": ""},
    {"id": 5, "type": "growth", "fieldId": 1, "fieldName": "1号地块", "farm": "幸福农场", "farmId": 1, "crop": "棉花", "date": "2024-01-15", "time": "09:00", "recorder": "王大明",
     "data": {"points": [{"no": 1, "area": "区域A", "height": 42, "growth": 1.2, "leaves": 6, "stems": 1}, {"no": 2, "area": "区域B", "height": 45, "growth": 1.5, "leaves": 7, "stems": 1}]},
     "photos": [], "notes": "观测点均位于田块中部。"},
]

# 钱包
wallet = {
    "balance": 5800.00,
    "accounts": [
        {"id": 1, "type": "corporate", "icon": "🏢", "label": "对公银行卡", "name": "华东农业科技有限公司", "bankName": "建设银行", "cardNo": "**** **** **** 8888", "tag": "对公"},
        {"id": 2, "type": "personal", "icon": "💳", "label": "个人银行卡", "name": "王大明", "bankName": "农业银行", "cardNo": "**** **** **** 6688", "tag": "个人"},
    ],
    "transactions": [
        {"id": 1, "type": "income", "time": "2024-01-15 14:32", "label": "订单收入", "ref": "ORD202401150012", "amt": 4380.00, "status": "success"},
        {"id": 2, "type": "withdraw", "time": "2024-01-14 09:15", "label": "提现", "ref": "建设银行 8888", "amt": -1000.00, "status": "success"},
        {"id": 3, "type": "income", "time": "2024-01-12 16:48", "label": "订单收入", "ref": "ORD202401120008", "amt": 2560.00, "status": "success"},
        {"id": 4, "type": "withdraw", "time": "2024-01-10 10:20", "label": "提现", "ref": "农业银行 6688", "amt": -3000.00, "status": "processing"},
    ],
}

# NDVI 数据
ndvi_data = {
    "A": {"avg": 0.68, "max": 0.89, "min": 0.32, "crop": "小麦", "bands": {"G": 0.72, "R": 0.38, "RE": 0.55, "NIR": 0.84},
          "health": [{"label": "优良(>0.6)", "pct": 58, "color": "#6B9B6E"}, {"label": "正常(0.3-0.6)", "pct": 32, "color": "#C99A6C"}, {"label": "较差(<0.3)", "pct": 10, "color": "#B87A7A"}]},
    "B": {"avg": 0.72, "max": 0.91, "min": 0.41, "crop": "水稻", "bands": {"G": 0.75, "R": 0.35, "RE": 0.58, "NIR": 0.88},
          "health": [{"label": "优良(>0.6)", "pct": 71, "color": "#6B9B6E"}, {"label": "正常(0.3-0.6)", "pct": 24, "color": "#C99A6C"}, {"label": "较差(<0.3)", "pct": 5, "color": "#B87A7A"}]},
    "C": {"avg": 0.41, "max": 0.72, "min": 0.12, "crop": "玉米", "bands": {"G": 0.55, "R": 0.52, "RE": 0.41, "NIR": 0.65},
          "health": [{"label": "优良(>0.6)", "pct": 22, "color": "#6B9B6E"}, {"label": "正常(0.3-0.6)", "pct": 51, "color": "#C99A6C"}, {"label": "较差(<0.3)", "pct": 27, "color": "#B87A7A"}]},
    "D": {"avg": 0.65, "max": 0.85, "min": 0.28, "crop": "大豆", "bands": {"G": 0.69, "R": 0.41, "RE": 0.52, "NIR": 0.81},
          "health": [{"label": "优良(>0.6)", "pct": 53, "color": "#6B9B6E"}, {"label": "正常(0.3-0.6)", "pct": 38, "color": "#C99A6C"}, {"label": "较差(<0.3)", "pct": 9, "color": "#B87A7A"}]},
}
