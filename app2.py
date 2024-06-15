import streamlit as st

col1, col2 = st.columns(2) # 두 개의 컬럼 생성. 표현하고 싶은 내용을 열 데이터로 나눠 보여주고 싶을 떄 사용합니다.

with col1:
    text1 = st.text_input("form을 이용하지 않는 경우")
    text2 = st.text_area("form을 이용하지 않는 경우")
    st.write("1번 입력값: " + text1)
    st.write("2번 입력값: " + text2)


with col2:
    with st.form("form을 사용합니다"):
        text3 = st.text_input("form을 이용하는 경우")
        text4 = st.text_area("form을 이용하는 경우")
        submitted = st.form_submit_button("제출")

        if submitted:
            st.write("1번 입력값: " + text3)
            st.write("2번 입력값: " + text4)
        else:
            st.write("1번 입력값: ")
            st.write("2번 입력값: ")