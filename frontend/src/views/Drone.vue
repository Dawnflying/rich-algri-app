<template>
  <div class="page">
    <div class="hdr"><div class="hdr-title">M3M 无人机任务</div><button class="hdr-action" @click="showCreateTask">➕</button></div>
    <div class="page-body">
      <div style="padding:12px 16px 0">
        <div class="card card-p">
          <div style="display:flex;align-items:center;gap:12px">
            <div style="font-size:40px">🚁</div>
            <div style="flex:1">
              <div style="font-size:15px;font-weight:600">Mavic 3 Multispectral</div>
              <div style="font-size:12px;color:var(--text2);margin-top:2px">SN: DJI-M3M-A8F2C1</div>
              <span class="badge badge-green">● 已连接</span>
            </div>
            <div style="text-align:right"><div style="font-family:var(--mono);font-size:24px;font-weight:500;color:var(--primary)">82%</div><div style="font-size:11px;color:var(--text2)">电量</div></div>
          </div>
        </div>
      </div>
      <div style="padding:14px 16px 0;display:flex;gap:8px">
        <div v-for="f in ['all','flying','pending','done']" :key="f" class="chip" :class="{ active: taskFilter === f }" @click="taskFilter = f; loadTasks()">{{ {all:'全部',flying:'飞行中',pending:'待执行',done:'已完成'}[f] }}</div>
      </div>
      <div class="sec">
        <div class="card">
          <div v-for="t in tasks" :key="t.id" class="list-row" @click="openTask(t)">
            <div class="list-icon" :style="{background:t.status==='flying'?'var(--blue-dim)':t.status==='done'?'var(--green-dim)':'var(--card2)'}">{{ t.status==='flying'?'🚁':t.status==='done'?'✅':'⏳' }}</div>
            <div class="list-body"><div class="list-title">{{ t.field }}</div><div class="list-sub">{{ t.type }} · {{ t.area }}亩</div><div v-if="t.status==='flying'" class="prog-wrap" style="margin-top:5px"><div class="prog-fill" :style="{width:t.progress+'%'}"></div></div></div>
            <div class="list-right"><span :class="['badge',t.status==='flying'?'badge-blue':t.status==='done'?'badge-green':'badge-amber']">{{ t.status==='flying'?'飞行中':t.status==='done'?'已完成':'待执行' }}</span></div>
          </div>
          <div v-if="!tasks.length" style="padding:30px;text-align:center;color:#9DB89C">暂无任务</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { droneApi, fieldsApi } from '../api'
import { useToast } from '../composables/useToast'

const router = useRouter()
const { toast } = useToast()
const tasks = ref([])
const fields = ref([])
const taskFilter = ref('all')

async function loadTasks() {
  const { data } = await droneApi.listTasks(taskFilter.value)
  tasks.value = data
}

function openTask(t) {
  if (t.status === 'flying') router.push('/tracking')
  else toast(t.status === 'done' ? '查看飞行报告' : '任务尚未开始')
}

function showCreateTask() {
  toast('创建任务功能')
}

onMounted(() => loadTasks())
</script>
