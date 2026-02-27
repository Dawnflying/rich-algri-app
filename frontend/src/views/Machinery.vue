<template>
  <div class="page machinery-home">
    <div class="hdr-title-bar"><button class="hdr-back" @click="$router.back()">‹</button>农机服务首页</div>
    <div class="hdr-banner">
      <span class="banner-title">农机服务</span>
      <div class="hdr-actions">
        <button class="btn-hdr" @click="$router.push('/machinery/demands')">
          <span class="btn-icon">✎</span>
          我的需求
        </button>
        <button class="btn-hdr" @click="$router.push('/machinery/orders')">
          <span class="btn-icon">📋</span>
          我的订单
        </button>
      </div>
    </div>

    <div class="page-body">
      <div class="loc-row">
        <span class="loc-pin">📍</span>
        <span class="loc-text">石河子市</span>
        <span class="loc-arrow">▼</span>
        <span class="loc-hint">根据您的位置推荐服务</span>
      </div>

      <div class="search-row">
        <div class="search-input-wrap">
          <span class="search-icon">🔍</span>
          <input v-model="searchKey" type="text" placeholder="搜索服务或服务商" class="search-input" />
        </div>
        <button class="btn-filter" @click="toast('筛选')">筛选</button>
      </div>

      <div class="machine-cats">
        <button v-for="c in machineCats" :key="c.key" class="cat-btn" :class="{ active: machineCat === c.key }" @click="machineCat = c.key">
          <span class="cat-icon">{{ c.icon }}</span>
          {{ c.label }}
        </button>
      </div>

      <div class="service-tabs" v-if="machineCat !== 'remote'">
        <button v-for="t in serviceTabs" :key="t.key" class="service-tab" :class="{ active: serviceTab === t.key }" @click="serviceTab = t.key">
          {{ t.label }}
        </button>
      </div>

      <!-- 遥感套餐列表 -->
      <template v-if="machineCat === 'remote'">
        <div class="remote-packages">
          <div v-for="pkg in remotePackages" :key="pkg.key" class="remote-pkg-card">
            <div class="pkg-name">{{ pkg.name }}</div>
            <div class="pkg-price">¥{{ pkg.price }}/亩</div>
            <div class="pkg-detail">服务频次: {{ pkg.frequency }}</div>
            <div class="pkg-detail">提供报告: {{ pkg.report }}</div>
            <div class="pkg-detail">可选分辨率: {{ pkg.resolution }}</div>
            <div class="pkg-detail">服务周期: {{ pkg.period }}</div>
            <div v-if="pkg.discount" class="pkg-discount">✓ 享受9折优惠</div>
            <button class="btn-select-pkg" @click="$router.push({ path: '/machinery/remote/' + pkg.key })">⚡ 选择此套餐</button>
          </div>
        </div>
        <div class="service-desc">
          <div class="desc-title">服务说明</div>
          <ul class="desc-list">
            <li>标准化平台服务，多服务商竞价模式</li>
            <li>基于卫星遥感技术，采集数据</li>
            <li>全国覆盖，不受地域限制</li>
            <li>专业团队分析，确保准确</li>
          </ul>
        </div>
      </template>

      <!-- 无人机/其他农机服务列表 -->
      <template v-else>
        <div class="list-header">
          <span class="list-title">智能推荐</span>
          <span class="list-arrow">▼</span>
          <button class="btn-filter-sm" @click="toast('筛选')">筛选</button>
        </div>
        <div class="service-list">
          <div v-for="s in filteredServices" :key="s.id" class="service-card" @click="$router.push('/machinery/package/' + s.id)">
            <div class="card-left">
              <span class="card-icon">{{ s.icon }}</span>
              <div class="card-info">
                <div class="card-title">{{ s.title }}</div>
                <span class="card-tag" :class="s.tagClass">{{ s.tag }}</span>
                <div class="card-model">{{ s.model }}</div>
                <div class="card-meta">服务商: {{ s.provider }}</div>
                <div class="card-meta">服务区域: {{ s.area }}</div>
                <div class="card-meta">计价方式: {{ s.pricing }}</div>
                <div class="card-meta">距离: {{ s.distance }}</div>
              </div>
            </div>
            <button class="btn-book" @click.stop="$router.push('/machinery/package/' + s.id)">⚡ 立即预约</button>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useToast } from '../composables/useToast'

const { toast } = useToast()
const searchKey = ref('')
const machineCat = ref('drone')
const serviceTab = ref('all')

const machineCats = [
  { key: 'drone', label: '无人机', icon: '✈️' },
  { key: 'other', label: '其他农机', icon: '🚜' },
  { key: 'remote', label: '遥感', icon: '📡' },
]

const serviceTabs = [
  { key: 'all', label: '全部' },
  { key: 'spray', label: '植保打药' },
  { key: 'patrol', label: '巡田监测' },
]

const remotePackages = [
  { key: 'month', name: '月套餐', price: 15, frequency: '5天一次', report: '长势分析报告', resolution: '10米、2米、1米、0.8米、0.5米', period: '30天', discount: false },
  { key: 'quarter', name: '季套餐', price: 40, frequency: '5天一次', report: '长势分析报告', resolution: '10米、2米、1米、0.8米、0.5米', period: '90天', discount: true },
  { key: 'year', name: '年套餐', price: 120, frequency: '5天一次', report: '长势分析报告', resolution: '10米、2米、1米、0.8米、0.5米', period: '365天', discount: true },
]

const services = [
  { id: 1, title: '无人机·植保打药套餐', tag: '现结', tagClass: 'tag-green', model: '大疆M3M多光谱无人机', provider: '蓝天无人机服务(企业)', area: '石河子市及周边', pricing: '¥15/亩', distance: '5km', icon: '✈️', type: 'spray' },
  { id: 2, title: '无人机·巡田监测套餐', tag: '年底结算', tagClass: 'tag-yellow', model: '大疆M300 RTK无人机', provider: '绿源农机服务(企业)', area: '石河子市', pricing: '¥8/亩', distance: '8km', icon: '✈️', type: 'patrol' },
]

const filteredServices = computed(() => {
  let list = services
  if (serviceTab.value !== 'all') list = list.filter(s => s.type === serviceTab.value)
  if (searchKey.value) {
    const k = searchKey.value.toLowerCase()
    list = list.filter(s => (s.title + s.provider).toLowerCase().includes(k))
  }
  return list
})
</script>

<style scoped>
.machinery-home .page-body { padding: 16px; padding-bottom: 32px; }
.hdr-title-bar { display: flex; align-items: center; gap: 12px; padding: 10px 16px; background: #F5F5F5; font-size: 14px; color: #666; }
.hdr-back { width: 32px; height: 32px; border: none; background: rgba(46,125,50,.1); color: var(--primary); font-size: 22px; border-radius: 8px; cursor: pointer; }
.hdr-banner {
  display: flex; align-items: center; justify-content: space-between; padding: 12px 16px;
  background: linear-gradient(135deg, var(--primary), var(--primary-light)); color: #FFF;
}
.banner-title { font-size: 18px; font-weight: 600; }
.hdr-actions { display: flex; gap: 10px; }
.btn-hdr { padding: 8px 12px; background: rgba(255,255,255,.2); color: #FFF; border: none; border-radius: 8px; font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 4px; }
.btn-icon { font-size: 14px; }
.loc-row { display: flex; align-items: center; gap: 6px; margin-bottom: 12px; font-size: 13px; }
.loc-pin { color: var(--primary); }
.loc-text { font-weight: 500; color: #1B2E1B; }
.loc-arrow { font-size: 10px; color: var(--text3); }
.loc-hint { margin-left: auto; color: var(--text2); font-size: 12px; }
.search-row { display: flex; gap: 10px; margin-bottom: 14px; }
.search-input-wrap { flex: 1; display: flex; align-items: center; gap: 8px; padding: 10px 14px; background: #F7FAF7; border: 1px solid rgba(46,125,50,.15); border-radius: 10px; }
.search-icon { font-size: 16px; }
.search-input { flex: 1; border: none; background: none; font-size: 14px; outline: none; }
.btn-filter { padding: 10px 16px; background: #FFF; color: var(--primary); border: 1px solid rgba(46,125,50,.3); border-radius: 10px; font-size: 13px; cursor: pointer; }
.machine-cats { display: flex; gap: 12px; margin-bottom: 14px; overflow-x: auto; padding-bottom: 4px; }
.cat-btn { flex-shrink: 0; padding: 10px 16px; border: 1px solid var(--primary-border); background: #FFF; color: var(--text2); border-radius: 10px; font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 6px; }
.cat-btn.active { background: var(--primary); color: #FFF; border-color: var(--primary); }
.cat-icon { font-size: 16px; }
.service-tabs { display: flex; gap: 10px; margin-bottom: 14px; }
.service-tab { padding: 8px 16px; border: 1px solid var(--primary-border); background: #FFF; color: var(--text2); border-radius: 20px; font-size: 13px; cursor: pointer; }
.service-tab.active { background: var(--primary); color: #FFF; border-color: var(--primary); }
.list-header { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
.list-title { font-size: 14px; font-weight: 600; color: #1B2E1B; }
.list-arrow { font-size: 10px; color: var(--text3); }
.btn-filter-sm { margin-left: auto; padding: 4px 10px; font-size: 12px; color: var(--primary); background: rgba(46,125,50,.1); border: none; border-radius: 6px; cursor: pointer; }
.service-list { display: flex; flex-direction: column; gap: 12px; }
.service-card { display: flex; gap: 12px; padding: 14px; background: #FFF; border: 1px solid rgba(46,125,50,.1); border-radius: 12px; box-shadow: 0 2px 8px rgba(46,125,50,.06); cursor: pointer; }
.card-left { flex: 1; display: flex; gap: 12px; }
.card-icon { font-size: 28px; flex-shrink: 0; }
.card-info { flex: 1; min-width: 0; }
.card-title { font-size: 14px; font-weight: 600; color: #1B2E1B; margin-bottom: 4px; }
.card-tag { font-size: 11px; padding: 2px 8px; border-radius: 10px; margin-left: 8px; }
.card-tag.tag-green { background: rgba(46,125,50,.15); color: var(--primary); }
.card-tag.tag-yellow { background: var(--orange-dim); color: var(--amber); }
.card-model { font-size: 12px; color: var(--text2); margin-bottom: 6px; }
.card-meta { font-size: 11px; color: var(--text3); margin-bottom: 2px; }
.btn-book { flex-shrink: 0; padding: 10px 14px; background: var(--primary); color: #FFF; border: none; border-radius: 8px; font-size: 13px; font-weight: 500; cursor: pointer; align-self: flex-start; }
.remote-packages { display: flex; flex-direction: column; gap: 16px; margin-bottom: 20px; }
.remote-pkg-card { background: #FFF; border: 1px solid rgba(103,58,183,.15); border-radius: 12px; padding: 16px; box-shadow: 0 2px 8px rgba(103,58,183,.08); }
.pkg-name { font-size: 16px; font-weight: 600; color: #1B2E1B; margin-bottom: 8px; }
.pkg-price { font-size: 18px; font-weight: 600; color: #673AB7; margin-bottom: 10px; }
.pkg-detail { font-size: 13px; color: #666; margin-bottom: 4px; }
.pkg-discount { font-size: 13px; color: var(--primary); margin: 8px 0; }
.btn-select-pkg { width: 100%; padding: 12px; background: linear-gradient(135deg, #673AB7, #7B1FA2); color: #FFF; border: none; border-radius: 10px; font-size: 14px; font-weight: 500; cursor: pointer; margin-top: 8px; }
.service-desc { background: #F5F5F5; border-radius: 12px; padding: 16px; }
.desc-title { font-size: 14px; font-weight: 600; color: #333; margin-bottom: 10px; }
.desc-list { font-size: 13px; color: #666; line-height: 1.8; padding-left: 18px; margin: 0; }
</style>
