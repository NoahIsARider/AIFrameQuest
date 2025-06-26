# coding:UTF-8
import os
import json
from openai import OpenAI

# ModelScope API配置
MODELSCOPE_BASE_URL = 'https://api-inference.modelscope.cn/v1/'
MODELSCOPE_API_KEY = 'YOUR_API_KEY'

# 初始化ModelScope客户端
def get_modelscope_client():
    try:
        client = OpenAI(
            base_url=MODELSCOPE_BASE_URL,
            api_key=MODELSCOPE_API_KEY,
        )
        return client
    except Exception as e:
        print(f"初始化ModelScope客户端失败: {e}")
        return None

# 使用ModelScope进行评论审核
def moderate_comment(text):
    """
    使用ModelScope的Qwen模型检查评论内容
    返回审核结果和详细信息
    """
    try:
        client = get_modelscope_client()
        if not client:
            return {"error": "ModelScope客户端初始化失败"}
        
        # 构建提示词
        prompt = f"""请分析以下评论内容，判断是否存在以下问题：
1. 政治不正确的言论
2. 消极激进的言论
3. 歧视性言论（包括种族、性别、宗教等方面）
4. 煽动性言论
5. 不适当的内容（色情、暴力等）
6. 人身攻击
7. 虚假信息传播

评论内容："{text}"

请以JSON格式返回分析结果，包括：
- flagged: 是否标记为不适当内容（true/false）
- categories: 各个问题类别的检测结果（true/false）
- category_scores: 各个问题类别的置信度分数（0-1之间）
"""
        
        # 调用ModelScope的Qwen模型
        response = client.chat.completions.create(
            model='Qwen/Qwen2.5-7B-Instruct',
            messages=[
                {"role": "system", "content": "你是一个专业的内容审核助手，负责分析评论内容是否合规。请以JSON格式返回结果。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        # 解析JSON响应
        try:
            result_text = response.choices[0].message.content
            # 提取JSON部分
            json_start = result_text.find('{')
            json_end = result_text.rfind('}')
            if json_start >= 0 and json_end >= 0:
                json_str = result_text[json_start:json_end+1]
                result = json.loads(json_str)
                return result
            else:
                # 如果没有找到JSON格式，尝试解析整个响应
                return json.loads(result_text)
        except json.JSONDecodeError:
            # 如果JSON解析失败，返回原始文本
            return {
                "flagged": "无法解析" in result_text or "不适当" in result_text,
                "raw_response": result_text
            }
    except Exception as e:
        return {"error": str(e)}

# 使用ModelScope的Qwen模型进行更深入的评论分析
def analyze_comment_content(text):
    """
    使用ModelScope的Qwen模型分析评论内容
    检查政治正确性、消极激进言论等
    """
    try:
        client = get_modelscope_client()
        if not client:
            return {"error": "ModelScope客户端初始化失败"}
        
        # 构建提示词
        prompt = f"""请分析以下评论内容，判断是否存在以下问题：
1. 政治不正确的言论
2. 消极激进的言论
3. 歧视性言论（包括种族、性别、宗教等方面）
4. 煽动性言论
5. 不适当的内容（色情、暴力等）
6. 人身攻击
7. 虚假信息传播

评论内容："{text}"

请以JSON格式返回分析结果，包括：
- is_appropriate: 是否适当（true/false）
- issues: 存在的问题列表
- explanation: 简要解释
- recommendation: 处理建议（通过/警告/删除）
"""
        
        # 调用ModelScope的Qwen模型
        response = client.chat.completions.create(
            model='Qwen/Qwen2.5-7B-Instruct',
            messages=[
                {"role": "system", "content": "你是一个专业的内容审核助手，负责分析评论内容是否合规。请以JSON格式返回结果。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        # 解析JSON响应
        try:
            result_text = response.choices[0].message.content
            # 提取JSON部分
            json_start = result_text.find('{')
            json_end = result_text.rfind('}')
            if json_start >= 0 and json_end >= 0:
                json_str = result_text[json_start:json_end+1]
                analysis = json.loads(json_str)
                return analysis
            else:
                # 如果没有找到JSON格式，尝试解析整个响应
                return json.loads(result_text)
        except json.JSONDecodeError:
            # 如果JSON解析失败，返回原始文本和简单分析
            is_appropriate = not ("不适当" in result_text or "问题" in result_text or "违规" in result_text)
            return {
                "is_appropriate": is_appropriate,
                "explanation": "无法解析JSON响应，但根据文本分析判断",
                "raw_response": result_text
            }
    except Exception as e:
        return {"error": str(e)}

# 批量审核评论
def moderate_comments(comments):
    """
    批量审核多条评论
    """
    results = []
    
    for comment in comments:
        comment_id = comment.get('id')
        text = comment.get('text', '')
        
        if not text:
            continue
        
        # 基础审核
        moderation = moderate_comment(text)
        
        # 进行深入分析
        content_analysis = analyze_comment_content(text)
        
        results.append({
            'id': comment_id,
            'text': text,
            'moderation': moderation,
            'content_analysis': content_analysis
        })
    
    return results
