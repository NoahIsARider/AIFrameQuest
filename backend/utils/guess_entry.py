from openai import OpenAI

api_key = "YOUR_API_KEY"  # 替换为你的API Key
api_base = "https://spark-api-open.xf-yun.com/v2/"

def get_spark_hint(prompt: str) -> str:
    """
    调用讯飞星火大模型，返回AI提示文本
    :param prompt: 用户问题（字符串）
    :return: AI回复内容（字符串）
    """
    client = OpenAI(api_key=api_key, base_url=api_base)
    tool = [
        {
            "type": "web_search",
            "web_search": {
                "enable": True,
                "search_mode": "deep"
            }
        }
    ]
    try:
        # 组装对话历史
        messages = [{"role": "user", "content": prompt}]
        # 非流式返回
        response = client.chat.completions.create(
            model="x1",
            messages=messages,
            stream=False,
            temperature=1.2,
            max_tokens=2048,
            tools=tool
        )
        # 只返回最终AI回复内容
        return response.choices[0].message.content
    except Exception as e:
        print(f"讯飞星火API调用失败: {e}")
        return "AI提示服务暂时不可用，请稍后再试。"
