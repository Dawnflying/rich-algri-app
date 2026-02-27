let toastTimer = null

export function useToast() {
  const show = (msg) => {
    const el = document.getElementById('toast')
    if (!el) return
    el.textContent = msg
    el.classList.add('show')
    clearTimeout(toastTimer)
    toastTimer = setTimeout(() => el.classList.remove('show'), 2200)
  }
  return { toast: show }
}
