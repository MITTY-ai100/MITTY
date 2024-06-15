from dotenv import load_dotenv
import os
from openai import OpenAI
import streamlit as st
from PIL import Image
import base64
import requests

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

st.columns(3)[1].title("MITTY BOT 🧑🏼‍🎨🧑🏼‍🎨🧑🏼‍🎨🧑🏼‍🎨🧑🏼‍🎨")

st.header(':violet[***당신의 상상이 곧 현실이 된다*** 🫢]', divider='rainbow')
st.markdown(
    """
    <h3 style='font-size:16px;'>키워드를 입력하거나 이미지를 업로드하면 AI가 이미지를 생성하고, 이를 기반으로 네 컷 만화와 짧은 만화 영상을 제작해 드립니다.</h3>
    """, unsafe_allow_html=True
)
choices = st.radio(
    "어떤 작업을 하고 싶으신가요?",
    [":violet-background[이미지 업로드]", ":violet-background[AI 기반 이미지 생성]"],
    index=None,
)

if choices == ":violet-background[이미지 업로드]":
    uploaded_file = st.file_uploader('이미지를 업로드 하세요.', type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None:  # 파일을 넣을 경우에만 실행 함
        base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')
        img = Image.open(uploaded_file)
        st.image(img, caption='업로드된 이미지', use_column_width=True)
        if st.button('AI로 이미지 완성', type='primary'):
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
                                    "text": "이 그림이 퀄리티가 좋은 그림인지 확인해주고, 만약 퀄리티가 떨어진다면 어떻게 하면 더 좋은 그림이 될지 300자 이내로 간단하게 피드백해줘."
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
                feedback = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                if feedback.status_code == 200:
                    result = feedback.json()
                    # content 값 추출
                    message_content = result['choices'][0]['message']['content']
                    st.write(message_content)
                
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
                        prompt=f'{message_content} 의 정보는 어린아이가 그린 그림에 대한 정보야. 이 그림에서 어린아이가 그리고 싶었던 그림을 파악하고, 너가 새롭게 멋있는 그림을 모든 방안을 동원해서 최고의 그림을 만들어줘!',
                        quality="standard",
                        size="1024x1024",
                        n=1,
                    )
                    image_url = img_response.data[0].url
                    st.image(image_url)
                else:
                    st.write("Error:", response.status_code, response.text)

if choices == ":violet-background[AI 기반 이미지 생성]":
    keyword = st.text_input("아래 입력란에 이미지의 특징을 간단히 설명하는 키워드를 입력해주세요. ‘용감한 소녀’, ‘긴 붉은색 머리’, ‘파란 눈’, ‘마법을 사용하는’ 등. 입력된 키워드를 바탕으로 AI가 멋진 이미지를 생성해 드립니다.")
    if st.button('AI로 이미지 생성', type="primary"):
      with st.spinner('생성중...'):
        response = client.images.generate(
            model="dall-e-3",
            prompt=f'{keyword}',
            quality="standard",
            size="1024x1024",
            n=1,
            )
        image_url = response.data[0].url
        st.image(image_url)

st.divider()

st.write("✔️ 영감을 얻을 시간! 👀")

st.link_button("다른 작품 감상하기", "https://streamlit.io/gallery")
st.caption("다른 사용자가 만든 창작물을 감상해보세요. 갤러리로 이동하여 영감을 얻어보세요.")
