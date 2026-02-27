<template>
  <div class="page">
    <div class="hdr"><div class="hdr-title">NDVI 植被分析</div><button class="hdr-action" @click="toast('导出报告')">📤</button></div>
    <div class="page-body">
      <div style="padding:12px 16px 0;display:flex;gap:8px">
        <div v-for="k in ['A','B','C','D']" :key="k" class="chip" :class="{ active: ndviField === k }" @click="ndviField = k; loadNdvi()">{{ k }}区</div>
      </div>
      <div class="sec" v-if="ndviData">
        <div class="card card-p">
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;text-align:center">
            <div><div class="stat-val" style="color:var(--primary)">{{ ndviData.avg }}</div><div class="stat-label">平均 NDVI</div></div>
            <div><div class="stat-val" style="color:#43A047">{{ ndviData.max }}</div><div class="stat-label">最高值</div></div>
            <div><div class="stat-val" style="color:var(--amber)">{{ ndviData.min }}</div><div class="stat-label">最低值</div></div>
          </div>
          <div style="margin-top:16px;padding-top:14px;border-top:1px solid rgba(46,125,50,.09)">
            <div style="margin-bottom:8px" v-for="h in ndviData.health" :key="h.label">
              <div style="display:flex;justify-content:space-between;margin-bottom:4px"><span style="font-size:11px;color:var(--text2)">{{ h.label }}</span><span style="font-family:var(--mono);font-size:11px" :style="{color:h.color}">{{ h.pct }}%</span></div>
              <div class="prog-wrap"><div style="height:100%;border-radius:4px;background:var(--color);width:100%" :style="{background:h.color,width:h.pct+'%'}"></div></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ndviApi } from '../api'
import { useToast } from '../composables/useToast'

const { toast } = useToast()
const ndviField = ref('A')
const ndviData = ref(null)

async function loadNdvi() {
  const { data } = await ndviApi.get(ndviField.value)
  ndviData.value = data
}

onMounted(() => loadNdvi())
</script>
