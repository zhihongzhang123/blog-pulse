#!/usr/bin/env python3
"""
Pulse Blog · 每日交易思考生成器

用法：
    python3 scripts/generate-daily-thought.py [主题]
    
示例：
    python3 scripts/generate-daily-thought.py "等待的艺术"
    python3 scripts/generate-daily-thought.py "周期与人性"
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# 配置
BLOG_ROOT = Path(__file__).parent.parent
CONTENT_DIR = BLOG_ROOT / "content" / "daily-thoughts"
PUBLIC_DIR = BLOG_ROOT / "public"

# 主题模板
THEME_TEMPLATES = {
    "等待的艺术": {
        "tags": ["交易技能", "利弗莫尔", "耐心"],
        "quote": "赚大钱的不是买卖，而是等待。",
        "quote_author": "杰西·利弗莫尔",
    },
    "周期与人性": {
        "tags": ["交易人生", "周期理论", "行为金融"],
        "quote": "市场周期本质是人性的周期。贪婪与恐惧代代相传，技术在变，人性不变。",
        "quote_author": "Pulse",
    },
    "风险的艺术": {
        "tags": ["风险管理", "生存法则", "仓位管理"],
        "quote": "第一条规则：永远不要亏钱；第二条规则：永远不要忘记第一条。",
        "quote_author": "沃伦·巴菲特",
    },
    "默认": {
        "tags": ["交易哲学", "深度思考"],
        "quote": "市场是宇宙的缩影，规律永恒，人性不变。",
        "quote_author": "Pulse",
    },
}


def generate_article(title: str, theme: str = None) -> str:
    """生成每日思考文章"""
    
    today = datetime.now()
    date_str = today.strftime("%Y 年 %m 月 %d 日")
    weekday = today.strftime("%A")
    file_date = today.strftime("%Y-%m-%d")
    
    # 获取主题配置
    theme_config = THEME_TEMPLATES.get(theme, THEME_TEMPLATES["默认"])
    tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in theme_config["tags"]])
    
    # 文章模板
    article = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} · Pulse</title>
    <link rel="stylesheet" href="../../styles.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;600;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        .article-container {{ max-width: 800px; margin: 0 auto; padding: var(--spacing-xl) var(--spacing-md); }}
        .article-header {{ text-align: center; margin-bottom: var(--spacing-xl); }}
        .article-date {{ color: var(--color-text-muted); font-size: 0.95rem; margin-bottom: var(--spacing-sm); }}
        .article-title {{ font-family: var(--font-serif); font-size: 2.5rem; line-height: 1.3; margin-bottom: var(--spacing-md); background: var(--gradient-gold); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
        .article-tags {{ display: flex; justify-content: center; gap: var(--spacing-xs); flex-wrap: wrap; }}
        .article-content {{ font-size: 1.1rem; line-height: 1.9; }}
        .article-content p {{ margin-bottom: var(--spacing-lg); }}
        .article-content blockquote {{ font-family: var(--font-serif); font-size: 1.3rem; font-style: italic; border-left: 3px solid var(--color-gold); padding-left: var(--spacing-md); margin: var(--spacing-xl) 0; color: var(--color-text); background: rgba(212, 175, 55, 0.05); padding: var(--spacing-lg); border-radius: 0 var(--radius-md) var(--radius-md) 0; }}
        .article-content h2 {{ font-family: var(--font-serif); font-size: 1.6rem; margin: var(--spacing-xl) 0 var(--spacing-md); color: var(--color-gold); }}
        .article-content ul {{ margin: var(--spacing-md) 0; padding-left: var(--spacing-lg); }}
        .article-content li {{ margin-bottom: var(--spacing-sm); }}
        .key-insight {{ background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: var(--radius-md); padding: var(--spacing-lg); margin: var(--spacing-xl) 0; }}
        .key-insight-title {{ color: var(--color-accent); font-weight: 600; margin-bottom: var(--spacing-sm); display: flex; align-items: center; gap: var(--spacing-xs); }}
        .back-link {{ display: inline-flex; align-items: center; gap: var(--spacing-xs); color: var(--color-accent); text-decoration: none; margin-bottom: var(--spacing-lg); transition: color 0.3s ease; }}
        .back-link:hover {{ color: var(--color-gold); }}
        .article-footer {{ margin-top: var(--spacing-xl); padding-top: var(--spacing-lg); border-top: 1px solid rgba(148, 163, 184, 0.1); text-align: center; color: var(--color-text-muted); font-size: 0.9rem; }}
    </style>
</head>
<body>
    <div class="article-container">
        <a href="../../index.html" class="back-link">← 返回首页</a>
        
        <header class="article-header">
            <div class="article-date">{date_str} · {weekday}</div>
            <h1 class="article-title">{title}</h1>
            <div class="article-tags">
                {tags_html}
            </div>
        </header>
        
        <article class="article-content">
            <blockquote>
                "{theme_config['quote']}"
                <br>—— {theme_config['quote_author']}
            </blockquote>
            
            <h2>核心思考</h2>
            
            <p>[在此撰写文章正文...]</p>
            
            <p>[深入分析主题，结合市场实例和个人见解]</p>
            
            <div class="key-insight">
                <div class="key-insight-title">💡 核心洞察</div>
                <p>[总结核心观点]</p>
            </div>
            
            <h2>实践建议</h2>
            
            <p>[提供可执行的建议]</p>
            
            <div class="key-insight">
                <div class="key-insight-title">🎯 行动建议</div>
                <p>[具体行动步骤]</p>
            </div>
            
            <h2>最后的思考</h2>
            
            <p>[升华主题，给读者启发]</p>
        </article>
        
        <footer class="article-footer">
            <p>💓 Pulse · 市场脉搏与交易哲学</p>
            <p>本文仅供参考，不构成投资建议。市场有风险，投资需谨慎。</p>
        </footer>
        
        <!-- 评论系统 -->
        <div id="giscus-container" style="margin-top: var(--spacing-xl);">
            <script src="https://giscus.app/client.js"
                    data-repo="minimac/blog-pulse"
                    data-repo-id="待配置"
                    data-category="General"
                    data-category-id="待配置"
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
        </div>
    </div>
</body>
</html>
'''
    
    return article, file_date


def main():
    if len(sys.argv) < 2:
        print("用法：python3 generate-daily-thought.py [主题]")
        print("示例主题：等待的艺术，周期与人性，风险的艺术")
        sys.exit(1)
    
    title = sys.argv[1]
    theme = title if title in THEME_TEMPLATES else None
    
    article, file_date = generate_article(title, theme)
    
    # 创建文件
    filename = f"{file_date}-{title.replace(' ', '-').replace('/', '-')}.html"
    filepath = CONTENT_DIR / filename
    
    # 确保目录存在
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(article)
    
    print(f"✅ 文章已生成：{filepath}")
    print(f"📝 请在文件中填写正文内容")
    print(f"🔗 访问：http://localhost:8000/content/daily-thoughts/{filename}")


if __name__ == "__main__":
    main()
