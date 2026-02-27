<template>
  <div class="page field-edit">
    <div class="hdr field-edit-hdr">
      <button class="hdr-back" @click="$router.back()">‹</button>
      <div class="hdr-left">
        <span class="hdr-label">编辑地块</span>
        <span class="hdr-icon">⚡</span>
      </div>
      <button class="btn-save" @click="save">保存</button>
    </div>

    <div class="page-body">
      <!-- 所属农场 -->
      <div class="form-group">
        <label class="form-label">所属农场</label>
        <select v-model="form.farmId" class="form-select">
          <option value="">请选择所属农场</option>
          <option v-for="f in farms" :key="f.id" :value="f.id">{{ f.name }}</option>
        </select>
      </div>

      <!-- 地块位置示意图 -->
      <div class="form-group">
        <div class="map-placeholder" @click="goToMapPlot">
          <span class="map-pin">📍</span>
          <span class="map-hint">地块位置示意图</span>
          <span class="map-loc">{{ form.location || '新疆维吾尔自治区 石河子市' }}</span>
          <button type="button" class="btn-adjust-range">✓ 调整地块范围</button>
        </div>
      </div>

      <!-- 地块名称 -->
      <div class="form-group">
        <label class="form-label">地块名称</label>
        <input v-model="form.name" type="text" class="form-input" placeholder="请输入地块名称" />
      </div>

      <!-- 作物类型 -->
      <div class="form-group">
        <label class="form-label">作物类型</label>
        <input v-model="form.crop" type="text" class="form-input" placeholder="请输入作物类型" list="crop-list" />
        <datalist id="crop-list">
          <option value="棉花" /><option value="小麦" /><option value="玉米" /><option value="水稻" /><option value="大豆" /><option value="番茄" />
        </datalist>
      </div>

      <!-- 作物种子 -->
      <div class="form-group">
        <label class="form-label">作物种子</label>
        <input v-model="form.cropSeed" type="text" class="form-input" placeholder="请输入作物种子" />
      </div>

      <!-- 种植模式 -->
      <div class="form-group">
        <label class="form-label">种植模式</label>
        <div class="option-row">
          <button v-for="opt in plantingModes" :key="opt" type="button" class="option-btn" :class="{ active: form.plantingMode === opt }" @click="form.plantingMode = opt">{{ opt }}</button>
        </div>
      </div>

      <!-- 种穴数量 -->
      <div class="form-group">
        <label class="form-label">种穴数量</label>
        <div class="option-row option-row-num">
          <button v-for="n in [11,12,13,14,15,16]" :key="n" type="button" class="option-btn" :class="{ active: form.plantHoleCount === n }" @click="form.plantHoleCount = n">{{ n }}</button>
        </div>
      </div>

      <!-- 滴灌带流量 -->
      <div class="form-group">
        <label class="form-label">滴灌带流量</label>
        <div class="flow-row">
          <input v-model.number="form.dripFlow" type="range" min="0.5" max="4" step="0.1" class="flow-slider" />
          <span class="flow-val">{{ form.dripFlow }} L/h</span>
        </div>
        <div class="flow-input-wrap">
          <input v-model.number="form.dripFlow" type="number" step="0.1" min="0.5" max="4" class="form-input flow-input" />
          <span class="flow-unit">L/h</span>
        </div>
      </div>

      <!-- 地孔间距 -->
      <div class="form-group">
        <label class="form-label">地孔间距</label>
        <div class="option-row">
          <button v-for="opt in holeSpacings" :key="opt" type="button" class="option-btn" :class="{ active: form.holeSpacing === opt }" @click="form.holeSpacing = opt">{{ opt }}</button>
        </div>
      </div>

      <!-- 水源类型 -->
      <div class="form-group">
        <label class="form-label">水源类型</label>
        <div class="option-row">
          <button v-for="opt in waterSources" :key="opt" type="button" class="option-btn" :class="{ active: form.waterSource === opt }" @click="form.waterSource = opt">{{ opt }}</button>
        </div>
      </div>

      <!-- 沟心间距 -->
      <div class="form-group">
        <label class="form-label">沟心间距</label>
        <div class="trench-row">
          <input v-model.number="form.trenchMeter" type="number" min="0" class="form-input trench-input" placeholder="0" />
          <span class="trench-sep">米</span>
          <input v-model.number="form.trenchCm" type="number" min="0" max="99" class="form-input trench-input" placeholder="0" />
          <span class="trench-sep">厘米</span>
        </div>
      </div>

      <!-- 土壤性质 -->
      <div class="form-group">
        <label class="form-label">土壤性质</label>
        <div class="option-row">
          <button v-for="opt in soilTypes" :key="opt" type="button" class="option-btn" :class="{ active: form.soilType === opt }" @click="form.soilType = opt">{{ opt }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { farmsApi, fieldsApi } from '../api'
import { useToast } from '../composables/useToast'

const route = useRoute()
const router = useRouter()
const { toast } = useToast()

const farms = ref([])
const form = reactive({
  farmId: '',
  name: '',
  crop: '',
  cropSeed: '',
  location: '新疆维吾尔自治区 石河子市',
  boundary: [], // 地块边界坐标，由地图打点页回传
  plantingMode: '一膜三行',
  plantHoleCount: 11,
  dripFlow: 2.0,
  holeSpacing: '20厘米',
  waterSource: '井水',
  trenchMeter: null,
  trenchCm: null,
  soilType: '沙土',
})

const plantingModes = ['一膜三行', '一膜四行', '一膜六行']
const holeSpacings = ['20厘米', '25厘米', '30厘米']
const waterSources = ['井水', '渠水']
const soilTypes = ['沙土', '壤土', '沙壤土', '粘土']

function goToMapPlot() {
  const query = { from: route.fullPath }
  if (form.farmId) query.farmId = form.farmId
  if (form.boundary?.length) query.boundary = JSON.stringify(form.boundary)
  router.push({ path: '/field/map-plot', query })
}

onMounted(async () => {
  const { data } = await farmsApi.list()
  farms.value = data || []
  const qFarmId = route.query.farmId
  if (qFarmId) form.farmId = parseInt(qFarmId) || qFarmId
  else if (farms.value.length && !form.farmId) form.farmId = farms.value[0].id
  const boundaryStr = route.query.boundary
  if (boundaryStr) {
    try {
      form.boundary = JSON.parse(boundaryStr)
    } catch (_) {}
  }
})

async function save() {
  if (!form.name?.trim()) {
    toast('请输入地块名称')
    return
  }
  if (!form.crop?.trim()) {
    toast('请输入作物类型')
    return
  }
  try {
    const area = calcAreaFromBoundary(form.boundary)
    const payload = {
      farmId: form.farmId || null,
      name: form.name.trim(),
      crop: form.crop.trim(),
      cropSeed: form.cropSeed || '',
      location: form.location,
      boundary: form.boundary,
      planting: form.plantingMode,
      plantHoleCount: form.plantHoleCount,
      dripFlow: form.dripFlow,
      holeSpacing: form.holeSpacing,
      waterSource: form.waterSource,
      trenchMeter: form.trenchMeter,
      trenchCm: form.trenchCm,
      soilType: form.soilType,
      area: area || 0,
    }
    const { data } = await fieldsApi.add(payload)
    if (data.success) {
      toast('保存成功 ✓')
      router.back()
    } else {
      toast(data.message || '保存失败')
    }
  } catch (e) {
    toast('保存失败')
  }
}

function calcAreaFromBoundary(boundary) {
  if (!boundary || boundary.length < 3) return 0
  // 简化：用多边形面积近似，实际应使用球面面积
  let area = 0
  const n = boundary.length
  for (let i = 0; i < n; i++) {
    const j = (i + 1) % n
    area += boundary[i].lng * boundary[j].lat
    area -= boundary[j].lng * boundary[i].lat
  }
  area = Math.abs(area) / 2
  // 粗略换算：1度约111km，石河子纬度约44°，1度经度约80km
  const sqDegToMu = (111 * 80 * 1e6) / 666.67 // 平方米转亩
  return Math.round(area * sqDegToMu * 100) / 100
}
</script>

<style scoped>
.field-edit .page-body { padding: 16px; padding-bottom: 32px; }
.field-edit-hdr {
  display: flex; align-items: center; padding: 12px 16px;
  background: #FFF; border-bottom: 1px solid rgba(46,125,50,.1);
}
.hdr-back { width: 36px; height: 36px; border: none; background: rgba(46,125,50,.1); color: var(--primary); font-size: 24px; border-radius: 8px; cursor: pointer; flex-shrink: 0; }
.hdr-left { flex: 1; display: flex; align-items: center; gap: 6px; margin-left: 12px; }
.hdr-label { font-size: 15px; font-weight: 600; color: #1B2E1B; }
.hdr-icon { font-size: 16px; }
.btn-save { padding: 8px 20px; background: var(--primary); color: #FFF; border: none; border-radius: 8px; font-size: 14px; font-weight: 500; cursor: pointer; }
.form-group { margin-bottom: 20px; }
.form-label { display: block; font-size: 14px; color: #1B2E1B; margin-bottom: 8px; font-weight: 500; }
.form-select, .form-input {
  width: 100%; padding: 12px 14px; background: #F7FAF7;
  border: 1.5px solid rgba(46,125,50,.2); border-radius: 10px;
  font-size: 14px; color: #1B2E1B; box-sizing: border-box;
}
.map-placeholder {
  background: #F0F0F0; border-radius: 10px; padding: 24px;
  display: flex; flex-direction: column; align-items: center; gap: 8px;
  cursor: pointer; border: 1px dashed rgba(46,125,50,.3);
}
.map-pin { font-size: 28px; }
.map-hint { font-size: 13px; color: #666; }
.map-loc { font-size: 12px; color: #5A7A5A; }
.btn-adjust-range {
  margin-top: 8px; padding: 10px 20px; background: var(--primary); color: #FFF;
  border: none; border-radius: 8px; font-size: 14px; cursor: pointer;
}
.option-row { display: flex; gap: 10px; flex-wrap: wrap; }
.option-btn {
  padding: 10px 16px; border: 1.5px solid rgba(46,125,50,.25);
  background: #FFF; color: #5A7A5A; border-radius: 8px; font-size: 13px; cursor: pointer;
}
.option-btn.active { background: var(--primary); color: #FFF; border-color: var(--primary); }
.option-row-num .option-btn { padding: 10px 14px; }
.flow-row { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
.flow-slider { flex: 1; height: 6px; accent-color: var(--primary); }
.flow-val { font-size: 14px; color: var(--primary); font-weight: 500; min-width: 70px; }
.flow-input-wrap { display: flex; align-items: center; gap: 8px; }
.flow-input { flex: 1; max-width: 120px; }
.flow-unit { font-size: 14px; color: #5A7A5A; }
.trench-row { display: flex; align-items: center; gap: 8px; }
.trench-input { flex: 1; max-width: 100px; }
.trench-sep { font-size: 14px; color: #5A7A5A; }
</style>
