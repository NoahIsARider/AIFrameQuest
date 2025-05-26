from flask import Flask, request, jsonify
import json
import os
import logging

logger = logging.getLogger(__name__)

# 数据文件路径 - 使用绝对路径
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'entries.json')

# 读取 JSON 文件 - 返回列表格式的帖子数据，以便与前端兼容
def read_posts():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            entries_dict = json.load(f)
            # 将字典格式转换为列表格式返回
            posts_list = []
            for entry_key, entry_data in entries_dict.items():
                # 构建与前端兼容的帖子对象
                post = {
                    'id': entry_data['id'],
                    'title': entry_data['title'],
                    'content': entry_data['description'][0] if entry_data['description'] else '',
                    'author': entry_data['comments'][0]['name'] if entry_data['comments'] else '',
                    'category': entry_data.get('type', '动漫'),  # 读取type字段
                    'date': entry_data['comments'][0]['date'] if entry_data['comments'] else '',
                    'views': 0,
                    'comments': len(entry_data['comments']),
                    'favorites': 0,
                    'cover': entry_data.get('cover', ''),  # 添加封面字段
                    'type': entry_data.get('type', '动漫'),  # 添加类型字段
                    'description': entry_data.get('description', [])  # 添加描述字段
                }
                posts_list.append(post)
            return posts_list
    except Exception as e:
        logger.error(f"读取帖子数据出错: {str(e)}")
        return []

# 写入 JSON 文件 - 将列表格式的帖子数据转换为新的字典格式
def write_posts(posts_list):
    try:
        # 读取当前的字典格式数据
        current_entries = {}
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                try:
                    current_entries = json.load(f)
                except json.JSONDecodeError:
                    current_entries = {}
        
        # 更新或添加新的帖子
        for post in posts_list:
            entry_key = f"entry{post['id']}"
            
            # 如果是更新现有条目
            if entry_key in current_entries:
                entry = current_entries[entry_key]
                entry['id'] = post['id']
                entry['title'] = post['title']
                # 新增：同步type
                entry['type'] = post.get('category', '动漫')
                
                # 更新description
                if 'content' in post and post['content']:
                    entry['description'] = [post['content']]
                
                # 如果没有评论，添加一个默认评论
                if not entry['comments']:
                    entry['comments'] = [{
                        'name': post.get('author', ''),
                        'text': post.get('content', ''),
                        'rating': 0,
                        'date': post.get('date', '')
                    }]
            else:
                # 创建新条目
                current_entries[entry_key] = {
                    'id': post['id'],
                    'title': post['title'],
                    'type': post.get('category', '动漫'),  # 新增
                    'description': [post.get('content', '')] if 'content' in post else [],
                    'comments': [{
                        'name': post.get('author', ''),
                        'text': post.get('content', ''),
                        'rating': 0,
                        'date': post.get('date', '')
                    }]
                }
        
        # 写入文件
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(current_entries, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"写入帖子数据出错: {str(e)}")
        raise e

# 获取单个帖子详情 - 包含完整的评论信息和平均评分
def get_post_detail(post_id):
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            entries_dict = json.load(f)
            entry_key = f"entry{post_id}"
            if entry_key in entries_dict:
                entry = entries_dict[entry_key]
                # 计算平均评分
                total_rating = 0
                rating_count = 0
                for comment in entry['comments']:
                    if 'rating' in comment and comment['rating'] > 0:
                        total_rating += comment['rating']
                        rating_count += 1
                
                # 添加平均评分到返回数据
                entry['avg_rating'] = round(total_rating / rating_count, 1) if rating_count > 0 else 0
                entry['rating_count'] = rating_count
                
                return entry
            return None
    except Exception as e:
        logger.error(f"获取帖子详情出错: {str(e)}")
        return None


