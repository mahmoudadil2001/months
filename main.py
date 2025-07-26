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

    # إضافة قائمة اليوم الحالي حتى اليوم المنقول
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
