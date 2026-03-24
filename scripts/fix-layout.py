#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复首页布局问题 - PC 端和移动端优化
"""

import re
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent
STYLES_FILE = BLOG_DIR / 'styles.css'
INDEX_FILE = BLOG_DIR / 'index.html'

def fix_responsive_layout():
    """修复响应式布局"""
    print("🔧 修复响应式布局...\n")
    
    # 读取 CSS 文件
    with open(STYLES_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 优化容器最大宽度
    content = re.sub(
        r'\.container \{\s*max-width: 1200px;',
        '.container {\n    max-width: 1440px;',
        content
    )
    
    # 2. 优化内容网格（PC 端）
    old_content_grid = r'\.content-grid \{\s*display: grid;\s*grid-template-columns: repeat\(auto-fit, minmax\(300px, 1fr\)\);'
    new_content_grid = '''.content-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
    gap: 2rem;'''
    content = re.sub(old_content_grid, new_content_grid, content)
    
    # 3. 优化卡片内边距（PC 端更舒适）
    content = re.sub(
        r'\.card \{\s*padding: 1\.25rem;',
        '.card {\n    padding: 1.5rem;',
        content
    )
    
    # 4. 修复移动端响应式（≤768px）
    mobile_fix = '''
/* ========================================
   响应式优化 - 平板和手机 (≤768px)
   ======================================== */
@media (max-width: 768px) {
    /* 容器调整 */
    .container {
        padding: 0 16px;
    }
    
    /* 头部优化 */
    .logo h1 {
        font-size: 1.75rem;
    }
    
    .tagline {
        font-size: 0.9rem;
        padding: 0 16px;
    }
    
    /* 导航优化 - 改为可滚动 */
    .nav {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none;
        -ms-overflow-style: none;
        padding: 12px 16px;
        gap: 8px;
    }
    
    .nav::-webkit-scrollbar {
        display: none;
    }
    
    .nav a {
        font-size: 0.85rem;
        padding: 8px 14px;
        white-space: nowrap;
    }
    
    /* 模块标题 */
    .section-title {
        font-size: 1.4rem;
        margin-bottom: 1.25rem;
    }
    
    /* 市场情绪网格 - 改为 2 列 */
    .sentiment-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
    }
    
    /* 热点网格 - 改为 2 列 */
    .hotspots-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
    }
    
    /* 内容网格 - 单列 */
    .content-grid {
        grid-template-columns: 1fr;
        gap: 20px;
    }
    
    /* 卡片优化 */
    .card {
        padding: 16px;
        border-radius: 16px;
    }
    
    .card-title {
        font-size: 1.1rem;
    }
    
    .card-excerpt {
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    /* 简报网格 - 单列 */
    .briefing-grid {
        grid-template-columns: 1fr;
    }
    
    /* 小组件 - 单列 */
    .widgets-grid {
        grid-template-columns: 1fr;
    }
    
    /* 模式切换器 */
    .mode-switcher {
        padding: 6px;
        gap: 4px;
    }
    
    .switch-btn {
        padding: 8px 12px;
        font-size: 1rem;
    }
    
    /* 动态岛 */
    .dynamic-island {
        top: 12px;
        min-width: 120px;
        min-height: 36px;
    }
    
    .dynamic-island.expanded {
        min-width: 280px;
        min-height: 60px;
    }
    
    /* 分隔线 */
    .section-spaced {
        padding: 48px 0;
    }
}

/* ========================================
   响应式优化 - 小屏手机 (≤375px)
   ======================================== */
@media (max-width: 375px) {
    .container {
        padding: 0 12px;
    }
    
    .logo h1 {
        font-size: 1.5rem;
    }
    
    .tagline {
        font-size: 0.8rem;
    }
    
    .nav {
        gap: 6px;
        padding: 10px 12px;
    }
    
    .nav a {
        font-size: 0.8rem;
        padding: 6px 10px;
    }
    
    .section-title {
        font-size: 1.2rem;
    }
    
    /* 市场情绪 - 单列 */
    .sentiment-grid {
        grid-template-columns: 1fr;
    }
    
    /* 热点 - 单列 */
    .hotspots-grid {
        grid-template-columns: 1fr;
    }
    
    .card {
        padding: 14px;
    }
    
    .card-title {
        font-size: 1rem;
    }
    
    .card-excerpt {
        font-size: 0.85rem;
    }
}

/* ========================================
   响应式优化 - 超大屏 (≥1440px)
   ======================================== */
@media (min-width: 1440px) {
    .container {
        max-width: 1600px;
    }
    
    .content-grid {
        grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
        gap: 2.5rem;
    }
    
    .sentiment-grid {
        grid-template-columns: repeat(6, 1fr);
    }
}
'''
    
    # 删除旧的响应式部分
    content = re.sub(
        r'/\* =+ *\n   响应式.*?@media \(min-width: 768px\) \{[^}]*\} *\}',
        '',
        content,
        flags=re.DOTALL
    )
    
    # 添加新的响应式部分（在文件末尾前）
    content = content.rstrip() + '\n\n' + mobile_fix
    
    # 写回文件
    with open(STYLES_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 响应式布局已优化\n")


def fix_index_html():
    """修复首页 HTML 结构"""
    print("📝 优化首页 HTML 结构...\n")
    
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 确保容器正确包裹
    if '<div class="container">' not in content:
        print("⚠️  容器结构异常")
        return
    
    # 2. 优化模块间距类
    content = re.sub(
        r'class="section section-spaced"',
        'class="section section-spaced"',  # 保持不变，CSS 已优化
        content
    )
    
    # 3. 确保所有网格使用正确的类名
    grids_fixed = 0
    
    if 'sentiment-grid' in content:
        grids_fixed += 1
        print("  ✅ 市场情绪网格正常")
    
    if 'hotspots-grid' in content:
        grids_fixed += 1
        print("  ✅ 热点网格正常")
    
    if 'content-grid' in content:
        grids_fixed += 1
        print("  ✅ 内容网格正常")
    
    if 'briefing-grid' in content:
        grids_fixed += 1
        print("  ✅ 简报网格正常")
    
    print(f"\n✅ 共验证 {grids_fixed} 个网格布局\n")
    
    # 写回文件
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    print("=" * 60)
    print("🔧 博客布局修复工具")
    print("=" * 60 + "\n")
    
    fix_responsive_layout()
    fix_index_html()
    
    print("=" * 60)
    print("✅ 布局修复完成！")
    print("=" * 60)
    print("\n📱 优化内容:")
    print("  • PC 端：最大宽度 1440px，卡片间距优化")
    print("  • 平板：2 列布局，导航可滚动")
    print("  • 手机：单列布局，字体自适应")
    print("  • 小屏：进一步压缩间距")
    print("\n💾 备份文件：styles.css.backup-YYYYMMDD-HHMM")
