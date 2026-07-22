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


def construct_prompt(comment):
    prompt = f"""
你是一名专业电商客服质量分析专家，请快速完成以下内容：
请对下面每条商品评论进行分析：
评论：
{comment}
并请依据每条评论都按照以下内容以及格式输出：
评论情绪：
问题类型：
优化建议：

必须返回json格式文件，例如：
{{
"情绪":"消极",
"类型":"质量",
"建议":"提升材料"
}}
"""

    return prompt

def open_file(filePath):
    with open(filePath, 'r', encoding='utf-8') as f:
        comment = f.read()
    print(comment)
    return comment

if __name__ == '__main__':
    load_dotenv()

    client = connect()
    comment = open_file('./AI评论分析器/comments.txt')
    prompt = construct_prompt(comment)
    output(prompt, client)
