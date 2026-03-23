#!/usr/bin/env python3
"""
简报数据自动更新脚本
自动清理和格式化 latest.json 中的标题和内容
"""

import json
import re
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, 'data/news/latest.json')

def clean_title(title):
    """清理和格式化标题"""
    if not title:
        return title
    
    # 移除 🟢 和 evening
    title = re.sub(r'🟢\s*\d{4}-\d{2}-\d{2}\s+evening', '', title)
    
    # 添加 📰 和晚报
    if '晚报' not in title and 'evening' not in title:
        # 已经是正确格式
        return title
    
    # 替换 evening 为 晚报
    title = title.replace('evening', '晚报')
    
    # 确保有 📰
    if not title.startswith('📰'):
        title = '📰 ' + title
    
    # 替换 核心交易线索 为 交易策略
    title = title.replace('核心交易线索', '交易策略')
    title = title.replace('全球宏观与核心交易', '全球宏观与交易')
    
    return title

def clean_content(content):
    """清理内容中的技术元数据"""
    if not content:
        return content
    
    # 移除 (TL;DR)
    content = content.replace(' (TL;DR)', '')
    
    # 移除 (Asia/Shanghai)
    content = content.replace(' (Asia/Shanghai)', '')
    
    # 移除 自动推送
    content = content.replace('· 自动推送', '')
    
    # 移除 推送渠道：PushPlus 微信
    content = re.sub(r'\n\*推送渠道：PushPlus 微信\*', '', content)
    content = content.replace('推送渠道：PushPlus 微信', '')
    
    # 移除 MsgID
    content = re.sub(r'\nMsgID: [a-f0-9]+\n', '\n', content)
    content = re.sub(r'MsgID: [a-f0-9]+', '', content)
    
    # 移除 模式：Jina API
    content = re.sub(r'\n模式：Jina API \(非 browser 工具\)\n', '\n', content)
    
    # 移除 推送时间行
    content = re.sub(r'\n推送时间：\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\n', '\n', content)
    
    # 统一标题格式
    content = re.sub(
        r'# 🟢 (\d{4}-\d{2}-\d{2}) evening \| (.*)',
        r'# 📰 \1 晚报 | \2',
        content
    )
    
    content = re.sub(
        r'🟢 (\d{4}-\d{2}-\d{2}) 晚报 \| 全球宏观与核心交易线索',
        r'📰 \1 晚报 | 全球宏观与交易策略',
        content
    )
    
    # 替换 核心交易线索 为 交易策略
    content = content.replace('核心交易线索', '交易策略')
    
    return content

def update_json():
    """更新 JSON 文件"""
    if not os.path.exists(JSON_PATH):
        print(f"❌ 文件不存在：{JSON_PATH}")
        return False
    
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 备份
    backup_path = JSON_PATH + '.bak.' + datetime.now().strftime('%Y%m%d%H%M%S')
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"💾 已备份：{backup_path}")
    
    # 更新标题
    old_title = data.get('title', '')
    data['title'] = clean_title(old_title)
    
    # 更新 fullContent
    old_content = data.get('fullContent', '')
    data['fullContent'] = clean_content(old_content)
    
    # 移除 sourceFile (技术信息)
    if 'sourceFile' in data:
        del data['sourceFile']
    
    # 保存
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已更新：{JSON_PATH}")
    print(f"   标题：{old_title} → {data['title']}")
    
    return True

if __name__ == '__main__':
    print("🔧 开始更新简报数据...\n")
    
    if update_json():
        print("\n✅ 更新完成！")
        print("\n📝 下一步:")
        print("   git add data/news/latest.json")
        print("   git commit -m '优化：自动清理简报数据'")
        print("   git push")
    else:
        print("\n❌ 更新失败")
