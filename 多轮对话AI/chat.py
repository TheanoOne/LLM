from dotenv import load_dotenv
import os
from openai import OpenAI
# from pathlib import Path

class GLM_4_7_flash:
    def __init__(self):
        self.client = OpenAI(
            base_url='https://open.bigmodel.cn/api/paas/v4'
        )
        self.chat_history = []
        self.full_answer = ''

    def user_input(self, prompt):
        self.save_history('user', prompt)

    def save_history(self, role, content):
        self.chat_history.append(
            {
                'role': role,
                'content': content
            }
        )

    def gen_response(self):
        self.response = self.client.chat.completions.create(
            model=os.getenv('model'),
            messages=self.chat_history,
            stream=True,
            # max_tokens=65536,
            temperature=1.0
        )
        
        print('GLM-4.7-flash: ', end='')
        for chunk in self.response:
            reasoning_content = getattr(chunk.choices[0].delta, 'reasoning_content', None)
            if reasoning_content:
                print(reasoning_content, end='', flush=True)

            content = getattr(chunk.choices[0].delta, 'content', None)
            if content:
                print(content, end='', flush=True)
                self.full_answer += content

        print()
        self.save_history('assistant', self.full_answer)
        print(self.chat_history)
        print()

if __name__ == '__main__':
    # Project_Root_Path = Path(__file__).resolve().parent.parent
    load_dotenv()
    chatAi = GLM_4_7_flash()
    prompt = input('user: ')
    while prompt != 'exit':
        chatAi.user_input(prompt)
        chatAi.gen_response()
        prompt = input('user: ')
