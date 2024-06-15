import streamlit as st

st.title('나의 첫 웹페이지')
st.subheader('This is a subheader with a divider', divider='rainbow')

if st.button('이름 보기'):
    st.write('KoJaem')

age = st.slider("How old are you?", 0, 130, 25)
st.write("I'm ", age, "years old")

option = st.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

st.write("You selected:", option)