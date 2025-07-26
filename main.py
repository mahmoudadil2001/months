import streamlit as st
from datetime import datetime, timedelta
from ummalqura.hijri_date import HijriDate

from data import get_dates, months_en, months_ar1, months_ar2, months_hijri
from ui_time import render_time
from ui_render import render_html

def main():
    st.set_page_config(page_title="التقويم الميلادي والهجري", layout="centered")

    # الحصول على الوقت الحالي بتوقيت العراق (+3 ساعات عن UTC)
    now = datetime.utcnow() + timedelta(hours=3)
    time_now = now.strftime("%I:%M %p").lower()

    # أسماء الأيام بالعربية
    days_ar = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
    today_name = days_ar[now.weekday()]

    # قسم التحكم في نقل التاريخ بعدد أيام
    st.sidebar.header("نقل التاريخ بعدد أيام")
    days_ahead = st.sidebar.number_input("أدخل عدد الأيام للنقل إلى الأمام:", min_value=0, step=1)

    transported_date = now + timedelta(days=days_ahead)

    # عرض التاريخ المنقول في الشريط الجانبي مع ترتيب التاريخ ميلادي yyyy/mm/dd من اليسار لليمين
    st.sidebar.markdown(
        f"""<div style='direction: ltr; unicode-bidi: embed;'>
            **التاريخ بعد {days_ahead} يوم هو:**
        </div>""",
        unsafe_allow_html=True
    )
    st.sidebar.markdown(
        f"""<div style='direction: ltr; unicode-bidi: embed;'>
            - ميلادي: {transported_date.strftime('%Y/%m/%d')}
        </div>""",
        unsafe_allow_html=True
    )

    # حساب التاريخ الهجري للتاريخ المنقول مع معالجة الخطأ عند الأيام الكبيرة
    try:
        hijri_date = HijriDate(transported_date.year, transported_date.month, transported_date.day, gr=True)
        hijri_str = f"- هجري: {hijri_date.day} / {hijri_date.month} / {hijri_date.year}"
    except Exception:
        hijri_str = ""  # عند الخطأ لا نعرض شيء

    if hijri_str:
        st.sidebar.markdown(
            f"""<div style='direction: ltr; unicode-bidi: embed;'>
                {hijri_str}
            </div>""",
            unsafe_allow_html=True
        )

    # جلب التواريخ الحالية لعرضها في الواجهة
    dates = get_dates()

    # عرض الوقت واسم اليوم في أعلى الصفحة
    render_time(time_now, today_name)

    # عرض باقي عناصر واجهة المستخدم
    render_html(dates, months_en, months_ar1, months_ar2, months_hijri, now)

if __name__ == "__main__":
    main()
