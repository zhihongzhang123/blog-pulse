# Pulse Blog · 市场脉搏与交易哲学

一个融合交易哲学、市场分析、新闻简报和实盘系统的个人博客。

**风格**: 艺术 · 哲学 · 金融  
**技术栈**: 静态 HTML/CSS/JS + Giscus 评论系统

---

## 🚀 快速启动

### 本地预览

```bash
cd blog-pulse/public
python3 -m http.server 8000
```

访问：http://localhost:8000

### 部署选项

#### 选项 1: GitHub Pages (推荐)

```bash
# 1. 创建 GitHub 仓库
gh repo create blog-pulse --public

# 2. 推送 public 目录内容
cd blog-pulse
git init
git add public/
git commit -m "Initial commit"
git branch -M main
git remote add origin git@github.com:minimac/blog-pulse.git
git push -u origin main

# 3. 启用 GitHub Pages
# Settings → Pages → Source: main branch → /public
```

#### 选项 2: Vercel / Netlify

直接连接 GitHub 仓库，自动部署。

#### 选项 3: 自有服务器

```bash
# Nginx 配置示例
server {
    listen 80;
    server_name pulse.blog;
    root /path/to/blog-pulse/public;
    index index.html;
}
```

---

## 📝 内容管理

### 每日思考文章

```bash
# 生成新文章模板
python3 scripts/generate-daily-thought.py "文章标题"

# 示例
python3 scripts/generate-daily-thought.py "等待的艺术"
```

生成的文件位置：`content/daily-thoughts/YYYY-MM-DD-标题.html`

### 更新主页

直接编辑 `public/index.html` 中的内容卡片。

---

## 🔧 集成现有系统

### 新闻简报集成

编辑 `public/index.html` 中的 `#briefings` 部分，添加脚本自动读取：

```javascript
// 从 memory/ 读取最新简报
fetch('../../memory/push-latest.json')
    .then(r => r.json())
    .then(data => {
        // 更新简报卡片
    });
```

### 美股分析集成

编辑 `public/index.html` 中的 `#market-analysis` 部分，添加脚本读取：

```javascript
// 从 skills/us-market-pipeline/output/ 读取分析报告
fetch('../../skills/us-market-pipeline/output/latest-analysis.json')
    .then(r => r.json())
    .then(data => {
        // 更新分析卡片
    });
```

### 实盘系统集成

在 `#live-trading` 部分嵌入交易系统的 iframe 或 API：

```html
<iframe src="https://your-trading-system.com/embed" 
        width="100%" 
        height="400" 
        frameborder="0">
</iframe>
```

---

## 💬 评论系统配置

使用 [Giscus](https://giscus.app/) (基于 GitHub Discussions):

### 步骤

1. 创建 GitHub 仓库 `minimac/blog-pulse`
2. 安装 Giscus App: https://github.com/apps/giscus
3. 启用 Discussions 功能
4. 获取配置参数 (repo-id, category-id)
5. 更新所有 HTML 文件中的 Giscus 配置：

```html
<script src="https://giscus.app/client.js"
        data-repo="minimac/blog-pulse"
        data-repo-id="YOUR_REPO_ID"
        data-category="General"
        data-category-id="YOUR_CATEGORY_ID"
        ...>
</script>
```

### 替代方案

- **Disqus**: 传统评论系统，支持匿名
- **Utterances**: 基于 GitHub Issues
- **Waline**: 自建评论系统

---

## 🎨 自定义样式

编辑 `public/styles.css`:

```css
:root {
    /* 主色调 */
    --color-bg: #0a0e14;
    --color-accent: #3b82f6;
    --color-gold: #d4af37;
    
    /* 字体 */
    --font-serif: 'Playfair Display', 'Noto Serif SC', serif;
}
```

---

## 📊 自动化脚本

### 每日文章生成

```bash
# 添加到 crontab (每日 06:00)
0 6 * * * cd /path/to/blog-pulse && python3 scripts/generate-daily-thought.py "今日主题"
```

### 简报同步

创建脚本 `scripts/sync-briefings.py`:

```python
#!/usr/bin/env python3
"""同步新闻简报到博客"""

import json
from pathlib import Path
from datetime import datetime

# 读取最新简报
briefing_file = Path('../../memory/push-latest.json')
with open(briefing_file) as f:
    briefing = json.load(f)

# 生成 HTML 页面
# ... (模板渲染逻辑)

print("✅ 简报已同步")
```

---

## 📁 目录结构

```
blog-pulse/
├── public/
│   ├── index.html          # 主页
│   ├── styles.css          # 样式
│   ├── main.js             # 交互脚本
│   └── assets/             # 图片等资源
├── content/
│   ├── daily-thoughts/     # 每日思考文章
│   ├── market-analysis/    # 市场分析报告
│   ├── briefings/          # 新闻简报归档
│   └── about/              # 关于页面
├── scripts/
│   ├── generate-daily-thought.py  # 文章生成器
│   ├── sync-briefings.py          # 简报同步
│   └── deploy.sh                  # 部署脚本
└── README.md               # 本文档
```

---

## 🔄 后续优化计划

### 阶段 1: 基础功能 (已完成 ✅)
- [x] 主页设计
- [x] 样式系统
- [x] 文章模板
- [x] 评论系统集成

### 阶段 2: 内容自动化 (进行中)
- [ ] 新闻简报自动同步
- [ ] 美股分析报告自动发布
- [ ] 每日思考 AI 辅助生成

### 阶段 3: 实盘集成
- [ ] 嵌入交易系统网页
- [ ] 实时持仓展示
- [ ] 盈亏曲线图表

### 阶段 4: 高级功能
- [ ] RSS 订阅
- [ ] 邮件订阅
- [ ] 搜索功能
- [ ] 标签/分类系统
- [ ] 暗黑模式切换

---

## 📝 使用规范

### 文章风格

- **语调**: 深邃、克制、优雅、直击本质
- **长度**: 800-2000 字
- **结构**: 核心思考 → 深入分析 → 实践建议 → 哲学升华
- **必含**: 大师名言引用 + 行动建议

### 发布频率

- **每日思考**: 每天 1 篇 (06:00 前发布)
- **新闻简报**: 每天 2 篇 (08:00/20:00)
- **市场分析**: 交易日盘前/盘后
- **深度文章**: 每周 1-2 篇

---

## 🙏 承诺

> 我承诺，每一篇文章都提供真实价值，不灌水，不凑数。
> 
> 我相信，长期积累的力量胜过短期流量的诱惑。
> 
> 我追求，每一句话都有信息量或思想深度。

---

*Pulse Blog · Created 2026-03-22*  
*💓 市场脉搏与交易哲学*
