#!/usr/bin/env python3
"""
阅读计数器后端 API
使用 SQLite 存储全局阅读数据
"""

import sqlite3
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'views.db')

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS article_views (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE NOT NULL,
            title TEXT,
            count INTEGER DEFAULT 0,
            first_view TIMESTAMP,
            last_view TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS view_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ 数据库初始化完成")

class ViewsAPIHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_OPTIONS(self):
        self._set_headers()
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        
        if path == '/api/views':
            # 获取所有文章阅读数
            self._get_all_views()
        elif path == '/api/views/count':
            # 获取单篇文章阅读数
            article_path = query.get('path', [''])[0]
            self._get_view_count(article_path)
        elif path == '/api/views/top':
            # 获取热门文章
            limit = int(query.get('limit', ['10'])[0])
            self._get_top_articles(limit)
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())
    
    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/api/views/increment':
            # 增加阅读数
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode()
            data = json.loads(body)
            self._increment_view(data)
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())
    
    def _get_all_views(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT path, title, count, first_view, last_view 
            FROM article_views 
            ORDER BY count DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        articles = [{
            'path': row[0],
            'title': row[1],
            'count': row[2],
            'first_view': row[3],
            'last_view': row[4]
        } for row in rows]
        
        self._set_headers()
        self.wfile.write(json.dumps({'articles': articles}).encode())
    
    def _get_view_count(self, path):
        if not path:
            self._set_headers(400)
            self.wfile.write(json.dumps({'error': 'Missing path parameter'}).encode())
            return
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT count FROM article_views WHERE path = ?', (path,))
        row = cursor.fetchone()
        conn.close()
        
        count = row[0] if row else 0
        
        self._set_headers()
        self.wfile.write(json.dumps({'path': path, 'count': count}).encode())
    
    def _get_top_articles(self, limit):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT path, title, count 
            FROM article_views 
            ORDER BY count DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        articles = [{
            'path': row[0],
            'title': row[1],
            'count': row[2]
        } for row in rows]
        
        self._set_headers()
        self.wfile.write(json.dumps({'articles': articles}).encode())
    
    def _increment_view(self, data):
        path = data.get('path')
        title = data.get('title', '未知文章')
        ip = data.get('ip', 'unknown')
        ua = data.get('user_agent', 'unknown')
        
        if not path:
            self._set_headers(400)
            self.wfile.write(json.dumps({'error': 'Missing path'}).encode())
            return
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 检查是否存在
        cursor.execute('SELECT id, count FROM article_views WHERE path = ?', (path,))
        row = cursor.fetchone()
        
        if row:
            # 更新
            cursor.execute('''
                UPDATE article_views 
                SET count = count + 1, 
                    last_view = CURRENT_TIMESTAMP,
                    updated_at = CURRENT_TIMESTAMP
                WHERE path = ?
            ''', (path,))
            
            count = row[1] + 1
        else:
            # 插入
            cursor.execute('''
                INSERT INTO article_views (path, title, count, first_view, last_view)
                VALUES (?, ?, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ''', (path, title))
            
            count = 1
        
        # 记录日志
        cursor.execute('''
            INSERT INTO view_logs (path, ip_address, user_agent)
            VALUES (?, ?, ?)
        ''', (path, ip, ua))
        
        conn.commit()
        conn.close()
        
        self._set_headers()
        self.wfile.write(json.dumps({
            'path': path,
            'count': count,
            'success': True
        }).encode())
    
    def log_message(self, format, *args):
        # 禁用默认日志
        pass

def run_server(port=8000):
    init_db()
    server = HTTPServer(('localhost', port), ViewsAPIHandler)
    print(f"🚀 阅读计数 API 服务器运行在 http://localhost:{port}")
    print("API 端点:")
    print("  GET  /api/views          - 获取所有文章阅读数")
    print("  GET  /api/views/count?path=xxx - 获取单篇阅读数")
    print("  GET  /api/views/top?limit=10 - 获取热门文章")
    print("  POST /api/views/increment - 增加阅读数")
    server.serve_forever()

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
