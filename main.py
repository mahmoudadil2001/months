import streamlit as st
from datetime import datetime
from ummalqura.hijri_date import HijriDate

from data import get_dates, months_en, months_ar1, months_ar2, months_hijri
from ui_time import render_time
from ui_render import render_html

def main():
    st.set_page_config(page_title="التقويم الميلادي والهجري", layout="centered")

    # الوقت الحالي
    now = datetime.now()
    time_now = now.strftime("%I:%M %p").lower()

    # التاريخ الميلادي والهجري
    dates = get_dates()

    # عرض الوقت
    render_time(time_now)

    # عرض المحتوى (HTML + CSS + JS)
    render_html(dates, months_en, months_ar1, months_ar2, months_hijri, now)

if __name__ == "__main__":
    main()
