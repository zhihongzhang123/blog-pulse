#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻简报同步脚本（优化版）

功能:
1. 从 memory/ 目录读取最新 Markdown 简报
2. 转换为 JSON 格式供博客使用
3. 生成 HTML 版本
4. 更新博客数据索引

用法:
    python3 scripts/sync-briefings-optimized.py
"""

import json
import re
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path('/Users/minimac/.openclaw/workspace')
MEMORY_DIR = WORKSPACE / 'memory'
BLOG_DATA = WORKSPACE / 'blog-pulse/data/news'

def find_latest_briefing():
    """查找最新的新闻简报文件"""
    # 查找所有简报文件
    patterns = [
        'news-brief-*evening*.md',
        'news-brief-*morning*.md',
        'news-brief-*.md'
    ]
    
    briefing_files = []
    for pattern in patterns:
        briefing_files.extend(MEMORY_DIR.glob(pattern))
    
    if not briefing_files:
        print("❌ 未找到简报文件")
        return None
    
    # 按修改时间排序，获取最新
    latest = max(briefing_files, key=lambda p: p.stat().st_mtime)
    return latest

def parse_briefing_markdown(filepath: Path):
    """解析 Markdown 简报内容"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取标题
    title_match = re.search(r'^#\s*(🟢.*?)(?:\n|$)', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "新闻简报"
    
    # 提取推送时间
    time_match = re.search(r'推送时间：(.+?)\n', content)
    push_time = time_match.group(1).strip() if time_match else None
    
    # 提取 MsgID
    msgid_match = re.search(r'MsgID:\s*(\w+)', content)
    msgid = msgid_match.group(1) if msgid_match else None
    
    # 提取核心主线
    core_match = re.search(r'💡\s*核心主线.*?(?=\n---|\n⏰)', content, re.DOTALL)
    core_content = core_match.group(0) if core_match else ""
    
    # 提取完整内容（前 2000 字用于预览）
    full_content = content
    
    # 统计新闻条数
    news_count = len(re.findall(r'•\s*\[级别', content)) + len(re.findall(r'^\[.*?\]', content, re.MULTILINE))
    if news_count == 0:
        news_count = len(content.split('\n')) // 3  # 估算
    
    return {
        'title': title,
        'pushTime': push_time,
        'msgid': msgid,
        'coreContent': core_content,
        'fullContent': full_content,
        'newsCount': news_count,
        'sourceFile': filepath.name
    }

def generate_briefing_json(data: dict):
    """生成 JSON 格式"""
    return {
        'version': '2.0',
        'title': data['title'],
        'timestamp': data['pushTime'],
        'msgid': data['msgid'],
        'newsCount': data['newsCount'],
        'coreContent': data['coreContent'],
        'fullContent': data['fullContent'],
        'sourceFile': data['sourceFile']
    }

def generate_briefing_html(data: dict):
    """生成 HTML 格式（苹果风格）"""
    # 将 Markdown 转换为简单 HTML
    content_html = data['fullContent']
    
    # 简单 Markdown 转 HTML
    content_html = content_html.replace('### ', '<h3>')
    content_html = content_html.replace('## ', '<h2>')
    content_html = content_html.replace('# ', '<h1>')
    content_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content_html)
    content_html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content_html)
    content_html = content_html.replace('\n---\n', '<hr>')
    content_html = content_html.replace('\n\n', '</p><p>')
    content_html = content_html.replace('\n', '<br>')
    
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['title']} · Pulse</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --apple-font: -apple-system, BlinkMacSystemFont, 'SF Pro SC', 'SF Pro Text', 'Helvetica Neue', 'PingFang SC', 'Noto Sans SC', sans-serif;
            --apple-bg: #ffffff;
            --apple-bg-secondary: #f5f5f7;
            --apple-text: #1d1d1f;
            --apple-text-secondary: #86868b;
            --apple-accent: #0a84ff;
            --apple-accent-hover: #0066cc;
            --apple-border: rgba(0, 0, 0, 0.08);
            --apple-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            --apple-shadow-hover: 0 4px 16px rgba(0, 0, 0, 0.08);
            --apple-radius: 12px;
            --apple-radius-lg: 18px;
        }}
        
        /* 深色模式变量 */
        body.dark-mode {{
            --apple-bg: #000000;
            --apple-bg-secondary: #1d1d1f;
            --apple-text: #f5f5f7;
            --apple-text-secondary: #86868b;
            --apple-border: rgba(255, 255, 255, 0.08);
            --apple-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            --apple-shadow-hover: 0 4px 16px rgba(0, 0, 0, 0.3);
        }}
        
        /* 系统自动深色模式 */
        @media (prefers-color-scheme: dark) {{
            :root {{
                --apple-bg-auto: #000000;
                --apple-bg-secondary-auto: #1d1d1f;
                --apple-text-auto: #f5f5f7;
                --apple-text-secondary-auto: #86868b;
                --apple-border-auto: rgba(255, 255, 255, 0.08);
                --apple-shadow-auto: 0 2px 8px rgba(0, 0, 0, 0.2);
                --apple-shadow-hover-auto: 0 4px 16px rgba(0, 0, 0, 0.3);
            }}
            
            body:not(.dark-mode):not(.light-mode) {{
                --apple-bg: var(--apple-bg-auto);
                --apple-bg-secondary: var(--apple-bg-secondary-auto);
                --apple-text: var(--apple-text-auto);
                --apple-text-secondary: var(--apple-text-secondary-auto);
                --apple-border: var(--apple-border-auto);
                --apple-shadow: var(--apple-shadow-auto);
                --apple-shadow-hover: var(--apple-shadow-hover-auto);
            }}
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: var(--apple-font);
            background: var(--apple-bg);
            color: var(--apple-text);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        
        .briefing-container {{
            max-width: 860px;
            margin: 0 auto;
            padding: 60px 24px;
        }}
        
        /* 导航栏 */
        .nav-back {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: var(--apple-accent);
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            padding: 8px 16px;
            border-radius: 20px;
            background: var(--apple-bg-secondary);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 32px;
        }}
        
        .nav-back:hover {{
            background: var(--apple-accent);
            color: white;
            transform: translateX(-4px);
        }}
        
        .nav-back::before {{
            content: '←';
            font-size: 16px;
            font-weight: 600;
        }}
        
        /* 头部 */
        .briefing-header {{
            margin-bottom: 48px;
            animation: fadeInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .briefing-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            background: linear-gradient(135deg, #0a84ff 0%, #0066cc 100%);
            color: #ffffff;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 4px 12px rgba(10, 132, 255, 0.3);
        }}
        
        .briefing-title {{
            font-family: var(--apple-font);
            font-size: clamp(28px, 5vw, 42px);
            font-weight: 700;
            line-height: 1.1;
            margin-bottom: 20px;
            letter-spacing: -0.02em;
            color: var(--apple-text);
        }}
        
        .briefing-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            padding: 16px 0;
            border-top: 1px solid var(--apple-border);
            border-bottom: 1px solid var(--apple-border);
        }}
        
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 14px;
            color: var(--apple-text-secondary);
            font-weight: 400;
        }}
        
        .meta-item::before {{
            font-size: 16px;
        }}
        
        /* 内容卡片 */
        .briefing-content-card {{
            background: var(--apple-bg-secondary);
            border-radius: var(--apple-radius-lg);
            padding: 48px 56px;
            margin-bottom: 32px;
            box-shadow: var(--apple-shadow);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            animation: fadeInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.2s both;
        }}
        
        .briefing-content-card:hover {{
            box-shadow: var(--apple-shadow-hover);
        }}
        
        .briefing-content {{
            font-size: 15px;
            line-height: 1.9;
            color: var(--apple-text);
            white-space: pre-wrap;
            word-wrap: break-word;
            font-weight: 300;
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
            max-width: 680px;
            margin: 0 auto;
        }}
        
        .briefing-content h1,
        .briefing-content h2,
        .briefing-content h3 {{
            font-family: var(--apple-font);
            font-weight: 500;
            margin: 42px 0 18px;
            letter-spacing: -0.01em;
            line-height: 1.4;
        }}
        
        .briefing-content h1 {{ 
            font-size: 28px;
            margin-top: 48px;
        }}
        .briefing-content h2 {{ 
            font-size: 22px;
            margin-top: 42px;
        }}
        .briefing-content h3 {{ 
            font-size: 17px;
            margin-top: 36px;
        }}
        
        .briefing-content strong {{
            font-weight: 500;
            color: var(--apple-text);
        }}
        
        .briefing-content p {{
            margin-bottom: 20px;
        }}
        
        .briefing-content hr {{
            border: none;
            height: 1px;
            background: var(--apple-border);
            margin: 42px 0;
        }}
        
        .briefing-content ul,
        .briefing-content ol {{
            margin: 24px 0;
            padding-left: 24px;
        }}
        
        .briefing-content li {{
            margin-bottom: 12px;
            line-height: 1.8;
        }}
        
        .briefing-content blockquote {{
            margin: 32px 0;
            padding: 20px 24px;
            border-left: 3px solid var(--apple-accent);
            background: var(--apple-bg-secondary);
            border-radius: 0 12px 12px 0;
            font-style: italic;
            line-height: 1.8;
        }}
        
        .briefing-content hr {{
            border: none;
            height: 1px;
            background: var(--apple-border);
            margin: 32px 0;
        }}
        
        .briefing-content p {{
            margin-bottom: 16px;
        }}
        
        /* 核心主线高亮 */
        .core-highlight {{
            background: linear-gradient(135deg, rgba(255, 214, 10, 0.1) 0%, rgba(255, 159, 10, 0.1) 100%);
            border-left: 4px solid #ffd60a;
            padding: 24px;
            border-radius: 12px;
            margin: 24px 0;
            font-size: 15px;
            line-height: 1.7;
        }}
        
        /* 按钮 */
        .action-buttons {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            animation: fadeInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.4s both;
        }}
        
        .btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 14px 28px;
            border-radius: var(--apple-radius);
            font-size: 15px;
            font-weight: 500;
            text-decoration: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            border: none;
            min-width: 160px;
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, #0a84ff 0%, #0066cc 100%);
            color: white;
        }}
        
        .btn-primary:hover {{
            background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(10, 132, 255, 0.4);
        }}
        
        .btn-secondary {{
            background: var(--apple-bg-secondary);
            color: var(--apple-text);
        }}
        
        .btn-secondary:hover {{
            background: var(--apple-border);
            transform: translateY(-2px);
        }}
        
        /* 动画 */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        /* 响应式 - 移动端优化 */
        @media (max-width: 768px) {{
            .briefing-container {{
                padding: 32px 16px;
            }}
            
            .briefing-content-card {{
                padding: 24px 20px;
                border-radius: var(--apple-radius);
            }}
            
            .briefing-meta {{
                flex-direction: column;
                gap: 8px;
            }}
            
            .meta-item {{
                font-size: 12px;
                padding: 4px 10px;
            }}
            
            .action-buttons {{
                flex-direction: column;
                gap: 10px;
            }}
            
            .btn {{
                width: 100%;
                padding: 14px 20px;
                font-size: 14px;
            }}
            
            /* 移动端优化 */
        @media (max-width: 768px) {{
            .briefing-content-card {{
                padding: 32px 24px;
                border-radius: var(--apple-radius);
            }}
        }}
        
        /* 移动端字体优化 */
            .briefing-content {{
                font-size: 14px;
                line-height: 1.85;
                letter-spacing: 0.01em;
                font-weight: 300;
                -webkit-font-smoothing: antialiased;
                max-width: 100%;
            }}
            
            .briefing-content h1 {{
                font-size: 24px;
                line-height: 1.35;
                margin: 36px 0 16px;
                font-weight: 500;
            }}
            
            .briefing-content h2 {{
                font-size: 20px;
                line-height: 1.4;
                margin: 32px 0 14px;
                font-weight: 500;
            }}
            
            .briefing-content h3 {{
                font-size: 16px;
                line-height: 1.45;
                margin: 28px 0 12px;
                font-weight: 500;
            }}
            
            .briefing-content p {{
                margin-bottom: 18px;
                word-break: break-word;
            }}
            
            .briefing-content strong {{
                font-weight: 500;
            }}
            
            .briefing-content hr {{
                margin: 36px 0;
            }}
            
            .briefing-content ul,
            .briefing-content ol {{
                margin: 20px 0;
                padding-left: 20px;
            }}
            
            .briefing-content li {{
                margin-bottom: 10px;
            }}
            
            .briefing-content blockquote {{
                margin: 28px 0;
                padding: 16px 20px;
            }}
            
            .core-highlight {{
                padding: 18px;
                font-size: 13px;
                line-height: 1.7;
                margin: 20px 0;
                border-left-width: 3px;
            }}
        }}
        
        /* 小屏幕手机优化 */
        @media (max-width: 375px) {{
            .briefing-content {{
                font-size: 13px;
                line-height: 1.8;
            }}
            
            .briefing-content h1 {{
                font-size: 22px;
            }}
            
            .briefing-content h2 {{
                font-size: 18px;
            }}
            
            .briefing-content h3 {{
                font-size: 15px;
            }}
            
            .briefing-content p {{
                margin-bottom: 16px;
            }}
        }}
        
        /* 小屏幕手机优化 */
        @media (max-width: 375px) {{
            .briefing-container {{
                padding: 24px 14px;
            }}
            
            .briefing-content {{
                font-size: 14px;
                line-height: 1.75;
            }}
            
            .briefing-content-card {{
                padding: 20px 16px;
            }}
            
            .briefing-title {{
                font-size: 24px;
            }}
            
            .nav-back {{
                font-size: 13px;
                padding: 6px 12px;
            }}
        }}
        
        /* 移动端字体渲染优化 */
        @media (max-width: 768px) {{
            body {{
                -webkit-text-size-adjust: 100%;
                text-size-adjust: 100%;
            }}
            
            .briefing-content {{
                text-rendering: optimizeLegibility;
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
            }}
        }}
        
        /* 平滑滚动 */
        html {{
            scroll-behavior: smooth;
        }}
        
        /* 选中效果 */
        ::selection {{
            background: rgba(0, 102, 204, 0.2);
            color: var(--apple-text);
        }}
        
        /* 移动端触摸优化 */
        @media (max-width: 768px) {{
            * {{
                -webkit-tap-highlight-color: transparent;
            }}
            
            .btn, .nav-back {{
                -webkit-touch-callout: none;
                user-select: none;
            }}
            
            /* 按钮点击反馈 */
            .btn:active {{
                transform: scale(0.98);
                opacity: 0.9;
            }}
        }}
    </style>
</head>
<body>
    <div class="briefing-container">
        <a href="../../index.html" class="nav-back">返回首页</a>
        
        <header class="briefing-header">
            <div class="briefing-badge">📰 宏观交易简报</div>
            <h1 class="briefing-title">{data['title'].replace('🟢 ', '')}</h1>
            <div class="briefing-meta">
                <span class="meta-item">📅 {data['pushTime'] or '未知'}</span>
                <span class="meta-item">📊 {data['newsCount']} 条新闻</span>
                <span class="meta-item">🆔 {data['msgid'] or 'N/A'}</span>
            </div>
        </header>
        
        <main>
            <div class="briefing-content-card">
                <div class="briefing-content">
{content_html}
                </div>
            </div>
            
            <div class="action-buttons">
                <a href="../../index.html" class="btn btn-primary">← 返回首页</a>
                <a href="latest.json" class="btn btn-secondary" download>📥 下载 JSON</a>
            </div>
        </main>
    </div>
    
    <script>
        // 核心主线高亮
        document.addEventListener('DOMContentLoaded', function() {{
            const content = document.querySelector('.briefing-content');
            if (content) {{
                const coreText = content.innerHTML;
                const highlighted = coreText.replace(
                    /(💡 核心主线.*?)(?=<h2>|<hr>|$)/s,
                    '<div class="core-highlight">$1</div>'
                );
                content.innerHTML = highlighted;
            }}
        }});
    </script>
</body>
</html>
"""
    return html_template

def sync_briefings():
    """主同步函数"""
    print("=" * 60)
    print("📰 新闻简报同步（优化版）")
    print("=" * 60)
    
    # 创建目标目录
    BLOG_DATA.mkdir(parents=True, exist_ok=True)
    
    # 查找最新简报
    latest_file = find_latest_briefing()
    if not latest_file:
        print("❌ 同步失败")
        return False
    
    print(f"📄 找到最新简报：{latest_file.name}")
    
    # 解析内容
    data = parse_briefing_markdown(latest_file)
    print(f"✅ 解析成功：{data['title']}")
    print(f"   新闻条数：{data['newsCount']}")
    print(f"   推送时间：{data['pushTime']}")
    
    # 生成 JSON
    json_data = generate_briefing_json(data)
    json_path = BLOG_DATA / 'latest.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    print(f"✅ JSON 已生成：{json_path}")
    
    # 生成 HTML
    html_content = generate_briefing_html(data)
    html_path = BLOG_DATA / 'latest.html'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✅ HTML 已生成：{html_path}")
    
    # 更新索引
    update_index(json_data)
    
    print("\n" + "=" * 60)
    print("✅ 简报同步完成")
    print("=" * 60)
    
    return True

def update_index(latest_data: dict):
    """更新数据索引"""
    index_path = WORKSPACE / 'blog-pulse/data/index.json'
    
    # 读取或创建索引
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            index = json.load(f)
        # 确保有 briefings 字段
        if 'briefings' not in index:
            index['briefings'] = []
    else:
        index = {'briefings': [], 'lastUpdated': None}
    
    # 添加新条目
    index['briefings'].insert(0, {
        'title': latest_data['title'],
        'timestamp': latest_data['timestamp'],
        'msgid': latest_data['msgid'],
        'newsCount': latest_data['newsCount'],
        'jsonPath': 'data/news/latest.json',
        'htmlPath': 'data/news/latest.html'
    })
    
    # 保留最近 20 条
    index['briefings'] = index['briefings'][:20]
    index['lastUpdated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 保存索引
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 索引已更新：{index_path}")

if __name__ == '__main__':
    sync_briefings()
