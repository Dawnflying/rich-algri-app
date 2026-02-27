import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/styles.css'
import { useAppStore } from './stores/app'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)

// 有 token 时预取用户信息
router.isReady().then(() => {
  const appStore = useAppStore()
  if (appStore.token) appStore.fetchUser()
})

app.mount('#app')
