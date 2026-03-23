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
    """生成 HTML 格式"""
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
    <link rel="stylesheet" href="../../styles.css">
    <style>
        .briefing-container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        .briefing-header {{
            margin-bottom: 40px;
        }}
        .briefing-title {{
            font-family: 'Playfair Display', serif;
            font-size: 2rem;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #ffd60a 0%, #ff9f0a 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .briefing-meta {{
            color: #86868b;
            font-size: 0.9rem;
        }}
        .briefing-content {{
            line-height: 1.8;
            white-space: pre-wrap;
        }}
        .back-link {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: #0a84ff;
            text-decoration: none;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="briefing-container">
        <a href="../../index.html" class="back-link">← 返回首页</a>
        
        <div class="briefing-header">
            <h1 class="briefing-title">{data['title']}</h1>
            <div class="briefing-meta">
                <span>📅 {data['pushTime'] or '未知'}</span> • 
                <span>📊 {data['newsCount']} 条新闻</span> •
                <span>🆔 {data['msgid'] or 'N/A'}</span>
            </div>
        </div>
        
        <div class="briefing-content">
{content_html}
        </div>
    </div>
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
