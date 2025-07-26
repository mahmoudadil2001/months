import streamlit.components.v1 as components
from ui_styles import get_styles
import calendar

def render_html(dates, months_en, months_ar1, months_ar2, months_hijri, now,
                transported_date=None, transported_day_name=""):
    gregorian_days_in_month = [
        calendar.monthrange(dates['gregorian_year'], month)[1]
        for month in range(1, 13)
    ]

    hijri_days_in_month = [30 if i % 2 == 0 else 29 for i in range(12)]

    gregorian_months_html = "".join(
        f'<div class="scroll-item">{i+1}. {ar2} - {en} - {ar1} ({gregorian_days_in_month[i]} يوم)</div>'
        for i, (ar2, en, ar1) in enumerate(zip(months_ar2, months_en, months_ar1))
    )

    hijri_months_html = "".join(
        f'<div class="scroll-item">{i+1}. {m} ({hijri_days_in_month[i]} يوم)</div>'
        for i, m in enumerate(months_hijri)
    )

    # قسم التاريخ المنقول + اسم اليوم أسفله بشكل واضح وكبير
    transported_section = ""
    if transported_date is not None:
        transported_section = f"""
        <div style="margin-top: 30px; text-align: center;">
            <div style="font-size: 22px; font-weight: bold; direction: ltr;">
                {transported_date.year}/{transported_date.month:02d}/{transported_date.day:02d} ميلادي
            </div>
            <div style="font-size: 22px; font-weight: bold; color: #4CAF50; margin-top: 6px;">
                {months_hijri[(dates['hijri_month_index'])]} {dates['hijri_year']}
            </div>
            <div style="font-size: 34px; font-weight: 900; color: #222; margin-top: 15px; direction: rtl;">
                {transported_day_name}
            </div>
        </div>
        """

    html_code = f"""
    {get_styles()}

    <style>
      .scroll-list {{
        width: 400px;
        max-height: 220px;
        overflow-y: auto;
        border: 1px solid #ccc;
        border-radius: 12px;
        padding: 10px;
        font-weight: bold;
        font-size: 18px;
        background-color: white;
        margin-top: 5px;
        display: none;
        text-align: center;
      }}
      .scroll-item {{
        padding: 6px 0;
      }}
      .card {{
        font-weight: 700;
        font-size: 22px;
        padding: 10px;
        border-radius: 10px;
        background: #f3f3f3;
        text-align: center;
      }}
      .hijri-card {{
        font-weight: 700;
        font-size: 22px;
        padding: 10px;
        border-radius: 10px;
        background: #d4f7d4;
        text-align: center;
      }}
      .month-name {{
        margin-top: 6px;
        font-weight: 600;
        font-size: 20px;
        text-align: center;
        direction: rtl;
      }}
      .months-three {{
        margin-top: 20px;
        font-weight: 700;
        font-size: 20px;
        text-align: center;
        direction: rtl;
      }}
    </style>

    <div class="container">

      <div class="row">
        <div class="card">{dates['gregorian_year']}/{now.month:02d}/{dates['gregorian_day']:02d}</div>
        <div class="month-name">{months_ar1[dates['gregorian_month_index']]}</div>
      </div>

      <div class="row">
        <div class="hijri-card">{dates['hijri_year']}/{dates['hijri_month_index']+1:02d}/{dates['hijri_day']:02d}</div>
        <div class="month-name" style="background:#b4f0a4;">{months_hijri[dates['hijri_month_index']]}</div>
      </div>

      <div class="months-three">{months_ar2[dates['gregorian_month_index']]} - {months_en[dates['gregorian_month_index']]} - {months_ar1[dates['gregorian_month_index']]}</div>

      {transported_section}

      <div style="margin-top: 30px;">
        <div id="gregorian" class="scrollable-box">📜 اضغط لعرض الأشهر الميلادية</div>
        <div id="gregorian-list" class="scroll-list">{gregorian_months_html}</div>
      </div>

      <div style="margin-top: 20px;">
        <div id="hijri" class="scrollable-box">📜 اضغط لعرض الأشهر الهجرية</div>
        <div id="hijri-list" class="scroll-list">{hijri_months_html}</div>
      </div>

    </div>

    <script>
      const gregorian = document.getElementById("gregorian");
      const gregorianList = document.getElementById("gregorian-list");
      const hijri = document.getElementById("hijri");
      const hijriList = document.getElementById("hijri-list");

      gregorian.onclick = () => {{
        gregorianList.style.display = gregorianList.style.display === "none" ? "block" : "none";
      }};

      hijri.onclick = () => {{
        hijriList.style.display = hijriList.style.display === "none" ? "block" : "none";
      }};
    </script>
    """

    components.html(html_code, height=700)
