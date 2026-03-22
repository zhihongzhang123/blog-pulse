// ========================================
// Pulse Blog · 交互脚本
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    
    // 标签页切换
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetTab = this.dataset.tab;
            
            // 移除所有 active
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // 添加 active 到当前
            this.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
    
    // 平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // 卡片悬停效果增强
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // 动态更新时间
    function updateTime() {
        const timeElements = document.querySelectorAll('.analysis-time');
        timeElements.forEach(el => {
            // 可以在这里添加动态更新时间逻辑
        });
    }
    
    updateTime();
    
    // 检查推送状态（可选：集成 API）
    function checkPushStatus() {
        // 未来可以集成后端 API 检查推送状态
        console.log('Push status check initialized');
    }
    
    checkPushStatus();
    
    // 键盘导航支持
    document.addEventListener('keydown', function(e) {
        // ESC 关闭任何打开的模态框（未来扩展）
        if (e.key === 'Escape') {
            // 预留功能
        }
    });
    
    // 初始化完成
    console.log('💓 Pulse Blog initialized');
});

// ========================================
// 工具函数
// ========================================

/**
 * 格式化日期
 */
function formatDate(date) {
    const options = { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' };
    return date.toLocaleDateString('zh-CN', options);
}

/**
 * 格式化时间
 */
function formatTime(date) {
    return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
}

/**
 * 计算相对时间
 */
function relativeTime(date) {
    const now = new Date();
    const diff = now - date;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);
    
    if (minutes < 1) return '刚刚';
    if (minutes < 60) return `${minutes}分钟前`;
    if (hours < 24) return `${hours}小时前`;
    if (days < 7) return `${days}天前`;
    return formatDate(date);
}

/**
 * 数字格式化（带千分位）
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * 百分比格式化
 */
function formatPercent(num) {
    const sign = num >= 0 ? '+' : '';
    return `${sign}${num.toFixed(2)}%`;
}
