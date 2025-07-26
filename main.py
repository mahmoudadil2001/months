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

    # أسماء الأيام بالعربي (حسب datetime.weekday() يبدأ الإثنين = 0)
    days_ar = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
    today_name = days_ar[now.weekday()]

    # قسم الشريط الجانبي للتحكم في نقل التاريخ بعدد أيام
    st.sidebar.header("نقل التاريخ بعدد أيام")
    days_ahead = st.sidebar.number_input("أدخل عدد الأيام للنقل إلى الأمام:", min_value=0, step=1)

    transported_date = now + timedelta(days=days_ahead)
    transported_day_name = days_ar[transported_date.weekday()]

    # عرض التاريخ المنقول في الشريط الجانبي
    st.sidebar.markdown(f"**التاريخ بعد {days_ahead} يوم هو:**")
    st.sidebar.markdown(f"- ميلادي: {transported_date.strftime('%Y-%m-%d')}")
    hijri_date = HijriDate(transported_date.year, transported_date.month, transported_date.day, gr=True)
    st.sidebar.markdown(f"- هجري: {hijri_date.day} / {hijri_date.month} / {hijri_date.year}")

    # عرض اسم اليوم الناتج تحت التواريخ بحجم كبير وواضح
    st.sidebar.markdown(
        f'<div style="font-size: 28px; font-weight: 700; color: #2c3e50; margin-top: 15px; text-align: center;">'
        f'{transported_day_name}'
        f'</div>', unsafe_allow_html=True
    )

    # الحصول على التواريخ الحالية لعرضها في الواجهة الرئيسية
    dates = get_dates()

    # عرض الوقت واسم اليوم الحالي في أعلى الصفحة الرئيسية
    render_time(time_now, today_name)

    # عرض باقي عناصر الواجهة الرئيسية (التواريخ فقط، بدون اسم اليوم هناك)
    render_html(dates, months_en, months_ar1, months_ar2, months_hijri, now)

if __name__ == "__main__":
    main()
