<template>
  <div class="page farm-detail">
    <div class="hdr farm-hdr">
      <button class="hdr-back" @click="$router.back()">‹</button>
      <div class="hdr-banner">
        <span class="banner-icon">⚡</span>
        <span class="banner-title">{{ farm?.name || '加载中...' }}</span>
      </div>
      <span class="hdr-edit" @click="toast('编辑农场')">✎</span>
    </div>

    <div class="page-body" v-if="farm">
      <!-- 农场概览 -->
      <div class="overview-card">
        <div class="overview-hd">
          <span class="overview-title">农场概览</span>
          <span class="overview-tag">{{ farm.cropType || '棉花农场' }}</span>
        </div>
        <div class="overview-info">
          <div class="info-row"><span class="info-label">农场名称</span><span class="info-val">{{ farm.name }}</span></div>
          <div class="info-row"><span class="info-label">所属地区</span><span class="info-val">{{ farm.region }}</span></div>
          <div class="info-row"><span class="info-label">企业信息</span><span class="info-val">{{ farm.isEnterprise ? '是' : '否' }}</span></div>
        </div>
        <div class="overview-stats">
          <div class="stat-item"><span class="stat-val">{{ farm.fieldCount || 0 }}</span><span class="stat-label">地块数</span></div>
          <div class="stat-item"><span class="stat-val">{{ farm.totalArea || 0 }}亩</span><span class="stat-label">种植面积</span></div>
          <div class="stat-item"><span class="stat-val">{{ farm.cropVariety || 0 }}</span><span class="stat-label">作物种类</span></div>
        </div>
        <div class="map-placeholder">
          <span class="map-icon">📍</span>
          <span class="map-text">位置: {{ farm.location }}</span>
        </div>
        <div class="overview-actions">
          <button class="btn-add-field" @click="$router.push('/field/edit?farmId=' + farm.id)">+ 添加地块</button>
          <button class="btn-share" @click="toast('分享')">分享</button>
        </div>
      </div>

      <!-- 全部地块 -->
      <div class="fields-sec">
        <div class="sec-title">全部地块</div>
        <div class="field-list">
          <div v-for="f in displayFields" :key="f.id" class="field-item" @click="$router.push('/field/' + f.id)">
            <div class="field-item-left">
              <div class="field-item-name">{{ f.name }}</div>
              <div class="field-item-meta">面积: {{ f.area }}亩</div>
            </div>
            <div class="field-item-right">
              <div class="field-item-date">{{ f.updatedAt }} 更新</div>
              <div class="field-item-crop">作物:{{ f.crop }}</div>
            </div>
          </div>
        </div>
        <button v-if="farm.fields?.length > 3" class="btn-expand" @click="expanded = !expanded">
          <span class="expand-icon">≡</span> {{ expanded ? '收起' : '全部展开' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { farmsApi } from '../api'
import { useToast } from '../composables/useToast'

const route = useRoute()
const { toast } = useToast()
const farm = ref(null)
const expanded = ref(false)

const displayFields = computed(() => {
  const list = farm.value?.fields || []
  if (!expanded.value && list.length > 3) return list.slice(0, 3)
  return list
})

onMounted(async () => {
  const id = route.params.id
  if (!id) return
  try {
    const { data } = await farmsApi.get(id)
    farm.value = data
  } catch (e) {
    toast('加载失败')
  }
})
</script>

<style scoped>
.farm-detail .page-body { padding: 16px; padding-bottom: 32px; }
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
  padding: 12px 20px; border-radius: 10px; margin: 0 12px;
}
.banner-icon { font-size: 18px; }
.banner-title { font-size: 16px; font-weight: 600; }
.hdr-edit { font-size: 20px; color: var(--primary); cursor: pointer; padding: 4px; }
.overview-card {
  background: #FFF; border: 1px solid rgba(46,125,50,.1); border-radius: 12px;
  padding: 16px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(46,125,50,.06);
}
.overview-hd { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
.overview-title { font-size: 16px; font-weight: 600; color: #1B2E1B; }
.overview-tag { background: var(--primary); color: #FFF; padding: 4px 12px; border-radius: 20px; font-size: 12px; }
.overview-info { margin-bottom: 14px; }
.info-row { display: flex; justify-content: space-between; padding: 8px 0; font-size: 14px; }
.info-label { color: #5A7A5A; }
.info-val { color: #1B2E1B; font-weight: 500; }
.overview-stats {
  display: flex; gap: 16px; padding: 14px 0; border-top: 1px solid rgba(46,125,50,.08);
  border-bottom: 1px solid rgba(46,125,50,.08); margin-bottom: 14px;
}
.stat-item { flex: 1; text-align: center; }
.stat-val { display: block; font-size: 18px; font-weight: 600; color: var(--primary); }
.stat-label { font-size: 12px; color: #5A7A5A; margin-top: 4px; }
.map-placeholder {
  background: #F7FAF7; border-radius: 10px; padding: 24px;
  display: flex; flex-direction: column; align-items: center; gap: 8px; margin-bottom: 14px;
}
.map-icon { font-size: 28px; }
.map-text { font-size: 13px; color: #5A7A5A; }
.overview-actions { display: flex; gap: 12px; }
.btn-add-field { flex: 1; padding: 12px; background: var(--primary); color: #FFF; border: none; border-radius: 10px; font-size: 14px; cursor: pointer; }
.btn-share { padding: 12px 20px; background: #F0F0F0; color: #666; border: none; border-radius: 10px; font-size: 14px; cursor: pointer; }
.fields-sec { margin-bottom: 20px; }
.sec-title { font-size: 16px; font-weight: 600; color: #1B2E1B; margin-bottom: 12px; }
.field-list { display: flex; flex-direction: column; gap: 10px; }
.field-item {
  display: flex; justify-content: space-between; align-items: flex-start;
  padding: 14px; background: #FFF; border: 1px solid rgba(46,125,50,.1);
  border-radius: 10px; box-shadow: 0 1px 4px rgba(46,125,50,.04);
  cursor: pointer;
}
.field-item-left { flex: 1; }
.field-item-name { font-size: 14px; font-weight: 600; color: #1B2E1B; margin-bottom: 4px; }
.field-item-meta { font-size: 12px; color: #5A7A5A; }
.field-item-right { text-align: right; }
.field-item-date { font-size: 12px; color: #9DB89C; margin-bottom: 4px; }
.field-item-crop { font-size: 12px; color: #5A7A5A; }
.btn-expand {
  width: 100%; margin-top: 12px; padding: 12px;
  background: transparent; color: var(--primary); border: 1px dashed var(--primary-border);
  border-radius: 10px; font-size: 14px; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px;
}
.expand-icon { font-size: 16px; }
</style>
