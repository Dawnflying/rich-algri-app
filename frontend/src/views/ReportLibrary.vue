<template>
  <div class="page report-library">
    <div class="hdr-bar">
      <button class="hdr-back" @click="$router.back()">‹</button>
      <span class="hdr-title">巡田记录与报告库</span>
      <span class="hdr-icon">⚡</span>
    </div>

    <div class="page-body">
    <div class="search-row">
      <span class="search-icon">🔍</span>
      <input v-model="searchKey" type="text" placeholder="搜索报告标题、订单号" class="search-input" />
    </div>

    <div class="intro-text">
      此处汇集您所有的巡田报告，包括无人机巡田和卫星遥感巡田的历史记录。
    </div>

    <div class="filter-section">
      <div class="filter-row">
        <span class="filter-label">报告来源:</span>
        <div class="filter-tags">
          <button v-for="t in sourceTabs" :key="t.key" class="filter-tag" :class="{ active: source === t.key }" @click="source = t.key">
            {{ t.label }}
          </button>
        </div>
      </div>
      <div class="filter-row">
        <span class="filter-label">时间范围:</span>
        <div class="filter-tags">
          <button v-for="t in timeTabs" :key="t.key" class="filter-tag" :class="{ active: timeRange === t.key }" @click="timeRange = t.key">
            {{ t.label }}
          </button>
        </div>
      </div>
      <div class="filter-row">
        <span class="filter-label">地块:</span>
        <div class="plot-select">
          <span>全部地块</span>
          <span class="chevron">⌄</span>
        </div>
      </div>
    </div>

    <div class="report-list">
      <div v-for="r in filteredReports" :key="r.id" class="report-card">
        <div class="card-left">
          <div class="report-avatar" :class="r.type">
            <span v-if="r.type === 'drone'">✈️</span>
            <span v-else>⭐</span>
          </div>
          <div class="report-info">
            <div class="report-title-row">
              <span class="report-title">{{ r.title }}</span>
              <span class="report-tag" :class="r.type">{{ r.type === 'drone' ? '无人机' : '卫星' }}</span>
            </div>
            <div class="report-provider">{{ r.provider }}</div>
            <div class="report-meta">
              <span>📅 {{ r.datetime }}</span>
            </div>
            <div class="report-meta">
              <span>📄 订单号: {{ r.orderNo }}</span>
            </div>
            <div class="report-meta">
              <span>📍 地块:{{ r.plotName }}</span>
            </div>
          </div>
        </div>
        <button class="btn-detail" @click="$router.push('/patrol/report/' + r.id)">⚡ 查看详情</button>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { patrolReportsApi } from '../api'

const searchKey = ref('')
const source = ref('all')
const timeRange = ref('month')
const reports = ref([])

const sourceTabs = [
  { key: 'all', label: '全部' },
  { key: 'drone', label: '无人机巡田' },
  { key: 'satellite', label: '卫星遥感' },
]

const timeTabs = [
  { key: 'month', label: '本月' },
  { key: '3month', label: '近3月' },
  { key: 'year', label: '近1年' },
  { key: 'custom', label: '自定义' },
]

const filteredReports = computed(() => {
  let list = reports.value
  const q = searchKey.value.trim().toLowerCase()
  if (q) {
    list = list.filter(r =>
      (r.title || '').toLowerCase().includes(q) ||
      (r.orderNo || '').toLowerCase().includes(q)
    )
  }
  if (source.value && source.value !== 'all') {
    list = list.filter(r => r.type === source.value)
  }
  return list
})

async function fetchReports() {
  try {
    const { data } = await patrolReportsApi.list({
      q: searchKey.value || undefined,
      source: source.value === 'all' ? undefined : source.value,
      timeRange: timeRange.value,
    })
    reports.value = data || []
  } catch (e) {
    reports.value = []
  }
}

onMounted(fetchReports)
watch([searchKey, source, timeRange], fetchReports)
</script>

<style scoped>
.report-library .page-body { padding: 16px; }
.hdr-bar { display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: var(--primary-gradient); color: #FFF; }
.hdr-back { width: 36px; height: 36px; border: none; background: rgba(255,255,255,.2); color: #FFF; font-size: 24px; border-radius: 8px; cursor: pointer; }
.hdr-title { font-size: 18px; font-weight: 600; flex: 1; }
.hdr-icon { font-size: 16px; }
.search-row { display: flex; align-items: center; gap: 8px; padding: 12px 16px; background: #FFF; border-bottom: 1px solid #EEE; }
.search-icon { font-size: 16px; }
.search-input { flex: 1; border: none; font-size: 14px; outline: none; }
.intro-text { font-size: 13px; color: #666; padding: 12px 16px; line-height: 1.6; }
.filter-section { padding: 0 16px 16px; }
.filter-row { margin-bottom: 12px; }
.filter-label { font-size: 13px; color: #666; display: block; margin-bottom: 8px; }
.filter-tags { display: flex; flex-wrap: wrap; gap: 8px; }
.filter-tag { padding: 6px 14px; border: 1px solid #E0E0E0; background: #FFF; border-radius: 20px; font-size: 13px; cursor: pointer; }
.filter-tag.active { background: var(--primary); color: #FFF; border-color: var(--primary); }
.plot-select { display: inline-flex; align-items: center; gap: 4px; padding: 6px 12px; border: 1px solid #E0E0E0; border-radius: 8px; font-size: 13px; color: #666; }
.chevron { font-size: 10px; }
.report-list { display: flex; flex-direction: column; gap: 12px; padding: 0 16px 32px; }
.report-card { background: #FFF; border-radius: 12px; padding: 16px; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.card-left { display: flex; gap: 12px; margin-bottom: 12px; }
.report-avatar { width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 22px; flex-shrink: 0; }
.report-avatar.drone { background: #E3F2FD; }
.report-avatar.satellite { background: #F3E5F5; }
.report-info { flex: 1; min-width: 0; }
.report-title-row { display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; margin-bottom: 4px; }
.report-title { font-size: 14px; font-weight: 600; color: var(--text); }
.report-tag { font-size: 11px; padding: 2px 8px; border-radius: 10px; flex-shrink: 0; }
.report-tag.drone { background: var(--blue); color: #FFF; }
.report-tag.satellite { background: #7B1FA2; color: #FFF; }
.report-provider { font-size: 13px; color: #666; margin-bottom: 6px; }
.report-meta { font-size: 12px; color: #999; margin-bottom: 2px; }
.btn-detail { width: 100%; padding: 10px; background: var(--primary); color: #FFF; border: none; border-radius: 8px; font-size: 14px; cursor: pointer; }
</style>
