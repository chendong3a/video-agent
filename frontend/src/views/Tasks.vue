<template>
  <div class="tasks">
    <van-nav-bar title="我的任务" fixed />
    
    <div class="content">
      <van-empty 
        v-if="tasks.length === 0" 
        description="暂无任务"
      />
      
      <div v-else class="task-list">
        <div 
          v-for="task in tasks" 
          :key="task.id"
          class="task-card"
          @click="goDetail(task.id)"
        >
          <div class="task-header">
            <span class="task-id">#{{ task.id }}</span>
            <van-tag :type="getStatusType(task.status)">
              {{ getStatusText(task.status) }}
            </van-tag>
          </div>
          
          <div class="task-info">
            <p class="task-url">{{ task.videoUrl }}</p>
            <p class="task-time">{{ task.createTime }}</p>
          </div>
          
          <van-progress 
            v-if="task.status === 'processing'"
            :percentage="task.progress" 
            stroke-width="6"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()
const tasks = ref([])

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

const goDetail = (id) => {
  router.push(`/task/${id}`)
}

onMounted(async () => {
  // TODO: 加载任务列表
  tasks.value = []
})
</script>

<style scoped>
.tasks {
  min-height: 100vh;
  background-color: #f7f8fa;
}

.content {
  padding: 56px 16px 20px;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.task-card {
  background: white;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.task-id {
  font-weight: bold;
  color: #323233;
}

.task-info {
  margin-bottom: 12px;
}

.task-url {
  font-size: 14px;
  color: #646566;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.task-time {
  font-size: 12px;
  color: #969799;
}
</style>
