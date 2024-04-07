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
import re
from find_positions import define_cols_containers
from collections import Counter

from pymongo.mongo_client import MongoClient

# st.set_page_config(layout="wide")

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
if 'duplicate_info' not in st.session_state:
    st.session_state['duplicate_info'] = {}  
    st.session_state['duplicate_info']['1q'] = []  
    st.session_state['duplicate_info']['2q'] = []  
    st.session_state['duplicate_info']['3q'] = []  
    st.session_state['duplicate_info']['4q'] = []  
if 'quarter_allocation_info' not in st.session_state:
    st.session_state['quarter_allocation_info'] = {} 
    st.session_state['quarter_allocation_info']['total'] = 0
    st.session_state['quarter_allocation_info']['stop_player_name_list_bool'] = False
    st.session_state['quarter_allocation_info']['stop_player_name_list'] = []
st.title("SOUTH_MAKER")


    
with st.expander('**1️⃣ 경기 정보 입력**'):
    finally_no_errors = False
    st.divider()
    date = st.date_input("**경기 날짜**")
    st.write("")
    # start_time = st.time_input("**경기 시간**", datetime.time(9,00), step=datetime.timedelta(minutes = 30))
    start_time = st.slider("**경기 시작 시간**", 6, 22,9)
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
    finally_no_errors = False
    st.divider()
    players = st.multiselect("**참가 인원**", all_players_list)
    st.session_state['squad_info']['players'] = players
    entry_df = pd.DataFrame()
    if st.session_state['squad_info']['players']:
        entry_df = pd.DataFrame([{"선수명":p, "배정쿼터수": 1, "주포지션":all_entry_dict[p]["주포지션"], "부포지션":','.join(all_entry_dict[p]["부포지션"])} for p in players], index = [idx+1 for idx in range(len(players))])
        edited_entry_df = st.data_editor(entry_df, use_container_width=True,
                                         column_config={
                                            "배정쿼터수": st.column_config.NumberColumn(
                                                min_value=1,
                                                max_value=4,
                                                step=1,
                                            ),
                                            "주포지션": st.column_config.TextColumn(
                                                validate='^(GK|CB|WB|CM|WM|CF|WF)$'
                                            ), 
                                            "부포지션": st.column_config.TextColumn(
                                                validate='^(GK|CB|WB|CM|WM|CF|WF)(,(GK|CB|WB|CM|WM|CF|WF))*$'
                                            )}, height=int(35.2*(len(entry_df)+1)))
        find_sub_pos_series = edited_entry_df['주포지션'] + ","+ edited_entry_df['부포지션']
        st.session_state['squad_info']['players'] = json.loads(edited_entry_df.to_json(orient='records'))
        
        if len(players) >= 11:
            st.write("**위치 이동**")
            st.markdown('<span style="color:blue; font-style:italic; font-size:15px;">* 주포지션을 기준으로 가장 공평하게 나눈 쿼터 수 입니다.</span>', unsafe_allow_html=True)
            gk_count = (edited_entry_df['주포지션'] == 'GK').sum()
            gk_quarter = 4 if gk_count == 0 else 4/gk_count
            except_gk_count = len(edited_entry_df) - (edited_entry_df['주포지션'] == 'GK').sum()
            except_gk_quarter = 44 if gk_count == 0 else 40
            if gk_count > 0:
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("전체인원", f"총 {len(edited_entry_df)}명", "")
                col2.metric("골키퍼", f"{gk_count}명", f"{int(gk_quarter)}쿼터")
                col3.metric("필드", f"{except_gk_count- int(except_gk_quarter%except_gk_count)}명", f"{int(except_gk_quarter/except_gk_count)}쿼터")
                if int(except_gk_quarter/except_gk_count) != 4:
                    col4.metric("필드", f"{int(except_gk_quarter%except_gk_count)}명", f"{int(except_gk_quarter/except_gk_count)+1}쿼터")
            else:
                col1, col2, col3 = st.columns(3)
                col1.metric("전체인원", f"총 {len(edited_entry_df)}명", f"골키퍼:{gk_count}명")
                col2.metric("필드", f"{except_gk_count- int(except_gk_quarter%except_gk_count)}명", f"{int(except_gk_quarter/except_gk_count)}쿼터")
                if int(except_gk_quarter/except_gk_count) != 4:
                    col3.metric("필드", f"{int(except_gk_quarter%except_gk_count)}명", f"{int(except_gk_quarter/except_gk_count)+1}쿼터")
            
            st.divider()
            allocated_quarters_num = edited_entry_df['배정쿼터수'].sum()
            allocated_quarters_players = (edited_entry_df['배정쿼터수'] != 0).sum()
            quarters_for_metric = list(edited_entry_df['배정쿼터수'].unique())
            quarters_for_metric.sort()
            if 0 in quarters_for_metric: quarters_for_metric.remove(0)
            
            columns = st.columns(len(quarters_for_metric)+1)
            columns[0].metric(label="현재 배정된 쿼터 수", value=f"{allocated_quarters_num}/44", delta=f"{allocated_quarters_players}명")
            for col,qfm in zip(columns[1:], quarters_for_metric):
                quarter_play = (edited_entry_df['배정쿼터수'] == qfm).sum()
                col.metric(label=" ", value=f"{quarter_play}명", delta=f"{qfm}쿼터")    
                

                
                
            st.divider()
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
                        edited_entry_df_mini = st.dataframe(mini_df, use_container_width=True, hide_index=True)
                    else:
                        mini_df = pd.DataFrame([[main_pos_list[idx]+main_pos_list[idx+3],main_pos_list[idx],main_pos_list[idx+3]]], columns=['총원','중앙', '윙'])
                        edited_entry_df_mini = st.dataframe(mini_df, use_container_width=True, hide_index=True)
                
            with tab2:
                chart_data_tab2= pd.DataFrame({"포지션": ['1.골키퍼', '2.수비수', '3.미드필더', '4.공격수'], "중앙": sub_pos_list[:4], "윙": [0] + sub_pos_list[4:]})
                st.bar_chart(chart_data_tab2, x="포지션", y=["중앙", "윙"], color=["#FF0000", "#0000FF"], use_container_width=True)
                for idx in range(4):
                    st.caption(f"{chart_data_tab1['포지션'][idx]}")
                    if idx == 0:
                        mini_df = pd.DataFrame([sub_pos_list[idx]], columns=['총원'])
                        edited_entry_df_mini = st.dataframe(mini_df, use_container_width=True, hide_index=True)
                    else:
                        mini_df = pd.DataFrame([[sub_pos_list[idx]+sub_pos_list[idx+3],sub_pos_list[idx],sub_pos_list[idx+3]]], columns=['총원','중앙', '윙'])
                        edited_entry_df_mini = st.dataframe(mini_df, use_container_width=True, hide_index=True)

            if allocated_quarters_num < 44:
                st.success("쿼터 수를 맞춰주세요.")
                st.stop()
                
            if allocated_quarters_num > 44:
                st.error("쿼터 수를 초과했습니다.")
                st.stop()
        
        
if (len(players) > 0) and (len(players) < 11):
    st.info("**\*notice**\n\n아직 스쿼드가 11명이 되지않았습니다. \n\n최소 11명이 되어야 다음 단계 진행이 가능합니다.")

if len(players) >= 11:
    expander3 = st.expander('**3️⃣ 포메이션 입력**')
    with expander3:
        finally_no_errors = False
        st.divider()
        formation1 = st.selectbox('**1쿼터 포메이션**',eng_formation_list, key="formation1")
        formation2 = st.selectbox('**2쿼터 포메이션**',eng_formation_list, key="formation2")
        formation3 = st.selectbox('**3쿼터 포메이션**',eng_formation_list, key="formation3")
        formation4 = st.selectbox('**4쿼터 포메이션**',eng_formation_list, key="formation4")
        st.session_state['formation_info']['formation'] = {"1q": formation1, "2q": formation2, "3q": formation3, "4q": formation4}
        edited_entry_df_copy = pd.DataFrame(st.session_state['squad_info']['players'])
        if "선택" not in list(st.session_state['formation_info']['formation'].values()):
            # 선수 목록 초기화
            # players = [f'Player {i}' for i in range(1, 22)]
            players = edited_entry_df_copy['선수명']

            # 선택된 선수 정보를 담을 세션 상태 초기화
            if "tab_selected_players" not in st.session_state:
                st.session_state["tab_selected_players"] = {f"tab{idx+1}": {} for idx in range(4)}

            # 탭 생성
            tabs = st.tabs(["**▪1쿼터▪**", "**▪2쿼터▪**", "**▪3쿼터▪**", "**▪4쿼터▪**"])

            # 모든 탭에서 선택된 선수들의 목록 생성 및 선수별 총 선택 횟수 계산
            all_selected_players = []
            for tab_players in st.session_state["tab_selected_players"].values():
                all_selected_players.extend([player for player in tab_players.values() if player != ''])
            total_selection_counts = Counter(all_selected_players)

            # 각 탭별로 선수 선택 로직 처리
            for tdx, tab in enumerate(tabs):
                tab_key = f"tab{tdx+1}"
                quarter = st.session_state['formation_info']['formation'][f'{tdx+1}q']
                with tab:
                    cols_list = define_cols_containers(quarter)
                    placeholder_list = [j for i in for_dot_position[quarter][::-1] for j in i]
                    
                    for i, cols in zip(range(11), cols_list):
                        unique_key = f"{tab_key}_pos{i+1}"
                        t1 = st.session_state["tab_selected_players"][tab_key].copy()
                        current_tab_players = st.session_state["tab_selected_players"][tab_key].values()

                        # 현재 탭에서 이미 선택된 선수를 제외하고, 다른 탭에서 2번 이상 선택된 선수를 제외한 옵션 목록 생성
                        available_options = [''] + [player for player in players if player not in total_selection_counts or (total_selection_counts[player] < edited_entry_df_copy[edited_entry_df_copy['선수명'] == player]['배정쿼터수'].values[0] and player not in current_tab_players) or player == st.session_state["tab_selected_players"][tab_key].get(unique_key, '')]

                        selected_player = cols.selectbox(
                            placeholder_list[i], options=available_options, key=unique_key, index=available_options.index(st.session_state["tab_selected_players"][tab_key].get(unique_key, ''))
                        )

                        # 선택된 선수 정보 업데이트
                        if selected_player != t1.get(unique_key, '') or (selected_player == '' and t1.get(unique_key, '') != ''):
                            st.session_state["tab_selected_players"][tab_key][unique_key] = selected_player
                            st.rerun()
            # 선택된 플레이어 출력
            for tab_key, players in st.session_state["tab_selected_players"].items():
                st.write(f"{tab_key.replace('tab', 'Quarter ')}:")
                for position, player in players.items():
                    st.write(f"{position.split('_')[-1]}: {player}")



with st.sidebar:
    finally_no_errors = False
    # st.write(st.session_state['game_info'])
    # st.write(st.session_state['squad_info'])
    # st.write(st.session_state['formation_info'])
    st.write(st.session_state["tab_selected_players"])
    # st.write(st.session_state['duplicate_info'])
    
    # is_all_empty = all(value == [] for value in st.session_state['duplicate_info'].values())
    # if (len(players) >= 11) and (is_all_empty) and (allocated_quarters_num == 44):
    formation_list = list(st.session_state['formation_info']['formation'].values())
    
    if '선택' not in formation_list:
        st.subheader("FORMATION")
        fig, ax = plt.subplots(figsize=(6, 8))
        
        graph_fig_dict = dict()
        scatter_horizon_dict = {4 : [16,12,8,4], 5 : [16,13,10,7,4]} 
        scatter_vertical_dict = {1 : [10], 2 : [8,12], 3 : [6,10,14], 4 : [4,8,12,16], 5 : [4,7,10,13,16]} 
        color_dict = {4 : ['red','#769bdb','orange','yellow'], 5 : ['red','#769bdb','#769bdb','orange','yellow']} 
        
        ground_gragh_list = [ground_gragh1, ground_gragh2, ground_gragh3, ground_gragh4] = \
            [st.expander("**▪1쿼터▪**"), st.expander("**▪2쿼터▪**"), st.expander("**▪3쿼터▪**"), st.expander("**▪4쿼터▪**")]
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
                
                # marking_players = st.session_state['formation_info'][f'{fdx+1}q'][:]
                marking_players = list(st.session_state['tab_selected_players'][f'tab{fdx+1}'].values)[:]
                
                scatter_dot = formation.split("-")[::-1] + ['1']
                horizon_coordinate = scatter_horizon_dict[len(scatter_dot)]
                vertical_coordinate = [scatter_vertical_dict[int(i)] for i in scatter_dot]
                dot_text_pos = for_dot_position[formation][::-1] + [['GK']]
                color = color_dict[len(scatter_dot)]
                if formation == '4-2-2-2': vertical_coordinate[1] = [4,16]
                print(horizon_coordinate)
                for c, hc, vc_list, dt_list, mp_list in zip(color, horizon_coordinate, vertical_coordinate, dot_text_pos, marking_players):
                    for vc,dt,mp in zip(vc_list, dt_list, mp_list):
                        plt.scatter(vc, hc,s=30**2, color=c, alpha=1)
                        plt.text(vc, hc, dt, fontdict={'size': 14},  verticalalignment='center' , horizontalalignment='center', alpha=1)
                        if not dt == mp:
                            plt.text(vc, hc-1.1, mp, fontdict={'size': 18, 'fontweight': 'bold'},  verticalalignment='center' , horizontalalignment='center', alpha=1)
        
                st.pyplot(graph_fig_dict[f"fig{fdx+1}"])
                    
#         # finally_no_errors = True
        
#             st.divider()
#             # with st.expander("**🔽 쿼터 확인 데이터**"):
#             final_quarter_allocate_table = edited_entry_df.reset_index(drop=True)
#             real_name_series = final_quarter_allocate_table['선수명']
#             quarter_table = pd.concat([final_quarter_allocate_table.iloc[:, :2],pd.DataFrame([["","","",""]]*len(final_quarter_allocate_table))], axis = 1)
#             quarter_table.columns = ["이름", "남은 쿼터 수", "1Q", "2Q", "3Q", "4Q"]
#             quarter_table.index = [idx+1 for idx in range(len(players))]
            
#             f_dict = copy.deepcopy(st.session_state['formation_info'])
            
#             for qdx, quarter in enumerate(f_dict['formation']):
#                 origin_position_list = [minis for mini_list in for_dot_position[f_dict['formation'][quarter]][::-1] + [['GK']] for minis in mini_list]
#                 include_chk_list = [minis for mini_list in f_dict[quarter] for minis in mini_list]
#                 for ndx, name in enumerate(include_chk_list):
#                     if name in real_name_series.values:
#                         quarter_table.loc[quarter_table['이름'] == name, f"{qdx+1}Q"] = origin_position_list[ndx]
#                         quarter_table.loc[quarter_table['이름'] == name, '남은 쿼터 수'] -= 1
            
#             t_quarter = quarter_table['남은 쿼터 수'].sum()
#             t_1q, t_2q, t_3q, t_4q = (quarter_table['1Q'] != "").sum(), (quarter_table['2Q'] != "").sum(), (quarter_table['3Q'] != "").sum(), (quarter_table['4Q'] != "").sum()
            
#             total_df = pd.DataFrame([["총합",t_quarter, str(t_1q), str(t_2q), str(t_3q), str(t_4q)]], columns=["이름", "남은 쿼터 수", "1Q", "2Q", "3Q", "4Q"])
#             final_quarter_table = pd.concat([total_df, quarter_table])
#             final_quarter_table['남은 쿼터 수'] = final_quarter_table['남은 쿼터 수'].astype(str)
#             slash_quarters = pd.concat([pd.Series(['44']), final_quarter_allocate_table['배정쿼터수'].astype(str)]).reset_index(drop=True)
#             final_quarter_table.loc[:, '남은 쿼터 수'] = final_quarter_table.loc[:, '남은 쿼터 수'].astype('str') + '/'+  slash_quarters
            
#             st.dataframe(final_quarter_table, use_container_width=True, 
#                         column_order= ("index", "이름", "남은 쿼터 수", "1Q", "2Q", "3Q", "4Q"), 
#                         hide_index = True,
#                         height=int(35.2*(len(final_quarter_table)+1)))
        
#     else:
#         if len(players) >= 11:
#             if (allocated_quarters_num == 44):
#                 duplicate_problem_list = [f"{key[0]}쿼터" for key, value in st.session_state['duplicate_info'].items() if value != []]
#                 st.error(f"**\*notice**\n\n{', '.join(duplicate_problem_list)}에 중복 인원이 존재합니다.")            
                

# st.session_state['quarter_allocation_info']['stop_player_name_list_bool'] = False
# if finally_no_errors:
#     find_stop_select = final_quarter_table.iloc[1:,:2]
#     over_quarter_alloncated = find_stop_select[find_stop_select['남은 쿼터 수'].apply(lambda x: int(x.split("/")[0])) < 0]
    
#     stop_player_name_list = find_stop_select[find_stop_select['남은 쿼터 수'].apply(lambda x: x.split("/")[0]) == "0"]['이름'].values
#     stop_player = "🔸"+stop_player_name_list+"🔸"
    
#     if len(stop_player)> 0:
#         with expander3:
#             st.success(f"**\*notice**\n\n{'     '.join(stop_player)}의 쿼터 배정이 끝났습니다. \n\n자세한 사항은 좌측 사이드 바에서 확인하세요.")
#             st.session_state['quarter_allocation_info']['stop_player_name_list_bool'] = True
#             st.session_state['quarter_allocation_info']['stop_player_name_list'] = stop_player_name_list
#             print(st.session_state['quarter_allocation_info']['stop_player_name_list_bool'])
#             print(st.session_state['quarter_allocation_info']['stop_player_name_list'])
#     else:
#         st.session_state['quarter_allocation_info']['stop_player_name_list_bool'] = False


############쿼터 다 찬 사람 해결 못함



















###################################################################################################


    
# if st.button('깃허브에 커밋 & 푸시하기'):
#     # 현재 시간을 커밋 메시지로 사용합니다.
#     commit_message = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     try:
#         subprocess.run(["git", "add", "."], check=True, stderr=subprocess.PIPE)
#         subprocess.run(["git", "commit", "-m", commit_message], check=True, stderr=subprocess.PIPE)
#         subprocess.run(["git", "push"], check=True, stderr=subprocess.PIPE)
#         st.success('깃허브에 성공적으로 커밋 & 푸시되었습니다.')
#     except subprocess.CalledProcessError as e:
#         st.error(f'명령어 실행 중 오류가 발생했습니다: {e}')

