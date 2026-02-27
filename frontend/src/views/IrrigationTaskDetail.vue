<template>
  <div class="page irrigation-detail">
    <div class="hdr-bar">
      <button class="hdr-back" @click="$router.back()">‹</button>
      <span class="hdr-title">{{ task?.farmPlot }}-{{ task?.name || '夏灌' }}</span>
      <span class="status-tag" :class="task?.status">{{ task?.statusText }}</span>
    </div>

    <div class="page-body" v-if="task">
      <div class="form-row">
        <select class="plot-select">
          <option value="">请选择农场地块</option>
          <option value="东区果园">东区果园</option>
        </select>
      </div>

      <div class="view-section">
        <div class="view-title">灌溉状态总览</div>
        <div class="view-tabs">
          <button class="view-tab" :class="{ active: viewMode === 'pipe' }" @click="viewMode = 'pipe'">
            <span class="tab-icon">🔧</span>
            管道视图
          </button>
          <button class="view-tab" :class="{ active: viewMode === 'map' }" @click="viewMode = 'map'">
            <span class="tab-icon">🗺️</span>
            地图视图
          </button>
        </div>
      </div>

      <!-- 管道视图 -->
      <div v-if="viewMode === 'pipe'" class="pipe-view">
        <div class="pipe-diagram">
          <div v-for="(branch, bi) in 3" :key="bi" class="branch-row">
            <div class="branch-label">{{ bi + 1 }}支管</div>
            <div class="pipe-nodes">
              <div class="node-row B">
                <div v-for="n in 7" :key="'B'+n" class="node" :class="getNodeStatus(bi, 'B', n)">{{ 8-n }}B</div>
              </div>
              <div class="node-row A">
                <div v-for="n in 7" :key="'A'+n" class="node" :class="getNodeStatus(bi, 'A', n)">{{ 8-n }}A</div>
              </div>
            </div>
          </div>
        </div>
        <div class="legend">
          <div class="legend-item"><span class="dot completed"></span>已完成</div>
          <div class="legend-item"><span class="dot pending"></span>待执行</div>
          <div class="legend-item"><span class="dot irrigating"></span>正在灌溉</div>
          <div class="legend-item"><span class="dot alarm"></span>设备告警</div>
        </div>
      </div>

      <!-- 地图视图 -->
      <div v-else class="map-view">
        <div class="map-placeholder">
          <div class="map-overlay">
            <span class="map-label">玛纳斯河</span>
            <div class="zone-labels">
              <span v-for="z in zoneLabels" :key="z.id" class="zone-tag" :class="z.status">{{ z.label }}</span>
            </div>
          </div>
        </div>
        <div class="legend">
          <div class="legend-item"><span class="dot completed"></span>已完成</div>
          <div class="legend-item"><span class="dot pending"></span>待执行</div>
          <div class="legend-item"><span class="dot irrigating"></span>正在灌溉</div>
          <div class="legend-item"><span class="dot alarm"></span>设备告警</div>
        </div>
      </div>

      <button class="btn-one-click">⚡ 一键灌溉</button>

      <div class="sub-task-list">
        <div v-for="(st, i) in task.subTasks" :key="i" class="sub-task-card">
          <div class="sub-task-info">
            <div class="sub-task-meta">{{ st.valves }}</div>
            <div class="sub-task-meta">灌溉时长 {{ st.duration }} · 总流量 {{ st.totalFlow }} · 瞬时 {{ st.instantFlow }}</div>
          </div>
          <button class="btn-action" :class="st.status" @click="toast(st.statusText)">
            {{ st.statusText }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { irrigationTasksApi } from '../api'
import { useToast } from '../composables/useToast'

const route = useRoute()
const { toast } = useToast()
const task = ref(null)
const viewMode = ref('pipe')

const zoneLabels = computed(() => [
  { id: 1, label: '1A', status: 'completed' },
  { id: 2, label: '2B', status: 'pending' },
  { id: 3, label: '7A', status: 'pending' },
  { id: 4, label: '8B', status: 'pending' },
  { id: 5, label: '1头', status: 'pending' },
  { id: 6, label: '2头', status: 'pending' },
  { id: 7, label: '1尾', status: 'pending' },
  { id: 8, label: '尾', status: 'pending' },
])

function getNodeStatus(branchIdx, row, num) {
  const nodes = task.value?.pipeNodes
  if (!nodes) return 'pending'
  const b = String(branchIdx + 1)
  const arr = nodes[b]?.[row]
  if (!arr || !Array.isArray(arr)) return 'pending'
  const idx = num - 1
  return arr[idx] || 'pending'
}

onMounted(async () => {
  const id = Number(route.params.id)
  if (!id) return
  try {
    const { data } = await irrigationTasksApi.get(id)
    task.value = data
  } catch (e) {
    task.value = null
  }
})
</script>

<style scoped>
.irrigation-detail .page-body { padding: 16px; }
.hdr-bar { display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: var(--primary-gradient); color: #FFF; }
.hdr-back { width: 36px; height: 36px; border: none; background: rgba(255,255,255,.2); color: #FFF; font-size: 24px; border-radius: 8px; cursor: pointer; }
.hdr-title { font-size: 16px; font-weight: 600; flex: 1; }
.status-tag { font-size: 12px; padding: 4px 10px; border-radius: 8px; background: rgba(255,255,255,.3); }
.status-tag.running { background: var(--primary-dim); color: var(--primary-dark); }
.plot-select { width: 100%; padding: 10px; border: 1px solid #E0E0E0; border-radius: 8px; font-size: 14px; margin-bottom: 16px; }
.view-section { margin-bottom: 16px; }
.view-title { font-size: 14px; font-weight: 600; margin-bottom: 10px; }
.view-tabs { display: flex; gap: 12px; }
.view-tab { flex: 1; padding: 12px; border: 1px solid #E0E0E0; background: #FFF; border-radius: 8px; font-size: 14px; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; }
.view-tab.active { background: var(--primary); color: #FFF; border-color: var(--primary); }
.tab-icon { font-size: 18px; }
.pipe-view, .map-view { background: #FFF; border-radius: 12px; padding: 16px; margin-bottom: 16px; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.pipe-diagram { margin-bottom: 16px; }
.branch-row { margin-bottom: 16px; }
.branch-label { font-size: 12px; color: #666; margin-bottom: 8px; }
.node-row { display: flex; gap: 6px; margin-bottom: 4px; }
.node { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 10px; }
.node.completed { background: #212121; color: #FFF; }
.node.pending { background: #FFF59D; color: #333; }
.node.irrigating { background: var(--primary-light); color: #FFF; }
.node.alarm { background: #F44336; color: #FFF; }
.legend { display: flex; flex-wrap: wrap; gap: 12px; padding: 12px 0; }
.legend-item { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #666; }
.dot { width: 10px; height: 10px; border-radius: 50%; }
.dot.completed { background: #212121; }
.dot.pending { background: #FFF59D; }
.dot.irrigating { background: var(--primary-light); }
.dot.alarm { background: #F44336; }
.map-placeholder { min-height: 200px; background: linear-gradient(180deg, var(--primary-dim) 0%, #D4EDDA 50%, #B8E6C4 100%); border-radius: 8px; position: relative; }
.map-overlay { position: absolute; inset: 0; padding: 16px; }
.map-label { position: absolute; bottom: 20px; left: 20px; font-size: 12px; color: var(--blue); }
.zone-labels { display: flex; flex-wrap: wrap; gap: 8px; }
.zone-tag { padding: 4px 10px; border-radius: 6px; font-size: 11px; }
.zone-tag.completed { background: #212121; color: #FFF; }
.zone-tag.pending { background: #FFF59D; color: #333; }
.btn-one-click { width: 100%; padding: 14px; background: var(--orange); color: #FFF; border: none; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; margin-bottom: 12px; }
.sub-task-list { display: flex; flex-direction: column; gap: 12px; }
.sub-task-card { display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; background: #F5F5F5; border-radius: 12px; }
.sub-task-info { flex: 1; }
.sub-task-meta { font-size: 13px; color: #666; margin-bottom: 4px; }
.btn-action { padding: 8px 20px; border: none; border-radius: 8px; font-size: 14px; cursor: pointer; }
.btn-action.completed { background: var(--blue); color: #FFF; }
.btn-action.running { background: #9E9E9E; color: #FFF; }
.btn-action.pending { background: var(--primary); color: #FFF; }
</style>
