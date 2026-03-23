/**
 * 懒加载非首屏内容
 * 使用 Intersection Observer API
 */

(function() {
    // 配置选项
    const options = {
        root: null,
        rootMargin: '50px',
        threshold: 0.01
    };
    
    // 创建观察者
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                
                // 加载图片
                if (target.tagName === 'IMG' && target.dataset.src) {
                    target.src = target.dataset.src;
                    target.removeAttribute('data-src');
                    target.classList.add('loaded');
                }
                
                // 加载 iframe
                if (target.tagName === 'IFRAME' && target.dataset.src) {
                    target.src = target.dataset.src;
                    target.removeAttribute('data-src');
                }
                
                // 加载 section 内容
                if (target.classList.contains('lazy-section')) {
                    target.classList.add('loaded');
                }
                
                // 停止观察
                observer.unobserve(target);
                console.log('✅ 懒加载内容已加载:', target);
            }
        });
    }, options);
    
    // 观察所有懒加载元素
    function initLazyLoad() {
        // 图片
        document.querySelectorAll('img[data-src]').forEach(img => {
            observer.observe(img);
        });
        
        // iframe
        document.querySelectorAll('iframe[data-src]').forEach(iframe => {
            observer.observe(iframe);
        });
        
        // 非首屏 section (市场情绪之后的内容)
        const sections = document.querySelectorAll('section:not(#market-sentiment):not(#daily-thoughts)');
        sections.forEach(section => {
            section.classList.add('lazy-section');
            observer.observe(section);
        });
        
        console.log('👀 懒加载初始化完成，观察', 
            document.querySelectorAll('img[data-src]').length + 
            document.querySelectorAll('iframe[data-src]').length + 
            sections.length, '个元素');
    }
    
    // 页面加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initLazyLoad);
    } else {
        initLazyLoad();
    }
    
    // 导出到全局
    window.LazyLoad = {
        init: initLazyLoad,
        observer: observer
    };
    
})();
