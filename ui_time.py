import streamlit as st

def render_time(time_now):
    st.markdown(f'''
        <div style="
            width: 100%;
            text-align: center;
            font-size: 28px;
            font-weight: 700;
            direction: ltr;
            margin-bottom: 30px;
        ">
            ⏰ {time_now}
        </div>
    ''', unsafe_allow_html=True)
