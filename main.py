import streamlit as st
from datetime import datetime, timedelta
from ummalqura.hijri_date import HijriDate

from data import get_dates, months_en, months_ar1, months_ar2, months_hijri
from ui_time import render_time
from ui_render import render_html

def main():
    st.set_page_config(page_title="التقويم الميلادي والهجري", layout="centered")

    # الوقت الحالي بتوقيت العراق (+3 ساعات عن UTC)
    now = datetime.utcnow() + timedelta(hours=3)
    time_now = now.strftime("%I:%M %p").lower()

    # أسماء الأيام بالعربية (بدءاً من الاثنين حسب datetime.weekday())
    days_ar = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]

    st.sidebar.header("نقل التاريخ بعدد أيام")
    days_ahead = st.sidebar.number_input("أدخل عدد الأيام للنقل إلى الأمام:", min_value=0, step=1)

    transported_date = now + timedelta(days=days_ahead)
    transported_day_name = days_ar[transported_date.weekday()]

    st.sidebar.markdown(f"**التاريخ بعد {days_ahead} يوم هو:**")
    st.sidebar.markdown(f"- ميلادي: {transported_date.strftime('%Y-%m-%d')} ({transported_day_name})")

    # حساب التاريخ الهجري للتاريخ المنقول
    transported_hijri = HijriDate(transported_date.year, transported_date.month, transported_date.day, gr=True)
    st.sidebar.markdown(f"- هجري: {transported_hijri.day} / {transported_hijri.month} / {transported_hijri.year}")

    # الحصول على التواريخ الحالية (اليوم الفعلي)
    dates = get_dates()

    # عرض الوقت في أعلى الصفحة
    render_time(time_now)

    # عرض التاريخين الحالي والمنقول + اسم اليوم المنقول تحتهم
    render_html(
        dates, months_en, months_ar1, months_ar2, months_hijri, now,
        transported_date=transported_date,
        transported_day_name=transported_day_name,
        transported_hijri=transported_hijri
    )

if __name__ == "__main__":
    main()
