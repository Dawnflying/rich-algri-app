<template>
  <div class="page">
    <div class="hdr" style="background:var(--primary);border-bottom:none"><button class="hdr-back" @click="$router.back()" style="color:#FFF;background:rgba(255,255,255,.15)">‹</button><div class="hdr-title" style="color:#FFF">我的钱包</div></div>
    <div class="page-body">
      <div class="wallet-hero">
        <div class="wallet-balance-label">账户总余额（元）</div>
        <div class="wallet-balance-amt">{{ balance }}</div>
        <button class="btn btn-orange" style="height:42px;padding:0 32px;border-radius:10px;font-size:15px;font-weight:600" @click="$router.push('/withdraw')">提 现</button>
      </div>
      <div style="padding:0 16px;margin-top:18px">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px"><span style="font-size:13px;font-weight:600">收支明细</span></div>
        <div class="card">
          <div v-for="tx in transactions.slice(0,3)" :key="tx.id" class="tx-item">
            <div class="tx-icon" :style="{background:tx.amt>0?'rgba(46,125,50,.1)':'rgba(255,111,0,.1)'}">{{ tx.amt>0?'📈':'💸' }}</div>
            <div style="flex:1"><div style="font-size:14px;font-weight:500">{{ tx.label }}</div><div style="font-size:11px;color:#9DB89C">{{ tx.time }}</div></div>
            <div style="font-family:var(--mono);font-size:16px;font-weight:600" :style="{color:tx.amt>0?'var(--primary)':'var(--text)'}">{{ tx.amt>0?'+':'' }} ¥{{ Math.abs(tx.amt).toFixed(2) }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { walletApi } from '../api'

const balance = ref('0.00')
const transactions = ref([])

onMounted(async () => {
  const { data } = await walletApi.get()
  balance.value = data.balance.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
  transactions.value = data.transactions || []
})
</script>
