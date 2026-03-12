import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 60000
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 可以在这里添加token等
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    return Promise.reject(error)
  }
)

export default {
  // 创建任务
  async createTask(data) {
    const formData = new FormData()
    formData.append('video_url', data.videoUrl)
    formData.append('script_style', data.scriptStyle)
    return api.post('/task/create', formData)
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
  }
}
