#!/usr/bin/env python3
"""
调整博客首页模块顺序
将市场情绪移到每日思考前面
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.join(BASE_DIR, 'index.html')

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 更新导航顺序
content = re.sub(
    r'<nav class="nav">\s*<a href="#daily-thoughts" class="active">每日思考</a>\s*<a href="#market-sentiment">市场情绪</a>\s*<a href="#market-analysis">市场分析</a>\s*<a href="#briefings">新闻简报</a>\s*<a href="about.html">关于</a>\s*</nav>',
    '''<nav class="nav">
                <a href="#market-sentiment">市场情绪</a>
                <a href="#daily-thoughts" class="active">每日思考</a>
                <a href="#market-analysis">市场分析</a>
                <a href="#briefings">新闻简报</a>
                <a href="about.html">关于</a>
            </nav>''',
    content,
    flags=re.MULTILINE | re.DOTALL
)

# 2. 调整模块顺序 - 提取市场情绪模块
sentiment_pattern = r'(        <!-- 市场情绪 -->\s*<section id="market-sentiment" class="section section-spaced">.*?</section>)'
sentiment_match = re.search(sentiment_pattern, content, re.DOTALL)

if sentiment_match:
    sentiment_section = sentiment_match.group(1)
    # 移除原位置
    content = content.replace(sentiment_section, '')
    # 插入到每日思考前面
    daily_thoughts_pos = content.find('<!-- 每日思考 -->')
    if daily_thoughts_pos != -1:
        content = content[:daily_thoughts_pos] + sentiment_section + '\n\n' + content[daily_thoughts_pos:]
        print("✅ 已调整市场情绪模块到每日思考前面")
    else:
        print("❌ 未找到每日思考模块")
else:
    print("❌ 未找到市场情绪模块")

with open(FILE_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 首页模块顺序已更新")
