import streamlit as st
from functions import chat_bot, available_document

# 페이지 설정
st.set_page_config(page_title="생기부 챗봇", layout="wide")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "available_document" not in st.session_state:
    st.session_state.available_document = available_document()
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# 메인 채팅 영역
st.title("🤖 생기부 챗봇")
st.markdown(
"""##### 2024 학생부 기재요령 문서와 학교생활기록부 종합지원포털의 질의응답을 토대로 답변합니다.

- 100% 신뢰할 수는 없으며, 답변을 참고하시되 기재요령 문서를 재확인하시길 바랍니다.
- [경남교육청 이성원 제작.](mailto:koreanssam@koreanssam.kr)

""")
st.divider()

# 채팅 컨테이너    
chat_container = st.container(height=600)

# 이전 메시지들 표시
for message in st.session_state.messages:
    with chat_container.chat_message(message["role"]):
        st.markdown(message["content"])

# 입력 영역
user_input = st.chat_input("질문을 입력해주세요")

if user_input:
    # 사용자 입력을 세션 상태에 저장
    st.session_state.user_input = user_input
    
    # 사용자 메시지 표시
    with chat_container.chat_message("user"):
        st.markdown(user_input)
    
    # 사용자 메시지를 세션에 저장
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # AI 응답
    with chat_container.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # 스트리밍 응답
        for chunk in chat_bot(system_prompt=st.secrets["prompt1"], use_docs=st.session_state.available_document):
            full_response += chunk
            message_placeholder.markdown(full_response)
            
    # AI 응답을 세션에 저장
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    # 페이지 리프레시
    st.rerun()
