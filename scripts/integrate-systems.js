// ========================================
// Pulse Blog · 系统集成脚本
// 自动加载最新数据并更新页面
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ========================================
    // 1. 加载新闻简报数据
    // ========================================
    loadLatestBriefing();
    
    // ========================================
    // 2. 加载美股分析数据
    // ========================================
    loadMarketAnalysis();
    
    // ========================================
    // 3. 加载交易仪表盘数据
    // ========================================
    loadTradingDashboard();
    
    // ========================================
    // 4. 定时刷新（每 5 分钟）
    // ========================================
    setInterval(() => {
        loadTradingDashboard(); // 只刷新交易数据
    }, 5 * 60 * 1000);
});

/**
 * 加载最新新闻简报
 */
async function loadLatestBriefing() {
    try {
        const response = await fetch('data/news/latest.json');
        if (!response.ok) throw new Error('简报数据不存在');
        
        const briefing = await response.json();
        
        // 更新首页简报卡片
        updateBriefingCard(briefing);
        
        console.log('✅ 新闻简报已加载');
    } catch (error) {
        console.log('⚠️ 新闻简报数据暂缺:', error.message);
        // 显示默认状态
        updateBriefingCard(null);
    }
}

/**
 * 更新简报卡片 UI
 */
function updateBriefingCard(briefing) {
    const briefingCards = document.querySelectorAll('.briefing-card');
    if (!briefingCards.length) return;
    
    // 早报卡片
    const morningCard = briefingCards[0];
    // 晚报卡片
    const eveningCard = briefingCards[1];
    
    if (briefing) {
        const timestamp = new Date(briefing.timestamp);
        const hour = timestamp.getHours();
        const isMorning = hour >= 5 && hour < 12;
        
        // 更新对应卡片
        const targetCard = isMorning ? morningCard : eveningCard;
        const statusEl = targetCard.querySelector('.briefing-status');
        const linkEl = targetCard.querySelector('.briefing-link');
        
        if (statusEl) {
            statusEl.textContent = '✅ 已推送';
            statusEl.classList.add('status-success');
        }
        
        if (linkEl) {
            linkEl.textContent = '查看简报';
            linkEl.href = 'data/news/latest.html';
            linkEl.classList.remove('disabled');
        }
    } else {
        // 无数据时显示默认状态
        if (morningCard) {
            const statusEl = morningCard.querySelector('.briefing-status');
            if (statusEl) {
                statusEl.textContent = '⏳ 待推送';
                statusEl.className = 'briefing-status status-pending';
            }
        }
    }
}

/**
 * 加载美股市场分析
 */
async function loadMarketAnalysis() {
    try {
        const response = await fetch('data/market/latest.json');
        if (!response.ok) throw new Error('分析数据不存在');
        
        const analysis = await response.json();
        
        // 更新分析卡片
        updateAnalysisCard(analysis);
        
        console.log('✅ 美股分析已加载');
    } catch (error) {
        console.log('⚠️ 美股分析数据暂缺:', error.message);
        updateAnalysisCard(null);
    }
}

/**
 * 更新分析卡片 UI
 */
function updateAnalysisCard(analysis) {
    const analysisCards = document.querySelectorAll('.analysis-card');
    if (!analysisCards.length) return;
    
    if (analysis) {
        const type = analysis.type; // 'pre-market' or 'post-market'
        const targetId = type === 'pre-market' ? 'pre-market' : 'post-market';
        const targetCard = document.getElementById(targetId);
        
        if (targetCard) {
            const statusEl = targetCard.querySelector('.analysis-status');
            const previewEl = targetCard.querySelector('.analysis-preview');
            const linkEl = targetCard.querySelector('.read-more');
            
            if (statusEl) {
                statusEl.textContent = '✅ 已更新';
                statusEl.className = 'analysis-status status-ready';
            }
            
            if (previewEl && analysis.summary) {
                previewEl.textContent = analysis.summary.substring(0, 100) + '...';
            }
            
            if (linkEl) {
                linkEl.href = `data/market/${type}.html`;
                linkEl.textContent = '查看完整分析 →';
            }
        }
    }
}

/**
 * 加载交易仪表盘数据
 */
async function loadTradingDashboard() {
    try {
        const response = await fetch('data/trading/dashboard.json');
        if (!response.ok) throw new Error('交易数据不存在');
        
        const data = await response.json();
        
        // 更新持仓概览
        updateMetric('总仓位', data.positions.total + '%');
        updateMetric('今日盈亏', formatPnL(data.positions.today_pnl));
        updateMetric('本月盈亏', formatPnL(data.positions.month_pnl));
        
        // 更新风险指标
        updateMetric('VIX', data.risk.vix);
        updateMetric('Put/Call', data.risk.put_call);
        updateMetric('情绪评分', data.risk.sentiment + '/100');
        
        // 更新时间戳
        updateUpdateTime(data.timestamp);
        
        console.log('✅ 交易数据已加载');
    } catch (error) {
        console.log('⚠️ 交易数据暂缺:', error.message);
        // 使用默认数据
        useDefaultTradingData();
    }
}

/**
 * 更新指标值
 */
function updateMetric(label, value) {
    const metrics = document.querySelectorAll('.metric');
    metrics.forEach(metric => {
        const labelEl = metric.querySelector('.metric-label');
        const valueEl = metric.querySelector('.metric-value');
        
        if (labelEl && labelEl.textContent === label) {
            // 添加动画
            valueEl.style.transform = 'scale(1.1)';
            setTimeout(() => {
                valueEl.textContent = value;
                valueEl.style.transform = 'scale(1)';
                
                // 更新正负样式
                if (typeof value === 'string' && value.includes('+')) {
                    valueEl.className = 'metric-value positive';
                } else if (typeof value === 'string' && value.includes('-')) {
                    valueEl.className = 'metric-value negative';
                } else {
                    valueEl.className = 'metric-value';
                }
            }, 150);
        }
    });
}

/**
 * 格式化盈亏
 */
function formatPnL(value) {
    const sign = value >= 0 ? '+' : '';
    return `${sign}${value.toFixed(2)}%`;
}

/**
 * 更新更新时间
 */
function updateUpdateTime(timestamp) {
    const updateEls = document.querySelectorAll('.widget-update-time');
    const timeStr = formatRelativeTime(timestamp);
    
    updateEls.forEach(el => {
        el.textContent = `更新于 ${timeStr}`;
    });
}

/**
 * 格式化相对时间
 */
function formatRelativeTime(isoString) {
    const date = new Date(isoString);
    const now = new Date();
    const diff = now - date;
    const minutes = Math.floor(diff / 60000);
    
    if (minutes < 1) return '刚刚';
    if (minutes < 60) return `${minutes}分钟前`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}小时前`;
    return `${hours}小时前`;
}

/**
 * 使用默认交易数据（当数据暂缺时）
 */
function useDefaultTradingData() {
    const defaultData = {
        positions: {
            total: 65,
            today_pnl: 0,
            month_pnl: 0
        },
        risk: {
            vix: 18.5,
            put_call: 0.82,
            sentiment: 55
        }
    };
    
    updateMetric('总仓位', defaultData.positions.total + '%');
    updateMetric('今日盈亏', formatPnL(defaultData.positions.today_pnl));
    updateMetric('本月盈亏', formatPnL(defaultData.positions.month_pnl));
    updateMetric('VIX', defaultData.risk.vix);
    updateMetric('Put/Call', defaultData.risk.put_call);
    updateMetric('情绪评分', defaultData.risk.sentiment + '/100');
}
