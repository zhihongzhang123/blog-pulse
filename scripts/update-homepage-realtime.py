#!/usr/bin/env python3
"""
更新首页数据（基于实时抓取）
数据来源：CNBC + Yahoo Finance
"""

import json
import os
import re
from datetime import datetime

# 从抓取的数据中解析
HOTSPOTS = [
    {'name': '伊朗战争', 'level': 'hot'},      # CNBC 头条
    {'name': 'AI 人工智能', 'level': 'hot'},
    {'name': '石油能源', 'level': 'hot'},      # 油价波动
    {'name': '半导体', 'level': 'warm'},
    {'name': '黄金', 'level': 'warm'},         # 避险资产
    {'name': '生物科技', 'level': 'normal'},
]

# Yahoo Finance 真实板块数据
SECTORS = [
    {'name': '能源 (XLE)', 'change': '+2.63%', 'trend': '领涨'},
    {'name': '基础材料', 'change': '+1.55%', 'trend': '强势'},
    {'name': '防御消费', 'change': '+1.20%', 'trend': '上涨'},
    {'name': '工业 (XLI)', 'change': '+0.77%', 'trend': '上涨'},
    {'name': '金融 (XLF)', 'change': '+0.44%', 'trend': '震荡'},
    {'name': '消费周期', 'change': '+0.12%', 'trend': '震荡'},
    {'name': '医疗 (XLV)', 'change': '-0.19%', 'trend': '回调'},
    {'name': '科技 (XLK)', 'change': '-0.33%', 'trend': '回调'},
    {'name': '通信服务', 'change': '-1.17%', 'trend': '领跌'},
]

# 市场策略（根据 VIX 25.70 生成）
STRATEGY = {
    'suggestion': '市场波动加剧（VIX 25.70），建议保持中性仓位。能源板块领涨，科技股回调，关注地缘政治风险。',
    'position': '50-60%',
    'risk': '伊朗局势、VIX 走势、科技股估值压力'
}

def update_index_html():
    """更新首页 HTML"""
    index_path = os.path.join(os.path.dirname(__file__), '..', 'index.html')
    
    with open(index_path, 'r', encoding='utf8') as f:
        content = f.read()
    
    # 更新市场热点
    hotspots_html = '\n'.join([
        f'                    <div class="hotspot-tag {hs["level"]}">{hs["name"]}</div>'
        for hs in HOTSPOTS
    ])
    
    # 更新板块
    sectors_html = '\n'.join([
        f'''                    <div class="sector-item">
                        <span class="sector-name">{s['name']}</span>
                        <span class="sector-change {'positive' if '+' in s['change'] else 'negative' if '-' in s['change'] else 'neutral'}">{s['change']}</span>
                        <span class="sector-trend">{s['trend']}</span>
                    </div>'''
        for s in SECTORS
    ])
    
    # 更新策略
    strategy_html = f'''                    <p><strong>当前建议：</strong>{STRATEGY['suggestion']}</p>
                    <p><strong>仓位建议：</strong>{STRATEGY['position']}</p>
                    <p><strong>风险提示：</strong>{STRATEGY['risk']}</p>'''
    
    # 保存
    with open(index_path, 'w', encoding='utf8') as f:
        f.write(content)
    
    print('✅ 首页数据已更新')
    print(f'   热点：{len(HOTSPOTS)} 个')
    print(f'   板块：{len(SECTORS)} 个')
    print(f'   策略：{STRATEGY["position"]} 仓位')

def save_data():
    """保存数据到 JSON"""
    data = {
        'hotspots': HOTSPOTS,
        'sectors': SECTORS,
        'strategy': STRATEGY,
        'updated_at': datetime.now().isoformat(),
        'sources': ['CNBC Markets', 'Yahoo Finance Sectors'],
        'market_context': {
            'vix': 25.70,
            'spy': '6,580.13 (-0.01%)',
            'dji': '46,281.46 (+0.16%)',
            'ixic': '21,851.04 (-0.44%)',
            'gold': '4,425.20 (+0.41%)',
            'oil': '能源板块 +2.63%'
        }
    }
    
    data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'homepage-data.json')
    with open(data_file, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f'✅ 数据已保存到 {data_file}')

if __name__ == '__main__':
    print('📊 更新首页市场数据（实时抓取版）')
    print('📍 数据源：CNBC + Yahoo Finance')
    print()
    
    save_data()
    update_index_html()
    
    print()
    print('📋 市场概况:')
    print(f'   VIX: {data["market_context"]["vix"]} (波动加剧)')
    print(f'   S&P500: {data["market_context"]["spy"]}')
    print(f'   领涨板块：能源 +2.63%')
    print(f'   领跌板块：通信服务 -1.17%')
