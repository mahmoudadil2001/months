from datetime import datetime
from ummalqura.hijri_date import HijriDate
from convertdate import islamic
import dateutil.relativedelta

months_hijri = [
    "محرم", "صفر", "ربيع الأول", "ربيع الآخر",
    "جمادى الأولى", "جمادى الآخرة", "رجب", "شعبان",
    "رمضان", "شوال", "ذو القعدة", "ذو الحجة"
]

def get_hijri_date(dt: datetime) -> str:
    """
    يحسب التاريخ الهجري باستخدام ummalqura إذا كان داخل النطاق،
    وإذا كان خارج النطاق يستخدم مكتبة convertdate كبديل تقريبي.
    """
    try:
        hijri_date = HijriDate(dt.year, dt.month, dt.day, gr=True)
        month_name = months_hijri[hijri_date.month - 1] if 1 <= hijri_date.month <= 12 else ""
        return f"{hijri_date.year}/{hijri_date.month}/{hijri_date.day} {month_name}"
    except Exception:
        islamic_date = islamic.from_gregorian(dt.year, dt.month, dt.day)
        month_num = islamic_date[1]
        month_name = months_hijri[month_num - 1] if 1 <= month_num <= 12 else ""
        return f"{islamic_date[0]}/{islamic_date[1]}/{islamic_date[2]} {month_name} (تقريبي)"

def calc_date_difference(dt1: datetime, dt2: datetime) -> dict:
    """
    يحسب الفرق بين تاريخين مع الإشارة إذا كان قبل أو بعد.
    """
    diff_seconds = (dt2 - dt1).total_seconds()
    direction = "بعد" if diff_seconds >= 0 else "قبل"

    if diff_seconds >= 0:
        diff = dateutil.relativedelta.relativedelta(dt2, dt1)
    else:
        diff = dateutil.relativedelta.relativedelta(dt1, dt2)

    return {
        "direction": direction,
        "years": abs(diff.years),
        "months": abs(diff.months),
        "days": abs(diff.days),
        "hours": abs(diff.hours),
        "minutes": abs(diff.minutes),
        "total_days": abs((dt2 - dt1).days),
    }
