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
    today_name = days_ar[now.weekday()]

    st.sidebar.header("نقل التاريخ بعدد أيام")
    days_ahead = st.sidebar.number_input("أدخل عدد الأيام للنقل إلى الأمام:", min_value=0, step=1)

    transported_date = now + timedelta(days=days_ahead)

    st.sidebar.markdown(f"**التاريخ بعد {days_ahead} يوم هو:**")
    st.sidebar.markdown(f"<div style='direction: ltr;'>- ميلادي: {transported_date.strftime('%Y/%m/%d')}</div>", unsafe_allow_html=True)

    try:
        hijri_date = HijriDate(transported_date.year, transported_date.month, transported_date.day, gr=True)
        hijri_str = f"{hijri_date.day} / {hijri_date.month} / {hijri_date.year}"
    except Exception:
        hijri_str = "غير متوفر"

    st.sidebar.markdown(f"<div style='direction: ltr;'>- هجري: {hijri_str}</div>", unsafe_allow_html=True)

    with st.sidebar.expander("من اليوم الحالي حتى اليوم المنقول", expanded=False):
        total_days = days_ahead + 1
        
        # دالة لمساعدتك على تحديد بداية الأسبوع (الأحد) لكل يوم
        def start_of_week(date):
            # weekday(): الاثنين=0 ... الأحد=6
            # نريد الأحد=0، لذا نحول الأحد ليكون بداية الأسبوع
            weekday = (date.weekday() + 1) % 7  # الأحد = 0, الاثنين=1, ...
            return date - timedelta(days=weekday)

        # جمع الأيام في قوائم حسب الأسبوع
        weeks_dict = {}
        for i in range(total_days):
            current_day = now + timedelta(days=i)
            sow = start_of_week(current_day)
            weeks_dict.setdefault(sow, []).append(current_day)

        # ترتيب الأسابيع تصاعديًا حسب تاريخ بداية الأسبوع
        sorted_weeks = sorted(weeks_dict.items())

        for week_num, (week_start, days_list) in enumerate(sorted_weeks, start=1):
            # عنوان الأسبوع فوق الخط
            st.markdown(f"<div style='font-weight: 700; margin-top: 10px; border-bottom: 2px solid #888;'>الأسبوع {week_num} (ابتداءً من {week_start.strftime('%Y/%m/%d')})</div>", unsafe_allow_html=True)
            for day_date in days_list:
                day_name = days_ar[day_date.weekday()]
                st.markdown(f"<div style='direction: ltr; font-weight: 600;'>{day_date.strftime('%Y/%m/%d')} - {day_name}</div>", unsafe_allow_html=True)

    dates = get_dates()

    render_time(time_now, today_name)
    render_html(dates, months_en, months_ar1, months_ar2, months_hijri, now)

if __name__ == "__main__":
    main()
