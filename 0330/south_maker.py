import matplotlib.pyplot as plt
from matplotlib.patches import Circle
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
import copy

from pymongo.mongo_client import MongoClient

st.set_page_config(layout="wide")

@st.cache_data
def fontRegistered():
    font_dirs = [os.getcwd() + '/customFonts']
    font_files = fm.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    fm._load_fontmanager(try_read_cache=False)
    
fontRegistered()
plt.rc('font', family='NanumGothic')

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
for_dot_position = copy.deepcopy(eng_formation_dict)
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
        entry_df = pd.DataFrame([{"선수명":p, "주포지션":all_entry_dict[p]["주포지션"], "부포지션":','.join(all_entry_dict[p]["부포지션"])} for p in players], index = [idx+1 for idx in range(len(players))])
        edited_entry_df = st.data_editor(entry_df, use_container_width=True,
                                         column_config={
                                            "주포지션": st.column_config.TextColumn(
                                                validate='^(GK|CB|WB|CM|WM|CF|WF)$'
                                            ), 
                                            "부포지션": st.column_config.TextColumn(
                                                validate='^(GK|CB|WB|CM|WM|CF|WF)(,(GK|CB|WB|CM|WM|CF|WF))*$'
                                            )}, height=int(35.2*(len(entry_df)+1)))
        find_sub_pos_series = edited_entry_df['주포지션'] + ","+ edited_entry_df['부포지션']
        st.session_state['squad_info']['players'] = json.loads(edited_entry_df.to_json(orient='records'))
        st.write("")
        
        main_pos_list = []
        sub_pos_list = []
        for i in ['GK','CB', 'CM', 'CF', 'WB', 'WM', 'WF']:
            main_pos_list.append((edited_entry_df['주포지션'] == i).sum()) 
            sub_pos_list.append((find_sub_pos_series.apply(lambda x : i in x)).sum())
        

        st.write("**스쿼드 분석**")
        tab1, tab2 = st.tabs(["**▪주포지션▪**", "**▪부포지션 포함▪**"])
        with tab1:
            chart_data_tab1= pd.DataFrame({"포지션": ['1.골키퍼', '2.수비수', '3.미드필더', '4.공격수'], "중앙": main_pos_list[:4], "윙": [0] + main_pos_list[4:]})
            st.bar_chart(chart_data_tab1, x="포지션", y=["중앙", "윙"], color=["#FF0000", "#0000FF"], use_container_width=True)
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
            st.bar_chart(chart_data_tab2, x="포지션", y=["중앙", "윙"], color=["#FF0000", "#0000FF"], use_container_width=True)
            for idx in range(4):
                st.caption(f"{chart_data_tab1['포지션'][idx]}")
                if idx == 0:
                    mini_df = pd.DataFrame([sub_pos_list[idx]], columns=['총원'])
                    edited_entry_df = st.dataframe(mini_df, use_container_width=True, hide_index=True)
                else:
                    mini_df = pd.DataFrame([[sub_pos_list[idx]+sub_pos_list[idx+3],sub_pos_list[idx],sub_pos_list[idx+3]]], columns=['총원','중앙', '윙'])
                    edited_entry_df = st.dataframe(mini_df, use_container_width=True, hide_index=True)

        
        
        
if (len(players) > 0) and (len(players) < 11):
    st.info("**\*notice**\n\n아직 스쿼드가 11명이 되지않았습니다. \n\n최소 11명이 되어야 다음 단계 진행이 가능합니다.")

if len(players) >= 11:
    with st.expander('**3️⃣ 포메이션 입력**'):
        st.divider()
        formation1 = st.selectbox('**1쿼터 포메이션**',eng_formation_list, key="formation1")
        formation2 = st.selectbox('**2쿼터 포메이션**',eng_formation_list, key="formation2")
        formation3 = st.selectbox('**3쿼터 포메이션**',eng_formation_list, key="formation3")
        formation4 = st.selectbox('**4쿼터 포메이션**',eng_formation_list, key="formation4")
        st.session_state['formation_info']['formation'] = {"1q": formation1, "2q": formation2, "3q": formation3, "4q": formation4}
        edited_entry_df_copy = pd.DataFrame(st.session_state['squad_info']['players'])
        
        if "선택" not in list(st.session_state['formation_info']['formation'].values()):
            st.divider()
            st.write("**쿼터 수 분석**")
            st.markdown('<span style="font-style:italic; font-size:15px;">* 주포지션을 기준으로 가장 공평하게 나눈 쿼터 수 입니다.</span>', unsafe_allow_html=True)
            gk_count = (edited_entry_df_copy['주포지션'] == 'GK').sum()
            gk_quarter = 4 if gk_count == 0 else 4/gk_count
            except_gk_count = len(edited_entry_df_copy) - (edited_entry_df_copy['주포지션'] == 'GK').sum()
            except_gk_quarter = 44 if gk_count == 0 else 40
            
            if len(players) >= 11:
                if gk_count > 0:
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("전체인원", f"총 {len(edited_entry_df_copy)}명", "")
                    col2.metric("골키퍼", f"{gk_count}명", f"{int(gk_quarter)}쿼터")
                    col3.metric("필드", f"{except_gk_count- int(except_gk_quarter%except_gk_count)}명", f"{int(except_gk_quarter/except_gk_count)}쿼터")
                    if int(except_gk_quarter/except_gk_count) != 4:
                        col4.metric("필드", f"{int(except_gk_quarter%except_gk_count)}명", f"{int(except_gk_quarter/except_gk_count)+1}쿼터")
                else:
                    col1, col2, col3 = st.columns(3)
                    col1.metric("전체인원", f"총 {len(edited_entry_df_copy)}명", f"골키퍼:{gk_count}명")
                    col2.metric("필드", f"{except_gk_count- int(except_gk_quarter%except_gk_count)}명", f"{int(except_gk_quarter/except_gk_count)}쿼터")
                    if int(except_gk_quarter/except_gk_count) != 4:
                        col3.metric("필드", f"{int(except_gk_quarter%except_gk_count)}명", f"{int(except_gk_quarter/except_gk_count)+1}쿼터")
        
            st.write("")
            formation_list = list(st.session_state['formation_info']['formation'].values())
            tab1, tab2, tab3, tab4 = st.tabs(["**▪1쿼터▪**", "**▪2쿼터▪**", "**▪3쿼터▪**", "**▪4쿼터▪**"])
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
                            markdown_formation[horizon_cont_count-1] = f'<span style="color:blue; font-weight:bold; font-size:25px;">{markdown_formation[horizon_cont_count-1]}</span>'
                            st.markdown(f'**{"-".join(markdown_formation[::-1])}**', unsafe_allow_html=True)

                            cols_num = splited_formation[(horizon_cont_count)*(-1)]
                            placeholder_list = st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1]
                            select_element_list = edited_entry_df_copy['선수명'] + ": " + edited_entry_df_copy['주포지션'] + "✅  " + edited_entry_df_copy['부포지션'] + "🔻"
                            if cols_num in ['2','4']:
                                cols1, cols2, cols3, cols4 = st.columns(4)
                                if cols_num == '2':
                                    if (splited_formation == ['4','2','2','2']) & ((horizon_cont_count)*(-1) == -2):
                                        cols_num2_1 = cols1.selectbox('tmp', select_element_list, key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 1", label_visibility="collapsed",index=None,placeholder="L"+placeholder_list[0])
                                        cols_num2_2 = cols4.selectbox('tmp', select_element_list, key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 2", label_visibility="collapsed",index=None,placeholder="R"+placeholder_list[1])
                                    else:
                                        cols_num2_1 = cols2.selectbox('tmp', select_element_list, key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 3", label_visibility="collapsed",index=None,placeholder=placeholder_list[0])
                                        cols_num2_2 = cols3.selectbox('tmp', select_element_list, key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 4", label_visibility="collapsed",index=None,placeholder=placeholder_list[1])
                                    if cols_num2_1:
                                        update_name = cols_num2_1.split(":")[0]
                                        st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1] = [update_name,
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][1]]
                                    if cols_num2_2:
                                        update_name = cols_num2_2.split(":")[0]
                                        st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1] = [st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][0], 
                                                                                                                 update_name]
                                else:
                                    cols_num4_1 = cols1.selectbox('tmp',select_element_list, key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 1", label_visibility="collapsed",index=None,placeholder="L"+placeholder_list[0])
                                    cols_num4_2 = cols2.selectbox('tmp',select_element_list, key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 2", label_visibility="collapsed",index=None,placeholder=placeholder_list[1])
                                    cols_num4_3 = cols3.selectbox('tmp',select_element_list, key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 3", label_visibility="collapsed",index=None,placeholder=placeholder_list[2])
                                    cols_num4_4 = cols4.selectbox('tmp',select_element_list, key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 4", label_visibility="collapsed",index=None,placeholder="R"+placeholder_list[3])
                                    if cols_num4_1:
                                        update_name = cols_num4_1.split(":")[0]
                                        st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1] = [update_name,
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][1],
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][2],
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][3]]
                                    if cols_num4_2:
                                        update_name = cols_num4_2.split(":")[0]
                                        st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1] = [st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][0], 
                                                                                                                update_name,
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][2],
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][3]]
                                    if cols_num4_3:
                                        update_name = cols_num4_3.split(":")[0]
                                        st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1] = [st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][0], 
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][1],
                                                                                                                update_name,
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][3]]
                                    if cols_num4_4:
                                        update_name = cols_num4_4.split(":")[0]
                                        st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1] = [st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][0], 
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][1],
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][2],
                                                                                                                update_name]
                            if cols_num in ['1','3','5']:
                                cols1, cols2, cols3, cols4, cols5 = st.columns(5)
                                if cols_num == '1':
                                    cols_num1_1 = cols3.selectbox('tmp',select_element_list, key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 3", label_visibility="collapsed",index=None,placeholder=placeholder_list[0])
                                    if cols_num1_1:
                                        update_name = cols_num1_1.split(":")[0]
                                        st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1] = [update_name]
                                if cols_num == '3':
                                    cols_num3_1 = cols2.selectbox('tmp',select_element_list, key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 2", label_visibility="collapsed",index=None,placeholder="L"+placeholder_list[0])
                                    cols_num3_2 = cols3.selectbox('tmp',select_element_list, key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 3", label_visibility="collapsed",index=None,placeholder=placeholder_list[1])
                                    cols_num3_3 = cols4.selectbox('tmp',select_element_list, key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 4", label_visibility="collapsed",index=None,placeholder="R"+placeholder_list[2])
                                    if cols_num3_1:
                                        update_name = cols_num3_1.split(":")[0]
                                        st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1] = [update_name,
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][1], 
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][2]]
                                    if cols_num3_2:
                                        update_name = cols_num3_2.split(":")[0]
                                        st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1] = [st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][0],
                                                                                                                update_name, 
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][2]]
                                    if cols_num3_3:
                                        update_name = cols_num3_3.split(":")[0]
                                        st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1] = [st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][0],
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][1],
                                                                                                                update_name]
                                if cols_num == '5':
                                    cols_num5_1 = cols1.selectbox('tmp',select_element_list, key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 1", label_visibility="collapsed",index=None,placeholder="L"+placeholder_list[0])
                                    cols_num5_2 = cols2.selectbox('tmp',select_element_list, key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 2", label_visibility="collapsed",index=None,placeholder=placeholder_list[1])
                                    cols_num5_3 = cols3.selectbox('tmp',select_element_list, key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 3", label_visibility="collapsed",index=None,placeholder=placeholder_list[2])
                                    cols_num5_4 = cols4.selectbox('tmp',select_element_list, key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 4", label_visibility="collapsed",index=None,placeholder=placeholder_list[3])
                                    cols_num5_5 = cols5.selectbox('tmp',select_element_list, key=f"selected_key : tab{tdx+1}, container{horizon_cont_count}, cols_num{cols_num}, 5", label_visibility="collapsed",index=None,placeholder="R"+placeholder_list[4])
                                    if cols_num5_1:
                                        update_name = cols_num5_1.split(":")[0]
                                        st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1] = [update_name,
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][1],
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][2],
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][3],
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][4]]
                                    if cols_num5_2:
                                        update_name = cols_num5_2.split(":")[0]
                                        st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1] = [st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][0],
                                                                                                                update_name,
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][2],
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][3],
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][4]]
                                    if cols_num5_3:
                                        update_name = cols_num5_3.split(":")[0]
                                        st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1] = [st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][0],
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][1],
                                                                                                                update_name,
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][3],
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][4]]
                                    if cols_num5_4:
                                        update_name = cols_num5_4.split(":")[0]
                                        st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1] = [st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][0],
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][1],
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][2],
                                                                                                                update_name,
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][4]]
                                    if cols_num5_5:
                                        update_name = cols_num5_5.split(":")[0]
                                        st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1] = [st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][0],
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][1],
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][2],
                                                                                                                st.session_state['formation_info'][f'{tdx+1}q'][horizon_cont_count-1][3],
                                                                                                                update_name]
                                
                    keep_container = st.container(border=True)
                    with keep_container:
                        for_session_list_GK = []
                        st.markdown('<span style="color:blue; font-weight:bold; font-size:25px;">GK</span>', unsafe_allow_html=True)
                        cols1, cols2, cols3, cols4, cols5 = st.columns(5)
                        for_session_list_GK = cols3.selectbox('tmp',select_element_list, key=f"selected_key : GK_{tdx}", label_visibility="collapsed",index=None,placeholder="GK")
                        if for_session_list_GK:
                            update_name = for_session_list_GK.split(":")[0]
                            st.session_state['formation_info'][f'{tdx+1}q'][-1] = [update_name]

    




with st.sidebar:
    # st.write(st.session_state['game_info'])
    # st.write(st.session_state['squad_info'])
    # st.write(st.session_state['formation_info'])
    
    if (len(players) >= 11):
        formation_list = list(st.session_state['formation_info']['formation'].values())
        
        if '선택' not in formation_list:
            with st.expander("**🔽 쿼터 확인 데이터**"):
                real_name_series = select_element_list.apply(lambda x: x.split(":")[0])
                quarter_table = pd.concat([real_name_series,pd.DataFrame([[0,"","","",""]]*len(select_element_list))], axis = 1)
                quarter_table.columns = ["이름", "쿼터 수", "1Q", "2Q", "3Q", "4Q"]
                quarter_table.index = [idx+1 for idx in range(len(players))]
                
                f_dict = copy.deepcopy(st.session_state['formation_info'])
                
                for qdx, quarter in enumerate(f_dict['formation']):
                    origin_position_list = [minis for mini_list in for_dot_position[f_dict['formation'][quarter]][::-1] + [['GK']] for minis in mini_list]
                    include_chk_list = [minis for mini_list in f_dict[quarter] for minis in mini_list]
                    for ndx, name in enumerate(include_chk_list):
                        if name in real_name_series.values:
                            quarter_table.loc[quarter_table['이름'] == name, f"{qdx+1}Q"] = origin_position_list[ndx]
                            quarter_table.loc[:, '쿼터 수'] = (quarter_table.loc[:, ['1Q','2Q','3Q','4Q']] != "").sum(axis = 1)
                
                t_quarter = quarter_table['쿼터 수'].sum()
                t_1q, t_2q, t_3q, t_4q = (quarter_table['1Q'] != "").sum(), (quarter_table['2Q'] != "").sum(), (quarter_table['3Q'] != "").sum(), (quarter_table['4Q'] != "").sum()
                
                total_df = pd.DataFrame([["총합",t_quarter, t_1q, t_2q, t_3q, t_4q]], columns=["이름", "쿼터 수", "1Q", "2Q", "3Q", "4Q"])
                final_quarter_table = pd.concat([total_df, quarter_table])
                
                st.dataframe(final_quarter_table, use_container_width=True, 
                            column_order= ("index", "이름", "쿼터 수", "1Q", "2Q", "3Q", "4Q"), 
                            hide_index = True,
                            height=int(35.2*(len(final_quarter_table)+1)))
            
            
            
            
            
            fig, ax = plt.subplots(figsize=(6, 8))
            
            graph_fig_dict = dict()
            scatter_horizon_dict = {4 : [16,12,8,4], 5 : [16,13,10,7,4]} 
            scatter_vertical_dict = {1 : [10], 2 : [8,12], 3 : [6,10,14], 4 : [4,8,12,16], 5 : [4,7,10,13,16]} 
            color_dict = {4 : ['red','#769bdb','orange','yellow'], 5 : ['red','#769bdb','#769bdb','orange','yellow']} 
            
            ground_gragh_list = [ground_gragh1, ground_gragh2, ground_gragh3, ground_gragh4] = \
                [st.expander("**1쿼터**"), st.expander("**2쿼터**"), st.expander("**3쿼터**"), st.expander("**4쿼터**")]
            for fdx, formation in enumerate(formation_list):
                with ground_gragh_list[fdx]:
                    graph_fig_dict[f"fig{fdx+1}"] = plt.figure(figsize=(7.5, 7.5))
                    plt.title(f"{fdx+1}쿼터\n", fontdict = {'fontsize': 16,'fontweight': 'bold'})
                    plt.gca().axes.xaxis.set_visible(False)
                    plt.gca().axes.yaxis.set_visible(False)
                    plt.gca().set_facecolor("#adc7b5")
                    plt.xlim(2, 18)
                    plt.ylim(2, 18)
                    
                    for i in range(2,17,2):
                        grass_color = "#0ceb55" if i%4 == 0 else "#0a5924"
                        plt.axhspan(i, i+2, color=grass_color, alpha=0.3) 
                            
                    plt.plot([2, 18], [10, 10], color='white', linewidth=2)
                    
                    plt.plot([8,8], [0,3], color='white', linewidth=2)
                    plt.plot([12,12], [0,3], color='white', linewidth=2)
                    plt.plot([8,12], [3,3], color='white', linewidth=2)
                    
                    plt.plot([8 ,8], [17,18], color='white', linewidth=2)
                    plt.plot([12 ,12], [17,18], color='white', linewidth=2)
                    plt.plot([8 ,12], [17,17], color='white', linewidth=2)
                    
                    circle = Circle((10, 10), 2, edgecolor='white', facecolor='none', linewidth=2)
                    plt.gcf().gca().add_artist(circle)
                    
                    marking_players = st.session_state['formation_info'][f'{fdx+1}q'][:]
                    
                    scatter_dot = formation.split("-")[::-1] + ['1']
                    horizon_coordinate = scatter_horizon_dict[len(scatter_dot)]
                    vertical_coordinate = [scatter_vertical_dict[int(i)] for i in scatter_dot]
                    dot_text_pos = for_dot_position[formation][::-1] + [['GK']]
                    color = color_dict[len(scatter_dot)]
                    if formation == '4-2-2-2': vertical_coordinate[1] = [4,16]
                    
                    for c, hc, vc_list, dt_list, mp_list in zip(color, horizon_coordinate, vertical_coordinate, dot_text_pos, marking_players):
                        for vc,dt,mp in zip(vc_list, dt_list, mp_list):
                            plt.scatter(vc, hc,s=30**2, color=c, alpha=1)
                            plt.text(vc, hc, dt, fontdict={'size': 14},  verticalalignment='center' , horizontalalignment='center', alpha=1)
                            if not dt == mp:
                                plt.text(vc, hc-1.1, mp, fontdict={'size': 18, 'fontweight': 'bold'},  verticalalignment='center' , horizontalalignment='center', alpha=1)
            
                    st.pyplot(graph_fig_dict[f"fig{fdx+1}"])
            # st.pyplot(graph_fig_dict['fig2'])
            # st.pyplot(graph_fig_dict['fig3'])
            # st.pyplot(graph_fig_dict['fig4'])
                
                



























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

