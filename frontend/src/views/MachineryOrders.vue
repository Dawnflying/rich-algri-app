<template>
  <div class="page orders-list">
    <div class="hdr-bar">
      <button class="hdr-back" @click="$router.back()">‹</button>
      <span class="hdr-title">我的订单</span>
    </div>

    <div class="search-row">
      <span class="search-icon">🔍</span>
      <input v-model="searchKey" type="text" placeholder="搜索订单号、套餐名称或服务商" class="search-input" />
    </div>

    <div class="filter-tabs">
      <div class="filter-row">
        <span class="filter-label">服务类型</span>
        <div class="tab-group">
          <button v-for="t in serviceTypes" :key="t.key" class="tab-btn" :class="{ active: serviceType === t.key }" @click="serviceType = t.key">
            {{ t.label }}
          </button>
        </div>
      </div>
      <div class="filter-row">
        <span class="filter-label">订单状态</span>
        <div class="tab-group">
          <button v-for="t in statusTabsWithCount" :key="t.key" class="tab-btn" :class="{ active: statusGroup === t.key }" @click="statusGroup = t.key">
            {{ t.label }} <span v-if="t.count" class="count">({{ t.count }})</span>
          </button>
        </div>
      </div>
    </div>

    <div class="page-body">
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="!filteredOrders.length" class="empty">暂无订单</div>
      <div v-else class="order-list">
        <div v-for="o in filteredOrders" :key="o.id" class="order-card" @click="$router.push('/machinery/order/' + o.id)">
          <div class="card-service">{{ o.serviceContent }}</div>
          <div class="card-provider">{{ o.provider }}</div>
          <div class="card-meta">
            <span>{{ o.plotCount }}个地块</span>
            <span class="sep">总价: ¥{{ formatPrice(o.finalPrice) }}</span>
          </div>
          <div class="card-footer">
            <span class="order-no">{{ o.orderNo }}</span>
            <span class="order-time">{{ o.orderTime }}</span>
          </div>
          <div class="card-actions">
            <span class="status-tag" :class="o.status">{{ o.statusText }}</span>
            <button v-if="o.status === 'pending_confirm'" class="btn-action primary" @click.stop="$router.push('/machinery/order/' + o.id)">去确认</button>
            <button v-else-if="o.status === 'pending_payment'" class="btn-action primary" @click.stop="$router.push('/machinery/order/' + o.id)">去支付</button>
            <button v-else-if="o.status === 'in_progress'" class="btn-action primary" @click.stop="$router.push('/machinery/order/' + o.id)">查看监控</button>
            <button v-else-if="o.status === 'pending_acceptance'" class="btn-action primary" @click.stop="$router.push('/machinery/order/' + o.id)">去验收</button>
          </div>
        </div>
      </div>
      <div v-if="filteredOrders.length" class="load-more">下拉加载更多</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { ordersApi } from '../api'

const loading = ref(true)
const orders = ref([])
const searchKey = ref('')
const serviceType = ref('all')
const statusGroup = ref('pending')

const serviceTypes = [
  { key: 'all', label: '全部' },
  { key: 'drone', label: '无人机' },
  { key: 'remote', label: '遥感' },
  { key: 'other', label: '其他农机' },
]

const statusTabs = [
  { key: 'pending', label: '待处理' },
  { key: 'progress', label: '进行中' },
  { key: 'acceptance', label: '待验收' },
  { key: 'completed', label: '已完成' },
]

const statusCounts = computed(() => {
  const p = { pending: 0, progress: 0, acceptance: 0, completed: 0 }
  orders.value.forEach(o => {
    const s = o.status
    if (['pending_quote', 'pending_confirm', 'pending_payment'].includes(s)) p.pending++
    else if (s === 'in_progress') p.progress++
    else if (s === 'pending_acceptance') p.acceptance++
    else if (['completed', 'cancelled'].includes(s)) p.completed++
  })
  return p
})

const statusTabsWithCount = computed(() =>
  statusTabs.map(t => ({ ...t, count: statusCounts.value[t.key] }))
)

const filteredOrders = computed(() => {
  let items = orders.value
  const q = searchKey.value.trim().toLowerCase()
  if (q) {
    items = items.filter(o =>
      (o.orderNo || '').toLowerCase().includes(q) ||
      (o.serviceContent || '').toLowerCase().includes(q) ||
      (o.provider || '').toLowerCase().includes(q)
    )
  }
  if (serviceType.value && serviceType.value !== 'all') {
    items = items.filter(o => o.serviceType === serviceType.value)
  }
  if (statusGroup.value === 'pending') {
    items = items.filter(o => ['pending_quote', 'pending_confirm', 'pending_payment'].includes(o.status))
  } else if (statusGroup.value === 'progress') {
    items = items.filter(o => o.status === 'in_progress')
  } else if (statusGroup.value === 'acceptance') {
    items = items.filter(o => o.status === 'pending_acceptance')
  } else if (statusGroup.value === 'completed') {
    items = items.filter(o => ['completed', 'cancelled'].includes(o.status))
  }
  return items
})

function formatPrice(v) {
  if (v == null) return '—'
  return Number(v).toFixed(2)
}

async function fetchOrders() {
  loading.value = true
  try {
    const { data } = await ordersApi.list({
      q: searchKey.value || undefined,
      serviceType: serviceType.value === 'all' ? undefined : serviceType.value,
    })
    orders.value = data || []
  } finally {
    loading.value = false
  }
}

onMounted(fetchOrders)
watch([searchKey, serviceType], fetchOrders)
</script>

<style scoped>
.orders-list .page-body { padding: 16px; padding-top: 0; }
.hdr-bar { display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: linear-gradient(135deg, var(--primary), var(--primary-light)); color: #FFF; }
.hdr-back { width: 36px; height: 36px; border: none; background: rgba(255,255,255,.2); color: #FFF; font-size: 24px; border-radius: 8px; cursor: pointer; }
.hdr-title { font-size: 18px; font-weight: 600; }
.search-row { display: flex; align-items: center; gap: 8px; padding: 12px 16px; background: #FFF; border-bottom: 1px solid #EEE; }
.search-icon { font-size: 16px; }
.search-input { flex: 1; border: none; font-size: 14px; outline: none; }
.filter-tabs { padding: 12px 16px; background: #F5F5F5; }
.filter-row { margin-bottom: 10px; }
.filter-row:last-child { margin-bottom: 0; }
.filter-label { font-size: 12px; color: #666; display: block; margin-bottom: 8px; }
.tab-group { display: flex; flex-wrap: wrap; gap: 8px; }
.tab-btn { font-size: 13px; padding: 6px 12px; border-radius: 8px; border: none; background: #FFF; color: #666; cursor: pointer; }
.tab-btn.active { background: var(--primary); color: #FFF; }
.tab-btn .count { opacity: .9; }
.loading, .empty { text-align: center; padding: 40px; color: #999; }
.order-list { display: flex; flex-direction: column; gap: 12px; }
.order-card { background: #FFF; border-radius: 12px; padding: 16px; box-shadow: 0 1px 4px rgba(0,0,0,.06); cursor: pointer; }
.card-service { font-size: 15px; font-weight: 600; color: #1B2E1B; margin-bottom: 6px; }
.card-provider { font-size: 13px; color: #666; margin-bottom: 6px; }
.card-meta { font-size: 13px; color: #666; margin-bottom: 8px; }
.card-meta .sep { margin-left: 12px; }
.card-footer { font-size: 12px; color: #999; margin-bottom: 10px; }
.order-time { margin-left: 12px; }
.card-actions { display: flex; justify-content: space-between; align-items: center; }
.status-tag { font-size: 12px; padding: 4px 10px; border-radius: 8px; }
.status-tag.pending_quote { background: var(--orange-dim); color: var(--amber); }
.status-tag.pending_confirm { background: #E8F0F8; color: var(--blue); }
.status-tag.pending_payment { background: var(--red-dim); color: var(--red); }
.status-tag.in_progress { background: #F0F7F0; color: var(--primary); }
.status-tag.pending_acceptance { background: #E8F0F8; color: var(--blue); }
.status-tag.completed, .status-tag.cancelled { background: #F5F5F5; color: #999; }
.btn-action { font-size: 13px; padding: 6px 14px; border-radius: 8px; border: none; cursor: pointer; }
.btn-action.primary { background: var(--primary); color: #FFF; }
.load-more { text-align: center; padding: 16px; font-size: 13px; color: #999; }
</style>
