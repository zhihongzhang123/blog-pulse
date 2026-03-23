#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日思考文章生成器

用法:
    python3 scripts/generate-daily-thought.py "文章标题" "标签 1" "标签 2"
    
示例:
    python3 scripts/generate-daily-thought.py "等待的艺术" "交易哲学" "利弗莫尔"
"""

import sys
import os
from datetime import datetime
from pathlib import Path

def generate_article(title: str, tags: list):
    """生成文章模板"""
    
    # 生成文件名
    today = datetime.now().strftime('%Y-%m-%d')
    filename_slug = title.replace(' ', '-').replace('。', '').replace('？', '')
    filename = f"{today}-{filename_slug}.html"
    
    # 文章路径
    output_dir = Path('content/daily-thoughts')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename
    
    # 文章模板
    article_template = f"""<!DOCTYPE html>
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
        .article-container {{
            max-width: 800px;
            margin: 0 auto;
            padding: var(--spacing-xl) var(--spacing-md);
        }}
        
        .article-header {{
            text-align: center;
            margin-bottom: var(--spacing-xl);
        }}
        
        .article-date {{
            color: var(--color-text-muted);
            font-size: 0.95rem;
            margin-bottom: var(--spacing-sm);
        }}
        
        .article-title {{
            font-family: var(--font-serif);
            font-size: 2.5rem;
            line-height: 1.3;
            margin-bottom: var(--spacing-md);
            background: var(--gradient-gold);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .article-tags {{
            display: flex;
            justify-content: center;
            gap: var(--spacing-xs);
            flex-wrap: wrap;
        }}
        
        .tag {{
            background: var(--color-gold-light);
            color: var(--color-gold);
            padding: var(--spacing-xs) var(--spacing-md);
            border-radius: var(--radius-full);
            font-size: 0.85rem;
            font-weight: 500;
        }}
        
        .article-content {{
            font-size: 1.1rem;
            line-height: 1.9;
        }}
        
        .article-content p {{
            margin-bottom: var(--spacing-lg);
        }}
        
        .article-content blockquote {{
            font-family: var(--font-serif);
            font-size: 1.3rem;
            font-style: italic;
            border-left: 3px solid var(--color-gold);
            padding-left: var(--spacing-md);
            margin: var(--spacing-xl) 0;
            color: var(--color-text);
            background: rgba(212, 175, 55, 0.05);
            padding: var(--spacing-lg);
            border-radius: 0 var(--radius-md) var(--radius-md) 0;
        }}
        
        .article-content h2 {{
            font-family: var(--font-serif);
            font-size: 1.6rem;
            margin: var(--spacing-xl) 0 var(--spacing-md);
            color: var(--color-gold);
        }}
        
        .article-content ul {{
            margin: var(--spacing-md) 0;
            padding-left: var(--spacing-lg);
        }}
        
        .article-footer {{
            margin-top: var(--spacing-xl);
            padding-top: var(--spacing-lg);
            border-top: 1px solid var(--color-border);
            text-align: center;
            color: var(--color-text-muted);
        }}
        
        /* 阅读计数 */
        .article-views {{
            text-align: center;
            color: var(--color-text-muted);
            font-size: 0.85rem;
            margin-top: var(--spacing-md);
        }}
    </style>
</head>
<body>
    <article class="article-container">
        <header class="article-header">
            <div class="article-date">📅 {today}</div>
            <h1 class="article-title">{title}</h1>
            <div class="article-tags">
                {''.join([f'<span class="tag">{tag}</span>' for tag in tags])}
            </div>
        </header>
        
        <div class="article-content">
            <p>【在这里开始你的思考...】</p>
            
            <h2>核心观点</h2>
            <p>【阐述你的核心观点...】</p>
            
            <h2>深度分析</h2>
            <p>【展开分析...】</p>
            
            <blockquote>
                【可以在这里引用大师名言或核心洞察】
            </blockquote>
            
            <h2>实战应用</h2>
            <p>【如何应用到实际交易中...】</p>
            
            <h2>最后的思考</h2>
            <p>【总结与升华...】</p>
        </div>
        
        <footer class="article-footer">
            <p>💓 Pulse · 市场脉搏与交易哲学</p>
            <p>本文仅供参考，不构成投资建议。市场有风险，投资需谨慎。</p>
            <div class="article-views">
                <span>👁️ 阅读次数：<span id="view-count">加载中...</span></span>
            </div>
        </footer>
    </article>
    
    <!-- 加载主脚本 (主题切换等) -->
    <script src="../../main.js"></script>
    
    <!-- 阅读计数脚本 -->
    <script>
        // 简单的阅读计数 (localStorage)
        (function() {{
            const key = 'article_views_' + window.location.pathname;
            let views = parseInt(localStorage.getItem(key) || '0') + 1;
            localStorage.setItem(key, views);
            
            // 显示计数
            const viewElement = document.getElementById('view-count');
            if (viewElement) {{
                viewElement.textContent = views.toLocaleString();
            }}
        }})();
    </script>
</body>
</html>
"""
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(article_template)
    
    print(f"✅ 文章模板已生成：{output_path}")
    print(f"📝 标题：{title}")
    print(f"🏷️  标签：{', '.join(tags)}")
    print(f"\n📝 下一步:")
    print(f"   1. 编辑文章：{output_path}")
    print(f"   2. 更新首页：index.html (添加文章卡片)")
    print(f"   3. 推送部署：git add . && git commit && git push")
    
    return str(output_path)


def main():
    if len(sys.argv) < 2:
        print("❌ 请提供文章标题")
        print(f"\n用法：python3 {sys.argv[0]} \"文章标题\" \"标签 1\" \"标签 2\" ...")
        print(f"\n示例：python3 {sys.argv[0]} \"等待的艺术\" \"交易哲学\" \"利弗莫尔\"")
        sys.exit(1)
    
    title = sys.argv[1]
    tags = sys.argv[2:] if len(sys.argv) > 2 else ['交易哲学']
    
    generate_article(title, tags)


if __name__ == '__main__':
    main()
