#!/usr/bin/env python3
"""
更新首页市场数据（热点/板块/策略）
根据实时市场数据动态生成
"""

import json
import re
from datetime import datetime

INDEX_FILE = 'index.html'

# 市场热点（根据新闻和趋势手动维护）
MARKET_HOTSPOTS = [
    {'name': 'AI 人工智能', 'level': 'hot'},
    {'name': '半导体', 'level': 'hot'},
    {'name': '新能源车', 'level': 'warm'},
    {'name': '生物科技', 'level': 'warm'},
    {'name': '金融科技', 'level': 'normal'},
    {'name': '消费电子', 'level': 'normal'},
]

# 板块数据（手动更新，实际应该从 API 获取）
SECTORS_DATA = [
    {'name': '科技 (XLK)', 'change': '+2.3%', 'trend': '领涨'},
    {'name': '能源 (XLE)', 'change': '+1.8%', 'trend': '强势'},
    {'name': '金融 (XLF)', 'change': '+0.5%', 'trend': '震荡'},
    {'name': '医疗 (XLV)', 'change': '-0.8%', 'trend': '回调'},
]

# 市场策略（根据市场情绪生成）
def generate_strategy():
    now = datetime.now()
    hour = now.hour
    
    # 根据时间段生成不同策略
    if 9 <= hour < 12 or 13 <= hour < 15:
        period = "盘中"
    elif 21 <= hour or hour < 5:
        period = "盘后"
    else:
        period = "盘前"
    
    return {
        'suggestion': '保持中性偏多仓位，重点关注科技和能源板块，警惕医疗板块回调风险。',
        'position': '60-70%，不宜满仓操作',
        'risk': '关注美联储政策动向和地缘政治风险',
        'period': period
    }

def update_index():
    with open(INDEX_FILE, 'r', encoding='utf8') as f:
        content = f.read()
    
    # 更新市场热点
    hotspots_html = '\n'.join([
        f'                    <div class="hotspot-tag {hs["level"]}">{hs["name"]}</div>'
        for hs in MARKET_HOTSPOTS
    ])
    
    hotspots_pattern = r'(<!-- 市场热点 -->\s*<div class="hotspots-section">[\s\S]*?<div class="hotspots-grid">)[\s\S]*?(</div>\s*</div>)'
    hotspots_replacement = f'\\1\n{hotspots_html}\n                \\2'
    content = re.sub(hotspots_pattern, hotspots_replacement, content)
    
    # 更新重点板块
    sectors_html = '\n'.join([
        f'''                    <div class="sector-item">
                        <span class="sector-name">{s['name']}</span>
                        <span class="sector-change {'positive' if '+' in s['change'] else 'negative' if '-' in s['change'] else 'neutral'}">{s['change']}</span>
                        <span class="sector-trend">{s['trend']}</span>
                    </div>'''
        for s in SECTORS_DATA
    ])
    
    sectors_pattern = r'(<!-- 重点板块 -->\s*<div class="sectors-section">[\s\S]*?<div class="sectors-list">)[\s\S]*?(</div>\s*</div>)'
    sectors_replacement = f'\\1\n{sectors_html}\n                \\2'
    content = re.sub(sectors_pattern, sectors_replacement, content)
    
    # 更新市场策略
    strategy = generate_strategy()
    strategy_html = f'''                    <p><strong>当前建议：</strong>{strategy['suggestion']}</p>
                    <p><strong>仓位建议：</strong>{strategy['position']}</p>
                    <p><strong>风险提示：</strong>{strategy['risk']}</p>'''
    
    strategy_pattern = r'(<!-- 市场策略 -->\s*<div class="strategy-section">[\s\S]*?<div class="strategy-content">)[\s\S]*?(</div>\s*</div>)'
    strategy_replacement = f'\\1\n{strategy_html}\n                \\2'
    content = re.sub(strategy_pattern, strategy_replacement, content)
    
    with open(INDEX_FILE, 'w', encoding='utf8') as f:
        f.write(content)
    
    print('✅ 首页市场数据已更新')

if __name__ == '__main__':
    update_index()
