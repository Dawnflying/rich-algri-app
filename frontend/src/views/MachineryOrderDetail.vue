<template>
  <div class="page order-detail">
    <div class="hdr-bar">
      <button class="hdr-back" @click="$router.back()">‹</button>
      <span class="hdr-title">订单详情</span>
      <span v-if="order?.status === 'pending_confirm'" class="hdr-badge">新</span>
    </div>

    <div class="page-body" v-if="order">
      <div class="order-status-row">
        <span class="status-tag" :class="order.status">{{ order.statusText }}</span>
        <button v-if="order.status === 'pending_quote'" class="btn-simulate" @click.stop="simulateNewQuote">模拟新报价</button>
        <button v-else-if="order.status === 'pending_payment'" class="btn-simulate" @click.stop="simulateStatus('in_progress')">模拟作业中</button>
        <button v-else-if="order.status === 'in_progress'" class="btn-simulate" @click.stop="simulateStatus('pending_acceptance')">模拟待验收</button>
      </div>

      <!-- 待验收/已完成：简化订单信息 -->
      <div v-if="order.status === 'pending_acceptance' || order.status === 'completed'" class="info-section">
        <div class="section-title service-title">{{ order.serviceContent }}</div>
        <div v-if="order.status === 'completed'" class="provider-row">服务商: {{ order.provider }}</div>
        <div class="info-item"><span class="info-label">订单号</span><span>{{ order.orderNo }}</span></div>
        <div class="info-item"><span class="info-label">服务类型</span><span>{{ serviceTypeText(order.serviceType) }}</span></div>
        <div v-if="order.status === 'completed'" class="info-item"><span class="info-label">服务商电话</span><span class="link-phone">{{ order.providerPhone }}</span></div>
        <div class="info-item"><span class="info-label">下单时间</span><span>{{ order.orderTime }}</span></div>
        <div class="info-item"><span class="info-label">预约开始时间</span><span>{{ order.bookingStartTime }}</span></div>
        <div class="info-item"><span class="info-label">服务地块</span><span>{{ order.plotNames }}</span></div>
        <div class="info-item"><span class="info-label">结算方式</span><span>{{ settlementText(order.userSettlement || order.providerSettlement) }}</span></div>
      </div>

      <!-- 其他状态：完整订单信息 -->
      <div v-else class="info-section">
        <div class="section-title">订单信息</div>
        <div class="info-item"><span class="info-label">服务名称</span><span>{{ order.serviceContent }}</span></div>
        <div class="info-item"><span class="info-label">订单号</span><span>{{ order.orderNo }}</span></div>
        <div class="info-item"><span class="info-label">服务类型</span><span>{{ serviceTypeText(order.serviceType) }}</span></div>
        <div class="info-item"><span class="info-label">服务商</span><span>{{ order.provider }}</span></div>
        <div class="info-item"><span class="info-label">服务商电话</span><span>{{ order.providerPhone }}</span></div>
        <div class="info-item"><span class="info-label">下单时间</span><span>{{ order.orderTime }}</span></div>
        <div class="info-item"><span class="info-label">预约开始时间</span><span>{{ order.bookingStartTime }}</span></div>
        <div class="info-item"><span class="info-label">服务地块</span><span>{{ order.plotNames }}</span></div>
        <div class="info-item"><span class="info-label">结算方式</span><span>{{ settlementText(order.userSettlement || order.providerSettlement) }}</span></div>
      </div>

      <!-- 待验收：作业完成信息 -->
      <div v-if="order.status === 'pending_acceptance'" class="info-section">
        <div class="section-title">作业完成信息</div>
        <div class="info-item"><span class="info-label">作业完成时间</span><span>{{ order.workCompleteTime }}</span></div>
        <div class="info-item"><span class="info-label">总作业时长</span><span>{{ order.totalWorkDuration }}</span></div>
        <div class="info-item"><span class="info-label">实际作业面积</span><span>{{ order.actualArea }}亩</span></div>
      </div>

      <!-- 待验收：报告信息 -->
      <div v-if="order.status === 'pending_acceptance'" class="info-section">
        <div class="section-title">报告信息</div>
        <div class="report-summary">{{ order.reportSummary }}</div>
        <button class="btn-report" @click="$router.push('/machinery/order/' + order.id + '/trace')">查看报告</button>
      </div>

      <!-- 已完成：完成时间线 -->
      <div v-if="order.status === 'completed'" class="info-section">
        <div class="section-title">完成时间线</div>
        <div class="completion-timeline">
          <div v-for="(t, i) in (order.completionTimeline || [])" :key="i" class="timeline-node">
            <span class="timeline-dot"></span>
            <span class="timeline-label">{{ t.label }}:</span>
            <span class="timeline-value">{{ t.value }}</span>
          </div>
        </div>
      </div>

      <!-- 已完成：支付提醒 -->
      <div v-if="order.status === 'completed' && order.paymentReminder" class="info-section payment-reminder">
        <div class="reminder-text">{{ order.paymentReminder }}</div>
      </div>

      <!-- 已完成：报告信息 -->
      <div v-if="order.status === 'completed'" class="info-section">
        <div class="section-title">报告信息</div>
        <div class="info-item"><span class="info-label">报告名称</span><span>{{ order.reportName }}</span></div>
        <div class="info-item"><span class="info-label">生成时间</span><span>{{ order.reportGenTime }}</span></div>
        <button class="btn-report outline" @click="$router.push('/machinery/order/' + order.id + '/trace')">⚡ 查看报告</button>
      </div>

      <!-- 价格信息（非待验收/已完成时显示） -->
      <div v-if="order.status !== 'pending_acceptance' && order.status !== 'completed'" class="info-section">
        <div class="section-title">价格信息</div>
        <div class="info-item"><span class="info-label">套餐单价</span><span>¥{{ order.pricePerMu }}/亩</span></div>
        <div class="info-item"><span class="info-label">总面积</span><span>{{ order.totalArea }}亩</span></div>
        <div class="info-item"><span class="info-label">总价</span><span>¥{{ formatPrice(order.finalPrice) }}</span></div>
        <div class="info-item"><span class="info-label">平台服务费</span><span>¥{{ formatPrice(order.platformFee) }}</span></div>
        <div class="info-item"><span class="info-label">最终应付</span><span class="price-val">¥{{ formatPrice(order.finalPrice) }}</span></div>
      </div>

      <!-- 待确认：价格协商区 -->
      <div v-if="order.status === 'pending_confirm'" class="info-section">
        <div class="section-title">价格协商</div>
        <div class="bargain-row">
          <span class="bargain-label">农户期望</span>
          <span>期望价格 ¥{{ order.userPricePerMu || order.userPrice }}/亩，期望结算方式 {{ settlementText(order.userSettlement) }}</span>
        </div>
        <div class="bargain-row highlight">
          <span class="bargain-label">服务商报价</span>
          <span>报价 ¥{{ order.providerPricePerMu || order.providerPrice }}/亩，结算方式 {{ settlementText(order.providerSettlement) }}</span>
        </div>
        <div class="info-item"><span class="info-label">平台服务费</span><span>¥{{ formatPrice(order.platformFee) }}</span></div>
        <div class="info-item"><span class="info-label">最终应付金额</span><span class="price-val">¥{{ formatPrice(order.onlinePayAmount || order.finalPrice) }}</span></div>
        <div v-if="order.providerMessage" class="provider-msg">
          <span class="msg-icon">💬</span>
          {{ order.providerMessage }}
        </div>
      </div>

      <!-- 待付款：支付信息 -->
      <div v-if="order.status === 'pending_payment'" class="info-section">
        <div class="section-title">支付信息</div>
        <div class="pay-row">
          <span>应付总额(线上20%)</span>
          <span class="price-val">¥{{ formatPrice(order.onlinePayAmount) }}</span>
        </div>
        <div class="pay-desc">请在7天内完成线上支付，剩余80%线下结算</div>
        <div class="countdown-row">
          <span>剩余时间:</span>
          <span class="countdown">{{ order.countdown || '6天 23小时 45分' }}</span>
        </div>
      </div>

      <!-- 作业要求（非待验收/已完成时显示） -->
      <div v-if="order.status !== 'pending_acceptance' && order.status !== 'completed'" class="info-section">
        <div class="section-title">作业要求</div>
        <div class="work-requirements">{{ order.workRequirements }}</div>
      </div>

      <!-- 作业中：执行人员、进度、时间线、查看报告入口 -->
      <template v-if="order.status === 'in_progress'">
        <div class="info-section">
          <button class="btn-report" @click="$router.push('/machinery/order/' + order.id + '/trace')">查看报告</button>
        </div>
        <div class="info-section">
          <div class="section-title">执行人员</div>
          <div class="executor-row">
            <span class="info-label">姓名</span><span>{{ order.executorName }}</span>
          </div>
          <div class="executor-row">
            <span class="info-label">联系电话</span><span>{{ order.executorPhone }}</span>
          </div>
          <div class="executor-row">
            <span class="info-label">实时位置</span><span>{{ order.executorLocation }}</span>
          </div>
        </div>
        <div class="info-section">
          <div class="section-title">作业概览</div>
          <div class="progress-bar-wrap">
            <div class="progress-bar" :style="{ width: progressPercent + '%' }"></div>
            <span class="progress-text">{{ order.progressCurrent || 0 }}/{{ order.progressTotal || 0 }}</span>
          </div>
          <div class="progress-meta">
            <span>已作业时长: {{ order.elapsedTime }}</span>
            <span>预计剩余时间: {{ order.remainingTime }}</span>
          </div>
        </div>
        <div v-if="order.plotProgress?.length" class="info-section">
          <div class="section-title">地块进度</div>
          <div v-for="p in order.plotProgress" :key="p.name" class="plot-progress-item">
            <span>{{ p.name }}</span>
            <span v-if="p.status === 'completed'" class="plot-done">已完成</span>
            <span v-else class="plot-progress">作业中 [{{ p.percent || 0 }}%]</span>
          </div>
        </div>
        <div v-if="order.timeline?.length" class="info-section">
          <div class="section-title">作业时间线</div>
          <div class="timeline">
            <div v-for="(t, i) in order.timeline" :key="i" class="timeline-item">
              <span class="timeline-time">{{ t.time }}</span>
              <span class="timeline-event">{{ t.event }}</span>
            </div>
          </div>
        </div>
      </template>

      <div style="height: 120px"></div>
    </div>

    <!-- 底部操作 -->
    <div class="bottom-actions" v-if="order && order.status !== 'cancelled'">
      <template v-if="order.status === 'completed'">
        <button class="btn-secondary" @click="$router.push('/')">返回首页</button>
        <button class="btn-primary" @click="$router.push('/machinery')">⚡ 再次预约</button>
      </template>
      <template v-else-if="order.status === 'pending_quote'">
        <button class="btn-danger" @click="cancelOrder">取消订单</button>
      </template>
      <template v-else-if="order.status === 'pending_confirm'">
        <button class="btn-primary" @click="acceptOrder">接受并下单</button>
        <button class="btn-secondary" @click="rejectQuote">拒绝并重新协商</button>
        <button class="btn-danger" @click="cancelOrder">取消订单</button>
      </template>
      <template v-else-if="order.status === 'pending_payment'">
        <button class="btn-primary" @click="payOrder">立即支付</button>
        <button class="btn-danger" @click="cancelOrder">取消订单</button>
      </template>
      <template v-else-if="order.status === 'pending_acceptance'">
        <button class="btn-primary btn-full" @click="confirmComplete">确认完成</button>
      </template>
      <template v-else-if="order.status === 'in_progress'">
        <button class="btn-danger" @click="cancelOrder">取消订单</button>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ordersApi } from '../api'
import { useToast } from '../composables/useToast'

const route = useRoute()
const router = useRouter()
const { toast } = useToast()
const order = ref(null)

const progressPercent = computed(() => {
  const o = order.value
  if (!o?.progressTotal) return 0
  return Math.round(((o.progressCurrent || 0) / o.progressTotal) * 100)
})

function formatPrice(v) {
  if (v == null) return '0.00'
  return Number(v).toFixed(2)
}

function settlementText(v) {
  const map = { spot: '现结', yearend: '年底结算' }
  return map[v] || v || '—'
}

function serviceTypeText(v) {
  const map = { drone: '无人机植保', remote: '遥感', other: '农机收割/插秧' }
  return map[v] || v || '—'
}

onMounted(async () => {
  const id = Number(route.params.id)
  if (!id) return
  try {
    const { data } = await ordersApi.get(id)
    order.value = data
  } catch (e) {
    toast('订单不存在')
    router.back()
  }
})

async function simulateNewQuote() {
  try {
    const { data } = await ordersApi.newQuote(order.value.id, {
      price: order.value.totalArea * 45,
      pricePerMu: 45,
      settlement: 'spot',
      message: '您好, 这是基于面积的核算价, 考虑了飞手成本和设备损耗, 供您参考。',
    })
    order.value = data.order
    toast('已模拟收到新报价')
  } catch (e) {
    toast(e?.response?.data?.detail || '操作失败')
  }
}

async function simulateStatus(target) {
  try {
    const { data } = await ordersApi.simulateStatus(order.value.id, target)
    order.value = data.order
    toast('状态已更新')
  } catch (e) {
    toast(e?.response?.data?.detail || '操作失败')
  }
}

async function acceptOrder() {
  try {
    const { data } = await ordersApi.accept(order.value.id)
    order.value = data.order
    toast('已接受报价')
  } catch (e) {
    toast(e?.response?.data?.detail || '操作失败')
  }
}

async function payOrder() {
  try {
    const { data } = await ordersApi.pay(order.value.id)
    order.value = data.order
    toast('支付成功')
  } catch (e) {
    toast(e?.response?.data?.detail || '操作失败')
  }
}

async function confirmComplete() {
  try {
    const { data } = await ordersApi.confirmComplete(order.value.id)
    order.value = data.order
    toast('已确认完成')
  } catch (e) {
    toast(e?.response?.data?.detail || '操作失败')
  }
}

async function rejectQuote() {
  toast('已拒绝，请与服务商协商')
}

async function cancelOrder() {
  try {
    await ordersApi.cancel(order.value.id)
    order.value.status = 'cancelled'
    order.value.statusText = '已取消'
    toast('订单已取消')
  } catch (e) {
    toast(e?.response?.data?.detail || '操作失败')
  }
}
</script>

<style scoped>
.order-detail .page-body { padding: 16px; padding-bottom: 32px; }
.hdr-bar { display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: var(--primary-gradient); color: #FFF; }
.hdr-back { width: 36px; height: 36px; border: none; background: rgba(255,255,255,.2); color: #FFF; font-size: 24px; border-radius: 8px; cursor: pointer; }
.hdr-title { font-size: 18px; font-weight: 600; flex: 1; }
.hdr-badge { background: #E53935; color: #FFF; font-size: 11px; padding: 2px 6px; border-radius: 8px; }
.order-status-row { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; padding: 12px 16px; background: #F5F5F5; border-radius: 12px; margin-bottom: 16px; }
.btn-simulate { font-size: 12px; padding: 4px 10px; background: #F3E5F5; color: #7B1FA2; border: none; border-radius: 6px; cursor: pointer; }
.status-tag { font-size: 13px; padding: 4px 12px; border-radius: 8px; }
.status-tag.pending_quote { background: var(--orange-dim); color: var(--amber); }
.status-tag.pending_confirm { background: var(--blue-dim); color: var(--blue); }
.status-tag.pending_payment { background: var(--red-dim); color: var(--red); }
.status-tag.in_progress { background: var(--primary-dim); color: var(--primary); }
.status-tag.pending_acceptance { background: var(--blue-dim); color: var(--blue); }
.status-tag.completed { background: var(--primary-dim); color: var(--primary); }
.status-tag.cancelled { background: #F5F5F5; color: #999; }
.service-title { font-size: 16px; font-weight: 600; color: #1B2E1B; margin-bottom: 8px; }
.provider-row { font-size: 14px; color: #666; margin-bottom: 12px; }
.link-phone { color: var(--blue); }
.report-summary { font-size: 14px; color: #333; line-height: 1.6; margin-bottom: 12px; }
.btn-report { width: 100%; padding: 12px; background: var(--primary-dim); color: var(--primary); border: 1px solid var(--primary); border-radius: 8px; font-size: 14px; cursor: pointer; }
.btn-report.outline { background: #FFF; }
.completion-timeline { font-size: 14px; }
.timeline-node { display: flex; align-items: center; gap: 8px; padding: 8px 0; }
.timeline-dot { width: 8px; height: 8px; background: var(--primary); border-radius: 50%; flex-shrink: 0; }
.timeline-label { color: #666; }
.timeline-value { color: #333; }
.payment-reminder { background: #FFEBEE !important; }
.reminder-text { font-size: 14px; color: var(--red); }
.btn-full { flex: 1 1 100%; }
.info-section { background: #FFF; border-radius: 12px; padding: 16px; margin-bottom: 16px; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.section-title { font-size: 15px; font-weight: 600; color: #1B2E1B; margin-bottom: 12px; }
.info-item { display: flex; justify-content: space-between; padding: 8px 0; font-size: 14px; }
.info-label { color: #666; }
.price-val { font-size: 16px; font-weight: 600; color: var(--primary); }
.bargain-row { padding: 10px 0; font-size: 14px; }
.bargain-row.highlight { color: var(--primary); font-weight: 600; }
.bargain-label { color: #666; margin-right: 8px; }
.provider-msg { display: flex; align-items: flex-start; gap: 8px; padding: 12px; background: var(--primary-dim); border-radius: 8px; margin-top: 10px; font-size: 14px; color: #1B5E20; }
.msg-icon { font-size: 16px; }
.pay-row { display: flex; justify-content: space-between; padding: 12px 0; }
.pay-desc { font-size: 13px; color: #666; margin-bottom: 12px; }
.countdown-row { font-size: 14px; }
.countdown { color: var(--amber); font-weight: 600; margin-left: 8px; }
.work-requirements { font-size: 14px; color: #333; line-height: 1.6; }
.executor-row { display: flex; justify-content: space-between; padding: 8px 0; font-size: 14px; }
.progress-bar-wrap { position: relative; height: 24px; background: #E0E0E0; border-radius: 12px; overflow: hidden; margin-bottom: 10px; }
.progress-bar { height: 100%; background: var(--primary-gradient); transition: width .3s; }
.progress-text { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); font-size: 12px; font-weight: 600; color: #FFF; text-shadow: 0 1px 2px rgba(0,0,0,.3); }
.progress-meta { font-size: 13px; color: #666; }
.plot-progress-item { display: flex; justify-content: space-between; padding: 8px 0; font-size: 14px; }
.plot-done { color: var(--primary); }
.plot-progress { color: var(--blue); }
.timeline { font-size: 14px; }
.timeline-item { display: flex; gap: 12px; padding: 8px 0; }
.timeline-time { color: #666; min-width: 140px; }
.timeline-event { color: #333; }
.bottom-actions { position: fixed; bottom: 0; left: 0; right: 0; padding: 12px 16px; background: #FFF; box-shadow: 0 -2px 8px rgba(0,0,0,.08); display: flex; flex-wrap: wrap; gap: 10px; }
.btn-primary { flex: 1; min-width: 120px; padding: 14px 20px; background: var(--primary-gradient); color: #FFF; border: none; border-radius: 12px; font-size: 15px; font-weight: 600; cursor: pointer; }
.btn-secondary { flex: 1; min-width: 100px; padding: 14px 16px; background: #F5F5F5; color: #666; border: none; border-radius: 12px; font-size: 14px; cursor: pointer; }
.btn-danger { flex: 1; min-width: 100px; padding: 14px 16px; background: #FFF; color: var(--red); border: 1px solid var(--red); border-radius: 12px; font-size: 14px; cursor: pointer; }
</style>
