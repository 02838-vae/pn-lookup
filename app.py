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

# ===== CSS Vintage =====
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Special+Elite&display=swap');

    /* Nền giấy cũ + overlay */
    .stApp {{
        background: 
            linear-gradient(rgba(245, 222, 179, 0.85), rgba(245, 222, 179, 0.85)),
            url("data:image/jpg;base64,{img_base64}") no-repeat center center fixed;
        background-size: cover;
        font-family: 'Special Elite', 'Courier New', monospace;
    }}

    .block-container {{
        padding-top: 0rem !important;
    }}

    header[data-testid="stHeader"] {{
        display: none;
    }}

    /* Dòng chữ Tổ bảo dưỡng số 1 */
    .top-title {{
        font-size: 34px;
        font-weight: bold;
        text-align: center;
        color: #5b3924;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-family: 'Playfair Display', serif;
        margin: 20px auto 10px auto;
    }}

    /* Tiêu đề chính */
    .main-title {{
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        color: #3b2f2f;
        font-family: 'Special Elite', cursive;
        margin-top: 10px;
        margin-bottom: 25px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6);
        letter-spacing: 2px;
    }}

    /* Label câu hỏi */
    .stSelectbox label {{
        font-weight: 700 !important;
        font-size: 18px !important;
        color: #4e342e !important;
        font-family: 'Courier New', monospace;
    }}

    /* Bảng vintage */
    table.dataframe {{
        width: 100%;
        border-collapse: collapse !important;
        border-radius: 8px;
        overflow: hidden;
        background: #fff8dc;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        font-family: 'Courier New', monospace;
    }}
    table.dataframe thead th {{
        background: #6d4c41 !important;
        color: #f5deb3 !important;
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
        color: #3e2723;
        border: 1px solid #8d6e63 !important;
    }}
    table.dataframe tbody tr:nth-child(even) td {{
        background: #fdf5e6 !important;
    }}
    table.dataframe tbody tr:hover td {{
        background: #ffe0b2 !important;
        transition: 0.3s ease-in-out;
    }}

    /* Thông báo tìm thấy dữ liệu */
    .highlight-msg {{
        font-size: 18px;
        font-weight: bold;
        color: #3e2723;
        background: #f5deb3;
        padding: 10px 15px;
        border-left: 6px solid #6d4c41;
        border-radius: 6px;
        margin: 15px 0;
        font-family: 'Playfair Display', serif;
        text-align: center;
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
    </style>
""", unsafe_allow_html=True)

# ===== Header =====
st.markdown('<div class="top-title">Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">📜 Tra cứu Part number</div>', unsafe_allow_html=True)

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
