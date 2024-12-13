import streamlit as st
from functions import chat_bot, available_document

# 페이지 설정
st.set_page_config(
    page_title="생기부 챗봇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "available_document" not in st.session_state:
    st.session_state.available_document = available_document()

# 사이드바 설정
with st.sidebar:
    st.title("💬 대화 기록")
    if st.button("새로운 대화 시작", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    # 대화 기록 표시
    for idx, msg in enumerate(st.session_state.messages):
        if msg["role"] == "human":
            if st.button(f"🗣️ {msg['content'][:20]}...", key=f"history_{idx}", use_container_width=True):
                # 해당 대화로 이동하는 로직 추가 가능
                pass

# 메인 채팅 영역
col1, col2 = st.columns([3, 1])

with col1:
    st.title("🤖 생기부 챗봇")
    
    # 채팅 컨테이너
    chat_container = st.container(height=600)
    
    # 메시지 표시
    for message in st.session_state.messages:
        with chat_container.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 입력 영역
    user_input = st.chat_input("질문을 입력해주세요", key="user_input")
    
    if user_input:
        st.session_state.messages.append({"role": "human", "content": user_input})
        with chat_container.chat_message("human"):
            st.markdown(user_input)
            
        with chat_container.chat_message("ai"):
            with st.spinner("생각하는 중..."):
                full_response = ""
                for chunk in chat_bot(system_prompt=st.secrets["prompt1"], use_docs=st.session_state.available_document):
                    full_response += chunk
                    st.markdown(chunk)  # 누적된 전체 응답 대신 현재 청크만 표시
                st.session_state.messages.append({"role": "ai", "content": full_response})
