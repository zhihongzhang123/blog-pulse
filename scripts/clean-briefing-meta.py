#!/usr/bin/env python3
"""
清理简报页面的技术元数据
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.join(BASE_DIR, 'data/news/latest.html')

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 移除技术元数据
content = content.replace(' (TL;DR)', '')
content = content.replace(' (Asia/Shanghai)', '')
content = content.replace('12H 宏观交易新闻简报 · 自动推送', '12H 宏观交易新闻简报')
content = content.replace('<em>推送渠道：PushPlus 微信</em><br>', '')

with open(FILE_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 已清理技术元数据")
