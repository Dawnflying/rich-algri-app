<template>
  <div class="page guidance-invite">
    <div class="hdr-bar">
      <button class="hdr-back" @click="$router.back()">‹</button>
      <span class="hdr-title">⚡ 邀请指导</span>
    </div>

    <div class="page-body">
      <div class="form-section">
        <div class="section-title">选择地块</div>
        <div class="form-row">
          <div class="form-group">
            <label>选择农田</label>
            <select v-model="form.farmId" class="form-select" @change="onFarmChange">
              <option value="">请选择</option>
              <option v-for="f in farms" :key="f.id" :value="f.id">{{ f.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>选择地块</label>
            <select v-model="form.fieldId" class="form-select" @change="onFieldChange">
              <option value="">请选择</option>
              <option v-for="f in availableFields" :key="f.id" :value="f.id">{{ f.name }}</option>
            </select>
          </div>
        </div>
      </div>

      <div v-if="selectedField" class="plot-detail">
        <div class="detail-item"><span class="label">地块名称</span><span>{{ selectedField.name }}</span></div>
        <div class="detail-item"><span class="label">所属农田</span><span>{{ selectedFarm?.name }}</span></div>
        <div class="detail-item"><span class="label">面积</span><span>{{ selectedField.area }}亩</span></div>
        <div class="detail-item"><span class="label">位置</span><span>{{ selectedFarm?.region || selectedFarm?.location || '新疆维吾尔自治区 石河子市' }}</span></div>
        <div class="detail-item"><span class="label">当前作物</span><span>{{ selectedField.crop }}</span></div>
      </div>

      <div class="form-section">
        <div class="section-title">选择类型</div>
        <select v-model="form.guidanceType" class="form-select">
          <option value="">请选择</option>
          <option value="棉花生长问题">棉花生长问题</option>
          <option value="病虫害防治">病虫害防治</option>
          <option value="土壤肥力问题">土壤肥力问题</option>
          <option value="灌溉指导">灌溉指导</option>
        </select>
      </div>

      <div class="form-section">
        <div class="section-title">选择人员</div>
        <select v-model="form.personId" class="form-select" @change="onPersonChange">
          <option value="">请选择</option>
          <option value="1">张三</option>
          <option value="2">李农师</option>
          <option value="3">王技师</option>
          <option value="4">张专家</option>
        </select>
      </div>

      <div class="form-section">
        <div class="section-title">填写问题</div>
        <textarea v-model="form.problem" class="form-textarea" placeholder="请描述需要指导的问题: 例如:地块北侧棉花叶片黄化,植株中下部明显,可是养分不足或病虫害导致...." rows="5"></textarea>
      </div>

      <div class="form-section">
        <div class="section-title">添加图片</div>
        <div class="upload-area" @click="toast('点击上传图片')">
          <span class="upload-icon">+</span>
          <div class="upload-text">点击上传图片</div>
          <div class="upload-hint">支持JPG、PNG格式,最多上传5张</div>
        </div>
      </div>

      <div class="form-section">
        <div class="section-title">重点记录选择(可选)</div>
        <select v-model="form.recordId" class="form-select">
          <option value="">选择记录...</option>
          <option value="1">玉米病虫害防治 (2024-01-18)</option>
        </select>
      </div>

      <div class="form-actions">
        <button class="btn-cancel" @click="$router.back()">取消</button>
        <button class="btn-submit" @click="submitInvite">发送邀请</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { farmsApi, guidanceApi } from '../api'
import { useToast } from '../composables/useToast'

const router = useRouter()
const { toast } = useToast()
const farms = ref([])
const form = reactive({
  farmId: '',
  fieldId: '',
  farmName: '',
  fieldName: '',
  guidanceType: '',
  personId: '',
  personName: '张三',
  problem: '',
  recordId: '',
})

const selectedFarm = computed(() => farms.value.find(f => f.id == form.farmId))
const availableFields = computed(() => selectedFarm.value?.fields || [])
const selectedField = computed(() => availableFields.value.find(f => f.id == form.fieldId))

function onFarmChange() {
  form.fieldId = ''
  form.fieldName = ''
  form.farmName = selectedFarm.value?.name || ''
}

function onFieldChange() {
  form.fieldName = selectedField.value?.name || ''
}

function onPersonChange() {
  const names = { 1: '张三', 2: '李农师', 3: '王技师', 4: '张专家' }
  form.personName = names[form.personId] || '张三'
}

async function submitInvite() {
  if (!form.farmId || !form.fieldId) {
    toast('请选择农场地块')
    return
  }
  if (!form.problem?.trim()) {
    toast('请填写问题描述')
    return
  }
  try {
    const { data } = await guidanceApi.create({
      farmId: Number(form.farmId),
      fieldId: Number(form.fieldId),
      farmName: form.farmName,
      fieldName: form.fieldName,
      guidanceType: form.guidanceType || '问题咨询',
      personId: form.personId,
      personName: form.personName,
      problem: form.problem,
      photos: [],
      recordId: form.recordId ? Number(form.recordId) : null,
    })
    toast('邀请已发送')
    router.push('/guidance')
  } catch (e) {
    toast(e?.response?.data?.detail || '发送失败')
  }
}

onMounted(async () => {
  const { data } = await farmsApi.list()
  farms.value = data || []
  if (farms.value.length) {
    form.farmId = farms.value[0].id
    form.farmName = farms.value[0].name
    if (farms.value[0].fields?.length) {
      form.fieldId = farms.value[0].fields[0].id
      form.fieldName = farms.value[0].fields[0].name
    }
  }
})
</script>

<style scoped>
.guidance-invite .page-body { padding: 16px; padding-bottom: 32px; }
.hdr-bar { display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: var(--primary-gradient); color: #FFF; }
.hdr-back { width: 36px; height: 36px; border: none; background: rgba(255,255,255,.2); color: #FFF; font-size: 24px; border-radius: 8px; cursor: pointer; }
.hdr-title { font-size: 18px; font-weight: 600; }
.form-section { margin-bottom: 20px; }
.section-title { font-size: 14px; font-weight: 600; margin-bottom: 10px; }
.form-row { display: flex; gap: 12px; }
.form-group { flex: 1; }
.form-group label { display: block; font-size: 12px; color: #666; margin-bottom: 4px; }
.form-select { width: 100%; padding: 10px; border: 1px solid #E0E0E0; border-radius: 8px; font-size: 14px; }
.plot-detail { background: var(--primary-dim); border: 1px solid var(--primary-border); border-radius: 12px; padding: 16px; margin-bottom: 20px; }
.detail-item { display: flex; justify-content: space-between; padding: 8px 0; font-size: 14px; }
.detail-item .label { color: #666; }
.form-textarea { width: 100%; padding: 12px; border: 1px solid #E0E0E0; border-radius: 8px; font-size: 14px; resize: vertical; }
.upload-area { border: 2px dashed #E0E0E0; border-radius: 12px; padding: 40px; text-align: center; cursor: pointer; background: #FAFAFA; }
.upload-icon { font-size: 48px; color: #9E9E9E; display: block; margin-bottom: 8px; }
.upload-text { font-size: 14px; color: #666; margin-bottom: 4px; }
.upload-hint { font-size: 12px; color: #999; }
.form-actions { display: flex; gap: 12px; margin-top: 24px; }
.btn-cancel { flex: 1; padding: 14px; background: #F5F5F5; color: #666; border: none; border-radius: 12px; font-size: 16px; cursor: pointer; }
.btn-submit { flex: 1; padding: 14px; background: var(--primary-gradient); color: #FFF; border: none; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; }
</style>
