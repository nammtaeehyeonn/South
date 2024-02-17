import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import streamlit as st

# 이미지 파일 로드
image_path = 'playground.png'  # 이미지 파일 경로 설정
image = Image.open(image_path)
width, height = image.size

# 이미지 위에 그래픽 그리기
def draw_on_image(image, *args):
    fig, ax = plt.subplots()
    ax.imshow(image)
    
    virtical_relative_positions = []
    horizontal_relative_positions = []
    
    virtical_rp = 0.75
    for _ in range(len(args)):
        virtical_relative_positions.append(round(virtical_rp,5))
        virtical_rp -= 0.55/(len(args)-1)
    # virtical_relative_positions += [0.9]
    
    for nums in args:
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
    
    print(virtical_relative_positions)
    print(horizontal_relative_positions)
    
    return fig

left_column, chat_column, right_column = st.columns([1, 2, 1])
formation = '선택','3-5-2','3-4-3','3-3-3-1','3-4-1-2','3-6-1','3-4-2-1','4-4-2','4-3-3','4-2-3-1','4-3-1-2','4-2-2-2','4-3-2-1','4-1-4-1','4-1-2-3','4-5-1','4-4-1-1','4-6-0','5-3-2','5-4-1'
with left_column:
    Quater_1 = st.selectbox("1쿼터 포메이션 선택", formation)
    st.write()
    Quater_2 = st.selectbox("2쿼터 포메이션 선택", formation)
    st.write()
    Quater_3 = st.selectbox("3쿼터 포메이션 선택", formation)
    st.write()
    Quater_4 = st.selectbox("4쿼터 포메이션 선택", formation)
    st.write()
    
    make_formation = st.button("실행하기")
    if make_formation:
        print(Quater_1)
        print(Quater_2)
        print(Quater_3)
        print(Quater_4)
        
fig = draw_on_image(image,4,3,3)

st.pyplot(fig)