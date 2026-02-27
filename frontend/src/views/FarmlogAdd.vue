<template>
  <div class="page farmlog-add">
    <div class="hdr-title-bar">
      <button class="hdr-back" @click="$router.back()">‹</button>
      记录-{{ typeLabels[form.type] || '记事' }}
    </div>
    <div class="hdr-banner">
      <span class="banner-icon">📋</span>
      <span class="banner-title">添加农事记录</span>
      <button class="btn-save-header" @click="submit">保存</button>
    </div>

    <div class="page-body">
      <!-- 选择农场、地块 -->
      <div class="form-row-2">
        <div class="form-group">
          <label class="form-label">选择农场</label>
          <select v-model="form.farmId" class="form-select" @change="onFarmChange">
            <option value="">请选择农场</option>
            <option v-for="f in farms" :key="f.id" :value="f.id">{{ f.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">选择地块</label>
          <select v-model="form.fieldId" class="form-select" @change="onFieldChange">
            <option value="">请选择地块</option>
            <option v-for="f in availableFields" :key="f.id" :value="f.id">{{ f.name }}</option>
          </select>
        </div>
      </div>

      <!-- 作物、作业日期 -->
      <div class="form-row-2">
        <div class="form-group">
          <label class="form-label">作物</label>
          <input v-model="form.crop" type="text" class="form-input" readonly placeholder="根据地块自动填充" />
        </div>
        <div class="form-group">
          <label class="form-label">作业日期</label>
          <input v-model="form.date" type="date" class="form-input form-date" />
        </div>
      </div>

      <!-- 选择记录类型（根据模板设置动态显示） -->
      <div class="form-group">
        <div class="form-label-row">
          <label class="form-label">选择记录类型</label>
          <span class="form-link" @click="$router.push('/farmlog/template-settings')">⚙️ 常用模板设 ⚡</span>
        </div>
        <div class="type-btns">
          <button v-for="t in enabledTypeOptions" :key="t.key" type="button" class="type-btn" :class="{ active: form.type === t.key }" @click="form.type = t.key">
            <span class="type-btn-icon">⚡</span>
            {{ t.label }}
          </button>
        </div>
      </div>

      <!-- 日生长量：观测点 -->
      <div v-if="form.type === 'growth'" class="form-group">
        <label class="form-label">当日生长量记录</label>
        <div v-for="(pt, idx) in form.points" :key="idx" class="repeat-block">
          <div class="repeat-hd">观察点{{ idx + 1 }} <span class="repeat-del" @click="removePoint(idx)">🗑️</span></div>
          <div class="form-row-2">
            <div class="form-group"><label>株高(厘米)</label><input v-model.number="pt.height" type="number" class="form-input" /></div>
            <div class="form-group"><label>日生长量(厘米)</label><input v-model.number="pt.growth" type="number" class="form-input" /></div>
          </div>
          <div class="form-row-2">
            <div class="form-group"><label>叶数(片)</label><input v-model.number="pt.leaves" type="number" class="form-input" /></div>
            <div class="form-group"><label>苔数(苔)</label><input v-model.number="pt.stems" type="number" class="form-input" /></div>
          </div>
        </div>
        <button type="button" class="btn-add-item" @click="addPoint">+ 添加观测点</button>
      </div>

      <!-- 农药使用 -->
      <div v-else-if="form.type === 'pest'" class="form-group">
        <label class="form-label">农药使用记录</label>
        <div v-for="(p, idx) in form.pesticides" :key="idx" class="repeat-block">
          <div class="repeat-hd">农药{{ idx + 1 }} <span class="repeat-del" @click="removePesticide(idx)">🗑️</span></div>
          <div class="form-group"><label>农药名称</label><input v-model="p.name" type="text" class="form-input" placeholder="请输入农药名称" /></div>
          <div class="form-group"><label>主要作用</label><input v-model="p.effect" type="text" class="form-input" placeholder="杀虫/杀菌/除草" /></div>
          <div class="form-group"><label>用量</label><input v-model="p.amount" type="text" class="form-input" placeholder="g/亩或ml/亩" /></div>
        </div>
        <button type="button" class="btn-add-item" @click="addPesticide">+ 添加一种农药</button>
      </div>

      <!-- 水肥使用 -->
      <div v-else-if="form.type === 'water'" class="form-group">
        <label class="form-label">水肥使用记录</label>
        <div class="form-group"><label>亩用水量</label><input v-model.number="form.waterAmt" type="number" class="form-input" placeholder="立方米" /></div>
        <div v-for="(f, idx) in form.fertilizers" :key="idx" class="repeat-block">
          <div class="repeat-hd">化肥{{ idx + 1 }} <span class="repeat-del" @click="removeFertilizer(idx)">🗑️</span></div>
          <div class="form-group"><label>化肥名称</label><input v-model="f.name" type="text" class="form-input" /></div>
          <div class="form-group"><label>亩用量(公斤)</label><input v-model.number="f.amount" type="number" class="form-input" /></div>
          <div class="form-row-3">
            <div class="form-group"><label>氮含量(%)</label><input v-model.number="f.N" type="number" class="form-input" /></div>
            <div class="form-group"><label>磷含量(%)</label><input v-model.number="f.P" type="number" class="form-input" /></div>
            <div class="form-group"><label>钾含量(%)</label><input v-model.number="f.K" type="number" class="form-input" /></div>
          </div>
        </div>
        <button type="button" class="btn-add-item" @click="addFertilizer">+ 添加一种化肥</button>
      </div>

      <!-- 记事 -->
      <div v-else-if="form.type === 'diary'" class="form-group">
        <label class="form-label">记事记录</label>
        <label class="form-sublabel">详细内容</label>
        <textarea v-model="form.content" class="form-textarea" placeholder="请输入记事内容..." rows="6"></textarea>
      </div>

      <!-- 田间问题 -->
      <div v-else-if="form.type === 'issue'" class="form-group">
        <label class="form-label">田间问题记录</label>
        <div class="form-group"><label>问题描述</label><textarea v-model="form.issueDesc" class="form-textarea" placeholder="请详细描述田间问题..." rows="4"></textarea></div>
        <div class="form-group"><label>问题类型</label><input v-model="form.issueType" type="text" class="form-input" placeholder="如：缺素、病害等" /></div>
        <div class="form-group"><label>严重程度</label><div class="radio-row"><label v-for="s in severities" :key="s.key"><input v-model="form.severity" type="radio" :value="s.key" /> {{ s.label }}</label></div></div>
      </div>

      <!-- 作业照片 -->
      <div class="form-group">
        <label class="form-label">作业照片</label>
        <div class="photo-upload" @click="toast('添加照片')">
          <span class="photo-icon">📷</span>
          <span class="photo-text">添加照片</span>
        </div>
      </div>

      <!-- 备注 -->
      <div class="form-group">
        <label class="form-label">备注</label>
        <textarea v-model="form.notes" class="form-textarea" placeholder="可在此补充说明..." rows="3"></textarea>
      </div>

      <button class="btn-submit" @click="submit">
        <span class="btn-icon">✓</span>
        提交记录
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { farmlogApi, farmsApi, fieldsApi } from '../api'
import { useToast } from '../composables/useToast'
import { useFarmlogTemplates } from '../composables/useFarmlogTemplates'

const router = useRouter()
const { toast } = useToast()
const { getEnabledOptions } = useFarmlogTemplates()
const farms = ref([])
const fields = ref([])

const form = reactive({
  farmId: '',
  fieldId: '',
  crop: '',
  date: '',
  time: '',
  type: 'diary',
  content: '',
  notes: '',
  points: [{ height: null, growth: null, leaves: null, stems: null }],
  pesticides: [{ name: '', effect: '', amount: '' }],
  waterAmt: 0,
  fertilizers: [{ name: '', amount: null, N: null, P: null, K: null }],
  issueDesc: '',
  issueType: '',
  severity: 'medium',
})

const typeLabels = { growth: '日生长量', pest: '农药使用', water: '水肥使用', diary: '记事', issue: '田间问题' }
const severities = [{ key: 'minor', label: '轻微' }, { key: 'medium', label: '中等' }, { key: 'severe', label: '严重' }]

const enabledTypeOptions = computed(() => {
  const opts = getEnabledOptions()
  if (opts.length && !opts.find(o => o.key === form.type)) form.type = opts[0].key
  return opts
})

const availableFields = computed(() => {
  if (!form.farmId) return fields.value
  const farm = farms.value.find(f => f.id == form.farmId)
  if (farm?.fields?.length) {
    return farm.fields.map(f => ({ id: f.id, name: f.name, crop: f.crop }))
  }
  return fields.value.filter(f => f.farm === (farm?.name) || f.farmId == form.farmId)
})

function addPoint() { form.points.push({ height: null, growth: null, leaves: null, stems: null }) }
function removePoint(i) { if (form.points.length > 1) form.points.splice(i, 1) }
function addPesticide() { form.pesticides.push({ name: '', effect: '', amount: '' }) }
function removePesticide(i) { if (form.pesticides.length > 1) form.pesticides.splice(i, 1) }
function addFertilizer() { form.fertilizers.push({ name: '', amount: null, N: null, P: null, K: null }) }
function removeFertilizer(i) { if (form.fertilizers.length > 1) form.fertilizers.splice(i, 1) }

function onFarmChange() { form.fieldId = ''; form.crop = '' }
function onFieldChange() {
  const f = availableFields.value.find(x => x.id == form.fieldId) || fields.value.find(x => x.id == form.fieldId)
  form.crop = f?.crop || ''
}

onMounted(async () => {
  const today = new Date()
  form.date = `${today.getFullYear()}-${String(today.getMonth()+1).padStart(2,'0')}-${String(today.getDate()).padStart(2,'0')}`
  form.time = `${String(today.getHours()).padStart(2,'0')}:${String(today.getMinutes()).padStart(2,'0')}`
  const [farmsRes, fieldsRes] = await Promise.all([farmsApi.list(), fieldsApi.list()])
  farms.value = farmsRes.data || []
  fields.value = fieldsRes.data || []
  if (farms.value.length && !form.farmId) form.farmId = farms.value[0].id
})

async function submit() {
  if (!form.fieldId) { toast('请选择地块'); return }
  if (!form.date) { toast('请选择作业日期'); return }
  const field = fields.value.find(f => f.id == form.fieldId) || availableFields.value.find(f => f.id == form.fieldId)
  if (!field) { toast('请选择有效地块'); return }

  let data = {}
  if (form.type === 'diary') data = { content: form.content }
  else if (form.type === 'growth') {
    data = { points: form.points.map((p, i) => ({ no: i + 1, area: '区域' + String.fromCharCode(65 + i), height: p.height || 0, growth: p.growth || 0, leaves: p.leaves || 0, stems: p.stems || 0 })) }
  }
  else if (form.type === 'water') {
    data = { waterAmt: form.waterAmt || 0, fertilizers: form.fertilizers.map((f, i) => ({ no: i + 1, name: f.name || '', amount: f.amount || 0, N: f.N || 0, P: f.P || 0, K: f.K || 0 })) }
  }
  else if (form.type === 'pest') {
    data = { pesticides: form.pesticides.map((p, i) => ({ no: i + 1, name: p.name || '', effect: p.effect || '', amount: p.amount || '' })) }
  }
  else if (form.type === 'issue') data = { desc: form.issueDesc || '', issueType: form.issueType || '', severity: form.severity || 'medium' }

  try {
    const { data: res } = await farmlogApi.create({
      farmId: form.farmId || null,
      fieldId: parseInt(form.fieldId),
      date: form.date,
      time: form.time,
      type: form.type,
      data,
      photos: [],
      notes: form.notes,
    })
    if (res.success) {
      toast('提交成功 ✓')
      router.push('/farmlog')
    } else {
      toast(res.message || '提交失败')
    }
  } catch (e) {
    toast('提交失败')
  }
}
</script>

<style scoped>
.farmlog-add .page-body { padding: 16px; padding-bottom: 32px; }
.hdr-title-bar { display: flex; align-items: center; gap: 12px; padding: 10px 16px; background: #F5F5F5; font-size: 14px; color: #666; }
.hdr-back { width: 32px; height: 32px; border: none; background: rgba(46,125,50,.1); color: var(--primary); font-size: 22px; border-radius: 8px; cursor: pointer; }
.hdr-banner {
  display: flex; align-items: center; padding: 14px 16px;
  background: linear-gradient(135deg, var(--primary), var(--primary-light)); color: #FFF;
}
.banner-icon { font-size: 22px; }
.banner-title { flex: 1; font-size: 16px; font-weight: 600; }
.btn-save-header { padding: 8px 16px; background: #FFF; color: var(--primary); border: none; border-radius: 8px; font-size: 14px; font-weight: 500; cursor: pointer; }
.form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.form-row-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: 13px; color: var(--text2); margin-bottom: 6px; }
.form-label { display: block; font-size: 14px; color: #1B2E1B; margin-bottom: 8px; font-weight: 500; }
.form-sublabel { display: block; font-size: 13px; color: var(--text2); margin-bottom: 6px; }
.form-label-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.form-link { font-size: 12px; color: var(--primary); cursor: pointer; }
.form-select, .form-input {
  width: 100%; padding: 12px 14px; background: #F7FAF7;
  border: 1.5px solid rgba(46,125,50,.2); border-radius: 10px;
  font-size: 14px; color: #1B2E1B; box-sizing: border-box;
}
.form-input[readonly] { background: #EEE; color: #666; }
.type-btns { display: flex; flex-wrap: wrap; gap: 10px; }
.type-btn {
  padding: 10px 16px; border: 1.5px solid rgba(46,125,50,.25);
  background: #FFF; color: var(--text2); border-radius: 10px; font-size: 13px;
  cursor: pointer; display: flex; align-items: center; gap: 4px;
}
.type-btn.active { background: var(--primary); color: #FFF; border-color: var(--primary); }
.type-btn-icon { font-size: 10px; }
.repeat-block { padding: 12px; background: #F7FAF7; border-radius: 10px; margin-bottom: 12px; border: 1px solid rgba(46,125,50,.1); }
.repeat-hd { font-size: 14px; font-weight: 600; color: #1B2E1B; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
.repeat-del { cursor: pointer; font-size: 14px; }
.btn-add-item { width: 100%; padding: 10px; background: #E8F0F8; color: var(--blue); border: 1px dashed #9BB8E0; border-radius: 8px; font-size: 13px; cursor: pointer; margin-bottom: 12px; }
.radio-row { display: flex; gap: 16px; flex-wrap: wrap; }
.radio-row label { display: flex; align-items: center; gap: 6px; cursor: pointer; font-size: 14px; color: #1B2E1B; }
.form-textarea {
  width: 100%; padding: 12px 14px; background: #F7FAF7;
  border: 1.5px solid rgba(46,125,50,.2); border-radius: 10px;
  font-size: 14px; color: #1B2E1B; resize: vertical; box-sizing: border-box;
}
.photo-upload {
  padding: 32px; background: #F0F0F0; border: 2px dashed rgba(46,125,50,.3);
  border-radius: 10px; display: flex; flex-direction: column; align-items: center; gap: 8px;
  cursor: pointer;
}
.photo-icon { font-size: 36px; }
.photo-text { font-size: 14px; color: #666; font-weight: 500; }
.btn-submit {
  width: 100%; padding: 14px; margin-top: 8px; background: var(--primary); color: #FFF;
  border: none; border-radius: 10px; font-size: 16px; font-weight: 600; cursor: pointer;
  display: flex; align-items: center; justify-content: center; gap: 8px;
}
.btn-icon { font-size: 18px; }
</style>
