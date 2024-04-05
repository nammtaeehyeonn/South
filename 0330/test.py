import streamlit as st

players = [''] + [f'Player {i}' for i in range(1, 22)]

if "selected_players" not in st.session_state:
    st.session_state["selected_players"] = {}

t1 = st.session_state["selected_players"].copy()

selection_changed = False

for i in range(11):
    available_options = [player for player in players if player not in st.session_state["selected_players"].values() or player == st.session_state["selected_players"].get(i, '')]

    selected_player = st.selectbox(
        f"Select Player for Position {i+1}", options=available_options, key=i, index=available_options.index(st.session_state["selected_players"].get(i, ''))
    )

    if selected_player and (t1.get(i, '') != selected_player):
        st.session_state["selected_players"][i] = selected_player
        selection_changed = True

if selection_changed:
    st.rerun()

# 선택된 플레이어 출력
for position, player in st.session_state["selected_players"].items():
    st.write(f"Position {position+1}: {player}")
