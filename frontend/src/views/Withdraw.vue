<template>
  <div class="page">
    <div class="hdr"><button class="hdr-back" @click="$router.back()">‹</button><div class="hdr-title">提现</div></div>
    <div class="page-body">
      <div style="background:linear-gradient(145deg,#E8F5E9,#F1F8E9);padding:18px 20px;margin:14px 16px 0;border-radius:14px;border:1px solid rgba(46,125,50,.12)">
        <div style="font-size:12px;color:#5A7A5A">可提现余额</div>
        <div style="font-family:var(--mono);font-size:28px;font-weight:700;color:#1B5E20;margin-top:4px">¥{{ balance }}</div>
      </div>
      <div style="margin:14px 16px 0;background:#FFF;border-radius:14px;padding:18px 20px">
        <div style="font-size:13px;font-weight:600;color:#5A7A5A;margin-bottom:14px">提现金额</div>
        <div style="display:flex;align-items:center;gap:8px;border-bottom:2px solid rgba(46,125,50,.15);padding-bottom:12px">
          <span style="font-size:24px;color:#9DB89C">¥</span>
          <input v-model="amount" type="number" placeholder="0.00" min="0.01" step="0.01" style="flex:1;font-size:24px;font-weight:600;border:none;outline:none" />
          <button @click="amount = balance" style="padding:6px 12px;background:var(--orange-dim);color:#FF6F00;border-radius:8px;font-size:12px;font-weight:600;border:none;cursor:pointer">全部提现</button>
        </div>
      </div>
      <div style="position:fixed;bottom:0;left:0;right:0;padding:12px 16px 32px;background:#FFF;border-top:1px solid rgba(46,125,50,.1)">
        <button class="btn btn-orange btn-full" style="height:48px;font-size:16px;font-weight:600;border-radius:12px" @click="submit">确认提现</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { walletApi } from '../api'
import { useToast } from '../composables/useToast'

const router = useRouter()
const { toast } = useToast()
const balance = ref('0.00')
const amount = ref('')
const accounts = ref([])
const selectedAcctId = ref(null)

onMounted(async () => {
  const { data } = await walletApi.get()
  balance.value = data.balance.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
  accounts.value = data.accounts || []
  if (accounts.value.length) selectedAcctId.value = accounts.value[0].id
})

async function submit() {
  const amt = parseFloat(amount.value)
  if (!amt || amt <= 0) { toast('请输入提现金额'); return }
  const bal = parseFloat(balance.value.replace(/,/g, ''))
  if (amt > bal) { toast('余额不足'); return }
  if (!accounts.value.length) { toast('请先绑定收款账户'); return }
  if (!selectedAcctId.value) { toast('请选择收款账户'); return }
  const { data } = await walletApi.withdraw(amt, selectedAcctId.value)
  if (data.success) {
    toast('提现申请已提交')
    router.push('/wallet')
  }
}
</script>
