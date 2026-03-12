# 视频智能体 - 项目结构说明

## 整体架构

```
video-agent/
├── backend/                    # Python后端服务
├── frontend/                   # Vue3 PWA前端
├── models/                     # AI模型文件（需自行下载）
├── storage/                    # 文件存储目录
│   ├── uploads/               # 用户上传文件
│   ├── outputs/               # 生成的视频
│   └── temp/                  # 临时文件
├── docker-compose.yml         # Docker编排配置
├── DEPLOYMENT.md              # 部署文档
└── README.md                  # 项目说明
```

---

## 后端结构 (backend/)

```
backend/
├── main.py                    # FastAPI入口
├── config.py                  # 配置管理
├── celery_app.py             # Celery配置
├── requirements.txt          # Python依赖
├── .env.example              # 环境变量模板
├── Dockerfile                # Docker镜像
│
├── api/                      # API接口层
│   ├── __init__.py
│   └── routes/               # 路由模块
│       ├── __init__.py
│       ├── health.py         # 健康检查
│       ├── task.py           # 任务管理
│       └── file.py           # 文件管理
│
├── modules/                  # AI功能模块
│   ├── __init__.py
│   ├── video_analyzer/       # 视频分析（BiliNote）
│   │   ├── __init__.py
│   │   └── bilinote_client.py
│   ├── script_generator/     # 文案生成（MiniMax）
│   │   ├── __init__.py
│   │   └── minimax_client.py
│   ├── voice_cloner/         # 声音克隆（CosyVoice3）
│   │   ├── __init__.py
│   │   └── cosyvoice_client.py
│   ├── lip_sync/             # 口型对齐（MuseTalk）
│   │   ├── __init__.py
│   │   └── musetalk_client.py
│   └── composer/             # 视频合成
│       ├── __init__.py
│       ├── subtitle_generator.py
│       └── video_composer.py
│
└── tasks/                    # Celery异步任务
    ├── __init__.py
    └── pipeline.py           # 完整流水线
```

### 核心模块说明

#### 1. API层 (api/)
- **health.py**: 健康检查和版本信息
- **task.py**: 任务创建、状态查询、结果获取
- **file.py**: 文件上传下载

#### 2. AI模块 (modules/)
- **video_analyzer**: 调用BiliNote分析视频，返回Markdown格式内容
- **script_generator**: 调用MiniMax API生成口播文案
- **voice_cloner**: 使用CosyVoice3克隆声音
- **lip_sync**: 使用MuseTalk进行口型对齐
- **composer**: 字幕生成、BGM混音、视频合成

#### 3. 任务流水线 (tasks/)
- **pipeline.py**: 定义完整的视频生成流程
  - Step 1: 视频分析
  - Step 2: 文案生成
  - Step 3: 声音克隆
  - Step 4: 口型对齐
  - Step 5: 后期合成

---

## 前端结构 (frontend/)

```
frontend/
├── index.html                # HTML入口
├── package.json              # NPM依赖
├── vite.config.js            # Vite配置（含PWA）
│
└── src/
    ├── main.js               # Vue入口
    ├── App.vue               # 根组件
    │
    ├── router/               # 路由配置
    │   └── index.js
    │
    ├── api/                  # API服务层
    │   └── index.js          # Axios封装
    │
    └── views/                # 页面组件
        ├── Home.vue          # 首页
        ├── Create.vue        # 创建任务
        ├── Tasks.vue         # 任务列表
        ├── TaskDetail.vue    # 任务详情
        └── Profile.vue       # 个人中心
```

### 页面说明

#### 1. Home.vue - 首页
- 展示功能特性
- 引导用户开始创作

#### 2. Create.vue - 创建任务
- 输入视频URL
- 上传声音样本和底片视频
- 选择文案风格
- 提交任务

#### 3. Tasks.vue - 任务列表
- 显示所有任务
- 任务状态标识
- 进度显示

#### 4. TaskDetail.vue - 任务详情
- 实时进度更新（轮询）
- 步骤状态展示
- 结果预览和下载

#### 5. Profile.vue - 个人中心
- 使用说明
- 关于信息

---

## 数据流程

```
用户操作 (PWA前端)
    ↓
FastAPI接口
    ↓
Celery任务队列 (Redis)
    ↓
AI处理流水线
    ↓
    ├─ BiliNote → 视频分析
    ├─ MiniMax → 文案生成
    ├─ CosyVoice3 → 声音克隆
    ├─ MuseTalk → 口型对齐
    └─ FFmpeg/MoviePy → 后期合成
    ↓
存储到 storage/outputs/
    ↓
返回结果给前端
```

---

## 技术栈总结

### 后端
- **Web框架**: FastAPI
- **任务队列**: Celery + Redis
- **视频处理**: FFmpeg, MoviePy
- **AI模型**: 
  - BiliNote (视频分析)
  - MiniMax (LLM文案生成)
  - CosyVoice3 (声音克隆)
  - MuseTalk (口型对齐)
  - faster-whisper (语音识别)

### 前端
- **框架**: Vue 3 + Vite
- **UI库**: Vant 4 (移动端)
- **状态管理**: Pinia
- **路由**: Vue Router
- **PWA**: vite-plugin-pwa

### 部署
- **容器化**: Docker + Docker Compose
- **GPU支持**: NVIDIA Docker Runtime
- **反向代理**: Nginx (可选)
- **进程管理**: Supervisor (可选)

---

## 开发规范

### 代码风格
- Python: PEP 8
- JavaScript: ESLint + Prettier
- Vue: Vue 3 Composition API

### 提交规范
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式
- refactor: 重构
- test: 测试
- chore: 构建/工具

---

## 扩展建议

### 功能扩展
1. 支持更多视频平台（YouTube、小红书等）
2. 添加用户认证系统
3. 任务队列优先级管理
4. 批量处理功能
5. 视频模板库

### 性能优化
1. 模型量化加速
2. 分布式任务处理
3. CDN加速静态资源
4. 数据库持久化任务记录
5. 缓存策略优化

### 监控运维
1. Prometheus + Grafana 监控
2. ELK日志分析
3. Sentry错误追踪
4. 自动化测试
5. CI/CD流水线
