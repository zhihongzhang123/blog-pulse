#!/usr/bin/env python3
"""
更新博客首页市场情绪模块
将 Crypto 实盘交易替换为市场情绪展示
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.join(BASE_DIR, 'index.html')

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换导航链接
content = content.replace(
    '<a href="#live-trading">实盘系统</a>',
    '<a href="#market-sentiment">市场情绪</a>'
)

# 替换整个 section
old_section = '''        <!-- 实盘系统 -->
        <section id="live-trading" class="section">
            <h2 class="section-title">
                <span class="title-icon">⚡</span>
                Crypto 实盘交易
            </h2>
            
            <!-- iOS 风格小组件网格 -->
            <div class="widgets-grid">
                <!-- 持仓概览小组件 -->
                <div class="widget widget-large">
                    <div class="widget-header">
                        <span class="widget-icon">📊</span>
                        <span class="widget-title">持仓概览</span>
                    </div>
                    <div class="widget-content">
                        <div class="widget-metric">
                            <span class="widget-metric-label">总仓位</span>
                            <span class="widget-metric-value">65%</span>
                        </div>
                        <div class="widget-metric">
                            <span class="widget-metric-label">今日盈亏</span>
                            <span class="widget-metric-value positive">+2.3%</span>
                        </div>
                        <div class="widget-metric">
                            <span class="widget-metric-label">本月盈亏</span>
                            <span class="widget-metric-value positive">+8.7%</span>
                        </div>
                    </div>
                    <div class="widget-footer">
                        <span class="widget-update-time">更新于 1 分钟前</span>
                    </div>
                </div>
                
                <!-- 风险指标小组件 -->
                <div class="widget widget-large">
                    <div class="widget-header">
                        <span class="widget-icon">🛡️</span>
                        <span class="widget-title">风险指标</span>
                    </div>
                    <div class="widget-content">
                        <div class="widget-metric">
                            <span class="widget-metric-label">VIX</span>
                            <span class="widget-metric-value">18.5</span>
                        </div>
                        <div class="widget-metric">
                            <span class="widget-metric-label">Put/Call</span>
                            <span class="widget-metric-value">0.82</span>
                        </div>
                        <div class="widget-metric">
                            <span class="widget-metric-label">情绪</span>
                            <span class="widget-metric-value">55/100</span>
                        </div>
                    </div>
                    <div class="widget-footer">
                        <span class="widget-update-time">更新于 1 分钟前</span>
                    </div>
                </div>
                
                <!-- 市场状态小组件 -->
                <div class="widget widget-small">
                    <div class="widget-header">
                        <span class="widget-icon">📈</span>
                        <span class="widget-title">技术指标</span>
                    </div>
                    <div class="widget-content-center">
                        <div class="temperature-gauge">
                            <div class="gauge-fill" style="width: 62%"></div>
                        </div>
                        <span class="temperature-text">RSI 62 中性</span>
                    </div>
                </div>
                
                <!-- 推送状态小组件 -->
                <div class="widget widget-small">
                    <div class="widget-header">
                        <span class="widget-icon">📬</span>
                        <span class="widget-title">今日推送</span>
                    </div>
                    <div class="widget-content-center">
                        <div class="push-status">
                            <span class="status-dot success"></span>
                            <span class="status-text">早报已推送</span>
                        </div>
                        <div class="push-status">
                            <span class="status-dot pending"></span>
                            <span class="status-text">晚报待推送</span>
                        </div>
                    </div>
                </div>
            </div>
            
        </section>'''

new_section = '''        <!-- 市场情绪 -->
        <section id="market-sentiment" class="section">
            <h2 class="section-title">
                <span class="title-icon">🌡️</span>
                市场情绪
            </h2>
            
            <div class="sentiment-grid">
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
            </div>
            
            <!-- 市场热点 -->
            <div class="hotspots-section">
                <h3 class="subsection-title">🔥 市场热点</h3>
                <div class="hotspots-grid">
                    <div class="hotspot-tag hot">AI 人工智能</div>
                    <div class="hotspot-tag hot">半导体</div>
                    <div class="hotspot-tag warm">新能源</div>
                    <div class="hotspot-tag warm">生物科技</div>
                    <div class="hotspot-tag normal">金融科技</div>
                    <div class="hotspot-tag normal">消费电子</div>
                </div>
            </div>
            
            <!-- 重点板块 -->
            <div class="sectors-section">
                <h3 class="subsection-title">📈 重点板块</h3>
                <div class="sectors-list">
                    <div class="sector-item">
                        <span class="sector-name">科技 (XLK)</span>
                        <span class="sector-change positive">+2.3%</span>
                        <span class="sector-trend">领涨</span>
                    </div>
                    <div class="sector-item">
                        <span class="sector-name">能源 (XLE)</span>
                        <span class="sector-change positive">+1.8%</span>
                        <span class="sector-trend">强势</span>
                    </div>
                    <div class="sector-item">
                        <span class="sector-name">金融 (XLF)</span>
                        <span class="sector-change neutral">+0.5%</span>
                        <span class="sector-trend">震荡</span>
                    </div>
                    <div class="sector-item">
                        <span class="sector-name">医疗 (XLV)</span>
                        <span class="sector-change negative">-0.8%</span>
                        <span class="sector-trend">回调</span>
                    </div>
                </div>
            </div>
            
            <!-- 市场策略 -->
            <div class="strategy-section">
                <h3 class="subsection-title">💡 市场策略</h3>
                <div class="strategy-content">
                    <p><strong>当前建议：</strong>保持中性偏多仓位，重点关注科技和能源板块，警惕医疗板块回调风险。</p>
                    <p><strong>仓位建议：</strong>60-70%，不宜满仓操作</p>
                    <p><strong>风险提示：</strong>关注美联储政策动向和地缘政治风险</p>
                </div>
            </div>
            
            <p class="section-note">⚠️ 以上数据仅供参考，不构成投资建议。市场有风险，投资需谨慎。</p>
        </section>'''

if old_section in content:
    content = content.replace(old_section, new_section)
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ 已更新市场情绪模块")
else:
    print("❌ 未找到旧模块，可能已被修改")
