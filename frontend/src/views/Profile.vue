<template>
  <div class="page profile-page">
    <div class="page-body profile-body">
      <!-- 顶部个人信息区 -->
      <div class="profile-header">
        <div class="profile-avatar">👨‍🌾</div>
        <div class="profile-info">
          <div class="profile-name">{{ user?.name || '张三' }} 农户</div>
          <div class="profile-id">ID: 20240203001</div>
        </div>
        <div class="profile-actions">
          <span class="profile-action-icon" @click="toast('分享')">📤</span>
          <span class="profile-action-icon" @click="toast('扫码')">📷</span>
          <span class="profile-action-icon" @click="toast('个人资料')">›</span>
        </div>
      </div>

      <!-- 数据概览卡片 -->
      <div class="profile-cards">
        <div class="profile-card">
          <div class="profile-card-title">总面积</div>
          <div class="profile-card-val">850.5亩</div>
          <div class="profile-card-sub">3农场·12地块</div>
        </div>
        <div class="profile-card">
          <div class="profile-card-title">种植结构</div>
          <div class="profile-card-val profile-card-val-sm">棉花382.7亩</div>
          <div class="profile-card-val profile-card-val-sm">玉米255.2亩</div>
        </div>
        <div class="profile-card">
          <div class="profile-card-title">月度农机投入</div>
          <div class="profile-card-val">8200元</div>
        </div>
      </div>

      <!-- 我的订单 -->
      <div class="profile-section">
        <div class="profile-section-title">我的订单</div>
        <div class="order-tabs">
          <div v-for="o in orderTabs" :key="o.key" class="order-tab" @click="toast(o.label)">
            <span class="order-tab-icon">{{ o.icon }}</span>
            <span class="order-tab-label">{{ o.label }}</span>
          </div>
        </div>
      </div>

      <!-- 消息通知 -->
      <div class="profile-section">
        <div class="profile-section-title">消息通知</div>
        <div class="profile-list-card">
          <div class="profile-list-item" @click="$router.push('/alerts')">
            <div class="profile-list-icon" style="background:rgba(46,125,50,.12)">🔔</div>
            <div class="profile-list-body">
              <div class="profile-list-title">消息通知</div>
              <div class="profile-list-sub">查看所有消息通知</div>
            </div>
            <span class="profile-badge">4</span>
            <span class="profile-arrow">›</span>
          </div>
        </div>
      </div>

      <!-- 设置 -->
      <div class="profile-section">
        <div class="profile-section-title">设置</div>
        <div class="profile-list-card">
          <div v-for="s in settings" :key="s.key" class="profile-list-item" @click="toast(s.title)">
            <div class="profile-list-icon" style="background:rgba(46,125,50,.12)">{{ s.icon }}</div>
            <div class="profile-list-body">
              <div class="profile-list-title">{{ s.title }}</div>
              <div class="profile-list-sub">{{ s.sub }}</div>
            </div>
            <span class="profile-arrow">›</span>
          </div>
        </div>
      </div>

      <!-- 退出登录 -->
      <div class="profile-logout-wrap">
        <button class="profile-logout-btn" @click="doLogout">退出登录</button>
      </div>

      <div style="height:24px"></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '../stores/app'
import { useToast } from '../composables/useToast'

const router = useRouter()
const appStore = useAppStore()
const { toast } = useToast()

const user = computed(() => appStore.user)

const orderTabs = [
  { key: 'all', icon: '📋', label: '全部' },
  { key: 'pending', icon: '⏳', label: '待处理' },
  { key: 'settle', icon: '💰', label: '待结算' },
  { key: 'progress', icon: '🔄', label: '进行中' },
  { key: 'accept', icon: '✅', label: '待验收' },
  { key: 'done', icon: '✔️', label: '已完成' },
]

const settings = [
  { key: 'pwd', icon: '🔒', title: '修改密码', sub: '更新账号登录密码' },
  { key: 'notify', icon: '🔔', title: '通知设置', sub: '消息通知偏好设置' },
  { key: 'agreement', icon: '📄', title: '用户协议', sub: '查看用户服务协议' },
  { key: 'privacy', icon: '🛡️', title: '隐私政策', sub: '查看隐私保护政策' },
  { key: 'about', icon: 'ℹ️', title: '关于我们', sub: '版本信息和公司介绍' },
]

function doLogout() {
  appStore.logout()
  toast('已安全退出')
  router.push('/login')
}
</script>

<style scoped>
.profile-page { display: flex; flex-direction: column; }
.profile-body {
  flex: 1; overflow-y: auto; overflow-x: hidden;
  -webkit-overflow-scrolling: touch;
  padding-bottom: calc(var(--nav-h) + 16px);
}
.profile-body::-webkit-scrollbar { display: none; }

.profile-header {
  display: flex; align-items: center; gap: 16px;
  padding: 24px 20px 28px;
  background: linear-gradient(135deg, var(--primary), var(--primary-light));
  color: #FFF;
}
.profile-avatar {
  width: 64px; height: 64px; border-radius: 50%;
  background: rgba(255,255,255,.25);
  display: flex; align-items: center; justify-content: center;
  font-size: 32px; flex-shrink: 0;
}
.profile-info { flex: 1; min-width: 0; }
.profile-name { font-size: 20px; font-weight: 700; }
.profile-id { font-size: 12px; opacity: .9; margin-top: 4px; font-family: var(--mono); }
.profile-actions { display: flex; align-items: center; gap: 16px; }
.profile-action-icon { font-size: 20px; cursor: pointer; opacity: .95; }

.profile-cards {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;
  padding: 16px; margin: -12px 16px 0; background: #FFF;
  border-radius: 12px; border: 1px solid rgba(46,125,50,.15);
  box-shadow: 0 2px 12px rgba(46,125,50,.08);
}
.profile-card {
  text-align: center; padding: 12px 8px;
  border: 1px solid rgba(46,125,50,.12); border-radius: 10px;
}
.profile-card-title { font-size: 12px; color: var(--text2); margin-bottom: 6px; }
.profile-card-val { font-size: 18px; font-weight: 600; color: #1B2E1B; font-family: var(--mono); }
.profile-card-val-sm { font-size: 13px; margin-top: 2px; }
.profile-card-sub { font-size: 11px; color: #9DB89C; margin-top: 4px; }

.profile-section { padding: 20px 16px 0; }
.profile-section-title { font-size: 14px; font-weight: 600; color: #1B2E1B; margin-bottom: 12px; }
.order-tabs {
  display: flex; gap: 12px; overflow-x: auto; padding-bottom: 4px;
}
.order-tabs::-webkit-scrollbar { display: none; }
.order-tab {
  flex-shrink: 0; display: flex; flex-direction: column; align-items: center; gap: 6px;
  padding: 14px 16px; background: #FFF; border: 1px solid rgba(46,125,50,.12);
  border-radius: 10px; cursor: pointer; min-width: 72px;
}
.order-tab:active { background: #F7FAF7; }
.order-tab-icon { font-size: 24px; }
.order-tab-label { font-size: 12px; color: var(--text2); }

.profile-list-card {
  background: #FFF; border: 1px solid rgba(46,125,50,.1); border-radius: 12px;
  overflow: hidden; box-shadow: 0 2px 8px rgba(46,125,50,.05);
}
.profile-list-item {
  display: flex; align-items: center; gap: 12px;
  padding: 14px 16px; border-bottom: 1px solid rgba(46,125,50,.06);
  cursor: pointer;
}
.profile-list-item:last-child { border-bottom: none; }
.profile-list-item:active { background: #F7FAF7; }
.profile-list-icon {
  width: 40px; height: 40px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0;
}
.profile-list-body { flex: 1; min-width: 0; }
.profile-list-title { font-size: 14px; font-weight: 500; color: #1B2E1B; }
.profile-list-sub { font-size: 12px; color: #9DB89C; margin-top: 2px; }
.profile-badge {
  min-width: 20px; height: 20px; padding: 0 6px;
  background: var(--red); color: #FFF; font-size: 11px; font-weight: 600;
  border-radius: 10px; display: flex; align-items: center; justify-content: center;
}
.profile-arrow { font-size: 18px; color: #9DB89C; }

.profile-logout-wrap { padding: 24px 16px 0; }
.profile-logout-btn {
  width: 100%; height: 48px; background: var(--red); color: #FFF;
  border: none; border-radius: 12px; font-size: 16px; font-weight: 600;
  cursor: pointer; font-family: var(--sans);
}
.profile-logout-btn:active { background: #B71C1C; }
</style>
