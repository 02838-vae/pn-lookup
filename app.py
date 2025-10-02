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

# ===== CSS Vintage + Film Grain =====
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

    /* Nền vintage với overlay sepia và film grain */
    .stApp {{
        background: 
            linear-gradient(rgba(94, 38, 18, 0.55), rgba(250, 240, 202, 0.7)), 
            url("data:image/jpg;base64,{img_base64}") no-repeat center center fixed;
        background-size: cover;
        background-blend-mode: multiply;
        font-family: 'Special Elite', cursive !important;
        position: relative;
        overflow: hidden;
    }}

    /* Lớp noise overlay giả lập film grain */
    .stApp::after {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("https://i.ibb.co/8c4tDvc/noise.png"); /* pattern noise */
        opacity: 0.15;
        pointer-events: none;
        z-index: 0;
        animation: grain 8s steps(10) infinite;
    }}

    @keyframes grain {{
        0% {{ transform: translate(0, 0); }}
        10% {{ transform: translate(-5%, -5%); }}
        20% {{ transform: translate(-10%, 5%); }}
        30% {{ transform: translate(5%, -10%); }}
        40% {{ transform: translate(-5%, 15%); }}
        50% {{ transform: translate(-10%, 5%); }}
        60% {{ transform: translate(15%, 0); }}
        70% {{ transform: translate(0, 10%); }}
        80% {{ transform: translate(-15%, 0); }}
        90% {{ transform: translate(10%, 5%); }}
        100% {{ transform: translate(5%, 0); }}
    }}

    .block-container {{
        padding-top: 0rem !important;
        position: relative;
        z-index: 1; /* giữ nội dung nổi trên noise */
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
        font-family: 'Special Elite', cursive !important;
        position: relative;
        z-index: 2;
    }}
    @keyframes colorchange {{
        0% {{color: #5d4037;}}
        25% {{color: #6d4c41;}}
        50% {{color: #8d6e63;}}
        75% {{color: #a1887f;}}
        100% {{color: #3e2723;}}
    }}

    /* Tiêu đề chính */
    .main-title {{
        font-size: 28px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #5d4037, #a1887f, #d7ccc8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 10px;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.4);
        white-space: nowrap;
        font-family: 'Special Elite', cursive !important;
        z-index: 2;
    }}

    /* Label câu hỏi */
    div[role="group"] label, label[data-testid="stWidgetLabel"] {{
        font-family: 'Special Elite', cursive !important;
        font-size: 19px !important;
        font-weight: bold !important;
        color: #2c1a0c !important;
        text-shadow: 1px 1px 2px #fdf6e3 !important;
    }}

    /* Hộp selectbox */
    .stSelectbox div[data-baseweb="select"] {{
        font-family: 'Special Elite', cursive !important;
        font-size: 15px !important;
        color: #2c1a0c !important;
        background: #fdf6e3 !important;
        border: 1.5px dashed #5d4037 !important;
        border-radius: 6px !important;
    }}
    .stSelectbox div[data-baseweb="popover"] {{
        font-family: 'Special Elite', cursive !important;
        font-size: 15px !important;
        background: #fdf6e3 !important;
        color: #2c1a0c !important;
        border: 1.5px dashed #5d4037 !important;
    }}

    /* Bảng kết quả */
    table.dataframe {{
        width: 100%;
        border-collapse: collapse !important;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        background: #fffef9;
        font-family: 'Special Elite', cursive !important;
    }}
    table.dataframe thead th {{
        background: #5d4037 !important;
        color: #fdf6e3 !important;
        font-weight: bold;
        text-align: center;
        padding: 10px !important;
        font-size: 15px;
        border: 2px solid #3e2723 !important;
    }}
    table.dataframe tbody td {{
        text-align: center !important;
        padding: 8px !important;
        font-size: 14px;
        color: #3e2723 !important;
        border: 1.5px solid #3e2723 !important;
    }}
    table.dataframe tbody tr:nth-child(even) td {{
        background: #f8f1df !important;
    }}
    table.dataframe tbody tr:hover td {{
        background: #ffeaa7 !important;
        transition: 0.2s ease-in-out;
    }}

    /* Thông báo tìm thấy */
    .highlight-msg {{
        font-size: 18px;
        font-weight: bold;
        color: #3e2723;
        background: #d7ccc8;
        padding: 10px 15px;
        border-left: 6px solid #3e2723;
        border-radius: 6px;
        margin: 15px 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        font-family: 'Special Elite', cursive !important;
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
