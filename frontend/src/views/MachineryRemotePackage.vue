<template>
  <div class="page remote-package">
    <div class="hdr-bar">
      <button class="hdr-back" @click="$router.back()">‹</button>
      <span class="hdr-title">遥感套餐订阅</span>
    </div>

    <div class="page-body">
      <div class="service-banner purple">
        <div class="banner-title">遥感巡田服务</div>
        <div class="banner-sub">5天一次监测，专业长势分析报告</div>
      </div>

      <div class="package-main">
        <div class="package-name">标准版遥感巡田套餐</div>
        <div class="period-tabs">
          <button v-for="t in periodTabs" :key="t.key" class="period-tab" :class="{ active: period === t.key }" @click="period = t.key">
            {{ t.label }}
          </button>
        </div>
        <div class="base-price">¥{{ currentPrice }}/亩</div>
        <div class="package-tags">
          <span class="tag">可预约</span>
          <span class="tag">5天1次监测</span>
          <span class="tag">全国覆盖</span>
        </div>
      </div>

      <div class="info-section">
        <div class="section-title">套餐包含内容</div>
        <ul class="content-list">
          <li>每天一次监测、每月并次完整报告</li>
          <li>高植被指数分析(NDVI、SAVI等)</li>
          <li>全国覆盖，不受地域限制</li>
        </ul>
      </div>

      <div class="info-section">
        <div class="section-title">服务商信息</div>
        <div class="provider-info">
          <span class="provider-icon">🏢</span>
          <div>
            <div class="provider-name">地小丰平台官方服务</div>
            <div class="provider-support">专业团队全国7×24小时技术支持</div>
          </div>
        </div>
      </div>

      <div class="info-section">
        <div class="section-title">计价规则</div>
        <div class="pricing-rules">
          <div class="rule-item">单价: ¥{{ currentPrice }}/亩</div>
          <div class="rule-item">月度套餐: ¥15/亩 (30天服务期)</div>
          <div class="rule-item">季度套餐: ¥40/亩 (90天服务期, 享受9折优惠)</div>
          <div class="rule-item">年度套餐: ¥120/亩 (365天服务期, 享受9折优惠)</div>
          <div class="rule-note">全国统一价格，不受地域限制</div>
        </div>
      </div>

      <div style="height: 100px"></div>
    </div>

    <div class="bottom-bar">
      <span class="bottom-name">标准版遥感巡田套餐 · ¥{{ estimatedTotal }}</span>
      <button class="btn-book" @click="showBooking = true">⚡ 立即预约</button>
    </div>

    <!-- 遥感预约弹窗 -->
    <div class="modal-overlay" :class="{ open: showBooking }" @click.self="showBooking = false">
      <div class="modal-sheet">
        <div class="modal-handle"></div>
        <div class="modal-hd">
          <span class="modal-title">⚡ 遥感预约</span>
        </div>
        <div class="modal-banner purple">
          <div class="banner-title">遥感巡田服务</div>
          <div class="banner-sub">5天一次监测，专业长势分析报告</div>
        </div>

        <div class="booking-section">
          <div class="booking-block">
            <div class="block-label">选择地块</div>
            <div v-for="farm in farmsWithFields" :key="farm.id" class="farm-group">
              <div class="farm-hd" @click="toggleFarm(farm.id)">
                <span class="farm-name">{{ farm.name }}</span>
                <span class="farm-arrow">{{ expandedFarms.has(farm.id) ? '▼' : '▶' }}</span>
              </div>
              <div v-if="expandedFarms.has(farm.id)" class="farm-plots">
                <label v-for="f in (farm.fields || [])" :key="f.id" class="plot-item">
                  <input type="checkbox" :value="farm.id+'-'+f.id" v-model="selectedPlotIds" />
                  <span>{{ f.name }}</span>
                  <span class="plot-area">{{ f.area }}亩</span>
                </label>
              </div>
            </div>
            <div class="plot-summary">已选择{{ selectedPlotIds.length }}个地块，总面积: {{ totalArea }}亩</div>
          </div>

          <div class="booking-block">
            <div class="block-label">选择时间与价格</div>
            <div class="form-row">
              <div class="form-group">
                <label>选择开始时间</label>
                <input v-model="bookingForm.startDate" type="date" class="form-input" />
              </div>
              <div class="form-group">
                <label>时段</label>
                <select v-model="bookingForm.period" class="form-select">
                  <option value="am">上午</option>
                  <option value="pm">下午</option>
                  <option value="all">全天</option>
                </select>
              </div>
            </div>
            <div class="price-row">
              <span class="price-label">总价</span>
              <span class="price-val">¥{{ estimatedTotal }}</span>
            </div>
            <div class="price-calc">{{ totalArea }}亩 × ¥{{ currentPrice }}/亩</div>
            <div class="settlement-hint">支付方式: 现结</div>
          </div>

          <button class="btn-submit" @click="submitBooking">⚡ 提交订单</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { farmsApi, ordersApi } from '../api'
import { useToast } from '../composables/useToast'

const route = useRoute()
const router = useRouter()
const { toast } = useToast()
const showBooking = ref(false)
const farmsWithFields = ref([])
const expandedFarms = ref(new Set())
const selectedPlotIds = ref([])
const period = ref(route.params.period || 'month')

const periodTabs = [
  { key: 'month', label: '包月', price: 15 },
  { key: 'quarter', label: '包季', price: 40 },
  { key: 'year', label: '包年', price: 120 },
]

const currentPrice = computed(() => periodTabs.find(t => t.key === period.value)?.price || 15)

const bookingForm = reactive({
  startDate: '',
  period: 'am',
})

const totalArea = computed(() => {
  let area = 0
  farmsWithFields.value.forEach(farm => {
    (farm.fields || []).forEach(f => {
      if (selectedPlotIds.value.includes(farm.id + '-' + f.id)) area += f.area || 0
    })
  })
  return area
})

const estimatedTotal = computed(() => Math.round(totalArea.value * currentPrice.value))

function toggleFarm(id) {
  const s = new Set(expandedFarms.value)
  if (s.has(id)) s.delete(id)
  else s.add(id)
  expandedFarms.value = s
}

onMounted(async () => {
  const p = route.params.period
  if (p && ['month', 'quarter', 'year'].includes(p)) period.value = p
  const { data } = await farmsApi.list()
  farmsWithFields.value = data || []
  if (farmsWithFields.value.length) expandedFarms.value = new Set([farmsWithFields.value[0].id])
  const d = new Date()
  bookingForm.startDate = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
})

function submitBooking() {
  if (selectedPlotIds.value.length === 0) {
    toast('请选择地块')
    return
  }
  const names = farmsWithFields.value.flatMap(f => (f.fields || []).filter(fld => selectedPlotIds.value.includes(f.id + '-' + fld.id)).map(fld => fld.name || '地块')).filter(Boolean)
  const plotNames = names.length ? names.join('、') + `，共${selectedPlotIds.value.length}个地块` : `共${selectedPlotIds.value.length}个地块`
  const startTime = `${bookingForm.startDate} ${bookingForm.period === 'all' ? '全天' : (bookingForm.period === 'am' ? '09:00' : '14:00')}`
  router.push({
    path: '/machinery/remote/confirm',
    state: {
      packageName: `卫星遥感巡田套餐(包${period.value === 'month' ? '月' : period.value === 'quarter' ? '季' : '年'})`,
      provider: '地小丰服务',
      pricePerMu: currentPrice.value,
      totalArea: totalArea.value,
      totalPrice: estimatedTotal.value,
      plotNames,
      plotCount: selectedPlotIds.value.length,
      startTime,
      serviceType: 'remote',
    },
  })
}
</script>

<style scoped>
.remote-package .page-body { padding: 16px; padding-bottom: 32px; }
.hdr-bar { display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: linear-gradient(135deg, #673AB7, #7B1FA2); color: #FFF; }
.hdr-back { width: 36px; height: 36px; border: none; background: rgba(255,255,255,.2); color: #FFF; font-size: 24px; border-radius: 8px; cursor: pointer; }
.hdr-title { font-size: 18px; font-weight: 600; }
.service-banner { padding: 20px 16px; border-radius: 12px; margin-bottom: 16px; color: #FFF; }
.service-banner.purple { background: linear-gradient(135deg, #673AB7, #7B1FA2); }
.banner-title { font-size: 18px; font-weight: 600; margin-bottom: 6px; }
.banner-sub { font-size: 13px; opacity: .9; }
.package-main { margin-bottom: 20px; }
.package-name { font-size: 16px; font-weight: 600; color: #1B2E1B; margin-bottom: 12px; }
.period-tabs { display: flex; gap: 10px; margin-bottom: 10px; }
.period-tab { padding: 8px 16px; border: 1px solid #E0E0E0; background: #FFF; border-radius: 8px; font-size: 13px; cursor: pointer; }
.period-tab.active { background: #673AB7; color: #FFF; border-color: #673AB7; }
.base-price { font-size: 20px; font-weight: 600; color: #673AB7; margin-bottom: 8px; }
.package-tags { display: flex; flex-wrap: wrap; gap: 8px; }
.package-tags .tag { font-size: 12px; padding: 4px 10px; border-radius: 12px; background: rgba(103,58,183,.15); color: #673AB7; }
.info-section { background: #FFF; border-radius: 12px; padding: 16px; margin-bottom: 16px; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.section-title { font-size: 15px; font-weight: 600; color: #1B2E1B; margin-bottom: 12px; }
.content-list { font-size: 14px; color: #666; line-height: 1.8; padding-left: 18px; margin: 0; }
.provider-info { display: flex; gap: 12px; align-items: flex-start; }
.provider-icon { font-size: 24px; }
.provider-name { font-size: 14px; font-weight: 600; color: #333; }
.provider-support { font-size: 13px; color: #666; margin-top: 4px; }
.pricing-rules { font-size: 14px; color: #666; }
.rule-item { padding: 6px 0; }
.rule-note { font-size: 13px; color: #999; margin-top: 10px; }
.bottom-bar { position: fixed; bottom: 0; left: 0; right: 0; padding: 12px 16px; background: #FFF; box-shadow: 0 -2px 8px rgba(0,0,0,.08); display: flex; align-items: center; justify-content: space-between; }
.bottom-name { font-size: 14px; color: #333; }
.btn-book { padding: 12px 24px; background: linear-gradient(135deg, #673AB7, #7B1FA2); color: #FFF; border: none; border-radius: 10px; font-size: 15px; font-weight: 600; cursor: pointer; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.4); z-index: 1000; display: flex; align-items: flex-end; justify-content: center; opacity: 0; visibility: hidden; transition: .3s; }
.modal-overlay.open { opacity: 1; visibility: visible; }
.modal-sheet { background: #FFF; border-radius: 20px 20px 0 0; width: 100%; max-height: 85vh; overflow-y: auto; padding-bottom: env(safe-area-inset-bottom); }
.modal-handle { width: 40px; height: 4px; background: #DDD; border-radius: 2px; margin: 12px auto; }
.modal-hd { padding: 0 16px 12px; }
.modal-title { font-size: 18px; font-weight: 600; }
.modal-banner { padding: 16px; border-radius: 12px; margin: 0 16px 16px; color: #FFF; }
.booking-section { padding: 0 16px 24px; }
.booking-block { margin-bottom: 20px; }
.block-label { font-size: 14px; font-weight: 500; margin-bottom: 10px; }
.farm-group { margin-bottom: 8px; }
.farm-hd { display: flex; justify-content: space-between; padding: 10px 12px; background: #F5F5F5; border-radius: 8px; cursor: pointer; }
.farm-name { font-size: 14px; }
.farm-arrow { font-size: 12px; color: #999; }
.farm-plots { padding: 8px 0 8px 12px; }
.plot-item { display: flex; align-items: center; gap: 8px; padding: 6px 0; font-size: 14px; cursor: pointer; }
.plot-area { margin-left: auto; color: #666; font-size: 12px; }
.plot-summary { font-size: 13px; color: #666; margin-top: 8px; }
.form-row { display: flex; gap: 12px; margin-bottom: 12px; }
.form-group { flex: 1; }
.form-group label { display: block; font-size: 12px; color: #666; margin-bottom: 4px; }
.form-input, .form-select { width: 100%; padding: 10px; border: 1px solid #E0E0E0; border-radius: 8px; font-size: 14px; }
.price-row { display: flex; justify-content: space-between; align-items: center; margin: 12px 0 4px; }
.price-label { font-size: 14px; }
.price-val { font-size: 18px; font-weight: 600; color: #673AB7; }
.price-calc { font-size: 13px; color: #666; }
.settlement-hint { font-size: 13px; color: #666; margin-top: 4px; }
.btn-submit { width: 100%; padding: 14px; background: var(--primary-gradient); color: #FFF; border: none; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; margin-top: 8px; }
</style>
