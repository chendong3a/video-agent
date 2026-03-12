# 推送到 Git 远程仓库指南

## 当前状态
- ✅ Git 仓库已初始化
- ✅ 所有文件已添加
- ⏳ 需要创建远程仓库并推送

---

## 步骤 1: 在 GitHub 创建新仓库

1. 访问 https://github.com/new
2. 仓库名称: `video-agent` 或你喜欢的名字
3. 描述: `AI驱动的视频内容再创作工具 - 8天冲刺项目`
4. 选择 **Private** 或 **Public**
5. **不要**勾选 "Initialize this repository with a README"
6. 点击 "Create repository"

---

## 步骤 2: 推送代码

创建仓库后，GitHub 会显示推送命令。复制并执行：

```bash
cd f:\Agent\video-agent

# 添加远程仓库（替换成你的仓库地址）
git remote add origin https://github.com/你的用户名/video-agent.git

# 重命名分支为 main
git branch -M main

# 推送代码
git push -u origin main
```

---

## 步骤 3: 验证

推送成功后，刷新 GitHub 页面，应该能看到所有文件。

---

## 如果遇到问题

### 问题 1: 需要登录
```bash
# 使用 GitHub CLI 登录
gh auth login

# 或配置 Git 凭据
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

### 问题 2: 推送被拒绝
```bash
# 强制推送（首次推送可以用）
git push -u origin main --force
```

---

## 快速命令（复制粘贴）

```bash
cd f:\Agent\video-agent
git add -A
git commit -m "Day 1: 项目初始化完成 - 完整脚手架和依赖"
git remote add origin https://github.com/你的用户名/video-agent.git
git branch -M main
git push -u origin main
```

---

**完成后，你的代码就会在 GitHub 上了！** 🎉
