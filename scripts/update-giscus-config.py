#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新 Giscus 评论系统配置

用法：python3 scripts/update-giscus-config.py
"""

from pathlib import Path
import re

# Giscus 配置（从 https://giscus.app 获取）
GISCUS_CONFIG = '''<script src="https://giscus.app/client.js"
        data-repo="zhihongzhang123/blog-pulse"
        data-repo-id="R_kgDORtmH5w"
        data-category="General"
        data-category-id="DIC_kwDORtmH584CnRbT"
        data-mapping="pathname"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="bottom"
        data-theme="preferred_color_scheme"
        data-lang="zh-CN"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>'''

def update_file(filepath: Path):
    """更新文件中的 Giscus 配置"""
    if not filepath.exists():
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找并替换 Giscus 配置
    pattern = r'<script src="https://giscus\.app/client\.js".*?</script>'
    new_content = re.sub(pattern, GISCUS_CONFIG, content, flags=re.DOTALL)
    
    if new_content == content:
        print(f"⚠️  未找到 Giscus 配置：{filepath}")
        return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ 已更新：{filepath}")
    return True

def main():
    """主函数"""
    blog_dir = Path(__file__).parent.parent
    
    # 需要更新的文件
    files_to_update = [
        blog_dir / 'index.html',
        blog_dir / 'about.html',
        blog_dir / 'market-analysis.html',
        blog_dir / 'briefings.html',
        blog_dir / 'live-trading.html',
    ]
    
    # 所有文章页面
    articles_dir = blog_dir / 'content' / 'daily-thoughts'
    if articles_dir.exists():
        files_to_update.extend(articles_dir.glob('*.html'))
    
    # 更新所有文件
    updated = 0
    for filepath in files_to_update:
        if update_file(filepath):
            updated += 1
    
    print(f"\n✅ 总计更新 {updated} 个文件")

if __name__ == '__main__':
    main()
