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
        background: none;
        position: relative;
    }
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("airplane.jpg") no-repeat center center fixed;
        background-size: cover;
        opacity: 0.25; /* chỉnh độ mờ để chữ dễ đọc */
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
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    thead th {
        background: #2c3e50;
        color: white !important;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        font-size: 15px;
    }
    tbody td {
        background: white;
        text-align: center;
        padding: 8px;
        font-size: 14px;
        color: #2c3e50;
    }
    tbody tr:nth-child(even) td {
        background: #f8f9fa;
    }
    tbody tr:hover td {
        background: #ffeaa7;
        transition: 0.2s ease-in-out;
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
        aircrafts = sorted([ac for ac in df["A/C"].dropna().unique().tolist() if ac and ac != "NAN"])
        aircraft = st.selectbox("✈️ Loại máy bay?", aircrafts, key="aircraft")
    else:
        aircraft = None

    if aircraft:
        df_ac = df[df["A/C"] == aircraft]

        # ===== Dropdown 3: Description =====
        if "DESCRIPTION" in df_ac.columns:
            desc_list = sorted([d for d in df_ac["DESCRIPTION"].dropna().unique().tolist() if d and d != "NAN"])
            description = st.selectbox("📑 Bạn muốn tra cứu phần nào?", desc_list, key="desc")
        else:
            description = None

        if description:
            df_desc = df_ac[df_ac["DESCRIPTION"] == description]

            # Nếu có cột ITEM thì hỏi thêm
            if "ITEM" in df_desc.columns:
                items = sorted([i for i in df_desc["ITEM"].dropna().unique().tolist() if i and i != "NAN"])
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

                st.success(f"Tìm thấy {len(df_result)} dòng dữ liệu:")
                st.write(df_result.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.error("Rất tiếc, không tìm thấy dữ liệu phù hợp.")
