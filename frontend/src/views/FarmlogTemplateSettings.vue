<template>
  <div class="page template-settings">
    <div class="hdr-title-bar">常用模板设置页</div>
    <div class="hdr-banner">
      <button class="hdr-back" @click="$router.back()">‹</button>
      <span class="hdr-title">常用模板设置</span>
    </div>

    <div class="page-body">
      <p class="instruction">请选择要使用的记录模板: (取消勾选的模板在记录时将不会出现)</p>

      <div class="template-list">
        <div v-for="(t, key) in templates" :key="key" class="template-item">
          <label class="template-check">
            <input v-model="templates[key].enabled" type="checkbox" />
            <span class="template-icon">{{ t.icon }}</span>
            <span class="template-name">{{ t.label }}</span>
          </label>
          <div class="template-indicators">
            <div class="indicators-label">包含指标:</div>
            <ul class="indicators-list">
              <li v-for="ind in templateIndicators[key]" :key="ind">{{ ind }}</li>
            </ul>
            <div v-if="key === 'growth'" class="template-note">(支持添加多个观测点)</div>
          </div>
        </div>
      </div>

      <div class="action-btns">
        <button class="btn-restore" @click="restoreDefault">
          <span class="btn-restore-icon">↻</span>
          恢复默认 (全选)
        </button>
        <button class="btn-save" @click="save">
          <span class="btn-save-icon">💾</span>
          保存设置
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useFarmlogTemplates } from '../composables/useFarmlogTemplates'
import { useToast } from '../composables/useToast'

const router = useRouter()
const { toast } = useToast()
const { load, save: saveTemplates } = useFarmlogTemplates()

const templates = ref({})

const templateIndicators = {
  growth: ['株高 (厘米)', '日生长量 (厘米)', '叶数 (片)', '苔数 (苔)'],
  water: ['化肥名称', '亩用量 (公斤)', '氮含量N (%)', '磷含量P (%)', '钾含量K (%)', '亩用水量'],
  pest: ['农药名称', '作用 (杀虫/杀菌/除草)', '用量 (g/亩或ml/亩)'],
  diary: ['记事内容'],
  issue: ['问题描述', '问题类型', '严重程度'],
}

function restoreDefault() {
  templates.value = load()
  Object.keys(templates.value).forEach(k => {
    templates.value[k].enabled = true
  })
}

function save() {
  saveTemplates(templates.value)
  toast('保存成功 ✓')
  router.back()
}

onMounted(() => {
  templates.value = JSON.parse(JSON.stringify(load()))
})
</script>

<style scoped>
.template-settings .page-body { padding: 16px; padding-bottom: 32px; }
.hdr-title-bar { padding: 10px 16px; background: #F5F5F5; font-size: 14px; color: #666; }
.hdr-banner {
  display: flex; align-items: center; padding: 12px 16px;
  background: linear-gradient(135deg, var(--primary), var(--primary-light)); color: #FFF;
}
.hdr-back {
  width: 36px; height: 36px; border: none; background: rgba(255,255,255,.2);
  color: #FFF; font-size: 24px; border-radius: 8px; cursor: pointer; flex-shrink: 0;
}
.hdr-title { flex: 1; font-size: 16px; font-weight: 600; margin-left: 12px; }
.instruction { font-size: 14px; color: #666; margin-bottom: 20px; line-height: 1.6; }
.template-list { display: flex; flex-direction: column; gap: 16px; margin-bottom: 24px; }
.template-item {
  padding: 16px; background: #FFF; border: 1px solid rgba(46,125,50,.1);
  border-radius: 12px; box-shadow: 0 2px 8px rgba(46,125,50,.06);
}
.template-check {
  display: flex; align-items: center; gap: 10px; cursor: pointer; margin-bottom: 12px;
}
.template-check input { width: 20px; height: 20px; accent-color: var(--primary); }
.template-icon { font-size: 20px; }
.template-name { font-size: 15px; font-weight: 600; color: #1B2E1B; }
.template-indicators { padding-left: 30px; }
.indicators-label { font-size: 13px; color: #5A7A5A; margin-bottom: 6px; }
.indicators-list { margin: 0; padding-left: 20px; font-size: 13px; color: #666; line-height: 1.8; }
.template-note { font-size: 12px; color: #9DB89C; margin-top: 6px; }
.action-btns { display: flex; gap: 12px; }
.btn-restore, .btn-save {
  flex: 1; padding: 14px; border: none; border-radius: 10px; font-size: 14px; font-weight: 500;
  cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px;
}
.btn-restore { background: #F0F0F0; color: #666; }
.btn-save { background: var(--primary); color: #FFF; }
.btn-restore-icon { font-size: 18px; }
.btn-save-icon { font-size: 16px; }
</style>
