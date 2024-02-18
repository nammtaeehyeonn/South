import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import streamlit as st
import io
import pandas as pd
import random
import math

# 이미지 파일 로드
image_path = 'playground.png'  # 이미지 파일 경로 설정
image = Image.open(image_path)
width, height = image.size

# 이미지 위에 그래픽 그리기
def draw_on_image(image, quarter_nums_list):
    quarter_nums_list = [int(i) for i in quarter_nums_list]
    fig, ax = plt.subplots()
    ax.imshow(image)
    
    virtical_relative_positions = []
    horizontal_relative_positions = []
    
    virtical_rp = 0.75
    for _ in range(len(quarter_nums_list)):
        virtical_relative_positions.append(round(virtical_rp,5))
        virtical_rp -= 0.55/(len(quarter_nums_list)-1)
    # virtical_relative_positions += [0.9]
    
    for nums in quarter_nums_list:
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
            horizontal_relative_per_positions = [0.4, 0.6]
        if len(horizontal_relative_per_positions) == 3:
            horizontal_relative_per_positions = [0.3, 0.5, 0.7]
        horizontal_relative_positions.append(horizontal_relative_per_positions)
    
    # 포지션(동그라미) 그리기 - 예시로 몇 개의 포지션을 임의로 추가
    for virtical_pos, horizontal_pos_list in zip(virtical_relative_positions, horizontal_relative_positions):
        circle_y = virtical_pos * height  # 세로 위치 계산
        for horizontal_pos in horizontal_pos_list:
            circle = plt.Circle((width * horizontal_pos, circle_y), width * 0.05, color="red", fill=False)
            ax.add_patch(circle)
            
    keep_circle_y = 0.9 * height        
    keep_circle = plt.Circle((width * 0.5, keep_circle_y), width * 0.05, color='yellow', fill=False)
    ax.add_patch(keep_circle)           
    
    # 축과 레이블 제거
    ax.axis('off')
    
    # print(virtical_relative_positions)
    # print(horizontal_relative_positions)
    
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
        GK_Quater_nums = round(quarter/GK_count)
        
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
formation = '선택','4-4-2','4-3-3','4-2-3-1','4-3-1-2','4-2-2-2','4-3-2-1','4-1-4-1','4-1-2-3','4-5-1','4-4-1-1','4-6-0','3-5-2','3-4-3','3-3-3-1','3-4-1-2','3-6-1','3-4-2-1','5-3-2','5-4-1'
left_quarter_value = 100


st.title("South FC Formation Maker")    
st.write("")
with st.expander('기초 설정') :
    quarter = st.slider('오늘의 쿼터 수', 1, 6, (4))
    st.write("")
    mans = st.slider('경기 선발 인원 수', 5, 13, (11))
    st.write("")
    st.write("")
    
    all_players = [f"선수{i+1}" for i in range(25)]
    ##### 포지션 삽입 구간 #####
    all_entry = dict()
    random.seed(2022)
    for p in all_players:
        positions = ["CF","WF","CM","WM","CB","WB","GK"]
        main_position = random.choice(positions)
        positions.remove(main_position)
        sub_position = random.sample(positions, random.randint(1, 5))
        if main_position == "GK":
            sub_position = []
            
        if "GK" in sub_position:
            sub_position.remove("GK")
        all_entry[p] = {"주포지션":main_position,"부포지션":sub_position}
    ############################
    play_players = st.multiselect('경기에 참가하는 인원을 고르세요.', all_players)
    play_entry = dict()
    GK_count = 0
    GK_list = []
    for key,value, in all_entry.items():
        if key in play_players:
            play_entry[key] = value
            if play_entry[key]['주포지션'] == "GK":
                GK_count += 1
                GK_list.append(key)
                print(GK_list)
        

        
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
            col1.metric(f"-", f"{Fewer_Quarter_mans}명", f"{Fewer_Quarter_nums}쿼터", delta_color="inverse")
            col2.metric(f"-", f"{More_Quarter_mans}명", f"{More_Quarter_nums}쿼터")
            col3.metric("키퍼", f"{GK_count}명", f"{GK_Quater_nums}쿼터")
            
    if st.session_state.first_button_pressed:  
        st.write("")
        change_quarter = st.button("직접 조정하기")
        no_change_quarter = st.button("그대로 가기(랜덤)")
        
        # 조정
        if change_quarter:
            st.session_state.change_button_pressed = True 
            st.session_state.no_change_button_pressed = False 
            
        if st.session_state.change_button_pressed == True:
            change_quarter_df = pd.DataFrame({'선수명단' : play_entry.keys(), '주포지션' : [play_entry[key]['주포지션'] for key in play_entry.keys()], '부포지션' : [play_entry[key]['부포지션'] for key in play_entry.keys()], '쿼터 수' : [0]*len(play_players)})
        
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
            GK_quarter_df = pd.DataFrame({'선수명단' : GK_list, '주포지션' : [play_entry[gk]['주포지션'] for gk in GK_list], '부포지션' : [play_entry[gk]['부포지션'] for gk in GK_list], '쿼터 수' : [GK_Quater_nums]*GK_count})
            except_GK_quarter_df = pd.DataFrame({'선수명단' : except_GK_list, '주포지션' : [play_entry[field]['주포지션'] for field in except_GK_list], '부포지션' : [play_entry[field]['부포지션'] for field in except_GK_list], '쿼터 수' : no_change_quarter_list})
            change_quarter_df = pd.concat([GK_quarter_df, except_GK_quarter_df], axis=0)
        
        
        if st.session_state.change_button_pressed:
            change_quarter_df_st = st.data_editor(change_quarter_df, use_container_width= True, disabled=["선수명단"], hide_index = True)
            left_quarter_value = (quarter*mans) - change_quarter_df_st['쿼터 수'].sum()
            if left_quarter_value >= 0:
                left_quarter = st.markdown(f"**남은 쿼터 수 : {left_quarter_value}**")
            if left_quarter_value < 0:
                st.error(f"쿼터 수 초과 : {change_quarter_df_st['쿼터 수'].sum() - (quarter*mans)}")
                
        if st.session_state.no_change_button_pressed:
            left_quarter_value = 0
            change_quarter_df_st = st.dataframe(change_quarter_df, use_container_width= True, hide_index = True)
            

st.write("")
with st.expander('포메이션 설정') :
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
                fig = draw_on_image(image,quarter_nums_list)
                fig_dict[f"Quarter_{qdx+1}"] = fig
            
                save_images_to_session_state(fig_dict)
        
    for key in fig_dict.keys():
        loaded_image = load_image_from_session_state(key)
        if loaded_image is not None:
            st.subheader(f"{key[-1]}쿼터")
            st.pyplot(loaded_image)
            st.write("")
                