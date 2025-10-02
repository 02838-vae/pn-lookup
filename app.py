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

# ===== CSS =====
st.markdown(f"""
    <style>
    /* Nền trang */
    .stApp {{
        background-image: url("data:image/jpg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp::after {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255,255,255,0.7); 
        z-index: -1;
    }}

    /* Fix khoảng trắng phía trên */
    .block-container {{
        padding-top: 0rem !important;
    }}
    header[data-testid="stHeader"] {{
        display: none;
    }}

    /* Dòng chữ Tổ bảo dưỡng số 1 */
    .top-title {{
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        animation: colorchange 5s infinite alternate;
        display: block;
        margin: 15px auto;
        white-space: nowrap;
    }}
    @keyframes colorchange {{
        0% {{color: #e74c3c;}}
        25% {{color: #3498db;}}
        50% {{color: #2ecc71;}}
        75% {{color: #f1c40f;}}
        100% {{color: #9b59b6;}}
    }}

    /* Tiêu đề chính Tra cứu Part number */
    .main-title {{
        font-size: 22px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #ff6a00, #ff8c00, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 5px;
        margin-bottom: 20px;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.5);
        white-space: nowrap;
    }}

    /* Bảng kết quả */
    table.dataframe {{
        width: 100%;
        border-collapse: collapse !important;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        background: white;
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
        color: #2c3e50;
        border: 1.5px solid #2c3e50 !important;
    }}
    table.dataframe tbody tr:nth-child(even) td {{
        background: #f8f9fa !important;
    }}
    table.dataframe tbody tr:hover td {{
        background: #ffeaa7 !important;
        transition: 0.2s ease-in-out;
    }}

    /* Thông báo tìm thấy dữ liệu */
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
    }}
    .shake {{
        display: inline-block;
        animation: shake 1s infinite;
    }}
    @keyframes shake {{
        0% {{ transform: translate(1px, 1px) rotate(0deg); }}
        10% {{ transform: translate(-1px, -2px) rotate(-1deg); }}
        20% {{ transform: translate(-3px, 0px) rotate(1deg); }}
        30% {{ transform: translate(3px, 2px) rotate(0deg); }}
        40% {{ transform: translate(1px, -1px) rotate(1deg); }}
        50% {{ transform: translate(-1px, 2px) rotate(-1deg); }}
        60% {{ transform: translate(-3px, 1px) rotate(0deg); }}
        70% {{ transform: translate(3px, 1px) rotate(-1deg); }}
        80% {{ transform: translate(-1px, -1px) rotate(1deg); }}
        90% {{ transform: translate(1px, 2px) rotate(0deg); }}
        100% {{ transform: translate(1px, -2px) rotate(-1deg); }}
    }}

    /* Label câu hỏi trong selectbox */
    .stSelectbox label {{
        font-weight: 900 !important;
        font-size: 18px !important;
        color: #000000 !important;  /* Nổi bật */
    }}
    </style>
""", unsafe_allow_html=True)

# ===== Header =====
st.markdown('<div class="top-title">Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🔎 Tra cứu Part number</div>', unsafe_allow_html=True)

# ===== Dropdown 1: Zone (sheet name) =====
zone = st.selectbox("📂 Bạn muốn tra cứu zone nào?", xls.sheet_names, key="zone")
if zone:
    df = load_and_clean(zone)

    # ===== Dropdown 2: A/C =====
    if "A/C" in df.columns:
        aircrafts = sorted([ac for ac in df["A/C"].dropna().unique().tolist() if ac and ac.upper() != "NAN"])
        aircraft = st.selectbox("✈️ Loại máy bay?", aircrafts, key="aircraft")
    else:
        aircraft = None

    if aircraft:
        df_ac = df[df["A/C"] == aircraft]

        # ===== Dropdown 3: Description =====
        if "DESCRIPTION" in df_ac.columns:
            desc_list = sorted([d for d in df_ac["DESCRIPTION"].dropna().unique().tolist() if d and d.upper() != "NAN"])
            description = st.selectbox("📑 Bạn muốn tra cứu phần nào?", desc_list, key="desc")
        else:
            description = None

        if description:
            df_desc = df_ac[df_ac["DESCRIPTION"] == description]

            # Nếu có cột ITEM thì hỏi thêm
            if "ITEM" in df_desc.columns:
                items = sorted([i for i in df_desc["ITEM"].dropna().unique().tolist() if i and i.upper() != "NAN"])
                if items:
                    item = st.selectbox("🔢 Bạn muốn tra cứu Item nào?", items, key="item")
                    df_desc = df_desc[df_desc["ITEM"] == item]

            # Hiển thị kết quả
            if not df_desc.empty:
                df_result = df_desc.copy().reset_index(drop=True)

                # Giữ cột mong muốn
                cols_to_show = ["PART NUMBER (PN)"]
                for alt_col in ["PART INTERCHANGE", "PN INTERCHANGE"]:
                    if alt_col in df_result.columns:
                        cols_to_show.append(alt_col)
                        break
                if "NOTE" in df_result.columns:
                    cols_to_show.append("NOTE")

                df_result = df_result[cols_to_show]

                # Thêm cột STT
                df_result.insert(0, "STT", range(1, len(df_result) + 1))

                st.markdown(
                    f'<div class="highlight-msg"><span class="shake">✅</span> Tìm thấy {len(df_result)} dòng dữ liệu</div>',
                    unsafe_allow_html=True
                )
                st.write(df_result.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.error("Rất tiếc, không tìm thấy dữ liệu phù hợp.")
