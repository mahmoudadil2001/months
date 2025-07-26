import streamlit as st
from datetime import datetime, timedelta

# إذا كانت مكتبة التحويل للهجري موجودة
try:
    from hijri_converter import convert
    hijri_available = True
except ImportError:
    hijri_available = False

st.set_page_config(page_title="حاسبة التاريخ", layout="centered")
st.title("🗓️ حاسبة اليوم والتاريخ")

# الوقت والتاريخ الحالي
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
current_day = now.strftime("%A")  # 👈 هذا اليوم الحالي
current_date = now.strftime("%Y-%m-%d")

# ترتيب العرض
st.markdown(f"### 🕒 الوقت الحالي: **{current_time}**")
st.markdown(f"### 📆 اليوم الحالي: **{current_day}**")  # 👈 هذا بين الوقت والتاريخ
st.markdown(f"### 📅 التاريخ الميلادي: **{current_date}**")

if hijri_available:
    hijri_today = convert.Gregorian(now.year, now.month, now.day).to_hijri()
    st.markdown(f"### 🕌 التاريخ الهجري: **{hijri_today.day} / {hijri_today.month} / {hijri_today.year}**")
else:
    st.warning("⚠️ مكتبة hijri_converter غير متوفرة لعرض التاريخ الهجري.")

st.markdown("---")
st.subheader("🔮 احسب اليوم والتاريخ بعد عدد من الأيام")

# إدخال عدد الأيام
days = st.number_input("أدخل عدد الأيام من اليوم:", min_value=0, value=0, step=1)

# التاريخ المستقبلي
future_date = now + timedelta(days=days)
future_day = future_date.strftime("%A")
future_date_str = future_date.strftime("%Y-%m-%d")

if hijri_available:
    hijri_future = convert.Gregorian(future_date.year, future_date.month, future_date.day).to_hijri()
    hijri_str = f"{hijri_future.day} / {hijri_future.month} / {hijri_future.year}"
else:
    hijri_str = "غير متوفّر (ثبّت hijri_converter)"

# عرض النتائج
st.success(f"📍 بعد {days} يوم:")
st.markdown(f"- اليوم سيكون: **{future_day}**")
st.markdown(f"- التاريخ الميلادي: **{future_date_str}**")
st.markdown(f"- التاريخ الهجري: **{hijri_str}**")
