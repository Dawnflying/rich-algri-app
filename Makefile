# 智农云 · Docker 镜像构建
# 用法: make build-backend | make build-frontend | make build

IMAGE_BACKEND = rich-algri-app-backend:latest
IMAGE_FRONTEND = rich-algri-app-frontend:latest

.PHONY: build build-backend build-frontend build-all

# 构建后端镜像
build-backend:
	docker build -t $(IMAGE_BACKEND) -f backend/Dockerfile backend/

# 构建前端镜像（需在项目根目录执行）
build-frontend:
	docker build -t $(IMAGE_FRONTEND) -f Dockerfile.frontend .

# 分别构建前后端
build: build-backend build-frontend

# 运行后端
run-backend:
	docker run -d -p 8000:8000 --name rich-algri-backend $(IMAGE_BACKEND)

# 运行前端（单独运行时 nginx 代理需配置后端地址，建议用 docker compose）
run-frontend:
	docker run -d -p 80:80 --name rich-algri-frontend $(IMAGE_FRONTEND)