import pandas as pd
import streamlit as st
import base64
import os

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

# ===== Load background =====
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_base64 = get_base64_of_bin_file("airplane.jpg")

# ===== Load gif (máy bay nhỏ bay ngang) =====
def get_gif_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

gif_path = "airplane.gif"
gif_base64 = ""
if os.path.exists(gif_path):
    gif_base64 = get_gif_base64(gif_path)

# ===== CSS =====
st.markdown(f"""
    <style>
    /* Nền vintage */
    .stApp {{
        background: 
            linear-gradient(rgba(245, 222, 179, 0.6), rgba(245, 222, 179, 0.6)), 
            url("data:image/jpg;base64,{img_base64}") no-repeat center center fixed;
        background-size: cover;
        font-family: 'Georgia', serif;
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
    }}
    @keyframes colorchange {{
        0% {{color: #8B0000;}}
        25% {{color: #5D3A00;}}
        50% {{color: #2E4B3F;}}
        75% {{color: #8B5E3C;}}
        100% {{color: #3B3B3B;}}
    }}

    /* Tiêu đề chính */
    .main-title {{
        font-size: 28px;
        font-weight: 900;
        text-align: center;
        color: #5B4636;
        margin-top: 10px;
        margin-bottom: 20px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
        white-space: nowrap;
    }}

    /* Label câu hỏi */
    .stSelectbox label {{
        font-weight: 900 !important;
        font-size: 18px !important;
        color: #3E2723 !important;
        font-family: 'Georgia', serif !important;
    }}

    /* Dropdown menu */
    .stSelectbox div[data-baseweb="select"] > div {{
        font-family: 'Georgia', serif !important;
        color: #2c3e50 !important;
    }}

    /* Bảng kết quả */
    table.dataframe {{
        width: 100%;
        border-collapse: collapse !important;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        background: #fff8dc;
        font-family: 'Georgia', serif;
    }}
    table.dataframe thead th {{
        background: #5D3A00 !important;
        color: white !important;
        font-weight: bold;
        text-align: center;
        padding: 10px !important;
        font-size: 15px;
        border: 2px solid #5D3A00 !important;
    }}
    table.dataframe tbody td {{
        text-align: center !important;
        padding: 8px !important;
        font-size: 14px;
        color: #2c3e50 !important;
        border: 1.5px solid #5D3A00 !important;
    }}
    table.dataframe tbody tr:nth-child(even) td {{
        background: #fdf5e6 !important;
    }}
    table.dataframe tbody tr:hover td {{
        background: #ffeaa7 !important;
        transition: 0.2s ease-in-out;
    }}

    .highlight-msg {{
        font-size: 18px;
        font-weight: bold;
        color: #3E2723;
        background: #f1e0c6;
        padding: 10px 15px;
        border-left: 6px solid #5D3A00;
        border-radius: 6px;
        margin: 15px 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        font-family: 'Georgia', serif;
    }}

    /* Máy bay gif chạy ngang dưới cùng */
    .plane-gif {{
        position: fixed;
        bottom: 10px;
        left: -200px;
        height: 60px;
        animation: fly 20s linear infinite;
        z-index: 9999;
    }}
    @keyframes fly {{
        0% {{ left: -200px; }}
        100% {{ left: 100%; }}
    }}
    </style>
""", unsafe_allow_html=True)

# ===== Header =====
st.markdown('<div class="top-title">Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🔎 Tra cứu Part number</div>', unsafe_allow_html=True)

# ===== Máy bay gif nếu có =====
if gif_base64:
    st.markdown(f"""
        <img src="data:image/gif;base64,{gif_base64}" class="plane-gif"/>
    """, unsafe_allow_html=True)

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
