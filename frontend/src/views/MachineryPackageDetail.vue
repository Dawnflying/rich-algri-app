<template>
  <div class="page package-detail">
    <div class="hdr-title-bar"><button class="hdr-back" @click="$router.back()">‹</button>套餐详情页</div>
    <div class="hdr-banner">
      <span class="hdr-icon">⚡</span>
      <span class="hdr-title">套餐详情</span>
    </div>

    <div class="page-body">
      <div class="service-banner">
        <div class="banner-title">无人机巡田服务</div>
        <div class="banner-sub">专业高效的农田监测解决方案</div>
      </div>

      <div class="service-main">
        <div class="service-name">小麦全生育期巡田服务</div>
        <div class="service-provider">
          <span class="provider-icon">B</span>
          蓝天无人机服务
          <span class="sold">已售128章</span>
        </div>
        <div class="service-tags">
          <span class="tag tag-blue">无人机巡田</span>
          <span class="tag tag-green">作物套路</span>
          <span class="tag tag-yellow">病虫害识别</span>
          <span class="tag tag-purple">专业报告</span>
        </div>
      </div>

      <div class="info-section">
        <div class="section-title">套餐基础信息</div>
        <div class="info-item"><span class="info-label">适用作物/场景</span><div class="info-tags"><span class="crop-tag">小麦</span><span class="crop-tag">玉米</span><span class="crop-tag">水稻</span></div></div>
        <div class="info-item"><span class="info-label">服务范围及套餐说明</span><div class="info-desc">服务区域: 山东区，时间:24小时内。可按季度扣。</div></div>
      </div>

      <div class="info-section">
        <div class="section-title">周期与频次</div>
        <div class="period-tabs">
          <button class="period-tab active">单次作业</button>
          <button class="period-tab">多次作业</button>
        </div>
      </div>

      <div class="info-section">
        <div class="section-title">设备与计价</div>
        <div class="info-item"><span class="info-label">设备提供</span><span>服务商提供设备</span></div>
        <div class="info-item"><span class="info-label">使用机型</span><span>大疆精灵4RTK、极飞P100</span></div>
        <div class="info-item"><span class="info-label">计价方式</span><span class="price-val">¥10/亩</span></div>
      </div>

      <div class="info-section">
        <div class="section-title">期望结算方式</div>
        <p class="settlement-desc">年度结算: 当年12月31日完成付款。支付比例: 线上20%, 其余80%线下结算</p>
      </div>

      <div class="info-section">
        <div class="section-title">服务承诺</div>
        <ul class="promise-list">
          <li>作业质量不达标免费重做</li>
          <li>24小时售后服务</li>
          <li>专业技术团队支持</li>
          <li>详细诊断报告交付</li>
        </ul>
      </div>

      <div style="height: 80px"></div>
    </div>

    <!-- 底部预约栏 -->
    <div class="bottom-bar">
      <span class="bottom-name">小麦全生育期巡田服务</span>
      <button class="btn-book" @click="showBooking = true">⚡ 立即预约</button>
    </div>

    <!-- 预约服务弹窗 -->
    <div class="modal-overlay" :class="{ open: showBooking }" @click.self="showBooking = false">
      <div class="modal-sheet">
        <div class="modal-handle"></div>
        <div class="modal-hd">
          <span class="modal-title">⚡ 套餐详情</span>
        </div>
        <div class="modal-banner">
          <div class="banner-title">无人机巡田服务</div>
          <div class="banner-sub">专业高效的农田监测解决方案</div>
        </div>
        <div class="modal-service">
          <div class="service-name">小麦全生育期巡田服务</div>
          <div class="service-provider">蓝天无人机服务 <span class="sold">已售128章</span></div>
        </div>

        <div class="booking-section">
          <div class="booking-title">⚡ 预约服务</div>

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
            <div class="plot-summary">已选择{{ selectedPlotIds.length }}个地块,总面积:{{ totalArea }}亩</div>
          </div>

          <div class="booking-block">
            <div class="block-label">选择时间与价格</div>
            <div class="form-row">
              <div class="form-group"><label>选择开始时间</label><input v-model="bookingForm.startDate" type="date" class="form-input" /></div>
              <div class="form-group"><label>时段</label><select v-model="bookingForm.period" class="form-select"><option value="am">上午</option><option value="pm">下午</option></select></div>
            </div>
            <div class="price-row">
              <span class="price-label">预估总价</span>
              <span class="price-val">¥{{ estimatedPrice }}</span>
            </div>
            <div class="price-calc">{{ totalArea }}亩 × 15/亩</div>
            <div class="settlement-hint">服务商账期: 年底结算 (12月31日统一付款,平台支付20%,线下支付80%)</div>
          </div>

          <div class="booking-block">
            <div class="block-label">填写您的期望价格(选填)</div>
            <input v-model.number="bookingForm.expectedPrice" type="number" class="form-input" placeholder="请输入您的期望价格" />
          </div>

          <div class="booking-block">
            <div class="block-label">您的期望结算方式</div>
            <label class="radio-item"><input v-model="bookingForm.settlement" type="radio" value="spot" /> 现结: 订单完成后7天内付,平台20%+线下80%</label>
            <label class="radio-item"><input v-model="bookingForm.settlement" type="radio" value="yearend" /> 年底结算: 12月31日付,平台20%+线下80%</label>
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

const bookingForm = reactive({
  startDate: '',
  period: 'am',
  expectedPrice: null,
  settlement: 'yearend',
})

const pricePerMu = 15

const totalArea = computed(() => {
  let area = 0
  farmsWithFields.value.forEach(farm => {
    (farm.fields || []).forEach(f => {
      if (selectedPlotIds.value.includes(farm.id + '-' + f.id)) area += f.area || 0
    })
  })
  return area
})

const estimatedPrice = computed(() => totalArea.value * pricePerMu)

function toggleFarm(id) {
  const s = new Set(expandedFarms.value)
  if (s.has(id)) s.delete(id)
  else s.add(id)
  expandedFarms.value = s
}

onMounted(async () => {
  const { data } = await farmsApi.list()
  farmsWithFields.value = data || []
  if (farmsWithFields.value.length) expandedFarms.value = new Set([farmsWithFields.value[0].id])
  const d = new Date()
  bookingForm.startDate = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
})

async function submitBooking() {
  if (selectedPlotIds.value.length === 0) {
    toast('请选择地块')
    return
  }
  try {
    const packageId = Number(route.params.id) || 1
    const names = farmsWithFields.value.flatMap(f => (f.fields || []).filter(fld => selectedPlotIds.value.includes(f.id + '-' + fld.id)).map(fld => fld.name || '地块')).filter(Boolean)
    const plotNames = names.length ? names.join('、') + `，共${selectedPlotIds.value.length}个地块` : `共${selectedPlotIds.value.length}个地块`
    const { data } = await ordersApi.create({
      packageId,
      packageName: '小麦全生育期巡田服务',
      serviceContent: '无人机·巡田监测套餐',
      provider: '蓝天无人机服务(企业)',
      totalArea: totalArea.value,
      pricePerMu,
      userPrice: bookingForm.expectedPrice || null,
      userSettlement: bookingForm.settlement,
      plotCount: selectedPlotIds.value.length,
      serviceType: 'drone',
      plotNames: plotNames || `共${selectedPlotIds.value.length}个地块`,
      bookingStartTime: `${bookingForm.startDate} ${bookingForm.period === 'am' ? '09:00' : '14:00'}`,
      workRequirements: '农药使用符合规范，覆盖均匀，无漏喷。',
    })
    showBooking.value = false
    toast('订单提交成功 ✓')
    router.push('/machinery/order/' + data.order.id)
  } catch (e) {
    toast(e?.response?.data?.detail || '提交失败')
  }
}
</script>

<style scoped>
.package-detail .page-body { padding: 16px; padding-bottom: 32px; }
.hdr-title-bar { display: flex; align-items: center; gap: 12px; padding: 10px 16px; background: #F5F5F5; font-size: 14px; color: #666; }
.hdr-back { width: 32px; height: 32px; border: none; background: rgba(46,125,50,.1); color: var(--primary); font-size: 22px; border-radius: 8px; cursor: pointer; }
.hdr-banner { display: flex; align-items: center; gap: 10px; padding: 12px 16px; background: linear-gradient(135deg, var(--primary), var(--primary-light)); color: #FFF; }
.hdr-icon { font-size: 16px; }
.hdr-title { font-size: 16px; font-weight: 600; }
.service-banner { padding: 24px 16px; background: linear-gradient(135deg, var(--blue), #9BB8E0); color: #FFF; border-radius: 12px; margin-bottom: 16px; }
.banner-title { font-size: 18px; font-weight: 600; margin-bottom: 8px; }
.banner-sub { font-size: 13px; opacity: .9; }
.service-main { margin-bottom: 20px; }
.service-name { font-size: 16px; font-weight: 600; color: #1B2E1B; margin-bottom: 8px; }
.service-provider { font-size: 14px; color: var(--text2); margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }
.provider-icon { width: 24px; height: 24px; background: var(--blue); color: #FFF; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 600; }
.sold { font-size: 12px; color: #9DB89C; margin-left: auto; }
.service-tags { display: flex; flex-wrap: wrap; gap: 8px; }
.tag { font-size: 12px; padding: 4px 10px; border-radius: 12px; }
.tag-blue { background: var(--blue-dim); color: var(--blue); }
.tag-green { background: var(--primary-dim); color: var(--primary); }
.tag-yellow { background: var(--orange-dim); color: var(--amber); }
.tag-purple { background: rgba(103,58,183,.15); color: #673AB7; }
.info-section { margin-bottom: 20px; padding: 16px; background: #FFF; border: 1px solid rgba(46,125,50,.1); border-radius: 12px; }
.section-title { font-size: 14px; font-weight: 600; color: #1B2E1B; margin-bottom: 12px; }
.info-item { margin-bottom: 10px; }
.info-label { display: block; font-size: 12px; color: var(--text2); margin-bottom: 6px; }
.info-tags { display: flex; gap: 8px; flex-wrap: wrap; }
.crop-tag { font-size: 12px; padding: 4px 12px; background: var(--primary-dim); color: var(--primary); border-radius: 12px; }
.info-desc { font-size: 13px; color: #666; line-height: 1.5; }
.period-tabs { display: flex; gap: 10px; }
.period-tab { padding: 8px 16px; border: 1px solid var(--primary-border); background: #FFF; color: var(--text2); border-radius: 8px; font-size: 13px; cursor: pointer; }
.period-tab.active { background: var(--primary); color: #FFF; border-color: var(--primary); }
.price-val { font-size: 16px; font-weight: 600; color: var(--primary); }
.settlement-desc { font-size: 13px; color: #666; line-height: 1.6; }
.promise-list { margin: 0; padding-left: 20px; font-size: 13px; color: #666; line-height: 2; }
.bottom-bar { position: fixed; bottom: 0; left: 0; right: 0; padding: 12px 16px; background: #FFF; border-top: 1px solid #EEE; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 -2px 10px rgba(0,0,0,.05); }
.bottom-name { font-size: 14px; font-weight: 500; color: #1B2E1B; }
.btn-book { padding: 12px 24px; background: var(--primary); color: #FFF; border: none; border-radius: 10px; font-size: 15px; font-weight: 600; cursor: pointer; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.4); z-index: 100; display: flex; align-items: flex-end; justify-content: center; opacity: 0; pointer-events: none; transition: .2s; }
.modal-overlay.open { opacity: 1; pointer-events: auto; }
.modal-sheet { width: 100%; max-width: 480px; max-height: 90vh; overflow-y: auto; background: #FFF; border-radius: 16px 16px 0 0; padding: 20px; transform: translateY(100%); transition: .2s; }
.modal-overlay.open .modal-sheet { transform: translateY(0); }
.modal-handle { width: 40px; height: 4px; background: #DDD; border-radius: 2px; margin: 0 auto 16px; }
.modal-hd { margin-bottom: 12px; }
.modal-title { font-size: 14px; font-weight: 600; color: #1B2E1B; }
.modal-banner { padding: 16px; background: linear-gradient(135deg, var(--blue), #9BB8E0); color: #FFF; border-radius: 10px; margin-bottom: 12px; }
.modal-service { margin-bottom: 16px; }
.booking-section { padding-top: 8px; }
.booking-title { font-size: 15px; font-weight: 600; color: #1B2E1B; margin-bottom: 14px; }
.booking-block { margin-bottom: 16px; }
.block-label { font-size: 13px; color: var(--text2); margin-bottom: 10px; }
.farm-group { margin-bottom: 10px; border: 1px solid var(--primary-dim); border-radius: 8px; overflow: hidden; }
.farm-hd { padding: 10px 12px; background: #F7FAF7; display: flex; align-items: center; justify-content: space-between; cursor: pointer; }
.farm-name { font-size: 14px; font-weight: 500; color: #1B2E1B; }
.farm-arrow { font-size: 12px; color: var(--primary); }
.farm-plots { padding: 8px 12px; }
.plot-item { display: flex; align-items: center; gap: 10px; padding: 8px 0; cursor: pointer; font-size: 14px; color: #1B2E1B; }
.plot-area { margin-left: auto; font-size: 12px; color: #9DB89C; }
.plot-summary { font-size: 13px; color: var(--primary); margin-top: 8px; font-weight: 500; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.form-group { margin-bottom: 0; }
.form-group label { display: block; font-size: 12px; color: var(--text2); margin-bottom: 4px; }
.form-input, .form-select { width: 100%; padding: 10px 12px; border: 1px solid rgba(46,125,50,.2); border-radius: 8px; font-size: 14px; box-sizing: border-box; }
.price-row { display: flex; align-items: center; justify-content: space-between; margin: 10px 0 4px; }
.price-label { font-size: 13px; color: var(--text2); }
.price-val { font-size: 18px; font-weight: 600; color: var(--primary); }
.price-calc { font-size: 12px; color: #9DB89C; }
.settlement-hint { font-size: 12px; color: #666; margin-top: 8px; line-height: 1.5; }
.radio-item { display: flex; align-items: flex-start; gap: 8px; margin-bottom: 10px; cursor: pointer; font-size: 13px; color: #1B2E1B; }
.btn-submit { width: 100%; padding: 14px; background: var(--primary); color: #FFF; border: none; border-radius: 10px; font-size: 16px; font-weight: 600; cursor: pointer; margin-top: 8px; }
</style>
