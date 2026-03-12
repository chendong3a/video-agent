<template>
  <div class="task-detail">
    <van-nav-bar 
      title="任务详情" 
      left-arrow 
      @click-left="$router.back()"
      fixed 
    />
    
    <div class="content">
      <van-loading v-if="loading" size="24px" vertical>加载中...</van-loading>
      
      <div v-else-if="task">
        <van-cell-group inset title="任务信息">
          <van-cell title="任务ID" :value="task.task_id" />
          <van-cell title="状态">
            <template #value>
              <van-tag :type="getStatusType(task.status)">
                {{ getStatusText(task.status) }}
              </van-tag>
            </template>
          </van-cell>
          <van-cell title="视频链接" :value="task.video_url" />
        </van-cell-group>

        <van-cell-group inset title="处理进度" v-if="task.status === 'processing'">
          <div class="progress-section">
            <van-progress 
              :percentage="task.progress" 
              stroke-width="8"
              color="#1989fa"
            />
            <p class="progress-text">{{ task.current_step }}</p>
            
            <div class="steps">
              <div 
                v-for="step in task.steps" 
                :key="step.name"
                class="step-item"
                :class="step.status"
              >
                <div class="step-icon">
                  <van-icon 
                    v-if="step.status === 'completed'" 
                    name="success" 
                    color="#07c160" 
                  />
                  <van-loading v-else-if="step.status === 'processing'" size="16px" />
                  <van-icon v-else name="circle" color="#dcdee0" />
                </div>
                <span class="step-name">{{ step.name }}</span>
              </div>
            </div>
          </div>
        </van-cell-group>

        <van-cell-group inset title="生成结果" v-if="task.status === 'completed'">
          <div class="result-section">
            <video 
              v-if="task.output_video_url"
              :src="task.output_video_url" 
              controls 
              class="result-video"
            />
            
            <van-cell title="文案内容" />
            <div class="script-content">{{ task.script }}</div>
            
            <van-button 
              type="primary" 
              block 
              round
              @click="downloadVideo"
            >
              下载视频
            </van-button>
          </div>
        </van-cell-group>

        <van-cell-group inset v-if="task.status === 'failed'">
          <van-empty description="任务失败" />
        </van-cell-group>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'

const route = useRoute()
const loading = ref(true)
const task = ref(null)
let pollTimer = null

const getStatusType = (status) => {
  const map = {
    pending: 'default',
    processing: 'primary',
    completed: 'success',
    failed: 'danger'
  }
  return map[status] || 'default'
}

const getStatusText = (status) => {
  const map = {
    pending: '等待中',
    processing: '处理中',
    completed: '已完成',
    failed: '失败'
  }
  return map[status] || status
}

const loadTask = async () => {
  try {
    const result = await api.getTaskStatus(route.params.id)
    task.value = result
    
    // 如果任务完成，获取结果
    if (result.status === 'completed') {
      const detailResult = await api.getTaskResult(route.params.id)
      task.value = { ...task.value, ...detailResult }
      stopPolling()
    }
  } catch (error) {
    console.error('加载任务失败:', error)
  } finally {
    loading.value = false
  }
}

const startPolling = () => {
  pollTimer = setInterval(() => {
    loadTask()
  }, 3000) // 每3秒轮询一次
}

const stopPolling = () => {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

const downloadVideo = () => {
  window.open(task.value.output_video_url, '_blank')
}

onMounted(() => {
  loadTask()
  startPolling()
})

onUnmounted(() => {
  stopPolling()
})
</script>

<style scoped>
.task-detail {
  min-height: 100vh;
  background-color: #f7f8fa;
}

.content {
  padding: 56px 0 20px;
}

.progress-section {
  padding: 16px;
}

.progress-text {
  text-align: center;
  margin-top: 12px;
  color: #646566;
  font-size: 14px;
}

.steps {
  margin-top: 24px;
}

.step-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
}

.step-icon {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
}

.step-name {
  font-size: 14px;
  color: #646566;
}

.step-item.completed .step-name {
  color: #07c160;
}

.step-item.processing .step-name {
  color: #1989fa;
  font-weight: bold;
}

.result-section {
  padding: 16px;
}

.result-video {
  width: 100%;
  border-radius: 8px;
  margin-bottom: 16px;
}

.script-content {
  padding: 16px;
  background: #f7f8fa;
  border-radius: 8px;
  margin: 12px 0 16px;
  line-height: 1.6;
  color: #323233;
}
</style>
