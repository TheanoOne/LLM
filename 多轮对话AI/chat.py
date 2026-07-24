from dotenv import load_dotenv
import os
from openai import AsyncOpenAI
import json
import asyncio
# from pathlib import Path

class GLM_4_7_flash:
    # 初始化模型
    def __init__(self):
        self.client = AsyncOpenAI(
            base_url='https://open.bigmodel.cn/api/paas/v4'
        )
        self.chat_history = []
        self.full_answer = ''

    # 用户输入
    async def user_input(self, prompt):
        await self.save_history('user', prompt)  # 记录用户输入内容

    # 保留对话记录
    async def save_history(self, role, content):
        self.chat_history.append(
            {
                'role': role,
                'content': content
            }
        )

    # 模型生成回答
    async def gen_response(self):
        print(f'{os.getenv("model")}: ')
        print('===========Thinking===========')

        self.response = await self.client.chat.completions.create(
            model=os.getenv('model'),
            messages=self.chat_history,
            stream=True, # 打开流式输出
            # max_tokens=65536,
            temperature=1.0
        )

        # 设置标记变量，实现只实行一次分割print的执行
        has_print_sep = False
        
        async for chunk in self.response:
            content = getattr(chunk.choices[0].delta, 'content', None)
            reasoning_content = getattr(chunk.choices[0].delta, 'reasoning_content', None)

            # 分隔符只执行一次，且是没有思考部分和有最终回答中间
            if not has_print_sep and not reasoning_content and content:
                print()
                print()
                print()
                print('===========Answer===========')
                has_print_sep = True

            # 思考部分流式输出
            if reasoning_content:
                print(reasoning_content, end='', flush=True)

            # 最终回答流式输出
            if content:
                print(content, end='', flush=True)
                self.full_answer += content
                
        print()
        await self.save_history('assistant', self.full_answer)
        self.full_answer = ''  # 重置完整回答，避免full_answer在保存到chat_history时还留有之前的所有记录
        self.print_ctnt(self.chat_history)
        print()

    # 自定义print输出，自动解析json格式，方便查看
    def print_ctnt(self, content):
        print(json.dumps(
                    content,
                    indent=4,
                    ensure_ascii=False
                ))

    # 清楚记录函数
    def clear_history(self):
        self.chat_history.clear()
        print('对话记录清空完毕。')
        self.print_ctnt(self.chat_history)

# 异步必须的格式，要通过asyncio.run来执行主函数
async def main():
    # Project_Root_Path = Path(__file__).resolve().parent.parent
    load_dotenv()
    chatAi = GLM_4_7_flash()
    while 1:
        # 异步获取输入
        prompt = await asyncio.to_thread(
            input,
            'user: '
        )

        # 判断clear和exit两种情况逻辑
        if prompt == 'clear':
            chatAi.clear_history()
            continue
        if prompt == 'exit':
            break

        await chatAi.user_input(prompt)

        await chatAi.gen_response()

if __name__ == '__main__':
    asyncio.run(main())
