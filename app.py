import streamlit as st
from functions import chat_bot, available_document

title = "생기부 챗봇"
st.set_page_config(page_title=title, layout="wide")

st.header(f"🤖 {title}")
st.divider()

# 챗봇에서 사용할 문서 목록과 시스템 프롬프트
if "available_document" not in st.session_state:
    st.session_state["available_document"] = available_document()
docs_name = st.session_state["available_document"]
system_prompt = st.secrets["prompt1"]  # 고정된 시스템 프롬프트

chat_container = st.container(height=600, border=True)
chat_container.subheader("생기부 챗봇")

# 채팅 메시지 표시를 위한 빈 컨테이너 생성
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with chat_container.chat_message(message["role"]):
        st.text(message["content"])

user_input = chat_container.chat_input("질문을 입력해주세요", key="user_input")

if user_input:
    st.session_state.messages.append({"role": "human", "content": user_input})
    with chat_container.chat_message("human"):
        st.text(user_input)
    with chat_container.chat_message("ai"):
        with st.spinner("생각하는 중..."):
            response = chat_bot(system_prompt=system_prompt, use_docs=docs_name)
            full_response = ""
            for chunk in response:
                full_response += chunk
                st.write(full_response)
            st.session_state.messages.append({"role": "ai", "content": full_response})
