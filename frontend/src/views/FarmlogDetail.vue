<template>
  <div class="page farmlog-detail">
    <div class="hdr-title-bar">农事记录详情页</div>
    <div class="hdr-banner">
      <button class="hdr-back" @click="$router.back()">‹</button>
      <div class="hdr-left">
        <span class="hdr-icon">⚡</span>
        <span class="hdr-label">记录详情</span>
      </div>
      <div class="hdr-actions">
        <span class="hdr-action" @click="toast('导出')">导出</span>
        <span class="hdr-action" @click="toast('更多')">⋮</span>
      </div>
    </div>

    <div class="page-body" v-if="record">
      <!-- 基本信息 -->
      <div class="info-section">
        <div class="info-row"><span class="info-icon">📅</span><span>{{ record.date }} {{ record.time || '' }}</span></div>
        <div class="info-row"><span class="info-icon">📍</span><span>地块: {{ record.fieldName }} ({{ record.farm }})</span></div>
        <div class="info-row"><span class="info-icon">🌱</span><span>类型: {{ FL_TYPE_MAP[record.type]?.label }}</span></div>
        <div class="info-row"><span class="info-icon">👤</span><span>记录人: {{ record.recorder }}</span></div>
      </div>

      <!-- 观察点详情（日生长量） -->
      <div v-if="record.type === 'growth' && record.data?.points?.length" class="obs-section">
        <div v-for="(p, i) in record.data.points" :key="i" class="obs-point">
          <div class="obs-title">观察点{{ p.no }}: {{ p.area || '区域' + (i+1) }}</div>
          <div class="obs-grid">
            <div class="obs-item"><span class="obs-label">株高 (厘米)</span><span class="obs-val">{{ p.height }}</span></div>
            <div class="obs-item"><span class="obs-label">日生长量 (厘米)</span><span class="obs-val">{{ p.growth }}</span></div>
            <div class="obs-item"><span class="obs-label">叶数 (片)</span><span class="obs-val">{{ p.leaves }}</span></div>
            <div class="obs-item"><span class="obs-label">苔数 (苔)</span><span class="obs-val">{{ p.stems }}</span></div>
          </div>
        </div>
      </div>

      <!-- 其他类型详情 -->
      <div v-else-if="record.type === 'water'" class="detail-section">
        <div v-for="f in (record.data?.fertilizers || [])" :key="f.no" class="detail-block">
          <div class="detail-row">化肥名称: {{ f.name }} 亩用量: {{ f.amount }}公斤 氮含量N: {{ f.N }}%</div>
        </div>
        <div v-if="record.data?.waterAmt" class="detail-row">用水量: {{ record.data.waterAmt }}立方米</div>
      </div>
      <div v-else-if="record.type === 'pest'" class="detail-section">
        <div v-for="p in (record.data?.pesticides || [])" :key="p.no" class="detail-block">
          <div class="detail-row">农药名称: {{ p.name }} 作用: {{ p.effect }} 用量: {{ p.amount }}</div>
        </div>
      </div>
      <div v-else-if="record.type === 'diary'" class="detail-section">
        <div class="detail-content">{{ record.data?.content }}</div>
      </div>
      <div v-else-if="record.type === 'issue'" class="detail-section">
        <div class="detail-content">{{ record.data?.desc }}</div>
      </div>

      <!-- 照片 -->
      <div v-if="record.photos?.length" class="photo-section">
        <div class="photo-title">📷 照片 ({{ record.photos.length }}张)</div>
        <div class="photo-grid">
          <div v-for="(p, i) in record.photos" :key="i" class="photo-item">
            <div class="photo-placeholder">{{ typeof p === 'string' && p.startsWith('img') ? '🖼️' : p }}</div>
          </div>
        </div>
      </div>

      <!-- 备注 -->
      <div v-if="record.notes" class="remarks-section">
        <div class="remarks-label">备注:</div>
        <div class="remarks-content">{{ record.notes }}</div>
      </div>

      <!-- 底部操作 -->
      <div class="bottom-actions">
        <button class="btn-edit" @click="toast('编辑功能开发中')">✓ 编辑记录</button>
        <button class="btn-delete" @click="onDelete">🗑️ 删除记录</button>
      </div>
    </div>
    <div v-else-if="loading" class="loading">加载中...</div>
    <div v-else class="loading">记录不存在</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { farmlogApi } from '../api'
import { useToast } from '../composables/useToast'

const route = useRoute()
const router = useRouter()
const { toast } = useToast()
const record = ref(null)
const loading = ref(true)

const FL_TYPE_MAP = {
  diary: { label: '记事' },
  growth: { label: '日生长量' },
  pest: { label: '农药使用' },
  water: { label: '水肥使用' },
  issue: { label: '田间问题' },
}

async function onDelete() {
  if (!confirm('确定要删除此记录吗？')) return
  try {
    await farmlogApi.delete(record.value.id)
    toast('已删除')
    router.back()
  } catch (e) {
    toast('删除失败')
  }
}

onMounted(async () => {
  const id = route.params.id
  try {
    const { data } = await farmlogApi.get(id)
    record.value = data
  } catch (_) {
    record.value = null
  }
  loading.value = false
})
</script>

<style scoped>
.farmlog-detail .page-body { padding: 16px; padding-bottom: 100px; }
.hdr-title-bar { padding: 10px 16px; background: #F5F5F5; font-size: 14px; color: #666; }
.hdr-banner {
  display: flex; align-items: center; padding: 12px 16px;
  background: linear-gradient(135deg, var(--primary), #388E3C); color: #FFF;
}
.hdr-back {
  width: 36px; height: 36px; border: none; background: rgba(255,255,255,.2);
  color: #FFF; font-size: 24px; border-radius: 8px; cursor: pointer; flex-shrink: 0;
}
.hdr-left { flex: 1; display: flex; align-items: center; gap: 8px; margin-left: 12px; }
.hdr-icon { font-size: 16px; }
.hdr-actions { flex-shrink: 0; }
.hdr-label { font-size: 16px; font-weight: 600; }
.hdr-actions { display: flex; gap: 16px; }
.hdr-action { cursor: pointer; font-size: 14px; opacity: .95; }
.info-section { margin-bottom: 20px; }
.info-row { display: flex; align-items: flex-start; gap: 10px; padding: 10px 0; font-size: 14px; color: #1B2E1B; }
.info-icon { font-size: 16px; flex-shrink: 0; }
.obs-section { margin-bottom: 20px; }
.obs-point { margin-bottom: 16px; padding: 14px; background: #F7FAF7; border-radius: 10px; }
.obs-title { font-size: 14px; font-weight: 600; color: #1B2E1B; margin-bottom: 10px; }
.obs-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px 16px; }
.obs-item { display: flex; flex-direction: column; gap: 2px; }
.obs-label { font-size: 12px; color: var(--text2); }
.obs-val { font-size: 14px; font-weight: 500; color: #1B2E1B; }
.detail-section { margin-bottom: 20px; padding: 14px; background: #F7FAF7; border-radius: 10px; }
.detail-row, .detail-content { font-size: 14px; color: #1B2E1B; line-height: 1.6; }
.detail-block { margin-bottom: 8px; }
.photo-section { margin-bottom: 20px; }
.photo-title { font-size: 14px; font-weight: 600; color: #1B2E1B; margin-bottom: 10px; }
.photo-grid { display: flex; gap: 10px; flex-wrap: wrap; }
.photo-item { width: 80px; height: 80px; }
.photo-placeholder { width: 100%; height: 100%; background: #E8E8E8; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 24px; }
.remarks-section { margin-bottom: 24px; }
.remarks-label { font-size: 14px; font-weight: 500; color: #1B2E1B; margin-bottom: 6px; }
.remarks-content { font-size: 14px; color: #666; line-height: 1.6; }
.bottom-actions { position: fixed; bottom: 0; left: 0; right: 0; display: flex; gap: 12px; padding: 12px 16px; background: #FFF; border-top: 1px solid #EEE; }
.btn-edit, .btn-delete { flex: 1; padding: 14px; border: none; border-radius: 10px; font-size: 15px; font-weight: 500; cursor: pointer; }
.btn-edit { background: var(--primary); color: #FFF; }
.btn-delete { background: var(--red); color: #FFF; }
.loading { padding: 48px; text-align: center; color: #9DB89C; }
</style>
