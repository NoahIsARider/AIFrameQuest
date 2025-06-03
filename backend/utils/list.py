from flask import Flask, request, jsonify
import json
import os
from utils_database.models import Post, Comment, db
import logging
logger = logging.getLogger(__name__)

#entries数据读取，comments目前只在getdetails
def read_posts():
    """从数据库中读取所有帖子并返回兼容前端的数据格式"""
    try:
        logger.debug(" 开始从数据库查询帖子数据...")
        posts = Post.query.all()
     
        result = []
        for post in posts:
            description = json.loads(post.description) if post.description else []
            content = description[0] if len(description) > 0 else ""

            # 获取第一个评论者信息
            comment = Comment.query.filter_by(post_id=post.id).first()
            author = comment.name if comment else "匿名"
            date_str = comment.date.isoformat() if comment and comment.date else ""
            result.append({
                'id': post.id,
                'title': post.title,
                'content': content,
                'author': author,
                'category': post.type,
                'date': date_str,
                'views': post.views or 0,
                'comments': len(post.comments),
                'favorites':  0,
                'cover': post.cover,
                'type': post.type,
                'description': description
            })
        return result
    except Exception as e:
        logger.error(f"从数据库读取帖子时出错: {str(e)}")
        return []


def write_posts(posts_list):
    """将列表格式的帖子写入数据库"""
    try:
        for post_data in posts_list:
            # 检查是否已有该 ID 的帖子
            existing = Post.query.get(post_data['id'])

            if existing:
                # 更新现有帖子
                description = [post_data['content']] if post_data.get('content') else []
                existing.title = post_data.get('title', existing.title)
                existing.description = json.dumps(description, ensure_ascii=False)
                existing.type = post_data.get('category', existing.type)
                existing.cover = post_data.get('cover', existing.cover)

                db.session.add(existing)
            else:
                # 创建新帖子
                description = [post_data['content']] if post_data.get('content') else []
                new_post = Post(
                    id=post_data['id'],
                    title=post_data.get('title', ''),
                    description=json.dumps(description, ensure_ascii=False),
                    cover=post_data.get('cover', ''),
                    type=post_data.get('category', '动漫')
                )
                db.session.add(new_post)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error(f"写入数据库时出错: {str(e)}")
        raise e


def get_post_detail(post_id):
    try:
        post = Post.query.get(post_id)
        if not post:
            return None
         # 计算平均评分
        comments = Comment.query.filter_by(post_id=post_id).all()
        avg_rating = round(sum(c.rating for c in comments) / len(comments), 1) if comments else 0

        return {
            "id": post.id,
            "title": post.title,
            "description": json.loads(post.description) if post.description else [],
            "cover": post.cover,
            "type": post.type,
            "views": post.views or 0,
            "comments": [
                {
                    "name": c.name,
                    "text": c.text,
                    "rating": c.rating,
                    "date": c.date.isoformat() if c.date else None
                } for c in comments
            ],
            # 添加平均评分到返回数据
            "avg_rating": avg_rating,
            "rating_count": len(comments)
        }

    except Exception as e:
        logger.error(f"获取帖子详情失败: {str(e)}")
        return None
    


