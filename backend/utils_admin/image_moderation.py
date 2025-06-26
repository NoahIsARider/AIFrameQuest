import json
import os
import base64
from openai import OpenAI
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ModelScope API配置
MODELSCOPE_BASE_URL = 'https://api-inference.modelscope.cn/v1/'
MODELSCOPE_API_KEY = 'YOUR_API_KEY'

def get_modelscope_client():
    """
    初始化并返回ModelScope客户端
    """
    try:
        client = OpenAI(
            base_url=MODELSCOPE_BASE_URL,
            api_key=MODELSCOPE_API_KEY,
        )
        return client
    except Exception as e:
        logger.error(f"初始化ModelScope客户端失败: {str(e)}")
        return None

def encode_image_to_base64(image_path):
    """
    将图片转换为base64编码
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        logger.error(f"图片编码失败: {str(e)}")
        return None

def moderate_image(image_path, entry_title=None):
    """
    使用ModelScope的Qwen2.5-VL-7B-Instruct模型审核图片
    检查图片是否包含不健康内容、违法内容
    """
    try:
        client = get_modelscope_client()
        if not client:
            return {"error": "ModelScope客户端初始化失败"}
        
        # 将图片转换为base64编码
        base64_image = encode_image_to_base64(image_path)
        if not base64_image:
            return {"error": "图片编码失败"}
        
        # 构建提示词
        prompt = "请分析这张图片，判断是否存在以下问题：\n"
        prompt += "1. 不健康内容（色情、暴力、血腥等）\n"
        prompt += "2. 违法内容（毒品、武器、违禁品等）\n"
        
        # # 如果提供了词条标题，则添加相关性检查
        # if entry_title:
        #     prompt += f"3. 与词条'{entry_title}'的相关性\n"
        
        prompt += "\n请以JSON格式返回分析结果，包括：\n"
        prompt += "- is_appropriate: 是否适当（true/false）\n"
        prompt += "- issues: 存在的问题列表\n"
        prompt += "- explanation: 简要解释\n"
        prompt += "- recommendation: 处理建议（通过/拒绝）\n"
        
        # if entry_title:
        #     prompt += "- relevance: 与词条的相关性评分（0-10）\n"
        #     prompt += "- relevance_explanation: 相关性解释\n"
        
        # 调用ModelScope的Qwen2.5-VL模型
        response = client.chat.completions.create(
            model='Qwen/Qwen2.5-VL-7B-Instruct',
            messages=[
                {"role": "system", "content": "你是一个专业的图片内容审核助手，负责分析图片内容是否合规。请以JSON格式返回结果。"},
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}
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
        logger.error(f"图片审核失败: {str(e)}")
        return {"error": str(e)}

def analyze_image_content(image_path, entry_title=None):
    """
    使用ModelScope的Qwen2.5-VL-7B-Instruct模型进行更深入的图片内容分析
    """
    try:
        client = get_modelscope_client()
        if not client:
            return {"error": "ModelScope客户端初始化失败"}
        
        # 将图片转换为base64编码
        base64_image = encode_image_to_base64(image_path)
        if not base64_image:
            return {"error": "图片编码失败"}
        
        # 构建提示词
        prompt = "请详细描述这张图片的内容，并分析以下方面：\n"
        prompt += "1. 图片主要内容\n"
        prompt += "2. 是否包含敏感或不适当内容\n"
        
        if entry_title:
            prompt += f"3. 图片内容与词条'{entry_title}'的相关性\n"
        
        prompt += "\n请以JSON格式返回分析结果，包括：\n"
        prompt += "- description: 图片描述\n"
        prompt += "- content_type: 内容类型（人物/风景/物品/其他）\n"
        prompt += "- sensitive_content: 是否包含敏感内容（true/false）\n"
        prompt += "- sensitive_details: 敏感内容详情（如有）\n"
        
        # if entry_title:
        #     prompt += "- relevance_score: 与词条的相关性评分（0-10）\n"
        #     prompt += "- relevance_details: 相关性详细解释\n"
        
        # 调用ModelScope的Qwen2.5-VL模型
        response = client.chat.completions.create(
            model='Qwen/Qwen2.5-VL-7B-Instruct',
            messages=[
                {"role": "system", "content": "你是一个专业的图片内容分析助手，负责详细分析图片内容。请以JSON格式返回结果。"},
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}
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
            # 如果JSON解析失败，返回原始文本
            return {
                "description": "无法解析JSON响应",
                "raw_response": result_text
            }
    except Exception as e:
        logger.error(f"图片内容分析失败: {str(e)}")
        return {"error": str(e)}

def moderate_images(images_info, uncensored_image_folder):
    """
    批量审核多张图片
    """
    results = []
    
    for image_id, image_info in images_info.items():
        file_name = image_info.get('file_name')
        entry = image_info.get('entry')
        
        if not file_name:
            continue
        
        # 构建图片完整路径
        image_path = os.path.join(uncensored_image_folder, file_name)
        
        if not os.path.exists(image_path):
            results.append({
                'id': image_id,
                'file_name': file_name,
                'error': '图片文件不存在'
            })
            continue
        
        # 基础审核
        moderation = moderate_image(image_path, entry)
        
        # 进行深入分析
        content_analysis = analyze_image_content(image_path, entry)
        
        results.append({
            'id': image_id,
            'file_name': file_name,
            'entry': entry,
            'moderation': moderation,
            'content_analysis': content_analysis
        })
    
    return results
