from dotenv import load_dotenv
import os
from openai import OpenAI
import streamlit as st
from PIL import Image
import base64
import requests

load_dotenv()

api_key=os.environ.get("OPENAI_API_KEY")

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

st.title("KoJaem's bot 🚀")


type = st.radio(
    "어떤 작업이 필요하세요?",
    [":rainbow[이미지 생성]", "***이미지 업로드***", "필요없어요"],
    captions = ["필요한 이미지를 생성해드립니다.", "업로드한 이미지를 기반으로 작업물을 만들 수 있습니다.", "😢"])

#이미지 업로드 저장하지는 않음
if(type == '***이미지 업로드***'):
    uploaded_file = st.file_uploader('이미지를 업로드 하세요.', type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None: # 파일을 넣을 경우에만 실행 함
        base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')
        img = Image.open(uploaded_file)
        st.image(img, caption='업로드된 이미지', use_column_width=True)

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
  elif(type == '***이미지 업로드***'):
    with st.spinner('이미지 생성중...'):
      
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "내가 업로드한 이미지 파일의 케릭터를 최대한 자세하게 분석해줘."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)


                
        if response.status_code == 200:
            result = response.json()
            # content 값 추출
            message_content = result['choices'][0]['message']['content']
            img_response = client.images.generate(
                model="dall-e-3",
                prompt=f'{message_content} 정보를 기반으로 케릭터를 디즈니풍으로 만들어줘',
                quality="standard",
                size="1024x1024",
                n=1,
            )
            image_url = img_response.data[0].url
            st.image(image_url)
        else:
            st.write("Error:", response.status_code, response.text)

  else:
    st.write('필요없다면서 왜 누르세요 😢😢😢')
