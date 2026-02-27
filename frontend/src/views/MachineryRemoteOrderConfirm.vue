<template>
  <div class="page order-confirm">
    <div class="hdr-bar">
      <button class="hdr-back" @click="$router.back()">‹</button>
      <span class="hdr-title">下单确认</span>
    </div>

    <div class="page-body" v-if="form">
      <div class="info-section">
        <div class="section-title">套餐信息</div>
        <div class="info-item">
          <span class="info-label">套餐名称</span>
          <span>{{ form.packageName }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">服务商</span>
          <span>{{ form.provider }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">单价</span>
          <span>¥{{ form.pricePerMu }}/亩</span>
        </div>
      </div>

      <div class="info-section">
        <div class="section-title">所选地块</div>
        <div class="plot-summary">
          <span>{{ form.plotNames || '棉花地块1' }}</span>
          <span class="plot-area">面积: {{ form.totalArea }}亩</span>
        </div>
        <button class="btn-modify" @click="$router.back()">修改</button>
      </div>

      <div class="info-section">
        <div class="section-title">服务时间</div>
        <div class="time-row">
          <span>预计开始: {{ form.startTime }}</span>
          <button class="btn-modify" @click="$router.back()">修改</button>
        </div>
      </div>

      <div class="info-section">
        <div class="section-title">联系人信息</div>
        <div class="info-item"><span class="info-label">联系人</span><span>张先生</span></div>
        <div class="info-item"><span class="info-label">联系电话</span><span>138****1234</span></div>
        <div class="info-item"><span class="info-label">联系地址</span><span>石河子市</span></div>
        <button class="btn-modify" @click="toast('修改联系人信息')">修改联系人信息</button>
      </div>

      <div class="info-section">
        <div class="section-title">支付方式</div>
        <div class="pay-methods">
          <label class="pay-option">
            <input v-model="payMethod" type="radio" value="alipay" />
            <span>支付宝</span>
          </label>
          <label class="pay-option">
            <input v-model="payMethod" type="radio" value="wechat" />
            <span>微信支付</span>
          </label>
        </div>
      </div>

      <div class="info-section">
        <div class="section-title">价格明细</div>
        <div class="price-detail">
          <div class="price-row">套餐费用: {{ form.totalArea }}亩 × ¥{{ form.pricePerMu }}/亩 = ¥{{ form.totalPrice }}</div>
          <div class="price-row">服务费用: ¥0</div>
          <div class="price-row total">总计: ¥{{ form.totalPrice }}</div>
        </div>
      </div>

      <div style="height: 120px"></div>
    </div>

    <div class="bottom-bar">
      <span class="total-text">总计: ¥{{ form?.totalPrice || 0 }}</span>
      <button class="btn-submit" @click="submitOrder">提交订单</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ordersApi } from '../api'
import { useToast } from '../composables/useToast'

const router = useRouter()
const { toast } = useToast()
const form = ref(null)
const payMethod = ref('alipay')

onMounted(() => {
  const state = history.state
  if (state && state.packageName) {
    form.value = { ...state }
  } else {
    const saved = sessionStorage.getItem('remoteOrderForm')
    if (saved) {
      form.value = JSON.parse(saved)
    } else {
      form.value = {
        packageName: '卫星遥感巡田套餐(包月)',
        provider: '地小丰服务',
        pricePerMu: 8,
        totalArea: 50,
        totalPrice: 400,
        plotNames: '棉花地块1',
        plotCount: 1,
        startTime: '2026-06-16 全天',
        serviceType: 'remote',
      }
    }
  }
  if (form.value) sessionStorage.setItem('remoteOrderForm', JSON.stringify(form.value))
})

async function submitOrder() {
  if (!form.value) return
  try {
    const { data } = await ordersApi.create({
      packageId: 0,
      packageName: form.value.packageName,
      serviceContent: form.value.packageName,
      provider: form.value.provider,
      totalArea: form.value.totalArea,
      pricePerMu: form.value.pricePerMu,
      userPrice: null,
      userSettlement: 'spot',
      plotCount: form.value.plotCount || 1,
      serviceType: 'remote',
      plotNames: form.value.plotNames,
      bookingStartTime: form.value.startTime,
      workRequirements: '遥感监测，长势分析报告。',
    })
    sessionStorage.removeItem('remoteOrderForm')
    toast('订单提交成功 ✓')
    router.push('/machinery/order/' + data.order.id)
  } catch (e) {
    toast(e?.response?.data?.detail || '提交失败')
  }
}
</script>

<style scoped>
.order-confirm .page-body { padding: 16px; }
.hdr-bar { display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: linear-gradient(135deg, var(--primary), var(--primary-light)); color: #FFF; }
.hdr-back { width: 36px; height: 36px; border: none; background: rgba(255,255,255,.2); color: #FFF; font-size: 24px; border-radius: 8px; cursor: pointer; }
.hdr-title { font-size: 18px; font-weight: 600; }
.info-section { background: #FFF; border-radius: 12px; padding: 16px; margin-bottom: 16px; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.section-title { font-size: 15px; font-weight: 600; color: #1B2E1B; margin-bottom: 12px; }
.info-item { display: flex; justify-content: space-between; padding: 8px 0; font-size: 14px; }
.info-label { color: #666; }
.plot-summary { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; }
.plot-area { font-size: 13px; color: #666; }
.time-row { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; }
.btn-modify { margin-top: 8px; padding: 8px 16px; background: #FFF; color: var(--primary); border: 1px solid var(--primary); border-radius: 8px; font-size: 13px; cursor: pointer; }
.pay-methods { display: flex; flex-direction: column; gap: 12px; }
.pay-option { display: flex; align-items: center; gap: 10px; font-size: 14px; cursor: pointer; }
.pay-option input { accent-color: var(--primary); }
.price-detail { font-size: 14px; }
.price-row { padding: 6px 0; }
.price-row.total { font-size: 16px; font-weight: 600; color: var(--primary); }
.bottom-bar { position: fixed; bottom: 0; left: 0; right: 0; padding: 12px 16px; background: #FFF; box-shadow: 0 -2px 8px rgba(0,0,0,.08); display: flex; align-items: center; justify-content: space-between; }
.total-text { font-size: 16px; font-weight: 600; }
.btn-submit { padding: 14px 28px; background: linear-gradient(135deg, var(--primary), var(--primary-light)); color: #FFF; border: none; border-radius: 12px; font-size: 15px; font-weight: 600; cursor: pointer; }
</style>
