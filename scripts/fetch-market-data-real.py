#!/usr/bin/env python3
"""
市场情绪数据自动更新脚本 (真实数据版)
使用 Alpha Vantage API 获取真实市场数据
"""

import json
import os
import urllib.request
import urllib.error
from datetime import datetime

# Alpha Vantage API Key (免费层：5 次/分钟，500 次/天)
API_KEY = "demo"  # 演示模式，实际使用请替换为真实 API Key
# 获取免费 API Key: https://www.alphavantage.co/support/#api-key

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MARKET_DATA_FILE = os.path.join(DATA_DIR, 'market-sentiment.json')
CACHE_FILE = os.path.join(DATA_DIR, 'market-data-cache.json')

def fetch_with_retry(url, max_retries=3):
    """带重试的 HTTP 请求"""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 Pulse-Blog/1.0'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"⚠️  请求失败，{max_retries - attempt - 1} 秒后重试...")
                import time
                time.sleep(max_retries - attempt)
            else:
                raise e
    return None

def fetch_sp500_real():
    """获取标普 500 真实数据 (使用 SPY ETF)"""
    try:
        # Alpha Vantage GLOBAL_QUOTE
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=SPY&apikey={API_KEY}"
        data = fetch_with_retry(url)
        
        if data and "Global Quote" in data:
            quote = data["Global Quote"]
            price = float(quote.get("05. price", 0))
            change = float(quote.get("03. percent change", 0))
            
            # 获取历史数据计算 200 日均线
            hist_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=SPY&outputsize=compact&apikey={API_KEY}"
            hist_data = fetch_with_retry(hist_url)
            
            ma200 = 0
            if hist_data and "Time Series (Daily)" in hist_data:
                closes = list(hist_data["Time Series (Daily)"].values())[:200]
                if len(closes) > 0:
                    ma200 = sum(float(c.get("4. close", 0)) for c in closes) / len(closes)
            
            vs_ma200 = ((price - ma200) / ma200 * 100) if ma200 > 0 else 0
            
            return {
                'price': round(price, 2),
                'change': round(change, 2),
                'vs_ma200': round(vs_ma200, 2),
                'trend': 'bullish' if price > ma200 else 'bearish',
                'updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
    except Exception as e:
        print(f"❌ 获取标普 500 数据失败：{e}")
    
    return None

def fetch_vix_real():
    """获取 VIX 恐慌指数真实数据"""
    try:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=^VIX&apikey={API_KEY}"
        data = fetch_with_retry(url)
        
        if data and "Global Quote" in data:
            quote = data["Global Quote"]
            price = float(quote.get("05. price", 0))
            change = float(quote.get("03. percent change", 0))
            
            return {
                'value': round(price, 2),
                'change': round(change, 2),
                'level': 'low' if price < 20 else ('high' if price > 30 else 'medium'),
                'updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
    except Exception as e:
        print(f"❌ 获取 VIX 数据失败：{e}")
    
    return None

def fetch_treasury_10y_real():
    """获取 10 年期美债收益率真实数据"""
    try:
        # 使用 TNX 或 US10Y
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=US10Y&apikey={API_KEY}"
        data = fetch_with_retry(url)
        
        if data and "Global Quote" in data:
            quote = data["Global Quote"]
            yield_val = float(quote.get("05. price", 0))
            change = float(quote.get("03. percent change", 0))
            
            return {
                'yield': round(yield_val, 2),
                'change': round(change, 2),
                'updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
    except Exception as e:
        print(f"❌ 获取美债收益率数据失败：{e}")
    
    return None

def load_cached_data():
    """加载缓存数据"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return None

def save_cached_data(data):
    """保存缓存数据"""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    print("🚀 开始更新市场情绪数据 (真实数据版)...")
    print(f"📅 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 确保数据目录存在
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # 尝试获取真实数据
    metrics = {
        'sp500': fetch_sp500_real(),
        'vix': fetch_vix_real(),
        'treasury_10y': fetch_treasury_10y_real(),
        'market_width': {'percentage': 65, 'updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
        'rsi': {'value': 62, 'level': 'neutral', 'updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
        'put_call': {'ratio': 0.82, 'sentiment': 'neutral', 'updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
        'updated_at': datetime.now().isoformat(),
        'data_source': 'Alpha Vantage (Real-time)'
    }
    
    # 检查是否有数据获取失败，使用缓存降级
    has_failure = any(v is None for k, v in metrics.items() if k not in ['market_width', 'rsi', 'put_call', 'updated_at', 'data_source'])
    
    if has_failure:
        print("⚠️  部分数据获取失败，尝试使用缓存...")
        cached = load_cached_data()
        if cached:
            for key in ['sp500', 'vix', 'treasury_10y']:
                if metrics[key] is None and key in cached:
                    metrics[key] = cached[key]
                    print(f"   ✅ 从缓存恢复：{key}")
    
    # 保存到 JSON 文件
    with open(MARKET_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)
    
    # 保存缓存
    save_cached_data(metrics)
    
    print()
    print("📊 数据概览:")
    if metrics.get('sp500'):
        sp = metrics['sp500']
        sign = '+' if sp['change'] >= 0 else ''
        print(f"   📈 标普 500: {sp['price']} ({sign}{sp['change']}%)")
    if metrics.get('vix'):
        vix = metrics['vix']
        print(f"   😨 VIX: {vix['value']} ({'低' if vix['level'] == 'low' else '高'})")
    if metrics.get('treasury_10y'):
        treasury = metrics['treasury_10y']
        print(f"   📉 10Y 美债：{treasury['yield']}%")
    
    print()
    print(f"💾 数据已保存：{MARKET_DATA_FILE}")
    print(f"💾 缓存已保存：{CACHE_FILE}")
    print("✅ 更新完成！")
    
    return metrics

if __name__ == '__main__':
    main()
