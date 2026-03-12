<template>
  <div class="profile">
    <van-nav-bar title="我的" fixed />
    
    <div class="content">
      <div class="user-info">
        <van-icon name="user-circle-o" size="60" color="#1989fa" />
        <p class="username">用户</p>
      </div>

      <van-cell-group inset>
        <van-cell title="使用说明" is-link @click="showHelp" />
        <van-cell title="关于" is-link @click="showAbout" />
      </van-cell-group>
    </div>
  </div>
</template>

<script setup>
import { showDialog } from 'vant'

const showHelp = () => {
  showDialog({
    title: '使用说明',
    message: `
1. 输入B站或抖音视频链接
2. 上传10-30秒的声音样本
3. 上传底片视频（人物出镜但嘴不动）
4. 选择文案风格
5. 等待AI生成完成
6. 下载成片
    `,
    confirmButtonText: '知道了'
  })
}

const showAbout = () => {
  showDialog({
    title: '关于',
    message: '视频智能体 v1.0.0\n\nAI驱动的视频内容再创作工具',
    confirmButtonText: '确定'
  })
}
</script>

<style scoped>
.profile {
  min-height: 100vh;
  background-color: #f7f8fa;
}

.content {
  padding: 56px 0 20px;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 0;
  background: white;
  margin-bottom: 12px;
}

.username {
  margin-top: 12px;
  font-size: 18px;
  font-weight: bold;
  color: #323233;
}
</style>
