<template>
  <div class="page order-trace">
    <div class="hdr-bar">
      <button class="hdr-back" @click="$router.back()">‹</button>
      <span class="hdr-title">作业留痕记录</span>
      <span class="hdr-icon">⚡</span>
    </div>

    <div class="page-body" v-if="trace">
      <div class="trace-info">
        <div class="info-row">
          <span class="info-label">订单号</span>
          <span>{{ trace.orderNo }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">状态</span>
          <span class="status-text" :class="trace.status">{{ trace.statusText }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">更新时间</span>
          <span>{{ trace.updatedAt }}</span>
        </div>
      </div>

      <div class="trace-section">
        <div class="section-title">留痕规则</div>
        <div class="trace-rule">{{ trace.traceRule }}</div>
      </div>

      <div class="trace-section">
        <div class="section-title">作业留痕时间线</div>
        <div class="timeline">
          <div v-for="(r, i) in trace.records" :key="i" class="trace-item">
            <div class="trace-meta">
              <span class="trace-time">{{ r.time }}</span>
              <span class="trace-source">{{ r.source }}</span>
            </div>
            <div class="trace-desc">{{ r.desc }}</div>
            <div v-if="r.images" class="trace-images">
              <div v-for="j in r.images" :key="j" class="img-placeholder">
                <span class="img-icon">🖼</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div style="height: 80px"></div>
    </div>

    <div class="bottom-bar">
      <button class="btn-back" @click="$router.push('/machinery/order/' + orderId)">返回监控</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ordersApi } from '../api'

const route = useRoute()
const trace = ref(null)
const orderId = computed(() => route.params.id)

onMounted(async () => {
  const id = Number(route.params.id)
  if (!id) return
  try {
    const { data } = await ordersApi.getTrace(id)
    trace.value = data
  } catch (e) {
    trace.value = null
  }
})
</script>

<style scoped>
.order-trace .page-body { padding: 16px; }
.hdr-bar { display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: linear-gradient(135deg, var(--primary), var(--primary-light)); color: #FFF; }
.hdr-back { width: 36px; height: 36px; border: none; background: rgba(255,255,255,.2); color: #FFF; font-size: 24px; border-radius: 8px; cursor: pointer; }
.hdr-title { font-size: 18px; font-weight: 600; flex: 1; }
.hdr-icon { font-size: 16px; }
.trace-info { background: #FFF; border-radius: 12px; padding: 16px; margin-bottom: 16px; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.info-row { display: flex; justify-content: space-between; padding: 8px 0; font-size: 14px; }
.info-label { color: #666; }
.status-text { color: var(--primary); font-weight: 600; }
.status-text.in_progress { color: var(--primary); }
.trace-section { background: #FFF; border-radius: 12px; padding: 16px; margin-bottom: 16px; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.section-title { font-size: 15px; font-weight: 600; color: #1B2E1B; margin-bottom: 12px; }
.trace-rule { font-size: 14px; color: #666; }
.timeline { font-size: 14px; }
.trace-item { padding: 16px 0; border-bottom: 1px solid #EEE; }
.trace-item:last-child { border-bottom: none; }
.trace-meta { display: flex; justify-content: space-between; margin-bottom: 8px; }
.trace-time { color: #333; font-weight: 500; }
.trace-source { font-size: 12px; color: var(--blue); }
.trace-desc { color: #666; margin-bottom: 10px; line-height: 1.5; }
.trace-images { display: flex; gap: 10px; flex-wrap: wrap; }
.img-placeholder { width: 80px; height: 80px; background: #F5F5F5; border-radius: 8px; display: flex; align-items: center; justify-content: center; }
.img-icon { font-size: 24px; }
.bottom-bar { position: fixed; bottom: 0; left: 0; right: 0; padding: 12px 16px; background: #FFF; box-shadow: 0 -2px 8px rgba(0,0,0,.08); }
.btn-back { width: 100%; padding: 14px; background: #FFF; color: var(--primary); border: 2px solid var(--primary); border-radius: 12px; font-size: 15px; font-weight: 600; cursor: pointer; }
</style>
