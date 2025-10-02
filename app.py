import streamlit as st
import pandas as pd
import base64

# ======= Load Excel ==========
excel_file = "A787.xlsx"
xls = pd.ExcelFile(excel_file)

# ======= Set page config =======
st.set_page_config(page_title="PN Lookup", layout="wide")

# ======= Background with Parallax =======
def set_background(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    page_bg = f"""
    <style>
    /* Layer 1: Ảnh máy bay */
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        position: relative;
        z-index: 0;
    }}

    /* Layer 2: Mây bay ngang */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: url("https://i.ibb.co/3Wf0v0q/clouds.png") repeat-x;
        background-size: contain;
        opacity: 0.35;
        animation: moveClouds 60s linear infinite;
        z-index: -2;
    }}

    /* Layer 3: Gradient động */
    .stApp::after {{
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(180deg, rgba(255,255,255,0.1), rgba(255,255,255,0.2));
        opacity: 0.6;
        animation: moveGradient 25s ease-in-out infinite;
        z-index: -1;
    }}

    @keyframes moveClouds {{
        from {{ background-position: 0 0; }}
        to {{ background-position: 10000px 0; }}
    }}

    @keyframes moveGradient {{
        0%   {{ background-position: 0 0; }}
        50%  {{ background-position: 0 300px; }}
        100% {{ background-position: 0 0; }}
    }}

    /* Chữ chạy đổi màu */
    .animated-title {{
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        animation: colorchange 6s infinite alternate;
    }}
    @keyframes colorchange {{
        0%   {{ color: #ff4b5c; }}
        25%  {{ color: #ff914d; }}
        50%  {{ color: #1dd1a1; }}
        75%  {{ color: #54a0ff; }}
        100% {{ color: #f368e0; }}
    }}

    /* Tiêu đề chính */
    .main-title {{
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        color: #ffe600;
        margin-top: -10px;
        margin-bottom: 20px;
    }}

    /* Kết quả tìm thấy */
    .found-text {{
        font-size: 20px;
        font-weight: bold;
        color: #ff1e56;
        animation: blink 1s infinite;
    }}
    @keyframes blink {{
        0%   {{ opacity: 1; }}
        50%  {{ opacity: 0.4; }}
        100% {{ opacity: 1; }}
    }}

    /* Bảng kết quả */
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 14px;
        text-align: center;
        background-color: #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        border-radius: 10px;
        overflow: hidden;
    }}
    thead th {{
        background-color: #004080;
        color: white;
        font-weight: bold;
        padding: 10px;
        border: 1px solid #333333;
    }}
    tbody td {{
        border: 1px solid #666666;
        padding: 8px;
        color: #000000;
    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

set_background("airplane.jpg")

# ======= Animated title =======
st.markdown("<div class='animated-title'>Tổ bảo dưỡng số 1</div>", unsafe_allow_html=True)

# ======= Main title =======
st.markdown("<div class='main-title'>Tra cứu Part number</div>", unsafe_allow_html=True)

# ======= Dropdown logic =======
sheet_name = st.selectbox("👉 Bạn muốn tra cứu zone nào?", xls.sheet_names)

if sheet_name:
    df = pd.read_excel(xls, sheet_name=sheet_name)
    df = df.dropna(how="all")
    df = df.fillna("")

    if "A/C" in df.columns:
        ac_list = sorted([x for x in df["A/C"].unique() if x not in ["", "nan", "NaN"]])
        ac_select = st.selectbox("👉 Loại máy bay?", ac_list)
    else:
        ac_select = None

    if ac_select:
        df_ac = df[df["A/C"] == ac_select] if "A/C" in df.columns else df

        if "Description" in df_ac.columns:
            desc_list = sorted([x for x in df_ac["Description"].unique() if x not in ["", "nan", "NaN"]])
            desc_select = st.selectbox("👉 Bạn muốn tra cứu phần nào?", desc_list)
        else:
            desc_select = None

        if desc_select:
            df_desc = df_ac[df_ac["Description"] == desc_select] if "Description" in df_ac.columns else df_ac

            if "Item" in df_desc.columns:
                item_list = sorted([x for x in df_desc["Item"].unique() if x not in ["", "nan", "NaN"]])
                item_select = st.selectbox("👉 Bạn muốn tra cứu Item nào?", item_list)
                result = df_desc[df_desc["Item"] == item_select]
            else:
                result = df_desc

            if not result.empty:
                result = result.reset_index(drop=True)
                result.index = result.index + 1  # STT từ 1

                cols_to_show = [c for c in ["PART NUMBER (PN)", "PN interchange", "Note"] if c in result.columns]
                result_display = result[cols_to_show].copy()
                result_display.index.name = "STT"

                st.markdown(f"<div class='found-text'>✅ Tìm thấy {len(result_display)} dòng dữ liệu:</div>", unsafe_allow_html=True)
                st.markdown(result_display.to_html(escape=False), unsafe_allow_html=True)
