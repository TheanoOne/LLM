from zai import ZhipuAiClient
import os
from dotenv import load_dotenv

load_dotenv()

# 初始化客户端
client = ZhipuAiClient(api_key=os.getenv('OPENAI_API_KEY'))

# 创建流式消息请求
response = client.chat.completions.create(
    model=os.getenv('model'),
    messages=[
        {"role": "user", "content": "写一首关于春天的诗"}
    ],
    stream=True  # 启用流式输出
)

# 处理流式响应
full_content = ""
for chunk in response:
    if not chunk.choices:
        continue
    
    delta = chunk.choices[0].delta
    
    # 处理增量内容
    if hasattr(delta, 'content') and delta.content:
        full_content += delta.content
        print(delta.content, end="", flush=True)
    
    # 检查是否完成
    if chunk.choices[0].finish_reason:
        print(f"\n\n完成原因: {chunk.choices[0].finish_reason}")
        if hasattr(chunk, 'usage') and chunk.usage:
            print(f"令牌使用: 输入 {chunk.usage.prompt_tokens}, 输出 {chunk.usage.completion_tokens}")

print(f"\n\n完整内容:\n{full_content}")