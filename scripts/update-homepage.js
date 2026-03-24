#!/usr/bin/env node
/**
 * 自动更新首页数据
 * 1. 更新每日思考文章列表（按日期倒序）
 * 2. 更新市场热点/板块/策略数据
 */

const fs = require('fs');
const path = require('path');

const BLOG_DIR = path.join(__dirname, '..');
const INDEX_FILE = path.join(BLOG_DIR, 'index.html');
const THOUGHTS_DIR = path.join(BLOG_DIR, 'content/daily-thoughts');

// 读取每日思考文章列表
function getThoughtArticles() {
    const files = fs.readdirSync(THOUGHTS_DIR);
    const articles = [];
    
    files.forEach(file => {
        if (file.endsWith('.html') && file !== 'index.html') {
            const filePath = path.join(THOUGHTS_DIR, file);
            const content = fs.readFileSync(filePath, 'utf8');
            
            // 提取标题
            const titleMatch = content.match(/<title>(.*?)<\/title>/);
            const title = titleMatch ? titleMatch[1].replace(' · Pulse', '') : file.replace('.html', '').replace(/^\d{4}-\d{2}-\d{2}-/, '');
            
            // 提取日期
            const dateMatch = file.match(/^(\d{4}-\d{2}-\d{2})/);
            const date = dateMatch ? dateMatch[1].replace(/-/g, '年').replace(/(\d{4})年(\d{2})月(\d{2})日/, '$1 年 $2 月 $3 日') : '未知日期';
            
            // 提取摘要
            const excerptMatch = content.match(/<div class="card-excerpt">\s*<p>(.*?)<\/p>/s);
            const excerpt = excerptMatch ? excerptMatch[1] : '...';
            
            // 提取标签
            const tags = [];
            const tagMatches = content.match(/<span class="tag">(.*?)<\/span>/g);
            if (tagMatches) {
                tagMatches.forEach(tag => {
                    const tagText = tag.replace(/<[^>]*>/g, '');
                    if (!tags.includes(tagText)) tags.push(tagText);
                });
            }
            
            articles.push({
                file,
                title,
                date,
                excerpt,
                tags,
                path: `content/daily-thoughts/${file}`
            });
        }
    });
    
    // 按日期倒序排序
    articles.sort((a, b) => {
        const dateA = a.file.match(/^\d{4}-\d{2}-\d{2}/)[0];
        const dateB = b.file.match(/^\d{4}-\d{2}-\d{2}/)[0];
        return dateB.localeCompare(dateA);
    });
    
    return articles;
}

// 生成文章卡片 HTML
function generateArticleCard(article, isFeatured = false) {
    const featuredClass = isFeatured ? ' featured' : '';
    const tags = article.tags.slice(0, 2).map(tag => `<span class="tag">${tag}</span>`).join('');
    
    return `
                <article class="card thought-card${featuredClass}">
                    <div class="card-date">${article.date}</div>
                    <h3 class="card-title">${article.title}</h3>
                    <div class="card-excerpt">
                        <p>${article.excerpt.substring(0, 150)}...</p>
                    </div>
                    <div class="card-meta">
                        ${tags}
                    </div>
                    <div class="card-views">👁️ 加载中...</div>
                    <a href="${article.path}" class="read-more">阅读全文 →</a>
                </article>`;
}

// 更新首页文章列表
function updateHomepage() {
    console.log('📝 读取每日思考文章...');
    const articles = getThoughtArticles();
    console.log(`✅ 找到 ${articles.length} 篇文章`);
    
    // 生成新的文章列表 HTML
    const articlesHtml = articles.slice(0, 4).map((article, index) => 
        generateArticleCard(article, index === 0)
    ).join('');
    
    // 读取首页
    let indexContent = fs.readFileSync(INDEX_FILE, 'utf8');
    
    // 替换文章列表
    const oldListRegex = /(<section id="daily-thoughts" class="section">[\s\S]*?<div class="content-grid">)[\s\S]*?(<\/div>\s*<\/section>)/;
    const newList = `$1${articlesHtml}\n            $2`;
    
    indexContent = indexContent.replace(oldListRegex, newList);
    
    // 保存首页
    fs.writeFileSync(INDEX_FILE, indexContent, 'utf8');
    console.log('✅ 首页已更新');
}

// 运行
updateHomepage();
