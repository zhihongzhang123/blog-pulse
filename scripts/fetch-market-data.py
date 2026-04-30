#!/usr/bin/env python3
"""Fetch real-time market data and save as JSON for the Pulse blog."""
import json
import os
from datetime import datetime, timezone
from typing import Optional, Dict, Any

import yfinance as yf

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content")
OUTPUT = os.path.join(CONTENT_DIR, "market-data.json")

# Yahoo Finance ticker mappings
INDICES = {
    "SPY": {"name": "S&P 500", "ticker": "SPY"},
    "QQQ": {"name": "NASDAQ", "ticker": "QQQ"},
    "DIA": {"name": "DOW", "ticker": "DIA"},
    "IWM": {"name": "Russell 2000", "ticker": "IWM"},
    "SOXX": {"name": "Semiconductor", "ticker": "SOXX"},
    "RSP": {"name": "S&P 500 Equal Weight", "ticker": "RSP"},
}

EXTRAS = {
    "VIX": {"name": "VIX", "ticker": "^VIX"},
    "US10Y": {"name": "US 10Y", "ticker": "^TNX"},
}

COMMODITIES = {
    "CL": {"name": "WTI Crude", "ticker": "CL=F"},
    "GC": {"name": "Gold", "ticker": "GC=F"},
    "SI": {"name": "Silver", "ticker": "SI=F"},
}

WATCHLIST = {
    "BABA": {"name": "阿里巴巴", "ticker": "BABA"},
    "GOOGL": {"name": "谷歌", "ticker": "GOOGL"},
    "TSLA": {"name": "特斯拉", "ticker": "TSLA"},
    "NVDA": {"name": "英伟达", "ticker": "NVDA"},
    "TSM": {"name": "台积电", "ticker": "TSM"},
    "0700": {"name": "腾讯控股", "ticker": "0700.HK"},
}


def fetch_price(ticker_sym: str) -> Optional[Dict[str, Any]]:
    try:
        t = yf.Ticker(ticker_sym)
        info = t.fast_info
        price = info.last_price
        if price is None:
            return None
        prev_close = info.previous_close
        change_pct = ((price - prev_close) / prev_close * 100) if prev_close else 0
        return {
            "price": round(price, 2),
            "change_pct": round(change_pct, 2),
        }
    except Exception as e:
        print(f"  WARN: Failed to fetch {ticker_sym}: {e}")
        return None


def main():
    print(f"[{datetime.now().isoformat()}] Fetching market data...")
    all_tickers = []
    for group in [INDICES, EXTRAS, COMMODITIES, WATCHLIST]:
        all_tickers.extend(v["ticker"] for v in group.values())

    # Batch download for speed
    print(f"  Downloading {len(all_tickers)} tickers...")
    data = yf.download(all_tickers, period="5d", group_by="ticker", progress=False)

    result = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "indices": {},
        "extras": {},
        "commodities": {},
        "watchlist": {},
    }

    def get_change_from_df(df):
        """Calculate change% from last 2 rows of dataframe."""
        if df is None or df.empty:
            return None
        # Handle multi-column (some tickers have Open/High/Low/Close)
        if isinstance(df.columns, tuple) or hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
            close_col = ("Close", "") if ("Close", "") in df.columns else df.columns[0]
        else:
            close_col = "Close" if "Close" in df.columns else df.columns[0]
        series = df[close_col].dropna()
        if len(series) < 2:
            return None
        prev = series.iloc[-2]
        last = series.iloc[-1]
        return round((last - prev) / prev * 100, 2) if prev else 0

    def get_last_price_from_df(df):
        if df is None or df.empty:
            return None
        if isinstance(df.columns, tuple) or hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
            close_col = ("Close", "") if ("Close", "") in df.columns else df.columns[0]
        else:
            close_col = "Close" if "Close" in df.columns else df.columns[0]
        series = df[close_col].dropna()
        if series.empty:
            return None
        return round(series.iloc[-1], 2)

    for key, info in INDICES.items():
        df = data.get(key) if isinstance(data, dict) else None
        if df is not None:
            price = get_last_price_from_df(df)
            change = get_change_from_df(df)
            if price is not None:
                result["indices"][key] = {"name": info["name"], "price": price, "change_pct": change or 0}
        # Fallback: try direct fetch
        if key not in result["indices"]:
            p = fetch_price(info["ticker"])
            if p:
                result["indices"][key] = {"name": info["name"], "price": p["price"], "change_pct": p["change_pct"]}

    for key, info in EXTRAS.items():
        df = data.get(key) if isinstance(data, dict) else None
        if df is not None:
            price = get_last_price_from_df(df)
            change = get_change_from_df(df)
            if price is not None:
                # TNX is yield * 10, convert back
                if key == "US10Y":
                    price = round(price / 100, 4)
                result["extras"][key] = {"name": info["name"], "price": price, "change_pct": change or 0}
        if key not in result["extras"]:
            p = fetch_price(info["ticker"])
            if p:
                if key == "US10Y":
                    p["price"] = round(p["price"] / 100, 4)
                result["extras"][key] = {"name": info["name"], "price": p["price"], "change_pct": p["change_pct"]}

    for key, info in COMMODITIES.items():
        df = data.get(key) if isinstance(data, dict) else None
        if df is not None:
            price = get_last_price_from_df(df)
            change = get_change_from_df(df)
            if price is not None:
                result["commodities"][key] = {"name": info["name"], "price": price, "change_pct": change or 0}
        if key not in result["commodities"]:
            p = fetch_price(info["ticker"])
            if p:
                result["commodities"][key] = {"name": info["name"], "price": p["price"], "change_pct": p["change_pct"]}

    for key, info in WATCHLIST.items():
        df = data.get(key) if isinstance(data, dict) else None
        if df is not None:
            price = get_last_price_from_df(df)
            change = get_change_from_df(df)
            if price is not None:
                result["watchlist"][key] = {"name": info["name"], "price": price, "change_pct": change or 0}
        if key not in result["watchlist"]:
            p = fetch_price(info["ticker"])
            if p:
                result["watchlist"][key] = {"name": info["name"], "price": p["price"], "change_pct": p["change_pct"]}

    # Generate SP500 chart data from 5-day history
    spy_df = data.get("SPY")
    if spy_df is not None:
        if isinstance(spy_df.columns, tuple) or hasattr(spy_df.columns, "nlevels") and spy_df.columns.nlevels > 1:
            close_col = ("Close", "") if ("Close", "") in spy_df.columns else spy_df.columns[0]
        else:
            close_col = "Close" if "Close" in spy_df.columns else spy_df.columns[0]
        series = spy_df[close_col].dropna()
        chart_data = []
        for idx, val in series.items():
            date_str = idx.strftime("%b %d") if hasattr(idx, "strftime") else str(idx)[:10]
            chart_data.append({"date": date_str, "value": round(val, 2)})
        result["chart_data"] = chart_data

    # Write output
    os.makedirs(CONTENT_DIR, exist_ok=True)
    with open(OUTPUT, "w") as f:
        json.dump(result, f, indent=2)

    print(f"  Saved to {OUTPUT}")
    count = sum(len(v) for k, v in result.items() if k != "updated_at")
    print(f"  Fetched {count} items successfully")

    # Generate market analysis data
    indices = result.get("indices", {})
    extras = result.get("extras", {})

    # Market width calculation
    positive_count = sum(1 for v in indices.values() if v.get("change_pct", 0) > 0)
    total_count = len(indices)
    market_width = round((positive_count / total_count) * 100) if total_count > 0 else 50

    # Trend status
    spy_change = indices.get("SPY", {}).get("change_pct", 0)
    qqq_change = indices.get("QQQ", {}).get("change_pct", 0)
    if spy_change > 0.3 and qqq_change > 0.3:
        trend_status = "uptrend"
    elif spy_change < -0.3 and qqq_change < -0.3:
        trend_status = "downtrend"
    else:
        trend_status = "consolidation"

    # Risk signals
    top_construction = abs(qqq_change) < 0.3 and market_width < 60
    fomo_gap = qqq_change > 1.0
    vix_price = extras.get("VIX", {}).get("price", 0)
    vix_change = extras.get("VIX", {}).get("change_pct", 0)
    liquidity_alert = vix_change > 10

    analysis_data = {
        "updated_at": result.get("updated_at", ""),
        "indicators": {
            "QQQ": {
                "name": "纳斯达克100 (QQQ)",
                "value": indices.get("QQQ", {}).get("price", 0),
                "change": indices.get("QQQ", {}).get("change_pct", 0),
                "signal": "bullish" if indices.get("QQQ", {}).get("change_pct", 0) > 0.5 else "neutral",
                "comment": "科技股方向指引，关注顶部构造与连涨天数"
            },
            "SPY": {
                "name": "标普500 (SPY)",
                "value": indices.get("SPY", {}).get("price", 0),
                "change": indices.get("SPY", {}).get("change_pct", 0),
                "signal": "neutral",
                "comment": "宽基指数，与QQQ对比判断市场分化"
            },
            "IWM": {
                "name": "罗素2000 (IWM)",
                "value": indices.get("IWM", {}).get("price", 0),
                "change": indices.get("IWM", {}).get("change_pct", 0),
                "signal": "bearish" if indices.get("IWM", {}).get("change_pct", 0) < -0.5 else "neutral",
                "comment": "小盘股表现，判断市场宽度与资金扩散"
            },
            "SOXX": {
                "name": "半导体指数 (SOXX)",
                "value": indices.get("SOXX", {}).get("price", 0),
                "change": indices.get("SOXX", {}).get("change_pct", 0),
                "signal": "bullish" if indices.get("SOXX", {}).get("change_pct", 0) > 0 else "warning",
                "comment": "科技股龙头风向标，AI资本开支周期核心指标"
            },
            "RSP": {
                "name": "标普等权 (RSP)",
                "value": indices.get("RSP", {}).get("price", 0),
                "change": indices.get("RSP", {}).get("change_pct", 0),
                "signal": "neutral",
                "comment": "判断是否只是权重股在涨，等权vs市值权重分化"
            },
            "VIX": {
                "name": "VIX恐慌指数",
                "value": vix_price,
                "change": vix_change,
                "signal": "warning" if vix_price > 20 else "neutral",
                "comment": "市场恐慌情绪，>20警示，>30极度恐惧"
            }
        },
        "market_width": market_width,
        "trend_status": trend_status,
        "risk_signals": {
            "top_construction": top_construction,
            "fomo_gap": fomo_gap,
            "liquidity_alert": liquidity_alert
        }
    }

    analysis_path = os.path.join(CONTENT_DIR, "market-analysis-data.json")
    with open(analysis_path, "w", encoding="utf-8") as f:
        json.dump(analysis_data, f, indent=2, ensure_ascii=False)

    print(f"  Saved analysis to {analysis_path}")
    return result


if __name__ == "__main__":
    main()
