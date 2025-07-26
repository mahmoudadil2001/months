import streamlit as st

def render_time(time_now, today_name):
    st.markdown(
        f"""
        <div style='text-align: center; margin-bottom: 20px;'>
            <h1 style='font-size: 48px; margin: 0;'>{time_now}</h1>
            <h2 style='font-size: 28px; color: #444; margin: 5px 0;'>{today_name}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
