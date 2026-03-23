#!/usr/bin/env python3
"""
优化简报标题格式
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.join(BASE_DIR, 'data/news/latest.html')

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 优化标题格式
# 原标题：🟢 2026-03-21 evening | 全球宏观与核心交易线索
# 新标题：📰 2026-03-21 晚报 | 全球宏观与核心交易线索

# 修复浏览器标题
content = re.sub(
    r'<title>🟢 (\d{4}-\d{2}-\d{2}) evening \| (.*?) · Pulse</title>',
    r'<title>📰 \1 晚报 | \2 · Pulse</title>',
    content
)

# 修复页面主标题
content = re.sub(
    r'<h1>🟢 (\d{4}-\d{2}-\d{2}) evening \| (.*?)</h1>',
    r'<h1>📰 \1 晚报 | \2</h1>',
    content
)

# 修复副标题
content = re.sub(
    r'<p>🟢 (\d{4}-\d{2}-\d{2}) 晚报 \| (.*?)</p>',
    r'<p><strong>\1 晚报</strong> | \2</p>',
    content
)

with open(FILE_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 已优化简报标题格式")
