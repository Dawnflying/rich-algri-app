<template>
  <div class="page farm-create">
    <div class="hdr farm-hdr">
      <button class="hdr-back" @click="$router.back()">‹</button>
      <div class="hdr-banner">
        <span class="banner-icon">⚡</span>
        <span class="banner-title">创建农场</span>
      </div>
    </div>

    <div class="page-body">
      <!-- 所属地区 -->
      <div class="form-group">
        <label class="form-label">所属地区</label>
        <div class="region-row">
          <select v-model="form.province" class="form-select" @change="onProvinceChange">
            <option value="">请选择省/自治区</option>
            <option v-for="p in provinces" :key="p" :value="p">{{ p }}</option>
          </select>
          <select v-model="form.city" class="form-select" @change="onCityChange">
            <option value="">请选择市</option>
            <option v-for="c in cities" :key="c" :value="c">{{ c }}</option>
          </select>
          <select v-model="form.county" class="form-select" @change="onCountyChange">
            <option value="">请选择县/区</option>
            <option v-for="ct in counties" :key="ct" :value="ct">{{ ct }}</option>
          </select>
          <select v-model="form.town" class="form-select">
            <option value="">请选择乡镇/街道</option>
            <option v-for="t in towns" :key="t" :value="t">{{ t }}</option>
          </select>
        </div>
      </div>

      <!-- 是否属于企业 -->
      <div class="form-group">
        <label class="form-label">是否属于企业</label>
        <div class="toggle-row">
          <button type="button" class="toggle-btn" :class="{ active: form.isEnterprise }" @click="form.isEnterprise = true">是</button>
          <button type="button" class="toggle-btn" :class="{ active: !form.isEnterprise }" @click="form.isEnterprise = false">否</button>
        </div>
      </div>

      <!-- 企业信息 -->
      <div v-if="form.isEnterprise" class="form-group enterprise-block">
        <div class="form-row">
          <label class="form-label">企业名称</label>
          <input v-model="form.enterpriseName" type="text" class="form-input" placeholder="请输入企业名称" />
        </div>
        <div class="form-row">
          <label class="form-label">企业地址</label>
          <input v-model="form.enterpriseAddress" type="text" class="form-input" placeholder="请输入企业地址" />
        </div>
        <div class="form-row">
          <label class="form-label">联系人</label>
          <input v-model="form.contact" type="text" class="form-input" placeholder="请输入联系人姓名" />
        </div>
        <div class="form-row">
          <label class="form-label">联系电话</label>
          <input v-model="form.phone" type="text" class="form-input" placeholder="请输入联系电话" />
        </div>
      </div>

      <!-- 农场名称 -->
      <div class="form-group">
        <label class="form-label">农场名称 <span class="required">*</span></label>
        <input v-model="form.name" type="text" class="form-input" :class="{ error: showNameError }" placeholder="请输入农场名称" />
        <p v-if="showNameError" class="form-error">请输入农场名称</p>
      </div>

      <!-- 底部按钮 -->
      <div class="form-actions">
        <button type="button" class="btn-cancel" @click="$router.back()">取消</button>
        <button type="button" class="btn-confirm" :class="{ enabled: form.name.trim() }" :disabled="!form.name.trim()" @click="submit">确认创建</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { farmsApi } from '../api'
import { useToast } from '../composables/useToast'

const router = useRouter()
const { toast } = useToast()

const regionData = {
  新疆维吾尔自治区: {
    哈密市: { 巴里坤哈萨克自治县: ['哈穆尔镇', '其他镇'], 伊州区: ['东河街道', '西河街道'] },
    石河子市: { 石河子市: ['北泉镇', '石河子镇'] },
    乌鲁木齐市: { 天山区: ['东门街道', '西门街道'], 水磨沟区: ['水磨沟街道'] },
  },
  内蒙古自治区: {
    呼和浩特市: { 新城区: ['东街街道', '西街街道'] },
  },
}

const provinces = Object.keys(regionData)

const form = reactive({
  province: '',
  city: '',
  county: '',
  town: '',
  isEnterprise: false,
  enterpriseName: '',
  enterpriseAddress: '',
  contact: '',
  phone: '',
  name: '',
})

const cities = computed(() => {
  if (!form.province) return []
  return Object.keys(regionData[form.province] || {})
})

const counties = computed(() => {
  if (!form.province || !form.city) return []
  const p = regionData[form.province]
  if (!p) return []
  return Object.keys(p[form.city] || {})
})

const towns = computed(() => {
  if (!form.province || !form.city || !form.county) return []
  const p = regionData[form.province]
  if (!p || !p[form.city]) return []
  return p[form.city][form.county] || []
})

function onProvinceChange() {
  form.city = ''
  form.county = ''
  form.town = ''
}
function onCityChange() {
  form.county = ''
  form.town = ''
}
function onCountyChange() {
  form.town = ''
}

const showNameError = ref(false)

async function submit() {
  if (!form.name.trim()) {
    showNameError.value = true
    return
  }
  showNameError.value = false
  try {
    const { data } = await farmsApi.create({
      province: form.province,
      city: form.city,
      county: form.county,
      town: form.town,
      isEnterprise: form.isEnterprise,
      enterpriseName: form.enterpriseName,
      enterpriseAddress: form.enterpriseAddress,
      contact: form.contact,
      phone: form.phone,
      name: form.name.trim(),
    })
    if (data.success) {
      toast('创建成功 ✓')
      router.push(`/farm/${data.farm.id}`)
    } else {
      toast(data.message || '创建失败')
    }
  } catch (e) {
    toast('创建失败')
  }
}
</script>

<style scoped>
.farm-create .page-body { padding: 16px; padding-bottom: 32px; }
.farm-hdr {
  display: flex; align-items: center; padding: 12px 16px;
  background: #FFF; border-bottom: 1px solid rgba(46,125,50,.1);
}
.hdr-back {
  width: 36px; height: 36px; border: none; background: rgba(46,125,50,.1);
  color: var(--primary); font-size: 24px; border-radius: 8px; cursor: pointer; flex-shrink: 0;
}
.hdr-banner {
  flex: 1; display: flex; align-items: center; justify-content: center; gap: 8px;
  background: linear-gradient(135deg, var(--primary), var(--primary-light)); color: #FFF;
  padding: 12px 20px; border-radius: 10px; margin-left: 12px;
}
.banner-icon { font-size: 18px; }
.banner-title { font-size: 16px; font-weight: 600; }
.form-group { margin-bottom: 20px; }
.form-label { display: block; font-size: 14px; color: #1B2E1B; margin-bottom: 8px; font-weight: 500; }
.form-label .required { color: var(--red); }
.region-row { display: flex; flex-direction: column; gap: 10px; }
.form-select {
  width: 100%; padding: 12px 14px; background: #F7FAF7;
  border: 1.5px solid rgba(46,125,50,.2); border-radius: 10px;
  font-size: 14px; color: #1B2E1B;
}
.toggle-row { display: flex; gap: 12px; }
.toggle-btn {
  flex: 1; padding: 12px; border: 1.5px solid rgba(46,125,50,.25);
  background: #FFF; color: var(--text2); border-radius: 10px; font-size: 14px; cursor: pointer;
}
.toggle-btn.active { background: var(--primary); color: #FFF; border-color: var(--primary); }
.enterprise-block .form-row { margin-bottom: 14px; }
.enterprise-block .form-row:last-child { margin-bottom: 0; }
.form-input {
  width: 100%; padding: 12px 14px; background: #F7FAF7;
  border: 1.5px solid rgba(46,125,50,.2); border-radius: 10px;
  font-size: 14px; color: #1B2E1B; box-sizing: border-box;
}
.form-input.error { border-color: var(--red); }
.form-input::placeholder { color: #9DB89C; }
.form-error { font-size: 12px; color: var(--red); margin-top: 6px; }
.form-actions {
  display: flex; gap: 12px; margin-top: 28px; padding-top: 20px;
}
.btn-cancel, .btn-confirm {
  flex: 1; padding: 14px; border: none; border-radius: 10px;
  font-size: 15px; font-weight: 500; cursor: pointer;
}
.btn-cancel { background: #F0F0F0; color: #666; }
.btn-confirm { background: #E0E0E0; color: #999; }
.btn-confirm.enabled { background: var(--primary); color: #FFF; }
</style>
