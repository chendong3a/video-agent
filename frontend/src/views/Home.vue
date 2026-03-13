<template>
  <div class="home">
    <div class="bg-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>

    <div class="content">
      <div class="hero">
        <div class="logo-wrap">
          <span class="logo-icon">🎬</span>
        </div>
        <h1>视频智能体</h1>
        <p class="subtitle">AI驱动的视频内容再创作平台</p>
      </div>

      <div class="stats-bar">
        <div class="stat-item">
          <span class="stat-num">5</span>
          <span class="stat-label">AI模块</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-num">4</span>
          <span class="stat-label">文案风格</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-num">∞</span>
          <span class="stat-label">创作可能</span>
        </div>
      </div>

      <div class="features">
        <div class="feature-card" v-for="feature in features" :key="feature.title">
          <div class="feature-icon">{{ feature.icon }}</div>
          <div class="feature-info">
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.desc }}</p>
          </div>
          <div class="feature-arrow">›</div>
        </div>
      </div>

      <div class="flow-section">
        <h2 class="section-title">工作流程</h2>
        <div class="flow-steps">
          <div class="flow-step" v-for="(step, i) in flowSteps" :key="i">
            <div class="step-dot" :style="{ background: step.color }">{{ i + 1 }}</div>
            <span class="step-text">{{ step.text }}</span>
          </div>
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
        <span>✨ 开始创作</span>
      </van-button>

      <p class="tip-text">支持B站、抖音视频链接 · 一键生成口播视频</p>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const goCreate = () => router.push('/create')

const features = [
  { icon: '📹', title: '智能视频分析', desc: '自动提取视频核心内容和转录文本' },
  { icon: '✍️', title: '多风格文案', desc: '专业/幽默/情感/带货 四种风格任选' },
  { icon: '🎤', title: '声音克隆', desc: '上传声音样本，AI克隆你的声音' },
  { icon: '💋', title: '口型对齐', desc: '智能匹配口型，效果自然逼真' },
  { icon: '🎬', title: '一键合成', desc: '字幕+标题+BGM 自动合成成片' }
]

const flowSteps = [
  { text: '粘贴链接', color: '#667eea' },
  { text: '分析内容', color: '#764ba2' },
  { text: '生成文案', color: '#f093fb' },
  { text: '克隆配音', color: '#4facfe' },
  { text: '输出成片', color: '#43e97b' }
]
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: #0f0c29;
  position: relative;
  overflow: hidden;
}

.bg-decoration {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.5;
}

.circle-1 {
  width: 300px;
  height: 300px;
  background: #667eea;
  top: -80px;
  right: -60px;
}

.circle-2 {
  width: 250px;
  height: 250px;
  background: #764ba2;
  bottom: 200px;
  left: -80px;
}

.circle-3 {
  width: 200px;
  height: 200px;
  background: #f093fb;
  bottom: -50px;
  right: 30px;
  opacity: 0.3;
}

.content {
  position: relative;
  z-index: 1;
  padding: 60px 20px 100px;
}

.hero {
  text-align: center;
  margin-bottom: 30px;
}

.logo-wrap {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 72px;
  height: 72px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  margin-bottom: 16px;
}

.logo-icon {
  font-size: 36px;
}

.hero h1 {
  font-size: 28px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 8px;
  letter-spacing: 2px;
}

.subtitle {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
}

.stats-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 16px 24px;
  margin-bottom: 28px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.stat-num {
  font-size: 24px;
  font-weight: 700;
  color: #fff;
}

.stat-label {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.5);
  margin-top: 4px;
}

.stat-divider {
  width: 1px;
  height: 28px;
  background: rgba(255, 255, 255, 0.15);
}

.features {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 32px;
}

.feature-card {
  display: flex;
  align-items: center;
  gap: 14px;
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 16px;
  transition: all 0.3s;
}

.feature-card:active {
  transform: scale(0.98);
  background: rgba(255, 255, 255, 0.1);
}

.feature-icon {
  font-size: 28px;
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 12px;
}

.feature-info {
  flex: 1;
}

.feature-info h3 {
  font-size: 15px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 3px;
}

.feature-info p {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.45);
}

.feature-arrow {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.2);
  flex-shrink: 0;
}

.flow-section {
  margin-bottom: 32px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 16px;
}

.flow-steps {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 20px 12px;
}

.flow-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.step-dot {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: #fff;
}

.step-text {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.5);
  white-space: nowrap;
}

.create-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  height: 50px;
  font-size: 17px;
  font-weight: 600;
  letter-spacing: 1px;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
}

.create-btn:active {
  transform: scale(0.98);
}

.tip-text {
  text-align: center;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.3);
  margin-top: 16px;
}
</style>
