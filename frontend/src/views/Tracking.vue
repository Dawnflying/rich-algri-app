<template>
  <div class="page">
    <div class="hdr"><button class="hdr-back" @click="$router.back()">‹</button><div class="hdr-title">实时轨迹</div></div>
    <div class="page-body">
      <div style="padding:12px 16px 0">
        <div class="drone-track" style="height:240px">
          <div class="drone-icon" style="left:50px;top:40px">🚁</div>
          <div style="position:absolute;top:10px;left:10px;background:rgba(255,255,255,.92);border-radius:8px;padding:6px 10px">
            <div style="font-size:10px;color:var(--text2)">实时位置</div>
            <div style="font-family:var(--mono);font-size:10px;color:var(--primary)">120.4523°E  30.7821°N</div>
          </div>
        </div>
      </div>
      <div style="padding:12px 16px 0;display:grid;grid-template-columns:repeat(2,1fr);gap:10px">
        <div class="stat-box"><div style="font-size:10px;color:var(--text2)">📍 飞行高度</div><div class="stat-val" style="color:var(--blue)">90.0 m</div></div>
        <div class="stat-box"><div style="font-size:10px;color:var(--text2)">⚡ 飞行速度</div><div class="stat-val" style="color:var(--amber)">8.4 m/s</div></div>
        <div class="stat-box"><div style="font-size:10px;color:var(--text2)">🔋 电量剩余</div><div class="stat-val" style="color:var(--primary)">78%</div></div>
        <div class="stat-box"><div style="font-size:10px;color:var(--text2)">📸 已拍张数</div><div class="stat-val" style="color:var(--primary)">124</div></div>
      </div>
      <div class="sec"><div style="display:flex;gap:10px">
        <button class="btn btn-danger btn-full" style="height:48px" @click="toast('任务已暂停')">⏸ 暂停</button>
        <button class="btn btn-ghost btn-full" style="height:48px" @click="$router.back()">🏠 返航</button>
      </div></div>
    </div>
  </div>
</template>

<script setup>
import { useToast } from '../composables/useToast'
const { toast } = useToast()
</script>
