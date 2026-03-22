#!/bin/bash
# Pulse Blog · 自动同步脚本
# 添加到 crontab 定时执行

set -e

WORKSPACE="/Users/minimac/.openclaw/workspace"
BLOG_DIR="$WORKSPACE/blog-pulse"

echo "========================================"
echo "📊 Pulse Blog 数据同步"
echo "========================================"
echo "时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 1. 运行数据同步脚本
echo "1️⃣ 同步数据..."
cd "$BLOG_DIR"
python3 scripts/sync-data.py

# 2. 提交并推送更新
echo ""
echo "2️⃣ 推送更新到 GitHub..."
cd "$BLOG_DIR"

if git status --porcelain | grep -q '.'; then
    git add -A
    git commit -m "Auto-sync: 更新数据 $(date '+%Y-%m-%d %H:%M')"
    git push
    echo "  ✅ 已推送"
else
    echo "  ⚠️ 无更新"
fi

echo ""
echo "========================================"
echo "✅ 同步完成"
echo "========================================"
