<template>
  <div class="page">
    <div class="hdr"><button class="hdr-back" @click="$router.back()">‹</button><div class="hdr-title">消息 · 预警 · 待办</div><button class="hdr-action" style="font-size:12px;color:var(--primary)" @click="markAllRead">全读</button></div>
    <div class="page-body">
      <div style="padding:12px 16px 0;display:flex;gap:8px">
        <div v-for="f in ['all','warn','todo','msg']" :key="f" class="chip" :class="{ active: filter === f }" @click="filter = f; loadAlerts()">{{ {all:'全部',warn:'预警',todo:'待办',msg:'消息'}[f] }}</div>
      </div>
      <div class="sec">
        <div v-for="a in alerts" :key="a.id" class="alert-item" style="background:#FFF;border:1px solid rgba(46,125,50,.09);border-left:3px solid" :style="{borderLeftColor:a.level==='red'?'#B87A7A':a.level==='amber'?'#C99A6C':'#7BA3D4',opacity:a.read?'0.65':'1'}" @click="readAlert(a)">
          <div style="font-size:24px">{{ a.icon }}</div>
          <div style="flex:1"><div style="font-size:14px;font-weight:600">{{ a.title }}</div><div style="font-size:12px;color:var(--text2);margin-top:3px">{{ a.desc }}</div><div style="font-size:11px;color:var(--text3);margin-top:5px">{{ a.time }}</div></div>
          <span :class="['badge',a.level==='red'?'badge-red':a.level==='amber'?'badge-amber':'badge-blue']">{{ a.type==='warn'?'预警':a.type==='todo'?'待办':'消息' }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { alertsApi } from '../api'
import { useToast } from '../composables/useToast'

const router = useRouter()
const { toast } = useToast()
const alerts = ref([])
const filter = ref('all')

async function loadAlerts() {
  const { data } = await alertsApi.list(filter.value)
  alerts.value = data
}

async function readAlert(a) {
  await alertsApi.read(a.id)
  a.read = true
  toast('已标记为已读')
}

async function markAllRead() {
  await alertsApi.readAll()
  alerts.value.forEach(a => a.read = true)
  toast('全部已读')
}

onMounted(() => loadAlerts())
</script>
