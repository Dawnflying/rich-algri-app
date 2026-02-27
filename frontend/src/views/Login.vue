<template>
  <div class="page" id="page-login" style="justify-content:flex-end;padding-bottom:0">
    <div class="login-bg"></div>
    <div class="login-art">
      <div>
        <div class="login-logo" style="text-align:center;font-size:72px">🌾</div>
        <div class="login-brand">
          <div class="login-brand-name">智农云</div>
          <div class="login-brand-sub">Smart Agriculture Platform</div>
        </div>
      </div>
    </div>
    <div class="login-form">
      <div class="login-tab">
        <button :class="{ active: tab === 'login' }" @click="tab = 'login'">登录</button>
        <button :class="{ active: tab === 'register' }" @click="tab = 'register'">注册</button>
      </div>
      <div v-if="tab === 'login'" style="display:flex;flex-direction:column;gap:12px">
        <div class="field">
          <span>📱</span>
          <input type="tel" v-model="phone" placeholder="手机号" maxlength="11" />
        </div>
        <div class="field">
          <span>🔒</span>
          <input type="password" v-model="password" placeholder="密码" />
        </div>
        <button class="btn btn-primary btn-full" style="margin-top:8px;height:48px;font-size:16px" @click="doLogin">登 录</button>
        <div style="text-align:center;font-size:12px;color:#9DB89C;margin-top:4px">演示账号已填入，直接点击登录</div>
      </div>
      <div v-else style="display:flex;flex-direction:column;gap:12px">
        <div class="field"><span>📱</span><input type="tel" placeholder="手机号" maxlength="11" /></div>
        <div class="field"><span>💬</span><input type="text" placeholder="验证码" maxlength="6" /><button style="color:var(--primary);font-size:13px" @click="toast('验证码已发送')">获取验证码</button></div>
        <div class="field"><span>🏢</span><input type="text" placeholder="姓名/企业名称" /></div>
        <div class="field"><span>🔒</span><input type="password" placeholder="设置密码" /></div>
        <button class="btn btn-primary btn-full" style="margin-top:8px;height:48px;font-size:16px" @click="toast('注册功能演示中')">注 册</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '../stores/app'
import { useToast } from '../composables/useToast'

const router = useRouter()
const appStore = useAppStore()
const { toast } = useToast()

const tab = ref('login')
const phone = ref('13800138000')
const password = ref('123456')

async function doLogin() {
  if (!phone.value || !password.value) {
    toast('请填写手机号和密码')
    return
  }
  const ok = await appStore.login(phone.value, password.value)
  if (ok) {
    toast('登录成功 ✓')
    router.push('/')
  } else {
    toast('登录失败')
  }
}
</script>
