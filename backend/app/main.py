"""
智农云 · 农业管理平台 - 后端 API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, fields, farms, drone, ndvi, alerts, farmlog, wallet, irrigation, irrigation_tasks, orders, patrol_reports, guidance

app = FastAPI(title="智农云 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议配置具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(fields.router, prefix="/api/fields", tags=["地块"])
app.include_router(farms.router, prefix="/api/farms", tags=["农场"])
app.include_router(drone.router, prefix="/api/drone", tags=["无人机"])
app.include_router(ndvi.router, prefix="/api/ndvi", tags=["NDVI"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["预警"])
app.include_router(farmlog.router, prefix="/api/farmlog", tags=["农事记录"])
app.include_router(wallet.router, prefix="/api/wallet", tags=["钱包"])
app.include_router(irrigation.router, prefix="/api/irrigation", tags=["灌溉"])
app.include_router(irrigation_tasks.router, prefix="/api/irrigation/tasks", tags=["灌溉任务"])
app.include_router(orders.router, prefix="/api/machinery/orders", tags=["农机订单"])
app.include_router(patrol_reports.router, prefix="/api/patrol/reports", tags=["巡田报告"])
app.include_router(guidance.router, prefix="/api/guidance", tags=["指导建议"])


@app.get("/api/health")
def health():
    return {"status": "ok"}
