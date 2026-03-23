#!/usr/bin/env python3
"""
为文章页面添加主题切换器
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.join(BASE_DIR, 'content/articles/market-sentiment-6-dimensions.html')

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 在 article-header 前添加主题切换器
old_header = '''        <header class="article-header">
            <div class="article-date">📅 2026 年 3 月 24 日</div>'''

new_header = '''        <!-- 主题切换器 -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px;">
            <a href="../../index.html" class="nav-back" style="margin-bottom: 0;">← 返回首页</a>
            <div class="mode-switcher" style="display: flex; gap: 8px;">
                <button class="switch-btn" data-mode="light" title="浅色模式" style="padding: 8px 12px; border: 1px solid var(--apple-border); border-radius: 20px; background: var(--apple-bg-secondary); cursor: pointer;">
                    <span style="font-size: 16px;">☀️</span>
                </button>
                <button class="switch-btn" data-mode="dark" title="深色模式" style="padding: 8px 12px; border: 1px solid var(--apple-border); border-radius: 20px; background: var(--apple-bg-secondary); cursor: pointer;">
                    <span style="font-size: 16px;">🌙</span>
                </button>
                <button class="switch-btn" data-mode="auto" title="跟随系统" style="padding: 8px 12px; border: 1px solid var(--apple-border); border-radius: 20px; background: var(--apple-bg-secondary); cursor: pointer;">
                    <span style="font-size: 16px;">🔄</span>
                </button>
            </div>
        </div>
        
        <header class="article-header">
            <div class="article-date">📅 2026 年 3 月 24 日</div>'''

content = content.replace(old_header, new_header)

# 2. 移除原来的返回链接 (重复了)
old_back_link = '''        <a href="../../index.html" class="nav-back">返回首页</a>
        
        <!-- 主题切换器 -->'''

content = content.replace(old_back_link, '')

with open(FILE_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 已添加主题切换器")
