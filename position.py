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

first_seed = int(str(datetime.datetime.now().month) + str(datetime.datetime.now().day))
second_seed = int(str(datetime.datetime.now().year) + str(datetime.datetime.now().month) + str(datetime.datetime.now().day))
# first_seed = random.sample(range(1,1000), 1)[0]
# second_seed = random.sample(range(1001,2000), 1)[0]
random.seed(first_seed)

# 이미지 파일 로드
image_path = 'playground.png'  # 이미지 파일 경로 설정
image = Image.open(image_path)
width, height = image.size

with open('./eng_formation_dict.json', 'r') as f : 
	eng_formation_dict = json.load(f)
 
with open('./entry.json', 'r') as f : 
	entry = json.load(f)
    
@st.cache_data
def fontRegistered():
    font_dirs = [os.getcwd() + '/customFonts']
    font_files = fm.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    fm._load_fontmanager(try_read_cache=False)

def adjust_squad_lengths(quater_squad, play_entry):
    # 목표 길이 설정
    target_length = 11
    start_time = time.time()
    
    # 모든 리스트의 길이가 목표 길이에 도달할 때까지 반복
    while not all(len(squad) == target_length for squad in quater_squad):
            # if time.time() - start_time > timeout:
            #     print("Timeout! Breaking the loop.")
            #     break

            # 모든 팀에서 옮길 수 있는 선수가 있는지 확인
            if not any(len(squad) > target_length for squad in quater_squad):
                print("No more players to move. Breaking the loop.")
                break

            for squad in quater_squad:
                if len(squad) < target_length:
                    # 선수를 옮길 수 있는 팀을 찾음
                    donor_squad = next((s for s in quater_squad if len(s) > target_length and any(player not in squad for player in s)), None)
                    if donor_squad is None:
                        print("No suitable players to move. Breaking the loop.")
                        break

                    # 선수를 옮김
                    for player in donor_squad:
                        if len(squad) == target_length:
                            break
                        if player not in squad:
                            squad.append(player)
                            donor_squad.remove(player)
                    
    all_list = []
    for qs in quater_squad:
        all_list.extend(qs)
    for al in set(all_list):
        play_entry[al]['참가 쿼터'] = []
        for qdx, qs in enumerate(quater_squad):
            if al in qs:
                play_entry[al]['참가 쿼터'].append(qdx+1)
    # print("@"*110)
    # print(quater_squad)
    # print("@"*110)
    # print("#"*50)
    # print(quater_squad)            
    # print(play_entry)   
    # print("#"*50)   
    # `
    # # 키퍼 쿼터 수 조정해라 쿼터 수 동일하게 나누고 같은 쿼터에 안들어가게
    # `
    return quater_squad, play_entry

def find_position(joined_formation, global_quater, play_entry):
    random.seed(second_seed)
    for k,v in play_entry.items():
        second_gk = False
        print(v)
        run_quaters = random.sample(range(1,global_quater+1), int(play_entry[k]['쿼터 수']))
        run_quaters.sort()
        
        if v['주포지션'] == 'GK':
            first_gk_run_quaters = run_quaters
            gk_full_quarter = [q for q in range(1,global_quater+1)]
            for f in first_gk_run_quaters:
                gk_full_quarter.remove(f)
            second_gk_run_quaters = gk_full_quarter
            second_gk = True
        
        play_entry[k]['참가 쿼터'] = run_quaters
        if second_gk:
            play_entry[k]['참가 쿼터'] = second_gk_run_quaters
        
    Quater_1_squad = [k for k,v in play_entry.items() if 1 in play_entry[k]['참가 쿼터']]
    Quater_2_squad = [k for k,v in play_entry.items() if 2 in play_entry[k]['참가 쿼터']]
    Quater_3_squad = [k for k,v in play_entry.items() if 3 in play_entry[k]['참가 쿼터']]
    Quater_4_squad = [k for k,v in play_entry.items() if 4 in play_entry[k]['참가 쿼터']]
    Quater_squad = [Quater_1_squad, Quater_2_squad, Quater_3_squad, Quater_4_squad]
    
    adjusted_quater_squad, play_entry = adjust_squad_lengths(Quater_squad, play_entry)
    
    #print("#"*100)
    #print("#"*100)
    #print(play_entry)
    #print("#"*100)
    #print("#"*100)
        
    
    find_position_dict = dict()
    for k in [joined_formation]:
        flattened_list = [item for sublist in eng_formation_dict[k] for item in sublist]
        #print(k, flattened_list)
        for fl in flattened_list:
            #print(fl)
            find_position_dict[fl] = {}
            main_fl_list = []
            sub_fl_list = []
            for k,v in play_entry.items():
                if (play_entry[k]['주포지션'] == fl):
                    #print("주포지션 :", k, " * ")
                    main_fl_list.append(k)
                if (fl in play_entry[k]['부포지션']):
                    #print("부포지션 :", k)
                    sub_fl_list.append(k)
            find_position_dict[fl]['주포지션'] = main_fl_list
            find_position_dict[fl]['부포지션'] = sub_fl_list
                    
        #print()   
        print(find_position_dict)
    return find_position_dict, play_entry
    
# 이미지 위에 그래픽 그리기
def draw_on_image(image, qdx, quarter_nums_list, eng_formation_dict, global_quater, play_entry):
    fontRegistered()
    plt.rc('font', family='NanumGothic')
    
    joined_formation = "-".join(quarter_nums_list)
    eng_joined_formation = eng_formation_dict[joined_formation]
    
    find_position_dict, quater_play_entry = find_position(joined_formation, global_quater, play_entry)
    quarter_nums_list = [int(i) for i in quarter_nums_list]
    fig, ax = plt.subplots()
    ax.imshow(image)
    
    virtical_relative_positions = []
    horizontal_relative_positions = []
    
    virtical_rp = 0.75
    for _ in range(len(quarter_nums_list)):
        virtical_relative_positions.append(round(virtical_rp,5))
        virtical_rp -= 0.55/(len(quarter_nums_list)-1)
    
    for ndx, nums in enumerate(quarter_nums_list):
        horizontal_rp = 0.2
        horizontal_relative_per_positions = []
        for _ in range(nums):
            horizontal_relative_per_positions.append(round(horizontal_rp,5))
            if nums == 1:
                horizontal_rp += 0.6/(1)
            else:
                horizontal_rp += 0.6/(nums-1)
        if len(horizontal_relative_per_positions) == 1:
            horizontal_relative_per_positions = [0.5]
        if len(horizontal_relative_per_positions) == 2:
            if (ndx == 2) & (quarter_nums_list == [4,2,2,2]):
                horizontal_relative_per_positions = [0.2, 0.8]
            else:
                horizontal_relative_per_positions = [0.4, 0.6]
        if len(horizontal_relative_per_positions) == 3:
            horizontal_relative_per_positions = [0.3, 0.5, 0.7]
        horizontal_relative_positions.append(horizontal_relative_per_positions)
    for eng_joined_formation_list, virtical_pos, horizontal_pos_list in zip(eng_joined_formation, virtical_relative_positions, horizontal_relative_positions):
        circle_y = virtical_pos * height  # 세로 위치 계산
        for eng_pos, horizontal_pos in zip(eng_joined_formation_list, horizontal_pos_list):
            main_pos_mans = ""
            for pdx, pl in enumerate(find_position_dict[eng_pos]['주포지션']):
                if qdx in quater_play_entry[pl]['참가 쿼터']:
                    # main_pos_mans += f"{find_position_dict[eng_pos]['주포지션']}\n"
                    main_pos_mans += f"{pl}\n"
                
            # main_pos_mans = "\n".join(find_position_dict[eng_pos]['주포지션'])
            circle = plt.Circle((width * horizontal_pos, circle_y), width * 0.05, color="blue", fill=True)
            ax.add_patch(circle)
            ax.text(width * horizontal_pos, circle_y, eng_pos, ha='center', va='center', color='white', fontsize=8)
            # if qdx in find_position_dict[eng_pos]['참가 쿼터']:
            ax.text(width * horizontal_pos, circle_y+30, main_pos_mans, ha='center', va='center', color='white', fontsize=5)

    for k, v in quater_play_entry.items():
        if (v["주포지션"] == 'GK') & (qdx in v["참가 쿼터"]):
            main_pos_gk = k
            print(main_pos_gk)
    keep_circle_y = 0.9 * height        
    keep_circle = plt.Circle((width * 0.5, keep_circle_y), width * 0.05, color='yellow', fill=True)
    ax.add_patch(keep_circle)           
    ax.text(width * 0.5, keep_circle_y, "GK", ha='center', va='center', color='black', fontsize=8)
    try:
        ax.text(width * 0.5, keep_circle_y+30, main_pos_gk, ha='center', va='center', color='black', fontsize=5)
    except:
        ax.text(width * 0.5, keep_circle_y+30, "쿼터 내 누군가", ha='center', va='center', color='black', fontsize=5)
    
    # 축과 레이블 제거
    ax.axis('off')
    
    return fig

def convert_fig_to_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='PNG', dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close(fig)  # 리소스 해제
    buf.seek(0)
    return buf.getvalue()

def save_images_to_session_state(fig_dict):
    if 'image_dict' not in st.session_state:
        st.session_state['image_dict'] = {}
    
    for key, fig in fig_dict.items():
        if fig:  # fig가 비어있지 않은 경우에만 처리
            byte_data = convert_fig_to_bytes(fig)
            st.session_state['image_dict'][key] = byte_data
        
def load_image_from_session_state(key):
    if 'image_dict' in st.session_state and key in st.session_state['image_dict']:  # 'images' 대신 'image_dict' 사용
        byte_data = st.session_state['image_dict'][key]
        image = Image.open(io.BytesIO(byte_data))
        fig, ax = plt.subplots()
        ax.imshow(image)
        ax.axis('off')  # 축 숨기기
        
        return fig
    return None

def quarter_calculator(quarter, mans, play_players, GK_count):
    if GK_count == 0:
        GK_Quater_nums = 0
    if GK_count > 0:
        GK_Quater_nums = round(quarter/GK_count,1)
        
    mans -= GK_count
    except_GK_play_players = len(play_players) - GK_count
    
    total_quarter_nums = quarter*mans

    least_quarter = math.floor(total_quarter_nums/except_GK_play_players)
    
    Number_of_Quarters_Remaining = total_quarter_nums - (least_quarter*except_GK_play_players)
    
    Fewer_Quarter_mans = except_GK_play_players-Number_of_Quarters_Remaining
    Fewer_Quarter_nums = least_quarter
    
    More_Quarter_mans = Number_of_Quarters_Remaining
    More_Quarter_nums = least_quarter+1
    
    return Fewer_Quarter_mans, Fewer_Quarter_nums, More_Quarter_mans, More_Quarter_nums, GK_count, GK_Quater_nums

left_column, chat_column, right_column = st.columns([1, 2, 1])
# formation = '선택','4-4-2','4-3-3','4-2-3-1','4-3-1-2','4-2-2-2','4-3-2-1','4-1-4-1','4-1-2-3','4-5-1','4-4-1-1','3-5-2','3-4-3','3-3-3-1','3-4-1-2','3-4-2-1','5-3-2','5-4-1'
formation = list(eng_formation_dict.keys())
left_quarter_value = 100
global_quater = 0

st.title("South FC Formation Maker")    
st.write("")
with st.expander('기초 설정') :
    quarter = st.slider('오늘의 쿼터 수', 1, 6, (4))
    global_quater = quarter
    st.write("")
    mans = st.slider('경기 선발 인원 수', 5, 13, (11))
    st.write("")
    st.write("")
    
    all_entry = dict()

    all_players = ["김동선" ,"김선광" ,"김성재" ,"김영목" ,"김은민" ,"김철영" ,"남태현" ,"민병인" ,"박창후" ,"서윤찬" ,"서종민" ,"소지호" ,"이병훈" ,"이산호" ,"이재성" ,"이종현" ,"정지원" ,"조성민" ,"조영수" ,"차종수" ,"최민규" ,"최형근" ,"최형주" ,"구형준" ,"홍태호", "용병1", "용병2", "용병3", "용병4", "용병5" ]
    all_main_position = ["WB", "CF", "CB", "CM", "CM", "WB", "CM", "GK", "WF", "WF", "CB", "WF", "CB", "WF", "CF", "WF", "WF", "WB", "CM", "CF", "CB", "CM", "WB", "CF", "CM", "", "", "", "", ""]
    all_sub_position = [["GK"], ["CM", "WB"], ["WB"], ["CB"], ["WB"], ["CB", "CF"], ["CB", "WB"], [], ["CM","WM","WB"], ["CM","CF"], ["WB", "WF"], ["CM", "WB"], ["CM", "WB"], ["WB", "WM"], ["WF", "CM", "WM"], ["CM", "WM", "CF"], ["CF", "WB"], ["CB"], ["WB"], ["WB", "GK"], ["CM"], ["WF", "WB", "CF"], ["CM"], ["WF", "WB"], ["WF", "CF"], [], [], [], [], []]

    for i, j, k in zip(all_players, all_main_position, all_sub_position):
        all_entry[i] = {"주포지션":j,"부포지션":k}
        
    play_players = st.multiselect('경기에 참가하는 인원을 고르세요.', all_players)
    import re
    pattern = r"용병\d+"
    matches = []
    for name in play_players:
        if re.match(pattern, name):
            matches.append(name)
    left_column_mercenary, chat_column_mercenary, right_column_mercenary = st.columns([1, 0.5, 2])
    if 'update_mercenary' not in st.session_state:
        st.session_state.update_mercenary = False
    if matches:
        mercenary_key = dict()
        mercenary_list = [dict()]*len(matches)
        for mdx, m in enumerate(matches):
            pos_list = ['CF', 'WF', 'CM', 'WM', 'CB', 'WB', 'GK']
            with left_column_mercenary:
                mercenary_name = st.text_input(f"{m} 이름", key=f"a{mdx}")       
            with chat_column_mercenary:
                mercenary_main_pos = st.selectbox("주포지션", ["-"] + pos_list, key=f"b{mdx}")       
            with right_column_mercenary:
                mercenary_sub_pos = st.multiselect("부포지션", pos_list, key=f"c{mdx}", placeholder="복수선택 가능")       
            mercenary_list[mdx] = {mercenary_name:{"주포지션":mercenary_main_pos, "부포지션":mercenary_sub_pos}}
            mercenary_key[m] = mercenary_name
        st.write("⏬⏬⏬정보 적용을 하지않으면 잘못된 스쿼드로 포지션을 구성하게 될 수 있습니다.")   
        
            
        if st.button("용병 정보 적용하기"):
            st.session_state.update_mercenary = True
        if st.session_state.update_mercenary:
            update_flag = True
            for mercenary_info in mercenary_list:
                for k, v in mercenary_info.items():
                    if (k == '') | (v['주포지션'] == '-'):
                        st.error("이름/주포지션에 빈 값이 존재합니다.")
                        update_flag = False
            if update_flag:
                for mercenary_info in mercenary_list:
                    all_entry.update(mercenary_info)
                tmp_names = "/".join(play_players)
                for k, v in mercenary_key.items():
                    tmp_names = tmp_names.replace(k,v)
                play_players = tmp_names.split("/")
                for m in matches:
                    # for pdx, pp in enumerate(play_players):
                    #     if m == pp:
                    #         play_players[pdx] = m
                    del all_entry[m]
                
                
                print("적용!!!")
                print(play_players)
                print(all_entry)
    
    play_entry = dict()
    GK_count = 0
    GK_list = []
    for key,value, in all_entry.items():
        if key in play_players:
            play_entry[key] = value
            if play_entry[key]['주포지션'] == "GK":
                GK_count += 1
                GK_list.append(key)
   

        
    st.write("")
    
    st.markdown("**경기 정보**")
    information_df = pd.DataFrame([[quarter, mans, len(play_players)]], columns = ['쿼터 수', '경기 인원 수','South FC Entry'], index = ['수치'])
    st.dataframe(information_df, use_container_width=True)
    st.write("")
    
    if 'first_button_pressed' not in st.session_state:
        st.session_state.first_button_pressed = False
    if 'change_button_pressed' not in st.session_state:
        st.session_state.change_button_pressed = False
    if 'no_change_button_pressed' not in st.session_state:
        st.session_state.no_change_button_pressed = False
    
    quarter_divider_button = st.button("쿼터 배분 분석하기")
    
    if quarter_divider_button:
        st.session_state.first_button_pressed = True  
        
    if st.session_state.first_button_pressed:
        if mans > len(play_players):
            st.error("경기 참가 인원이 너무 적습니다.")
        else:
            Fewer_Quarter_mans, Fewer_Quarter_nums, More_Quarter_mans, More_Quarter_nums, GK_count, GK_Quater_nums = quarter_calculator(quarter, mans, play_players, GK_count)
            st.divider()
            st.markdown("**가장 공평한 쿼터 수 분배**")
            
            col1, col2, col3= st.columns(3)
            col1.metric("필드", f"{Fewer_Quarter_mans}명", f"{Fewer_Quarter_nums}쿼터", delta_color="inverse")
            col2.metric("필드", f"{More_Quarter_mans}명", f"{More_Quarter_nums}쿼터")
            col3.metric("키퍼", f"{GK_count}명", f"{GK_Quater_nums}쿼터",  delta_color="off")
            
            if st.session_state.first_button_pressed:  
                st.write("")
                change_quarter = st.button("직접 조정하기")
                no_change_quarter = st.button("그대로 가기(랜덤)")
                
                # 조정
                if change_quarter:
                    st.session_state.change_button_pressed = True 
                    st.session_state.no_change_button_pressed = False 
                    
                if st.session_state.change_button_pressed == True:
                    print()
                    change_quarter_df = pd.DataFrame({'선수명단' : play_entry.keys(), '주포지션' : [play_entry[key]['주포지션'] for key in play_entry.keys()], '부포지션' : [" ".join(play_entry[key]['부포지션']) for key in play_entry.keys()], '쿼터 수' : [0]*len(play_players)})
                
                # 그대로
                if no_change_quarter:
                    st.session_state.change_button_pressed = False 
                    st.session_state.no_change_button_pressed = True 
                
                if st.session_state.no_change_button_pressed == True:
                    except_GK_list = list(play_entry.keys())
                    for gk in GK_list:
                        except_GK_list.remove(gk)
                    no_change_quarter_list = [Fewer_Quarter_nums]*Fewer_Quarter_mans + [More_Quarter_nums]*More_Quarter_mans
                    random.shuffle(no_change_quarter_list)
                    GK_quarter_df = pd.DataFrame({'선수명단' : GK_list, '주포지션' : [play_entry[gk]['주포지션'] for gk in GK_list], '부포지션' : [" ".join(play_entry[gk]['부포지션']) for gk in GK_list], '쿼터 수' : [GK_Quater_nums]*GK_count})
                    except_GK_quarter_df = pd.DataFrame({'선수명단' : except_GK_list, '주포지션' : [play_entry[field]['주포지션'] for field in except_GK_list], '부포지션' : [" ".join(play_entry[field]['부포지션']) for field in except_GK_list], '쿼터 수' : no_change_quarter_list})
                    change_quarter_df = pd.concat([GK_quarter_df, except_GK_quarter_df], axis=0)
                
                
                if st.session_state.change_button_pressed:
                    change_quarter_df_st = st.data_editor(change_quarter_df, use_container_width= True, disabled=["선수명단"], hide_index = True)
                    left_quarter_value = (quarter*mans) - change_quarter_df_st['쿼터 수'].sum()
                    if left_quarter_value >= 0:
                        left_quarter = st.markdown(f"**남은 쿼터 수 : {left_quarter_value}**")
                    if left_quarter_value < 0:
                        st.error(f"쿼터 수 초과 : {change_quarter_df_st['쿼터 수'].sum() - (quarter*mans)}")
                    for k in play_entry.keys():
                        play_entry[k]['쿼터 수'] = change_quarter_df_st.loc[change_quarter_df_st['선수명단'] == k, '쿼터 수'].values[0]
                        play_entry[k]['주포지션'] = change_quarter_df_st.loc[change_quarter_df_st['선수명단'] == k, '주포지션'].values[0]
                        play_entry[k]['부포지션'] = change_quarter_df_st.loc[change_quarter_df_st['선수명단'] == k, '부포지션'].values[0]
                        #print(play_entry)
                        
                if st.session_state.no_change_button_pressed:
                    left_quarter_value = 0
                    change_quarter_df_st = st.data_editor(change_quarter_df, use_container_width= True, hide_index = True, disabled=["선수명단", "쿼터 수"])
                    for k in play_entry.keys():
                        play_entry[k]['쿼터 수'] = change_quarter_df_st.loc[change_quarter_df_st['선수명단'] == k, '쿼터 수'].values[0]
                        play_entry[k]['주포지션'] = change_quarter_df_st.loc[change_quarter_df_st['선수명단'] == k, '주포지션'].values[0]
                        play_entry[k]['부포지션'] = change_quarter_df_st.loc[change_quarter_df_st['선수명단'] == k, '부포지션'].values[0]
                    
                        #print(play_entry)
                # #print(change_quarter_df['선수명단'].values)
                # #print(change_quarter_df['주포지션'].values)
                # #print(change_quarter_df['부포지션'].values)
                # #print(change_quarter_df['쿼터 수'].values)
                
                # for k in play_entry.keys():
                #     play_entry[k]['쿼터 수'] = change_quarter_df_st.loc[change_quarter_df_st['선수명단'] == k, '쿼터 수'].values[0]
                    
st.write("")
with st.expander('포메이션 설정') :
    if 'recommend_button_pressed' not in st.session_state:
        st.session_state.recommend_button_pressed = False
        
    if left_quarter_value == 0:
        Recommended_Formation = st.button("포메이션 추천")
    if left_quarter_value != 0:
        Recommended_Formation = st.button("포메이션 추천", disabled=True)
        
    if Recommended_Formation:
        st.session_state.recommend_button_pressed = True 
        
    if (st.session_state.recommend_button_pressed) & (left_quarter_value == 0):
        sub_pos_list = []
        main_pos_list = list(change_quarter_df['주포지션'].values)
        for sub_p in change_quarter_df['부포지션'].values:
            sub_pos_list.extend(sub_p)    
        
        positions = ["CF","WF","CM","WM","CB","WB","GK"]
        positions_mans = [0,0,0]
        total_point = [0,0,0]
        
        df_dict = dict()
        for idx, p in enumerate(positions[:-1][::-1]):
            df_dict[p] = [main_pos_list.count(p), (sub_pos_list.count(p)), main_pos_list.count(p)+(sub_pos_list.count(p)), math.floor((main_pos_list.count(p)+(sub_pos_list.count(p)))/global_quater)]
            if p[-1] == 'B':
                positions_mans[0] += df_dict[p][-1]
                total_point[0] += df_dict[p][-2]
            if p[-1] == 'M':
                positions_mans[1] += df_dict[p][-1]
                total_point[1] += df_dict[p][-2]
            if p[-1] == 'F':
                positions_mans[2] += df_dict[p][-1]
                total_point[2] += df_dict[p][-2]
        point_df = pd.DataFrame(df_dict, index = ['주포지션', '부포지션', '총점', '적정 인원'])
        
        final_positions_mans = positions_mans.copy()
        
        max_nums_positions = positions_mans.index(max(positions_mans))
        positions_mans[max_nums_positions] = 100
        
        min_nums_positions = positions_mans.index(min(positions_mans))
        positions_mans[min_nums_positions] = -100
        
        median_nums_positions = [i for i in range(len(total_point)) if (i != max_nums_positions) & (i != min_nums_positions)][0]
        
        count_positions = ["수비", "미드필더", "공격"]
        count_positions = [count_positions[max_nums_positions], count_positions[median_nums_positions], count_positions[min_nums_positions]]
        
            
        if final_positions_mans[0] < 3:
            final_positions_mans[0] = 3
            
        if final_positions_mans[0] > 4:
            final_positions_mans[0] = 4    
            
        if final_positions_mans[2] >= 4:
            final_positions_mans[2] = 3
        
        if count_positions[0] == "수비":
            final_positions_mans[0] = 4
            if count_positions[2] == "공격":
                final_positions_mans[2] = 1
            else:
                final_positions_mans[2] = 2
            final_positions_mans[1] = 10 - (final_positions_mans[0] + final_positions_mans[2])
                
        if count_positions[0] == "미드필더":
            final_positions_mans[1] = 5
            if count_positions[2] == "공격":
                final_positions_mans[2] = 1
            else:
                final_positions_mans[2] = 2                
            final_positions_mans[0] = 10 - (final_positions_mans[1] + final_positions_mans[2])
            
        if count_positions[0] == "공격":
            final_positions_mans[2] = 3
            if count_positions[2] == "수비":
                final_positions_mans[0] = 3
            else:
                final_positions_mans[0] = 4                
            final_positions_mans[1] = 10 - (final_positions_mans[2] + final_positions_mans[0])    
        
        st.markdown(f"오늘 South FC의 선수들은 **{count_positions[0]}, {count_positions[1]}, {count_positions[2]}** 포지션 순으로 많습니다.")
        st.subheader("추천 포메이션 : " + "-".join([str(i) for i in final_positions_mans]))
        st.write("")
    
    quarter_list = []
    for q in range(quarter):
        select_quarter = st.selectbox(f"{q+1}쿼터 포메이션 선택", formation)
        quarter_list.append(select_quarter)
        st.write()

st.write("")
fig_dict = {"Quarter_1":"", "Quarter_2":"", "Quarter_3":"", "Quarter_4":""}
if left_quarter_value == 0:
    make_formation = st.button("포지션 배치하기", type="primary")
if left_quarter_value != 0:
    make_formation = st.button("포지션 배치하기", type="primary", disabled=True)

st.write("")
with st.spinner("포지션 배치 중"):
    if make_formation:
        for qdx, quarter in enumerate(quarter_list):
            if quarter == "선택":
                st.error(f"{qdx+1}쿼터의 포메이션을 정해주세요.")
                st.session_state['image_dict'] = {}
                break
            else:
                quarter_nums_list = quarter.split("-")
                fig = draw_on_image(image, qdx+1, quarter_nums_list,eng_formation_dict,global_quater, play_entry)
                fig_dict[f"Quarter_{qdx+1}"] = fig
            
                save_images_to_session_state(fig_dict)
        
    for key in fig_dict.keys():
        loaded_image = load_image_from_session_state(key)
        if loaded_image is not None:
            st.subheader(f"{key[-1]}쿼터")
            st.pyplot(loaded_image)
            st.write("")