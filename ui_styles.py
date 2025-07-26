def get_styles():
    return """
    <style>
      .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px;
      }
      .row {
        display: flex;
        gap: 15px;
        justify-content: flex-end;
        width: 400px;
      }
      .card {
        background:#f1f1f1;
        padding: 15px 25px;
        border-radius: 15px;
        font-size: 22px;
        font-weight: bold;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: right;
        direction: ltr;
        width: 180px;
        display: flex;
        justify-content: center;
        align-items: center;
      }
      .hijri-card {
        background:#d7ffd9;
        padding: 15px 25px;
        border-radius: 15px;
        font-size: 22px;
        font-weight: bold;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: right;
        direction: ltr;
        width: 180px;
        display: flex;
        justify-content: center;
        align-items: center;
      }
      .month-name {
        background:#f1f1f1;
        padding: 15px 25px;
        border-radius: 15px;
        font-size: 22px;
        font-weight: bold;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        width: 180px;
        display: flex;
        justify-content: center;
        align-items: center;
      }
      .months-three {
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        width: 400px;
        margin-top: 20px;
      }
      .scrollable-box {
        width: 400px;
        max-height: 40px;
        overflow: hidden;
        border: 1px solid #ccc;
        border-radius: 12px;
        padding: 10px;
        font-weight: bold;
        font-size: 18px;
        cursor: pointer;
        user-select: none;
        background-color: #f0f8ff;
        transition: max-height 0.3s ease;
        direction: ltr;
      }
      .scrollable-box.active {
        max-height: 220px;
        overflow-y: auto;
        background-color: white;
      }
      .scroll-item {
        padding: 8px;
        margin: 5px 0;
        background: #d0eaff;
        border-radius: 8px;
      }
    </style>
    """
