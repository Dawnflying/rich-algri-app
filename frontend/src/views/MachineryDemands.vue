<template>
  <div class="page machinery-demands">
    <div class="hdr-title-bar"><button class="hdr-back" @click="$router.back()">‹</button>农户端_我的需求</div>
    <div class="hdr-banner">
      <span class="hdr-left">
        <span class="hdr-icon">⚡</span>
        我的需求
      </span>
      <button class="btn-publish" @click="showPublishModal = true">
        <span class="btn-icon">🔍</span>
        发布需求
      </button>
    </div>

    <div class="page-body">
      <div v-for="d in demands" :key="d.id" class="demand-card">
        <div class="card-hd">
          <span class="card-title">{{ d.title }}</span>
          <span class="card-status" :class="d.statusClass">{{ d.statusText }}</span>
        </div>
        <div class="card-meta">作业类型: {{ d.opType }}</div>
        <div class="card-meta">地块数: {{ d.plotCount }}个</div>
        <div class="card-meta">期望开始时间: {{ d.startTime }}</div>
        <div class="card-meta">发布时间: {{ d.publishTime }}</div>
        <div class="card-actions">
          <template v-if="d.status === 'pending'">
            <button class="btn-edit" @click="toast('编辑')">编辑</button>
            <button class="btn-cancel" @click="toast('取消')">取消</button>
          </template>
          <button v-else-if="d.status === 'accepted'" class="btn-view" @click="toast('查看订单')">查看订单</button>
          <button v-else-if="d.status === 'done'" class="btn-republish" @click="showPublishModal = true">再次发布</button>
        </div>
      </div>
    </div>

    <!-- 发布需求弹窗：选择需求类型 -->
    <div class="modal-overlay" :class="{ open: showPublishModal }" @click.self="showPublishModal = false">
      <div class="modal-content">
        <div class="modal-hd">选择需求类型</div>
        <div class="modal-section">
          <div class="section-label">需求类型</div>
          <div class="option-row">
            <button class="option-btn" :class="{ active: publishForm.demandType === 'drone' }" @click="publishForm.demandType = 'drone'">
              <span class="option-icon">✈️</span>
              找无人机
            </button>
            <button class="option-btn" :class="{ active: publishForm.demandType === 'other' }" @click="publishForm.demandType = 'other'">
              <span class="option-icon">🚜</span>
              找其他农机
            </button>
          </div>
        </div>
        <div class="modal-section">
          <div class="section-label">作业类型/用途</div>
          <div class="option-col">
            <button class="option-btn option-btn-full" :class="{ active: publishForm.opType === 'patrol' }" @click="publishForm.opType = 'patrol'">
              巡田监测
              <span v-if="publishForm.opType === 'patrol'" class="option-check">✓</span>
            </button>
            <button class="option-btn option-btn-full" :class="{ active: publishForm.opType === 'spray' }" @click="publishForm.opType = 'spray'">
              植保打药
              <span v-if="publishForm.opType === 'spray'" class="option-check">✓</span>
            </button>
          </div>
        </div>
        <button class="btn-confirm" @click="goToPublish">确定</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from '../composables/useToast'

const router = useRouter()
const { toast } = useToast()
const showPublishModal = ref(false)

const publishForm = reactive({
  demandType: 'drone',
  opType: 'patrol',
})

const demands = [
  { id: 1, title: '玉米植保专业打药服务需求', status: 'pending', statusText: '待接单', statusClass: 'status-blue', opType: '无人机打药', plotCount: 3, startTime: '2026-06-25 09:00', publishTime: '2026-06-20 15:30' },
  { id: 2, title: '小麦收割服务需求', status: 'accepted', statusText: '已接单', statusClass: 'status-orange', opType: '收割机作业', plotCount: 2, startTime: '2026-06-28 08:00', publishTime: '2026-06-19 10:15' },
  { id: 3, title: '水稻播种服务需求', status: 'done', statusText: '已完成', statusClass: 'status-green', opType: '播种机作业', plotCount: 1, startTime: '2026-06-15 07:30', publishTime: '2026-06-10 14:20' },
  { id: 4, title: '果园修剪服务需求', status: 'cancelled', statusText: '已取消', statusClass: 'status-gray', opType: '人工修剪', plotCount: 1, startTime: '2026-06-20 09:00', publishTime: '2026-06-08 09:45' },
]

function goToPublish() {
  showPublishModal.value = false
  if (publishForm.demandType === 'drone') {
    if (publishForm.opType === 'patrol') {
      router.push('/machinery/demand/publish/patrol')
    } else {
      router.push('/machinery/demand/publish/spray')
    }
  } else {
    toast('其他农机需求开发中')
  }
}
</script>

<style scoped>
.machinery-demands .page-body { padding: 16px; padding-bottom: 32px; }
.hdr-title-bar { display: flex; align-items: center; gap: 12px; padding: 10px 16px; background: #F5F5F5; font-size: 14px; color: #666; }
.hdr-back { width: 32px; height: 32px; border: none; background: rgba(46,125,50,.1); color: var(--primary); font-size: 22px; border-radius: 8px; cursor: pointer; }
.hdr-banner {
  display: flex; align-items: center; justify-content: space-between; padding: 12px 16px;
  background: linear-gradient(135deg, var(--primary), var(--primary-light)); color: #FFF;
}
.hdr-left { display: flex; align-items: center; gap: 8px; font-size: 16px; font-weight: 600; }
.hdr-icon { font-size: 14px; }
.btn-publish { padding: 8px 14px; background: rgba(255,255,255,.2); color: #FFF; border: 1px solid rgba(255,255,255,.4); border-radius: 8px; font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 4px; }
.btn-icon { font-size: 14px; }
.demand-card { padding: 14px; margin-bottom: 12px; background: #FFF; border: 1px solid rgba(46,125,50,.1); border-radius: 12px; box-shadow: 0 2px 8px rgba(46,125,50,.06); }
.card-hd { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; }
.card-title { font-size: 14px; font-weight: 600; color: #1B2E1B; flex: 1; }
.card-status { font-size: 12px; padding: 2px 10px; border-radius: 12px; flex-shrink: 0; }
.status-blue { background: var(--blue-dim); color: var(--blue); }
.status-orange { background: var(--orange-dim); color: var(--amber); }
.status-green { background: rgba(46,125,50,.15); color: var(--primary); }
.status-gray { background: #EEE; color: #666; }
.card-meta { font-size: 12px; color: var(--text2); margin-bottom: 4px; }
.card-actions { display: flex; gap: 10px; margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(46,125,50,.08); }
.btn-edit { padding: 8px 16px; background: #F0F0F0; color: #666; border: none; border-radius: 8px; font-size: 13px; cursor: pointer; }
.btn-cancel { padding: 8px 16px; background: #FFF; color: var(--red); border: 1px solid var(--red); border-radius: 8px; font-size: 13px; cursor: pointer; }
.btn-view, .btn-republish { padding: 8px 20px; background: var(--primary); color: #FFF; border: none; border-radius: 8px; font-size: 13px; cursor: pointer; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.4); display: flex; align-items: flex-end; justify-content: center; z-index: 100; opacity: 0; pointer-events: none; transition: .2s; }
.modal-overlay.open { opacity: 1; pointer-events: auto; }
.modal-content { width: 100%; max-width: 480px; background: #FFF; border-radius: 16px 16px 0 0; padding: 24px; transform: translateY(100%); transition: .2s; }
.modal-overlay.open .modal-content { transform: translateY(0); }
.modal-hd { font-size: 16px; font-weight: 600; color: #1B2E1B; margin-bottom: 20px; }
.modal-section { margin-bottom: 20px; }
.section-label { font-size: 13px; color: var(--text2); margin-bottom: 10px; }
.option-row { display: flex; gap: 12px; }
.option-col { display: flex; flex-direction: column; gap: 10px; }
.option-btn { flex: 1; padding: 12px 16px; border: 1.5px solid var(--primary-border); background: #FFF; color: var(--text2); border-radius: 10px; font-size: 14px; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; }
.option-btn.active { background: var(--primary); color: #FFF; border-color: var(--primary); }
.option-btn-full { width: 100%; }
.option-icon { font-size: 18px; }
.option-check { margin-left: auto; font-size: 16px; }
.btn-confirm { width: 100%; padding: 14px; background: var(--primary); color: #FFF; border: none; border-radius: 10px; font-size: 15px; font-weight: 600; cursor: pointer; margin-top: 8px; }
</style>
