import os
import json
from typing import Dict, Any

def get_json_data() -> Dict[str, Any]:
    """
    读取JSON文件并返回数据
    
    Returns:
        Dict[str, Any]: JSON文件中的数据
    """
    try:
        # 获取当前文件的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Current directory: {current_dir}")
        # 构建JSON文件的完整路径
        json_path = os.path.join(current_dir, '..', 'data', 'sample_data.json')
        print(f"JSON file path: {json_path}")
        
        # 检查文件是否存在
        if not os.path.exists(json_path):
            raise Exception(f"JSON file not found at {json_path}")
            
        # 读取JSON文件
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print("Successfully loaded JSON data")
            return data
            
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise Exception(f"Error reading JSON file at {json_path}: {str(e)}")
