import streamlit.components.v1 as components
from ui_styles import get_styles

def render_html(dates, months_en, months_ar1, months_ar2, months_hijri, now):
    # ✅ توليد الأشهر الميلادية مع الترقيم
    gregorian_months_html = "".join(
        f'<div class="scroll-item">{i+1}. {ar2} - {en} - {ar1}</div>'
        for i, (ar2, en, ar1) in enumerate(zip(months_ar2, months_en, months_ar1))
    )

    # ✅ توليد الأشهر الهجرية مع الترقيم
    hijri_months_html = "".join(
        f'<div class="scroll-item">{i+1}. {m}</div>'
        for i, m in enumerate(months_hijri)
    )

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
      }}
      .scroll-item {{
        padding: 6px 0;
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

    components.html(html_code, height=600)
