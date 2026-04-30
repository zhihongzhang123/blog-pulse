#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简报生成器 - 博客集成版

流程：
1. 运行新闻简报 v4.0 脚本获取数据
2. AI 读取数据生成简报 Markdown
3. 保存为博客内容文件
4. 可选推送到 Telegram/PushPlus

用法:
    python3 generate_blog_briefing.py morning
    python3 generate_blog_briefing.py evening
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

CONTENT_DIR = Path(__file__).parent.parent / 'content' / 'briefings'


def run_data_pipeline(pipeline_type: str) -> dict:
    """运行数据获取管线"""
    script_path = Path('/Users/minimac/.hermes/skills/finance/news-brief/scripts/generate_v3.py')
    
    result = subprocess.run(
        ['python3', str(script_path), pipeline_type],
        capture_output=True,
        text=True,
        timeout=120
    )
    
    # 读取生成的 JSON
    json_path = Path(f'/tmp/news-brief-v3-{pipeline_type}.json')
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    raise Exception(f"数据管线失败: {result.stderr}")


def generate_briefing_content(data: dict, pipeline_type: str) -> str:
    """生成简报 Markdown 内容"""
    now = datetime.now()
    date_str = data.get('date', now.strftime('%Y-%m-%d'))
    time_str = data.get('time', now.strftime('%H:%M'))
    type_label = "早报" if pipeline_type == "morning" else "晚报"
    
    # 提取市场数据
    market = data.get('market_data', {})
    stocks = data.get('stock_prices', [])
    news = data.get('news', [])
    
    # 生成简报内容
    content = f"""# {type_label}简报 — {date_str}

## 核心主线

"""
    
    # 添加新闻摘要
    if news:
        content += "### 今日要闻\n\n"
        for i, item in enumerate(news[:8], 1):
            title = item.get('title', '')
            source = item.get('source', '')
            content += f"{i}. **{title}** — {source}\n"
    
    # 添加市场数据
    content += "\n## 市场数据\n\n"
    
    indices = market.get('indices', {})
    if indices:
        content += "### 指数\n\n| 指数 | 价格 | 涨跌幅 |\n|------|------|--------|\n"
        for symbol, info in indices.items():
            price = info.get('price', 0)
            change = info.get('change_pct', 0)
            change_str = f"{change:+.2f}%"
            content += f"| {symbol} | {price:.2f} | {change_str} |\n"
    
    commodities = market.get('commodities', {})
    if commodities:
        content += "\n### 商品\n\n| 商品 | 价格 | 涨跌幅 |\n|------|------|--------|\n"
        for symbol, info in commodities.items():
            name = info.get('name', symbol)
            price = info.get('price', 0)
            change = info.get('change_pct', 0)
            change_str = f"{change:+.2f}%"
            content += f"| {name} | ${price:.2f} | {change_str} |\n"
    
    # 添加个股数据
    if stocks:
        content += "\n## 关注个股\n\n| 代码 | 名称 | 价格 | 涨跌幅 |\n|------|------|------|--------|\n"
        for stock in stocks:
            symbol = stock.get('symbol', '')
            name = stock.get('name', '')
            price = stock.get('price', 0)
            change = stock.get('change_pct', 0)
            change_str = f"{change:+.2f}%"
            content += f"| {symbol} | {name} | ${price:.2f} | {change_str} |\n"
    
    # 添加数据截点
    content += f"\n---\n\n⏰ 数据截点：{date_str} {time_str}\n\n"
    content += "*12H 宏观交易简报 · Pulse 生成 · 永远利他*\n"
    
    return content


def save_briefing(content: str, pipeline_type: str, date_str: str) -> str:
    """保存简报为 Markdown 文件"""
    slug = f"{pipeline_type}-{date_str.replace('-', '')}"
    filepath = CONTENT_DIR / f"{slug}.md"
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return str(filepath)


def main(pipeline_type: str = 'evening'):
    print(f"📝 生成{pipeline_type}简报...")
    
    # 1. 获取数据
    print("📊 获取数据...")
    data = run_data_pipeline(pipeline_type)
    print(f"✅ 获取 {data.get('news_count', 0)} 条新闻")
    
    # 2. 生成内容
    print("✍️  生成简报内容...")
    content = generate_briefing_content(data, pipeline_type)
    
    # 3. 保存
    date_str = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    filepath = save_briefing(content, pipeline_type, date_str)
    print(f"✅ 简报已保存：{filepath}")
    
    return filepath


if __name__ == '__main__':
    pipeline_type = sys.argv[1] if len(sys.argv) > 1 else 'evening'
    main(pipeline_type)
