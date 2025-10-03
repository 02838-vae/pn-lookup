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

# ===== Load background vintage airplane.jpg =====
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_base64 = get_base64_of_bin_file("airplane.jpg")

# ===== Load gif động airplane.gif =====
def get_gif_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

gif_base64 = get_gif_base64("airplane.gif")

# ===== CSS =====
st.markdown(f"""
    <style>
    /* Nền trang vintage */
    .stApp {{
        background: 
            linear-gradient(rgba(245, 222, 179, 0.6), rgba(245, 222, 179, 0.6)), 
            url("data:image/jpg;base64,{img_base64}") no-repeat center center fixed;
        background-size: cover;
    }}

    .block-container {{
        padding-top: 0rem !important;
    }}

    header[data-testid="stHeader"] {{
        display: none;
    }}

    /* Dòng chữ Tổ bảo dưỡng số 1 */
    .top-title {{
        font-size: 32px;
        font-weight: 900;
        text-align: center;
        animation: colorchange 5s infinite alternate;
        margin: 20px auto 10px auto;
        white-space: nowrap;
        font-family: Arial, sans-serif;
    }}
    @keyframes colorchange {{
        0% {{color: #e74c3c;}}
        25% {{color: #3498db;}}
        50% {{color: #2ecc71;}}
        75% {{color: #f1c40f;}}
        100% {{color: #9b59b6;}}
    }}

    /* Tiêu đề chính */
    .main-title {{
        font-size: 28px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #ff6a00, #ff8c00, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 10px;
        margin-bottom: 20px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.4);
        white-space: nowrap;
        font-family: Arial, sans-serif;
    }}

    /* Font cho label câu hỏi + dropdown */
    .stSelectbox label, .stSelectbox div[data-baseweb="select"] * {{
        font-family: Arial, sans-serif !important;
        font-size: 16px !important;
        color: #2c3e50 !important;
    }}

    /* Bảng kết quả */
    table.dataframe {{
        width: 100%;
        border-collapse: collapse !important;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        background: white;
        font-family: Arial, sans-serif;
    }}
    table.dataframe thead th {{
        background: #2c3e50 !important;
        color: white !important;
        font-weight: bold;
        text-align: center;
        padding: 10px !important;
        font-size: 15px;
        border: 2px solid #2c3e50 !important;
    }}
    table.dataframe tbody td {{
        text-align: center !important;
        padding: 8px !important;
        font-size: 14px;
        color: #2c3e50 !important;
        border: 1.5px solid #2c3e50 !important;
    }}
    table.dataframe tbody tr:nth-child(even) td {{
        background: #f8f9fa !important;
    }}
    table.dataframe tbody tr:hover td {{
        background: #ffeaa7 !important;
        transition: 0.2s ease-in-out;
    }}

    .highlight-msg {{
        font-size: 18px;
        font-weight: bold;
        color: #154360;
        background: #d6eaf8;
        padding: 10px 15px;
        border-left: 6px solid #154360;
        border-radius: 6px;
        margin: 15px 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        font-family: Arial, sans-serif;
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

    /* Máy bay GIF động */
    .plane-gif {{
        position: fixed;
        bottom: 20px;
        left: -150px;
        width: 80px;
        animation: flygif 15s linear infinite;
        z-index: 1000;
    }}
    @keyframes flygif {{
        0%   {{ left: -150px; transform: scaleX(1); }}
        49%  {{ transform: scaleX(1); }}
        50%  {{ left: 100%; transform: scaleX(-1); }}
        99%  {{ transform: scaleX(-1); }}
        100% {{ left: -150px; transform: scaleX(1); }}
    }}
    </style>

    <img src="data:image/gif;base64,{gif_base64}" class="plane-gif"/>
""", unsafe_allow_html=True)

# ===== Header =====
st.markdown('<div class="top-title">Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
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
