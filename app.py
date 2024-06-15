from dotenv import load_dotenv
import os
from openai import OpenAI
import streamlit as st

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

st.title("KoJaem's bot 🚀")


type = st.radio(
    "어떤 작업이 필요하세요?",
    [":rainbow[이미지 생성]", "***Text 생성***", "필요없어요"],
    captions = ["필요한 이미지를 생성해드립니다.", "요구사항에 맞게 텍스트를 출력해드립니다.", "😢"])

keyword = st.text_input('필요한것을 입력해주세요.')

if st.button('요청하기'):
  if(type == ':rainbow[이미지 생성]'):
    with st.spinner('이미지 생성중...'):
        chat_completion = client.chat.completions.create(
          messages=[
              {
                  "role": "user",
                  "content": keyword,
              },
              {
                  "role": "system",
                  "content": "사용자가 말한 content 에 대해 다양한 정보를 알려줘.",
              }
          ],
          model="gpt-4o",
          )
        response = client.images.generate(
          model="dall-e-3",
          prompt=f'{keyword}',
          quality="standard",
          size="1024x1024",
          n=1,
      )
        result = chat_completion.choices[0].message.content
        image_url = response.data[0].url
        st.write(result)
        st.image(image_url)
  elif(type == '***Text 생성***'):
    with st.spinner('텍스트 생성중...'):
      chat_completion = client.chat.completions.create(
      messages=[
          {
              "role": "user",
              "content": keyword,
          },
          {
              "role": "system",
              "content": "사용자가 말한 요구사항을 친절하게 300자 이내로 답변해줘",
          }
      ],
      model="gpt-4o",
      )
      result = chat_completion.choices[0].message.content
      st.write(result)
  else:
    st.write('필요없다면서 왜 누르세요 😢😢😢')
