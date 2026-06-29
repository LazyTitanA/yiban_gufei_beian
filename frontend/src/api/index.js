import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// 请求拦截器：自动附加 token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器：统一处理错误
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      const { status, data } = error.response
      if (status === 401) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        ElMessage.error('登录已过期，请重新登录')
        setTimeout(() => { window.location.href = '/login' }, 1500)
      } else if (data) {
        // 提取错误信息
        const msg = typeof data === 'string' ? data
          : data.error || data.detail || Object.values(data).flat().join('；')
        ElMessage.error(msg || '请求失败')
      }
    } else {
      ElMessage.error('网络错误，请检查网络连接')
    }
    return Promise.reject(error)
  }
)

// ==================== 认证 ====================

export function register(data) {
  return api.post('/register/', data)
}

export function login(data) {
  return api.post('/login/', data)
}

export function getMe() {
  return api.get('/me/')
}

// ==================== 统计 ====================

export function getStats() {
  return api.get('/stats/')
}

// ==================== 备案申请 ====================

export function getApplications(params) {
  return api.get('/applications/', { params })
}

export function getApplication(id) {
  return api.get(`/applications/${id}/`)
}

export function createApplication(data) {
  return api.post('/applications/', data)
}

export function updateApplication(id, data) {
  return api.patch(`/applications/${id}/`, data)
}

export function submitApplication(id) {
  return api.post(`/applications/${id}/submit/`)
}

export function uploadFile(applicationId, fileType, file) {
  const formData = new FormData()
  formData.append('file_type', fileType)
  formData.append('file', file)
  return api.post(`/applications/${applicationId}/upload_file/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export function deleteFile(applicationId, fileId) {
  return api.delete(`/applications/${applicationId}/files/${fileId}/`)
}

export function getAIReview(applicationId) {
  return api.get(`/applications/${applicationId}/ai_review_result/`)
}

// ==================== 管理员 ====================

export function reviewApplication(applicationId, data) {
  return api.post(`/applications/${applicationId}/review/`, data)
}

export default api