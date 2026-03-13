# 视频智能体 - 开发计划

## 项目状态
- **当前阶段**: Day 2 - BiliNote + MiniMax + 前端UI (已完成)
- **开始日期**: 2026-03-12
- **交付日期**: 2026-03-20 (8天冲刺)
- **GitHub**: https://github.com/chendong3a/video-agent
- **工作模式**: 每天10-12小时高强度开发

---

## 开发路线图

### ✅ Phase 0: 项目脚手架 (Day 1 - 已完成)
- [x] 创建项目目录结构
- [x] 后端 FastAPI + Celery 框架
- [x] 前端 Vue3 + PWA 框架
- [x] Docker 配置
- [x] 文档编写
- [x] Git 仓库创建并推送 GitHub

---

### ✅ Phase 1: 环境搭建与基础测试 (Day 1 - 已完成)

#### 1.1 系统环境
- [x] Python 3.10.10 ✅
- [x] Node.js v24.12.0 ✅
- [x] Redis (Memurai 4.1.2) ✅
- [x] FFmpeg 8.0.1 ✅
- [x] GPU RTX 5070 Ti + CUDA 13.0 ✅

#### 1.2 依赖安装
- [x] 后端 Python 依赖 (34个包)
- [x] 前端 NPM 依赖 (391个包)
- [x] setuptools 升级到 82.0.1
- [x] faster-whisper 升级到 >=1.0.0 (兼容 av 12)

#### 1.3 基础服务验证
- [x] FastAPI 服务加载成功 (14个路由)
- [x] 前端 Vite 构建成功 (361模块)
- [x] Redis (Memurai) PONG 验证通过
- [x] FFmpeg 命令行可用
- [x] .env 配置文件创建

#### 已知问题
- `stable-ts` 暂时跳过 (openai-whisper 构建问题，后期解决)

---

### ✅ Phase 2: BiliNote + MiniMax 集成 (Day 2 - 已完成)

#### 2.1 BiliNote 视频分析模块
- [x] 平台检测 (B站/抖音)
- [x] 视频ID提取 (BV号/av号/抖音ID)
- [x] API调用实现 + 错误处理
- [x] Markdown解析 (摘要/要点/章节提取)
- [x] 健康检查接口
- [x] 日志记录 (loguru)

#### 2.2 MiniMax 文案生成模块
- [x] 4种风格Prompt模板 (专业/幽默/情感/带货)
- [x] API调用实现
- [x] Mock数据 (API Key未配置时)
- [x] 批量生成所有风格
- [x] 字数/朗读时长预估
- [x] 自定义指令支持

#### 2.3 后端API路由重构
- [x] POST /api/task/analyze - 视频分析
- [x] POST /api/task/generate-script - 单风格文案生成
- [x] POST /api/task/generate-all-scripts - 批量文案生成
- [x] GET /api/task/list - 任务列表
- [x] POST /api/task/create - 创建任务
- [x] POST /api/task/upload/voice - 上传声音样本
- [x] POST /api/task/upload/video - 上传底片视频
- [x] GET /api/task/{id}/status - 任务状态
- [x] GET /api/task/{id}/result - 任务结果
- [x] DELETE /api/task/{id} - 取消任务

#### 2.4 前端UI重构
- [x] 首页暗色毛玻璃风格
- [x] 功能卡片列表
- [x] 工作流程展示
- [x] 统计数据栏
- [x] 创建任务页面 - 分步引导
- [x] 视频分析预览
- [x] 文案风格选择卡片 (2x2网格)
- [x] 文案预览功能
- [x] 前端API层更新

#### 代码统计
- Git提交: +1213 -235 行
- 7个文件修改

---

### 📋 Phase 3: 任务队列与状态管理 (Day 3 - 待开始)

#### 3.1 Celery 任务完善
- [ ] 完整流水线实现 (5步串联)
- [ ] 任务状态实时更新
- [ ] 进度推送 (WebSocket/SSE)
- [ ] 错误处理和重试机制

#### 3.2 文件管理
- [ ] 文件上传存储策略
- [ ] 临时文件清理机制
- [ ] 下载接口完善

#### 3.3 端到端流程打通
- [ ] 前后端联调
- [ ] 任务创建 → 状态查询 → 结果获取

---

### 🎤 Phase 4: CosyVoice3 声音克隆 (Day 4)

#### 4.1 模型部署
- [ ] 下载 CosyVoice3 模型
- [ ] 配置模型路径
- [ ] GPU 显存检查

#### 4.2 声音克隆实现
- [ ] 完善 cosyvoice_client.py
- [ ] 零样本克隆
- [ ] 长文本 TTS
- [ ] 音频后处理

---

### 💋 Phase 5: MuseTalk 口型对齐 (Day 5)

#### 5.1 模型部署
- [ ] 下载 MuseTalk 模型
- [ ] 配置模型路径

#### 5.2 口型对齐实现
- [ ] 完善 musetalk_client.py
- [ ] 人脸检测 + 口型生成
- [ ] 视频合成

---

### 🎬 Phase 6: 后期合成模块 (Day 6)

- [ ] faster-whisper 字幕生成
- [ ] FFmpeg 字幕烧录
- [ ] BGM 混音
- [ ] 标题叠加
- [ ] 最终合成输出

---

### 🎨 Phase 7: 前端完善 + 联调 (Day 7)

- [ ] 实时进度显示
- [ ] 结果预览下载
- [ ] 响应式布局优化
- [ ] PWA 功能完善

---

### 🚀 Phase 8: 优化 + 测试 + 部署 (Day 8)

- [ ] 端到端测试
- [ ] 性能优化
- [ ] Docker 镜像构建
- [ ] 文档完善

---

## 8天冲刺时间表

| 日期 | 任务 | 状态 |
|------|------|------|
| 3/12 (Day 1) | 环境搭建 + 项目脚手架 | ✅ 完成 |
| 3/13 (Day 2) | BiliNote + MiniMax + 前端UI | ✅ 完成 |
| 3/14 (Day 3) | 任务队列 + Celery流水线 | ⏳ 待开始 |
| 3/15 (Day 4) | CosyVoice3 声音克隆 | ⏳ |
| 3/16 (Day 5) | MuseTalk 口型对齐 | ⏳ |
| 3/17 (Day 6) | 后期合成 (字幕+标题+BGM) | ⏳ |
| 3/18 (Day 7) | 前端完善 + 联调 | ⏳ |
| 3/19 (Day 8) | 优化 + 测试 + 部署 | ⏳ |

---

## 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| 后端框架 | FastAPI | 0.109.0 |
| 任务队列 | Celery + Redis | 5.3.4 |
| 前端框架 | Vue3 + Vite | 5.4.21 |
| UI组件库 | Vant | 4.x |
| 视频分析 | BiliNote | - |
| 文案生成 | MiniMax API | abab6.5 |
| 声音克隆 | CosyVoice3 | - |
| 口型对齐 | MuseTalk | - |
| 视频处理 | FFmpeg + MoviePy | 8.0.1 |
| 语音识别 | faster-whisper | 1.2.1 |

---

**最后更新**: 2026-03-13 13:10
**状态**: Day 2 完成，进度正常
