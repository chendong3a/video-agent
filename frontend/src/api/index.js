import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 120000
})

api.interceptors.request.use(
  config => config,
  error => Promise.reject(error)
)

api.interceptors.response.use(
  response => response.data,
  error => {
    const msg = error.response?.data?.detail || error.message || '请求失败'
    return Promise.reject(new Error(msg))
  }
)

export default {
  // 创建任务
  async createTask(data) {
    const formData = new FormData()
    formData.append('video_url', data.videoUrl)
    formData.append('script_style', data.scriptStyle)
    formData.append('bgm_style', data.bgmStyle || 'auto')
    return api.post('/task/create', formData)
  },

  // 视频分析（预览）
  async analyzeVideo(videoUrl) {
    const formData = new FormData()
    formData.append('video_url', videoUrl)
    return api.post('/task/analyze', formData)
  },

  // 生成单个风格文案
  async generateScript(content, style = 'professional', maxLength = 500) {
    const formData = new FormData()
    formData.append('content', content)
    formData.append('style', style)
    formData.append('max_length', maxLength)
    return api.post('/task/generate-script', formData)
  },

  // 生成所有风格文案
  async generateAllScripts(content, maxLength = 500) {
    const formData = new FormData()
    formData.append('content', content)
    formData.append('max_length', maxLength)
    return api.post('/task/generate-all-scripts', formData)
  },

  // 上传声音样本
  async uploadVoice(file) {
    const formData = new FormData()
    formData.append('file', file)
    const result = await api.post('/task/upload/voice', formData)
    return result.file_id
  },

  // 上传底片视频
  async uploadVideo(file) {
    const formData = new FormData()
    formData.append('file', file)
    const result = await api.post('/task/upload/video', formData)
    return result.file_id
  },

  // 获取任务列表
  async getTaskList() {
    return api.get('/task/list')
  },

  // 获取任务状态
  async getTaskStatus(taskId) {
    return api.get(`/task/${taskId}/status`)
  },

  // 获取任务结果
  async getTaskResult(taskId) {
    return api.get(`/task/${taskId}/result`)
  },

  // 取消任务
  async cancelTask(taskId) {
    return api.delete(`/task/${taskId}`)
  },

  // 健康检查
  async healthCheck() {
    return api.get('/health')
  }
}
