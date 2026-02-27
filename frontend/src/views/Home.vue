<template>
  <div class="page farmer-home">
    <!-- 顶部绿色状态栏 -->
    <div class="home-top-bar">
      <div class="top-bar-left">
        <span class="loc-icon">📍</span>
        <span class="loc-text">石河子市</span>
      </div>
      <div class="top-bar-center">
        <span class="weather-main">晴 22°</span>
        <span class="weather-sun">☀️</span>
      </div>
      <div class="top-bar-right">
        <span class="weather-detail">风力3级 · PM2.5 35 · 湿度 45%</span>
        <span class="bell-icon" @click="$router.push('/alerts')">🔔</span>
      </div>
    </div>

    <div class="page-body">
      <!-- 预警模块 -->
      <div class="alert-card" @click="$router.push('/alerts')">
        <span class="alert-icon">⚠️</span>
        <span class="alert-text">预警 {{ unreadCount }}</span>
        <span class="alert-arrow">▼</span>
      </div>

      <!-- 核心功能 -->
      <div class="sec">
        <div class="sec-hd"><span class="sec-title">核心功能</span></div>
        <div class="core-grid">
          <div v-for="item in coreFuncs" :key="item.key" class="core-item" :class="{ 'core-item-add': item.key === 'add' }" @click="onCoreFunc(item)">
            <span class="core-icon-wrap" v-if="item.key !== 'add'"><span class="core-icon">{{ item.icon }}</span><span class="ai-badge">⚡</span></span>
            <span class="core-icon-wrap" v-else><span class="core-icon-add">+</span></span>
            <span class="core-label">{{ item.label }}</span>
          </div>
        </div>
      </div>

      <!-- 待办模块 -->
      <div class="todo-card" @click="toast('待办列表')">
        <span class="todo-text">待办 {{ todoCount }}</span>
        <span class="todo-arrow">▼</span>
      </div>

      <!-- 我的农场地块 -->
      <div class="sec">
        <div class="sec-hd" style="margin-bottom:12px">
          <span class="sec-title">我的农场地块</span>
          <div style="display:flex;gap:8px">
            <button class="btn-add btn-farm" @click="$router.push('/farm/create')">+ 农场</button>
            <button class="btn-add btn-field" @click="$router.push('/fields')">+ 地块</button>
          </div>
        </div>
        <div class="filter-row">
          <select v-model="farmFilter" class="filter-select"><option value="">全部农场</option><option v-for="f in mergedFarmOptions" :key="f.id || f.name" :value="f.name">{{ f.name }}</option></select>
          <button v-if="farmFilter && selectedFarm?.id" class="btn-view-farm" @click="$router.push('/farm/' + selectedFarm.id)">查看农场</button>
          <select v-model="fieldFilter" class="filter-select"><option value="">全部地块</option></select>
          <div class="search-wrap"><span class="search-icon">🔍</span><input v-model="searchKey" type="text" placeholder="搜索地块或作物、主管" class="search-input" /></div>
        </div>
        <div class="field-grid">
          <div v-for="f in filteredFields" :key="f.id" class="field-card" @click="$router.push('/field/' + f.id)">
            <div class="field-card-hd">
              <span class="field-name">{{ f.name }}</span>
              <span class="field-status" :class="f.status">
                <span v-if="f.status === 'pending_irrigate'" class="status-icon">💧</span>
                <span v-else class="status-icon">🕐</span>
                {{ f.statusText }}{{ f.statusDuration ? ' ' + f.statusDuration : '' }}
              </span>
            </div>
            <div class="field-crop">{{ f.crop }} · {{ f.planting }}</div>
            <div class="field-meta">面积: {{ f.area }}亩 · 主管: {{ f.supervisor }}</div>
            <div class="field-actions">
              <button class="field-btn" @click.stop="$router.push('/farmlog/add')">记农事</button>
              <button class="field-btn" @click.stop="toast('分享')">分享</button>
              <button class="field-btn" @click.stop="toast('更多')">⋯</button>
            </div>
          </div>
        </div>
      </div>
      <div style="height:24px"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from '../composables/useToast'
import { fieldsApi, alertsApi, farmsApi } from '../api'

const router = useRouter()
const { toast } = useToast()

const fields = ref([])
const alerts = ref([])
const farmFilter = ref('')
const fieldFilter = ref('')
const searchKey = ref('')

const coreFuncs = [
  { key: 'add_manager', icon: '👤', label: '添加大总管' },
  { key: 'add_farmlog', icon: '📝', label: '添加农事记录' },
  { key: 'view_farmlog', icon: '📋', label: '查看农事记录' },
  { key: 'add_valve', icon: '🔘', label: '添加阀门' },
  { key: 'adjust_valve', icon: '🎛️', label: '调整电动阀' },
  { key: 'irrigation', icon: '💧', label: '灌溉任务' },
  { key: 'machinery', icon: '🚜', label: '农机服务' },
  { key: 'patrol', icon: '✈️', label: '智能巡田' },
  { key: 'advice', icon: '💡', label: '指导建议' },
  { key: 'add', icon: '+', label: '添加' },
]

const farmList = ref([])
const unreadCount = computed(() => alerts.value.filter(a => !a.read).length)
const todoCount = ref(3)
const farms = computed(() => [...new Set(fields.value.map(f => f.farm).filter(Boolean))])
const mergedFarmOptions = computed(() => {
  const byName = {}
  farmList.value.forEach(f => { byName[f.name] = f })
  farms.value.forEach(n => { if (n && !byName[n]) byName[n] = { id: null, name: n } })
  return Object.values(byName)
})
const selectedFarm = computed(() => mergedFarmOptions.value.find(f => f.name === farmFilter.value) || null)
const filteredFields = computed(() => {
  let list = fields.value
  if (farmFilter.value) list = list.filter(f => f.farm === farmFilter.value)
  if (searchKey.value) {
    const k = searchKey.value.toLowerCase()
    list = list.filter(f =>
      (f.name && f.name.toLowerCase().includes(k)) ||
      (f.crop && f.crop.toLowerCase().includes(k)) ||
      (f.supervisor && f.supervisor.includes(searchKey.value))
    )
  }
  return list
})

function onCoreFunc(item) {
  if (item.key === 'add_farmlog') router.push('/farmlog/add')
  else if (item.key === 'view_farmlog') router.push('/farmlog')
  else if (item.key === 'adjust_valve') toast('灌溉控制')
  else if (item.key === 'irrigation') router.push('/irrigation')
  else if (item.key === 'patrol') router.push('/patrol')
  else if (item.key === 'machinery') router.push('/machinery')
  else if (item.key === 'advice') router.push('/guidance')
  else toast(item.label)
}

onMounted(async () => {
  try {
    const [fRes, aRes, farmsRes] = await Promise.all([fieldsApi.list(), alertsApi.list(), farmsApi.list()])
    fields.value = fRes.data
    alerts.value = aRes.data
    farmList.value = farmsRes.data || []
  } catch (e) {
    toast('数据加载失败')
  }
})
</script>

<style scoped>
.farmer-home .page-body { padding-top: 0; }
.home-top-bar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 16px 14px; background: var(--primary-gradient);
  color: #FFF; flex-shrink: 0;
}
.top-bar-left { display: flex; align-items: center; gap: 6px; font-size: 14px; }
.loc-icon { font-size: 16px; }
.top-bar-center { display: flex; align-items: center; gap: 8px; font-size: 18px; font-weight: 600; }
.weather-sun { font-size: 22px; }
.top-bar-right { display: flex; align-items: center; gap: 10px; font-size: 12px; opacity: .95; }
.bell-icon { font-size: 18px; cursor: pointer; }
.alert-card {
  margin: 12px 16px 0; padding: 12px 16px; background: var(--red); color: #FFF;
  border-radius: 10px; display: flex; align-items: center; gap: 10px; cursor: pointer;
}
.alert-icon { font-size: 20px; }
.alert-text { flex: 1; font-size: 15px; font-weight: 600; }
.alert-arrow { font-size: 12px; opacity: .8; }
.core-grid {
  display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px;
}
.core-item {
  display: flex; flex-direction: column; align-items: center; gap: 6px;
  padding: 12px 6px; background: var(--card); border: 1px solid var(--border2);
  border-radius: 10px; cursor: pointer; transition: .15s;
}
.core-item:active { background: var(--card2); transform: scale(.97); }
.core-item-add { border: 2px dashed var(--primary-border); }
.core-item-add .core-icon-add { font-size: 28px; font-weight: 300; color: var(--primary); }
.core-icon-wrap { position: relative; }
.core-icon { font-size: 24px; }
.ai-badge { position: absolute; top: -4px; right: -6px; font-size: 10px; }
.core-label { font-size: 11px; color: var(--text2); text-align: center; line-height: 1.3; }
.todo-card {
  margin: 12px 16px 0; padding: 12px 16px; background: var(--card);
  border: 1px solid var(--border2); border-radius: 10px;
  display: flex; align-items: center; justify-content: space-between; cursor: pointer;
}
.todo-text { font-size: 14px; font-weight: 500; color: var(--text); }
.todo-arrow { font-size: 12px; color: var(--text3); }
.btn-add { padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: 500; border: none; cursor: pointer; }
.btn-farm { background: var(--card); color: var(--primary); border: 1px solid var(--primary-border); }
.btn-field { background: var(--primary); color: #FFF; }
.btn-view-farm { padding: 6px 12px; font-size: 12px; color: var(--primary); background: var(--primary-dim); border: 1px solid var(--primary-border); border-radius: 8px; cursor: pointer; white-space: nowrap; }
.filter-row { display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap; }
.filter-select { flex: 1; min-width: 80px; padding: 8px 10px; border: 1px solid var(--primary-border); border-radius: 8px; font-size: 13px; background: var(--card); }
.search-wrap { flex: 2; min-width: 140px; display: flex; align-items: center; gap: 8px; padding: 8px 12px; background: var(--surface); border: 1px solid var(--border2); border-radius: 8px; }
.search-icon { font-size: 14px; }
.search-input { flex: 1; font-size: 13px; background: none; border: none; outline: none; }
.field-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.field-card {
  background: var(--card); border: 1px solid var(--border2); border-radius: 12px;
  padding: 14px; box-shadow: 0 2px 8px var(--primary-dim);
  cursor: pointer;
}
.field-card-hd { display: flex; align-items: flex-start; justify-content: space-between; gap: 8px; margin-bottom: 6px; }
.field-name { font-size: 14px; font-weight: 600; color: var(--text); }
.field-status { font-size: 11px; padding: 2px 8px; border-radius: 10px; white-space: nowrap; }
.field-status.pending_irrigate { background: var(--orange-dim); color: var(--amber); }
.field-status.irrigating { background: var(--blue-dim); color: var(--blue); }
.field-status.working { background: rgba(103,58,183,.12); color: #673AB7; }
.status-icon { font-size: 10px; margin-right: 2px; }
.field-crop { font-size: 12px; color: var(--text2); margin-bottom: 4px; }
.field-meta { font-size: 11px; color: var(--text3); margin-bottom: 10px; }
.field-actions { display: flex; gap: 8px; }
.field-btn { flex: 1; padding: 6px 0; font-size: 12px; color: var(--primary); background: var(--primary-dim); border: none; border-radius: 6px; cursor: pointer; }
</style>
