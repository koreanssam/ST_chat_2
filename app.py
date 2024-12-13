import streamlit as st
from functions import chat_bot, available_document

# 페이지 설정
st.set_page_config(page_title="생기부 챗봇", layout="wide")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "available_document" not in st.session_state:
    st.session_state.available_document = available_document()

# 메인 채팅 영역
st.title("🤖 생기부 챗봇")

# 채팅 컨테이너    
chat_container = st.container(height=600)

# 메시지 표시
for message in st.session_state.messages:
    with chat_container.chat_message(message["role"]):
        st.markdown(message["content"])

# 입력 영역
user_input = st.chat_input("질문을 입력해주세요")

if user_input:
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "human", "content": user_input})
    
    # AI 응답을 위한 placeholder 생성
    with chat_container.chat_message("ai"):
        placeholder = st.empty()
        full_response = ""
        
        # 스트리밍 응답 처리
        for chunk in chat_bot(system_prompt=st.secrets["prompt1"], use_docs=st.session_state.available_document):
            full_response += chunk
            # placeholder를 사용하여 누적 없이 업데이트
            placeholder.markdown(full_response)
            
        # 최종 응답 저장
        st.session_state.messages.append({"role": "ai", "content": full_response})
