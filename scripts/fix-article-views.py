#!/usr/bin/env python3
"""
修复文章页面的阅读计数器脚本引用
"""

import os
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(BASE_DIR, 'content', 'daily-thoughts')

def fix_article_pages():
    """修复所有文章页面，添加阅读计数器脚本"""
    
    files = glob.glob(os.path.join(CONTENT_DIR, '*.html'))
    
    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已包含 article-views.js
        if 'article-views.js' in content:
            print(f"⏭️  跳过：{os.path.basename(filepath)} (已包含)")
            continue
        
        # 在 main.js 之前添加 article-views.js
        old_main = '<script src="../../main.js"></script>'
        new_scripts = '''<script src="../../scripts/article-views.js"></script>
    <script src="../../main.js"></script>'''
        
        if old_main in content:
            content = content.replace(old_main, new_scripts)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 修复：{os.path.basename(filepath)}")
        else:
            print(f"⚠️  未找到 main.js 引用：{os.path.basename(filepath)}")

if __name__ == '__main__':
    print("🔧 开始修复文章页面...\n")
    fix_article_pages()
    print("\n✅ 完成！")
