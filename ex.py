############################################ streamilt ############################################

st.set_page_config(layout="wide")

if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content": prompt})
    
st.title("상담 예약하기_chat버전")

# for text in st.session_state.messages:
#     if (type(text) != dict):
#         # print(text)
#         st.session_state.messages.remove(text)
#     elif (text['role'] not in ['system', 'user', 'assistant']):
#         # print(text)
#         st.session_state.messages.remove(text)

left_column, chat_column, right_column = st.columns([1, 2, 1])

user_input = st.chat_input("물어보고 싶은 것을 입력하세요!")

with left_column:
    with st.chat_message(st.session_state.messages[0]['role']):
        st.write(st.session_state.messages[0]['content'].split('\'상담 정보\':')[0])


with chat_column:
    # 대화 처리
    if user_input:
        # 사용자의 입력을 메시지 리스트에 추가
        st.session_state.messages.append({"role": "user", "content": user_input})
        # for i in st.session_state.messages:
        #     if (type(i) != dict) | (i['role'] not in ['user', 'assistant']):
        #         st.session_state.messages.remove(i)
        response = run_conversation(st.session_state.messages)
        
        # 시스템의 답변을 메시지 리스트에 추가
        response_message = response.choices[0].message
        st.session_state.messages.append({"role": response_message.role, "content": response_message.content})
        # for i in st.session_state.messages:
        #     print(i)
        #     print()

    # 메시지 리스트를 화면에 표시
    for message in st.session_state.messages[1:]:
        if type(message) == dict:
            if message["role"] in ['user', 'assistant']:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

with right_column:
    with st.chat_message(st.session_state.messages[0]['role']):
        st.write(json.loads(st.session_state.messages[0]['content'].split('\'상담 정보\':')[-1].replace("'", '"')))