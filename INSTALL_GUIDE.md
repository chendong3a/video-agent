# 快速安装指南 (Windows)

## 立即安装 Redis 和 FFmpeg

### 方案 A: 使用 Docker (推荐，最快)

#### 1. 安装 Docker Desktop
如果还没有安装 Docker:
- 下载: https://www.docker.com/products/docker-desktop/
- 安装后重启电脑

#### 2. 启动 Redis
```bash
docker run -d --name video-agent-redis -p 6379:6379 redis:7-alpine
```

验证:
```bash
docker ps
# 应该看到 redis 容器在运行
```

---

### 方案 B: 直接安装 (如果不想用 Docker)

#### 1. 安装 Redis (Memurai)
```
1. 下载 Memurai: https://www.memurai.com/get-memurai
2. 运行安装程序
3. 安装完成后，Redis 会自动启动
```

验证:
```bash
redis-cli ping
# 应该返回 PONG
```

#### 2. 安装 FFmpeg
```
1. 下载 FFmpeg: https://www.gyan.dev/ffmpeg/builds/
   - 选择 "ffmpeg-release-full.7z"
2. 解压到 C:\ffmpeg
3. 添加到系统 PATH:
   - 右键"此电脑" → 属性 → 高级系统设置
   - 环境变量 → 系统变量 → Path → 编辑
   - 新建 → 输入: C:\ffmpeg\bin
   - 确定保存
4. 重启终端
```

验证:
```bash
ffmpeg -version
# 应该显示版本信息
```

---

## 安装项目依赖

### 1. 后端依赖
```bash
cd video-agent/backend
pip install -r requirements.txt
```

### 2. 前端依赖
```bash
cd video-agent/frontend
npm install
```

---

## 测试服务

### 1. 测试 Redis
```bash
redis-cli ping
```

### 2. 测试 FastAPI
```bash
cd video-agent/backend
python main.py
```
访问: http://localhost:8000/api/health

### 3. 测试前端
```bash
cd video-agent/frontend
npm run dev
```
访问: http://localhost:5173

---

## 预计时间
- Docker 方式: 10-15分钟
- 直接安装: 20-30分钟
