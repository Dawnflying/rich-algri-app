<template>
  <div class="page irrigation-create">
    <div class="hdr-bar">
      <button class="hdr-back" @click="$router.back()">‹</button>
      <span class="hdr-title">创建灌溉任务</span>
    </div>

    <div class="page-body">
      <div class="form-row">
        <div class="form-group">
          <label>请选择农场地块</label>
          <select v-model="form.farmPlot" class="form-select">
            <option value="">请选择</option>
            <option value="东区果园">东区果园</option>
            <option value="西区棉田">西区棉田</option>
            <option value="南区果园">南区果园</option>
          </select>
        </div>
        <div class="form-group">
          <label>请选择日期</label>
          <input v-model="form.date" type="date" class="form-input" />
        </div>
        <button class="btn-zoom">🔍 放大查看</button>
      </div>

      <div class="section">
        <div class="section-title">灌溉任务</div>
        <div class="section-hint">友情提示: 同一任务尽量选择同一地块/同类的滴灌带地块</div>

        <div class="pipe-section">
          <div v-for="b in 3" :key="b" class="branch">
            <div class="branch-label">{{ b }}支管尾</div>
            <div class="pipe-rows">
              <div class="pipe-row B">
                <button v-for="n in 7" :key="'B'+n" class="pipe-node" :class="{ selected: selectedNodes[b-1]?.B?.includes(n) }" @click="toggleNode(b, 'B', n)">{{ 8-n }}B</button>
              </div>
              <div class="pipe-row A">
                <button v-for="n in 7" :key="'A'+n" class="pipe-node active" :class="{ selected: selectedNodes[b-1]?.A?.includes(n) }" @click="toggleNode(b, 'A', n)">{{ 8-n }}A</button>
              </div>
            </div>
            <div class="branch-head">{{ b }}A {{ b }}支管头</div>
          </div>
        </div>

        <div class="sub-tasks">
          <div v-for="(st, i) in form.subTasks" :key="i" class="sub-task">
            <div class="sub-task-hd">任务{{ i + 1 }}</div>
            <div class="sub-task-body">
              <div class="duration-row">
                <span>灌溉时长</span>
                <input v-model.number="st.hour" type="number" placeholder="时" class="dur-input" /> 时
                <input v-model.number="st.min" type="number" placeholder="分" class="dur-input" /> 分
              </div>
              <div class="valve-row">
                <button class="btn-valve" @click="toast('选择电动阀')">选择电动阀</button>
                <span class="valve-text">{{ st.valves || '1支管/A' }}</span>
                <button class="btn-delete" @click="removeSubTask(i)">🗑</button>
              </div>
            </div>
          </div>
        </div>

        <button class="btn-add-task" @click="addSubTask">+ 添加任务</button>
        <button class="btn-submit" @click="submitTask">提交任务</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { irrigationTasksApi } from '../api'
import { useToast } from '../composables/useToast'

const router = useRouter()
const { toast } = useToast()

const selectedNodes = ref([{ A: [], B: [] }, { A: [], B: [] }, { A: [], B: [] }])

const form = reactive({
  farmPlot: '东区果园',
  date: '',
  subTasks: [
    { hour: 2, min: 20, valves: '1支管/A' },
    { hour: 2, min: 20, valves: '2支管/A' },
    { hour: 2, min: 20, valves: '3支管/A' },
  ],
})

function toggleNode(branch, row, num) {
  const b = branch - 1
  if (!selectedNodes.value[b]) selectedNodes.value[b] = { A: [], B: [] }
  const arr = selectedNodes.value[b][row] || []
  const idx = arr.indexOf(num)
  if (idx >= 0) arr.splice(idx, 1)
  else arr.push(num)
}

function addSubTask() {
  form.subTasks.push({ hour: 2, min: 20, valves: '1支管/A' })
}

function removeSubTask(i) {
  form.subTasks.splice(i, 1)
}

async function submitTask() {
  if (!form.farmPlot) {
    toast('请选择农场地块')
    return
  }
  try {
    const { data } = await irrigationTasksApi.create({
      name: form.farmPlot + '-灌溉',
      farmPlot: form.farmPlot,
      date: form.date || new Date().toISOString().slice(0, 10),
      subTasks: form.subTasks.map(st => ({
        duration: `${st.hour || 0}h${st.min || 0}m`,
        totalFlow: '640m³',
        instantFlow: '300m³/h',
        valves: st.valves,
      })),
    })
    toast('任务创建成功')
    router.push('/irrigation')
  } catch (e) {
    toast(e?.response?.data?.detail || '创建失败')
  }
}

onMounted(() => {
  const d = new Date()
  form.date = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
})
</script>

<style scoped>
.irrigation-create .page-body { padding: 16px; }
.hdr-bar { display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: var(--primary-gradient); color: #FFF; }
.hdr-back { width: 36px; height: 36px; border: none; background: rgba(255,255,255,.2); color: #FFF; font-size: 24px; border-radius: 8px; cursor: pointer; }
.hdr-title { font-size: 18px; font-weight: 600; }
.form-row { display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
.form-group { flex: 1; min-width: 120px; }
.form-group label { display: block; font-size: 12px; color: #666; margin-bottom: 4px; }
.form-select, .form-input { width: 100%; padding: 10px; border: 1px solid #E0E0E0; border-radius: 8px; font-size: 14px; }
.btn-zoom { padding: 10px 16px; background: var(--primary); color: #FFF; border: none; border-radius: 8px; font-size: 13px; cursor: pointer; align-self: flex-end; }
.section { background: #FFF; border-radius: 12px; padding: 16px; margin-bottom: 16px; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.section-title { font-size: 16px; font-weight: 600; margin-bottom: 8px; }
.section-hint { font-size: 12px; color: #999; margin-bottom: 16px; }
.pipe-section { margin-bottom: 20px; }
.branch { margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid #EEE; }
.branch:last-child { border-bottom: none; }
.branch-label { font-size: 13px; color: #666; margin-bottom: 8px; }
.pipe-rows { display: flex; flex-direction: column; gap: 4px; }
.pipe-row { display: flex; gap: 6px; align-items: center; }
.pipe-node { width: 36px; height: 36px; border-radius: 50%; border: 1px solid #E0E0E0; background: #F5F5F5; font-size: 11px; cursor: pointer; }
.pipe-node.active { background: var(--blue-dim); border-color: var(--blue); color: var(--blue); }
.pipe-node.selected { background: var(--primary); border-color: var(--primary); color: #FFF; }
.branch-head { font-size: 12px; color: #666; margin-top: 4px; }
.sub-tasks { margin-bottom: 16px; }
.sub-task { background: #F5F5F5; border-radius: 8px; padding: 12px; margin-bottom: 10px; }
.sub-task-hd { font-size: 14px; font-weight: 600; margin-bottom: 8px; }
.duration-row { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; font-size: 14px; }
.dur-input { width: 50px; padding: 6px; border: 1px solid #E0E0E0; border-radius: 6px; text-align: center; }
.valve-row { display: flex; align-items: center; gap: 8px; }
.btn-valve { padding: 6px 12px; background: var(--blue); color: #FFF; border: none; border-radius: 6px; font-size: 12px; cursor: pointer; }
.valve-text { font-size: 13px; color: #666; flex: 1; }
.btn-delete { background: none; border: none; font-size: 16px; cursor: pointer; color: var(--red); }
.btn-add-task { width: 100%; padding: 12px; background: var(--card); color: var(--primary); border: 2px dashed var(--primary); border-radius: 8px; font-size: 14px; cursor: pointer; margin-bottom: 12px; }
.btn-submit { width: 100%; padding: 14px; background: var(--blue); color: #FFF; border: none; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; }
</style>
