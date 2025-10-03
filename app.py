import pandas as pd
import streamlit as st
import base64

# ===== Đọc file Excel =====
excel_file = "A787.xlsx"
xls = pd.ExcelFile(excel_file)

def load_and_clean(sheet):
    df = pd.read_excel(excel_file, sheet_name=sheet)
    df.columns = df.columns.str.strip().str.upper()
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("").astype(str).str.strip()
    return df

# ===== Load background airplane.jpg =====
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_base64 = get_base64_of_bin_file("airplane.jpg")

# ===== CSS Vintage + icon máy bay chạy ngang =====
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

    .stApp {{
        font-family: 'Special Elite', cursive !important;
        background: 
            linear-gradient(rgba(245, 242, 230, 0.85), rgba(245, 242, 230, 0.85)), 
            url("data:image/jpg;base64,{img_base64}") no-repeat center center fixed;
        background-size: cover;
    }}

    .stApp::after {{
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: url("https://www.transparenttextures.com/patterns/aged-paper.png");
        opacity: 0.35;
        pointer-events: none;
        z-index: -1;
    }}

    .block-container {{
        padding-top: 0rem !important;
    }}
    header[data-testid="stHeader"] {{ display: none; }}

    .top-title {{
        font-size: 34px;
        font-weight: bold;
        text-align: center;
        margin: 20px auto 10px auto;
        color: #3e2723;
        text-shadow: 1px 1px 0px #fff;
    }}

    .main-title {{
        font-size: 26px;
        font-weight: 900;
        text-align: center;
        color: #5d4037;
        margin-top: 5px;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
    }}

    .stSelectbox label {{
        font-weight: bold !important;
        font-size: 18px !important;
        color: #4e342e !important;
        font-family: 'Special Elite', cursive !important;
    }}

    .stSelectbox div[data-baseweb="select"] {{
        font-family: 'Special Elite', cursive !important;
        font-size: 15px !important;
        color: #3e2723 !important;
        background: #fdfbf5 !important;
        border: 1.5px dashed #5d4037 !important;
        border-radius: 6px !important;
    }}
    .stSelectbox div[data-baseweb="popover"] {{
        font-family: 'Special Elite', cursive !important;
        font-size: 15px !important;
        background: #fdfbf5 !important;
        color: #3e2723 !important;
        border: 1.5px dashed #5d4037 !important;
    }}

    table.dataframe {{
        width: 100%;
        border-collapse: collapse !important;
        border: 2px solid #5d4037;
        font-family: 'Special Elite', cursive !important;
        background: #fdfbf5;
    }}
    table.dataframe thead th {{
        background: #795548 !important;
        color: white !important;
        font-weight: bold;
        text-align: center;
        padding: 10px !important;
        font-size: 15px;
        border: 2px solid #5d4037 !important;
    }}
    table.dataframe tbody td {{
        text-align: center !important;
        padding: 8px !important;
        font-size: 14px;
        color: #3e2723 !important;
        border: 1.5px dashed #5d4037 !important;
    }}
    table.dataframe tbody tr:nth-child(even) td {{ background: #f8f4ec !important; }}
    table.dataframe tbody tr:hover td {{
        background: #f1e0c6 !important;
        transition: 0.3s ease-in-out;
    }}

    .highlight-msg {{
        font-size: 18px;
        font-weight: bold;
        color: #3e2723;
        background: #efebe9;
        padding: 10px 15px;
        border-left: 6px solid #6d4c41;
        border-radius: 6px;
        margin: 15px 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }}
    .shake {{
        display: inline-block;
        animation: shake 1s infinite;
    }}
    @keyframes shake {{
        0% {{ transform: translate(1px, 1px) rotate(0deg); }}
        25% {{ transform: translate(-1px, -1px) rotate(-1deg); }}
        50% {{ transform: translate(-2px, 2px) rotate(1deg); }}
        75% {{ transform: translate(2px, -2px) rotate(1deg); }}
        100% {{ transform: translate(1px, 1px) rotate(0deg); }}
    }}

    /* Icon máy bay chạy ngang đáy */
    .plane {{
        position: fixed;
        bottom: 20px;
        left: -100px;
        font-size: 32px;
        animation: fly 15s linear infinite;
        z-index: 1000;
    }}
    @keyframes fly {{
        0%   {{ left: -100px; transform: scaleX(1); }}
        49%  {{ transform: scaleX(1); }}
        50%  {{ left: 100%; transform: scaleX(-1); }}
        99%  {{ transform: scaleX(-1); }}
        100% {{ left: -100px; transform: scaleX(1); }}
    }}
    </style>

    <div class="plane">✈️</div>
""", unsafe_allow_html=True)

# ===== Header =====
st.markdown('<div class="top-title">📜 Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🔎 Tra cứu Part number</div>', unsafe_allow_html=True)

# ===== Dropdowns và logic =====
zone = st.selectbox("📂 Bạn muốn tra cứu zone nào?", xls.sheet_names, key="zone")
if zone:
    df = load_and_clean(zone)

    if "A/C" in df.columns:
        aircrafts = sorted([ac for ac in df["A/C"].dropna().unique().tolist() if ac and ac.upper() != "NAN"])
        aircraft = st.selectbox("✈️ Loại máy bay?", aircrafts, key="aircraft")
    else:
        aircraft = None

    if aircraft:
        df_ac = df[df["A/C"] == aircraft]

        if "DESCRIPTION" in df_ac.columns:
            desc_list = sorted([d for d in df_ac["DESCRIPTION"].dropna().unique().tolist() if d and d.upper() != "NAN"])
            description = st.selectbox("📑 Bạn muốn tra cứu phần nào?", desc_list, key="desc")
        else:
            description = None

        if description:
            df_desc = df_ac[df_ac["DESCRIPTION"] == description]

            if "ITEM" in df_desc.columns:
                items = sorted([i for i in df_desc["ITEM"].dropna().unique().tolist() if i and i.upper() != "NAN"])
                if items:
                    item = st.selectbox("🔢 Bạn muốn tra cứu Item nào?", items, key="item")
                    df_desc = df_desc[df_desc["ITEM"] == item]

            if not df_desc.empty:
                df_result = df_desc.copy().reset_index(drop=True)

                cols_to_show = ["PART NUMBER (PN)"]
                for alt_col in ["PART INTERCHANGE", "PN INTERCHANGE"]:
                    if alt_col in df_result.columns:
                        cols_to_show.append(alt_col)
                        break
                if "NOTE" in df_result.columns:
                    cols_to_show.append("NOTE")

                df_result = df_result[cols_to_show]
                df_result.insert(0, "STT", range(1, len(df_result) + 1))

                st.markdown(
                    f'<div class="highlight-msg"><span class="shake">✅</span> Tìm thấy {len(df_result)} dòng dữ liệu</div>',
                    unsafe_allow_html=True
                )
                st.write(df_result.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.error("Rất tiếc, không tìm thấy dữ liệu phù hợp.")
