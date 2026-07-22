from openai import OpenAI
import os
from dotenv import load_dotenv

def chat():
    client = OpenAI(
        api_key = os.getenv('API_key'),
        base_url = 'https://open.bigmodel.cn/api/paas/v4'
    )

    ques = input('user:')

    response = client.chat.completions.create(
        model=os.getenv('model'),
        messages=[
            {
                "role": "user",
                "content": ques
            }
        ],
        stream= True
    )

    print('ai:', end='')

    for chunk in response:
        # chunk 就是模型实时吐出的一小段文字
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)  # end="" 不换行；flush=True立刻打印
    print() # 对话结束换行

if __name__ == '__main__':
    load_dotenv()
    
    chat()