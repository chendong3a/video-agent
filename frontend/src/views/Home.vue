<template>
  <div class="home">
    <van-nav-bar title="视频智能体" fixed />
    
    <div class="content">
      <div class="hero">
        <h1>🎬 视频智能体</h1>
        <p>AI驱动的视频内容再创作</p>
      </div>

      <div class="features">
        <div class="feature-card">
          <div class="icon">📹</div>
          <h3>视频分析</h3>
          <p>支持B站、抖音视频链接</p>
        </div>
        <div class="feature-card">
          <div class="icon">✍️</div>
          <h3>文案生成</h3>
          <p>AI生成多风格口播文案</p>
        </div>
        <div class="feature-card">
          <div class="icon">🎤</div>
          <h3>声音克隆</h3>
          <p>克隆你的声音进行配音</p>
        </div>
        <div class="feature-card">
          <div class="icon">💋</div>
          <h3>口型对齐</h3>
          <p>智能匹配口型动作</p>
        </div>
      </div>

      <van-button 
        type="primary" 
        size="large" 
        round 
        block
        @click="goCreate"
        class="create-btn"
      >
        开始创作
      </van-button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goCreate = () => {
  router.push('/create')
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.content {
  padding: 70px 20px 20px;
}

.hero {
  text-align: center;
  color: white;
  margin-bottom: 40px;
}

.hero h1 {
  font-size: 32px;
  margin-bottom: 10px;
}

.hero p {
  font-size: 16px;
  opacity: 0.9;
}

.features {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-bottom: 40px;
}

.feature-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.feature-card .icon {
  font-size: 36px;
  margin-bottom: 10px;
}

.feature-card h3 {
  font-size: 16px;
  margin-bottom: 5px;
  color: #323233;
}

.feature-card p {
  font-size: 12px;
  color: #969799;
}

.create-btn {
  margin-top: 20px;
}
</style>
