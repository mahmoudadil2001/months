import streamlit as st
from datetime import datetime, timedelta
from ummalqura.hijri_date import HijriDate
import dateutil.relativedelta

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

    if option == "بعد كذا يوم (تاريخ ميلادي وهجري ويوم)":
        days_ahead = st.sidebar.number_input("أدخل عدد الأيام للنقل إلى الأمام:", min_value=0, step=1)

        transported_date = now + timedelta(days=days_ahead)
        transported_day_name = days_ar[transported_date.weekday()]

        st.sidebar.markdown(f"**التاريخ بعد {days_ahead} يوم هو:**")
        st.sidebar.markdown(f"- ميلادي: {transported_date.strftime('%d-%m-%Y')}")

        try:
            hijri_date = HijriDate(transported_date.year, transported_date.month, transported_date.day, gr=True)
            hijri_str = f"{hijri_date.day} / {hijri_date.month} / {hijri_date.year}"
        except Exception:
            hijri_str = "غير متوفر"

        st.sidebar.markdown(f"- هجري: {hijri_str}")
        st.sidebar.markdown(
            f"<div style='text-align:center; font-size:20px; font-weight:900; color:#0055cc; margin:10px 0;'>{transported_day_name}</div>",
            unsafe_allow_html=True
        )

        if days_ahead <= 210:
            st.sidebar.markdown("### اليوم الحالي حتى اليوم المنقول")
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
        else:
            st.sidebar.warning("⚠️ لا أستطيع قراءة أكثر من 210 يوم")

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

    elif option == "إلى التاريخ والساعة (كم تبقى من يوم وساعة)":
        today_default = now.strftime("%Y/%m/%d")
        time_default = now.strftime("%H:%M")

        date_input_str = st.sidebar.text_input("ادخل التاريخ المستقبلي:", value=today_default)

        col1, col2 = st.sidebar.columns([2, 1])
        time_input_str = col1.text_input("ادخل الساعة:", value=time_default)
        am_pm_choice = col2.selectbox("AM/PM", ["AM", "PM"])

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
                        if am_pm_choice == "PM" and hour < 12:
                            hour += 12
                        elif am_pm_choice == "AM" and hour == 12:
                            hour = 0

                        target_datetime = datetime(year, month, day, hour, minute)
                        diff = target_datetime - now
                        if diff.total_seconds() > 0:
                            days_left = diff.days
                            hours_left = diff.seconds // 3600
                            minutes_left = (diff.seconds % 3600) // 60
                            day_name = days_ar[target_datetime.weekday()]

                            period = "صباحًا" if target_datetime.hour < 12 else "مساءً"
                            time_display = target_datetime.strftime("%I:%M").lstrip("0")

                            st.sidebar.info(
                                f"يتبقى **{days_left} يوم** و **{hours_left} ساعة** و **{minutes_left} دقيقة**\n"
                                f"(يصادف اليوم {day_name} الساعة {time_display} {period})"
                            )
                        else:
                            st.sidebar.warning("⏳ التاريخ والوقت المحددين قد مرا بالفعل.")
                else:
                    st.sidebar.error("⚠️ صيغة التاريخ غير صحيحة.")
            except ValueError:
                st.sidebar.error("⚠️ صيغة التاريخ غير صحيحة.")

    elif option == "تحويل بين تاريخين":
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

            diff_seconds = (dt2 - dt1).total_seconds()
            direction = "بعد" if diff_seconds > 0 else "قبل"

            diff = dateutil.relativedelta.relativedelta(dt2, dt1) if diff_seconds >= 0 else dateutil.relativedelta.relativedelta(dt1, dt2)

            years = diff.years
            months = diff.months
            days = diff.days
            hours = diff.hours
            minutes = diff.minutes

            total_days = abs((dt2 - dt1).days)

            parts = []
            if years > 0:
                parts.append(f"**{years} سنة**")
            if months > 0:
                parts.append(f"**{months} شهر**")
            if days > 0:
                parts.append(f"**{days} يوم**")
            if hours > 0:
                parts.append(f"**{hours} ساعة**")
            if minutes > 0:
                parts.append(f"**{minutes} دقيقة**")

            if not parts:
                parts.append("0 دقيقة")

            result_text = f"{direction} " + " و ".join(parts) + f"\n(الإجمالي: {total_days} يوم)"

            st.sidebar.success(result_text)

    dates = get_dates()
    render_time(time_now, today_name)
    render_html(dates, months_en, months_ar1, months_ar2, months_hijri, now)


if __name__ == "__main__":
    main()
