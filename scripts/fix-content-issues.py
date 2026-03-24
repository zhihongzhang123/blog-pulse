#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
博客内容修复脚本

修复问题：
1. 文章页面内容为空（占位符）
2. 首页市场情绪数据硬编码
"""

import json
import re
from pathlib import Path
from datetime import datetime

BLOG_DIR = Path(__file__).parent.parent
CONTENT_DIR = BLOG_DIR / 'content'
DATA_DIR = BLOG_DIR / 'data'

def fix_daily_thought_articles():
    """修复每日思考文章内容"""
    print("📝 修复每日思考文章...")
    
    articles_dir = CONTENT_DIR / 'daily-thoughts'
    if not articles_dir.exists():
        print("  ⚠️  目录不存在")
        return
    
    # 文章内容模板（根据标题生成不同内容）
    article_contents = {
        '等待的价值': '''
            <p>利弗莫尔说："赚大钱的不是买卖，而是等待。"</p>
            
            <p>这句话听起来简单，但真正理解的人寥寥无几。</p>
            
            <h2>等待不是无所作为</h2>
            
            <p>大多数人对等待有误解。他们以为等待就是什么都不做，就是被动。</p>
            
            <p>错。等待是<strong>主动的选择</strong>。</p>
            
            <p>猎人等待猎物，不是因为他懒惰，而是因为他知道：过早暴露只会让猎物逃跑。交易者等待机会，不是因为他犹豫，而是因为他明白：频繁交易只会消耗本金。</p>
            
            <div class="insight-box">
                <div class="insight-box-title">💡 核心洞察</div>
                <p><strong>等待的本质是纪律。</strong></p>
                <p>等待不是被动挨打，而是主动选择最佳击球区。</p>
            </div>
            
            <h2>什么是"最佳击球区"？</h2>
            
            <p>巴菲特用棒球比喻投资：投资最棒的地方是没有好球数限制。你可以等待那个最甜的击球区，没有人会判你三振出局。</p>
            
            <p>但大多数人做不到。为什么？</p>
            
            <p>因为<strong>无聊</strong>。因为<strong>FOMO</strong>（害怕错过）。因为<strong>自我怀疑</strong>。</p>
            
            <blockquote>
                "市场永远有机会，但你的本金只有一次。"
                <br>—— 老雷
            </blockquote>
            
            <h2>等待的三重境界</h2>
            
            <p><strong>第一重：等待趋势</strong></p>
            <p>趋势不明朗时，空仓等待。这是技术层面的等待。</p>
            
            <p><strong>第二重：等待价格</strong></p>
            <p>好公司也需要好价格。价格过高时，耐心等待估值回归。这是价值层面的等待。</p>
            
            <p><strong>第三重：等待自己</strong></p>
            <p>等待自己的情绪稳定，等待自己的判断清晰，等待自己的心态平和。这是心智层面的等待。</p>
            
            <h2>实战应用</h2>
            
            <p>1. <strong>设定明确标准</strong>：什么情况下入场？什么情况下观望？写下来，严格执行。</p>
            
            <p>2. <strong>接受错过</strong>：错过 10 次机会，好过错 1 次本金。</p>
            
            <p>3. <strong>利用等待时间</strong>：学习、复盘、锻炼、陪伴家人。等待不是虚度光阴。</p>
            
            <h2>最后的思考</h2>
            
            <p>市场先生每天都会来敲门。今天他出价 100 块，明天出价 80 块，后天出价 120 块。</p>
            
            <p>你不必每次都和他交易。</p>
            
            <p>你可以说："今天价格不合适，明天再来吧。"</p>
            
            <p>这就是等待的力量。</p>
            
            <div class="action-box">
                <div class="action-box-title">🎯 本周行动</div>
                <p>1. 写下你的入场标准（至少 3 条）</p>
                <p>2. 回顾过去 3 个月，有多少次交易不符合标准？</p>
                <p>3. 如果只交易符合标准的，收益率会提高还是降低？</p>
            </div>
        ''',
        
        '市场先生的礼物': '''
            <p>格雷厄姆讲过一个经典寓言：市场先生。</p>
            
            <p>市场先生是你的合作伙伴，他每天都会来敲你的门，给你一个报价：要么他买你的股份，要么他卖给你股份。</p>
            
            <p>但市场先生有个问题——他情绪不稳定。</p>
            
            <h2>市场先生的两种状态</h2>
            
            <p><strong>状态一：极度乐观</strong></p>
            <p>今天市场先生心情大好，他觉得世界一片光明，经济繁荣，企业盈利会持续增长。于是他出一个<strong>很高的价格</strong>，想买下你的股份。</p>
            
            <p><strong>状态二：极度悲观</strong></p>
            <p>明天市场先生情绪崩溃，他觉得世界末日要来了，经济要崩盘，企业要倒闭。于是他出一个<strong>很低的价格</strong>，想卖掉他的股份。</p>
            
            <div class="insight-box">
                <div class="insight-box-title">💡 核心洞察</div>
                <p><strong>市场先生是为你服务的，不是来指导你的。</strong></p>
                <p>他的报价是参考，不是命令。</p>
            </div>
            
            <h2>大多数人怎么对待市场先生？</h2>
            
            <p>他们把市场先生当成<strong>老师</strong>。</p>
            
            <p>市场先生出高价，他们就跟着兴奋，觉得资产增值了，自己变聪明了。</p>
            
            <p>市场先生出低价，他们就跟着恐慌，觉得资产缩水了，自己犯错了。</p>
            
            <p>于是他们<strong>高买低卖</strong>——在市场先生乐观时买入，在市场先生悲观时卖出。</p>
            
            <blockquote>
                "别人贪婪时恐惧，别人恐惧时贪婪。"
                <br>—— 巴菲特
            </blockquote>
            
            <h2>聪明人怎么对待市场先生？</h2>
            
            <p>他们把市场先生当成<strong>仆人</strong>。</p>
            
            <p>市场先生出高价时，聪明人说："哦，你想买？价格不错，但我暂时不想卖。"</p>
            
            <p>市场先生出低价时，聪明人说："哦，你想卖？价格很诱人，我考虑一下。"</p>
            
            <p><strong>主动权在谁手里？在聪明人手里。</strong></p>
            
            <h2>市场先生的礼物</h2>
            
            <p>市场先生最大的礼物是什么？</p>
            
            <p>是<strong>极端情绪</strong>。</p>
            
            <p>当他极度悲观时，他给你<strong>低价买入</strong>的机会。</p>
            
            <p>当他极度乐观时，他给你<strong>高价卖出</strong>的机会。</p>
            
            <p>但大多数人把这份礼物当成了<strong>威胁</strong>。</p>
            
            <h2>实战应用</h2>
            
            <p>1. <strong>逆向思考</strong>：市场恐慌时，问自己"这是机会还是风险？"</p>
            
            <p>2. <strong>设定标准</strong>：什么价格算"便宜"？什么价格算"贵"？提前算好，不要临时决定。</p>
            
            <p>3. <strong>保持现金</strong>：没有现金，市场先生给你再好的价格你也买不了。</p>
            
            <h2>最后的思考</h2>
            
            <p>下次市场先生来敲门时，记住：</p>
            
            <p>他是个情绪化的疯子。</p>
            
            <p>但他的疯狂，是你的机会。</p>
            
            <div class="action-box">
                <div class="action-box-title">🎯 本周行动</div>
                <p>1. 列出你关注的 3-5 只股票/ETF</p>
                <p>2. 计算它们的"便宜价格"和"贵价格"</p>
                <p>3. 写下：如果市场先生给出这个价格，你会怎么做？</p>
            </div>
        ''',
    }
    
    # 遍历所有文章
    for html_file in articles_dir.glob('*.html'):
        # 跳过索引页
        if html_file.name == 'index.html':
            continue
        
        # 读取文件
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取标题
        title_match = re.search(r'<h1 class="article-title">(.*?)</h1>', content)
        if not title_match:
            print(f"  ⚠️  无法提取标题：{html_file.name}")
            continue
        
        title = title_match.group(1).replace(' · Pulse', '').strip()
        
        # 查找对应内容
        article_content = None
        for key, value in article_contents.items():
            if key in title:
                article_content = value
                break
        
        if not article_content:
            print(f"  ⚪ 跳过（无预设内容）：{title}")
            continue
        
        # 替换占位符内容
        old_content_pattern = r'<div class="article-content">.*?</div>\s*<footer class="article-footer">'
        new_content = f'''<div class="article-content">
            {article_content}
        </div>
        
        <footer class="article-footer">'''
        
        new_content_full = re.sub(old_content_pattern, new_content, content, flags=re.DOTALL)
        
        # 写回文件
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content_full)
        
        print(f"  ✅ 已修复：{title}")
    
    print("✅ 每日思考文章修复完成\n")


def update_homepage_market_data():
    """更新首页市场情绪数据为动态加载"""
    print("📊 更新首页市场数据...")
    
    # 读取市场数据
    market_file = DATA_DIR / 'market-sentiment.json'
    if not market_file.exists():
        print("  ⚠️  市场数据文件不存在")
        return
    
    with open(market_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 读取首页 HTML
    index_file = BLOG_DIR / 'index.html'
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换硬编码数据为动态数据
    replacements = {
        # 标普 500
        r'<div class="sentiment-value positive">\+0\.8%</div>\s*<div class="sentiment-bar">.*?<p class="sentiment-desc">价格位于 200 日均线上方，趋势偏多</p>':
        f'''<div class="sentiment-value {'positive' if data.get('sp500', {}).get('vs_ma200', 0) > 0 else 'negative'}">{data.get('sp500', {}).get('vs_ma200', 0):+.1f}%</div>
                    <div class="sentiment-bar">
                        <div class="sentiment-fill {'positive' if data.get('sp500', {}).get('vs_ma200', 0) > 0 else 'negative'}" style="width: {min(abs(data.get('sp500', {}).get('vs_ma200', 0)) * 10, 100)}%"></div>
                    </div>
                    <p class="sentiment-desc">价格位于 200 日均线{'上方' if data.get('sp500', {}).get('vs_ma200', 0) > 0 else '下方'}，趋势{'偏多' if data.get('sp500', {}).get('vs_ma200', 0) > 0 else '偏空'}</p>''',
        
        # VIX
        r'<div class="sentiment-value low">18\.5</div>\s*<p class="sentiment-desc">低于 20，市场情绪稳定，适合持仓</p>':
        f'''<div class="sentiment-value {'low' if data.get('vix', {}).get('value', 0) < 20 else ('high' if data.get('vix', {}).get('value', 0) > 30 else 'neutral')}">{data.get('vix', {}).get('value', 0)}</div>
                    <p class="sentiment-desc">{'低于 20，市场情绪稳定，适合持仓' if data.get('vix', {}).get('value', 0) < 20 else ('高于 30，市场恐慌，关注机会' if data.get('vix', {}).get('value', 0) > 30 else '中性区间，观望为主')}</p>''',
        
        # 美债
        r'<div class="sentiment-value">4\.28%</div>\s*<p class="sentiment-desc">收益率平稳，经济预期温和</p>':
        f'''<div class="sentiment-value">{data.get('treasury_10y', {}).get('yield', 4.28):.2f}%</div>
                    <p class="sentiment-desc">{'收益率上升，通胀预期升温' if data.get('treasury_10y', {}).get('yield', 4.28) > 4.5 else '收益率平稳，经济预期温和'}</p>''',
    }
    
    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content)
    
    # 写回文件
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("  ✅ 首页市场数据已更新为动态加载\n")


if __name__ == '__main__':
    print("=" * 60)
    print("🔧 博客内容修复工具")
    print("=" * 60 + "\n")
    
    fix_daily_thought_articles()
    update_homepage_market_data()
    
    print("=" * 60)
    print("✅ 所有修复完成！")
    print("=" * 60)
