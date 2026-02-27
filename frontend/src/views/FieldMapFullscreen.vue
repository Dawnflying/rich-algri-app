<template>
  <div class="page field-map-fullscreen">
    <div class="map-hdr">
      <button class="hdr-back" @click="$router.back()">‹ 返回</button>
      <span class="hdr-title">{{ field?.name || '地块位置' }}</span>
    </div>
    <div class="map-container" ref="mapContainer">
      <div v-if="!amapReady" class="map-loading">
        <span v-if="!amapError">地图加载中...</span>
        <span v-else class="error-msg">{{ amapError }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRoute } from 'vue-router'
import { fieldsApi } from '../api'

const route = useRoute()
const mapContainer = ref(null)
const amapReady = ref(false)
const amapError = ref('')
const map = ref(null)
const field = ref(null)
let polygonObj = null
let markerObj = null

const DEFAULT_CENTER = [86.0411, 44.3059]

function loadAmap() {
  if (window.AMap) {
    initMap()
    return
  }
  const key = import.meta.env.VITE_AMAP_KEY || ''
  if (!key) {
    amapError.value = '请在 .env 中配置 VITE_AMAP_KEY'
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
  if (!mapContainer.value || !window.AMap) return
  const center = field.value?.center || DEFAULT_CENTER
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
  if (polygonObj) {
    map.value.remove(polygonObj)
    polygonObj = null
  }
  if (markerObj) {
    map.value.remove(markerObj)
    markerObj = null
  }
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
          radius: 12,
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

async function fetchField() {
  const id = route.params.id
  if (!id) return
  try {
    const { data } = await fieldsApi.get(id)
    field.value = data
  } catch (_) {
    field.value = { center: DEFAULT_CENTER }
  }
}

onMounted(async () => {
  await fetchField()
  loadAmap()
})

watch(() => route.params.id, fetchField)

onBeforeUnmount(() => {
  map.value?.destroy()
})
</script>

<style scoped>
.field-map-fullscreen {
  position: fixed; inset: 0; z-index: 999;
  display: flex; flex-direction: column;
  background: #FFF;
}
.map-hdr {
  display: flex; align-items: center; gap: 12px; padding: 12px 16px;
  background: var(--primary-gradient); color: #FFF; flex-shrink: 0;
}
.hdr-back {
  padding: 8px 12px; background: rgba(255,255,255,.2); color: #FFF;
  border: none; border-radius: 8px; font-size: 14px; cursor: pointer;
}
.hdr-title { font-size: 16px; font-weight: 600; flex: 1; }
.map-container { flex: 1; width: 100%; min-height: 0; position: relative; }
.map-loading {
  position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
  background: #E8E8E8; color: #666; font-size: 14px;
}
.error-msg { color: var(--red); font-size: 12px; padding: 16px; text-align: center; }
</style>
