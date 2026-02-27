<template>
  <div class="page">
    <div class="hdr"><button class="hdr-back" @click="$router.back()">‹</button><div class="hdr-title">{{ title }}</div></div>
    <div class="page-body" style="padding:40px 20px;text-align:center;color:#9DB89C">
      <div style="font-size:48px;margin-bottom:16px">{{ icon }}</div>
      <div style="font-size:16px;font-weight:500;color:#5A7A5A">{{ title }} 功能开发中</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const title = computed(() => ({ '/chat': '地小帮', '/ai': 'AI帮助', '/community': '小农聚力' }[route.path] || '页面'))
const icon = computed(() => ({ '/chat': '💬', '/ai': '🤝', '/community': '👥' }[route.path] || '📄'))
</script>
