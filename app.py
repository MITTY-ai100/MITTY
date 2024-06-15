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
    [":rainbow[이미지 생성]", "비디오 생성", "음성파일!"],
    captions = ["필요한 이미지를 생성해드립니다.", "아직 구현 안됐어요😢", "./speech.mp3"])

keyword = st.text_input('필요한것을 입력해주세요.')

if st.button('요청하기'):
  if(type == ':rainbow[이미지 생성]'):
    with st.spinner('이미지 생성중...'):
        response = client.images.generate(
          model="dall-e-3",
          prompt=f'{keyword}',
          quality="standard",
          size="1024x1024",
          n=1,
      )
        image_url = response.data[0].url
        st.image(image_url)
  elif(type=='비디오 생성'):
     st.write('아직 안됐다니까요 😢😢😢')
  else:
     with st.spinner('이미지 생성중...'):
        audio_file= open("./speech.mp3", "rb")
        transcription = client.audio.transcriptions.create(
           model="whisper-1", 
           file=audio_file
           )
        audioText = transcription.text
        print(audioText)
        response = client.images.generate(
          model="dall-e-3",
          prompt=f'{audioText}',
          quality="standard",
          size="1024x1024",
          n=1,
      )
        image_url = response.data[0].url
        st.image(image_url)
