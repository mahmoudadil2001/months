from datetime import datetime
from convertdate import islamic

HIJRI_MONTH_NAMES_AR = [
    "محرم", "صفر", "ربيع الأول", "ربيع الثاني", "جمادى الأولى", "جمادى الآخرة",
    "رجب", "شعبان", "رمضان", "شوال", "ذو القعدة", "ذو الحجة"
]

def get_hijri_date(dt: datetime) -> str:
    """حساب التاريخ الهجري بشكل آمن باستخدام UmmAlQura إذا كان متاحًا وإلا convertdate"""
    try:
        from ummalqura.hijri_date import HijriDate

        if datetime(2015, 8, 2) <= dt <= datetime(2035, 8, 2):
            hijri_date = HijriDate(dt.year, dt.month, dt.day, gr=True)
            month_name = HIJRI_MONTH_NAMES_AR[hijri_date.month - 1]
            return f"{hijri_date.year}/{month_name}/{hijri_date.day} (أم القرى)"
    except Exception:
        pass

    # بديل تقريبي إذا كان التاريخ خارج النطاق
    islamic_date = islamic.from_gregorian(dt.year, dt.month, dt.day)
    month_name = HIJRI_MONTH_NAMES_AR[islamic_date[1] - 1]
    return f"{islamic_date[0]}/{month_name}/{islamic_date[2]} (تقريبي)"


def calc_date_difference(dt1: datetime, dt2: datetime) -> dict:
    """حساب الفرق بين تاريخين ميلاديين"""
    import dateutil.relativedelta

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
