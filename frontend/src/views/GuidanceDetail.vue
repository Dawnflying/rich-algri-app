<template>
  <div class="page guidance-detail">
    <div class="hdr-bar">
      <button class="hdr-back" @click="$router.back()">‹</button>
      <span class="hdr-title">指导建议详情</span>
      <span v-if="guidance?.replied" class="hdr-status">已回复</span>
    </div>

    <div class="page-body" v-if="guidance">
      <div class="info-header">
        <div class="provider-name">{{ guidance.provider }}({{ guidance.providerLabel || '农资服务商' }})</div>
        <div class="location">{{ guidance.farm }} - {{ guidance.plotName }}</div>
        <div class="create-time">创建时间: {{ guidance.createTime }}</div>
      </div>

      <div class="messages">
        <div v-for="(msg, i) in guidance.messages" :key="i" class="msg-row" :class="msg.role">
          <div class="msg-avatar" :class="msg.role">
            <span>{{ msg.role === 'farmer' ? '👤' : '👤' }}</span>
          </div>
          <div class="msg-body">
            <div class="msg-sender">{{ msg.name }}</div>
            <div class="msg-time">{{ msg.time }}</div>
            <div class="msg-content">{{ msg.content }}</div>
            <div v-if="msg.photos" class="msg-photos">
              <div v-for="p in msg.photos" :key="p" class="photo-placeholder">🖼</div>
            </div>
            <div v-if="msg.record" class="msg-record">
              关联农事记录: <span class="record-link">{{ msg.record }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="detail-actions">
        <button class="btn-contact" @click="toast('联系农户')">📞 联系农户</button>
        <button class="btn-reply" @click="toast('再次回复')">↩ 再次回复</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { guidanceApi } from '../api'
import { useToast } from '../composables/useToast'

const route = useRoute()
const { toast } = useToast()
const guidance = ref(null)

onMounted(async () => {
  const id = Number(route.params.id)
  if (!id) return
  try {
    const { data } = await guidanceApi.get(id)
    guidance.value = data
    if (!guidance.value.providerLabel) guidance.value.providerLabel = '农资服务商'
  } catch (e) {
    guidance.value = null
  }
})
</script>

<style scoped>
.guidance-detail .page-body { padding: 16px; padding-bottom: 32px; }
.hdr-bar { display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: var(--blue); color: #FFF; }
.hdr-back { width: 36px; height: 36px; border: none; background: rgba(255,255,255,.2); color: #FFF; font-size: 24px; border-radius: 8px; cursor: pointer; }
.hdr-title { font-size: 18px; font-weight: 600; flex: 1; }
.hdr-status { padding: 6px 14px; background: rgba(255,255,255,.3); border-radius: 8px; font-size: 13px; }
.info-header { background: var(--surface); border-radius: 12px; padding: 16px; margin-bottom: 20px; }
.provider-name { font-size: 15px; font-weight: 600; margin-bottom: 6px; }
.location { font-size: 14px; color: #666; margin-bottom: 4px; }
.create-time { font-size: 13px; color: #999; }
.messages { display: flex; flex-direction: column; gap: 20px; }
.msg-row { display: flex; gap: 12px; }
.msg-row.provider { flex-direction: row-reverse; }
.msg-avatar { width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 22px; flex-shrink: 0; }
.msg-avatar.farmer { background: #FFE8CC; }
.msg-avatar.provider { background: #D4EDDA; }
.msg-body { flex: 1; min-width: 0; }
.msg-sender { font-size: 14px; font-weight: 600; margin-bottom: 2px; }
.msg-time { font-size: 12px; color: #999; margin-bottom: 8px; }
.msg-content { background: #F5F5F5; padding: 12px; border-radius: 12px; font-size: 14px; line-height: 1.6; white-space: pre-wrap; }
.msg-row.provider .msg-content { background: var(--primary-dim); }
.msg-photos { display: flex; gap: 8px; margin-top: 10px; }
.photo-placeholder { width: 60px; height: 60px; background: #E0E0E0; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 24px; }
.msg-record { font-size: 13px; color: var(--blue); margin-top: 8px; }
.record-link { text-decoration: underline; cursor: pointer; }
.detail-actions { display: flex; gap: 12px; margin-top: 24px; }
.btn-contact { flex: 1; padding: 14px; background: #F5F5F5; color: #666; border: none; border-radius: 12px; font-size: 15px; cursor: pointer; }
.btn-reply { flex: 1; padding: 14px; background: var(--primary-gradient); color: #FFF; border: none; border-radius: 12px; font-size: 15px; font-weight: 600; cursor: pointer; }
</style>
