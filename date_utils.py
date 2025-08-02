from datetime import datetime
from convertdate import islamic
import dateutil.relativedelta


def get_hijri_date(dt: datetime) -> str:
    """
    حساب التاريخ الهجري باستخدام مكتبة convertdate بشكل مباشر،
    لتجنب مشكلة نطاق أم القرى.
    """
    islamic_date = islamic.from_gregorian(dt.year, dt.month, dt.day)
    return f"{islamic_date[0]}/{islamic_date[1]}/{islamic_date[2]} (تقريبي)"


def calc_date_difference(dt1: datetime, dt2: datetime) -> dict:
    """
    يحسب الفرق بين تاريخين ميلاديين مع تحديد الاتجاه (قبل/بعد).
    يرجع قاموس يحتوي السنوات، الشهور، الأيام، الساعات، الدقائق، والاتجاه.
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
