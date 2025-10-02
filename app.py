import pandas as pd
import streamlit as st

# ---- CẤU HÌNH FILE ----
excel_file = "A787.xlsx"   # Tên file Excel
xls = pd.ExcelFile(excel_file)

# ---- CSS TÙY BIẾN ----
st.markdown(
    """
    <style>
    body {
        background-color: #f5f7fa;
    }
    /* Background image mờ */
    .stApp {
        background: url("airplane.jpg") no-repeat center center fixed;
        background-size: cover;
    }
    .stApp::before {
        content: "";
        position: fixed;
        top:0; left:0;
        width:100%; height:100%;
        background: rgba(255,255,255,0.7);
        z-index:0;
    }
    /* Chữ trên app */
    .stMarkdown, .stSelectbox label {
        font-weight: bold;
        color: #333;
    }
    /* Bảng */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 14px;
        text-align: center;
        background-color: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
    }
    thead th {
        background-color: #2c3e50;
        color: white !important;
        font-weight: bold;
        padding: 8px;
    }
    tbody td {
        padding: 6px;
        border: 1px solid #ddd;
        color: #000;
    }
    tbody tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    tbody tr:hover {
        background-color: #e8f0fe;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- TIÊU ĐỀ ----
st.markdown(
    """
    <h2 style='text-align: center; font-weight: bold; 
    background: linear-gradient(90deg, red, orange, green, blue, purple);
    -webkit-background-clip: text;
    color: transparent;
    animation: gradient 5s infinite alternate;'>Tổ bảo dưỡng số 1</h2>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center; margin-top: -10px;'>🔎 Tra cứu Part Number (PN)</h1>", unsafe_allow_html=True)

# ---- STEP 1: Chọn sheet ----
sheet = st.selectbox("📂 Bạn muốn tra cứu zone nào?", xls.sheet_names)

if sheet:
    df = pd.read_excel(excel_file, sheet_name=sheet)

    # Chuẩn hóa header
    df.columns = df.columns.str.strip().str.upper()

    # Loại bỏ NaN
    df = df.dropna(how="all")

    # ---- STEP 2: Chọn A/C ----
    if "A/C" in df.columns:
        ac_list = sorted([x for x in df["A/C"].dropna().unique() if str(x).strip().upper() != "NAN"])
        aircraft = st.selectbox("✈️ Loại máy bay?", ac_list)
    else:
        aircraft = None

    if aircraft:
        df_ac = df[df["A/C"] == aircraft]

        # ---- STEP 3: Chọn Description ----
        if "DESCRIPTION" in df_ac.columns:
            desc_list = sorted([x for x in df_ac["DESCRIPTION"].dropna().unique() if str(x).strip().upper() != "NAN"])
            description = st.selectbox("📑 Bạn muốn tra cứu phần nào?", desc_list)
        else:
            description = None

        if description:
            df_desc = df_ac[df_ac["DESCRIPTION"] == description]

            # ---- Nếu có ITEM thì hỏi thêm ----
            if "ITEM" in df_desc.columns:
                item_list = sorted([x for x in df_desc["ITEM"].dropna().unique() if str(x).strip().upper() != "NAN"])
                if item_list:
                    item = st.selectbox("📦 Bạn muốn tra cứu Item nào?", item_list)
                    df_desc = df_desc[df_desc["ITEM"] == item]

            # ---- Hiển thị kết quả ----
            if not df_desc.empty:
                result = df_desc.copy()

                # Thêm cột STT
                result.insert(0, "STT", range(1, len(result) + 1))

                # Chỉ giữ các cột cần
                cols_to_show = []
                for col in ["STT", "PART NUMBER (PN)", "PART INTERCHANGE", "NOTE"]:
                    if col in result.columns:
                        cols_to_show.append(col)

                result = result[cols_to_show]

                st.success(f"Tìm thấy {len(result)} dòng dữ liệu:")

                # Render bảng
                st.markdown(result.to_html(index=False, escape=False), unsafe_allow_html=True)
            else:
                st.error("Rất tiếc, dữ liệu bạn chọn chưa có.")
