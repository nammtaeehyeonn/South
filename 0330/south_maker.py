import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import streamlit as st
import io
import pandas as pd
import random
import math
import json
import os
import matplotlib.font_manager as fm
import time
import datetime
import subprocess

all_players_list = ["김동선" ,"김선광" ,"김성재" ,"김영목" ,"김은민" ,"김철영" ,"남태현" ,"민병인" ,"박창후" ,"서윤찬" ,"서종민" ,"소지호" ,"이병훈" ,"이산호" ,"이재성" ,"이종현" ,"정지원" ,"조성민" ,"조영수" ,"차민재" ,"차종수" ,"최민규" ,"최형근" ,"최형주" ,"구형준" ,"홍태호", "용병1", "용병2", "용병3", "용병4", "용병5" ]

st.title("SOUTH_MAKER")
with st.expander('**1️⃣ 경기 정보 입력**'):
    st.divider()
    date = st.date_input("**경기 날짜**")
    st.write("")
    start_time = st.time_input("**경기 시간**", datetime.time(9,00), step=datetime.timedelta(minutes = 30))
    st.write("")
    location = st.text_input("**경기 장소**")
    st.divider()
    st.write("")
    opposing_team = st.text_input("**상대팀 명**")
    
with st.expander('**2️⃣ 스쿼드 입력**'):
    st.divider()
    players = st.multiselect("**참가 인원**", all_players_list)


if st.button("정보 저장"):
    with open("./123.txt", 'a') as f:
        f.write(str(date))









    
# 버튼을 생성합니다.
if st.button('깃허브에 커밋 & 푸시하기'):
    # 현재 시간을 커밋 메시지로 사용합니다.
    commit_message = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # subprocess를 사용하여 깃 명령어를 실행합니다.
    try:
        # 깃 add 명령어를 실행합니다.
        subprocess.run(["git", "add", "."], check=True)
        # 깃 commit 명령어를 실행합니다.
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        # 깃 push 명령어를 실행합니다.
        subprocess.run(["git", "push"], check=True)
        st.success('깃허브에 성공적으로 커밋 & 푸시되었습니다.')
    except subprocess.CalledProcessError as e:
        st.error(f'명령어 실행 중 오류가 발생했습니다: {e}')
