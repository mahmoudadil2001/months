import streamlit as st
from datetime import datetime, timedelta
from ummalqura.hijri_date import HijriDate

from data import get_dates, months_en, months_ar1, months_ar2, months_hijri
from ui_time import render_time
from ui_render import render_html

def main():
    st.set_page_config(page_title="التقويم الميلادي والهجري", layout="centered")

    now = datetime.utcnow() + timedelta(hours=3)
    time_now = now.strftime("%I:%M %p").lower()

    days_ar = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]

    st.sidebar.header("نقل التاريخ بعدد أيام")
    days_ahead = st.sidebar.number_input("أدخل عدد الأيام للنقل إلى الأمام:", min_value=0, step=1)

    transported_date = now + timedelta(days=days_ahead)
    transported_day_name = days_ar[transported_date.weekday()]

    st.sidebar.markdown(
        f"<div style='direction: ltr; font-weight: 700; margin-top: 15px;'>التاريخ بعد {days_ahead} يوم هو:</div>",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        f"<div style='direction: ltr; font-size: 18px;'>- ميلادي: {transported_date.strftime('%Y/%m/%d')}</div>",
        unsafe_allow_html=True,
    )

    try:
        hijri_date = HijriDate(transported_date.year, transported_date.month, transported_date.day, gr=True)
        hijri_str = f"- هجري: {hijri_date.day} / {hijri_date.month} / {hijri_date.year}"
        st.sidebar.markdown(f"<div style='direction: ltr; font-size: 18px;'>{hijri_str}</div>", unsafe_allow_html=True)
    except Exception:
        pass

    st.sidebar.markdown(
        f"<div style='direction: rtl; font-size: 24px; font-weight: 800; margin-top: 10px; color: #444;'>{transported_day_name}</div>",
        unsafe_allow_html=True,
    )

    with st.sidebar.expander("عرض الأيام من اليوم الحالي حتى اليوم المنقول", expanded=False):
        total_days = days_ahead + 1
        weeks = (total_days + 6) // 7  # حساب عدد الأسابيع

        for w in range(weeks):
            start_day = w * 7
            end_day = min(start_day + 7, total_days)
            st.markdown(f"<div style='font-weight: 700; margin-top: 10px; border-top: 2px solid #888;'>الأسبوع {w + 1}</div>", unsafe_allow_html=True)
            for i in range(start_day, end_day):
                day_date = now + timedelta(days=i)
                day_name = days_ar[day_date.weekday()]
                st.markdown(f"<div style='direction: ltr; font-weight: 600;'>{day_date.strftime('%Y/%m/%d')} - {day_name}</div>", unsafe_allow_html=True)

    dates = get_dates()
    today_name = days_ar[now.weekday()]
    render_time(time_now, today_name)
    render_html(dates, months_en, months_ar1, months_ar2, months_hijri, now)

if __name__ == "__main__":
    main()
