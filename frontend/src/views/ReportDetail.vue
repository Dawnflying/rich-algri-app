<template>
  <div class="page report-detail">
    <div class="hdr-bar">
      <button class="hdr-back" @click="$router.back()">‹</button>
      <span class="hdr-title">报告详情</span>
      <button class="hdr-download" @click="toast('下载报告')">↓</button>
    </div>

    <div class="page-body" v-if="report">
      <div class="report-title">{{ report.title }}</div>

      <!-- 无人机：服务信息 -->
      <div v-if="report.type === 'drone'" class="info-section">
        <div class="info-item"><span class="info-label">服务时间</span><span>{{ report.serviceTime }}</span></div>
        <div class="info-item"><span class="info-label">服务地块</span><span>{{ report.plot }}</span></div>
        <div class="info-item"><span class="info-label">服务商</span><span>{{ report.provider }}(企业)</span></div>
        <div class="info-item">
          <span class="info-label">关联订单</span>
          <span class="link-order" @click="$router.push('/machinery/order/1')">{{ report.orderNo }} ></span>
        </div>
      </div>

      <!-- 卫星：报告信息 -->
      <div v-else class="info-section">
        <div class="info-item"><span class="info-label">报告日期</span><span>{{ report.reportDate }}</span></div>
        <div class="info-item"><span class="info-label">监测地块</span><span>{{ report.plot }}</span></div>
        <div class="info-item"><span class="info-label">数据来源</span><span>{{ report.dataSource }}</span></div>
        <div class="info-item"><span class="info-label">更新频率</span><span>{{ report.updateFreq }}</span></div>
        <div class="info-item"><span class="info-label">套餐周期</span><span>{{ report.packageCycle }}</span></div>
        <div class="info-item">
          <span class="info-label">关联订单</span>
          <span class="link-order" @click="$router.push('/machinery/order/1')">{{ report.orderNo }} ></span>
        </div>
      </div>

      <!-- 同批次地块 -->
      <div class="info-section">
        <div class="section-title">{{ report.type === 'drone' ? '本次作业同批次地块' : '本次卫星巡田批次同地块' }}</div>
        <div class="batch-plots">
          <button v-for="p in report.batchPlots" :key="p" class="plot-tag" :class="{ active: p === report.plot }">{{ p }}</button>
        </div>
      </div>

      <!-- 报告类型 tabs -->
      <div class="chart-tabs">
        <button class="chart-tab active">长势分布图</button>
        <button v-if="report.type === 'drone'" class="chart-tab">株高分布图</button>
      </div>

      <!-- 长势分布图 -->
      <div class="chart-section">
        <div class="chart-title">长势分布图</div>
        <!-- 卫星：期数导航 -->
        <div v-if="report.type === 'satellite' && report.totalPeriods" class="period-nav">
          <button class="nav-btn">‹ 上一期</button>
          <span class="period-text">第{{ report.currentPeriod }}期 / 共{{ report.totalPeriods }}期</span>
          <button class="nav-btn">下一期 ></button>
        </div>
        <div class="chart-placeholder">
          <div class="map-legend">
            <div v-if="report.legend" class="legend-items">
              <div v-for="(l, i) in report.legend" :key="i" class="legend-item">
                <span class="legend-color" :style="{ background: l.color }"></span>
                <span>{{ l.label }} {{ l.percent }}</span>
              </div>
            </div>
            <div v-else class="legend-bar"></div>
          </div>
          <div class="map-image">
            <div class="map-overlay"></div>
          </div>
        </div>
        <div class="chart-date" v-if="report.reportDate">{{ report.reportDate }}</div>
        <div class="chart-desc">{{ report.chartDesc }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { patrolReportsApi } from '../api'
import { useToast } from '../composables/useToast'

const route = useRoute()
const { toast } = useToast()
const report = ref(null)

onMounted(async () => {
  const id = Number(route.params.id)
  if (!id) return
  try {
    const { data } = await patrolReportsApi.get(id)
    report.value = data
  } catch (e) {
    report.value = null
  }
})
</script>

<style scoped>
.report-detail .page-body { padding: 16px; padding-bottom: 32px; }
.hdr-bar { display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: var(--primary-gradient); color: #FFF; }
.hdr-back { width: 36px; height: 36px; border: none; background: rgba(255,255,255,.2); color: #FFF; font-size: 24px; border-radius: 8px; cursor: pointer; }
.hdr-title { font-size: 18px; font-weight: 600; flex: 1; }
.hdr-download { width: 36px; height: 36px; border: none; background: rgba(255,255,255,.2); color: #FFF; font-size: 18px; border-radius: 8px; cursor: pointer; }
.report-title { font-size: 16px; font-weight: 600; color: var(--text); margin-bottom: 16px; }
.info-section { background: #FFF; border-radius: 12px; padding: 16px; margin-bottom: 16px; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.section-title { font-size: 14px; font-weight: 600; color: #333; margin-bottom: 12px; }
.info-item { display: flex; justify-content: space-between; padding: 8px 0; font-size: 14px; }
.info-label { color: #666; }
.link-order { color: var(--primary); cursor: pointer; }
.batch-plots { display: flex; flex-wrap: wrap; gap: 8px; }
.plot-tag { padding: 8px 16px; border: 1px solid #E0E0E0; background: #FFF; border-radius: 8px; font-size: 13px; cursor: pointer; }
.plot-tag.active { background: var(--primary); color: #FFF; border-color: var(--primary); }
.chart-tabs { display: flex; gap: 12px; margin-bottom: 16px; }
.chart-tab { padding: 10px 20px; border: none; background: #F5F5F5; color: #666; border-radius: 8px; font-size: 14px; cursor: pointer; }
.chart-tab.active { background: var(--primary); color: #FFF; }
.chart-section { background: #FFF; border-radius: 12px; padding: 16px; margin-bottom: 16px; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.chart-title { font-size: 15px; font-weight: 600; margin-bottom: 12px; }
.period-nav { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.nav-btn { padding: 6px 12px; background: #F5F5F5; border: none; border-radius: 6px; font-size: 13px; cursor: pointer; }
.period-text { font-size: 14px; color: #666; }
.chart-placeholder { position: relative; background: var(--primary-dim); border-radius: 8px; min-height: 200px; overflow: hidden; }
.map-legend { position: absolute; right: 12px; top: 12px; z-index: 2; }
.legend-items { background: rgba(255,255,255,.9); padding: 8px 12px; border-radius: 8px; font-size: 12px; }
.legend-item { display: flex; align-items: center; gap: 6px; margin-bottom: 4px; }
.legend-item:last-child { margin-bottom: 0; }
.legend-color { width: 12px; height: 12px; border-radius: 2px; }
.legend-bar { width: 20px; height: 120px; background: linear-gradient(to top, #4CAF50, #8BC34A, #FFEB3B, #F44336); border-radius: 4px; }
.map-image { width: 100%; height: 200px; background: linear-gradient(135deg, #C8E6C9 0%, #FFF9C4 50%, #FFCDD2 100%); }
.map-overlay { width: 100%; height: 100%; }
.chart-date { font-size: 13px; color: #666; margin: 12px 0 8px; }
.chart-desc { font-size: 13px; color: #666; line-height: 1.6; }
</style>
