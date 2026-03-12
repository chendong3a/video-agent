# Redis 和 FFmpeg 最终安装指南

## 当前状态
自动安装脚本遇到权限问题。采用最简单的手动安装方式。

---

## 方案：直接下载安装（5-10分钟）

### 步骤 1: 安装 Redis (Memurai) - 3分钟

1. **下载**: 
   - 打开浏览器访问: https://www.memurai.com/get-memurai
   - 点击 "Download Memurai Developer" 按钮
   
2. **安装**:
   - 运行下载的 `.msi` 安装包
   - 一路点击 "Next"
   - 安装完成后会自动启动服务

3. **验证**:
   ```powershell
   redis-cli ping
   # 应该返回: PONG
   ```

---

### 步骤 2: 安装 FFmpeg - 5分钟

1. **下载**:
   - 访问: https://www.gyan.dev/ffmpeg/builds/
   - 下载 "ffmpeg-release-essentials.zip" (约80MB)

2. **解压**:
   - 解压到 `C:\ffmpeg`
   - 确保路径是 `C:\ffmpeg\bin\ffmpeg.exe`

3. **添加到 PATH**:
   ```powershell
   # 复制这个命令，在普通 PowerShell 中运行
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\ffmpeg\bin", "User")
   ```

4. **重启终端并验证**:
   ```powershell
   # 关闭当前终端，打开新终端
   ffmpeg -version
   # 应该显示版本信息
   ```

---

## 安装完成后

运行验证命令:
```powershell
redis-cli ping
ffmpeg -version
```

两个都成功后，Day 1 的所有任务就完成了！

---

## 预计时间
- Redis: 3分钟
- FFmpeg: 5分钟  
- **总计: 8分钟**

---

**完成后立即通知我，我们开始今晚的 UI 重构任务！**
