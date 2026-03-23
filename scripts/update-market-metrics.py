#!/usr/bin/env python3
"""
更新市场情绪模块指标
替换抽象指标为具体数据指标
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.join(BASE_DIR, 'index.html')

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换整个 sentiment-grid 部分
old_grid = '''            <div class="sentiment-grid">
                <!-- 市场整体情绪 -->
                <div class="sentiment-card">
                    <div class="sentiment-header">
                        <span class="sentiment-icon">🎯</span>
                        <h3>市场整体情绪</h3>
                    </div>
                    <div class="sentiment-value neutral">中性偏多</div>
                    <div class="sentiment-bar">
                        <div class="sentiment-fill" style="width: 60%"></div>
                    </div>
                    <p class="sentiment-desc">风险情绪回暖，投资者谨慎乐观</p>
                </div>
                
                <!-- 市场宽度 -->
                <div class="sentiment-card">
                    <div class="sentiment-header">
                        <span class="sentiment-icon">📊</span>
                        <h3>市场宽度</h3>
                    </div>
                    <div class="sentiment-value positive">65%</div>
                    <p class="sentiment-desc">上涨股票占比，市场参与度良好</p>
                </div>
                
                <!-- 市场温度 -->
                <div class="sentiment-card">
                    <div class="sentiment-header">
                        <span class="sentiment-icon">🌡️</span>
                        <h3>市场温度</h3>
                    </div>
                    <div class="sentiment-value warm">62°C</div>
                    <div class="temperature-gauge">
                        <div class="gauge-fill" style="width: 62%"></div>
                    </div>
                    <p class="sentiment-desc">温度适中，不宜过度交易</p>
                </div>
                
                <!-- 恐慌指数 -->
                <div class="sentiment-card">
                    <div class="sentiment-header">
                        <span class="sentiment-icon">😨</span>
                        <h3>VIX 恐慌指数</h3>
                    </div>
                    <div class="sentiment-value low">18.5</div>
                    <p class="sentiment-desc">低于 20，市场情绪稳定</p>
                </div>
            </div>'''

new_grid = '''            <div class="sentiment-grid">
                <!-- 标普 500 趋势 -->
                <div class="sentiment-card">
                    <div class="sentiment-header">
                        <span class="sentiment-icon">📈</span>
                        <h3>标普 500 趋势</h3>
                    </div>
                    <div class="sentiment-value positive">+0.8%</div>
                    <div class="sentiment-bar">
                        <div class="sentiment-fill positive" style="width: 65%"></div>
                    </div>
                    <p class="sentiment-desc">价格位于 200 日均线上方，趋势偏多</p>
                </div>
                
                <!-- 市场宽度 -->
                <div class="sentiment-card">
                    <div class="sentiment-header">
                        <span class="sentiment-icon">📊</span>
                        <h3>市场宽度</h3>
                    </div>
                    <div class="sentiment-value positive">65%</div>
                    <p class="sentiment-desc">NYSE 上涨家数占比，市场参与度良好</p>
                </div>
                
                <!-- 市场温度 (RSI) -->
                <div class="sentiment-card">
                    <div class="sentiment-header">
                        <span class="sentiment-icon">🌡️</span>
                        <h3>市场温度 (RSI)</h3>
                    </div>
                    <div class="sentiment-value warm">62</div>
                    <div class="temperature-gauge">
                        <div class="gauge-fill warm" style="width: 62%"></div>
                    </div>
                    <p class="sentiment-desc">RSI 62 中性偏热，不宜追高</p>
                </div>
                
                <!-- VIX 恐慌指数 -->
                <div class="sentiment-card">
                    <div class="sentiment-header">
                        <span class="sentiment-icon">😨</span>
                        <h3>VIX 恐慌指数</h3>
                    </div>
                    <div class="sentiment-value low">18.5</div>
                    <p class="sentiment-desc">低于 20，市场情绪稳定，适合持仓</p>
                </div>
                
                <!-- Put/Call 比率 -->
                <div class="sentiment-card">
                    <div class="sentiment-header">
                        <span class="sentiment-icon">🛡️</span>
                        <h3>Put/Call 比率</h3>
                    </div>
                    <div class="sentiment-value neutral">0.82</div>
                    <p class="sentiment-desc">期权情绪中性，略偏乐观</p>
                </div>
                
                <!-- 美债收益率 -->
                <div class="sentiment-card">
                    <div class="sentiment-header">
                        <span class="sentiment-icon">📉</span>
                        <h3>10Y 美债收益率</h3>
                    </div>
                    <div class="sentiment-value">4.28%</div>
                    <p class="sentiment-desc">收益率平稳，经济预期温和</p>
                </div>
            </div>'''

if old_grid in content:
    content = content.replace(old_grid, new_grid)
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ 已更新市场情绪指标")
    print("   新增：标普 500 趋势、Put/Call 比率、美债收益率")
    print("   优化：市场温度添加 RSI 说明")
else:
    print("❌ 未找到旧的指标网格，可能已被修改")
