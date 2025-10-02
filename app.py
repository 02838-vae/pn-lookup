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

# ===== CSS Trang trí =====
st.markdown(f"""
    <style>
    /* Nền trang */
    .stApp {{
        background-image: url("data:image/jpg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Overlay trắng mờ để chữ rõ */
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

    /* Dòng chữ Tổ bảo dưỡng số 1 */
    .top-title {{
        font-size: 26px;
        font-weight: bold;
        text-align: center;
        animation: colorchange 5s infinite alternate;
        display: block;
        margin: 15px auto;
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
        font-size: 36px;
        font-weight: 900;
        text-align: center;
        color: #2c3e50;
        margin-top: 10px;
        margin-bottom: 20px;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    }}

    /* Bảng kết quả */
    table {{
        width: 100%;
        border-collapse: collapse;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        background: white;
    }}
    thead th {{
        background: #2c3e50;
        color: white !important;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        font-size: 15px;
    }}
    tbody td {{
        background: white;
        text-align: center;
        padding: 8px;
        font-size: 14px;
        color: #2c3e50;
    }}
    tbody tr:nth-child(even) td {{
        background: #f8f9fa;
    }}
    tbody tr:hover td {{
        background: #ffeaa7;
        transition: 0.2s ease-in-out;
    }}

    /* Thông báo tìm thấy dữ liệu - blink */
    .highlight-msg {{
        font-size: 18px;
        font-weight: bold;
        color: #154360;
        background: #d6eaf8;
        padding: 10px 15px;
        border-left: 6px solid #154360;
        border-radius: 6px;
        margin: 15px 0;
        animation: blink 1.2s infinite;
    }}
    @keyframes blink {{
        0% {{ opacity: 1; }}
        50% {{ opacity: 0.4; }}
        100% {{ opacity: 1; }}
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

                st.markdown(f'<div class="highlight-msg">✅ Tìm thấy {len(df_result)} dòng dữ liệu</div>', unsafe_allow_html=True)
                st.write(df_result.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.error("Rất tiếc, không tìm thấy dữ liệu phù hợp.")
