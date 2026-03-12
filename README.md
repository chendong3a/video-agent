# 视频智能体项目 (Video Agent)

## 项目简介

一个端到端的视频内容再创作智能体，支持从视频URL分析内容，生成新文案，克隆声音，口型对齐，最终输出带字幕、标题、BGM的完整视频。

## 技术栈

### 后端
- **FastAPI** - Web框架
- **Celery + Redis** - 异步任务队列
- **Python 3.10+**

### AI模块
- **BiliNote** - B站/抖音视频分析
- **MiniMax API** - LLM文案生成
- **CosyVoice3** - 声音克隆
- **MuseTalk** - 口型对齐
- **FFmpeg + MoviePy** - 视频合成

### 前端
- **Vue3 + Vite** - PWA应用
- **Vant** - 移动端UI组件库

## 功能流程

```
视频URL → BiliNote分析 → MiniMax生成文案 → CosyVoice3声音克隆 
→ MuseTalk口型对齐 → 字幕+标题+BGM → 成片输出
```

## 快速开始

### 后端启动
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 前端启动
```bash
cd frontend
npm install
npm run dev
```

## 项目结构

详见各目录下的 README.md
