import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
})

// 认证
export const authApi = {
  login: (phone, password) => api.post('/auth/login', { phone, password }),
  getUser: () => api.get('/auth/user'),
  logout: () => api.post('/auth/logout'),
}

// 农场
export const farmsApi = {
  list: () => api.get('/farms'),
  get: (id) => api.get(`/farms/${id}`),
  create: (data) => api.post('/farms', data),
}

// 地块
export const fieldsApi = {
  list: () => api.get('/fields'),
  get: (id) => api.get(`/fields/${id}`),
  add: (data) => api.post('/fields', data),
}

// 无人机
export const droneApi = {
  listTasks: (status) => api.get('/drone/tasks', { params: { status } }),
  createTask: (data) => api.post('/drone/tasks', data),
}

// NDVI
export const ndviApi = {
  get: (fieldKey) => api.get(`/ndvi/${fieldKey}`),
}

// 预警
export const alertsApi = {
  list: (filter) => api.get('/alerts', { params: { filter_type: filter } }),
  read: (id) => api.post(`/alerts/${id}/read`),
  readAll: () => api.post('/alerts/read-all'),
}

// 灌溉
export const irrigationApi = {
  listValves: () => api.get('/irrigation/valves'),
  toggleValve: (id) => api.post(`/irrigation/valves/${id}/toggle`),
}

// 灌溉任务
export const irrigationTasksApi = {
  list: (params) => api.get('/irrigation/tasks', { params }),
  get: (id) => api.get(`/irrigation/tasks/${id}`),
  create: (data) => api.post('/irrigation/tasks', data),
  delete: (id) => api.delete(`/irrigation/tasks/${id}`),
}

// 农事记录
export const farmlogApi = {
  list: (params) => api.get('/farmlog', { params }),
  get: (id) => api.get(`/farmlog/${id}`),
  create: (data) => api.post('/farmlog', data),
  update: (id, data) => api.put(`/farmlog/${id}`, data),
  delete: (id) => api.delete(`/farmlog/${id}`),
}

// 农机订单
export const ordersApi = {
  list: (params) => api.get('/machinery/orders', { params }),
  get: (id) => api.get(`/machinery/orders/${id}`),
  create: (data) => api.post('/machinery/orders', data),
  accept: (id) => api.post(`/machinery/orders/${id}/accept`),
  cancel: (id) => api.post(`/machinery/orders/${id}/cancel`),
  pay: (id) => api.post(`/machinery/orders/${id}/pay`),
  confirmComplete: (id) => api.post(`/machinery/orders/${id}/confirm-complete`),
  getTrace: (id) => api.get(`/machinery/orders/${id}/trace`),
  newQuote: (id, data) => api.post(`/machinery/orders/${id}/new-quote`, data || {}),
  simulateStatus: (id, status) => api.post(`/machinery/orders/${id}/simulate/${status}`),
}

// 指导建议
export const guidanceApi = {
  list: (params) => api.get('/guidance', { params }),
  get: (id) => api.get(`/guidance/${id}`),
  create: (data) => api.post('/guidance', data),
}

// 巡田报告
export const patrolReportsApi = {
  list: (params) => api.get('/patrol/reports', { params }),
  get: (id) => api.get(`/patrol/reports/${id}`),
}

// 钱包
export const walletApi = {
  get: () => api.get('/wallet'),
  addAccount: (data) => api.post('/wallet/accounts', data),
  withdraw: (amount, accountId) => api.post('/wallet/withdraw', { amount, accountId }),
}

export default api
