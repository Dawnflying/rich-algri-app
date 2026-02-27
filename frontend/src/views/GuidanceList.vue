<template>
  <div class="page guidance-list">
    <div class="hdr-bar">
      <button class="hdr-back" @click="$router.back()">‹</button>
      <span class="hdr-title">指导建议</span>
      <button class="hdr-search" @click="toast('搜索')">🔍</button>
    </div>

    <div class="page-body">
      <button class="btn-invite" @click="$router.push('/guidance/invite')">
        <span class="btn-icon">👤</span>
        邀请指导
        <span v-if="inviteBadge" class="invite-badge">{{ inviteBadge }}</span>
      </button>

      <div class="filter-tabs">
        <button v-for="t in filterTabs" :key="t.key" class="filter-tab" :class="{ active: filterType === t.key }" @click="filterType = t.key">
          {{ t.label }}
        </button>
      </div>

      <div class="summary">总计: {{ list.length }}条建议 | 未读: {{ unreadCount }}条</div>

      <div class="guidance-list">
        <div v-for="g in filteredList" :key="g.id" class="guidance-card" :class="g.badge" @click="$router.push('/guidance/' + g.id)">
          <div class="card-left">
            <span class="badge-tag" :class="g.badge">{{ g.badgeText }}</span>
            <div class="card-time">{{ g.time }}</div>
            <div class="card-title">📍 {{ g.plotName }} - {{ g.issue }}</div>
            <div class="card-meta">📷 {{ g.photoCount }}张照片</div>
            <div class="card-status">
              <span v-if="g.status === 'processed'" class="status-dot processed">✓</span>
              <span v-else class="status-dot unprocessed">○</span>
              {{ g.statusText }}
            </div>
          </div>
          <div class="card-expert">{{ g.expert }}</div>
        </div>
      </div>

      <div class="list-end">
        <span class="end-icon">💡</span>
        <div class="end-text">没有更多建议了</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { guidanceApi } from '../api'
import { useToast } from '../composables/useToast'

const { toast } = useToast()
const list = ref([])
const filterType = ref('all')
const inviteBadge = ref('4')

const filterTabs = [
  { key: 'all', label: '全部' },
  { key: 'unread', label: '未读' },
  { key: 'unprocessed', label: '未处理' },
]

const unreadCount = computed(() => list.value.filter(g => !g.read).length)

const filteredList = computed(() => {
  if (filterType.value === 'unread') return list.value.filter(g => !g.read)
  if (filterType.value === 'unprocessed') return list.value.filter(g => g.status === 'unprocessed')
  return list.value
})

async function fetchList() {
  try {
    const { data } = await guidanceApi.list({ filter_type: filterType.value })
    list.value = data || []
  } catch (e) {
    list.value = []
  }
}

onMounted(fetchList)
watch(filterType, fetchList)
</script>

<style scoped>
.guidance-list .page-body { padding: 16px; }
.hdr-bar { display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: var(--primary-gradient); color: #FFF; }
.hdr-back { width: 36px; height: 36px; border: none; background: rgba(255,255,255,.2); color: #FFF; font-size: 24px; border-radius: 8px; cursor: pointer; }
.hdr-title { font-size: 18px; font-weight: 600; flex: 1; }
.hdr-search { width: 40px; height: 40px; border: none; background: rgba(255,255,255,.2); color: #FFF; font-size: 18px; border-radius: 8px; cursor: pointer; }
.btn-invite { position: relative; width: 100%; padding: 16px; background: var(--primary-gradient); color: #FFF; border: none; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 16px; }
.invite-badge { position: absolute; top: -4px; right: 16px; background: var(--blue); font-size: 12px; padding: 2px 8px; border-radius: 10px; }
.filter-tabs { display: flex; gap: 12px; margin-bottom: 12px; }
.filter-tab { flex: 1; padding: 10px; border: 1px solid #E0E0E0; background: #FFF; border-radius: 8px; font-size: 14px; cursor: pointer; }
.filter-tab.active { background: var(--primary); color: #FFF; border-color: var(--primary); }
.summary { font-size: 13px; color: #666; margin-bottom: 16px; }
.guidance-list { display: flex; flex-direction: column; gap: 12px; }
.guidance-card { display: flex; justify-content: space-between; padding: 16px; background: #FFF; border-radius: 12px; box-shadow: 0 1px 4px rgba(0,0,0,.06); cursor: pointer; border-left: 4px solid transparent; }
.guidance-card.new { border-left-color: var(--primary); }
.guidance-card.unprocessed { border-left-color: var(--orange); }
.badge-tag { font-size: 12px; padding: 2px 8px; border-radius: 6px; margin-right: 8px; }
.badge-tag.new { background: var(--primary-dim); color: var(--primary); }
.badge-tag.read { background: #E0E0E0; color: #616161; }
.badge-tag.unprocessed { background: var(--orange-dim); color: var(--amber); }
.card-left { flex: 1; min-width: 0; }
.card-time { font-size: 13px; color: #666; margin-bottom: 4px; }
.card-title { font-size: 14px; font-weight: 500; color: #333; margin-bottom: 6px; }
.card-meta { font-size: 12px; color: #999; margin-bottom: 4px; }
.card-status { font-size: 12px; color: #666; }
.status-dot { margin-right: 4px; }
.status-dot.processed { color: var(--primary); }
.status-dot.unprocessed { color: #9E9E9E; }
.card-expert { font-size: 14px; font-weight: 500; color: #333; align-self: center; }
.list-end { text-align: center; padding: 24px; color: #9E9E9E; }
.end-icon { font-size: 24px; display: block; margin-bottom: 8px; }
.end-text { font-size: 13px; }
</style>
