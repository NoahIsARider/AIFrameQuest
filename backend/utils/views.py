import json
import logging
from utils_database.models import Post, db

# 配置日志
logger = logging.getLogger(__name__)

def update_post_views(post_id):
    """
    更新帖子的浏览次数
    
    Args:
        post_id (int): 帖子ID
        
    Returns:
        tuple: (response_data, status_code)
            - response_data: 包含更新结果的字典
            - status_code: HTTP状态码
    """
    try:
        logger.debug(f"开始更新帖子 {post_id} 的浏览数")
        
        # 从数据库查询帖子
        post = Post.query.get(post_id)
        
        if not post:
            logger.error(f"帖子不存在: {post_id}")
            return {"error": "帖子不存在"}, 404
            
        # 增加浏览数
        current_views = post.views or 0
        post.views = current_views + 1
        logger.debug(f"更新浏览数: {current_views} -> {post.views}")
        
        # 保存更新后的数据
        try:
            db.session.commit()
            logger.debug("成功保存更新后的数据")
        except Exception as e:
            db.session.rollback()
            logger.error(f"保存数据库失败: {str(e)}")
            return {"error": "保存数据库失败"}, 500
            
        return {
            "message": "浏览数更新成功",
            "views": post.views
        }, 200
        
    except Exception as e:
        logger.error(f"更新浏览数时出错: {str(e)}", exc_info=True)
        return {"error": str(e)}, 500
