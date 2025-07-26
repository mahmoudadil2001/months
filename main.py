with st.sidebar.expander("عرض الأيام من اليوم الحالي حتى اليوم المنقول", expanded=False):
    total_days = days_ahead + 1
    weeks = (total_days + 6) // 7  # حساب عدد الأسابيع

    for w in range(weeks):
        start_day = w * 7
        end_day = min(start_day + 7, total_days)
        st.markdown(f"<div style='font-weight: 700; margin-top: 10px; border-top: 2px solid #888;'>الأسبوع {w + 1}</div>", unsafe_allow_html=True)
        for i in range(start_day, end_day):
            day_date = now + timedelta(days=i)
            day_name = days_ar[day_date.weekday()]
            st.markdown(f"<div style='direction: ltr; font-weight: 600;'>{day_date.strftime('%Y/%m/%d')} - {day_name}</div>", unsafe_allow_html=True)
