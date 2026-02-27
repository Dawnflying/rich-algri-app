<template>
  <div class="page field-map-plot">
    <div class="hdr map-hdr">
      <button class="hdr-back" @click="goBack">‹</button>
      <div class="hdr-title-wrap">
        <span class="hdr-title">连续打点</span>
        <span class="hdr-icon">⚡</span>
      </div>
      <button class="btn-done" @click="finish">
        <span class="btn-icon">⚡</span>
        完成打点
      </button>
    </div>

    <div class="control-bar">
      <button type="button" class="btn-reset" @click="resetCurrent">重置当前</button>
      <button type="button" class="btn-close" @click="closePolygon">闭合</button>
      <div class="hint-card">
        <p>点击地图添加边界点</p>
        <p>至少需要3个点才能闭合地块</p>
        <p>点击闭合按钮完成当前地块</p>
      </div>
    </div>

    <div class="map-container" ref="mapContainer">
      <div v-if="!amapReady" class="map-loading">
        <span v-if="!amapError">地图加载中...</span>
        <span v-else class="error-msg">{{ amapError }}</span>
      </div>
    </div>

    <p v-if="currentPoints.length > 0" class="close-hint">点击'闭合'按钮完成此地块,或继续</p>

    <div class="created-section">
      <div class="created-title">已创建地块 {{ createdPolygons.length }}个</div>
      <div class="created-list">
        <div v-for="(p, i) in createdPolygons" :key="i" class="created-item">
          <span class="created-color" :style="{ background: p.color }"></span>
          <div class="created-info">
            <span class="created-name">{{ p.name }}</span>
            <span class="created-area">面积约{{ p.area }}亩</span>
          </div>
          <span class="created-delete" @click="removePolygon(i)">🗑️</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const mapContainer = ref(null)
const amapReady = ref(false)
const amapError = ref('')
const map = ref(null)
const currentPoints = ref([])
const currentMarkers = ref([])
const currentPolyline = ref(null)
const createdPolygons = ref([])
const polygonColors = ['#81C784', '#64B5F6', '#FFB74D', '#E57373']

let clickHandler = null

function loadAmap() {
  if (window.AMap) {
    initMap()
    return
  }
  const key = import.meta.env.VITE_AMAP_KEY || ''
  if (!key) {
    amapError.value = '请在 .env 中配置 VITE_AMAP_KEY。前往 lbs.amap.com 申请 Web 端 JS API key'
    return
  }
  const script = document.createElement('script')
  script.src = `https://webapi.amap.com/maps?v=2.0&key=${key}`
  script.async = true
  script.onload = () => initMap()
  script.onerror = () => {
    amapError.value = '请配置 VITE_AMAP_KEY 并重启。前往 lbs.amap.com 申请 Web 端 JS API key'
  }
  document.head.appendChild(script)
}

function initMap() {
  if (!mapContainer.value || !window.AMap) return
  // 石河子市中心
  const center = [86.0411, 44.3059]
  map.value = new window.AMap.Map(mapContainer.value, {
    zoom: 14,
    center,
    mapStyle: 'amap://styles/whitesmoke',
    viewMode: '2D',
  })
  map.value.on('click', onMapClick)
  amapReady.value = true
}

function onMapClick(e) {
  const { lng, lat } = e.lnglat
  currentPoints.value.push({ lng, lat })
  addPointMarker(lng, lat)
  updatePolyline()
}

function addPointMarker(lng, lat) {
  if (!map.value || !window.AMap) return
  const marker = window.AMap.CircleMarker
    ? new window.AMap.CircleMarker({
        position: [lng, lat],
        radius: 6,
        fillColor: '#6B9B6E',
        fillOpacity: 1,
        strokeWeight: 2,
        strokeColor: '#FFF',
      })
    : new window.AMap.Circle({
        center: [lng, lat],
        radius: 8,
        fillColor: '#6B9B6E',
        fillOpacity: 1,
        strokeWeight: 2,
        strokeColor: '#FFF',
      })
  map.value.add(marker)
  currentMarkers.value.push(marker)
}

function updatePolyline() {
  if (!map.value || !window.AMap) return
  if (currentPolyline.value) {
    map.value.remove(currentPolyline.value)
    currentPolyline.value = null
  }
  if (currentPoints.value.length < 2) return
  const path = currentPoints.value.map(p => [p.lng, p.lat])
  currentPolyline.value = new window.AMap.Polyline({
    path,
    strokeColor: '#6B9B6E',
    strokeWeight: 3,
    strokeStyle: 'dashed',
    strokeOpacity: 0.9,
  })
  map.value.add(currentPolyline.value)
}

function resetCurrent() {
  currentMarkers.value.forEach(m => map.value?.remove(m))
  currentMarkers.value = []
  if (currentPolyline.value) {
    map.value.remove(currentPolyline.value)
    currentPolyline.value = null
  }
  currentPoints.value = []
}

function closePolygon() {
  if (currentPoints.value.length < 3) return
  const path = currentPoints.value.map(p => [p.lng, p.lat])
  const area = calcArea(path)
  const color = polygonColors[createdPolygons.value.length % polygonColors.length]
  const polygon = new window.AMap.Polygon({
    path: [...path, path[0]],
    strokeColor: color,
    strokeWeight: 2,
    fillColor: color,
    fillOpacity: 0.35,
  })
  map.value.add(polygon)
  createdPolygons.value.push({
    path: currentPoints.value.map(p => ({ lng: p.lng, lat: p.lat })),
    area,
    name: `地块${createdPolygons.value.length + 1}`,
    color,
    amapObj: polygon,
  })
  resetCurrent()
}

function calcArea(path) {
  if (!path || path.length < 3) return 0
  let area = 0
  const n = path.length
  for (let i = 0; i < n; i++) {
    const j = (i + 1) % n
    area += path[i][0] * path[j][1]
    area -= path[j][0] * path[i][1]
  }
  area = Math.abs(area) / 2
  const sqDegToMu = (111 * 80 * 1e6) / 666.67
  return (area * sqDegToMu).toFixed(1)
}

function removePolygon(i) {
  const p = createdPolygons.value[i]
  if (p?.amapObj) map.value?.remove(p.amapObj)
  createdPolygons.value.splice(i, 1)
}

function goBack() {
  router.back()
}

function finish() {
  const from = route.query.from || '/field/edit'
  const boundary = createdPolygons.value[0]?.path || []
  const polygons = createdPolygons.value
  const path = from.split('?')[0] || '/field/edit'

  const query = {}
  try {
    const fromQuery = new URLSearchParams(from.includes('?') ? from.split('?')[1] : '')
    fromQuery.forEach((v, k) => { if (k !== 'boundary' && k !== 'polygons') query[k] = v })
  } catch (_) {}
  if (boundary.length > 0) query.boundary = JSON.stringify(boundary)
  if (polygons.length > 1) query.polygons = JSON.stringify(polygons.map(p => ({ path: p.path, area: p.area, name: p.name })))

  router.push({ path, query })
}

onMounted(() => {
  loadAmap()
})

onBeforeUnmount(() => {
  map.value?.destroy()
})
</script>

<style scoped>
.field-map-plot { display: flex; flex-direction: column; height: 100vh; background: #FFF; }
.map-hdr {
  display: flex; align-items: center; padding: 12px 16px;
  background: linear-gradient(135deg, #6B9B6E, #8FBC92); color: #FFF; flex-shrink: 0;
}
.hdr-back { width: 36px; height: 36px; border: none; background: rgba(255,255,255,.2); color: #FFF; font-size: 24px; border-radius: 8px; cursor: pointer; flex-shrink: 0; }
.hdr-title-wrap { flex: 1; display: flex; align-items: center; justify-content: center; gap: 6px; }
.hdr-title { font-size: 16px; font-weight: 600; }
.hdr-icon { font-size: 16px; }
.btn-done {
  padding: 8px 14px; background: #FFF; color: #6B9B6E; border: none;
  border-radius: 8px; font-size: 13px; font-weight: 500; cursor: pointer;
  display: flex; align-items: center; gap: 4px;
}
.btn-icon { font-size: 12px; }
.control-bar {
  display: flex; align-items: center; gap: 12px; padding: 12px 16px;
  background: #F5F5F5; flex-shrink: 0;
}
.btn-reset { padding: 8px 14px; background: #FFF; border: 1px solid var(--primary-border); color: var(--text2); border-radius: 8px; font-size: 13px; cursor: pointer; }
.btn-close { padding: 8px 18px; background: #6B9B6E; color: #FFF; border: none; border-radius: 8px; font-size: 13px; cursor: pointer; }
.hint-card {
  flex: 1; background: #FFF; padding: 10px 14px; border-radius: 8px;
  font-size: 12px; color: #666; line-height: 1.5;
}
.map-container { flex: 1; min-height: 280px; position: relative; }
.map-loading {
  position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
  background: #E8E8E8; color: #666; font-size: 14px;
}
.error-msg { color: var(--red); font-size: 12px; text-align: center; padding: 16px; }
.close-hint { padding: 8px 16px; font-size: 12px; color: var(--text2); text-align: center; }
.created-section { padding: 12px 16px; background: #FFF; border-top: 1px solid #EEE; flex-shrink: 0; }
.created-title { font-size: 14px; font-weight: 600; color: #1B2E1B; margin-bottom: 10px; }
.created-list { display: flex; flex-direction: column; gap: 8px; max-height: 140px; overflow-y: auto; }
.created-item { display: flex; align-items: center; gap: 10px; padding: 10px 12px; background: #F7FAF7; border-radius: 8px; }
.created-color { width: 12px; height: 12px; border-radius: 4px; flex-shrink: 0; }
.created-info { flex: 1; display: flex; flex-direction: column; gap: 2px; }
.created-name { font-size: 14px; font-weight: 500; color: #1B2E1B; }
.created-area { font-size: 12px; color: var(--text2); }
.created-delete { font-size: 16px; cursor: pointer; padding: 4px; }
</style>
