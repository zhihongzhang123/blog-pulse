/**
 * 导航栏滚动高亮
 * 根据当前滚动位置自动更新导航 active 状态
 */

(function() {
    const navLinks = document.querySelectorAll('.nav a[href^="#"]');
    const sections = document.querySelectorAll('section[id]');
    
    if (navLinks.length === 0 || sections.length === 0) {
        console.log('⚠️ 导航或 section 未找到');
        return;
    }
    
    /**
     * 更新导航 active 状态
     */
    function updateActiveNav() {
        const scrollY = window.scrollY;
        const windowHeight = window.innerHeight;
        const viewportCenter = scrollY + (windowHeight / 2);
        
        let currentSection = '';
        let minDistance = Infinity;
        
        // 找到距离视口中心最近的 section
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionBottom = sectionTop + section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            // 计算 section 中心点与视口中心点的距离
            const sectionCenter = sectionTop + (section.offsetHeight / 2);
            const distance = Math.abs(viewportCenter - sectionCenter);
            
            // 只有当 section 在视口内或接近视口时才考虑
            if (scrollY < sectionBottom && scrollY + windowHeight > sectionTop) {
                if (distance < minDistance) {
                    minDistance = distance;
                    currentSection = sectionId;
                }
            }
        });
        
        // 移除所有 active
        navLinks.forEach(link => {
            link.classList.remove('active');
        });
        
        // 添加当前 section 的 active
        if (currentSection) {
            const activeLink = document.querySelector(`.nav a[href="#${currentSection}"]`);
            if (activeLink) {
                activeLink.classList.add('active');
            }
        }
    }
    
    /**
     * 平滑滚动到目标 section
     */
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // 只在是锚点链接时阻止默认行为
            if (href.startsWith('#')) {
                e.preventDefault();
                
                const targetId = href.substring(1);
                const targetSection = document.getElementById(targetId);
                
                if (targetSection) {
                    const offsetTop = targetSection.offsetTop - 100;
                    
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                    
                    // 更新 URL (不触发滚动)
                    history.pushState(null, null, href);
                }
            }
        });
    });
    
    // 监听滚动事件 (带节流)
    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                updateActiveNav();
                ticking = false;
            });
            ticking = true;
        }
    });
    
    // 初始化
    updateActiveNav();
    
    console.log('✅ 导航滚动高亮已初始化');
    
})();
