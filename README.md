# 智农云 · 农业管理平台

前后端分离架构：Vue 3 前端 + Python FastAPI 后端。

## 项目结构

```
rich-algri-app/
├── backend/          # Python FastAPI 后端
│   ├── app/
│   │   ├── main.py   # 入口
│   │   ├── store.py  # 内存数据存储
│   │   └── routers/  # API 路由
│   └── requirements.txt
├── frontend/         # Vue 3 前端
│   ├── src/
│   │   ├── api/      # API 调用
│   │   ├── views/    # 页面组件
│   │   ├── stores/   # Pinia 状态
│   │   ├── router/   # 路由
│   │   └── composables/
│   └── package.json
└── index.html        # 原始单体应用（保留）
```

## 快速启动

### 1. 启动后端

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 启动前端

```bash
cd frontend
npm install
npm run dev
```

### 3. 访问

- 前端：http://localhost:5173
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

### 4. 演示登录

- 手机号：13800138000
- 密码：123456

## API 接口

| 模块 | 路径 | 说明 |
|------|------|------|
| 认证 | /api/auth/login | 登录 |
| 地块 | /api/fields | 地块列表、新增 |
| 无人机 | /api/drone/tasks | 任务列表、创建 |
| NDVI | /api/ndvi/{field} | 获取地块 NDVI 数据 |
| 预警 | /api/alerts | 预警列表、已读 |
| 农事记录 | /api/farmlog | 农事记录 CRUD |
| 钱包 | /api/wallet | 钱包、提现 |
| 灌溉 | /api/irrigation/valves | 阀门列表、切换 |

## 技术栈

- **前端**：Vue 3、Vue Router、Pinia、Axios、Vite
- **后端**：FastAPI、Pydantic
