from datetime import datetime
from ummalqura.hijri_date import HijriDate

# الأشهر الميلادية والعربية والهجرية
months_en = ["January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December"]

months_ar1 = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
              "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]

months_ar2 = ["كانون الثاني", "شباط", "آذار", "نيسان", "أيار", "حزيران",
              "تموز", "آب", "أيلول", "تشرين الأول", "تشرين الثاني", "كانون الأول"]

months_hijri = ["محرم", "صفر", "ربيع الأول", "ربيع الآخر",
                "جمادى الأولى", "جمادى الآخرة", "رجب", "شعبان",
                "رمضان", "شوال", "ذو القعدة", "ذو الحجة"]

def get_dates():
    now = datetime.now()
    month_index = now.month - 1
    day = now.day
    year = now.year

    hijri_today = HijriDate.today()
    hijri_month_index = hijri_today.month - 1
    hijri_day = hijri_today.day
    hijri_year = hijri_today.year

    return {
        "gregorian_day": day,
        "gregorian_month_index": month_index,
        "gregorian_year": year,
        "hijri_day": hijri_day,
        "hijri_month_index": hijri_month_index,
        "hijri_year": hijri_year
    }
