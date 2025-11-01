import streamlit as st
import pandas as pd
import base64
import os

# --- CẤU HÌNH ---
st.set_page_config(
    page_title="Tổ Bảo Dưỡng Số 1 - Tra Cứu PN",
    layout="wide",
)

# --- HÀM TIỆN ÍCH ---
def get_base64_encoded_file(file_path):
    fallback_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return fallback_base64
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode("utf-8")
    except:
        return fallback_base64

def load_and_clean(excel_file, sheet):
    try:
        df = pd.read_excel(excel_file, sheet_name=sheet)
        df.columns = df.columns.str.strip().str.upper()
        df = df.replace(r'^\s*$', pd.NA, regex=True).dropna(how="all")
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].fillna("").astype(str).str.strip()
        return df
    except:
        return pd.DataFrame()

# --- ẢNH NỀN ---
bg_pc_base64 = get_base64_encoded_file("PN_PC.jpg")
bg_mobile_base64 = get_base64_encoded_file("PN_mobile.jpg")

# --- GIAO DIỆN CHÍNH ---
def render_main_interface():
    excel_file = "A787.xlsx"
    if not os.path.exists(excel_file):
        st.error("❌ Không tìm thấy file A787.xlsx.")
        st.stop()

    # --- CSS ---
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');

    #MainMenu, footer, header {{visibility: hidden;}}
    div.block-container {{padding-top: 20px;}}

    /* PC BACKGROUND */
    .stApp {{
        font-family: 'Oswald', sans-serif !important;
        background-image: url("data:image/jpeg;base64,{bg_pc_base64}");
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center center;
        background-size: cover;
    }}

    /* Hiệu ứng chạy + màu */
    @keyframes scrollText {{
        0% {{ transform: translateX(100vw); }}
        100% {{ transform: translateX(-100%); }}
    }}
    @keyframes colorShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /* TIÊU ĐỀ CHÍNH */
    #main-animated-title-container {{
        width: 100%; height: 70px;
        overflow: hidden;
        white-space: nowrap;
        text-align: center;
    }}
    #main-animated-title-container h1 {{
        font-family: 'Oswald', sans-serif;
        font-size: 4rem;
        font-weight: 700;
        letter-spacing: 5px;
        margin: 0; padding: 0 40px;
        display: inline-block;
        text-transform: uppercase;
        background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: colorShift 10s ease infinite, scrollText 18s linear infinite;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
    }}

    /* TIÊU ĐỀ PHỤ */
    #sub-static-title h2 {{
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        color: #1f77b4;
        text-align: center;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
        margin: 10px 0 20px 0;
    }}

    /* MOBILE FIX */
    @media (max-width: 768px) {{
        .stApp {{
            background-image: url("data:image/jpeg;base64,{bg_mobile_base64}") !important;
            background-repeat: no-repeat !important;
            background-attachment: scroll !important;
            background-position: center center !important;
            background-size: cover !important;
        }}

        #main-animated-title-container {{
            overflow: hidden;
            height: auto;
            white-space: nowrap;
        }}
        #main-animated-title-container h1 {{
            font-size: 8.5vw;
            letter-spacing: 3px;
            padding: 0 10px;
            line-height: 1;
            display: inline-block;
            white-space: nowrap;
            animation: colorShift 10s ease infinite, scrollText 15s linear infinite;
        }}

        #sub-static-title h2 {{
            font-size: 4.5vw;
            margin-top: 35px;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

    # --- TIÊU ĐỀ ---
    st.markdown('<div id="main-animated-title-container"><h1>TỔ BẢO DƯỠNG SỐ 1</h1></div>', unsafe_allow_html=True)
    st.markdown('<div id="sub-static-title"><h2>🔎 TRA CỨU PART NUMBER</h2></div>', unsafe_allow_html=True)
    st.markdown("---")

    # --- TRA CỨU EXCEL ---
    try:
        xls = pd.ExcelFile(excel_file)
        sheet_names = [s for s in xls.sheet_names if not s.startswith("Sheet")]

        st.markdown("### Chọn thông số để tra cứu:")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            zone = st.selectbox("📂 Zone", sheet_names, key="select_zone")

        df = load_and_clean(excel_file, zone)

        with col2:
            aircraft = st.selectbox("✈️ Loại máy bay", sorted(df["A/C"].dropna().unique())) if "A/C" in df.columns else None
        df_ac = df[df["A/C"] == aircraft] if aircraft else df

        with col3:
            description = st.selectbox("📑 Mô tả chi tiết", sorted(df_ac["DESCRIPTION"].dropna().unique())) if "DESCRIPTION" in df_ac.columns else None
        df_desc = df_ac[df_ac["DESCRIPTION"] == description] if description else df_ac

        with col4:
            item = st.selectbox("🔢 Item", sorted(df_desc["ITEM"].dropna().unique())) if "ITEM" in df_desc.columns else None
            df_desc = df_desc[df_desc["ITEM"] == item] if item else df_desc

        st.markdown("---")
        st.markdown("### Kết quả tra cứu:")

        df_display = df_desc.drop(columns=["A/C", "ITEM", "DESCRIPTION"], errors="ignore").dropna(axis=1, how='all')
        if not df_display.empty:
            df_display.insert(0, "STT", range(1, len(df_display) + 1))
            st.markdown(f'<p style="color:green;font-weight:bold;">✅ Tìm thấy {len(df_display)} dòng dữ liệu</p>', unsafe_allow_html=True)
            st.dataframe(df_display)
        else:
            st.warning("📌 Không có dữ liệu phù hợp.")
    except Exception as e:
        st.error(f"Lỗi khi xử lý file Excel: {e}")

# --- CHẠY ---
render_main_interface()
