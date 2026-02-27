<template>
  <div class="page farmlog-list">
    <div class="hdr-title-bar">农事记录历史列表页</div>
    <div class="hdr-banner">
      <button class="hdr-back" @click="$router.back()">‹</button>
      <div class="hdr-left">
        <span class="hdr-label">农事记录</span>
        <span class="hdr-icon">⚡</span>
      </div>
      <div class="hdr-actions">
        <button class="btn-add" @click="$router.push('/farmlog/add')">+ 添加 <span class="btn-icon">⚡</span></button>
        <button class="btn-export" @click="toast('导出')">导出</button>
      </div>
    </div>

    <div class="page-body">
      <!-- 搜索与筛选 -->
      <div class="filter-section">
        <input v-model="search" type="text" class="search-input" placeholder="搜索记录内容..." />
        <div class="filter-row">
          <div class="filter-item">
            <label>开始日期:</label>
            <input v-model="startDate" type="date" class="filter-input" />
          </div>
          <div class="filter-item">
            <label>结束日期:</label>
            <input v-model="endDate" type="date" class="filter-input" />
          </div>
        </div>
        <div class="filter-row">
          <div class="filter-item">
            <label>地块:</label>
            <select v-model="fieldFilter" class="filter-select">
              <option value="">全部</option>
              <option v-for="f in fields" :key="f.id" :value="f.id">{{ f.name }}</option>
            </select>
          </div>
          <div class="filter-item">
            <label>作物:</label>
            <select v-model="cropFilter" class="filter-select">
              <option value="">全部</option>
              <option v-for="c in crops" :key="c" :value="c">{{ c }}</option>
            </select>
          </div>
        </div>
      </div>

      <!-- 类型筛选 -->
      <div class="type-tabs">
        <button v-for="t in typeTabs" :key="t.key" class="type-tab" :class="{ active: typeFilter === t.key }" @click="typeFilter = t.key; load()">
          <span class="type-icon">{{ t.icon }}</span>
          {{ t.label }}
        </button>
      </div>

      <!-- 记录列表（按日期分组） -->
      <div class="log-list">
        <div v-for="(group, date) in groupedList" :key="date" class="date-group">
          <div class="date-header" @click="toggleDate(date)">
            <span class="date-arrow">{{ expandedDates.has(date) ? '▼' : '▶' }}</span>
            {{ formatDateLabel(date) }}
          </div>
          <div v-if="expandedDates.has(date)" class="date-entries">
            <div v-for="r in group" :key="r.id" class="log-entry" @click="$router.push('/farmlog/' + r.id)">
              <div class="entry-time">{{ r.time || '--:--' }}</div>
              <div class="entry-main">
                <span class="entry-type" :style="{ background: FL_TYPE_MAP[r.type]?.bg, color: FL_TYPE_MAP[r.type]?.color }">
                  {{ FL_TYPE_MAP[r.type]?.icon }} {{ FL_TYPE_MAP[r.type]?.label }}
                </span>
                <div class="entry-loc">{{ r.fieldName }}</div>
                <div class="entry-recorder">记录人: {{ r.recorder }}</div>
                <div class="entry-detail">{{ getEntryDetail(r) }}</div>
              </div>
            </div>
          </div>
        </div>
        <div v-if="!list.length" class="empty">暂无记录</div>
      </div>

      <button class="btn-load-more" @click="toast('加载更多')">▼ 加载更多...</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { farmlogApi, fieldsApi } from '../api'
import { useToast } from '../composables/useToast'

const { toast } = useToast()
const list = ref([])
const fields = ref([])
const search = ref('')
const startDate = ref('')
const endDate = ref('')
const fieldFilter = ref('')
const cropFilter = ref('')
const typeFilter = ref('all')
const expandedDates = ref(new Set())

const typeTabs = [
  { key: 'all', label: '全部', icon: '' },
  { key: 'growth', label: '日生长量', icon: '🌱' },
  { key: 'water', label: '水肥使用', icon: '💧' },
  { key: 'pest', label: '农药', icon: '🧪' },
  { key: 'diary', label: '记事', icon: '📋' },
  { key: 'issue', label: '田间问题', icon: '⚠️' },
]

const FL_TYPE_MAP = {
  diary: { label: '记事', icon: '📋', bg: 'rgba(123,163,212,.12)', color: '#7BA3D4' },
  growth: { label: '日生长量', icon: '🌱', bg: 'rgba(107,155,110,.1)', color: '#6B9B6E' },
  pest: { label: '农药使用', icon: '🧪', bg: 'rgba(184,122,122,.12)', color: '#B87A7A' },
  water: { label: '水肥使用', icon: '💧', bg: 'rgba(123,163,212,.12)', color: '#7BA3D4' },
  issue: { label: '田间问题', icon: '⚠️', bg: 'rgba(212,165,116,.12)', color: '#C99A6C' },
}

const crops = computed(() => [...new Set(fields.value.map(f => f.crop).filter(Boolean))])

const groupedList = computed(() => {
  const g = {}
  list.value.forEach(r => {
    const d = r.date || ''
    if (!g[d]) g[d] = []
    g[d].push(r)
  })
  return g
})

function formatDateLabel(date) {
  if (!date) return ''
  const [y, m, d] = date.split('-')
  return `${y}年${parseInt(m)}月${parseInt(d)}日`
}

function toggleDate(date) {
  const s = new Set(expandedDates.value)
  if (s.has(date)) s.delete(date)
  else s.add(date)
  expandedDates.value = s
}

function getEntryDetail(r) {
  if (r.type === 'growth') {
    const pts = r.data?.points || []
    return `观测点${pts.length}个:` + pts.map(p => ` ${p.area || '区域' + p.no}: 株高${p.height}厘米 日生长量${p.growth}厘米 叶数${p.leaves}片 苔数${p.stems}苔`).join('; ')
  }
  if (r.type === 'water') {
    const f = r.data?.fertilizers?.[0]
    return f ? `化肥名称: ${f.name} 亩用量: ${f.amount}公斤 氮含量N: ${f.N}% 用水量: ${r.data?.waterAmt || 0}立方米` : `用水量: ${r.data?.waterAmt || 0}立方米`
  }
  if (r.type === 'pest') {
    const p = r.data?.pesticides?.[0]
    return p ? `农药名称: ${p.name} 作用: ${p.effect} 用量: ${p.amount}` : ''
  }
  if (r.type === 'diary') return (r.data?.content || '').slice(0, 80)
  if (r.type === 'issue') return (r.data?.desc || '').slice(0, 80)
  return ''
}

async function load() {
  const params = { type_filter: typeFilter.value }
  if (search.value) params.search = search.value
  if (startDate.value) params.start_date = startDate.value
  if (endDate.value) params.end_date = endDate.value
  if (fieldFilter.value) params.field_id = fieldFilter.value
  if (cropFilter.value) params.crop = cropFilter.value
  const { data } = await farmlogApi.list(params)
  list.value = data || []
  if (expandedDates.value.size === 0 && list.value.length) {
    expandedDates.value = new Set(Object.keys(groupedList.value))
  }
}

watch([search, startDate, endDate, fieldFilter, cropFilter], () => load())

onMounted(async () => {
  const { data } = await fieldsApi.list()
  fields.value = data || []
  load()
})
</script>

<style scoped>
.farmlog-list .page-body { padding: 16px; padding-bottom: 80px; }
.hdr-title-bar { padding: 10px 16px; background: #F5F5F5; font-size: 14px; color: #666; }
.hdr-banner {
  display: flex; align-items: center; padding: 12px 16px;
  background: var(--primary-gradient); color: #FFF;
}
.hdr-back { width: 36px; height: 36px; border: none; background: rgba(255,255,255,.2); color: #FFF; font-size: 24px; border-radius: 8px; cursor: pointer; flex-shrink: 0; }
.hdr-left { flex: 1; display: flex; align-items: center; gap: 6px; margin-left: 12px; }
.hdr-label { font-size: 16px; font-weight: 600; }
.hdr-icon { font-size: 14px; }
.hdr-actions { display: flex; align-items: center; gap: 10px; }
.btn-add, .btn-export { padding: 8px 14px; border-radius: 8px; font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 4px; }
.btn-add { background: #FFF; color: var(--primary); border: none; }
.btn-export { background: rgba(255,255,255,.2); color: #FFF; border: 1px solid rgba(255,255,255,.4); }
.btn-icon { font-size: 10px; }
.filter-section { margin-bottom: 16px; }
.search-input { width: 100%; padding: 12px 14px; border: 1px solid rgba(46,125,50,.2); border-radius: 10px; font-size: 14px; margin-bottom: 10px; box-sizing: border-box; }
.filter-row { display: flex; gap: 12px; margin-bottom: 10px; }
.filter-item { flex: 1; display: flex; align-items: center; gap: 8px; }
.filter-item label { font-size: 13px; color: #666; white-space: nowrap; }
.filter-input, .filter-select { flex: 1; padding: 8px 10px; border: 1px solid rgba(46,125,50,.2); border-radius: 8px; font-size: 13px; }
.type-tabs { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }
.type-tab { padding: 8px 14px; border: 1px solid var(--primary-border); background: #FFF; color: var(--text2); border-radius: 20px; font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 4px; }
.type-tab.active { background: var(--primary); color: #FFF; border-color: var(--primary); }
.type-icon { font-size: 14px; }
.log-list { display: flex; flex-direction: column; gap: 12px; }
.date-group { background: #FFF; border: 1px solid rgba(46,125,50,.1); border-radius: 12px; overflow: hidden; }
.date-header { padding: 12px 16px; background: #F7FAF7; font-size: 14px; font-weight: 600; color: #1B2E1B; cursor: pointer; display: flex; align-items: center; gap: 8px; }
.date-arrow { color: var(--primary); font-size: 12px; }
.date-entries { padding: 0 16px 12px; }
.log-entry { padding: 12px 0; border-bottom: 1px solid rgba(46,125,50,.08); display: flex; gap: 12px; cursor: pointer; }
.log-entry:last-child { border-bottom: none; }
.entry-time { font-size: 14px; font-weight: 600; color: var(--primary); min-width: 50px; }
.entry-main { flex: 1; }
.entry-type { display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 12px; margin-bottom: 6px; }
.entry-loc { font-size: 14px; font-weight: 500; color: #1B2E1B; margin-bottom: 2px; }
.entry-recorder { font-size: 12px; color: var(--text2); margin-bottom: 4px; }
.entry-detail { font-size: 12px; color: #666; line-height: 1.5; }
.empty { padding: 48px 0; text-align: center; color: #9DB89C; font-size: 14px; }
.btn-load-more { width: 100%; padding: 12px; margin-top: 16px; background: #F7FAF7; color: var(--primary); border: 1px dashed var(--primary-border); border-radius: 10px; font-size: 14px; cursor: pointer; }
</style>
