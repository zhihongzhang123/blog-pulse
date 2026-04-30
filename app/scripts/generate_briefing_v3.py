#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简报生成器 v3 - 数据获取脚本

只负责获取数据并保存 JSON，AI 生成简报由 cron 任务完成。

用法:
    python3 generate_briefing_v3.py morning
    python3 generate_briefing_v3.py evening
"""

import sys
import json
import subprocess
from pathlib import Path

def run_data_pipeline(pipeline_type: str) -> dict:
    """运行数据获取管线"""
    script_path = Path('/Users/minimac/.hermes/skills/finance/news-brief/scripts/generate_v3.py')
    
    result = subprocess.run(
        ['python3', str(script_path), pipeline_type],
        capture_output=True,
        text=True,
        timeout=120
    )
    
    json_path = Path(f'/tmp/news-brief-v3-{pipeline_type}.json')
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    raise Exception(f"数据管线失败: {result.stderr}")


def main(pipeline_type: str = 'evening'):
    print(f"📊 获取{pipeline_type}简报数据...")
    data = run_data_pipeline(pipeline_type)
    print(f"✅ 获取 {data.get('news_count', 0)} 条新闻")
    print(f"📁 数据已保存：/tmp/news-brief-v3-{pipeline_type}.json")
    return data


if __name__ == '__main__':
    pipeline_type = sys.argv[1] if len(sys.argv) > 1 else 'evening'
    main(pipeline_type)
