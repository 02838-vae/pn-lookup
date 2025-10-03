import os
import pandas as pd
import streamlit as st

# ====== File Excel ======
excel_file = "A787.xlsx"

# ====== Load & clean Excel ======
def load_and_clean(sheet):
    df = pd.read_excel(excel_file, sheet_name=sheet)
    df.columns = df.columns.str.strip().str.upper()
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("").astype(str).str.strip()
    return df

# ====== CSS Vintage với overlay vàng ======
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

.stApp {
    background: linear-gradient(rgba(255,235,175,0.4), rgba(255,235,175,0.4)), 
                url('airplane.jpg');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    font-family: 'Special+Elite', cursive !important;
    filter: sepia(0.25) contrast(1.05) brightness(1.05);
    position: relative;
}

.block-container {
    position: relative;
    z-index: 1;
    padding-top: 0rem !important;
}

header[data-testid="stHeader"] {display: none;}

/* Tiêu đề */
.top-title {
    font-size: 34px;
    font-weight: 900;
    text-align: center;
    margin: 15px 0 5px 0;
    color: #3e2723;
    text-shadow: 1px 1px #fff;
}
.main-title {
    font-size: 24px;
    text-align: center;
    margin-bottom: 20px;
    color: #5d4037;
}

/* Label câu hỏi */
label, div[role="group"] label {
    font-family: 'Special Elite', cursive !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    color: #2c1a0c !important;
    text-shadow: 0.5px 0.5px 0.8px #fff;
}

/* Dropdown */
.stSelectbox div[data-baseweb="select"],
.stSelectbox div[data-baseweb="popover"] {
    font-family: 'Special Elite', cursive !important;
    font-size: 15px !important;
    color: #2c1a0c !important;
    background: #fdf6e3 !important;
    border: 1px solid #5d4037 !important;
    border-radius: 6px !important;
}

/* Bảng vintage */
table.dataframe {
    border-collapse: collapse;
    width: 100%;
    background: #fffaf0;
    font-family: 'Special Elite', cursive !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}
table.dataframe thead th {
    background: #5d4037 !important;
    color: #f8f1df !important;
    padding: 8px;
}
table.dataframe tbody td {
    padding: 6px;
    border: 1px solid #d9cbb5;
    color: #3e2723;
}
table.dataframe tbody tr:nth-child(even) td {
    background: #f6efe0 !important;
}
table.dataframe tbody tr:hover td {
    background: #fceec8 !important;
}

/* Thông báo */
.highlight-msg {
    font-size: 18px;
    font-weight: bold;
    color: #3e2723;
    background: #e9decf;
    padding: 10px;
    border-left: 6px solid #3e2723;
    border-radius: 5px;
    margin: 12px 0;
}
</style>
""", unsafe_allow_html=True)

# ====== Header ======
st.markdown('<div class="top-title">📜 Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🔎 Tra cứu Part number</div>', unsafe_allow_html=True)

# ====== App logic ======
if not os.path.exists(excel_file):
    st.error(f"⚠️ Không tìm thấy file {excel_file}")
    st.stop()

xls = pd.ExcelFile(excel_file)

zone = st.selectbox("📂 Bạn muốn tra cứu zone nào?", xls.sheet_names)
if zone:
    df = load_and_clean(zone)

    aircraft = None
    if "A/C" in df.columns:
        aircrafts = sorted(df["A/C"].dropna().unique().tolist())
        aircraft = st.selectbox("✈️ Loại máy bay?", aircrafts)

    if aircraft:
        df_ac = df[df["A/C"] == aircraft]

        description = None
        if "DESCRIPTION" in df_ac.columns:
            desc_list = sorted(df_ac["DESCRIPTION"].dropna().unique().tolist())
            description = st.selectbox("📑 Bạn muốn tra cứu phần nào?", desc_list)

        if description:
            df_desc = df_ac[df_ac["DESCRIPTION"] == description]

            if "ITEM" in df_desc.columns:
                items = sorted(df_desc["ITEM"].dropna().unique().tolist())
                if items:
                    item = st.selectbox("🔢 Item nào?", items)
                    df_desc = df_desc[df_desc["ITEM"] == item]

            if not df_desc.empty:
                df_result = df_desc.reset_index(drop=True)

                cols_to_show = ["PART NUMBER (PN)"]
                for alt_col in ["PART INTERCHANGE", "PN INTERCHANGE"]:
                    if alt_col in df_result.columns:
                        cols_to_show.append(alt_col)
                        break
                if "NOTE" in df_result.columns:
                    cols_to_show.append("NOTE")

                df_result = df_result[cols_to_show]
                df_result.insert(0, "STT", range(1, len(df_result)+1))

                st.markdown(f'<div class="highlight-msg">✅ Tìm thấy {len(df_result)} dòng dữ liệu</div>', unsafe_allow_html=True)
                st.write(df_result.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.error("❌ Không tìm thấy dữ liệu.")
