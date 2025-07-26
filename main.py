import streamlit as st
from datetime import datetime, timedelta
from ummalqura.hijri_date import HijriDate

from data import get_dates, months_en, months_ar1, months_ar2, months_hijri
from ui_time import render_time
from ui_render import render_html

def parse_time_input(time_str):
    time_str = time_str.strip()
    if ":" in time_str:
        parts = time_str.split(":")
        if len(parts) == 2:
            try:
                hour = int(parts[0])
                minute = int(parts[1])
                if 0 <= hour < 24 and 0 <= minute < 60:
                    return hour, minute
            except:
                return None
        return None
    else:
        try:
            hour = int(time_str)
            if 0 <= hour < 24:
                return hour, 0
        except:
            return None
    return None

def main():
    st.set_page_config(page_title="التقويم الميلادي والهجري", layout="centered")

    now = datetime.utcnow() + timedelta(hours=3)
    time_now = now.strftime("%I:%M %p").lower()

    days_ar = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
    today_name = days_ar[now.weekday()]

    # ======================== القائمة الجانبية ========================
    st.sidebar.header("حسابات التاريخ والوقت")

    # جزء 1: نقل التاريخ بعدد أيام (من الكود السابق)
    days_ahead = st.sidebar.number_input("أدخل عدد الأيام للنقل إلى الأمام:", min_value=0, step=1)

    transported_date = now + timedelta(days=days_ahead)
    transported_day_name = days_ar[transported_date.weekday()]

    st.sidebar.markdown(f"**التاريخ بعد {days_ahead} يوم هو:**")
    st.sidebar.markdown(
        f"<div style='direction:ltr;'>- ميلادي: {transported_date.strftime('%Y/%m/%d')}</div>",
        unsafe_allow_html=True
    )

    try:
        hijri_date = HijriDate(transported_date.year, transported_date.month, transported_date.day, gr=True)
        hijri_str = f"{hijri_date.day} / {hijri_date.month} / {hijri_date.year}"
    except Exception:
        hijri_str = "غير متوفر"

    st.sidebar.markdown(
        f"<div style='direction:ltr;'>- هجري: {hijri_str}</div>",
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        f"<div style='text-align:center; font-size:26px; font-weight:900; color:#0055cc; margin:10px 0;'>{transported_day_name}</div>",
        unsafe_allow_html=True
    )

    if days_ahead > 210:
        st.sidebar.warning("⚠️ لا أستطيع قراءة أكثر من 210 يوم")
    else:
        with st.sidebar.expander("اليوم الحالي حتى اليوم المنقول", expanded=False):
            total_days = days_ahead + 1

            def start_of_week(date):
                weekday = (date.weekday() + 1) % 7
                return date - timedelta(days=weekday)

            weeks_dict = {}
            for i in range(total_days):
                current_day = now + timedelta(days=i)
                sow = start_of_week(current_day)
                weeks_dict.setdefault(sow, []).append(current_day)

            sorted_weeks = sorted(weeks_dict.items())

            for week_num, (_, days_list) in enumerate(sorted_weeks, start=1):
                for day_date in days_list:
                    day_name = days_ar[day_date.weekday()]
                    st.sidebar.markdown(
                        f"<div style='direction:ltr; font-weight:600;'>{day_date.strftime('%Y/%m/%d')} - {day_name}</div>",
                        unsafe_allow_html=True
                    )

                st.sidebar.markdown(
                    f"<div style='font-weight:700; text-align:center; margin-top:4px;'>الأسبوع {week_num}</div>",
                    unsafe_allow_html=True
                )
                st.sidebar.markdown("<hr style='margin-top:2px; margin-bottom:10px;'>", unsafe_allow_html=True)

    # جزء 2 و 3: حسابات التاريخ والوقت الثلاثة ضمن sidebar باستخدام Radio لاختيار العملية
    option = st.sidebar.radio(
        "اختر العملية",
        ["بعد كذا يوم (تاريخ ميلادي وهجري ويوم)",
         "بعد كذا يوم وساعة (تاريخ ويوم وساعة)",
         "إلى التاريخ والساعة (كم تبقى من يوم وساعة)"],
        index=0
    )

    # نستخدم المتغير now بنفس القيمة مع التوقيت المحلي +3 كما في الكود الرئيسي

    if option == "بعد كذا يوم (تاريخ ميلادي وهجري ويوم)":
        days_ahead_2 = st.sidebar.number_input("أدخل عدد الأيام للنقل إلى الأمام (الحساب الثاني):", min_value=0, step=1, key="days_ahead_2")

        transported_date_2 = now + timedelta(days=days_ahead_2)
        transported_day_name_2 = days_ar[transported_date_2.weekday()]

        st.sidebar.markdown(f"**التاريخ بعد {days_ahead_2} يوم هو:**")
        st.sidebar.markdown(f"- ميلادي: {transported_date_2.strftime('%d-%m-%Y')}")

        try:
            hijri_date_2 = HijriDate(transported_date_2.year, transported_date_2.month, transported_date_2.day, gr=True)
            hijri_str_2 = f"{hijri_date_2.day} / {hijri_date_2.month} / {hijri_date_2.year}"
        except Exception:
            hijri_str_2 = "غير متوفر"

        st.sidebar.markdown(f"- هجري: {hijri_str_2}")
        st.sidebar.markdown(
            f"<div style='text-align:center; font-size:20px; font-weight:900; color:#0055cc; margin:10px 0;'>{transported_day_name_2}</div>",
            unsafe_allow_html=True
        )

    elif option == "بعد كذا يوم وساعة (تاريخ ويوم وساعة)":
        days_input = st.sidebar.number_input("أدخل عدد الأيام:", min_value=0, step=1, key="days_input")
        hours_input = st.sidebar.number_input("أدخل عدد الساعات:", min_value=0, max_value=23, step=1, key="hours_input")

        future_time = now + timedelta(days=days_input, hours=hours_input)
        day_name = days_ar[future_time.weekday()]
        date_str = future_time.strftime("%d-%m-%Y")
        period = "صباحًا" if future_time.hour < 12 else "مساءً"
        time_str = future_time.strftime("%I:%M").lstrip("0")

        st.sidebar.success(
            f"بعد {days_input} يوم و {hours_input} ساعة سيكون اليوم **{day_name}** والتاريخ **{date_str}** والوقت حوالي **{time_str} {period}**"
        )

    elif option == "إلى التاريخ والساعة (كم تبقى من يوم وساعة)":
        today_default = now.strftime("%Y/%m/%d")
        time_default = now.strftime("%H:%M")

        date_input_str = st.sidebar.text_input("ادخل التاريخ المستقبلي:", value=today_default, key="date_input")
        time_input_str = st.sidebar.text_input("ادخل الساعة:", value=time_default, key="time_input")

        if date_input_str and time_input_str:
            try:
                parts = date_input_str.replace("-", "/").split("/")
                if len(parts) == 3:
                    year, month, day = map(int, parts)
                    parsed_time = parse_time_input(time_input_str)
                    if parsed_time is None:
                        st.sidebar.error("⚠️ صيغة الوقت غير صحيحة.")
                    else:
                        hour, minute = parsed_time
                        target_datetime = datetime(year, month, day, hour, minute)
                        diff = target_datetime - now
                        if diff.total_seconds() > 0:
                            days_left = diff.days
                            hours_left = diff.seconds // 3600
                            minutes_left = (diff.seconds % 3600) // 60
                            day_name = days_ar[target_datetime.weekday()]
                            st.sidebar.info(f"يتبقى **{days_left} يوم** و **{hours_left} ساعة** و **{minutes_left} دقيقة** (يصادف يوم {day_name})")
                        else:
                            st.sidebar.warning("⏳ التاريخ والوقت المحددين قد مرا بالفعل.")
                else:
                    st.sidebar.error("⚠️ صيغة التاريخ غير صحيحة.")
            except ValueError:
                st.sidebar.error("⚠️ صيغة التاريخ غير صحيحة.")

    # ======================== نهاية القائمة الجانبية ========================

    # عرض المحتوى الأساسي بالصفحة
    dates = get_dates()
    render_time(time_now, today_name)
    render_html(dates, months_en, months_ar1, months_ar2, months_hijri, now)

if __name__ == "__main__":
    main()
