import os
import numpy as np
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import glob
import json
from transformers import CLIPProcessor, CLIPModel
import faiss

# 配置路径
IMAGE_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'images')
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')
TEXT_INDEX_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'text_to_image_index.index')
TOP_K = 10  # 返回的相似图片数量

# 确保数据目录存在
os.makedirs(os.path.dirname(TEXT_INDEX_PATH), exist_ok=True)

# 全局变量
global_text_model = None
global_processor = None
global_index = None
global_image_files = []
index_built = False

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 加载CLIP模型
def get_clip_model():
    global global_text_model, global_processor
    
    if global_text_model is not None and global_processor is not None:
        return global_text_model, global_processor
    
    try:
        # 加载CLIP模型和处理器
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        
        global_text_model = model
        global_processor = processor
        
        return model, processor
    except Exception as e:
        print(f"加载CLIP模型失败: {e}")
        return None, None

# 提取图片特征
def extract_image_features(img_path, model, processor):
    try:
        image = Image.open(img_path).convert('RGB')
        inputs = processor(images=image, return_tensors="pt")
        
        with torch.no_grad():
            image_features = model.get_image_features(**inputs)
            
        # 归一化特征向量
        image_features = image_features / image_features.norm(dim=1, keepdim=True)
        
        return image_features.cpu().numpy()[0]
    except Exception as e:
        print(f"提取图片特征失败: {e}")
        return None

# 提取文本特征
def extract_text_features(text, model, processor):
    try:
        inputs = processor(text=text, return_tensors="pt")
        
        with torch.no_grad():
            text_features = model.get_text_features(**inputs)
            
        # 归一化特征向量
        text_features = text_features / text_features.norm(dim=1, keepdim=True)
        
        return text_features.cpu().numpy()[0]
    except Exception as e:
        print(f"提取文本特征失败: {e}")
        return None

# 构建索引
def build_text_to_image_index():
    global global_index, global_image_files, index_built
    
    # 如果索引已经构建，直接返回
    if index_built and global_index is not None:
        print("索引已经构建并加载到内存")
        return global_index, global_image_files
    
    try:
        # 加载CLIP模型
        model, processor = get_clip_model()
        if model is None or processor is None:
            print("加载CLIP模型失败")
            return None, []
        
        # 获取所有图片文件
        image_files = glob.glob(os.path.join(IMAGE_FOLDER, '*.jpg'))
        image_files.extend(glob.glob(os.path.join(IMAGE_FOLDER, '*.png')))
        
        if not image_files:
            print(f"在 {IMAGE_FOLDER} 中没有找到图片文件")
            return None, []
        
        print(f"找到 {len(image_files)} 张图片用于索引")
        
        # 提取第一张图片的特征，获取特征维度
        sample_features = extract_image_features(image_files[0], model, processor)
        if sample_features is None:
            print("提取样本特征失败")
            return None, []
            
        dimension = len(sample_features)
        
        # 创建新索引
        index = faiss.IndexFlatIP(dimension)  # 使用内积相似度（余弦相似度）
        
        # 提取所有图片特征并添加到索引
        all_features = []
        valid_image_files = []
        
        for i, img_path in enumerate(image_files):
            try:
                features = extract_image_features(img_path, model, processor)
                if features is not None:
                    all_features.append(features)
                    valid_image_files.append(img_path)
                if i % 100 == 0:
                    print(f"已处理 {i}/{len(image_files)} 张图片")
            except Exception as e:
                print(f"处理 {img_path} 时出错: {e}")
        
        if not all_features:
            print("没有从图片中提取到有效特征")
            return None, []
        
        # 转换为numpy数组并添加到索引
        all_features = np.array(all_features).astype('float32')
        index.add(all_features)
        
        # 保存索引
        try:
            print(f"尝试保存索引到 {TEXT_INDEX_PATH}")
            faiss.write_index(index, TEXT_INDEX_PATH)
            print(f"成功保存包含 {index.ntotal} 个向量的索引")
        except Exception as e:
            print(f"保存索引时出错: {e}")
            print("继续使用内存中的索引")
        
        # 存储到全局变量
        global_index = index
        global_image_files = valid_image_files
        index_built = True
        
        return index, valid_image_files
    except Exception as e:
        print(f"构建索引时出现意外错误: {e}")
        return None, []

# 加载索引
def load_text_to_image_index():
    global global_index, global_image_files, index_built
    
    # 如果索引已经加载到内存，直接返回
    if global_index is not None:
        return global_index
    
    try:
        if not os.path.exists(TEXT_INDEX_PATH):
            print(f"在 {TEXT_INDEX_PATH} 中没有找到索引文件")
            return None
            
        index = faiss.read_index(TEXT_INDEX_PATH)
        print(f"加载了包含 {index.ntotal} 个向量的索引")
        global_index = index
        return index
    except Exception as e:
        print(f"加载索引时出错: {e}")
        return None

# 获取图片对应的词条信息
def get_image_entry_info(image_filename):
    try:
        from utils_database.models import Image, Post
        from flask import current_app
        
        # 使用数据库查询图片信息
        with current_app.app_context():
            # 查找图片对应的词条ID
            image = Image.query.filter_by(file_name=image_filename).first()
            
            if not image:
                print(f"在数据库中未找到图片: {image_filename}")
                return None
            
            # 如果找到图片，获取关联的帖子信息
            if image.post_id:
                post = Post.query.get(image.post_id)
                if post:
                    # 如果description是JSON字符串，解析它
                    description = ""
                    if post.description:
                        try:
                            desc_list = json.loads(post.description)
                            description = desc_list[0] if desc_list else ""
                        except:
                            description = post.description
                    
                    return {
                        'entry_id': image.post_id,
                        'title': post.title,
                        'type': post.type or '',
                        'description': description
                    }
        
        return None
    except Exception as e:
        print(f"获取图片 {image_filename} 的词条信息时出错: {e}")
        return None

# 搜索相似图片
def search_images_by_text(text_features, index, image_files, k=TOP_K):
    # 重塑文本特征用于Faiss
    text_features = text_features.reshape(1, -1).astype('float32')
    
    # 搜索索引
    similarities, indices = index.search(text_features, k)
    
    # 获取结果的图片路径
    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(image_files):
            try:
                image_filename = os.path.basename(image_files[idx])
                result = {
                    'image': image_filename,
                    'similarity': float(similarities[0][i])  # 相似度分数
                }
                
                # 获取图片对应的词条信息
                entry_info = get_image_entry_info(image_filename)
                if entry_info:
                    result['entry_info'] = entry_info
                
                results.append(result)
            except Exception as e:
                print(f"处理搜索结果 {idx} 时出错: {e}")
                continue
    
    return results

# 处理文字搜图请求
def process_text_search_request(text_query):
    global global_index, global_image_files
    
    try:
        # 检查查询文本是否为空
        if not text_query or text_query.strip() == "":
            return {'error': '查询文本为空'}
            
        # 加载CLIP模型
        model, processor = get_clip_model()
        if model is None or processor is None:
            return {'error': '加载CLIP模型失败'}
        
        # 提取文本特征
        text_features = extract_text_features(text_query, model, processor)
        if text_features is None:
            return {'error': '提取文本特征失败'}
        
        # 使用全局索引（如果可用），否则加载或构建索引
        index = global_index
        image_files = global_image_files
        
        if index is None:
            # 尝试从磁盘加载索引
            index = load_text_to_image_index()
            image_files = glob.glob(os.path.join(IMAGE_FOLDER, '*.jpg'))
            image_files.extend(glob.glob(os.path.join(IMAGE_FOLDER, '*.png')))
        
        if index is None:
            # 如果仍然为None，构建索引
            print("构建索引...")
            index, valid_image_files = build_text_to_image_index()
            if index is None:
                return {'error': '构建索引失败，请检查服务器日志'}
            image_files = valid_image_files
        
        # 搜索相似图片
        results = search_images_by_text(text_features, index, image_files)
        
        return {
            'query': text_query,
            'results': results
        }
    except Exception as e:
        print(f"处理文字搜图请求时出错: {e}")
        return {
            'error': f'处理搜索请求时出错: {str(e)}',
            'query': text_query,
            'results': []
        }

# 初始化索引
def initialize_text_to_image_index():
    global global_index, global_image_files
    print("初始化文字搜图索引...")
    global_index, global_image_files = build_text_to_image_index()
    if global_index is not None:
        print("索引成功构建并加载到内存")
        return True
    else:
        print("启动时构建索引失败，将在需要时重试")
        return False