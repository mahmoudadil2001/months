import streamlit as st
from datetime import datetime, timedelta

from date_utils import get_hijri_date, calc_date_difference
from data import get_dates, months_en, months_ar1, months_ar2, months_hijri
from ui_time import render_time
from ui_render import render_html


def main():
    st.set_page_config(page_title="التقويم الميلادي والهجري", layout="centered")

    now = datetime.utcnow() + timedelta(hours=3)
    time_now = now.strftime("%I:%M %p").lower()

    days_ar = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
    today_name = days_ar[now.weekday()]

    option = st.sidebar.selectbox(
        "",
        [
            "بعد كذا يوم (تاريخ ميلادي وهجري ويوم)",
            "بعد كذا يوم وساعة (تاريخ ويوم وساعة)",
            "إلى التاريخ والساعة (كم تبقى من يوم وساعة)",
            "تحويل بين تاريخين"
        ],
        index=0,
    )

    # باقي الخيارات كما في كودك الأساسي...
    # هنا فقط سأضع الكود الخاص بتحويل بين تاريخين مع استخدام الدوال من date_utils.py

    if option == "تحويل بين تاريخين":
        default_date = datetime.now().date()
        default_time = datetime.now().time()

        st.sidebar.markdown("### 📆 اختر التاريخين")

        date1 = st.sidebar.date_input("التاريخ الأول", value=default_date)
        time1 = st.sidebar.time_input("الوقت الأول", value=default_time)

        date2 = st.sidebar.date_input("التاريخ الثاني", value=default_date)
        time2 = st.sidebar.time_input("الوقت الثاني", value=default_time)

        if st.sidebar.button("احسب الفرق"):
            dt1 = datetime.combine(date1, time1)
            dt2 = datetime.combine(date2, time2)

            diff_info = calc_date_difference(dt1, dt2)

            parts = []
            if diff_info["years"] > 0:
                parts.append(f"**{diff_info['years']} سنة**")
            if diff_info["months"] > 0:
                parts.append(f"**{diff_info['months']} شهر**")
            if diff_info["days"] > 0:
                parts.append(f"**{diff_info['days']} يوم**")
            if diff_info["hours"] > 0:
                parts.append(f"**{diff_info['hours']} ساعة**")
            if diff_info["minutes"] > 0:
                parts.append(f"**{diff_info['minutes']} دقيقة**")

            if not parts:
                parts.append("0 دقيقة")

            result_text = f"{diff_info['direction']} " + " و ".join(parts) + f"\n(الإجمالي: {diff_info['total_days']} يوم)"

            st.sidebar.success(result_text)

            # عرض يوم الأسبوع والوقت بنمط 12 ساعة للتاريخ الثاني
            day_name = days_ar[dt2.weekday()]
            period = "صباحًا" if dt2.hour < 12 else "مساءً"
            time_display = dt2.strftime("%I:%M").lstrip("0")

            st.sidebar.markdown(f"يصادف اليوم: **{day_name}** والساعة: **{time_display} {period}**")

            # حساب وعرض التاريخ الهجري للتاريخ الثاني
            hijri_str = get_hijri_date(dt2)
            st.sidebar.markdown(f"التاريخ الهجري: **{hijri_str}**")

    # هنا ضع باقي كود الخيارات الأخرى الخاصة بك كما في main.py الأصلي
    # مثل "بعد كذا يوم (تاريخ ميلادي وهجري ويوم)"، "بعد كذا يوم وساعة" و "إلى التاريخ والساعة"...

    dates = get_dates()
    render_time(time_now, today_name)
    render_html(dates, months_en, months_ar1, months_ar2, months_hijri, now)


if __name__ == "__main__":
    main()
