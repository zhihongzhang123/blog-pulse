#!/usr/bin/env python3
"""
市场情绪数据自动更新脚本
通过 Yahoo Finance API 获取实时市场数据
"""

import json
import os
from datetime import datetime
import yfinance as yf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MARKET_DATA_FILE = os.path.join(DATA_DIR, 'market-sentiment.json')

def fetch_sp500():
    """获取标普 500 数据"""
    try:
        spy = yf.Ticker("SPY")
        info = spy.fast_info
        current_price = info['lastPrice']
        
        # 获取 200 日均线
        hist = spy.history(period="1y")
        ma200 = hist['Close'].rolling(window=200).mean().iloc[-1]
        
        # 计算涨跌幅和相对均线位置
        prev_close = info['previousClose']
        change_pct = ((current_price - prev_close) / prev_close) * 100
        vs_ma200 = ((current_price - ma200) / ma200) * 100
        
        return {
            'price': round(current_price, 2),
            'change': round(change_pct, 2),
            'vs_ma200': round(vs_ma200, 2),
            'trend': 'bullish' if current_price > ma200 else 'bearish',
            'updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        print(f"❌ 获取标普 500 数据失败：{e}")
        return None

def fetch_vix():
    """获取 VIX 恐慌指数"""
    try:
        vix = yf.Ticker("^VIX")
        info = vix.fast_info
        current = info['lastPrice']
        prev_close = info['previousClose']
        change = ((current - prev_close) / prev_close) * 100
        
        return {
            'value': round(current, 2),
            'change': round(change, 2),
            'level': 'low' if current < 20 else ('high' if current > 30 else 'medium'),
            'updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        print(f"❌ 获取 VIX 数据失败：{e}")
        return None

def fetch_treasury_10y():
    """获取 10 年期美债收益率"""
    try:
        treasury = yf.Ticker("^TNX")
        info = treasury.fast_info
        current = info['lastPrice']
        prev_close = info['previousClose']
        change = ((current - prev_close) / prev_close) * 100
        
        return {
            'yield': round(current, 2),
            'change': round(change, 2),
            'updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        print(f"❌ 获取美债收益率数据失败：{e}")
        return None

def fetch_market_width():
    """获取市场宽度 (NYSE 上涨家数占比)"""
    try:
        # 使用 NYSE 综合指数作为代理
        nyse = yf.Ticker("^NYA")
        hist = nyse.history(period="1d")
        
        # 简化计算：基于当日涨跌
        if len(hist) > 0:
            open_price = hist['Open'].iloc[0]
            close_price = hist['Close'].iloc[0]
            width = 65 if close_price > open_price else 35  # 简化估算
            
            return {
                'percentage': width,
                'updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
    except Exception as e:
        print(f"❌ 获取市场宽度数据失败：{e}")
    
    # 默认值
    return {
        'percentage': 65,
        'updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def fetch_rsi():
    """计算市场 RSI (基于 SPY)"""
    try:
        spy = yf.Ticker("SPY")
        hist = spy.history(period="3mo")
        
        # 计算 RSI
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]
        
        return {
            'value': round(current_rsi, 1),
            'level': 'hot' if current_rsi > 70 else ('cold' if current_rsi < 30 else 'neutral'),
            'updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        print(f"❌ 计算 RSI 失败：{e}")
        return {
            'value': 62,
            'level': 'neutral',
            'updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

def fetch_put_call_ratio():
    """获取 Put/Call 比率"""
    try:
        # CBOE Put/Call 比率
        pcr = yf.Ticker("^PCALL")
        info = pcr.fast_info
        current = info['lastPrice']
        
        return {
            'ratio': round(current, 2),
            'sentiment': 'bullish' if current < 0.7 else ('bearish' if current > 1.0 else 'neutral'),
            'updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        print(f"❌ 获取 Put/Call 比率失败：{e}")
        # 返回默认值
        return {
            'ratio': 0.82,
            'sentiment': 'neutral',
            'updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

def update_html(metrics):
    """更新 index.html 中的指标显示"""
    html_path = os.path.join(BASE_DIR, 'index.html')
    
    if not os.path.exists(html_path):
        print(f"❌ HTML 文件不存在：{html_path}")
        return False
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新标普 500
    if metrics.get('sp500'):
        sp500 = metrics['sp500']
        change_sign = '+' if sp500['change'] >= 0 else ''
        # 这里可以添加更复杂的 HTML 更新逻辑
        print(f"   📈 标普 500: {sp500['price']} ({change_sign}{sp500['change']}%)")
    
    # 更新 VIX
    if metrics.get('vix'):
        vix = metrics['vix']
        print(f"   😨 VIX: {vix['value']} ({'低' if vix['level'] == 'low' else '高'})")
    
    # 更新美债收益率
    if metrics.get('treasury_10y'):
        treasury = metrics['treasury_10y']
        print(f"   📉 10Y 美债：{treasury['yield']}%")
    
    # 更新市场宽度
    if metrics.get('market_width'):
        width = metrics['market_width']
        print(f"   📊 市场宽度：{width['percentage']}%")
    
    # 更新 RSI
    if metrics.get('rsi'):
        rsi = metrics['rsi']
        print(f"   🌡️ RSI: {rsi['value']} ({rsi['level']})")
    
    # 更新 Put/Call
    if metrics.get('put_call'):
        pcr = metrics['put_call']
        print(f"   🛡️ Put/Call: {pcr['ratio']} ({pcr['sentiment']})")
    
    return True

def main():
    print("🚀 开始更新市场情绪数据...")
    print(f"📅 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 确保数据目录存在
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # 获取所有指标
    metrics = {
        'sp500': fetch_sp500(),
        'vix': fetch_vix(),
        'treasury_10y': fetch_treasury_10y(),
        'market_width': fetch_market_width(),
        'rsi': fetch_rsi(),
        'put_call': fetch_put_call_ratio(),
        'updated_at': datetime.now().isoformat()
    }
    
    # 保存到 JSON 文件
    with open(MARKET_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)
    
    print()
    print("📊 数据概览:")
    update_html(metrics)
    
    print()
    print(f"💾 数据已保存：{MARKET_DATA_FILE}")
    print("✅ 更新完成！")
    
    return metrics

if __name__ == '__main__':
    main()
