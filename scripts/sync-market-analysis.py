#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
美股分析报告自动同步脚本

功能:
1. 从 us-market-pipeline 输出目录同步最新报告
2. 转换为博客文章格式
3. 更新首页市场分析板块

用法:
    python3 scripts/sync-market-analysis.py [post-market|pre-market]
"""

import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

def sync_market_report(report_type: str = 'post-market'):
    """同步美股分析报告到博客"""
    
    # 源目录 (us-market-pipeline 输出)
    source_dir = Path('../us-market-pipeline/output')
    if not source_dir.exists():
        print(f"❌ 源目录不存在：{source_dir}")
        print("   请先运行美股分析流水线生成报告")
        return None
    
    # 目标目录 (博客内容)
    target_dir = Path('content/market-analysis')
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # 查找最新报告
    report_files = list(source_dir.glob(f'report-{report_type}-*.md'))
    if not report_files:
        print(f"❌ 未找到 {report_type} 报告")
        return None
    
    # 按时间排序，获取最新
    latest_report = max(report_files, key=lambda p: p.stat().st_mtime)
    print(f"📄 找到最新报告：{latest_report.name}")
    
    # 读取报告内容
    with open(latest_report, 'r', encoding='utf-8') as f:
        report_content = f.read()
    
    # 生成文件名
    today = datetime.now().strftime('%Y-%m-%d')
    time_str = datetime.now().strftime('%H%M%S')
    filename = f"{today}-{report_type}-{time_str}.md"
    target_path = target_dir / filename
    
    # 保存报告
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"✅ 报告已同步：{target_path}")
    
    # 生成 HTML 版本 (可选)
    html_path = generate_html_report(report_content, target_dir, today, report_type)
    if html_path:
        print(f"✅ HTML 报告：{html_path}")
    
    return str(target_path)


def generate_html_report(content: str, target_dir: Path, date: str, report_type: str):
    """将 Markdown 报告转换为 HTML"""
    
    report_type_name = "盘后总结" if report_type == 'post-market' else "盘前预测"
    
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>美股市场分析 · {report_type_name} · Pulse</title>
    <link rel="stylesheet" href="../../styles.css">
    <style>
        .report-container {{
            max-width: 900px;
            margin: 0 auto;
            padding: var(--spacing-xl) var(--spacing-md);
        }}
        
        .report-header {{
            text-align: center;
            margin-bottom: var(--spacing-xl);
            padding-bottom: var(--spacing-lg);
            border-bottom: 2px solid var(--color-gold);
        }}
        
        .report-title {{
            font-family: var(--font-serif);
            font-size: 2rem;
            margin-bottom: var(--spacing-sm);
        }}
        
        .report-date {{
            color: var(--color-text-muted);
            font-size: 0.95rem;
        }}
        
        .report-content {{
            font-size: 1rem;
            line-height: 1.8;
            white-space: pre-wrap;
        }}
        
        .report-content h1,
        .report-content h2,
        .report-content h3 {{
            font-family: var(--font-serif);
            margin-top: var(--spacing-xl);
            margin-bottom: var(--spacing-md);
        }}
        
        .report-content table {{
            width: 100%;
            border-collapse: collapse;
            margin: var(--spacing-lg) 0;
        }}
        
        .report-content th,
        .report-content td {{
            padding: var(--spacing-sm) var(--spacing-md);
            border: 1px solid var(--color-border);
            text-align: left;
        }}
        
        .report-content th {{
            background: var(--color-gold-light);
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="report-container">
        <header class="report-header">
            <h1 class="report-title">💎 美股市场分析 · {report_type_name}</h1>
            <div class="report-date">📅 {date} (Asia/Shanghai)</div>
        </header>
        
        <div class="report-content">
{content}
        </div>
    </div>
    
    <script src="../../main.js"></script>
</body>
</html>
"""
    
    # 保存 HTML
    html_filename = f"{date}-{report_type}-{datetime.now().strftime('%H%M%S')}.html"
    html_path = target_dir / html_filename
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    return str(html_path)


def update_homepage(latest_report_path: str, report_type: str):
    """更新首页市场分析板块"""
    
    homepage = Path('index.html')
    if not homepage.exists():
        print("⚠️  首页不存在，跳过更新")
        return
    
    # 读取首页内容
    with open(homepage, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # TODO: 更新首页的分析卡片状态
    # 这里可以添加逻辑来更新首页的"已更新"状态
    
    print("📝 首页更新待实现")


def main():
    if len(sys.argv) > 1:
        report_type = sys.argv[1]
        if report_type not in ['post-market', 'pre-market']:
            print("❌ 无效的报告类型，请使用 post-market 或 pre-market")
            sys.exit(1)
    else:
        report_type = 'post-market'
    
    print("=" * 60)
    print("📈 美股分析报告同步工具")
    print("=" * 60)
    
    result = sync_market_report(report_type)
    
    if result:
        print("\n✅ 同步完成！")
        print(f"\n📝 下一步:")
        print(f"   1. 查看报告：{result}")
        print(f"   2. 更新首页链接")
        print(f"   3. 推送部署：git add . && git commit && git push")
    else:
        print("\n❌ 同步失败")
        sys.exit(1)


if __name__ == '__main__':
    main()
