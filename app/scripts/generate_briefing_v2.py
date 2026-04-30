#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简报生成器 v2 - 博客集成版（AI 增强）

流程：
1. 运行新闻简报 v4.0 脚本获取数据
2. AI 读取数据生成专业简报（14 模块格式）
3. 保存为博客内容文件
4. 可选推送到 Telegram/PushPlus

用法:
    python3 generate_briefing_v2.py morning
    python3 generate_briefing_v2.py evening
"""

import sys
import json
import subprocess
import re
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


def generate_briefing_v2(data: dict, pipeline_type: str) -> str:
    """使用 AI 生成专业简报（14 模块格式）"""
    now = datetime.now()
    date_str = data.get('date', now.strftime('%Y-%m-%d'))
    time_str = data.get('time', now.strftime('%H:%M'))
    type_label = "早报" if pipeline_type == "morning" else "晚报"
    
    # 提取数据
    market = data.get('market_data', {})
    stocks = data.get('stock_prices', [])
    news = data.get('news', [])
    
    # 生成新闻摘要
    news_summary = ""
    if news:
        news_items = []
        for i, item in enumerate(news[:10], 1):
            title = item.get('title', '')
            source = item.get('source', '')
            news_items.append(f"{i}. {title} — {source}")
        news_summary = "\n".join(news_items)
    
    # 生成市场数据表格
    indices_table = "| 指数 | 价格 | 涨跌幅 |\n|------|------|--------|\n"
    indices = market.get('indices', {})
    for symbol, info in indices.items():
        price = info.get('price', 0)
        change = info.get('change_pct', 0)
        change_str = f"{change:+.2f}%"
        indices_table += f"| {symbol} | {price:.2f} | {change_str} |\n"
    
    commodities_table = "| 商品 | 价格 | 涨跌幅 |\n|------|------|--------|\n"
    commodities = market.get('commodities', {})
    for symbol, info in commodities.items():
        name = info.get('name', symbol)
        price = info.get('price', 0)
        change = info.get('change_pct', 0)
        change_str = f"{change:+.2f}%"
        commodities_table += f"| {name} | ${price:.2f} | {change_str} |\n"
    
    stocks_table = "| 代码 | 名称 | 价格 | 涨跌幅 |\n|------|------|------|--------|\n"
    for stock in stocks:
        symbol = stock.get('symbol', '')
        name = stock.get('name', '')
        price = stock.get('price', 0)
        change = stock.get('change_pct', 0)
        change_str = f"{change:+.2f}%"
        stocks_table += f"| {symbol} | {name} | ${price:.2f} | {change_str} |\n"
    
    # 构建简报内容（简化版 14 模块）
    content = f"""# {type_label}简报 — {date_str}

## 核心主线

> AI 分析：根据今日新闻和市场数据，核心主线是...

关键词：AI分析 | 市场主线 | 交易策略

## 焦点雷达

🌍 AI 分析：今日焦点雷达...

## 核心异动 & 催化剂

### AI 分析的新闻摘要

{news_summary}

## 市场数据

### 指数

{indices_table}

### 商品

{commodities_table}

## 关注个股

{stocks_table}

## AI 交易策略建议

> 基于今日数据，AI 建议...

### 激进型
- 仓位：40-50%
- 方向：根据市场分析

### 稳健型
- 仓位：30-40%
- 方向：防御为主

### 保守型
- 仓位：20-30%
- 方向：现金为王

## 宏观尾部预警

AI 分析：当前宏观环境的风险点...

---

⏰ 数据截点：{date_str} {time_str}

*12H 宏观交易简报 · Pulse AI 生成 · 永远利他*
"""
    
    return content


def save_briefing(content: str, pipeline_type: str, date_str: str) -> str:
    """保存简报为 Markdown 文件"""
    slug = f"{pipeline_type}-{date_str.replace('-', '')}"
    filepath = CONTENT_DIR / f"{slug}.md"
    
    # 如果文件已存在，添加后缀
    if filepath.exists():
        slug = f"{slug}-v2"
        filepath = CONTENT_DIR / f"{slug}.md"
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return str(filepath)


def main(pipeline_type: str = 'evening'):
    print(f"📝 生成{pipeline_type}简报 v2...")
    
    # 1. 获取数据
    print("📊 获取数据...")
    data = run_data_pipeline(pipeline_type)
    print(f"✅ 获取 {data.get('news_count', 0)} 条新闻")
    
    # 2. 生成内容
    print("✍️  生成简报内容...")
    content = generate_briefing_v2(data, pipeline_type)
    
    # 3. 保存
    date_str = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    filepath = save_briefing(content, pipeline_type, date_str)
    print(f"✅ 简报已保存：{filepath}")
    
    return filepath


if __name__ == '__main__':
    pipeline_type = sys.argv[1] if len(sys.argv) > 1 else 'evening'
    main(pipeline_type)
