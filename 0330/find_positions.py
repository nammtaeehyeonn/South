import streamlit as st

def define_cols_containers(formation):
    f = formation
    # final_cols_list = []
    # for q, f in formation_dict.items():
    if f == '4-4-2':
        f_cols1, f_cols2, f_cols3, f_cols4 = st.columns(4)
        m_cols1, m_cols2, m_cols3, m_cols4 = st.columns(4)
        d_cols1, d_cols2, d_cols3, d_cols4 = st.columns(4)
        cols_list = [         f_cols2, f_cols3, 
                        m_cols1, m_cols2, m_cols3, m_cols4, 
                        d_cols1, d_cols2, d_cols3, d_cols4]
    if f == '4-3-3':
        f_cols1, f_cols2, f_cols3, f_cols4, f_cols5 = st.columns(5)
        m_cols1, m_cols2, m_cols3, m_cols4, m_cols5 = st.columns(5)
        d_cols1, d_cols2, d_cols3, d_cols4 = st.columns(4)
        cols_list = [     f_cols2, f_cols3, f_cols4, 
                            m_cols2, m_cols3, m_cols4, 
                        d_cols1, d_cols2, d_cols3, d_cols4]
    if f == '4-2-3-1':
        f_cols1, f_cols2, f_cols3, f_cols4, f_cols5 = st.columns(5)
        m_cols1_1, m_cols2_1, m_cols3_1, m_cols4_1, m_cols5_1 = st.columns(5)
        m_cols1_2, m_cols2_2, m_cols3_2, m_cols4_2 = st.columns(4)
        d_cols1, d_cols2, d_cols3, d_cols4 = st.columns(4)
        cols_list = [              f_cols3, 
                        m_cols2_1, m_cols3_1, m_cols4_1, 
                                m_cols2_2, m_cols3_2,
                        d_cols1, d_cols2, d_cols3, d_cols4]
    if f == '4-3-1-2':
        f_cols1, f_cols2, f_cols3, f_cols4= st.columns(4)
        m_cols1_1, m_cols2_1, m_cols3_1, m_cols4_1, m_cols5_1 = st.columns(5)
        m_cols1_2, m_cols2_2, m_cols3_2, m_cols4_2, m_cols5_2 = st.columns(5)
        d_cols1, d_cols2, d_cols3, d_cols4 = st.columns(4)
        cols_list = [         f_cols2, f_cols3, 
                                    m_cols3_1,
                        m_cols2_2, m_cols3_2, m_cols4_2,
                        d_cols1, d_cols2, d_cols3, d_cols4]
    if f == '4-2-2-2':
        f_cols1, f_cols2, f_cols3, f_cols4= st.columns(4)
        m_cols1_1, m_cols2_1, m_cols3_1, m_cols4_1, = st.columns(4)
        m_cols1_2, m_cols2_2, m_cols3_2, m_cols4_2, = st.columns(4)
        d_cols1, d_cols2, d_cols3, d_cols4 = st.columns(4)
        cols_list = [         f_cols2, f_cols3, 
                        m_cols1_1,                 m_cols4_1,
                            m_cols2_2, m_cols3_2,
                        d_cols1, d_cols2, d_cols3, d_cols4]
    if f == '4-3-2-1':
        f_cols1, f_cols2, f_cols3, f_cols4, f_cols5 = st.columns(5)
        m_cols1_1, m_cols2_1, m_cols3_1, m_cols4_1 = st.columns(4)
        m_cols1_2, m_cols2_2, m_cols3_2, m_cols4_2, m_cols5_2 = st.columns(5)
        d_cols1, d_cols2, d_cols3, d_cols4 = st.columns(4)
        cols_list = [              f_cols3, 
                                m_cols2_1, m_cols3_1,
                        m_cols2_2, m_cols3_2, m_cols4_2,
                        d_cols1, d_cols2, d_cols3, d_cols4]
    if f == '4-1-4-1':
        f_cols1, f_cols2, f_cols3, f_cols4, f_cols5 = st.columns(5)
        m_cols1_1, m_cols2_1, m_cols3_1, m_cols4_1 = st.columns(4)
        m_cols1_2, m_cols2_2, m_cols3_2, m_cols4_2, m_cols5_2 = st.columns(5)
        d_cols1, d_cols2, d_cols3, d_cols4 = st.columns(4)
        cols_list = [              f_cols3, 
                    m_cols1_1, m_cols2_1, m_cols3_1, m_cols4_1,
                                    m_cols3_2,
                        d_cols1, d_cols2, d_cols3, d_cols4]
    if f == '4-1-2-3':
        f_cols1, f_cols2, f_cols3, f_cols4, f_cols5 = st.columns(5)
        m_cols1_1, m_cols2_1, m_cols3_1, m_cols4_1 = st.columns(4)
        m_cols1_2, m_cols2_2, m_cols3_2, m_cols4_2, m_cols5_2 = st.columns(5)
        d_cols1, d_cols2, d_cols3, d_cols4 = st.columns(4)
        cols_list = [     f_cols2, f_cols3, f_cols4,
                            m_cols2_1, m_cols3_1,
                                    m_cols3_2,
                        d_cols1, d_cols2, d_cols3, d_cols4]
    if f == '4-5-1':
        f_cols1, f_cols2, f_cols3, f_cols4, f_cols5 = st.columns(5)
        m_cols1, m_cols2, m_cols3, m_cols4, m_cols5 = st.columns(5)
        d_cols1, d_cols2, d_cols3, d_cols4 = st.columns(4)
        cols_list = [             f_cols3,
                m_cols1, m_cols2, m_cols3, m_cols4, m_cols5,
                        d_cols1, d_cols2, d_cols3, d_cols4]
    if f == '4-4-1-1':
        f_cols1, f_cols2, f_cols3, f_cols4, f_cols5 = st.columns(5)
        m_cols1_1, m_cols2_1, m_cols3_1, m_cols4_1, m_cols5_1 = st.columns(5)
        m_cols1_2, m_cols2_2, m_cols3_2, m_cols4_2 = st.columns(4)
        d_cols1, d_cols2, d_cols3, d_cols4 = st.columns(4)
        cols_list = [             f_cols3,
                                    m_cols3_1,
                m_cols1_2, m_cols2_2, m_cols3_2, m_cols4_2,
                        d_cols1, d_cols2, d_cols3, d_cols4]
    if f == '3-5-2':
        f_cols1, f_cols2, f_cols3, f_cols4= st.columns(4)
        m_cols1, m_cols2, m_cols3, m_cols4, m_cols5 = st.columns(5)
        d_cols1, d_cols2, d_cols3, d_cols4, d_cols5 = st.columns(5)
        cols_list = [         f_cols2, f_cols3,
                m_cols1, m_cols2, m_cols3, m_cols4, m_cols5,
                            d_cols2, d_cols3, d_cols4]
    if f == '3-4-3':
        f_cols1, f_cols2, f_cols3, f_cols4, f_cols5 = st.columns(5)
        m_cols1, m_cols2, m_cols3, m_cols4= st.columns(4)
        d_cols1, d_cols2, d_cols3, d_cols4, d_cols5 = st.columns(5)
        cols_list = [    f_cols2, f_cols3, f_cols4,
                    m_cols1, m_cols2, m_cols3, m_cols4,
                            d_cols2, d_cols3, d_cols4]
    if f == '3-3-3-1':
        f_cols1, f_cols2, f_cols3, f_cols4, f_cols5 = st.columns(5)
        m_cols1_1, m_cols2_1, m_cols3_1, m_cols4_1, m_cols5_1 = st.columns(5)
        m_cols1_2, m_cols2_2, m_cols3_2, m_cols4_2, m_cols5_2 = st.columns(5)
        d_cols1, d_cols2, d_cols3, d_cols4, d_cols5 = st.columns(5)
        cols_list = [             f_cols3,
                        m_cols2_1, m_cols3_1, m_cols4_1,
                        m_cols2_2, m_cols3_2, m_cols4_2,
                            d_cols2, d_cols3, d_cols4]
    if f == '3-4-1-2':
        f_cols1, f_cols2, f_cols3, f_cols4= st.columns(4)
        m_cols1_1, m_cols2_1, m_cols3_1, m_cols4_1, m_cols5_1 = st.columns(5)
        m_cols1_2, m_cols2_2, m_cols3_2, m_cols4_2 = st.columns(4)
        d_cols1, d_cols2, d_cols3, d_cols4, d_cols5 = st.columns(5)
        cols_list = [         f_cols2, f_cols3,
                                    m_cols3_1,
                    m_cols1_2, m_cols2_2, m_cols3_2, m_cols4_2,
                            d_cols2, d_cols3, d_cols4]
    if f == '3-4-2-1':
        f_cols1, f_cols2, f_cols3, f_cols4, f_cols5 = st.columns(5)
        m_cols1_1, m_cols2_1, m_cols3_1, m_cols4_1= st.columns(4)
        m_cols1_2, m_cols2_2, m_cols3_2, m_cols4_2 = st.columns(4)
        d_cols1, d_cols2, d_cols3, d_cols4, d_cols5 = st.columns(5)
        cols_list = [             f_cols3,
                                m_cols2_1, m_cols3_1,
                    m_cols1_2, m_cols2_2, m_cols3_2, m_cols4_2,
                            d_cols2, d_cols3, d_cols4]
    if f == '5-3-2':
        f_cols1, f_cols2, f_cols3, f_cols4 = st.columns(4)
        m_cols1, m_cols2, m_cols3, m_cols4, m_cols5 = st.columns(5)
        d_cols1, d_cols2, d_cols3, d_cols4, d_cols5 = st.columns(5)
        cols_list = [         f_cols2, f_cols3,
                            m_cols2, m_cols3, m_cols4,
                d_cols1, d_cols2, d_cols3, d_cols4, d_cols5]
    if f == '5-4-1':
        f_cols1, f_cols2, f_cols3, f_cols4, f_cols5  = st.columns(5)
        m_cols1, m_cols2, m_cols3, m_cols4 = st.columns(4)
        d_cols1, d_cols2, d_cols3, d_cols4, d_cols5 = st.columns(5)
        cols_list = [             f_cols3,
                        m_cols1, m_cols2, m_cols3, m_cols4,
                d_cols1, d_cols2, d_cols3, d_cols4, d_cols5]
            
    g_cols1, g_cols2, g_cols3, g_cols4, g_cols5 = st.columns(5)                
    cols_list = cols_list + [g_cols3]
        # final_cols_list.append(cols_list)
    return cols_list