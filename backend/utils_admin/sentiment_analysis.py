#coding:UTF-8
import sys
import os
import pandas as pd
import json
import requests
from snownlp import SnowNLP

# BERT模型相关导入（如果安装了相关库）
try:
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    BERT_AVAILABLE = True
except ImportError:
    BERT_AVAILABLE = False

# 百度API密钥
BAIDU_API_KEY = "Inb6acS4ywQGq4WLredZQ9bI"
BAIDU_SECRET_KEY = "YOUR_API_KEY"

# 初始化BERT模型（如果可用）
if BERT_AVAILABLE:
    try:
        tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
        model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
    except Exception as e:
        print(f"加载BERT模型失败: {e}")
        BERT_AVAILABLE = False

# 获取百度API的access token
def get_baidu_access_token():
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={BAIDU_API_KEY}&client_secret={BAIDU_SECRET_KEY}"
    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json().get("access_token")
    except Exception as e:
        print(f"获取百度API access token失败: {e}")
        return None

# 使用BERT模型进行情感分析
def analyze_sentiment_bert(text):
    if not BERT_AVAILABLE:
        return {"error": "BERT模型不可用"}
    
    try:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=1)
        # 将1-5分转换为0-1之间的情感得分
        sentiment_score = (predictions.item() + 1) / 5.0
        return {"score": sentiment_score}
    except Exception as e:
        return {"error": str(e)}

# 使用SnowNLP进行情感分析
def analyze_sentiment_snownlp(text):
    try:
        s = SnowNLP(text)
        sentiment_score = s.sentiments
        return {"score": sentiment_score}
    except Exception as e:
        return {"error": str(e)}

# 使用百度API进行情感分析
def analyze_sentiment_baidu(text):
    try:
        access_token = get_baidu_access_token()
        if not access_token:
            return {"error": "获取百度API access token失败"}
        
        api_url = f"https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token={access_token}"
        payload = {"text": text}
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = requests.post(api_url, headers=headers, json=payload)
        response_data = response.json()
        
        if 'items' in response_data and response_data['items']:
            item = response_data['items'][0]
            return {
                "confidence": item.get('confidence', 0),
                "negative_prob": item.get('negative_prob', 0),
                "positive_prob": item.get('positive_prob', 0),
                "sentiment": item.get('sentiment', 0)
            }
        else:
            return {"error": "百度API返回数据格式错误"}
    except Exception as e:
        return {"error": str(e)}

# 批量分析评论
def analyze_comments(comments, method='snownlp'):
    results = []
    
    for comment in comments:
        comment_id = comment.get('id')
        text = comment.get('text', '')
        
        if not text:
            continue
        
        if method == 'bert':
            sentiment_result = analyze_sentiment_bert(text)
        elif method == 'baidu':
            sentiment_result = analyze_sentiment_baidu(text)
        else:  # 默认使用snownlp
            sentiment_result = analyze_sentiment_snownlp(text)
        
        # 检查是否有错误
        if "error" in sentiment_result:
            print(f"评论ID {comment_id} 分析失败: {sentiment_result['error']}")
            continue
        
        results.append({
            'id': comment_id,
            'text': text,
            'sentiment': sentiment_result
        })
    
    return results
