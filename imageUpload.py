from dotenv import load_dotenv
import os
from openai import OpenAI
import streamlit as st
from PIL import Image
import base64
import requests

load_dotenv()

img = None
base64_image = None
api_key=os.environ.get("OPENAI_API_KEY")

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

st.title("KoJaem's bot 🚀")


uploaded_file = st.file_uploader('이미지를 업로드 하세요.', type=['png', 'jpg', 'jpeg'])
if uploaded_file is not None: # 파일을 넣을 경우에만 실행 함
    base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')
    img = Image.open(uploaded_file)
    st.image(img, caption='업로드된 이미지', use_column_width=True)

keyword = st.text_input('필요한것을 입력해주세요.')

if st.button('요청하기'):
    with st.spinner('이미지 생성중...'):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "model": "gpt-4o",
            "image": base64_image,
        }

        response = requests.post("https://api.openai.com/v1/images/variations", headers=headers, json=payload)
        if response.status_code == 200:
                result = response.json()
                st.write(result)
        else:
            st.write("Error:", response.status_code, response.text)
