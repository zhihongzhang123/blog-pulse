#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
博客数据同步脚本

功能：
1. 同步最新新闻简报到 data/news/
2. 同步美股分析报告到 data/market/
3. 生成实时数据索引
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path('/Users/minimac/.openclaw/workspace')
BLOG_DATA = WORKSPACE / 'blog-pulse/data'

# 数据源路径
PUSH_STATS = WORKSPACE / 'memory/push-stats.json'
MEMORY_DIR = WORKSPACE / 'memory'

# 目标路径
NEWS_DIR = BLOG_DATA / 'news'
MARKET_DIR = BLOG_DATA / 'market'
TRADING_DIR = BLOG_DATA / 'trading'


def sync_latest_briefing():
    """同步最新新闻简报"""
    print("📰 同步新闻简报...")
    
    # 读取推送统计
    if not PUSH_STATS.exists():
        print("  ⚠️  push-stats.json 不存在")
        return False
    
    with open(PUSH_STATS) as f:
        stats = json.load(f)
    
    # 查找对应的简报文件
    # 格式：memory/push-YYYYMMDD-HHMMSS.json
    briefing_files = list(MEMORY_DIR.glob('push-*.json'))
    if not briefing_files:
        print("  ⚠️  未找到推送文件，创建测试数据")
        # 创建测试数据
        NEWS_DIR.mkdir(parents=True, exist_ok=True)
        test_briefing = {
            'title': '🟢 2026-03-22 晚报 | 全球宏观与核心交易线索',
            'content': '测试数据：新闻简报已推送\nMsgID: 831e17d5edf749e190289d9f449a5a4b\n\n核心主线:\n- 中东局势升级\n- 美股连续下跌\n- 科技巨头扩张\n- 能源危机',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'evening',
            'newsCount': 49
        }
        dest = NEWS_DIR / 'latest.json'
        with open(dest, 'w', encoding='utf-8') as f:
            json.dump(test_briefing, f, indent=2, ensure_ascii=False)
        
        # 生成 HTML
        html_content = generate_briefing_html(test_briefing)
        html_dest = NEWS_DIR / 'latest.html'
        with open(html_dest, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"  ✅ 已创建测试数据")
        return True
    
    # 取最新的
    latest_file = max(briefing_files, key=lambda p: p.stat().st_mtime)
    
    # 复制到博客数据目录
    NEWS_DIR.mkdir(parents=True, exist_ok=True)
    dest = NEWS_DIR / 'latest.json'
    shutil.copy2(latest_file, dest)
    
    # 同时保存 HTML 版本
    with open(latest_file) as f:
        briefing = json.load(f)
    
    html_content = generate_briefing_html(briefing)
    html_dest = NEWS_DIR / 'latest.html'
    with open(html_dest, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"  ✅ 已同步：{latest_file.name}")
    return True


def generate_briefing_html(briefing: dict) -> str:
    """生成简报 HTML"""
    title = briefing.get('title', '新闻简报')
    content = briefing.get('content', '')
    timestamp = briefing.get('timestamp', '')
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} · Pulse</title>
    <link rel="stylesheet" href="../styles.css">
    <style>
        .briefing-container {{ max-width: 900px; margin: 0 auto; padding: 40px 20px; }}
        .briefing-header {{ text-align: center; margin-bottom: 40px; }}
        .briefing-title {{ font-size: 2rem; margin-bottom: 10px; }}
        .briefing-time {{ color: #86868b; }}
        .briefing-content {{ 
            background: rgba(44, 44, 46, 0.65);
            backdrop-filter: blur(20px);
            padding: 30px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            white-space: pre-wrap;
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
            line-height: 1.8;
        }}
        .back-link {{ 
            display: inline-block; 
            margin-bottom: 20px; 
            color: #0a84ff; 
            text-decoration: none; 
        }}
    </style>
</head>
<body>
    <div class="briefing-container">
        <a href="../index.html" class="back-link">← 返回首页</a>
        <header class="briefing-header">
            <h1 class="briefing-title">{title}</h1>
            <div class="briefing-time">{timestamp}</div>
        </header>
        <div class="briefing-content">
{content}
        </div>
    </div>
</body>
</html>
"""
    return html


def sync_market_analysis():
    """同步美股市场分析"""
    print("📈 同步美股分析...")
    
    # 查找最新的分析报告
    analysis_files = list(MEMORY_DIR.glob('market-analysis-*.json'))
    
    if not analysis_files:
        print("  ⚠️  未找到分析报告")
        return False
    
    latest_file = max(analysis_files, key=lambda p: p.stat().st_mtime)
    
    # 复制到博客数据目录
    MARKET_DIR.mkdir(parents=True, exist_ok=True)
    dest = MARKET_DIR / 'latest.json'
    shutil.copy2(latest_file, dest)
    
    print(f"  ✅ 已同步：{latest_file.name}")
    return True


def generate_trading_data():
    """生成交易数据（模拟，后续接入真实 API）"""
    print("⚡ 生成交易数据...")
    
    # 模拟数据（后续替换为真实 API）
    trading_data = {
        'timestamp': datetime.now().isoformat(),
        'positions': {
            'total': 65,
            'today_pnl': 2.3,
            'month_pnl': 8.7
        },
        'risk': {
            'vix': 18.5,
            'put_call': 0.82,
            'sentiment': 55
        }
    }
    
    TRADING_DIR.mkdir(parents=True, exist_ok=True)
    dest = TRADING_DIR / 'dashboard.json'
    
    with open(dest, 'w', encoding='utf-8') as f:
        json.dump(trading_data, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ 已生成：{dest.name}")
    return True


def update_index():
    """更新数据索引"""
    print("📑 更新索引...")
    
    index = {
        'updated': datetime.now().isoformat(),
        'news': (NEWS_DIR / 'latest.json').exists(),
        'market': (MARKET_DIR / 'latest.json').exists(),
        'trading': (TRADING_DIR / 'dashboard.json').exists()
    }
    
    with open(BLOG_DATA / 'index.json', 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print("  ✅ 索引已更新")
    return True


def main():
    """主函数"""
    print("="*60)
    print("📊 博客数据同步")
    print("="*60)
    
    results = []
    results.append(('新闻简报', sync_latest_briefing()))
    results.append(('美股分析', sync_market_analysis()))
    results.append(('交易数据', generate_trading_data()))
    results.append(('数据索引', update_index()))
    
    print("\n" + "="*60)
    print("同步结果:")
    for name, success in results:
        status = "✅" if success else "❌"
        print(f"  {status} {name}")
    print("="*60)
    
    # 返回成功数量
    success_count = sum(1 for _, s in results if s)
    print(f"\n总计：{success_count}/{len(results)} 成功")
    
    return success_count == len(results)


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
