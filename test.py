import streamlit as st

# 첫 번째 버튼의 눌린 상태를 저장할 세션 상태 변수 초기화
if 'first_button_pressed' not in st.session_state:
    st.session_state.first_button_pressed = False

# 첫 번째 버튼
if st.button('첫 번째 버튼'):
    st.session_state.first_button_pressed = True  # 버튼이 눌리면 세션 상태 업데이트

# 첫 번째 버튼이 눌린 경우, 두 번째 버튼 생성
if st.session_state.first_button_pressed:
    st.write('첫 번째 버튼이 눌렸습니다!')
    
    # 두 번째 버튼
    if st.button('두 번째 버튼'):
        st.write('두 번째 버튼도 눌렸습니다!')

# 첫 번째 버튼의 눌린 상태를 유지하면서, 두 번째 버튼이 동적으로 생성됩니다.
