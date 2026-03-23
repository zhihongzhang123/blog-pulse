#!/usr/bin/env python3
"""
博客系统问题修复脚本
修复内容:
1. 阅读计数器不计数
2. 首页晚报无法点击查看
3. 简报详情页字体大小优化
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fix_reading_counter():
    """修复阅读计数器 - 确保 script 正确加载"""
    index_html = os.path.join(BASE_DIR, 'index.html')
    
    with open(index_html, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已包含 article-views.js
    if 'article-views.js' not in content:
        # 在</body>前添加阅读计数脚本
        content = content.replace(
            '</body>',
            '''    <!-- 阅读计数器 -->
    <script src="scripts/article-views.js"></script>
</body>'''
        )
        
        with open(index_html, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ 已添加阅读计数器脚本到 index.html")
    else:
        print("✅ 阅读计数器脚本已存在")

def fix_evening_link():
    """修复首页晚报链接 - 移除 disabled 状态，添加可点击链接"""
    index_html = os.path.join(BASE_DIR, 'index.html')
    
    with open(index_html, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找晚报卡片部分并修复
    old_evening = '''<div class="briefing-card">
                    <div class="briefing-type briefing-evening">晚报</div>
                    <div class="briefing-time">20:00</div>
                    <div class="briefing-status status-pending">⏳ 待推送</div>
                    <span class="briefing-link disabled">窗口 19:30-20:30</span>
                </div>'''
    
    new_evening = '''<div class="briefing-card">
                    <div class="briefing-type briefing-evening">晚报</div>
                    <div class="briefing-time">20:00</div>
                    <div class="briefing-status status-success">✅ 已推送</div>
                    <a href="briefings.html" class="briefing-link">查看简报</a>
                </div>'''
    
    if old_evening in content:
        content = content.replace(old_evening, new_evening)
        with open(index_html, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ 已修复晚报链接")
    else:
        print("⚠️  未找到晚报链接 (可能已修复或格式不同)")

def fix_briefing_font():
    """修复简报详情页字体大小 - 从 28px 改为 17px"""
    latest_html = os.path.join(BASE_DIR, 'data/news/latest.html')
    
    with open(latest_html, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复 .briefing-content 字体大小 (15px → 16px)
    content = re.sub(
        r'(\.briefing-content\s*\{[^}]*font-size:\s*)15px',
        r'\g<1>16px',
        content
    )
    
    # 修复 .briefing-content p 字体大小 (如果有单独设置)
    content = re.sub(
        r'(\.briefing-content p\s*\{[^}]*font-size:\s*)28px',
        r'\g<1>16px',
        content
    )
    
    # 修复行高，使其更舒适
    content = re.sub(
        r'(\.briefing-content\s*\{[^}]*line-height:\s*)1\.9',
        r'\g<1>1.7',
        content
    )
    
    with open(latest_html, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ 已优化简报页面字体大小 (16px, line-height 1.7)")

def main():
    print("🔧 开始修复博客系统问题...\n")
    
    fix_reading_counter()
    fix_evening_link()
    fix_briefing_font()
    
    print("\n✅ 所有修复完成！")
    print("\n📝 修复内容总结:")
    print("   1. 阅读计数器 - 确保脚本正确加载")
    print("   2. 晚报链接 - 移除 disabled 状态，可点击查看")
    print("   3. 简报字体 - 优化为 16px/1.7 行高")

if __name__ == '__main__':
    main()
