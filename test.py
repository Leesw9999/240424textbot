import streamlit as st # 스트림릿
import openai #openai
from datetime import datetime # 시간정보


def ask_gpt (prompt, model, apikey): # 질문 답변
    client=openai.OpenAI(api_key = apikey)
    response = client.chat.completions.create(model=model,messages=prompt)
    gptResponse = response.choices[0].message.content
    return gptResponse

def main():
    st.set_page_config(page_title="채팅 비서 프로그램",layout="wide") # 기본설정
    st.header("채팅 비서 프로그램") # 제목
    st.markdown("---") # 구분선
    with st.expander("채팅 비서 프로그램",expanded=True): # 기본설명
        # 설명 수정
        st.write(
        """
        - 2024년 04월 24일 인공지능서비스개발 중간고사입니다.
        - 202284060 - 이승우
        """
        )
        st.markdown("")
        # session state 초기화
        if "chat" not in st.session_state:
            st.session_state["chat"] = []
        if "OPENAI_API" not in st.session_state:
            st.session_state["OPENAI_API"] = ""
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "You are a thoughtful assistant. Respond to all input 50 words and answer in korean"}]

    with st.sidebar:
        st.session_state["OPENAI_API"] = st.text_input(label="OPENAI API 키", placeholder="Enter your API key", value="", type="password")
        st.markdown("---")
        model=st.radio(label="GPT 모델", options=["gpt-3.5-turbo", "gpt-4"])
        st.markdown("---")

        if st.button(label="초기화"):
            # 리셋 코드
            st.session_state["chat"] = []
            st.session_state["messages"] = [{"role": "assistant", "content": "You are a thoughtful assistant. Respond to all input 50 words and answer in korean"}]
            st.session_state["check_reset"] = True

    col1, col2=st.columns(2)
    with col1:
        st.subheader("질문하기")
        user_question=st.text_input(label="질문을 입력하세요.")
        
        if st.button("질문"):
            if user_question:
                now = datetime.now().strftime("%H:%M") # 채팅을 시각화하기 위해 질문 내용 저장
                st.session_state["chat"] = st.session_state["chat"]+[("user",now,user_question)]
                st.session_state["messages"]=st.session_state["messages"]+[{"role":"user","content":user_question}] # GPT 모델에 넣을 프롬프트를 위해 질문 내용 저장

    with col2:
        st.subheader("질문/답변")
        if user_question:
            response = ask_gpt(st.session_state["messages"], model, st.session_state["OPENAI_API"]) # 답변 얻기
            st.session_state["messages"]=st.session_state["messages"]+[{"role":"assistant","content":response}] # GPT 모델에 넣을 프롬프트를 위해 답변 내용 저장
            now = datetime.now().strftime("%H:%M") # 채팅을 시각화하기 위해 답변 내용 저장
            st.session_state["chat"] = st.session_state["chat"]+ [("bot",now,response)]
            
            for sender, time, message in st.session_state["chat"]:
                if sender == "user":
                    st.write(f'<div style="display:flex;align-items:center;"><div style="background-color:#007AFF;color:white;border-radius:12px;padding:8px 12px;margin-right:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)
                    st.write("")
                else:
                    st.write(f'<div style="display:flex;align-items:center;justify-content:flex-end;"><div style="background-color:lightgray;border-radius:12px;padding:8px 12px;margin-left:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)
                    st.write("")

if __name__=="__main__":
    main()
