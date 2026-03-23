/**
 * 文章阅读计数
 * 
 * 功能:
 * 1. 统计每篇文章的阅读次数
 * 2. 显示热门文章
 * 3. 数据存储在 localStorage
 * 
 * 注意：这是简单的本地计数，非跨设备统计
 * 如需精确统计，需接入后端服务
 */

(function() {
    'use strict';
    
    const STORAGE_KEY = 'pulse_article_views';
    const VIEWS_DISPLAY_KEY = 'pulse_views_display';
    
    /**
     * 获取阅读计数数据
     */
    function getViewsData() {
        const data = localStorage.getItem(STORAGE_KEY);
        return data ? JSON.parse(data) : {};
    }
    
    /**
     * 保存阅读计数数据
     */
    function saveViewsData(data) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    }
    
    /**
     * 增加文章阅读计数
     */
    function incrementViews(path) {
        const data = getViewsData();
        const now = Date.now();
        
        if (!data[path]) {
            data[path] = {
                count: 0,
                firstView: now,
                lastView: now
            };
        }
        
        data[path].count += 1;
        data[path].lastView = now;
        
        saveViewsData(data);
        
        return data[path].count;
    }
    
    /**
     * 获取文章阅读计数
     */
    function getViews(path) {
        const data = getViewsData();
        return data[path] ? data[path].count : 0;
    }
    
    /**
     * 获取所有文章阅读排行
     */
    function getTopArticles(limit = 5) {
        const data = getViewsData();
        const articles = Object.entries(data).map(([path, info]) => ({
            path,
            count: info.count,
            firstView: info.firstView,
            lastView: info.lastView
        }));
        
        // 按阅读数排序
        articles.sort((a, b) => b.count - a.count);
        
        return articles.slice(0, limit);
    }
    
    /**
     * 显示阅读计数
     */
    function displayViews(elementId, count) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = count.toLocaleString();
        }
    }
    
    /**
     * 显示热门文章列表
     */
    function displayTopArticles(containerId, limit = 5) {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        const topArticles = getTopArticles(limit);
        
        if (topArticles.length === 0) {
            container.innerHTML = '<p>暂无阅读数据</p>';
            return;
        }
        
        let html = '<ul class="top-articles-list">';
        topArticles.forEach((article, index) => {
            const path = article.path;
            const title = extractTitle(path);
            const views = article.count.toLocaleString();
            
            html += `
                <li class="top-article-item">
                    <span class="rank">#${index + 1}</span>
                    <a href="${path}" class="article-link">${title}</a>
                    <span class="views-count">👁️ ${views}</span>
                </li>
            `;
        });
        html += '</ul>';
        
        container.innerHTML = html;
    }
    
    /**
     * 从路径提取文章标题
     */
    function extractTitle(path) {
        // 从路径提取标题，例如：
        // /content/daily-thoughts/2026-03-22-fear-and-opportunity.html
        // → "Fear And Opportunity"
        
        const filename = path.split('/').pop();
        if (!filename) return path;
        
        // 移除日期前缀和扩展名
        const title = filename
            .replace(/^\d{4}-\d{2}-\d{2}-/, '')
            .replace(/\.[^.]+$/, '')
            .replace(/-/g, ' ')
            .split(' ')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
        
        return title;
    }
    
    /**
     * 初始化当前页面阅读计数
     */
    function initCurrentPageViews() {
        const path = window.location.pathname;
        const count = incrementViews(path);
        
        // 显示计数
        displayViews('view-count', count);
        displayViews('article-views-count', count);
        
        // 保存到显示缓存 (用于首页显示)
        const displayData = JSON.parse(localStorage.getItem(VIEWS_DISPLAY_KEY) || '{}');
        displayData[path] = count;
        localStorage.setItem(VIEWS_DISPLAY_KEY, JSON.stringify(displayData));
    }
    
    /**
     * 更新首页文章卡片的阅读数显示
     */
    function updateHomepageViews() {
        const displayData = JSON.parse(localStorage.getItem(VIEWS_DISPLAY_KEY) || '{}');
        
        // 查找所有文章卡片
        const cards = document.querySelectorAll('.thought-card, .article-card');
        cards.forEach(card => {
            const link = card.querySelector('a[href*="content/daily-thoughts"]');
            if (!link) return;
            
            const path = link.getAttribute('href');
            const views = displayData[path] || getViews(path);
            
            // 创建或更新阅读数显示
            let viewsElement = card.querySelector('.card-views');
            if (!viewsElement) {
                viewsElement = document.createElement('div');
                viewsElement.className = 'card-views';
                card.appendChild(viewsElement);
            }
            
            viewsElement.textContent = `👁️ ${views.toLocaleString()}`;
        });
    }
    
    /**
     * 页面加载完成后初始化
     */
    function init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                initCurrentPageViews();
                updateHomepageViews();
            });
        } else {
            initCurrentPageViews();
            updateHomepageViews();
        }
    }
    
    // 启动
    init();
    
    // 导出到全局
    window.PulseViews = {
        getViews,
        getTopArticles,
        displayTopArticles,
        incrementViews
    };
    
})();
