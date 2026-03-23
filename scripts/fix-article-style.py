#!/usr/bin/env python3
"""
统一优化所有文章页面的格式
"""

import os
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(BASE_DIR, 'content', 'daily-thoughts')

def update_article_template():
    """更新所有文章页面的样式"""
    
    files = glob.glob(os.path.join(CONTENT_DIR, '*.html'))
    
    for filepath in files:
        filename = os.path.basename(filepath)
        
        # 跳过已优化的文件
        if '2026-03-23-复利的本质.html' in filename:
            print(f"⏭️  跳过：{filename} (已优化)")
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已包含 article-views.js
        if '../../scripts/article-views.js' not in content:
            # 添加阅读计数脚本
            content = content.replace(
                '<script src="../../main.js"></script>',
                '<script src="../../scripts/article-views.js"></script>\n    <script src="../../main.js"></script>'
            )
            print(f"✅ 添加阅读计数：{filename}")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == '__main__':
    print("🔧 开始优化文章页面...\n")
    update_article_template()
    print("\n✅ 完成！")
