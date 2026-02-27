import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/login', name: 'Login', component: () => import('../views/Login.vue'), meta: { noNav: true } },
  { path: '/', name: 'Home', component: () => import('../views/Home.vue') },
  { path: '/fields', name: 'Fields', component: () => import('../views/Fields.vue') },
  { path: '/drone', name: 'Drone', component: () => import('../views/Drone.vue') },
  { path: '/ndvi', name: 'Ndvi', component: () => import('../views/Ndvi.vue') },
  { path: '/profile', name: 'Profile', component: () => import('../views/Profile.vue') },
  { path: '/chat', name: 'Chat', component: () => import('../views/Placeholder.vue') },
  { path: '/ai', name: 'AI', component: () => import('../views/Placeholder.vue') },
  { path: '/community', name: 'Community', component: () => import('../views/Placeholder.vue') },
  { path: '/alerts', name: 'Alerts', component: () => import('../views/Alerts.vue'), meta: { noNav: true } },
  { path: '/tracking', name: 'Tracking', component: () => import('../views/Tracking.vue'), meta: { noNav: true } },
  { path: '/farmlog', name: 'Farmlog', component: () => import('../views/Farmlog.vue'), meta: { noNav: true } },
  { path: '/farmlog/add', name: 'FarmlogAdd', component: () => import('../views/FarmlogAdd.vue'), meta: { noNav: true } },
  { path: '/farmlog/template-settings', name: 'FarmlogTemplateSettings', component: () => import('../views/FarmlogTemplateSettings.vue'), meta: { noNav: true } },
  { path: '/farmlog/:id', name: 'FarmlogDetail', component: () => import('../views/FarmlogDetail.vue'), meta: { noNav: true } },
  { path: '/wallet', name: 'Wallet', component: () => import('../views/Wallet.vue'), meta: { noNav: true } },
  { path: '/withdraw', name: 'Withdraw', component: () => import('../views/Withdraw.vue'), meta: { noNav: true } },
  { path: '/farm/create', name: 'FarmCreate', component: () => import('../views/FarmCreate.vue'), meta: { noNav: true } },
  { path: '/farm/:id', name: 'FarmDetail', component: () => import('../views/FarmDetail.vue'), meta: { noNav: true } },
  { path: '/field/edit', name: 'FieldEdit', component: () => import('../views/FieldEdit.vue'), meta: { noNav: true } },
  { path: '/field/map-plot', name: 'FieldMapPlot', component: () => import('../views/FieldMapPlot.vue'), meta: { noNav: true } },
  { path: '/field/:id', name: 'FieldDetail', component: () => import('../views/FieldDetail.vue'), meta: { noNav: true } },
  { path: '/field/:id/map', name: 'FieldMapFullscreen', component: () => import('../views/FieldMapFullscreen.vue'), meta: { noNav: true } },
  { path: '/machinery', name: 'Machinery', component: () => import('../views/Machinery.vue'), meta: { noNav: true } },
  { path: '/machinery/package/:id', name: 'MachineryPackageDetail', component: () => import('../views/MachineryPackageDetail.vue'), meta: { noNav: true } },
  { path: '/machinery/remote/:period', name: 'MachineryRemotePackage', component: () => import('../views/MachineryRemotePackage.vue'), meta: { noNav: true } },
  { path: '/machinery/remote/confirm', name: 'MachineryRemoteOrderConfirm', component: () => import('../views/MachineryRemoteOrderConfirm.vue'), meta: { noNav: true } },
  { path: '/machinery/demands', name: 'MachineryDemands', component: () => import('../views/MachineryDemands.vue'), meta: { noNav: true } },
  { path: '/machinery/demand/publish/patrol', name: 'DemandPublishPatrol', component: () => import('../views/DemandPublishPatrol.vue'), meta: { noNav: true } },
  { path: '/machinery/demand/publish/spray', name: 'DemandPublishSpray', component: () => import('../views/DemandPublishSpray.vue'), meta: { noNav: true } },
  { path: '/machinery/orders', name: 'MachineryOrders', component: () => import('../views/MachineryOrders.vue'), meta: { noNav: true } },
  { path: '/machinery/order/:id', name: 'MachineryOrderDetail', component: () => import('../views/MachineryOrderDetail.vue'), meta: { noNav: true } },
  { path: '/machinery/order/:id/trace', name: 'MachineryOrderTrace', component: () => import('../views/MachineryOrderTrace.vue'), meta: { noNav: true } },
  { path: '/patrol', name: 'ReportLibrary', component: () => import('../views/ReportLibrary.vue'), meta: { noNav: true } },
  { path: '/patrol/report/:id', name: 'ReportDetail', component: () => import('../views/ReportDetail.vue'), meta: { noNav: true } },
  { path: '/irrigation', name: 'IrrigationTaskList', component: () => import('../views/IrrigationTaskList.vue'), meta: { noNav: true } },
  { path: '/irrigation/create', name: 'IrrigationTaskCreate', component: () => import('../views/IrrigationTaskCreate.vue'), meta: { noNav: true } },
  { path: '/irrigation/:id', name: 'IrrigationTaskDetail', component: () => import('../views/IrrigationTaskDetail.vue'), meta: { noNav: true } },
  { path: '/guidance', name: 'GuidanceList', component: () => import('../views/GuidanceList.vue'), meta: { noNav: true } },
  { path: '/guidance/invite', name: 'GuidanceInvite', component: () => import('../views/GuidanceInvite.vue'), meta: { noNav: true } },
  { path: '/guidance/:id', name: 'GuidanceDetail', component: () => import('../views/GuidanceDetail.vue'), meta: { noNav: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (!token && to.path !== '/login') {
    next('/login')
  } else if (token && to.path === '/login') {
    next('/')
  } else {
    next()
  }
})

export default router
