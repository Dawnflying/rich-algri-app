<template>
  <div class="page">
    <div class="hdr"><div class="hdr-title">地块管理</div><button class="hdr-action" @click="$router.push('/field/edit')">➕</button></div>
    <div class="page-body">
      <div style="padding:12px 16px 0">
        <div class="map-box" style="height:200px">
          <svg width="100%" height="100%" viewBox="0 0 340 200">
            <polygon points="30,40 120,25 180,60 160,110 60,120" fill="rgba(107,155,110,.12)" stroke="#6B9B6E" stroke-width="1.5"/>
            <polygon points="190,30 280,20 310,70 270,90 195,75" fill="rgba(123,163,212,.12)" stroke="#7BA3D4" stroke-width="1.5"/>
            <text x="90" y="80" fill="#1B5E20" font-size="10">A区 · 小麦</text>
            <text x="230" y="58" fill="#7BA3D4" font-size="10">B区 · 水稻</text>
          </svg>
        </div>
      </div>
      <div class="sec" style="margin-top:16px">
        <div class="sec-hd"><span class="sec-title">地块列表</span><span style="font-size:12px;color:#5A7A5A">共 {{ fields.length }} 块</span></div>
        <div class="card">
          <div v-for="f in fields" :key="f.id" class="list-row" @click="$router.push('/field/' + f.id)">
            <div class="list-icon" style="background:#F2F8F2;font-size:20px">🌾</div>
            <div class="list-body">
              <div class="list-title">{{ f.name }}</div>
              <div class="list-sub">{{ f.location || '--' }} · {{ f.area }}亩 · {{ f.crop }}{{ f.planting ? ' · ' + f.planting : '' }}</div>
              <div style="margin-top:6px;display:flex;align-items:center;gap:6px">
                <div class="prog-wrap" style="flex:1"><div class="prog-fill" :style="{width:((f.ndvi||0)*100)+'%'}"></div></div>
                <span style="font-family:var(--mono);font-size:11px;color:var(--primary)">NDVI {{ f.ndvi ?? '--' }}</span>
              </div>
            </div>
            <div class="list-right"><span :class="['badge',(f.status==='alert'||f.status==='pending_irrigate')?'badge-amber':'badge-green']">{{ f.statusText || (f.status==='alert'?'预警':'正常') }}</span></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fieldsApi } from '../api'
import { useToast } from '../composables/useToast'

const { toast } = useToast()
const fields = ref([])

onMounted(async () => {
  const { data } = await fieldsApi.list()
  fields.value = data
})
</script>
