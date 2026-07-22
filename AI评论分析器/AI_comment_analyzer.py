import os
from openai import OpenAI
from dotenv import load_dotenv

def connect():
    client = OpenAI(
        base_url='https://open.bigmodel.cn/api/paas/v4'
    )
    return client

    

def output(prompt, client):
    response = client.chat.completions.create(
        model=os.getenv('model'),
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ],
        stream=True
    )

    print('AI评论分析：')

    for chunk in response:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end='', flush=True)
    print()


def construct_prompt():
    comment = input('请输入商品评价：')

    prompt = f"""
你是一名专业电商客服质量分析专家。
请分析下面商品评论：
评论：
{comment}
请按照以下内容以及格式输出：
问题类型：
问题描述：
优化建议：
"""

    return prompt


if __name__ == '__main__':
    load_dotenv()

    client = connect()
    prompt = construct_prompt()
    output(prompt, client)
