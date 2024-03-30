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

from pymongo.mongo_client import MongoClient

    
uri = "mongodb+srv://skaxogusdl:skaclxo661@southdb.h5j75si.mongodb.net/?retryWrites=true&w=majority&appName=SOUTHDB"
client = MongoClient(uri)
db = client.mydb
if 'DB' not in st.session_state:
    st.session_state.DB = {"uri":uri, "client":client, "db":db}
    print("="*100)
    print("Pinged your deployment. You successfully connected to MongoDB!")
    print("="*100)
    
with open("./0330/all_entry.json", "r") as f:
    all_entry_dict = json.load(f)   
all_players_list = list(all_entry_dict.keys())
if 'all_entry_dict' not in st.session_state:
    st.session_state.all_entry_dict = {"all_entry_dict":all_entry_dict}
    print("="*100)
    print("load all_entry")
    print("="*100)
    
with open("./0330/eng_formation_dict.json", "r") as f:
    eng_formation_dict = json.load(f)   
eng_formation_list = list(eng_formation_dict.keys())
if 'eng_formation_dict' not in st.session_state:
    st.session_state.eng_formation_dict = {"eng_formation_dict":eng_formation_dict}
    print("="*100)
    print("load eng_formation")
    print("="*100)


if 'game_info' not in st.session_state:
    st.session_state['game_info'] = {}
if 'squad_info' not in st.session_state:
    st.session_state['squad_info'] = {}
if 'formation_info' not in st.session_state:
    st.session_state['formation_info'] = {}    

st.title("SOUTH_MAKER")


    
with st.expander('**1️⃣ 경기 정보 입력**'):
    st.divider()
    date = st.date_input("**경기 날짜**")
    st.write("")
    start_time = st.time_input("**경기 시간**", datetime.time(9,00), step=datetime.timedelta(minutes = 30))
    st.write("")
    location = st.text_input("**경기 장소**")
    if location:
        st.page_link(f"https://map.naver.com/p/search/{location}?c=15.00,0,0,0,dh", label="구장찾기🚙🚗🚓", icon="🏁")
    st.divider()
    st.write("")
    opposing_team = st.text_input("**상대팀 명**")
    
    st.session_state['game_info']['date'] = date
    st.session_state['game_info']['start_time'] = start_time
    st.session_state['game_info']['location'] = location
    st.session_state['game_info']['opposing_team'] = opposing_team
    
with st.expander('**2️⃣ 스쿼드 입력**'):
    st.divider()
    players = st.multiselect("**참가 인원**", all_players_list)
    st.session_state['squad_info']['players'] = players
    if st.session_state['squad_info']['players']:
        entry_df = pd.DataFrame([{"선수명":p, "주포지션":all_entry_dict[p]["주포지션"], "부포지션":all_entry_dict[p]["부포지션"]} for p in players], index = [idx+1 for idx in range(len(players))])
        edited_entry_df = st.data_editor(entry_df, use_container_width=True)
        find_sub_pos_series = entry_df['주포지션'] + ","+ entry_df['부포지션'].apply(lambda x : ",".join(x))
        
        st.write("")
        st.write("**스쿼드 분석**")
        
        main_pos_list = []
        sub_pos_list = []
        for i in ['GK','CB', 'WB', 'CM', 'WM', 'CF', 'WF']:
            main_pos_list.append((entry_df['주포지션'] == i).sum()) 
            sub_pos_list.append((find_sub_pos_series.apply(lambda x : i in x)).sum())
            
        
        tab1, tab2 = st.tabs(["주포지션", "부포지션 포함"])

        with tab1:
            chart_data_tab1= pd.DataFrame({"포지션": ['1.골키퍼', '2.수비수', '3.미드필더', '4.공격수'], "중앙": main_pos_list[:4], "윙": [0] + main_pos_list[4:]})
            st.bar_chart(chart_data_tab1, x="포지션", y=["중앙", "윙"], color=["#FF0000", "#0000FF"])
            st.write(f"전체인원 : {len(entry_df)}명")
            for idx in range(4):
                st.caption(f"{chart_data_tab1['포지션'][idx]}")
                if idx == 0:
                    mini_df = pd.DataFrame([main_pos_list[idx]], columns=['총원'])
                    edited_entry_df = st.dataframe(mini_df, use_container_width=True, hide_index=True)
                else:
                    mini_df = pd.DataFrame([[main_pos_list[idx]+main_pos_list[idx+3],main_pos_list[idx],main_pos_list[idx+3]]], columns=['총원','중앙', '윙'])
                    edited_entry_df = st.dataframe(mini_df, use_container_width=True, hide_index=True)
            
        with tab2:
            chart_data_tab2= pd.DataFrame({"포지션": ['1.골키퍼', '2.수비수', '3.미드필더', '4.공격수'], "중앙": sub_pos_list[:4], "윙": [0] + sub_pos_list[4:]})
            st.bar_chart(chart_data_tab2, x="포지션", y=["중앙", "윙"], color=["#FF0000", "#0000FF"])
            st.write(f"전체인원 : {len(entry_df)}명")
            for idx in range(4):
                st.caption(f"{chart_data_tab1['포지션'][idx]}")
                if idx == 0:
                    mini_df = pd.DataFrame([sub_pos_list[idx]], columns=['총원'])
                    edited_entry_df = st.dataframe(mini_df, use_container_width=True, hide_index=True)
                else:
                    mini_df = pd.DataFrame([[sub_pos_list[idx]+sub_pos_list[idx+3],sub_pos_list[idx],sub_pos_list[idx+3]]], columns=['총원','중앙', '윙'])
                    edited_entry_df = st.dataframe(mini_df, use_container_width=True, hide_index=True)


with st.expander('**3️⃣ 포메이션 입력**'):
    st.divider()
    formation1 = st.selectbox('**1쿼터 포메이션**',eng_formation_list, key="formation1")
    formation2 = st.selectbox('**2쿼터 포메이션**',eng_formation_list, key="formation2")
    formation3 = st.selectbox('**3쿼터 포메이션**',eng_formation_list, key="formation3")
    formation4 = st.selectbox('**4쿼터 포메이션**',eng_formation_list, key="formation4")
    st.session_state['formation_info']['formation'] = [formation1, formation2, formation3, formation4]
    
    if "선택" not in st.session_state['formation_info']['formation']:
        tab1, tab2, tab3, tab4 = st.tabs(["1쿼터", "2쿼터", "3쿼터", "4쿼터"])
        
        with tab1:
            st.write("tab1")
        with tab2:
            st.write("tab2")
        with tab3:
            st.write("tab3")
        with tab4:
            st.write("tab4")
    
    




with st.sidebar:
    st.write(st.session_state['game_info'])
    st.write(st.session_state['squad_info'])
    st.write(st.session_state['formation_info'])
    





























###################################################################################################


    
if st.button('깃허브에 커밋 & 푸시하기'):
    # 현재 시간을 커밋 메시지로 사용합니다.
    commit_message = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        subprocess.run(["git", "add", "."], check=True, stderr=subprocess.PIPE)
        subprocess.run(["git", "commit", "-m", commit_message], check=True, stderr=subprocess.PIPE)
        subprocess.run(["git", "push"], check=True, stderr=subprocess.PIPE)
        st.success('깃허브에 성공적으로 커밋 & 푸시되었습니다.')
    except subprocess.CalledProcessError as e:
        st.error(f'명령어 실행 중 오류가 발생했습니다: {e}')

