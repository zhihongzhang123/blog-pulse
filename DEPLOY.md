# 部署到 GitHub Pages

## 方法一：GitHub CLI (推荐)

### 1. 登录 GitHub

```bash
cd /Users/minimac/.openclaw/workspace/blog-pulse
gh auth login
```

按提示操作：
1. 选择 **HTTPS**
2. 选择 **Yes** 登录 GitHub.com
3. 复制显示的代码
4. 浏览器打开 https://github.com/login/device
5. 粘贴代码授权
6. 回到终端完成登录

### 2. 创建仓库并推送

```bash
# 创建远程仓库
gh repo create blog-pulse --public --source=. --remote=origin

# 推送代码
git push -u origin main
```

### 3. 启用 GitHub Pages

1. 打开 https://github.com/minimac/blog-pulse/settings/pages
2. **Build and deployment** → Source: **Deploy from a branch**
3. **Branch**: 选择 `main`，文件夹 `/ (root)`
4. 点击 **Save**

等待 1-2 分钟，页面会显示：
> Your site is live at `https://minimac.github.io/blog-pulse/`

---

## 方法二：手动 Git 推送

### 1. 创建 GitHub 仓库

浏览器打开 https://github.com/new
- Repository name: `blog-pulse`
- 选择 **Public**
- **不要** 勾选 "Add a README file"
- 点击 **Create repository**

### 2. 推送代码

```bash
cd /Users/minimac/.openclaw/workspace/blog-pulse

# 添加远程仓库
git remote add origin https://github.com/minimac/blog-pulse.git

# 推送
git branch -M main
git push -u origin main
```

### 3. 启用 Pages

同上（方法一第 3 步）。

---

## 方法三：Vercel 部署 (自动 CI/CD)

### 1. 连接 GitHub

1. 打开 https://vercel.com/new
2. 点击 **Continue with GitHub**
3. 授权 Vercel 访问 GitHub

### 2. 导入项目

1. 点击 **Import Git Repository**
2. 选择 `minimac/blog-pulse`
3. 点击 **Import**

### 3. 部署设置

- **Framework Preset**: Other
- **Build Command**: (留空)
- **Output Directory**: `public`
- 点击 **Deploy**

Vercel 会自动分配域名：`https://blog-pulse-xxx.vercel.app`

---

## 部署后配置

### 1. 配置评论系统 (Giscus)

1. 打开 https://giscus.app/
2. 输入仓库：`minimac/blog-pulse`
3. 点击 **Configure Giscus**
4. 启用 Discussions: https://github.com/minimac/blog-pulse/discussions (点击 "Get started")
5. 获取配置参数：
   - Repository
   - Repository ID
   - Category: Announcements
   - Category ID

6. 更新 HTML 文件中的 Giscus 配置：

```html
<script src="https://giscus.app/client.js"
        data-repo="minimac/blog-pulse"
        data-repo-id="YOUR_REPO_ID"
        data-category="Announcements"
        data-category-id="YOUR_CATEGORY_ID"
        data-mapping="pathname"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="bottom"
        data-theme="preferred_color_scheme"
        data-lang="zh-CN"
        crossorigin="anonymous"
        async>
</script>
```

### 2. 自定义域名 (可选)

**GitHub Pages**:
1. Settings → Pages → Custom domain
2. 输入域名 (如 `pulse.blog`)
3. DNS 配置 CNAME 记录

**Vercel**:
1. Settings → Domains
2. 添加域名
3. 按提示配置 DNS

---

## 验证部署

访问：
- GitHub Pages: https://minimac.github.io/blog-pulse/
- Vercel: https://blog-pulse-xxx.vercel.app

检查项目：
- ✅ 页面正常加载
- ✅ 样式正确显示
- ✅ 动画流畅
- ✅ 响应式正常
- ✅ 深色/浅色模式切换

---

## 后续更新

```bash
cd /Users/minimac/.openclaw/workspace/blog-pulse

# 提交更改
git add -A
git commit -m "更新内容"

# 推送 (自动部署)
git push
```

GitHub Pages/Vercel 会在 1-2 分钟内自动重新部署。

---

## 故障排查

### 页面 404

- 确认 `public/index.html` 存在
- 确认 Pages 设置正确 (branch: main, folder: /)
- 等待 2 分钟缓存刷新

### 样式不加载

- 检查 CSS 路径是否正确
- 浏览器硬刷新 (Cmd+Shift+R)
- 检查浏览器控制台错误

### 评论系统不显示

- 确认 Discussions 已启用
- 确认 Giscus 配置参数正确
- 检查浏览器控制台 CORS 错误

---

*DEPLOY.md · Pulse Blog 部署指南*
