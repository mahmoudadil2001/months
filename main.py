import streamlit as st
from datetime import datetime, timedelta
from convertdate import islamic

from date_utils import get_hijri_date, calc_date_difference
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
    else:
        try:
            hour = int(time_str)
            if 0 <= hour < 24:
                return hour, 0
        except:
            return None
    return None


def parse_date_input(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
    except:
        return None


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
            "تحويل بين تاريخين",
            "هجري إلى ميلادي"
        ],
        index=0,
    )

    # 🔹 1) بعد كذا يوم
    if option == "بعد كذا يوم (تاريخ ميلادي وهجري ويوم)":
        days_ahead = st.sidebar.number_input("أدخل عدد الأيام للنقل إلى الأمام:", min_value=0, step=1)
        transported_date = now + timedelta(days=days_ahead)
        transported_day_name = days_ar[transported_date.weekday()]

        st.sidebar.markdown(f"**التاريخ بعد {days_ahead} يوم هو:**")
        st.sidebar.markdown(f"- ميلادي: {transported_date.strftime('%d-%m-%Y')}")
        hijri_str = get_hijri_date(transported_date)
        st.sidebar.markdown(f"- هجري: {hijri_str}")
        st.sidebar.markdown(
            f"<div style='text-align:center; font-size:20px; font-weight:900; color:#0055cc; margin:10px 0;'>{transported_day_name}</div>",
            unsafe_allow_html=True
        )

    # 🔹 2) بعد كذا يوم وساعة
    elif option == "بعد كذا يوم وساعة (تاريخ ويوم وساعة)":
        days_input = st.sidebar.number_input("أدخل عدد الأيام:", min_value=0, step=1)
        hours_input = st.sidebar.number_input("أدخل عدد الساعات:", min_value=0, max_value=23, step=1)
        future_time = now + timedelta(days=days_input, hours=hours_input)
        day_name = days_ar[future_time.weekday()]
        date_str = future_time.strftime("%d-%m-%Y")
        period = "صباحًا" if future_time.hour < 12 else "مساءً"
        time_str = future_time.strftime("%I:%M").lstrip("0")
        st.sidebar.success(
            f"بعد {days_input} يوم و {hours_input} ساعة سيكون اليوم **{day_name}** والتاريخ **{date_str}** والوقت حوالي **{time_str} {period}**"
        )

    # 🔹 3) إلى التاريخ والساعة
    elif option == "إلى التاريخ والساعة (كم تبقى من يوم وساعة)":
        today_default = now.strftime("%Y-%m-%d")
        time_default = now.strftime("%H:%M")
        date_input_str = st.sidebar.text_input("ادخل التاريخ المستقبلي (YYYY-MM-DD):", value=today_default)

        col1, col2 = st.sidebar.columns([2, 1])
        time_input_str = col1.text_input("ادخل الساعة:", value=time_default)
        am_pm_choice = col2.selectbox("AM/PM", ["AM", "PM"])

        target_date = parse_date_input(date_input_str)
        parsed_time = parse_time_input(time_input_str)

        if target_date and parsed_time:
            hour, minute = parsed_time
            if am_pm_choice == "PM" and hour < 12:
                hour += 12
            elif am_pm_choice == "AM" and hour == 12:
                hour = 0

            target_datetime = datetime.combine(target_date, datetime.min.time()) + timedelta(hours=hour, minutes=minute)
            diff = target_datetime - now
            if diff.total_seconds() > 0:
                st.sidebar.info(f"يتبقى {diff.days} يوم و {diff.seconds//3600} ساعة و {(diff.seconds%3600)//60} دقيقة")
            else:
                st.sidebar.warning("⏳ التاريخ والوقت المحددين قد مرا بالفعل.")
        else:
            st.sidebar.error("⚠️ صيغة التاريخ أو الوقت غير صحيحة.")

    # 🔹 4) تحويل بين تاريخين
    elif option == "تحويل بين تاريخين":
        st.sidebar.markdown("### 📆 أدخل التاريخين يدويًا (YYYY-MM-DD)")

        date1_str = st.sidebar.text_input("التاريخ الأول:", value=now.strftime("%Y-%m-%d"))
        time1_str = st.sidebar.text_input("الوقت الأول (HH:MM):", value=now.strftime("%H:%M"))

        date2_str = st.sidebar.text_input("التاريخ الثاني:", value=now.strftime("%Y-%m-%d"))
        time2_str = st.sidebar.text_input("الوقت الثاني (HH:MM):", value=now.strftime("%H:%M"))

        if st.sidebar.button("احسب الفرق"):
            d1 = parse_date_input(date1_str)
            d2 = parse_date_input(date2_str)
            t1 = parse_time_input(time1_str)
            t2 = parse_time_input(time2_str)

            if d1 and d2 and t1 and t2:
                dt1 = datetime.combine(d1, datetime.min.time()) + timedelta(hours=t1[0], minutes=t1[1])
                dt2 = datetime.combine(d2, datetime.min.time()) + timedelta(hours=t2[0], minutes=t2[1])

                diff_info = calc_date_difference(dt1, dt2)

                parts = []
                if diff_info["years"]: parts.append(f"**{diff_info['years']} سنة**")
                if diff_info["months"]: parts.append(f"**{diff_info['months']} شهر**")
                if diff_info["days"]: parts.append(f"**{diff_info['days']} يوم**")
                if diff_info["hours"]: parts.append(f"**{diff_info['hours']} ساعة**")
                if diff_info["minutes"]: parts.append(f"**{diff_info['minutes']} دقيقة**")

                if not parts:
                    parts.append("0 دقيقة")

                st.sidebar.success(
                    f"{diff_info['direction']} " + " و ".join(parts) +
                    f"\n(الإجمالي: {diff_info['total_days']} يوم)"
                )

                day_name = days_ar[dt2.weekday()]
                period = "صباحًا" if dt2.hour < 12 else "مساءً"
                time_display = dt2.strftime("%I:%M").lstrip("0")

                st.sidebar.markdown(f"يصادف اليوم: **{day_name}** والساعة: **{time_display} {period}**")

                hijri_str = get_hijri_date(dt2)
                st.sidebar.markdown(f"التاريخ الهجري: **{hijri_str}**")
            else:
                st.sidebar.error("⚠️ تحقق من صيغة التواريخ والأوقات.")

    # 🔹 5) هجري إلى ميلادي
    elif option == "هجري إلى ميلادي":
        st.sidebar.markdown("### ✨ أدخل التاريخ الهجري (YYYY/MM/DD)")

        hijri_input = st.sidebar.text_input("التاريخ الهجري:", value="1445/01/01")

        if st.sidebar.button("تحويل"):
            try:
                parts = hijri_input.strip().split("/")
                if len(parts) == 3:
                    hy, hm, hd = map(int, parts)
                    g_year, g_month, g_day = islamic.to_gregorian(hy, hm, hd)
                    g_date = datetime(g_year, g_month, g_day)

                    day_name = days_ar[g_date.weekday()]
                    st.sidebar.success(
                        f"📅 التاريخ الميلادي: **{g_date.strftime('%Y-%m-%d')}**\n"
                        f"🗓️ اليوم: **{day_name}**"
                    )
                else:
                    st.sidebar.error("⚠️ الصيغة يجب أن تكون YYYY/MM/DD")
            except:
                st.sidebar.error("⚠️ تحقق من صيغة التاريخ.")


    dates = get_dates()
    render_time(time_now, today_name)
    render_html(dates, months_en, months_ar1, months_ar2, months_hijri, now)


if __name__ == "__main__":
    main()
