<template>
  <div class="create">
    <van-nav-bar 
      title="创建任务" 
      left-arrow 
      @click-left="$router.back()"
      fixed
      :border="false"
      class="nav-dark"
    />
    
    <div class="content">
      <!-- Step 1: 视频链接 -->
      <div class="section">
        <div class="section-header">
          <span class="step-badge">1</span>
          <h3>视频链接</h3>
        </div>
        <div class="input-wrap">
          <van-field
            v-model="form.videoUrl"
            placeholder="粘贴B站或抖音视频链接"
            clearable
            class="dark-input"
          />
          <van-button 
            size="small" 
            type="primary" 
            :loading="analyzing"
            :disabled="!form.videoUrl"
            @click="onAnalyze"
            class="analyze-btn"
          >
            {{ analyzing ? '分析中' : '分析' }}
          </van-button>
        </div>
        
        <!-- 分析结果预览 -->
        <div v-if="analysisResult" class="analysis-preview">
          <div class="preview-header">
            <span class="preview-tag">{{ analysisResult.platform }}</span>
            <span class="preview-duration">{{ formatDuration(analysisResult.duration) }}</span>
          </div>
          <h4>{{ analysisResult.title }}</h4>
          <p class="preview-summary">{{ analysisResult.summary }}</p>
          <div v-if="analysisResult.key_points?.length" class="preview-points">
            <span v-for="(p, i) in analysisResult.key_points.slice(0, 3)" :key="i" class="point-tag">
              {{ p.slice(0, 20) }}{{ p.length > 20 ? '...' : '' }}
            </span>
          </div>
        </div>
      </div>

      <!-- Step 2: 文案风格 -->
      <div class="section">
        <div class="section-header">
          <span class="step-badge">2</span>
          <h3>文案风格</h3>
        </div>
        <div class="style-grid">
          <div 
            v-for="s in styles" 
            :key="s.value"
            class="style-card"
            :class="{ active: form.scriptStyle === s.value }"
            @click="form.scriptStyle = s.value"
          >
            <span class="style-icon">{{ s.icon }}</span>
            <span class="style-name">{{ s.label }}</span>
            <span class="style-desc">{{ s.desc }}</span>
          </div>
        </div>
        
        <!-- 文案预览 -->
        <van-button 
          v-if="analysisResult"
          size="small" 
          plain 
          type="primary"
          :loading="generatingScript"
          @click="onPreviewScript"
          class="preview-script-btn"
        >
          {{ generatingScript ? '生成中...' : '预览文案' }}
        </van-button>
        
        <div v-if="scriptPreview" class="script-preview">
          <div class="script-header">
            <span>{{ scriptPreview.style_name }}</span>
            <span class="script-meta">{{ scriptPreview.word_count }}字 · 约{{ scriptPreview.estimated_duration }}秒</span>
          </div>
          <p>{{ scriptPreview.script }}</p>
        </div>
      </div>

      <!-- Step 3: 上传文件 -->
      <div class="section">
        <div class="section-header">
          <span class="step-badge">3</span>
          <h3>上传素材</h3>
        </div>
        
        <div class="upload-row">
          <div class="upload-item">
            <div class="upload-label">🎤 声音样本</div>
            <van-uploader 
              v-model="voiceFile" 
              :max-count="1"
              accept="audio/*"
              :after-read="() => {}"
            >
              <div class="upload-trigger">
                <span>{{ voiceFile.length ? '已选择' : '点击上传' }}</span>
              </div>
            </van-uploader>
          </div>
          <div class="upload-item">
            <div class="upload-label">📹 底片视频</div>
            <van-uploader 
              v-model="videoFile" 
              :max-count="1"
              accept="video/*"
              :after-read="() => {}"
            >
              <div class="upload-trigger">
                <span>{{ videoFile.length ? '已选择' : '点击上传' }}</span>
              </div>
            </van-uploader>
          </div>
        </div>
      </div>

      <!-- 提交按钮 -->
      <van-button 
        round 
        block 
        type="primary" 
        :loading="submitting"
        :disabled="!canSubmit"
        @click="onSubmit"
        class="submit-btn"
      >
        ✨ 开始生成视频
      </van-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import api from '../api'

const router = useRouter()

const form = ref({
  videoUrl: '',
  scriptStyle: 'professional'
})

const voiceFile = ref([])
const videoFile = ref([])
const analyzing = ref(false)
const generatingScript = ref(false)
const submitting = ref(false)
const analysisResult = ref(null)
const scriptPreview = ref(null)

const styles = [
  { value: 'professional', label: '专业', icon: '🎓', desc: '严谨有深度' },
  { value: 'funny', label: '幽默', icon: '😄', desc: '轻松有趣' },
  { value: 'emotional', label: '情感', icon: '💖', desc: '走心共鸣' },
  { value: 'sales', label: '带货', icon: '🔥', desc: '激发购买' }
]

const canSubmit = computed(() => {
  return form.value.videoUrl && voiceFile.value.length > 0 && videoFile.value.length > 0
})

const formatDuration = (seconds) => {
  if (!seconds) return ''
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${m}:${String(s).padStart(2, '0')}`
}

const onAnalyze = async () => {
  if (!form.value.videoUrl) return
  analyzing.value = true
  analysisResult.value = null
  scriptPreview.value = null
  
  try {
    const res = await api.analyzeVideo(form.value.videoUrl)
    analysisResult.value = res.data
    showToast('分析完成')
  } catch (e) {
    showToast('分析失败: ' + e.message)
  } finally {
    analyzing.value = false
  }
}

const onPreviewScript = async () => {
  if (!analysisResult.value) return
  generatingScript.value = true
  scriptPreview.value = null
  
  try {
    const content = analysisResult.value.markdown || analysisResult.value.summary
    const res = await api.generateScript(content, form.value.scriptStyle)
    scriptPreview.value = res.data
  } catch (e) {
    showToast('文案生成失败: ' + e.message)
  } finally {
    generatingScript.value = false
  }
}

const onSubmit = async () => {
  submitting.value = true
  
  try {
    await api.uploadVoice(voiceFile.value[0].file)
    await api.uploadVideo(videoFile.value[0].file)
    
    const result = await api.createTask({
      videoUrl: form.value.videoUrl,
      scriptStyle: form.value.scriptStyle
    })
    
    showToast('任务创建成功')
    router.push(`/task/${result.task_id}`)
  } catch (e) {
    showToast('创建失败: ' + e.message)
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.create {
  min-height: 100vh;
  background: #0f0c29;
}

.nav-dark {
  background: rgba(15, 12, 41, 0.9) !important;
  backdrop-filter: blur(10px);
}

.nav-dark :deep(.van-nav-bar__title) {
  color: #fff;
}

.nav-dark :deep(.van-nav-bar__arrow) {
  color: #fff;
}

.content {
  padding: 60px 16px 100px;
}

.section {
  margin-bottom: 24px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.step-badge {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  font-size: 13px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.section-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #fff;
}

.input-wrap {
  display: flex;
  gap: 8px;
  align-items: stretch;
}

.dark-input {
  flex: 1;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.dark-input :deep(.van-field__control) {
  color: #fff;
}

.dark-input :deep(.van-field__control::placeholder) {
  color: rgba(255, 255, 255, 0.3);
}

.analyze-btn {
  border-radius: 10px;
  min-width: 70px;
}

.analysis-preview {
  margin-top: 12px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 14px;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.preview-tag {
  background: rgba(102, 126, 234, 0.3);
  color: #a5b4fc;
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 4px;
}

.preview-duration {
  color: rgba(255, 255, 255, 0.4);
  font-size: 12px;
}

.analysis-preview h4 {
  color: #fff;
  font-size: 14px;
  margin-bottom: 6px;
}

.preview-summary {
  color: rgba(255, 255, 255, 0.5);
  font-size: 12px;
  line-height: 1.6;
  margin-bottom: 8px;
}

.preview-points {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.point-tag {
  background: rgba(255, 255, 255, 0.06);
  color: rgba(255, 255, 255, 0.5);
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 4px;
}

.style-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.style-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 16px 8px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.style-card.active {
  background: rgba(102, 126, 234, 0.15);
  border-color: rgba(102, 126, 234, 0.5);
}

.style-icon {
  font-size: 28px;
}

.style-name {
  font-size: 14px;
  font-weight: 600;
  color: #fff;
}

.style-desc {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.4);
}

.preview-script-btn {
  margin-top: 12px;
  border-radius: 8px;
}

.script-preview {
  margin-top: 12px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 14px;
}

.script-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  color: #a5b4fc;
  font-size: 12px;
}

.script-meta {
  color: rgba(255, 255, 255, 0.4);
}

.script-preview p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 13px;
  line-height: 1.8;
}

.upload-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.upload-item {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 16px;
  text-align: center;
}

.upload-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 10px;
}

.upload-trigger {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
  background: rgba(102, 126, 234, 0.15);
  border: 1px dashed rgba(102, 126, 234, 0.4);
  border-radius: 8px;
  color: #a5b4fc;
  font-size: 13px;
  cursor: pointer;
}

.submit-btn {
  margin-top: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  height: 50px;
  font-size: 17px;
  font-weight: 600;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
}
</style>
