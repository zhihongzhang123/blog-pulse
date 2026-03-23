// ========================================
// Pulse Blog · 交互脚本 (Apple 风格增强)
// ========================================

// 先加载主题同步增强脚本
(function() {
    const script = document.createElement('script');
    script.src = 'scripts/theme-sync.js';
    script.async = true;
    document.head.appendChild(script);
})();

document.addEventListener('DOMContentLoaded', function() {
    
    // 动态岛通知
    const dynamicIsland = document.getElementById('dynamic-island');
    
    function showIslandNotification(text, icon = '💓', duration = 3000) {
        const islandContent = dynamicIsland.querySelector('.island-content');
        islandContent.innerHTML = `
            <span class="island-icon">${icon}</span>
            <span class="island-text">${text}</span>
        `;
        
        dynamicIsland.classList.add('visible');
        dynamicIsland.classList.add('expanded');
        
        setTimeout(() => {
            dynamicIsland.classList.remove('expanded');
            setTimeout(() => {
                dynamicIsland.classList.remove('visible');
            }, 400);
        }, duration);
    }
    
    // 显示欢迎通知
    setTimeout(() => {
        showIslandNotification('Pulse 已就绪', '💓', 2500);
    }, 1000);
    
    // 模式切换器
    const switchBtns = document.querySelectorAll('.switch-btn');
    const body = document.body;
    
    // 读取保存的模式（默认跟随系统）
    const savedMode = localStorage.getItem('pulse-theme-mode') || 'auto';
    applyMode(savedMode);
    
    // 页面加载时同步主题到所有模式切换按钮
    function syncThemeButtons() {
        const currentMode = localStorage.getItem('pulse-theme-mode') || 'light';
        switchBtns.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.mode === currentMode);
        });
    }
    
    // 更新按钮状态
    switchBtns.forEach(btn => {
        if (btn.dataset.mode === savedMode) {
            btn.classList.add('active');
        }
        
        btn.addEventListener('click', function() {
            const mode = this.dataset.mode;
            applyMode(mode);
            
            // 保存偏好
            localStorage.setItem('pulse-theme-mode', mode);
            
            // 同步所有页面的按钮状态
            syncThemeButtons();
            
            // 触觉反馈动画
            this.classList.add('haptic-press');
            setTimeout(() => this.classList.remove('haptic-press'), 150);
            
            // 动态岛通知
            const modeNames = { dark: '深色模式', light: '浅色模式', auto: '跟随系统' };
            showIslandNotification(`已切换到${modeNames[mode]}`, this.querySelector('.switch-icon').textContent, 2000);
        });
    });
    
    function applyMode(mode) {
        // 移除所有模式类
        body.classList.remove('dark-mode', 'light-mode');
        
        if (mode === 'auto') {
            // 跟随系统
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            body.classList.add(prefersDark ? 'dark-mode' : 'light-mode');
        } else {
            body.classList.add(mode === 'dark' ? 'dark-mode' : 'light-mode');
        }
        
        // 更新按钮状态
        switchBtns.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.mode === mode);
        });
    }
    
    // 监听系统主题变化
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        const currentMode = localStorage.getItem('pulse-theme-mode');
        if (currentMode === 'auto') {
            applyMode('auto');
            showIslandNotification('跟随系统主题', e.matches ? '🌙' : '☀️', 2000);
        }
    });
    
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
            
            // 触觉反馈
            this.classList.add('haptic-press');
            setTimeout(() => this.classList.remove('haptic-press'), 150);
        });
    });
    
    // 平滑滚动 + 触觉反馈
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // 触觉反馈
                this.classList.add('haptic-press');
                setTimeout(() => this.classList.remove('haptic-press'), 150);
            }
        });
    });
    
    // 卡片悬停效果增强 + 微光扫过
    const cards = document.querySelectorAll('.card, .widget');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-6px) scale(1.02)';
            
            // 添加微光效果
            const shimmer = document.createElement('div');
            shimmer.className = 'shimmer';
            shimmer.style.position = 'absolute';
            shimmer.style.top = '0';
            shimmer.style.left = '0';
            shimmer.style.right = '0';
            shimmer.style.bottom = '0';
            shimmer.style.borderRadius = 'inherit';
            shimmer.style.pointerEvents = 'none';
            this.appendChild(shimmer);
            
            setTimeout(() => shimmer.remove(), 2000);
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // 鼠标移动视差效果 (桌面端)
    if (window.matchMedia('(hover: hover)').matches) {
        document.addEventListener('mousemove', (e) => {
            const mouseX = e.clientX / window.innerWidth - 0.5;
            const mouseY = e.clientY / window.innerHeight - 0.5;
            
            // 背景光晕轻微跟随鼠标
            const ambient = document.querySelector('.ambient-light');
            if (ambient) {
                ambient.style.transform = `translate(${mouseX * 20}px, ${mouseY * 20}px)`;
            }
        });
    }
    
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

// 加载阅读计数
(function() {
    const script = document.createElement('script');
    script.src = 'scripts/article-views.js';
    script.async = true;
    document.head.appendChild(script);
})();
