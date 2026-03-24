/**
 * Pulse Blog · 主题同步增强
 * 
 * 功能:
 * 1. 页面加载时同步主题
 * 2. 监听 storage 事件 (多标签页同步)
 * 3. 动态岛通知
 */

(function() {
    'use strict';
    
    // 主题配置
    const THEME_KEY = 'pulse-theme-mode';
    const DEFAULT_MODE = 'dark';
    
    /**
     * 应用主题模式
     */
    function applyMode(mode) {
        const body = document.body;
        if (!body) return;
        
        // 移除所有模式类
        body.classList.remove('dark-mode', 'light-mode');
        
        if (mode === 'auto') {
            // 跟随系统
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            body.classList.add(prefersDark ? 'dark-mode' : 'light-mode');
        } else {
            body.classList.add(mode === 'dark' ? 'dark-mode' : 'light-mode');
        }
        
        // 同步按钮状态
        syncButtons(mode);
    }
    
    /**
     * 同步按钮状态
     */
    function syncButtons(mode) {
        const buttons = document.querySelectorAll('.switch-btn');
        buttons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.mode === mode);
        });
    }
    
    /**
     * 初始化主题
     */
    function initTheme() {
        const savedMode = localStorage.getItem(THEME_KEY) || DEFAULT_MODE;
        applyMode(savedMode);
        console.log('💓 Pulse Blog 主题已加载:', savedMode);
    }
    
    /**
     * 监听 storage 事件 (多标签页同步)
     */
    function setupStorageListener() {
        window.addEventListener('storage', function(e) {
            if (e.key === THEME_KEY && e.newValue) {
                applyMode(e.newValue);
                showNotification(`主题已同步`, e.newValue === 'dark' ? '🌙' : '☀️');
            }
        });
    }
    
    /**
     * 显示通知 (简化版动态岛)
     */
    function showNotification(text, icon = '💓') {
        // 检查是否有动态岛元素
        const island = document.getElementById('dynamic-island');
        if (island) {
            const content = island.querySelector('.island-content');
            if (content) {
                content.innerHTML = `<span class="island-icon">${icon}</span><span class="island-text">${text}</span>`;
                island.classList.add('visible', 'expanded');
                
                setTimeout(() => {
                    island.classList.remove('expanded');
                    setTimeout(() => {
                        island.classList.remove('visible');
                    }, 400);
                }, 2000);
            }
        } else {
            // 降级：使用 console
            console.log(`${icon} ${text}`);
        }
    }
    
    /**
     * 绑定模式切换按钮
     */
    function bindSwitchButtons() {
        const buttons = document.querySelectorAll('.switch-btn');
        buttons.forEach(btn => {
            btn.addEventListener('click', function() {
                const mode = this.dataset.mode;
                
                // 保存偏好
                localStorage.setItem(THEME_KEY, mode);
                
                // 应用主题
                applyMode(mode);
                
                // 触觉反馈
                this.classList.add('haptic-press');
                setTimeout(() => this.classList.remove('haptic-press'), 150);
                
                // 通知
                const modeNames = {
                    dark: '深色模式',
                    light: '浅色模式',
                    auto: '跟随系统'
                };
                const icon = this.querySelector('.switch-icon');
                showNotification(`已切换到${modeNames[mode]}`, icon ? icon.textContent : '💓');
                
                // 触发 storage 事件 (同标签页内同步)
                window.dispatchEvent(new Event('storage'));
            });
        });
    }
    
    /**
     * 监听系统主题变化
     */
    function setupSystemThemeListener() {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        
        const handler = (e) => {
            const currentMode = localStorage.getItem(THEME_KEY);
            if (currentMode === 'auto') {
                applyMode('auto');
                showNotification(`系统主题已切换`, e.matches ? '🌙' : '☀️');
            }
        };
        
        // 现代浏览器
        if (mediaQuery.addEventListener) {
            mediaQuery.addEventListener('change', handler);
        } else if (mediaQuery.addListener) {
            // 旧版浏览器兼容
            mediaQuery.addListener(handler);
        }
    }
    
    /**
     * 初始化
     */
    function init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                initTheme();
                bindSwitchButtons();
                setupStorageListener();
                setupSystemThemeListener();
            });
        } else {
            initTheme();
            bindSwitchButtons();
            setupStorageListener();
            setupSystemThemeListener();
        }
    }
    
    // 启动
    init();
    
    // 导出到全局 (供调试使用)
    window.PulseTheme = {
        applyMode,
        syncButtons,
        showNotification,
        getTheme: () => localStorage.getItem(THEME_KEY) || DEFAULT_MODE
    };
    
})();
