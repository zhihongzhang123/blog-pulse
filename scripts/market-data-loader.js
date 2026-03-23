/**
 * 市场情绪数据加载器
 * 从 JSON 文件加载数据并更新页面显示
 */

(function() {
    const DATA_FILE = 'data/market-sentiment.json';
    
    /**
     * 格式化相对时间 (更新于 X 分钟前)
     */
    function formatRelativeTime(isoString) {
        if (!isoString) return '更新于 --';
        
        const updateTime = new Date(isoString);
        const now = new Date();
        const diffMs = now - updateTime;
        const diffMins = Math.floor(diffMs / 60000); // 转换为分钟
        
        if (diffMins < 1) {
            return '刚刚更新';
        } else if (diffMins < 60) {
            return `更新于${diffMins}分钟前`;
        } else if (diffMins < 1440) { // 24 小时内
            const hours = Math.floor(diffMins / 60);
            return `更新于${hours}小时前`;
        } else {
            const days = Math.floor(diffMins / 1440);
            return `更新于${days}天前`;
        }
    }
    
    /**
     * 更新页面显示
     */
    function updateDisplay(data) {
        // 指标映射
        const metricMap = {
            'sp500': data.sp500,
            'width': data.market_width,
            'rsi': data.rsi,
            'vix': data.vix,
            'pcr': data.put_call,
            'treasury': data.treasury_10y
        };
        
        // 更新每个指标的更新时间
        Object.keys(metricMap).forEach(key => {
            const element = document.querySelector(`[data-metric="${key}"]`);
            if (element && metricMap[key]) {
                const updateTime = metricMap[key].updated || data.updated_at;
                element.textContent = formatRelativeTime(updateTime);
                element.title = `最后更新：${updateTime}`;
            }
        });
        
        console.log('✅ 市场数据已加载', data);
    }
    
    /**
     * 加载市场数据
     */
    async function loadMarketData() {
        try {
            // 添加时间戳避免缓存
            const timestamp = new Date().getTime();
            const response = await fetch(`${DATA_FILE}?t=${timestamp}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            updateDisplay(data);
            
        } catch (error) {
            console.warn('⚠️ 加载市场数据失败:', error.message);
            // 显示默认文本
            document.querySelectorAll('.update-time').forEach(el => {
                el.textContent = '更新于 --';
            });
        }
    }
    
    /**
     * 页面加载完成后执行
     */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadMarketData);
    } else {
        loadMarketData();
    }
    
    // 每 5 分钟自动刷新一次显示
    setInterval(loadMarketData, 5 * 60 * 1000);
    
    // 导出到全局
    window.MarketDataLoader = {
        load: loadMarketData,
        formatRelativeTime: formatRelativeTime
    };
    
})();
