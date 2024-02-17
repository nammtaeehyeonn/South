import streamlit as st
import matplotlib.pyplot as plt

# 운동장(큰 네모) 그리기
def draw_field():
    fig, ax = plt.subplots()
    # 운동장의 경계를 그립니다. 여기서는 100x50 크기를 가정합니다.
    field = plt.Rectangle((0,0), 100, 50, edgecolor="black", facecolor="none")
    ax.add_patch(field)
    
    # 포지션(동그라미) 추가 - 예시로 몇 개의 포지션을 임의로 추가합니다.
    for x, y in [(20, 25), (40, 10), (40, 40), (60, 25)]:
        player = plt.Circle((x, y), 2, color="blue")
        ax.add_patch(player)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.set_aspect('equal')  # 운동장의 가로세로 비율을 유지합니다.
    
    return fig

# Streamlit 앱에서 그래픽 표시
def app():
    st.title("축구 포지션 자동 배치")

    st.write("운동장 및 포지션 시각화")
    fig = draw_field()
    st.pyplot(fig)

if __name__ == "__main__":
    app()
