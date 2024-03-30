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

st.set_page_config(layout="wide")

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
    entry_df = pd.DataFrame()
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
    # if len(entry_df) < 11:
    #     st.error("스쿼드가 11명이 안됩니다.")
    #     st.stop()
    st.divider()
    formation1 = st.selectbox('**1쿼터 포메이션**',eng_formation_list, key="formation1")
    formation2 = st.selectbox('**2쿼터 포메이션**',eng_formation_list, key="formation2")
    formation3 = st.selectbox('**3쿼터 포메이션**',eng_formation_list, key="formation3")
    formation4 = st.selectbox('**4쿼터 포메이션**',eng_formation_list, key="formation4")
    st.session_state['formation_info']['formation'] = {"1q": formation1, "2q": formation2, "3q": formation3, "4q": formation4}
    
    if "선택" not in list(st.session_state['formation_info']['formation'].values()):
        formation_list = list(st.session_state['formation_info']['formation'].values())
        tab1, tab2, tab3, tab4 = st.tabs(["1쿼터", "2쿼터", "3쿼터", "4쿼터"])
        con_dict = {}
        
        for tdx, tab in enumerate([tab1, tab2, tab3, tab4]):
            with tab:
                con_dict[tab] = {}
                splited_formation = formation_list[tdx].split("-")
                st.session_state['formation_info'][f'{tdx+1}q'] = eng_formation_dict[formation_list[tdx]][::-1] + [["GK"]]
                for horizon_cont in range(len(splited_formation)):
                    horizon_cont_count = horizon_cont+1
                    con_dict[tab]['formation'] = splited_formation
                    con_dict[tab][f'container{horizon_cont_count}'] = st.container(border=True)
                    with con_dict[tab][f'container{horizon_cont_count}']:
                        markdown_formation = splited_formation[::-1]
                        markdown_formation[horizon_cont_count-1] = f'<span style="color:red; font-weight:bold; font-size:25px;">{markdown_formation[horizon_cont_count-1]}</span>'
                        st.markdown(f'**{"-".join(markdown_formation[::-1])}**', unsafe_allow_html=True)

                        cols_num = splited_formation[(horizon_cont_count)*(-1)]
                        placeholder_list = st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1]
                        if cols_num in ['2','4']:
                            cols1, cols2, cols3, cols4 = st.columns(4)
                            if cols_num == '2':
                                if (splited_formation == ['4','2','2','2']) & ((horizon_cont_count)*(-1) == -2):
                                    cols_num2_1 = cols1.multiselect('tmp', entry_df['선수명'], key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 1", label_visibility="collapsed",placeholder=placeholder_list[0])
                                    cols_num2_2 = cols4.multiselect('tmp', entry_df['선수명'], key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 2", label_visibility="collapsed",placeholder=placeholder_list[1])
                                else:
                                    cols_num2_1 = cols2.multiselect('tmp', entry_df['선수명'], key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 1", label_visibility="collapsed",placeholder=placeholder_list[0])
                                    cols_num2_2 = cols3.multiselect('tmp', entry_df['선수명'], key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 2", label_visibility="collapsed",placeholder=placeholder_list[1])
                                for_session_list = cols_num2_1+cols_num2_2
                            else:
                                cols_num4_1 = cols1.multiselect('tmp',entry_df['선수명'], key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 1", label_visibility="collapsed",placeholder=placeholder_list[0])
                                cols_num4_2 = cols2.multiselect('tmp',entry_df['선수명'], key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 2", label_visibility="collapsed",placeholder=placeholder_list[1])
                                cols_num4_3 = cols3.multiselect('tmp',entry_df['선수명'], key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 3", label_visibility="collapsed",placeholder=placeholder_list[2])
                                cols_num4_4 = cols4.multiselect('tmp',entry_df['선수명'], key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 4", label_visibility="collapsed",placeholder=placeholder_list[3])
                                for_session_list = cols_num4_1 + cols_num4_2 + cols_num4_3 + cols_num4_4 
                        if cols_num in ['1','3','5']:
                            cols1, cols2, cols3, cols4, cols5 = st.columns(5)
                            if cols_num == '1':
                                cols_num1_1 = cols3.multiselect('tmp',entry_df['선수명'], key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 3", label_visibility="collapsed",placeholder=placeholder_list[0])
                                for_session_list = cols_num1_1
                            if cols_num == '3':
                                cols_num3_1 = cols2.multiselect('tmp',entry_df['선수명'], key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 2", label_visibility="collapsed",placeholder=placeholder_list[0])
                                cols_num3_2 = cols3.multiselect('tmp',entry_df['선수명'], key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 3", label_visibility="collapsed",placeholder=placeholder_list[1])
                                cols_num3_3 = cols4.multiselect('tmp',entry_df['선수명'], key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 4", label_visibility="collapsed",placeholder=placeholder_list[2])
                                for_session_list = cols_num3_1 + cols_num3_2 + cols_num3_3
                            if cols_num == '5':
                                cols_num5_1 = cols1.multiselect('tmp',entry_df['선수명'], key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 1", label_visibility="collapsed",placeholder=placeholder_list[0])
                                cols_num5_2 = cols2.multiselect('tmp',entry_df['선수명'], key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 2", label_visibility="collapsed",placeholder=placeholder_list[1])
                                cols_num5_3 = cols3.multiselect('tmp',entry_df['선수명'], key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 3", label_visibility="collapsed",placeholder=placeholder_list[2])
                                cols_num5_4 = cols4.multiselect('tmp',entry_df['선수명'], key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 4", label_visibility="collapsed",placeholder=placeholder_list[3])
                                cols_num5_5 = cols5.multiselect('tmp',entry_df['선수명'], key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 5", label_visibility="collapsed",placeholder=placeholder_list[4])
                                for_session_list = cols_num5_1 + cols_num5_2 + cols_num5_3 + cols_num5_4 + cols_num5_5
                        st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1] = for_session_list
                        
                keep_container = st.container(border=True)
                with keep_container:
                    st.markdown('<span style="color:red; font-weight:bold; font-size:25px;">GK</span>', unsafe_allow_html=True)
                    cols1, cols2, cols3, cols4, cols5 = st.columns(5)
                    cols3.multiselect('tmp',entry_df['선수명'], key=f"selected_key : GK_{tdx}", label_visibility="collapsed",placeholder="GK")
            
                for idx in range(len(st.session_state['formation_info'][f'{tdx+1}q'])):
                    st.session_state['formation_info'][f'{tdx+1}q'][idx]
            




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

