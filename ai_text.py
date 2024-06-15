from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "좋은 아침입니다.",
        },
        {
            "role": "system",
            "content": "입력 받은 키워드에 대한 흥미진진한 300자 이내의 시나리오를 작성해줘.",
        }
    ],
    model="gpt-4o",
)

result = chat_completion.choices[0].message.content

print(result)