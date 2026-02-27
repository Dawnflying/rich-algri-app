<template>
  <div class="page field-detail">
    <div class="hdr-title-bar">地块详情页</div>
    <div class="hdr-banner">
      <button class="hdr-back" @click="$router.back()">‹</button>
      <div class="hdr-name-wrap">
        <span class="hdr-name">{{ field?.name || '加载中...' }}</span>
        <span class="hdr-icon">⚡</span>
      </div>
      <div class="hdr-actions">
        <span class="hdr-action-icon" @click="toast('智能功能')">⚡</span>
        <span class="hdr-action-icon" @click="$router.push('/field/edit?id=' + field?.id)">✎</span>
        <span class="hdr-action-icon" @click="onDelete">🗑️</span>
      </div>
    </div>

    <div class="page-body" v-if="field">
      <!-- 地块基本信息 -->
      <div class="section">
        <div class="section-title">地块基本信息</div>
        <div class="info-grid">
          <div class="info-item"><span class="info-label">所属农场</span><span class="info-val">{{ field.farm || '--' }}</span></div>
          <div class="info-item"><span class="info-label">地块面积</span><span class="info-val">{{ field.area ?? 0 }} 亩</span></div>
          <div class="info-item"><span class="info-label">耕种作物</span><span class="info-val">{{ field.crop || '--' }}</span></div>
          <div class="info-item"><span class="info-label">种子名称</span><span class="info-val">{{ field.cropSeed || '--' }}</span></div>
          <div class="info-item"><span class="info-label">种植模式</span><span class="info-val">{{ field.planting || '--' }}</span></div>
          <div class="info-item"><span class="info-label">滴灌流量</span><span class="info-val">{{ (field.dripFlow ?? 0) }} 升/小时</span></div>
          <div class="info-item"><span class="info-label">滴孔间距</span><span class="info-val">{{ field.holeSpacing || '--' }}</span></div>
          <div class="info-item"><span class="info-label">水源</span><span class="info-val">{{ field.waterSource || '--' }}</span></div>
          <div class="info-item"><span class="info-label">沟心间距</span><span class="info-val">{{ formatTrench(field) }}</span></div>
          <div class="info-item"><span class="info-label">土壤性质</span><span class="info-val">{{ field.soilType || '--' }}</span></div>
          <div class="info-item"><span class="info-label">是否盐碱地</span><span class="info-val">{{ field.saltAlkali || '不含盐碱' }}</span></div>
        </div>
      </div>

      <!-- 地块位置 -->
      <div class="section">
        <div class="section-title section-title-gray">地块位置</div>
        <div class="map-placeholder" ref="mapContainer">
          <div v-if="!amapReady" class="map-loading">
            <span v-if="!amapError">地图加载中...</span>
            <span v-else class="map-error">{{ amapError }}</span>
          </div>
        </div>
        <button class="btn-view-map" @click="goToFullscreenMap">
          <span class="btn-map-icon">⊞</span>
          查看完整地图
        </button>
      </div>

      <!-- 底部操作 -->
      <div class="bottom-actions">
        <button class="btn-action btn-record" @click="$router.push('/farmlog/add')">
          <span class="btn-action-icon">📝</span>
          记录农事
          <span class="btn-action-badge">⚡</span>
        </button>
        <button class="btn-action btn-invite" @click="toast('邀请指导')">
          <span class="btn-action-icon">👤</span>
          邀请指导
          <span class="btn-action-badge">⚡</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { fieldsApi } from '../api'
import { useToast } from '../composables/useToast'

const route = useRoute()
const router = useRouter()
const { toast } = useToast()
const field = ref(null)
const mapContainer = ref(null)
const amapReady = ref(false)
const amapError = ref('')
const map = ref(null)
let polygonObj = null
let markerObj = null
const DEFAULT_CENTER = [86.0411, 44.3059]

function formatTrench(f) {
  const m = f.trenchMeter ?? 0
  const cm = f.trenchCm ?? 0
  if (!m && !cm) return '--'
  const parts = []
  if (m) parts.push(m + ' 米')
  if (cm) parts.push(cm + ' 厘米')
  return parts.join(' ')
}

function onDelete() {
  if (!confirm('确定要删除此地块吗？')) return
  toast('删除功能开发中')
}

function goToFullscreenMap() {
  if (field.value?.id) router.push(`/field/${field.value.id}/map`)
  else toast('地块信息加载中')
}

function loadAmap() {
  if (window.AMap) {
    initMap()
    return
  }
  const key = import.meta.env.VITE_AMAP_KEY || ''
  if (!key) {
    amapError.value = '请配置 VITE_AMAP_KEY'
    return
  }
  const script = document.createElement('script')
  script.src = `https://webapi.amap.com/maps?v=2.0&key=${key}`
  script.async = true
  script.onload = () => initMap()
  script.onerror = () => { amapError.value = '地图加载失败' }
  document.head.appendChild(script)
}

function initMap() {
  if (!mapContainer.value || !window.AMap || !field.value) return
  const center = field.value.center || DEFAULT_CENTER
  map.value = new window.AMap.Map(mapContainer.value, {
    zoom: 14,
    center,
    mapStyle: 'amap://styles/whitesmoke',
    viewMode: '2D',
  })
  drawField()
  amapReady.value = true
}

function drawField() {
  if (!map.value || !window.AMap || !field.value) return
  if (polygonObj) { map.value.remove(polygonObj); polygonObj = null }
  if (markerObj) { map.value.remove(markerObj); markerObj = null }
  const center = field.value.center || DEFAULT_CENTER
  const boundary = field.value.boundary
  if (boundary && Array.isArray(boundary) && boundary.length >= 3) {
    const path = boundary.map(p => Array.isArray(p) ? p : [p.lng ?? p[0], p.lat ?? p[1]])
    polygonObj = new window.AMap.Polygon({
      path: [...path, path[0]],
      strokeColor: '#6B9B6E',
      strokeWeight: 2,
      fillColor: '#6B9B6E',
      fillOpacity: 0.25,
    })
    map.value.add(polygonObj)
    map.value.setFitView([polygonObj])
  } else {
    markerObj = window.AMap.CircleMarker
      ? new window.AMap.CircleMarker({
          position: center,
          radius: 8,
          fillColor: '#6B9B6E',
          fillOpacity: 1,
          strokeWeight: 2,
          strokeColor: '#FFF',
        })
      : new window.AMap.Marker({ position: center })
    map.value.add(markerObj)
    map.value.setCenter(center)
  }
}

onMounted(async () => {
  const id = route.params.id
  if (!id) return
  try {
    const { data } = await fieldsApi.get(id)
    field.value = data
    loadAmap()
  } catch (e) {
    toast('加载失败')
  }
})

onBeforeUnmount(() => {
  map.value?.destroy()
})
</script>

<style scoped>
.field-detail .page-body { padding: 16px; padding-bottom: 100px; }
.hdr-title-bar {
  padding: 12px 16px; background: #F5F5F5; font-size: 14px; color: #666;
}
.hdr-banner {
  display: flex; align-items: center; padding: 12px 16px;
  background: var(--primary-gradient); color: #FFF;
}
.hdr-back {
  width: 36px; height: 36px; border: none; background: rgba(255,255,255,.2);
  color: #FFF; font-size: 24px; border-radius: 8px; cursor: pointer; flex-shrink: 0;
}
.hdr-name-wrap { flex: 1; display: flex; align-items: center; gap: 6px; margin-left: 12px; }
.hdr-name { font-size: 16px; font-weight: 600; }
.hdr-icon { font-size: 14px; }
.hdr-actions { display: flex; align-items: center; gap: 12px; }
.hdr-action-icon { font-size: 20px; cursor: pointer; padding: 4px; opacity: .95; }
.section { margin-bottom: 24px; }
.section-title { font-size: 15px; font-weight: 600; color: var(--primary); margin-bottom: 12px; }
.section-title-gray { color: #666; }
.info-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 12px 16px;
  background: #FFF; border: 1px solid rgba(46,125,50,.1); border-radius: 12px;
  padding: 16px; box-shadow: 0 2px 8px rgba(46,125,50,.06);
}
.info-item { display: flex; flex-direction: column; gap: 4px; }
.info-label { font-size: 12px; color: var(--text2); }
.info-val { font-size: 14px; font-weight: 500; color: #1B2E1B; }
.map-placeholder {
  background: #E8E8E8; border-radius: 10px; height: 160px; overflow: hidden;
  margin-bottom: 12px; position: relative;
}
.map-loading {
  position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
  background: #E8E8E8; color: #666; font-size: 13px;
}
.map-error { color: var(--red); font-size: 12px; }
.btn-view-map {
  width: 100%; padding: 12px; background: #F0F0F0; color: #666;
  border: none; border-radius: 10px; font-size: 14px; cursor: pointer;
  display: flex; align-items: center; justify-content: center; gap: 8px;
}
.btn-map-icon { font-size: 18px; }
.bottom-actions {
  position: fixed; bottom: 0; left: 0; right: 0;
  display: flex; gap: 12px; padding: 12px 16px;
  background: #FFF; border-top: 1px solid #EEE; box-shadow: 0 -2px 10px rgba(0,0,0,.05);
}
.btn-action {
  flex: 1; display: flex; align-items: center; justify-content: center; gap: 8px;
  padding: 14px; border: none; border-radius: 10px; font-size: 15px; font-weight: 500;
  cursor: pointer; color: #FFF;
}
.btn-record { background: var(--primary); }
.btn-invite { background: var(--primary-light); }
.btn-action-icon { font-size: 18px; }
.btn-action-badge { font-size: 12px; opacity: .9; }
</style>
