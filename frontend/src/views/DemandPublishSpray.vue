<template>
  <div class="page demand-publish">
    <div class="hdr-title-bar"><button class="hdr-back" @click="$router.back()">‹</button>需求发布页-无人机植保打药</div>
    <div class="hdr-banner">
      <span class="banner-icon">⚡</span>
      <span class="banner-title">发布植保打药需求</span>
    </div>

    <div class="page-body">
      <div class="section">
        <div class="section-title">选择服务地块</div>
        <div class="form-group"><label>请选择农场</label><select v-model="form.farmId" class="form-select" @change="onFarmChange"><option value="">请选择农场</option><option v-for="f in farms" :key="f.id" :value="f.id">{{ f.name }}</option></select></div>
        <div class="form-group"><label>请选择地块</label><select v-model="form.fieldId" class="form-select"><option value="">请选择地块</option><option v-for="f in availableFields" :key="f.id" :value="f.id">{{ f.name }}</option></select></div>
        <div class="form-group"><label class="checkbox-label"><input v-model="form.selectAll" type="checkbox" /> 全选当前农场</label></div>
      </div>

      <div class="section">
        <div class="section-title">作业要求</div>
        <div class="form-group"><label>请描述病虫害情况或作业目标</label><textarea v-model="form.target" class="form-textarea" placeholder="请描述病虫害情况或作业目标" rows="4"></textarea></div>
      </div>

      <div class="section">
        <div class="section-title">作业参数</div>
        <div class="form-group"><label>药剂 (选填)</label><input v-model="form.pesticide" type="text" class="form-input" placeholder="请输入使用的药剂" /></div>
        <div class="form-group"><label>药剂图片 (选填)</label><div class="photo-upload" @click="toast('拍照上传')"><span class="photo-icon">📷</span>拍照上传<br><span class="photo-hint">拍摄药剂瓶身包装</span></div></div>
        <div class="form-row-2">
          <div class="form-group"><label>每用量 (选填)</label><input v-model="form.dosage" type="number" class="form-input" /></div>
          <div class="form-group"><label>单位</label><select v-model="form.dosageUnit" class="form-select"><option value="ml">毫升</option><option value="g">克</option></select></div>
        </div>
        <div class="form-group"><label>作业标准/要求 (选填)</label><textarea v-model="form.standard" class="form-textarea" placeholder="例如:防治椿象虫,建议使用XX药剂,每用量50毫升,要求飞助作业。" rows="3"></textarea></div>
      </div>

      <div class="section">
        <div class="section-title">时间与预算</div>
        <div class="form-row-2">
          <div class="form-group"><label>期望作业开始时间</label><input v-model="form.startDate" type="date" class="form-input" /></div>
          <div class="form-group"><label>时间</label><input v-model="form.startTime" type="time" class="form-input" /></div>
        </div>
        <div class="form-group"><label>预期单价 [元/亩]</label><input v-model.number="form.unitPrice" type="number" class="form-input" /></div>
        <div class="form-group"><label>结算方式</label><div class="radio-row"><label><input v-model="form.settlement" type="radio" value="yearend" /> 年底结算 (12月31日统一结算)</label></div><div class="radio-row"><label><input v-model="form.settlement" type="radio" value="spot" /> 现结 (订单完成并验收后7天内支付)</label></div></div>
        <p class="form-hint">支付比例: 线上仅支付20%至服务商,剩余80%请线下自行结算。</p>
      </div>

      <div class="section">
        <div class="form-group"><label>备注</label><textarea v-model="form.notes" class="form-textarea" placeholder="请填写其他需要说明的事项,如飞行高度" rows="3"></textarea></div>
      </div>

      <button class="btn-submit" @click="submit">📤 发布需求</button>
      <p class="submit-hint">发布后,需求将进入市场,服务商可进行报价</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { farmsApi } from '../api'
import { useToast } from '../composables/useToast'

const router = useRouter()
const { toast } = useToast()
const farms = ref([])

const form = reactive({
  farmId: '',
  fieldId: '',
  selectAll: false,
  target: '',
  pesticide: '',
  dosage: null,
  dosageUnit: 'ml',
  standard: '',
  startDate: '',
  startTime: '09:00',
  unitPrice: null,
  settlement: 'spot',
  notes: '',
})

const availableFields = computed(() => {
  const farm = farms.value.find(f => f.id == form.farmId)
  return farm?.fields || []
})

watch(() => form.selectAll, (v) => {
  if (v && availableFields.value.length) form.fieldId = availableFields.value[0].id
})

watch(() => form.farmId, () => {
  form.selectAll = false
  form.fieldId = ''
})

function onFarmChange() {
  form.fieldId = ''
  form.selectAll = false
}

onMounted(async () => {
  const { data } = await farmsApi.list()
  farms.value = data || []
  const d = new Date()
  form.startDate = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
})

function submit() {
  if (!form.farmId) { toast('请选择农场'); return }
  if (!form.fieldId && !form.selectAll) { toast('请选择地块'); return }
  toast('发布成功 ✓')
  router.push('/machinery/demands')
}
</script>

<style scoped>
.demand-publish .page-body { padding: 16px; padding-bottom: 32px; }
.hdr-title-bar { display: flex; align-items: center; gap: 12px; padding: 10px 16px; background: #F5F5F5; font-size: 14px; color: #666; }
.hdr-back { width: 32px; height: 32px; border: none; background: var(--primary-dim); color: var(--primary); font-size: 22px; border-radius: 8px; cursor: pointer; }
.hdr-banner { display: flex; align-items: center; gap: 10px; padding: 14px 16px; background: linear-gradient(135deg, var(--primary), var(--primary-light)); color: #FFF; }
.banner-icon { font-size: 18px; }
.banner-title { font-size: 16px; font-weight: 600; }
.section { margin-bottom: 24px; }
.section-title { font-size: 15px; font-weight: 600; color: #1B2E1B; margin-bottom: 12px; }
.form-group { margin-bottom: 14px; }
.form-group label { display: block; font-size: 13px; color: var(--text2); margin-bottom: 6px; }
.checkbox-label { display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 14px; color: var(--primary); }
.form-select, .form-input { width: 100%; padding: 12px 14px; background: #F7FAF7; border: 1.5px solid rgba(46,125,50,.2); border-radius: 10px; font-size: 14px; box-sizing: border-box; }
.form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.form-textarea { width: 100%; padding: 12px 14px; background: #F7FAF7; border: 1.5px solid rgba(46,125,50,.2); border-radius: 10px; font-size: 14px; resize: vertical; box-sizing: border-box; }
.photo-upload { padding: 24px; background: #F0F0F0; border: 2px dashed rgba(46,125,50,.3); border-radius: 10px; text-align: center; cursor: pointer; }
.photo-icon { font-size: 28px; display: block; margin-bottom: 8px; }
.photo-hint { font-size: 12px; color: #9DB89C; }
.radio-row { margin-bottom: 8px; }
.radio-row label { display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 14px; color: #1B2E1B; }
.form-hint { font-size: 12px; color: #9DB89C; margin-top: 6px; line-height: 1.5; }
.btn-submit { width: 100%; padding: 14px; background: var(--primary); color: #FFF; border: none; border-radius: 10px; font-size: 16px; font-weight: 600; cursor: pointer; margin-top: 8px; }
.submit-hint { font-size: 12px; color: #9DB89C; margin-top: 10px; text-align: center; }
</style>
