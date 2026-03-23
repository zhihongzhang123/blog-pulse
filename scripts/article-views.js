/**
 * 文章阅读计数 v3.0 (修复版)
 * 
 * 修复内容:
 * 1. 修复首页卡片选择器 (.card 通用选择器)
 * 2. 优化路径归一化 (处理相对路径)
 * 3. 改进冷却时间逻辑
 * 4. 添加调试日志
 */

(function() {
    'use strict';
    
    const STORAGE_KEY = 'pulse_article_views';
    const COOLDOWN_KEY = 'pulse_view_cooldown';
    const COOLDOWN_MS = 30 * 60 * 1000; // 30 分钟冷却时间
    
    /**
     * 路径归一化 (解决路径不一致问题)
     */
    function normalizePath(path) {
        if (!path) return '';
        
        // 移除域名部分 (如果有)
        path = path.replace(/^https?:\/\/[^\/]+/, '');
        
        // 确保以 / 开头
        if (!path.startsWith('/')) {
            path = '/' + path;
        }
        
        // 移除查询参数和哈希
        path = path.split('?')[0].split('#')[0];
        
        // 解析相对路径 (处理 content/daily-thoughts/xxx.html)
        if (path.startsWith('/content/')) {
            // 已经是绝对路径
            return path;
        }
        
        return path;
    }
    
    /**
     * 获取当前标准化路径
     */
    function getCurrentPath() {
        return normalizePath(window.location.pathname);
    }
    
    /**
     * 获取阅读计数数据
     */
    function getViewsData() {
        try {
            const data = localStorage.getItem(STORAGE_KEY);
            return data ? JSON.parse(data) : {};
        } catch (e) {
            console.warn('读取阅读数据失败:', e);
            return {};
        }
    }
    
    /**
     * 保存阅读计数数据
     */
    function saveViewsData(data) {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
        } catch (e) {
            console.warn('保存阅读数据失败:', e);
        }
    }
    
    /**
     * 检查是否在冷却时间内
     */
    function isInCooldown(path) {
        const cooldownData = JSON.parse(localStorage.getItem(COOLDOWN_KEY) || '{}');
        const lastView = cooldownData[path];
        
        if (!lastView) return false;
        
        const now = Date.now();
        return (now - lastView) < COOLDOWN_MS;
    }
    
    /**
     * 设置冷却时间
     */
    function setCooldown(path) {
        const cooldownData = JSON.parse(localStorage.getItem(COOLDOWN_KEY) || '{}');
        cooldownData[path] = Date.now();
        localStorage.setItem(COOLDOWN_KEY, JSON.stringify(cooldownData));
    }
    
    /**
     * 从路径提取文章标题
     */
    function extractTitle(path) {
        const filename = path.split('/').pop();
        if (!filename) return '未知文章';
        
        // 移除日期前缀和扩展名
        const title = filename
            .replace(/^\d{4}-\d{2}-\d{2}-/, '')
            .replace(/\.[^.]+$/, '')
            .replace(/-/g, ' ')
            .replace(/_/g, ' ')
            .trim();
        
        return title;
    }
    
    /**
     * 增加文章阅读计数
     */
    function incrementViews(path) {
        const normalizedPath = normalizePath(path);
        
        // 检查冷却时间
        if (isInCooldown(normalizedPath)) {
            console.log('⏱️ 冷却时间内，不增加计数');
            return getViews(normalizedPath);
        }
        
        const data = getViewsData();
        const now = Date.now();
        
        if (!data[normalizedPath]) {
            data[normalizedPath] = {
                count: 0,
                firstView: now,
                lastView: now,
                title: extractTitle(normalizedPath)
            };
        }
        
        data[normalizedPath].count += 1;
        data[normalizedPath].lastView = now;
        
        saveViewsData(data);
        setCooldown(normalizedPath);
        
        console.log(`📊 ${normalizedPath} 阅读数 +1 = ${data[normalizedPath].count}`);
        
        return data[normalizedPath].count;
    }
    
    /**
     * 获取文章阅读计数
     */
    function getViews(path) {
        const normalizedPath = normalizePath(path);
        const data = getViewsData();
        return data[normalizedPath] ? data[normalizedPath].count : 0;
    }
    
    /**
     * 初始化当前页面阅读计数
     */
    function initCurrentPageViews() {
        const path = getCurrentPath();
        
        // 只在文章页面计数 (排除首页、列表页等)
        const isArticlePage = path.includes('/content/daily-thoughts/') && 
                              path.endsWith('.html');
        
        if (!isArticlePage) {
            console.log('📄 非文章页面，不计数');
            return;
        }
        
        const count = incrementViews(path);
        console.log(`📖 文章页面阅读计数：${count}`);
        
        // 显示计数
        displayViews('view-count', count);
        displayViews('article-views-count', count);
        displayViews('article-views', `👁️ ${count}`);
    }
    
    /**
     * 更新首页文章卡片的阅读数显示
     */
    function updateHomepageViews() {
        const data = getViewsData();
        console.log('🏠 更新首页阅读计数，当前数据:', data);
        
        // 查找所有文章卡片 (使用通用 .card 选择器)
        const cards = document.querySelectorAll('.card');
        console.log(`📇 找到 ${cards.length} 个卡片`);
        
        cards.forEach((card, index) => {
            const link = card.querySelector('a[href*="content/daily-thoughts"]');
            if (!link) {
                console.log(`⏭️ 卡片 ${index}: 无文章链接`);
                return;
            }
            
            // 获取链接路径并归一化
            const href = link.getAttribute('href');
            const path = normalizePath(href);
            console.log(`📇 卡片 ${index}: ${href} → ${path}`);
            
            // 获取阅读数
            const articleData = data[path];
            const views = articleData ? articleData.count : 0;
            
            // 创建或更新阅读数显示
            let viewsElement = card.querySelector('.card-views');
            if (!viewsElement) {
                viewsElement = document.createElement('div');
                viewsElement.className = 'card-views';
                
                // 插入到 read-more 链接之前
                const readMore = card.querySelector('.read-more');
                if (readMore) {
                    readMore.parentNode.insertBefore(viewsElement, readMore);
                } else {
                    card.appendChild(viewsElement);
                }
            }
            
            viewsElement.textContent = `👁️ ${views}`;
            console.log(`✅ 卡片 ${index}: 更新为 ${views} 次阅读`);
        });
        
        console.log(`🏠 更新了 ${cards.length} 个文章卡片的阅读数`);
    }
    
    /**
     * 显示阅读计数
     */
    function displayViews(elementId, count) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = typeof count === 'string' ? count : (count ? count.toLocaleString() : '0');
        }
    }
    
    /**
     * 页面加载完成后初始化
     */
    function init() {
        console.log('🚀 阅读计数器初始化...');
        
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                initCurrentPageViews();
                updateHomepageViews();
            });
        } else {
            // DOM 已加载完成
            initCurrentPageViews();
            updateHomepageViews();
        }
    }
    
    // 启动
    init();
    
    // 导出到全局
    window.PulseViews = {
        getViews,
        getViewsData,
        incrementViews,
        normalizePath,
        getCurrentPath
    };
    
})();
