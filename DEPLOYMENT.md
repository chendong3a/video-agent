# 视频智能体 - 部署文档

## 环境要求

### 硬件要求
- GPU: NVIDIA 5070Ti / 3090 或更高
- 显存: 16GB+ (推荐24GB)
- 内存: 32GB+
- 硬盘: 100GB+ SSD

### 软件要求
- Python 3.10+
- Node.js 18+
- Redis 6+
- FFmpeg 4.4+
- CUDA 11.8+ (GPU驱动)

---

## 后端部署

### 1. 安装依赖

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装Python依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入配置：

```env
# MiniMax API
MINIMAX_API_KEY=your_api_key
MINIMAX_GROUP_ID=your_group_id

# BiliNote服务地址
BILINOTE_API_URL=http://localhost:8001

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 3. 下载AI模型

```bash
# 创建模型目录
mkdir -p models

# 下载CosyVoice3模型
cd models
git clone https://github.com/FunAudioLLM/CosyVoice cosyvoice3

# 下载MuseTalk模型
git clone https://github.com/TMElyralab/MuseTalk musetalk
```

### 4. 启动Redis

```bash
redis-server
```

### 5. 启动Celery Worker

```bash
celery -A celery_app worker --loglevel=info --pool=solo
```

### 6. 启动FastAPI服务

```bash
python main.py
```

后端服务将运行在 `http://localhost:8000`

---

## 前端部署

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 开发模式

```bash
npm run dev
```

前端将运行在 `http://localhost:5173`

### 3. 生产构建

```bash
npm run build
```

构建产物在 `dist/` 目录，可部署到任何静态服务器。

---

## BiliNote部署

### 1. 克隆BiliNote项目

```bash
git clone https://github.com/JefferyHcool/BiliNote
cd BiliNote
```

### 2. 按照BiliNote文档部署

参考 BiliNote 的 README.md 进行部署，确保服务运行在 `http://localhost:8001`

---

## Docker部署（推荐）

### 1. 创建 docker-compose.yml

```yaml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - REDIS_HOST=redis
      - MINIMAX_API_KEY=${MINIMAX_API_KEY}
    volumes:
      - ./backend:/app
      - ./models:/app/models
      - ./storage:/app/storage
    depends_on:
      - redis
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  celery:
    build: ./backend
    command: celery -A celery_app worker --loglevel=info
    environment:
      - REDIS_HOST=redis
    volumes:
      - ./backend:/app
      - ./models:/app/models
      - ./storage:/app/storage
    depends_on:
      - redis
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  frontend:
    build: ./frontend
    ports:
      - "5173:80"
    depends_on:
      - backend

volumes:
  redis_data:
```

### 2. 启动服务

```bash
docker-compose up -d
```

---

## 生产环境优化

### 1. 使用Nginx反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端
    location / {
        root /var/www/video-agent/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. 使用Supervisor管理进程

```ini
[program:video-agent-api]
command=/path/to/venv/bin/python main.py
directory=/path/to/backend
autostart=true
autorestart=true

[program:video-agent-celery]
command=/path/to/venv/bin/celery -A celery_app worker --loglevel=info
directory=/path/to/backend
autostart=true
autorestart=true
```

---

## 常见问题

### Q: GPU内存不足
A: 调整模型批处理大小，或使用更小的模型版本

### Q: Celery任务超时
A: 增加 `task_time_limit` 配置

### Q: 视频处理失败
A: 检查FFmpeg是否正确安装，确保有足够的磁盘空间

---

## 监控与日志

### 查看日志

```bash
# FastAPI日志
tail -f logs/api.log

# Celery日志
tail -f logs/celery.log
```

### 监控Celery

```bash
celery -A celery_app flower
```

访问 `http://localhost:5555` 查看任务状态

---

## 性能优化建议

1. 使用SSD存储临时文件
2. 启用Redis持久化
3. 配置Celery并发数（根据GPU数量）
4. 使用CDN加速前端资源
5. 定期清理临时文件和过期任务

---

## 安全建议

1. 使用HTTPS
2. 限制API访问频率
3. 验证上传文件类型和大小
4. 定期更新依赖包
5. 不要在代码中硬编码API密钥
