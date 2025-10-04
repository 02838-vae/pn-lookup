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

# ===== Hàm chuyển file ảnh thành base64 =====
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# ===== Load ảnh GIF động =====
gif_base64 = get_base64_of_bin_file("Airplane.gif")

# ===== CSS nền & hiệu ứng máy bay =====
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

    /* Toàn trang */
    .stApp {{
        font-family: 'Special Elite', cursive !important;
        background: #f5f2e6;
    }}

    header[data-testid="stHeader"] {{
        display: none;
    }}

    .block-container {{
        padding-top: 0rem !important;
    }}

    /* Tiêu đề */
    .top-title {{
        font-size: 34px;
        font-weight: bold;
        text-align: center;
        color: #3e2723;
        margin: 20px auto 5px auto;
        text-shadow: 1px 1px 0px #fff;
    }}

    .main-title {{
        font-size: 26px;
        font-weight: 900;
        text-align: center;
        color: #5d4037;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
    }}

    /* --- Hiệu ứng máy bay bay ngang qua tiêu đề --- */
    .airplane-container {{
        position: relative;
        width: 100%;
        height: 120px;
        overflow: hidden;
        margin-bottom: -30px;
    }}

    .airplane {{
        position: absolute;
        top: 20px;
        left: -200px;
        width: 160px;
        animation: flyAcross 12s linear infinite;
        mix-blend-mode: multiply;
        opacity: 0.9;
        filter: brightness(0.95) contrast(1.05);
    }}

    @keyframes flyAcross {{
        0% {{ left: -200px; transform: rotate(5deg); }}
        50% {{ top: 15px; transform: rotate(0deg); }}
        100% {{ left: 100%; transform: rotate(-3deg); }}
    }}
    </style>
""", unsafe_allow_html=True)

# ===== Hiệu ứng máy bay động (GIF Base64) =====
st.markdown(f"""
<div class="airplane-container">
    <img class="airplane" src="data:image/gif;base64,{gif_base64}">
</div>
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

                st.success(f"✅ Tìm thấy {len(df_result)} dòng dữ liệu")
                st.dataframe(df_result)
            else:
                st.error("📌 Rất tiếc, không tìm thấy dữ liệu phù hợp.")
