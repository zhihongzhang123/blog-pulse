# 首页数据自动更新配置

## 数据源

### 市场热点
- CNBC Markets: https://cnbc.com/markets/
- CoinDesk: https://coindesk.com/
- Kitco: https://kitco.com/

### 板块数据
- Yahoo Finance Sectors: https://finance.yahoo.com/sectors/
- MarketWatch: https://marketwatch.com/tools/screener/sector-performance

### 市场情绪
- TradingView: https://tradingview.com/markets/stocks-usa/market-movers-active/
- CBOE VIX: https://cboe.com/tradable_products/vix/

## 更新频率

- **市场热点**: 每 4 小时
- **板块数据**: 每 1 小时（美股交易时段）
- **市场策略**: 根据 VIX 实时生成

## Crontab 配置

```bash
# 首页数据更新
0 */4 * * * cd /Users/minimac/.openclaw/workspace/blog-pulse && python3 scripts/fetch-homepage-browser.py
0 9-16 * * 1-5 cd /Users/minimac/.openclaw/workspace/blog-pulse && python3 scripts/fetch-homepage-browser.py  # 美股交易时段每小时
```

## 手动触发

```bash
cd /Users/minimac/.openclaw/workspace/blog-pulse
python3 scripts/fetch-homepage-browser.py
```

## 数据格式

```json
{
  "hotspots": [
    {"name": "AI 人工智能", "level": "hot"},
    {"name": "半导体", "level": "hot"},
    {"name": "新能源车", "level": "warm"}
  ],
  "sectors": [
    {"name": "科技 (XLK)", "change": "+2.3%", "trend": "领涨"},
    {"name": "能源 (XLE)", "change": "+1.8%", "trend": "强势"}
  ],
  "strategy": {
    "suggestion": "保持中性偏多仓位...",
    "position": "60-70%",
    "risk": "关注美联储政策动向"
  },
  "updated_at": "2026-03-24T23:53:00"
}
```

## 下一步优化

1. ✅ 创建浏览器自动化脚本
2. ⏳ 集成 OpenClaw browser 工具
3. ⏳ 创建 HTML 自动更新逻辑
4. ⏳ 配置定时任务
5. ⏳ 添加数据缓存和降级策略
