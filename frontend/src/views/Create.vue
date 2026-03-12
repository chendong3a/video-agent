<template>
  <div class="create">
    <van-nav-bar 
      title="创建任务" 
      left-arrow 
      @click-left="$router.back()"
      fixed 
    />
    
    <div class="content">
      <van-form @submit="onSubmit">
        <van-cell-group inset>
          <van-field
            v-model="form.videoUrl"
            name="videoUrl"
            label="视频链接"
            placeholder="请输入B站或抖音视频链接"
            :rules="[{ required: true, message: '请输入视频链接' }]"
          />
          
          <van-field name="scriptStyle" label="文案风格">
            <template #input>
              <van-radio-group v-model="form.scriptStyle" direction="horizontal">
                <van-radio name="professional">专业</van-radio>
                <van-radio name="funny">幽默</van-radio>
                <van-radio name="emotional">情感</van-radio>
                <van-radio name="sales">带货</van-radio>
              </van-radio-group>
            </template>
          </van-field>
        </van-cell-group>

        <van-cell-group inset title="上传文件">
          <van-field name="voiceSample" label="声音样本">
            <template #input>
              <van-uploader 
                v-model="voiceFile" 
                :max-count="1"
                accept="audio/*"
              />
            </template>
          </van-field>
          
          <van-field name="baseVideo" label="底片视频">
            <template #input>
              <van-uploader 
                v-model="videoFile" 
                :max-count="1"
                accept="video/*"
              />
            </template>
          </van-field>
        </van-cell-group>

        <div style="margin: 16px;">
          <van-button 
            round 
            block 
            type="primary" 
            native-type="submit"
            :loading="loading"
          >
            开始生成
          </van-button>
        </div>
      </van-form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import api from '../api'

const router = useRouter()
const loading = ref(false)

const form = ref({
  videoUrl: '',
  scriptStyle: 'professional'
})

const voiceFile = ref([])
const videoFile = ref([])

const onSubmit = async () => {
  if (voiceFile.value.length === 0) {
    showToast('请上传声音样本')
    return
  }
  
  if (videoFile.value.length === 0) {
    showToast('请上传底片视频')
    return
  }

  loading.value = true
  
  try {
    // 上传文件
    const voiceId = await api.uploadVoice(voiceFile.value[0].file)
    const videoId = await api.uploadVideo(videoFile.value[0].file)
    
    // 创建任务
    const result = await api.createTask({
      videoUrl: form.value.videoUrl,
      scriptStyle: form.value.scriptStyle,
      voiceId,
      videoId
    })
    
    showToast('任务创建成功')
    router.push(`/task/${result.task_id}`)
  } catch (error) {
    showToast('创建失败: ' + error.message)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.create {
  min-height: 100vh;
  background-color: #f7f8fa;
}

.content {
  padding: 56px 0 20px;
}
</style>
