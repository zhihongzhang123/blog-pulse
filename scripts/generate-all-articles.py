#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量生成所有每日思考文章内容
"""

import json
import re
from pathlib import Path
from datetime import datetime

BLOG_DIR = Path(__file__).parent.parent
CONTENT_DIR = BLOG_DIR / 'content'

# 文章内容库
ARTICLE_TEMPLATES = {
    '复利的本质': {
        'tags': ['交易哲学', '长期主义'],
        'content': '''
            <p>巴菲特说："复利是世界第八大奇迹。"</p>
            
            <p>但大多数人理解的复利，只是公式：<strong>(1+r)^n</strong>。</p>
            
            <p>他们看到的是 r（收益率），却忽略了 n（时间）。</p>
            
            <h2>复利的真正敌人</h2>
            
            <p>不是低收益率，而是<strong>中断</strong>。</p>
            
            <p>一次爆仓，n 归零。一次情绪化交易，n 重置。一次"就这一次"的例外，n 断裂。</p>
            
            <blockquote>
                "活着才能享受复利。"
                <br>—— 老雷
            </blockquote>
            
            <h2>为什么大多数人享受不到复利？</h2>
            
            <p>因为他们追求的是<strong>暴富</strong>，不是<strong>变富</strong>。</p>
            
            <p>暴富需要高 r，变富需要长 n。</p>
            
            <p>高 r 意味着高风险，高风险意味着可能出局。出局的人，没有资格谈复利。</p>
            
            <div class="insight-box">
                <div class="insight-box-title">💡 核心洞察</div>
                <p><strong>复利的本质不是数学，是生存。</strong></p>
                <p>先活下来，再谈增长。先保证 n 不断裂，再考虑 r 的大小。</p>
            </div>
            
            <h2>如何保证 n 不断裂？</h2>
            
            <p><strong>1. 永不 All-in</strong></p>
            <p>无论机会有多好，永远保留退路。All-in 的人，一次错误就出局。</p>
            
            <p><strong>2. 设置止损</strong></p>
            <p>止损不是承认失败，是保护 n。小亏是成本，爆仓是终点。</p>
            
            <p><strong>3. 控制情绪</strong></p>
            <p>情绪化交易是 n 的最大杀手。愤怒、贪婪、恐惧都会让你做出愚蠢决定。</p>
            
            <h2>复利的三个阶段</h2>
            
            <p><strong>第一阶段：缓慢积累（1-3 年）</strong></p>
            <p>这个阶段最无聊。收益率不高，增长缓慢。大多数人在这一步放弃。</p>
            
            <p><strong>第二阶段：加速增长（3-7 年）</strong></p>
            <p>复利开始显现威力。你的收益开始超过本金投入。</p>
            
            <p><strong>第三阶段：指数爆发（7 年以上）</strong></p>
            <p>这时候你不需要再投入太多本金，收益本身就在滚雪球。</p>
            
            <h2>实战应用</h2>
            
            <p>1. <strong>先活下来</strong>：任何交易前，先问"最坏情况是什么？我能承受吗？"</p>
            
            <p>2. <strong>追求可持续</strong>：年化 15% 持续 20 年，远好于三年翻倍然后归零。</p>
            
            <p>3. <strong>保持耐心</strong>：复利前期很慢，后期很快。不要在前 5 年放弃。</p>
            
            <h2>最后的思考</h2>
            
            <p>爱因斯坦还说了一句话："复利只有对那些理解它的人有效。"</p>
            
            <p>理解什么？</p>
            
            <p>理解<strong>慢就是快</strong>。</p>
            
            <div class="action-box">
                <div class="action-box-title">🎯 本周行动</div>
                <p>1. 检查你的仓位：有没有 All-in 的情况？</p>
                <p>2. 设置止损：每笔交易的最大亏损是多少？</p>
                <p>3. 写下你的长期目标：5 年后、10 年后你想达到什么状态？</p>
            </div>
        '''
    },
    
    '在别人恐惧时，你看到了什么？': {
        'tags': ['交易哲学', '巴菲特智慧'],
        'content': '''
            <p>巴菲特的名言："别人贪婪时恐惧，别人恐惧时贪婪。"</p>
            
            <p>这句话人人都知道，但很少有人真正做到。</p>
            
            <p>为什么？</p>
            
            <h2>恐惧的本质</h2>
            
            <p>恐惧不是来自亏损本身，而是来自<strong>不确定性</strong>。</p>
            
            <p>当市场暴跌时，你不知道：</p>
            <ul>
                <li>还会跌多少？</li>
                <li>什么时候见底？</li>
                <li>公司会不会破产？</li>
                <li>经济会不会崩溃？</li>
            </ul>
            
            <p>这种不确定性，让人恐慌。</p>
            
            <blockquote>
                "市场暴跌时，大多数人看到的是数字。聪明人看到的是机会。"
            </blockquote>
            
            <h2>别人恐惧时，他们在想什么？</h2>
            
            <p>他们在想："完了，又要大跌了，赶紧跑！"</p>
            
            <p>他们在想："我的资产缩水了，我是个失败者。"</p>
            
            <p>他们在想："这次不一样，这次是真的完了。"</p>
            
            <p><strong>但事实是什么？</strong></p>
            
            <div class="insight-box">
                <div class="insight-box-title">💡 核心洞察</div>
                <p><strong>每次暴跌后，市场都会创新高。</strong></p>
                <p>2008 年金融危机，标普跌了 57%。但 10 年后，它涨了 3 倍。</p>
                <p>2020 年疫情崩盘，标普一个月跌了 34%。但 6 个月后，它创新高。</p>
            </div>
            
            <h2>别人恐惧时，你应该看到什么？</h2>
            
            <p><strong>1. 价格与价值的偏离</strong></p>
            <p>好公司的价格打 5 折、6 折。这是打折促销，不是世界末日。</p>
            
            <p><strong>2. 风险释放</strong></p>
            <p>暴跌是风险快速释放的过程。跌完了，风险就小了。</p>
            
            <p><strong>3. 财富转移</strong></p>
            <p>每次危机都是财富从弱者转移到强者的过程。你选择做哪一方？</p>
            
            <h2>如何做到"别人恐惧时贪婪"？</h2>
            
            <p><strong>前提 1：你有现金</strong></p>
            <p>满仓的人，看到暴跌只能干瞪眼。保持 20-30% 现金，你才有资格贪婪。</p>
            
            <p><strong>前提 2：你有标准</strong></p>
            <p>什么价格算便宜？提前算好。跌到这个价格，就买。不要临时决定。</p>
            
            <p><strong>前提 3：你有勇气</strong></p>
            <p>逆势买入需要勇气。但勇气不是盲目的，是基于计算的。</p>
            
            <h2>实战应用</h2>
            
            <p>1. <strong>列出清单</strong>：写下 5-10 只你想买的股票/ETF，以及它们的"便宜价格"。</p>
            
            <p>2. <strong>准备现金</strong>：保持 20-30% 现金，等待机会。</p>
            
            <p>3. <strong>模拟练习</strong>：下次暴跌时，先别操作，写下"如果我有现金，我会买什么？"</p>
            
            <h2>最后的思考</h2>
            
            <p>市场暴跌时，问自己一个问题：</p>
            
            <p><strong>"如果股市关门 5 年，我现在会买入还是卖出？"</strong></p>
            
            <p>如果答案是买入，那就对了。</p>
            
            <div class="action-box">
                <div class="action-box-title">🎯 本周行动</div>
                <p>1. 列出 3-5 只你想长期持有的股票/ETF</p>
                <p>2. 计算它们的"便宜价格"（比如历史 PE 的 30% 分位）</p>
                <p>3. 写下：如果跌到这个价格，你会买入多少？</p>
            </div>
        '''
    },
    
    '周期与人性': {
        'tags': ['交易哲学', '市场周期'],
        'content': '''
            <p>霍华德·马克斯说："太阳底下没有新鲜事。"</p>
            
            <p>市场在循环，人性不变。</p>
            
            <h2>周期的本质</h2>
            
            <p>周期不是随机波动，是<strong>人性的循环</strong>。</p>
            
            <p>繁荣时，人们贪婪，相信"这次不一样"。</p>
            <p>萧条时，人们恐惧，相信"这次更不一样"。</p>
            
            <p>但事实是：<strong>每次都一样</strong>。</p>
            
            <blockquote>
                "涨久必跌，跌久必涨，周期永恒。"
            </blockquote>
            
            <h2>你处于周期的哪个位置？</h2>
            
            <p>这是最重要的问题，但很少有人问。</p>
            
            <p><strong>牛市后期特征：</strong></p>
            <ul>
                <li>人人都是股神</li>
                <li>估值高得离谱</li>
                <li>新人疯狂入场</li>
                <li>"这次不一样"成为共识</li>
            </ul>
            
            <p><strong>熊市后期特征：</strong></p>
            <ul>
                <li>人人都是专家（解释为什么不能买）</li>
                <li>估值低得离谱</li>
                <li>新人销户离场</li>
                <li>"这次更不一样"成为共识</li>
            </ul>
            
            <div class="insight-box">
                <div class="insight-box-title">💡 核心洞察</div>
                <p><strong>最好的机会，出现在所有人都绝望时。</strong></p>
                <p>最差的时机，出现在所有人都兴奋时。</p>
            </div>
            
            <h2>如何利用周期？</h2>
            
            <p><strong>1. 识别位置</strong></p>
            <p>看估值（PE、PB）、看情绪（VIX、成交量）、看新闻（头条是贪婪还是恐惧）。</p>
            
            <p><strong>2. 逆向布局</strong></p>
            <p>别人贪婪时，你减仓。别人恐惧时，你加仓。</p>
            
            <p><strong>3. 保持耐心</strong></p>
            <p>周期转换需要时间。可能 1 年，可能 3 年。但一定会来。</p>
            
            <h2>人性不变</h2>
            
            <p>为什么周期会重复？</p>
            
            <p>因为人性不变。</p>
            
            <p>贪婪、恐惧、从众、过度自信……这些刻在基因里的东西，不会改变。</p>
            
            <p>100 年前的人，和现在的人，面对市场时的反应是一样的。</p>
            
            <p>100 年后，也会一样。</p>
            
            <h2>实战应用</h2>
            
            <p>1. <strong>评估当前周期位置</strong>：现在市场是贪婪还是恐惧？估值是高还是低？</p>
            
            <p>2. <strong>调整仓位</strong>：贪婪时降低仓位，恐惧时增加仓位。</p>
            
            <p>3. <strong>保持记录</strong>：写下你对当前周期的判断，6 个月后回头看。</p>
            
            <h2>最后的思考</h2>
            
            <p>你无法预测周期何时转向。</p>
            
            <p>但你可以知道：</p>
            <p><strong>现在处于什么位置。</strong></p>
            
            <p>这就够了。</p>
            
            <div class="action-box">
                <div class="action-box-title">🎯 本周行动</div>
                <p>1. 写下当前市场的 3 个特征（估值、情绪、新闻）</p>
                <p>2. 判断：现在处于周期的哪个阶段？（早期/中期/后期）</p>
                <p>3. 根据判断，你的仓位应该增加还是减少？</p>
            </div>
        '''
    },
    
    '等待的艺术': {
        'tags': ['交易哲学', '利弗莫尔'],
        'content': '''
            <p>利弗莫尔说："赚大钱的不是买卖，而是等待。"</p>
            
            <p>这句话，我花了 10 年才真正理解。</p>
            
            <h2>等待的三重境界</h2>
            
            <p><strong>第一重：被迫等待</strong></p>
            <p>新手最讨厌等待。他们觉得等待就是浪费时间，就是错过机会。</p>
            <p>所以他们不停交易，不停操作，不停犯错。</p>
            
            <p><strong>第二重：主动等待</strong></p>
            <p>老手知道等待的价值。他们设定标准，等待机会出现。</p>
            <p>机会不来，他们不动。机会来了，他们重拳出击。</p>
            
            <p><strong>第三重：享受等待</strong></p>
            <p>高手享受等待。他们知道，等待是交易的一部分。</p>
            <p>等待时，他们学习、复盘、锻炼、陪伴家人。</p>
            <p>等待不是虚度，是蓄力。</p>
            
            <blockquote>
                "市场永远有机会，但你的本金只有一次。"
            </blockquote>
            
            <h2>为什么要等待？</h2>
            
            <p><strong>1. 好机会不常有</strong></p>
            <p>真正的好机会，一年可能就 2-3 次。其他时间都是噪音。</p>
            
            <p><strong>2. 频繁交易消耗本金</strong></p>
            <p>手续费、滑点、错误决策……频繁交易的成本，远超你的想象。</p>
            
            <p><strong>3. 等待提升胜率</strong></p>
            <p>等待最佳击球区，胜率自然提高。勉强挥棒，只会三振出局。</p>
            
            <div class="insight-box">
                <div class="insight-box-title">💡 核心洞察</div>
                <p><strong>交易的本质是选择，不是行动。</strong></p>
                <p>选择做什么，比做什么更重要。</p>
                <p>选择不做什么，比做什么更更重要。</p>
            </div>
            
            <h2>等待什么？</h2>
            
            <p><strong>1. 等待趋势</strong></p>
            <p>趋势不明朗时，观望。趋势清晰时，跟随。</p>
            
            <p><strong>2. 等待价格</strong></p>
            <p>好公司也需要好价格。价格过高时，等待估值回归。</p>
            
            <p><strong>3. 等待自己</strong></p>
            <p>等待自己的情绪稳定，等待自己的判断清晰，等待自己的心态平和。</p>
            
            <h2>如何等待？</h2>
            
            <p><strong>1. 设定标准</strong></p>
            <p>什么情况下入场？什么情况下观望？写下来，严格执行。</p>
            
            <p><strong>2. 接受错过</strong></p>
            <p>错过 10 次机会，好过错 1 次本金。错过不是错误，是纪律。</p>
            
            <p><strong>3. 利用时间</strong></p>
            <p>等待时不要闲着。学习、复盘、锻炼、陪伴家人。等待是投资自己。</p>
            
            <h2>实战应用</h2>
            
            <p>1. <strong>写下标准</strong>：你的入场条件是什么？（至少 3 条）</p>
            
            <p>2. <strong>回顾历史</strong>：过去 3 个月，有多少次交易不符合标准？</p>
            
            <p>3. <strong>模拟练习</strong>：接下来 2 周，只交易符合标准的，其他全部观望。</p>
            
            <h2>最后的思考</h2>
            
            <p>交易不是比谁更勤奋。</p>
            
            <p>是比谁更有耐心。</p>
            
            <p>等待，是交易者最好的朋友。</p>
            
            <div class="action-box">
                <div class="action-box-title">🎯 本周行动</div>
                <p>1. 写下你的入场标准（至少 3 条）</p>
                <p>2. 回顾过去 10 次交易，有多少次符合标准？</p>
                <p>3. 如果只交易符合标准的，收益率会提高还是降低？</p>
            </div>
        '''
    },
}


def generate_articles():
    """生成所有文章内容"""
    print("📝 生成每日思考文章...\n")
    
    articles_dir = CONTENT_DIR / 'daily-thoughts'
    if not articles_dir.exists():
        print("⚠️  目录不存在")
        return
    
    for html_file in articles_dir.glob('*.html'):
        if html_file.name == 'index.html':
            continue
        
        # 读取文件
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取标题
        title_match = re.search(r'<h1 class="article-title">(.*?)</h1>', content)
        if not title_match:
            print(f"⚠️  无法提取标题：{html_file.name}")
            continue
        
        title = title_match.group(1).replace(' · Pulse', '').strip()
        
        # 查找对应模板
        template = None
        for key, value in ARTICLE_TEMPLATES.items():
            if key in title:
                template = value
                break
        
        if not template:
            print(f"⚪ 跳过（无模板）：{title}")
            continue
        
        # 生成新内容
        old_pattern = r'<div class="article-content">.*?</div>\s*<footer class="article-footer">'
        new_content = f'''<div class="article-content">
            {template['content']}
        </div>
        
        <footer class="article-footer">'''
        
        new_full = re.sub(old_pattern, new_content, content, flags=re.DOTALL)
        
        # 写回文件
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_full)
        
        print(f"✅ 已生成：{title}")
    
    print("\n✅ 文章生成完成！")


if __name__ == '__main__':
    generate_articles()
