<template>
  <div class="page irrigation-list">
    <div class="hdr-bar">
      <button class="hdr-back" @click="$router.back()">‹</button>
      <span class="hdr-title">⚡ 灌溉任务</span>
      <button class="hdr-flow" @click="toast('流量数据')">
        <span class="flow-icon">📈</span>
        <span v-if="flowBadge" class="flow-badge">{{ flowBadge }}</span>
      </button>
    </div>

    <div class="page-body">
      <button class="btn-create" @click="$router.push('/irrigation/create')">
        <span class="btn-plus">+</span>
        新建灌溉任务
      </button>

      <div class="filter-row">
        <div class="filter-group">
          <label>农场</label>
          <select v-model="farmFilter" class="filter-select">
            <option value="">全部</option>
            <option value="东区">东区</option>
            <option value="西区">西区</option>
            <option value="南区">南区</option>
          </select>
        </div>
        <div class="filter-group">
          <label>地块</label>
          <select v-model="plotFilter" class="filter-select">
            <option value="">全部</option>
          </select>
        </div>
        <button class="btn-filter">筛选 ▼</button>
      </div>

      <div class="task-list">
        <div v-for="t in filteredTasks" :key="t.id" class="task-card">
          <div class="card-hd">
            <span class="task-name">{{ t.name }}</span>
            <span class="status-tag" :class="t.status">{{ t.statusText }}</span>
          </div>
          <div class="card-body">
            <div class="task-meta">创建日期: {{ t.createDate }}</div>
            <div class="task-meta">小任务数: {{ t.subTaskCount }}个</div>
            <div class="task-meta">灌溉时长: {{ t.duration }}</div>
            <div class="task-meta">总流量: {{ t.totalFlow }}</div>
            <div class="task-meta">瞬时: {{ t.instantFlow }}</div>
          </div>
          <div class="card-actions">
            <button class="btn-primary" @click="$router.push('/irrigation/' + t.id)">查看/执行</button>
            <button class="btn-secondary" @click="toast('编辑')">编辑</button>
            <button class="btn-secondary" @click="deleteTask(t.id)">删除</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { irrigationTasksApi } from '../api'
import { useToast } from '../composables/useToast'

const { toast } = useToast()
const tasks = ref([])
const farmFilter = ref('')
const plotFilter = ref('')
const flowBadge = ref('3+')

const filteredTasks = computed(() => {
  let list = tasks.value
  if (farmFilter.value) {
    list = list.filter(t => (t.farmPlot || '').startsWith(farmFilter.value))
  }
  return list
})

async function fetchTasks() {
  try {
    const { data } = await irrigationTasksApi.list()
    tasks.value = data || []
  } catch (e) {
    tasks.value = []
  }
}

async function deleteTask(id) {
  try {
    await irrigationTasksApi.delete(id)
    tasks.value = tasks.value.filter(t => t.id !== id)
    toast('已删除')
  } catch (e) {
    toast('删除失败')
  }
}

onMounted(fetchTasks)
</script>

<style scoped>
.irrigation-list .page-body { padding: 16px; }
.hdr-bar { display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: var(--primary-gradient); color: #FFF; }
.hdr-back { width: 36px; height: 36px; border: none; background: rgba(255,255,255,.2); color: #FFF; font-size: 24px; border-radius: 8px; cursor: pointer; }
.hdr-title { font-size: 18px; font-weight: 600; flex: 1; }
.hdr-flow { position: relative; width: 40px; height: 40px; border: none; background: rgba(255,255,255,.2); color: #FFF; font-size: 20px; border-radius: 8px; cursor: pointer; }
.flow-badge { position: absolute; top: -4px; right: -4px; background: var(--red); font-size: 10px; padding: 2px 5px; border-radius: 10px; }
.btn-create { width: 100%; padding: 16px; background: var(--primary-gradient); color: #FFF; border: none; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 16px; }
.btn-plus { font-size: 24px; }
.filter-row { display: flex; gap: 12px; margin-bottom: 16px; align-items: flex-end; }
.filter-group { flex: 1; }
.filter-group label { display: block; font-size: 12px; color: #666; margin-bottom: 4px; }
.filter-select { width: 100%; padding: 10px; border: 1px solid #E0E0E0; border-radius: 8px; font-size: 14px; }
.btn-filter { padding: 10px 16px; background: #F5F5F5; color: #666; border: 1px solid #E0E0E0; border-radius: 8px; font-size: 13px; cursor: pointer; }
.task-list { display: flex; flex-direction: column; gap: 12px; }
.task-card { background: #F5F5F5; border-radius: 12px; padding: 16px; }
.card-hd { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.task-name { font-size: 16px; font-weight: 600; color: var(--text); }
.status-tag { font-size: 12px; padding: 4px 10px; border-radius: 8px; }
.status-tag.pending { background: #E8EBE8; color: #616161; }
.status-tag.running { background: var(--primary-dim); color: var(--primary); }
.status-tag.completed { background: var(--blue-dim); color: var(--blue); }
.card-body { margin-bottom: 12px; }
.task-meta { font-size: 13px; color: #666; margin-bottom: 4px; }
.card-actions { display: flex; gap: 10px; }
.btn-primary { flex: 1; padding: 10px; background: var(--primary); color: #FFF; border: none; border-radius: 8px; font-size: 14px; cursor: pointer; }
.btn-secondary { padding: 10px 16px; background: #FFF; color: #666; border: 1px solid #E0E0E0; border-radius: 8px; font-size: 13px; cursor: pointer; }
</style>
