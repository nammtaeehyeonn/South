# from find_positions import define_cols_containers
# import json
# import copy
# with open("./0330/eng_formation_dict.json", "r") as f:
#     eng_formation_dict = json.load(f)   
# for_dot_position = copy.deepcopy(eng_formation_dict)



# import streamlit as st

# players = [f'Player {i}' for i in range(1, 22)]

# if "tab_selected_players" not in st.session_state:
#     st.session_state["tab_selected_players"] = {f"tab{idx+1}": {} for idx in range(4)}

# except_count = []
# if "selected_players_count" not in st.session_state:
#     st.session_state["selected_players_count"] = {}
# else:
#     for k, v in st.session_state["selected_players_count"].items():
#         if int(v) >= 2:
#             except_count.append(k)
# print(except_count)


# forma = {"1q": '4-3-2-1', "2q": '4-5-1', "3q": '4-4-2', "4q": '4-3-3'}

# tab1, tab2, tab3, tab4 = st.tabs(["**▪1쿼터▪**", "**▪2쿼터▪**", "**▪3쿼터▪**", "**▪4쿼터▪**"])

# for tdx, tab in enumerate([tab1, tab2, tab3, tab4]):
#     tab_key = f"tab{tdx+1}"
#     with tab:
#         cols_list = define_cols_containers(forma[f'{tdx+1}q'])
#         placehorder_list = for_dot_position[forma[f'{tdx+1}q']][::-1]
#         placehorder_list = [j for i in placehorder_list for j in i]
#         for i, cols in zip(range(11), cols_list):
#             unique_key = f"{tab_key}_pos{i+1}"
#             t1 = st.session_state["tab_selected_players"][tab_key].copy()

#             available_options = [''] + [player for player in players if player not in st.session_state["tab_selected_players"][tab_key].values() or player == st.session_state["tab_selected_players"][tab_key].get(unique_key, '')]
#             available_options  = [i for i in available_options if i not in except_count]
            
#             selected_player = cols.selectbox(
#                 placehorder_list[i], options=available_options, key=unique_key, index=available_options.index(st.session_state["tab_selected_players"][tab_key].get(unique_key, ''))
#             )

#             if selected_player != t1.get(unique_key, '') or (selected_player == '' and t1.get(unique_key, '') != ''):
#                 st.session_state["tab_selected_players"][tab_key][unique_key] = selected_player
#                 st.rerun()

# # 선택된 플레이어 출력
# for tab_key, players in st.session_state["tab_selected_players"].items():
#     st.write(f"{tab_key.replace('tab', 'Quarter ')}:")
#     for position, player in players.items():
#         st.write(f"Position {position.split('_')[-1]}: {player}")
        
        
        
# from collections import Counter
# all_selected_players = []
# for tab_players in st.session_state["tab_selected_players"].values():
#     for player in tab_players.values():
#         if player != '':  # 공백 선택 제외
#             all_selected_players.append(player)

# # 선수별 선택 횟수를 계산
# player_selection_counts = Counter(all_selected_players)

# st.session_state["selected_players_count"] = player_selection_counts
# # 결과 출력
# st.write("선수별 선택 횟수:", player_selection_counts)


from collections import Counter
import json
import streamlit as st
from find_positions import define_cols_containers

# 포메이션 데이터 로드
with open("./0330/eng_formation_dict.json", "r") as f:
    eng_formation_dict = json.load(f)
for_dot_position = eng_formation_dict

# 선수 목록 초기화
players = [f'Player {i}' for i in range(1, 22)]

# 선택된 선수 정보를 담을 세션 상태 초기화
if "tab_selected_players" not in st.session_state:
    st.session_state["tab_selected_players"] = {f"tab{idx+1}": {} for idx in range(4)}

# 포메이션 설정
forma = {"1q": '4-3-2-1', "2q": '4-5-1', "3q": '4-4-2', "4q": '4-3-3'}

# 탭 생성
tabs = st.tabs(["**▪1쿼터▪**", "**▪2쿼터▪**", "**▪3쿼터▪**", "**▪4쿼터▪**"])

# 모든 탭에서 선택된 선수들의 목록 생성 및 선수별 총 선택 횟수 계산
all_selected_players = []
for tab_players in st.session_state["tab_selected_players"].values():
    all_selected_players.extend([player for player in tab_players.values() if player != ''])
total_selection_counts = Counter(all_selected_players)
print(total_selection_counts)

# 각 탭별로 선수 선택 로직 처리
for tdx, tab in enumerate(tabs):
    tab_key = f"tab{tdx+1}"
    with tab:
        cols_list = define_cols_containers(forma[f'{tdx+1}q'])
        placeholder_list = [j for i in for_dot_position[forma[f'{tdx+1}q']][::-1] for j in i]
        
        for i, cols in zip(range(11), cols_list):
            unique_key = f"{tab_key}_pos{i+1}"
            t1 = st.session_state["tab_selected_players"][tab_key].copy()
            current_tab_players = st.session_state["tab_selected_players"][tab_key].values()

            # 현재 탭에서 이미 선택된 선수를 제외하고, 다른 탭에서 2번 이상 선택된 선수를 제외한 옵션 목록 생성
            available_options = [''] + [player for player in players if player not in total_selection_counts or (total_selection_counts[player] < 2 and player not in current_tab_players) or player == st.session_state["tab_selected_players"][tab_key].get(unique_key, '')]

            selected_player = cols.selectbox(
                placeholder_list[i], options=available_options, key=unique_key, index=available_options.index(st.session_state["tab_selected_players"][tab_key].get(unique_key, ''))
            )

            # 선택된 선수 정보 업데이트
            if selected_player != t1.get(unique_key, '') or (selected_player == '' and t1.get(unique_key, '') != ''):
                st.session_state["tab_selected_players"][tab_key][unique_key] = selected_player
                st.rerun()
            # st.session_state["tab_selected_players"][tab_key][unique_key] = selected_player

# 선택된 플레이어 출력
for tab_key, players in st.session_state["tab_selected_players"].items():
    st.write(f"{tab_key.replace('tab', 'Quarter ')}:")
    for position, player in players.items():
        st.write(f"{position.split('_')[-1]}: {player}")
