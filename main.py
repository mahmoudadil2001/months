from dateutil.relativedelta import relativedelta  # تحتاج تثبيت مكتبة dateutil

elif option == "تحويل بين تاريخين":
    import dateutil.relativedelta

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

        # الفرق الكلي بالثواني
        diff_seconds = (dt2 - dt1).total_seconds()
        direction = "بعد" if diff_seconds > 0 else "قبل"

        # نحسب الفرق باستخدام relativedelta للحصول على سنوات، شهور، أيام، ساعات، دقائق
        diff = relativedelta.relativedelta(dt2, dt1) if diff_seconds >= 0 else relativedelta.relativedelta(dt1, dt2)

        years = diff.years
        months = diff.months
        days = diff.days
        hours = diff.hours
        minutes = diff.minutes

        # الفرق الكلي بالأيام (بالعدد المطلق)
        total_days = abs((dt2 - dt1).days)

        # صياغة النص بمرونة حسب القيم الموجودة (مثلاً لو سنة=0 لا تظهر)
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
