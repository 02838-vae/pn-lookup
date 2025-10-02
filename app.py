import pandas as pd
import streamlit as st

# ===== Đọc file Excel =====
excel_file = "A787.xlsx"
xls = pd.ExcelFile(excel_file)

# Chuẩn hóa tên cột
def load_and_clean(sheet):
    df = pd.read_excel(excel_file, sheet_name=sheet)
    df.columns = df.columns.str.strip().str.upper()
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("").astype(str).str.strip()
    return df

# ===== CSS Trang trí =====
st.markdown("""
    <style>
    /* Background ảnh máy bay */
    .stApp {
        background: url("airplane.jpg") no-repeat center center fixed;
        background-size: cover;
    }
    .stApp::before {
        content: "";
        position: fixed;
        top:0;
        left:0;
        width:100%;
        height:100%;
        background: rgba(255,255,255,0.55); /* làm nhạt ảnh nhưng vẫn nhìn rõ */
        z-index: -1;
    }

    /* Dòng chữ Tổ bảo dưỡng số 1 */
    .top-title {
        font-size: 26px;
        font-weight: bold;
        text-align: center;
        animation: colorchange 5s infinite alternate;
    }
    @keyframes colorchange {
        0% {color: #e74c3c;}
        25% {color: #3498db;}
        50% {color: #2ecc71;}
        75% {color: #f1c40f;}
        100% {color: #9b59b6;}
    }

    /* Tiêu đề chính */
    .main-title {
        font-size: 38px;
        font-weight: 900;
        text-align: center;
        color: #2c3e50;
        margin-top: 10px;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }

    /* Bảng kết quả */
    table {
        width: 100%;
        border-collapse: collapse;
        border-radius: 12px;
        overflow: hidden;
    }
    thead th {
        background: #34495e;
        color: white !important;
        font-weight: bold;
        text-align: center;
        padding: 10px;
    }
    tbody td {
        background: white;
        text-align: center;
        padding: 8px;
        font-size: 14px;
        color: #2c3e50;
    }
    tbody tr:nth-child(even) td {
        background: #f2f2f2;
    }
    tbody tr:hover td {
        background: #ffeaa7;
        transition: 0.2s ease-in-out;
    }

    /* Dropdown + button */
    .stSelectbox, .stButton>button {
        border-radius: 12px !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ===== Header =====
st.markdown('<div class="top-title">Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🔎 Tra cứu Part Number (PN)</div>', unsafe_allow_html=True)

# ===== Dropdown 1: Zone (sheet name) =====
zone = st.selectbox("📂 Bạn muốn tra cứu zone nào?", xls.sheet_names, key="zone")
if zone:
    df = load_and_clean(zone)

    # ===== Dropdown 2: A/C =====
    if "A/C" in df.columns:
        aircrafts = sorted(df["A/C"].dropna().unique().tolist())
        aircraft = st.selectbox("✈️ Loại máy bay?", aircrafts, key="aircraft")
    else:
        aircraft = None

    if aircraft:
        df_ac = df[df["A/C"] == aircraft]

        # ===== Dropdown 3: Description =====
        if "DESCRIPTION" in df_ac.columns:
            desc_list = sorted(df_ac["DESCRIPTION"].dropna().unique().tolist())
            description = st.selectbox("📑 Bạn muốn tra cứu phần nào?", desc_list, key="desc")
        else:
            description = None

        if description:
            df_desc = df_ac[df_ac["DESCRIPTION"] == description]

            # Nếu có cột ITEM thì hỏi thêm
            if "ITEM" in df_desc.columns:
                items = sorted(df_desc["ITEM"].dropna().unique().tolist())
                if items:
                    item = st.selectbox("🔢 Bạn muốn tra cứu Item nào?", items, key="item")
                    df_desc = df_desc[df_desc["ITEM"] == item]

            # Hiển thị kết quả
            if not df_desc.empty:
                df_result = df_desc.copy().reset_index(drop=True)

                # Giữ cột mong muốn
                cols_to_show = ["PART NUMBER (PN)"]
                if "PART INTERCHANGE" in df_result.columns:
                    cols_to_show.append("PART INTERCHANGE")
                if "NOTE" in df_result.columns:
                    cols_to_show.append("NOTE")

                df_result = df_result[cols_to_show]

                # Thêm STT bắt đầu từ 1 (ở header dòng 1)
                df_result.index = df_result.index + 1
                df_result.index.name = "STT"

                st.success(f"Tìm thấy {len(df_result)} dòng dữ liệu:")
                st.write(df_result.to_html(escape=False), unsafe_allow_html=True)
            else:
                st.error("Rất tiếc, không tìm thấy dữ liệu phù hợp.")
