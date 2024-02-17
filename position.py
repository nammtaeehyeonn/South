import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import streamlit as st
import io

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
    fig.savefig(buf, format='JPEG')
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
        return image
    return None


left_column, chat_column, right_column = st.columns([1, 2, 1])
formation = '선택','3-5-2','3-4-3','3-3-3-1','3-4-1-2','3-6-1','3-4-2-1','4-4-2','4-3-3','4-2-3-1','4-3-1-2','4-2-2-2','4-3-2-1','4-1-4-1','4-1-2-3','4-5-1','4-4-1-1','4-6-0','5-3-2','5-4-1'

# if 'formation' not in st.session_state:
#     st.session_state.formation = {"Quater_1":"", "Quater_2":"", "Quater_3":"", "Quater_4":""}
    
Quater_1 = st.selectbox("1쿼터 포메이션 선택", formation)
st.write()
Quater_2 = st.selectbox("2쿼터 포메이션 선택", formation)
st.write()
Quater_3 = st.selectbox("3쿼터 포메이션 선택", formation)
st.write()
Quater_4 = st.selectbox("4쿼터 포메이션 선택", formation)
st.write()


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
    print(fig_dict)
    loaded_image = load_image_from_session_state(key)
    print(loaded_image)
    if loaded_image is not None:
        st.write(f"{key}")
        st.image(loaded_image)
        st.write("")
            
        
# fig = draw_on_image(image,4,3,3)

# st.pyplot(fig)