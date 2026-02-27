<template>
  <div class="page demand-publish">
    <div class="hdr-title-bar"><button class="hdr-back" @click="$router.back()">‹</button>需求发布页-无人机巡田监测</div>
    <div class="hdr-banner">
      <span class="banner-icon">⚡</span>
      <span class="banner-title">发布巡田需求</span>
    </div>

    <div class="page-body">
      <div class="section">
        <div class="section-title">选择服务地块</div>
        <div class="form-group"><label>请选择农场</label><select v-model="form.farmId" class="form-select" @change="onFarmChange"><option value="">请选择农场</option><option v-for="f in farms" :key="f.id" :value="f.id">{{ f.name }}</option></select></div>
        <div class="form-group"><label>请选择地块</label><div class="field-list"><label v-for="f in availableFields" :key="f.id" class="field-check"><input type="checkbox" :value="f.id" v-model="form.fieldIds" /><span>{{ f.name }}</span></label></div></div>
        <div class="form-group"><label class="checkbox-label"><input v-model="form.selectAll" type="checkbox" /> 全选当前农场</label></div>
      </div>

      <div class="section">
        <div class="section-title">设置作业要求</div>
        <div class="form-row-2">
          <div class="form-group"><label>期望作业开始时间</label><input v-model="form.startDate" type="date" class="form-input" /></div>
          <div class="form-group"><label>时间</label><input v-model="form.startTime" type="time" class="form-input" /></div>
        </div>
        <div class="form-group"><label>服务周期*</label><div class="radio-row"><label><input v-model="form.period" type="radio" value="single" /> 单次</label><label><input v-model="form.period" type="radio" value="monthly" /> 月度</label></div></div>
        <div v-if="form.period === 'monthly'" class="form-group"><label>作业次数</label><input v-model.number="form.opCount" type="number" class="form-input" placeholder="每月次数" /></div>
        <p class="form-hint">如需多次作业,请选择月度并填写每月次数。</p>
      </div>

      <div class="section">
        <div class="section-title">需求描述</div>
        <textarea v-model="form.desc" class="form-textarea" placeholder="请描述您的具体监测需求,例如关注作物长势、病虫早期发现等" rows="4"></textarea>
      </div>

      <div class="section">
        <div class="section-title">预算与备注</div>
        <div class="form-group"><label>预期总价 (元)</label><input v-model.number="form.budget" type="number" class="form-input" /></div>
        <div class="form-group"><label>结算方式</label><div class="radio-row"><label><input v-model="form.settlement" type="radio" value="yearend" /> 年底结算 (12月31日统一结算)</label></div><div class="radio-row"><label><input v-model="form.settlement" type="radio" value="spot" /> 现结 (订单完成并验收后7天内支付)</label></div></div>
        <p class="form-hint">年底结算:当年12月31日完成付款。现结:订单完成并验收后7天内支付。支付比例:线上仅支付20%至服务商,剩余80%线下自行结算。</p>
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
  fieldIds: [],
  selectAll: false,
  startDate: '',
  startTime: '09:00',
  period: 'single',
  opCount: 1,
  desc: '',
  budget: null,
  settlement: 'spot',
  notes: '',
})

const availableFields = computed(() => {
  const farm = farms.value.find(f => f.id == form.farmId)
  return farm?.fields || []
})

watch(() => form.selectAll, (v) => {
  if (v) form.fieldIds = availableFields.value.map(f => f.id)
  else form.fieldIds = []
})

watch(() => form.farmId, () => {
  form.selectAll = false
  form.fieldIds = []
})

function onFarmChange() {
  form.fieldIds = []
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
  if (!form.fieldIds?.length && !form.selectAll) { toast('请选择地块'); return }
  toast('发布成功 ✓')
  router.push('/machinery/demands')
}
</script>

<style scoped>
.demand-publish .page-body { padding: 16px; padding-bottom: 32px; }
.hdr-title-bar { display: flex; align-items: center; gap: 12px; padding: 10px 16px; background: #F5F5F5; font-size: 14px; color: #666; }
.hdr-back { width: 32px; height: 32px; border: none; background: var(--primary-dim); color: var(--primary); font-size: 22px; border-radius: 8px; cursor: pointer; }
.hdr-banner { display: flex; align-items: center; gap: 10px; padding: 14px 16px; background: linear-gradient(135deg, var(--primary), #388E3C); color: #FFF; }
.banner-icon { font-size: 18px; }
.banner-title { font-size: 16px; font-weight: 600; }
.section { margin-bottom: 24px; }
.section-title { font-size: 15px; font-weight: 600; color: #1B2E1B; margin-bottom: 12px; }
.form-group { margin-bottom: 14px; }
.form-group label { display: block; font-size: 13px; color: var(--text2); margin-bottom: 6px; }
.form-label-row { display: flex; gap: 16px; }
.checkbox-label { display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 14px; color: var(--primary); }
.form-select, .form-input { width: 100%; padding: 12px 14px; background: #F7FAF7; border: 1.5px solid rgba(46,125,50,.2); border-radius: 10px; font-size: 14px; box-sizing: border-box; }
.form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.form-textarea { width: 100%; padding: 12px 14px; background: #F7FAF7; border: 1.5px solid rgba(46,125,50,.2); border-radius: 10px; font-size: 14px; resize: vertical; box-sizing: border-box; }
.radio-row { margin-bottom: 8px; }
.radio-row label { display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 14px; color: #1B2E1B; }
.form-hint { font-size: 12px; color: #9DB89C; margin-top: 6px; line-height: 1.5; }
.btn-submit { width: 100%; padding: 14px; background: var(--primary); color: #FFF; border: none; border-radius: 10px; font-size: 16px; font-weight: 600; cursor: pointer; margin-top: 8px; }
.submit-hint { font-size: 12px; color: #9DB89C; margin-top: 10px; text-align: center; }
.field-list { display: flex; flex-direction: column; gap: 8px; max-height: 120px; overflow-y: auto; }
.field-check { display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 14px; color: #1B2E1B; }
</style>
