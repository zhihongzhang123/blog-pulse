#!/usr/bin/env python3
"""
优化博客首页模块顺序和间距
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.join(BASE_DIR, 'index.html')

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 优化导航顺序：市场情绪提前到市场分析前面
content = content.replace(
    '''<nav class="nav">
                <a href="#daily-thoughts" class="active">每日思考</a>
                <a href="#market-analysis">市场分析</a>
                <a href="#briefings">新闻简报</a>
                <a href="about.html">关于</a>
            </nav>''',
    '''<nav class="nav">
                <a href="#daily-thoughts" class="active">每日思考</a>
                <a href="#market-sentiment">市场情绪</a>
                <a href="#market-analysis">市场分析</a>
                <a href="#briefings">新闻简报</a>
                <a href="about.html">关于</a>
            </nav>'''
)

# 2. 增加模块间距 - 在 section 类名中添加额外间距类
content = content.replace(
    '<section id="market-sentiment" class="section">',
    '<section id="market-sentiment" class="section section-spaced">'
)

content = content.replace(
    '<section id="briefings" class="section">',
    '<section id="briefings" class="section section-spaced">'
)

with open(FILE_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 已优化首页模块顺序和间距")
print("   - 导航顺序：市场情绪提前到市场分析前")
print("   - 增加市场情绪和新闻简报的上下间距")
