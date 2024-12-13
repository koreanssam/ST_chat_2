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
    """
    <style>
        .custom-card {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 40px;
            margin-bottom: 40px;
            background: linear-gradient(135deg, #f5f5f5, #e0e0e0);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            width: 80%;
            max-width: 2000px;
            text-align: center;
            transition: transform 0.3s ease;
            flex-direction: column; /* 추가된 부분 */
        }
        .custom-card:hover {
            transform: scale(1.05);
        }
        .custom-card strong {
            font-size: 20px;
            color: #333;
        }
        .custom-card a {
            font-size: 16px;
            color: #007bff;
            text-decoration: none;
        }
        .custom-card a:hover {
            text-decoration: underline;
        }
    </style>
    <div class='custom-card'>
        <strong>경남교육청 국어 교사 이성원</strong>
        <a href='mailto:koreanssam@koreanssam.kr'>koreanssam@koreanssam.kr</a>
    </div>
    """,
    unsafe_allow_html=True
)

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
