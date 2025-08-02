from datetime import datetime
from ummalqura.hijri_date import HijriDate
from convertdate import islamic
import dateutil.relativedelta

def get_hijri_date(dt: datetime) -> str:
    """
    حساب التاريخ الهجري باستخدام ummalqura أولاً، وإذا لم يكن متاحًا
    (خارج النطاق) يتم استخدام convertdate كبديل تقريبي.
    """
    try:
        hijri_date = HijriDate(dt.year, dt.month, dt.day, gr=True)
        return f"{hijri_date.year}/{hijri_date.month}/{hijri_date.day} (أم القرى)"
    except Exception:
        islamic_date = islamic.from_gregorian(dt.year, dt.month, dt.day)
        return f"{islamic_date[0]}/{islamic_date[1]}/{islamic_date[2]} (تقريبي)"

def calc_date_difference(dt1: datetime, dt2: datetime) -> dict:
    """
    حساب الفرق بين تاريخين ميلاديين مع الإشارة إلى الاتجاه (قبل/بعد).
    يرجع قاموس يحتوي على السنوات، الشهور، الأيام، الساعات، الدقائق، والاتجاه.
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
