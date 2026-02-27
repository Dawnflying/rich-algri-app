# 智农云 · 部署与打包指南

## 一、后端 Docker 镜像

### 1. 单独构建后端镜像

```bash
# 在项目根目录
docker build -t rich-algri-app-backend:latest -f backend/Dockerfile backend/
```

### 2. 运行后端容器

```bash
docker run -d -p 8000:8000 --name rich-algri-backend rich-algri-app-backend:latest
```

---

## 二、前端 Docker 镜像

### 1. 单独构建前端镜像

```bash
# 在项目根目录（需包含 frontend/、nginx.conf）
docker build -t rich-algri-app-frontend:latest -f Dockerfile.frontend .
```

### 2. 运行前端容器

前端镜像内含 Nginx，API 代理指向 `backend:8000`。单独运行时需配合后端，建议用 docker compose。

---

## 三、使用 Makefile 快速构建

```bash
make build-backend    # 仅构建后端
make build-frontend   # 仅构建前端
make build            # 构建前后端
```

---

## 四、完整栈（后端 + 前端）

```bash
# 在项目根目录
docker compose up -d

# 仅后端
docker compose up -d backend

# 查看日志
docker compose logs -f
```

- 后端 API: http://localhost:8000
- 前端（含 API 代理）: http://localhost:80

---

## 五、UniApp 打包 APK

当前前端为 Vue3 + Vite 项目，打包 APK 有两种方式：

### 方式 A：UniApp WebView 壳（推荐）

将已部署的 H5 地址用 UniApp 的 `web-view` 包成原生壳，再打包 APK。

#### 1. 创建 UniApp 项目

```bash
# 在项目外创建
npx degit dcloudio/uni-preset-vue#vite rich-algri-uniapp
cd rich-algri-uniapp
npm install
```

#### 2. 修改为 WebView 壳

将 `pages/index/index.vue` 改为：

```vue
<template>
  <view class="container">
    <web-view :src="h5Url"></web-view>
  </view>
</template>

<script setup>
// 部署后的 H5 地址，如: https://your-domain.com
const h5Url = 'https://your-domain.com'
</script>

<style scoped>
.container {
  width: 100%;
  height: 100vh;
}
web-view {
  width: 100%;
  height: 100%;
}
</style>
```

#### 3. 配置 manifest.json

在 `manifest.json` 中配置 Android 应用信息（包名、应用名等）。

#### 4. 打包 APK

**使用 HBuilderX（推荐）：**

1. 用 [HBuilderX](https://www.dcloud.io/hbuilderx.html) 打开 `rich-algri-uniapp` 项目
2. 菜单：发行 → 原生 App-云打包
3. 选择 Android，勾选「使用公共测试证书」或上传自有证书
4. 打包完成后下载 APK

**使用命令行（仅生成离线资源）：**

```bash
npm run build:app-plus
# 生成在 unpackage/resources 下，需用 Android Studio 或 HBuilderX 继续打包
```

### 方式 B：wap2app（DCloud 工具）

若 H5 已上线，可使用 [wap2app](https://www.dcloud.io/wap2app.html) 将网址转为 App，再云打包。

---

## 六、环境变量

### 前端 API 地址

打包前需确保前端请求的 API 地址正确。当前使用相对路径 `/api`，部署时由 Nginx 代理到后端。

若 H5 与 API 非同源，需在 `frontend/src/api/index.js` 中修改 `baseURL` 为完整地址。

### 后端 CORS

生产环境建议在 `backend/app/main.py` 中将 `allow_origins` 改为具体域名，例如：

```python
allow_origins=["https://your-domain.com", "https://app.your-domain.com"]
```

---

## 七、快速验证

```bash
# 1. 构建并启动
docker compose up -d

# 2. 访问
curl http://localhost:8000/api/health
# 浏览器打开 http://localhost
```
