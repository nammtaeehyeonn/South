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
def draw_on_image(image, Quater_nums_list):
    Quater_nums_list = [int(i) for i in Quater_nums_list]
    fig, ax = plt.subplots()
    ax.imshow(image)
    
    virtical_relative_positions = []
    horizontal_relative_positions = []
    
    virtical_rp = 0.75
    for _ in range(len(Quater_nums_list)):
        virtical_relative_positions.append(round(virtical_rp,5))
        virtical_rp -= 0.55/(len(Quater_nums_list)-1)
    # virtical_relative_positions += [0.9]
    
    for nums in Quater_nums_list:
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

def Quater_calculator(quater, mans, play_players):
    
    total_Quater_nums = quater*mans

    least_quater = math.floor(total_Quater_nums/len(play_players))
    
    Number_of_Quarters_Remaining = total_Quater_nums - (least_quater*len(play_players))
    
    Fewer_Quarter_mans = len(play_players)-Number_of_Quarters_Remaining
    Fewer_Quarter_nums = least_quater
    
    More_Quarter_mans = Number_of_Quarters_Remaining
    More_Quarter_nums = least_quater+1
    
    return Fewer_Quarter_mans, Fewer_Quarter_nums, More_Quarter_mans, More_Quarter_nums

left_column, chat_column, right_column = st.columns([1, 2, 1])
formation = '선택','4-4-2','4-3-3','4-2-3-1','4-3-1-2','4-2-2-2','4-3-2-1','4-1-4-1','4-1-2-3','4-5-1','4-4-1-1','4-6-0','3-5-2','3-4-3','3-3-3-1','3-4-1-2','3-6-1','3-4-2-1','5-3-2','5-4-1'


st.title("South FC Formation Maker")    
st.write("")
with st.expander('기초 설정') :
    quater = st.slider('오늘의 쿼터 수', 1, 6, (4))
    mans = st.slider('경기 선발 인원 수', 5, 13, (11))
    
    all_players = [f"선수{i+1}" for i in range(25)]
    play_players = st.multiselect('경기에 참가하는 인원을 고르세요.', all_players)
    # play_players = random.sample(all_players, 15)
    st.write("")
    st.markdown("**경기 정보**")
    information_df = pd.DataFrame([[quater, mans, len(play_players)]], columns = ['쿼터 수', '경기 인원 수','South FC Entry'], index = ['수치'])
    st.dataframe(information_df, use_container_width=True)

    if 'first_button_pressed' not in st.session_state:
        st.session_state.first_button_pressed = False
    if 'change_button_pressed' not in st.session_state:
        st.session_state.change_button_pressed = False
    if 'no_change_button_pressed' not in st.session_state:
        st.session_state.no_change_button_pressed = False
    
    quater_divider_button = st.button("쿼터 배분 분석하기")
    
    if quater_divider_button:
        st.session_state.first_button_pressed = True  
        
    if st.session_state.first_button_pressed:
        if mans > len(play_players):
            st.error("경기 참가 인원이 너무 적습니다.")
        else:
            Fewer_Quarter_mans, Fewer_Quarter_nums, More_Quarter_mans, More_Quarter_nums = Quater_calculator(quater, mans, play_players)
            st.divider()
            st.markdown("**가장 공평한 쿼터 수 분배**")
            
            col1, col2= st.columns(2)
            col1.metric(f"-", f"{Fewer_Quarter_mans}명", f"{Fewer_Quarter_nums}쿼터", delta_color="inverse")
            col2.metric(f"-", f"{More_Quarter_mans}명", f"{More_Quarter_nums}쿼터")
            
    if st.session_state.first_button_pressed:  
        change_quater = st.button("직접 조정하기")
        no_change_quater = st.button("그대로 가기(랜덤)")
        
        # 조정
        if change_quater:
            st.session_state.change_button_pressed = True 
            st.session_state.no_change_button_pressed = False 
            
        if st.session_state.change_button_pressed == True:
            change_quater_df = pd.DataFrame({'선수명단' : play_players, '쿼터 수' : [0]*len(play_players)}, index=[i+1 for i in range(len(play_players))])
            change_quater_df.index.name = '순서'
        
        # 그대로
        if no_change_quater:
            st.session_state.change_button_pressed = False 
            st.session_state.no_change_button_pressed = True 
        
        if st.session_state.no_change_button_pressed == True:
            no_change_quater_list = [Fewer_Quarter_nums]*Fewer_Quarter_mans + [More_Quarter_nums]*More_Quarter_mans
            random.shuffle(no_change_quater_list)
            change_quater_df = pd.DataFrame({'선수명단' : play_players, '쿼터 수' : no_change_quater_list}, index=[i+1 for i in range(len(play_players))])
            change_quater_df.index.name = '순서'
        
        
        if st.session_state.change_button_pressed:
            change_quater_df_st = st.data_editor(change_quater_df, use_container_width= True, disabled=["선수명단"])
            left_quater_value = (quater*mans) - change_quater_df_st['쿼터 수'].sum()
            if left_quater_value < 0:
                st.error("쿼터 수 초과")
            if left_quater_value >= 0:
                left_quater = st.markdown(f"**남은 쿼터 수 : {left_quater_value}**")
                
        if st.session_state.no_change_button_pressed:
            change_quater_df_st = st.dataframe(change_quater_df, use_container_width= True)
            

st.write("")
with st.expander('포메이션 설정') :

    Quater_1 = st.selectbox("1쿼터 포메이션 선택", formation)
    st.write()
    Quater_2 = st.selectbox("2쿼터 포메이션 선택", formation)
    st.write()
    Quater_3 = st.selectbox("3쿼터 포메이션 선택", formation)
    st.write()
    Quater_4 = st.selectbox("4쿼터 포메이션 선택", formation)
    st.write()

st.write("")
fig_dict = {"Quater_1":"", "Quater_2":"", "Quater_3":"", "Quater_4":""}
make_formation = st.button("실행하기")
if make_formation:
    Quater_list = [Quater_1, Quater_2, Quater_3, Quater_4]
    
    for qdx, Quater in enumerate(Quater_list):
        if Quater != "선택":
            Quater_nums_list = Quater.split("-")
            fig = draw_on_image(image,Quater_nums_list)
            fig_dict[f"Quater_{qdx+1}"] = fig
            
    save_images_to_session_state(fig_dict)
    
for key in fig_dict.keys():
    loaded_image = load_image_from_session_state(key)
    if loaded_image is not None:
        st.write(f"{key}")
        st.pyplot(loaded_image)
        st.write("")
            
        
# fig = draw_on_image(image,4,3,3)

# st.pyplot(fig)