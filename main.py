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

    # أسماء الأيام بالعربي (حسب datetime.weekday())
    days_ar = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
    today_name = days_ar[now.weekday()]

    # قسم التحكم في نقل التاريخ بعدد أيام - الشريط الجانبي
    st.sidebar.header("نقل التاريخ بعدد أيام")
    days_ahead = st.sidebar.number_input("أدخل عدد الأيام للنقل إلى الأمام:", min_value=0, step=1)

    transported_date = now + timedelta(days=days_ahead)
    transported_day_name = days_ar[transported_date.weekday()]

    st.sidebar.markdown(f"**التاريخ بعد {days_ahead} يوم هو:**")

    # عرض التاريخ الميلادي بالتنسيق المطلوب وباتجاه LTR (يسار لليمين)
    st.sidebar.markdown(
        f"<div style='direction: ltr;'>{'- ميلادي: ' + transported_date.strftime('%Y/%m/%d')}</div>",
        unsafe_allow_html=True
    )

    # محاولة حساب التاريخ الهجري وعرضه باتجاه LTR، وإذا فشل (مثلاً بعد أيام كثيرة) لا يظهر
    hijri_str = None
    try:
        hijri_date = HijriDate(transported_date.year, transported_date.month, transported_date.day, gr=True)
        hijri_str = f"- هجري: {hijri_date.day} / {hijri_date.month} / {hijri_date.year}"
    except Exception:
        pass

    if hijri_str:
        st.sidebar.markdown(f"<div style='direction: ltr;'>{hijri_str}</div>", unsafe_allow_html=True)

    # عرض اسم اليوم بحجم كبير وتحته (مركز النص)
    st.sidebar.markdown(
        f"<div style='font-size:28px; font-weight:bold; margin-top:12px; text-align:center;'>{transported_day_name}</div>",
        unsafe_allow_html=True
    )

    # جلب التواريخ الحالية للعرض في الواجهة الرئيسية
    dates = get_dates()

    # عرض الوقت واسم اليوم في أعلى الصفحة الرئيسية
    render_time(time_now, today_name)

    # عرض باقي عناصر واجهة المستخدم في الصفحة الرئيسية
    render_html(dates, months_en, months_ar1, months_ar2, months_hijri, now)

if __name__ == "__main__":
    main()
