<template>
  <div id="app">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
    <nav id="nav" v-if="showNav" class="farmer-nav">
      <router-link to="/" class="nav-item" :class="{ active: $route.path === '/' }">
        <span class="nav-icon">🏠</span><span class="nav-label">首页</span>
      </router-link>
      <router-link to="/chat" class="nav-item" :class="{ active: $route.path === '/chat' }">
        <span class="nav-icon">💬</span><span class="nav-label">地小帮</span>
      </router-link>
      <router-link to="/ai" class="nav-item" :class="{ active: $route.path === '/ai' }">
        <span class="nav-icon">🤝</span><span class="nav-label">AI帮助</span>
      </router-link>
      <router-link to="/community" class="nav-item" :class="{ active: $route.path === '/community' }">
        <span class="nav-icon">👥</span><span class="nav-label">小农聚力</span>
      </router-link>
      <router-link to="/profile" class="nav-item" :class="{ active: $route.path === '/profile' }">
        <span class="nav-icon">👤</span><span class="nav-label">我的</span>
      </router-link>
    </nav>
    <div id="toast"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const showNav = computed(() => {
  const noNav = ['/login', '/alerts', '/tracking', '/farmlog/add', '/wallet', '/withdraw', '/farm/create', '/field/edit', '/field/map-plot']
  if (route.path === '/farmlog' || route.path.startsWith('/farmlog/') || route.path.startsWith('/farm/') || route.path.startsWith('/field/') || route.path.startsWith('/machinery')) return false
  return !noNav.some(p => route.path.startsWith(p))
})
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s }
.fade-enter-from, .fade-leave-to { opacity: 0 }
</style>
