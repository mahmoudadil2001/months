import streamlit as st

def render_time(time_now, today_name):
    st.markdown(f'''
        <div style="
            width: 100%;
            text-align: center;
            margin-bottom: 30px;
        ">
            <div style="
                font-size: 48px;
                font-weight: 700;
                direction: ltr;
                margin-bottom: 5px;
            ">
                ⏰ {time_now}
            </div>
            <div style="
                font-size: 28px;
                color: #444;
                font-weight: 600;
                direction: rtl;
            ">
                {today_name}
            </div>
        </div>
    ''', unsafe_allow_html=True)
