# ⚠️ 紧急安装说明

## 当前状态
- ✅ Python 3.10 已就绪
- ✅ Node.js v24.12.0 已就绪
- ✅ GPU RTX 5070 Ti + CUDA 13.0 已就绪
- ⏳ 正在安装项目依赖...
- ❌ Redis 需要手动安装
- ❌ FFmpeg 需要手动安装

---

## 立即行动（并行进行）

### 任务 1: 安装 Redis (5分钟)

**推荐方式 - 使用 Memurai**:
1. 打开浏览器访问: https://www.memurai.com/get-memurai
2. 点击 "Download" 下载安装包
3. 运行安装程序（一路下一步）
4. 安装完成后 Redis 会自动启动

**验证安装**:
```powershell
redis-cli ping
# 应该返回 PONG
```

---

### 任务 2: 安装 FFmpeg (10分钟)

**快速安装步骤**:

1. **下载 FFmpeg**
   - 访问: https://www.gyan.dev/ffmpeg/builds/
   - 下载 "ffmpeg-release-full.7z" (约150MB)

2. **解压文件**
   - 解压到 `C:\ffmpeg`
   - 确保路径是 `C:\ffmpeg\bin\ffmpeg.exe`

3. **添加到系统 PATH**
   ```
   方法1 (快速):
   - 按 Win + X，选择"系统"
   - 点击"高级系统设置"
   - 点击"环境变量"
   - 在"系统变量"中找到"Path"，双击
   - 点击"新建"，输入: C:\ffmpeg\bin
   - 点击"确定"保存
   
   方法2 (命令行):
   以管理员身份运行 PowerShell，执行:
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\ffmpeg\bin", "Machine")
   ```

4. **重启终端并验证**
   ```powershell
   ffmpeg -version
   # 应该显示版本信息
   ```

---

## 项目依赖安装（自动进行中）

### 后端依赖
```bash
cd video-agent/backend
pip install -r requirements.txt
```
预计时间: 5-10分钟

### 前端依赖
```bash
cd video-agent/frontend
npm install
```
预计时间: 2-3分钟

---

## 安装完成后的验证

### 1. 验证 Redis
```powershell
redis-cli ping
```

### 2. 验证 FFmpeg
```powershell
ffmpeg -version
```

### 3. 测试后端
```powershell
cd video-agent/backend
python main.py
```
访问: http://localhost:8000/api/health

### 4. 测试前端
```powershell
cd video-agent/frontend
npm run dev
```
访问: http://localhost:5173

---

## 时间估算

- Redis 安装: 5分钟
- FFmpeg 安装: 10分钟
- Python 依赖: 5-10分钟（自动）
- Node.js 依赖: 2-3分钟（自动）

**总计: 约20-30分钟**

---

## 遇到问题？

### Redis 安装失败
- 备选方案: 使用 WSL2 安装 Redis
- 或者暂时跳过，使用内存队列（性能较差）

### FFmpeg 安装失败
- 确保解压路径正确
- 确保 PATH 添加正确
- 重启终端后再试

### Python 依赖安装失败
- 检查网络连接
- 使用国内镜像: `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

### Node.js 依赖安装失败
- 检查网络连接
- 使用国内镜像: `npm install --registry=https://registry.npmmirror.com`

---

**安装完成后，立即通知我，我们继续 Day 1 晚上的 UI 重构任务！**
