const STORAGE_KEY = 'farmlog_templates'

const DEFAULT_TEMPLATES = {
  growth: { enabled: true, label: '日生长量', icon: '🌱' },
  water: { enabled: true, label: '水肥使用', icon: '💧' },
  pest: { enabled: true, label: '农药使用', icon: '🧪' },
  diary: { enabled: true, label: '记事', icon: '📋' },
  issue: { enabled: true, label: '田间问题', icon: '⚠️' },
}

export function useFarmlogTemplates() {
  function load() {
    const base = {}
    Object.keys(DEFAULT_TEMPLATES).forEach(k => {
      base[k] = { ...DEFAULT_TEMPLATES[k] }
    })
    try {
      const s = localStorage.getItem(STORAGE_KEY)
      if (s) {
        const parsed = JSON.parse(s)
        Object.keys(parsed).forEach(k => {
          if (base[k]) base[k] = { ...base[k], ...parsed[k] }
        })
      }
    } catch (_) {}
    return base
  }

  function save(templates) {
    const toSave = {}
    Object.keys(templates).forEach(k => {
      toSave[k] = { enabled: templates[k].enabled, label: templates[k].label, icon: templates[k].icon }
    })
    localStorage.setItem(STORAGE_KEY, JSON.stringify(toSave))
  }

  function getEnabledTypes() {
    const t = load()
    return Object.entries(t)
      .filter(([_, v]) => v.enabled)
      .map(([key]) => key)
  }

  function getEnabledOptions() {
    const t = load()
    return Object.entries(t)
      .filter(([_, v]) => v.enabled)
      .map(([key, v]) => ({ key, label: v.label, icon: v.icon }))
  }

  return { load, save, getEnabledTypes, getEnabledOptions, DEFAULT_TEMPLATES }
}
