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
    /* Toàn bộ app */
    .stApp {
        background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Segoe UI', sans-serif;
    }

    @keyframes gradientBG {
        0%{background-position:0% 50%}
        50%{background-position:100% 50%}
        100%{background-position:0% 50%}
    }

    /* Neon Header */
    .neon-title {
        font-size: 42px;
        font-weight: 900;
        text-align: center;
        color: #fff;
        text-shadow:
            0 0 5px #fff,
            0 0 10px #ff00de,
            0 0 20px #ff00de,
            0 0 40px #ff00de;
        animation: glow 3s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from {
            text-shadow: 0 0 10px #ff00de, 0 0 20px #ff00de, 0 0 30px #ff00de;
        }
        to {
            text-shadow: 0 0 20px #00ffff, 0 0 40px #00ffff, 0 0 60px #00ffff;
        }
    }

    /* Glassmorphism box */
    .glass-box {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }

    /* Bảng kết quả */
    table {
        width: 100%;
        border-collapse: collapse;
        border-radius: 12px;
        overflow: hidden;
    }
    thead th {
        background: #222;
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
    }
    tbody tr:nth-child(even) td {
        background: #f2f2f2;
    }
    tbody tr:hover td {
        background: #ffeaa7;
        transform: scale(1.01);
        transition: 0.2s ease-in-out;
    }

    /* Dropdown + button đẹp */
    .stSelectbox, .stButton>button {
        border-radius: 12px !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ===== Header =====
st.markdown('<div class="neon-title">✨ Tra cứu Part Number (PN) ✨</div>', unsafe_allow_html=True)
st.write("")  # khoảng cách

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

                # Thêm STT bắt đầu từ 1
                df_result.index = df_result.index + 1
                df_result.index.name = "STT"

                st.markdown('<div class="glass-box">', unsafe_allow_html=True)
                st.success(f"Tìm thấy {len(df_result)} dòng dữ liệu:")
                st.write(df_result.to_html(escape=False), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("Rất tiếc, không tìm thấy dữ liệu phù hợp.")
