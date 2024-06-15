from dotenv import load_dotenv
import os
import openai
import streamlit as st
from PIL import Image
import base64
import io

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")

openai.api_key = api_key

st.title("KoJaem's bot 🚀")

uploaded_file = st.file_uploader('이미지를 업로드 하세요.', type=['png', 'jpg', 'jpeg'])
if uploaded_file is not None:  # 파일을 넣을 경우에만 실행 함
    img = Image.open(uploaded_file).convert('RGBA')  # 이미지를 RGBA 형식으로 변환
    st.image(img, caption='업로드된 이미지', use_column_width=True)

keyword = st.text_input('필요한 것을 입력해주세요.')

if st.button('요청하기'):
    with st.spinner('이미지 생성중...'):
        # 이미지를 바이트 스트림으로 변환
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')  # 이미지를 PNG 형식으로 저장
        img_byte_arr.seek(0)  # 바이트 스트림의 시작으로 이동

        response = openai.Image.create_edit(
            image=img_byte_arr.getvalue(),  # 바이트 스트림을 전달
            prompt=keyword,
            n=1,
            size="1024x1024"
        )
        print('keyword', keyword)
        print(response)
        if response and 'data' in response:
            st.image(response['data'][0]['url'])  # 이미지 URL을 올바르게 참조
        else:
            st.error("이미지 생성에 실패했습니다.")
