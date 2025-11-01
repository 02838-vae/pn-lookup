import streamlit as st
import pandas as pd
import base64
import os

# --- CẤU HÌNH BAN ĐẦU ---
st.set_page_config(
    page_title="Tổ Bảo Dưỡng Số 1 - Tra Cứu PN",
    layout="wide",
)

# --- HÀM TIỆN ÍCH ---
def get_base64_encoded_file(file_path):
    """Đọc file và trả về Base64 encoded string (fallback nếu lỗi)."""
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

# --- TẢI ẢNH NỀN ---
bg_pc_base64 = get_base64_encoded_file("PN_PC.jpg")
bg_mobile_base64 = get_base64_encoded_file("PN_mobile.jpg")  # đúng chữ thường

# --- GIAO DIỆN CHÍNH ---
def render_main_interface():
    excel_file = "A787.xlsx"
    if not os.path.exists(excel_file):
        st.error("❌ Không tìm thấy file A787.xlsx. Vui lòng đặt file này cùng thư mục.")
        st.stop()

    bg_img_base64 = get_base64_encoded_file("PN_PC.jpg")
    bg_mobile_img_base64 = get_base64_encoded_file("PN_mobile.jpg")

    # --- CSS HOÀN CHỈNH ---
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&display=swap');

    #MainMenu, footer, header {{visibility: hidden;}}
    .main {{ padding: 0; margin: 0; }}
    div.block-container {{ padding-top: 20px; }}

    /* PC background */
    .stApp {{
        font-family: 'Special Elite', cursive !important;
        background: linear-gradient(rgba(245, 242, 230, 0.5), rgba(245, 242, 230, 0.5)),
            url("data:image/jpeg;base64,{bg_img_base64}") no-repeat center center fixed;
        background-size: cover;
    }}

    /* Hiệu ứng màu & chạy ngang */
    @keyframes scrollText {{
        0% {{ transform: translateX(100vw); }}
        100% {{ transform: translateX(-100%); }}
    }}
    @keyframes colorShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /* Tiêu đề chính (PC) */
    #main-animated-title-container {{
        width: 100%; height: 60px; overflow: hidden; text-align: center; white-space: nowrap;
    }}
    #main-animated-title-container h1 {{
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem; font-weight: 900;
        letter-spacing: 5px; margin: 0; padding: 0 50px;
        display: inline-block;
        background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: colorShift 10s ease infinite, scrollText 20s linear infinite;
        text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.7);
    }}

    /* Chữ số 1 hiển thị đều cỡ với chữ */
    #main-animated-title-container h1 span.one {{
        font-family: 'Special Elite', cursive;
        font-size: 1.05em;
        display: inline-block;
        transform: translateY(-2%);
    }}

    /* Tiêu đề phụ */
    #sub-static-title h2 {{
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem; font-weight: 700;
        color: #1f77b4;
        text-align: center;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
        margin: 10px 0 20px 0;
        white-space: nowrap;
    }}

    /* MOBILE FIX */
    @media (max-width: 768px) {{
        .stApp {{
            background: linear-gradient(rgba(245, 242, 230, 0.5), rgba(245, 242, 230, 0.5)),
                url("data:image/jpeg;base64,{bg_mobile_img_base64}") no-repeat center center fixed !important;
            background-size: cover !important;
            background-attachment: fixed !important;
        }}

        #main-animated-title-container {{
            overflow: hidden;
            height: auto;
            white-space: nowrap;
        }}

        #main-animated-title-container h1 {{
            font-size: 7vw;
            letter-spacing: 2px;
            padding: 0 10px;
            animation: colorShift 10s ease infinite, scrollText 15s linear infinite;
            display: inline-block;
        }}

        #main-animated-title-container h1 span.one {{
            font-size: 1.08em;
            transform: translateY(-1%);
        }}

        #sub-static-title h2 {{
            font-size: 4.5vw;
            margin-top: 40px;
            margin-bottom: 20px;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

    # --- TIÊU ĐỀ ---
    st.markdown('<div id="main-animated-title-container"><h1>TỔ BẢO DƯỠNG SỐ <span class="one">1</span></h1></div>', unsafe_allow_html=True)
    st.markdown('<div id="sub-static-title"><h2>🔎 TRA CỨU PART NUMBER</h2></div>', unsafe_allow_html=True)
    st.markdown("---")

    # --- NỘI DUNG TRA CỨU ---
    try:
        xls = pd.ExcelFile(excel_file)
        sheet_names = [s for s in xls.sheet_names if not s.startswith("Sheet")]

        st.markdown("### Chọn thông số để tra cứu:")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            zone = st.selectbox("📂 Zone", sheet_names, key="select_zone")

        df = load_and_clean(excel_file, zone)

        with col2:
            if "A/C" in df.columns:
                aircrafts = sorted([ac for ac in df["A/C"].dropna().unique().tolist() if ac])
                aircraft = st.selectbox("✈️ Loại máy bay", aircrafts, key="select_ac")
            else:
                aircraft = None
        df_ac = df[df["A/C"] == aircraft] if aircraft else df

        with col3:
            if "DESCRIPTION" in df_ac.columns:
                desc_list = sorted([d for d in df_ac["DESCRIPTION"].dropna().unique().tolist() if d])
                description = st.selectbox("📑 Mô tả chi tiết", desc_list, key="select_desc")
            else:
                description = None
        df_desc = df_ac[df_ac["DESCRIPTION"] == description] if description else df_ac

        with col4:
            if "ITEM" in df_desc.columns:
                items = sorted([i for i in df_desc["ITEM"].dropna().unique().tolist() if i])
                item = st.selectbox("🔢 Item", items, key="select_item")
                df_desc = df_desc[df_desc["ITEM"] == item] if item else df_desc
            else:
                item = None

        st.markdown("---")
        st.markdown("### Kết quả tra cứu:")

        df_display = df_desc.drop(columns=["A/C", "ITEM", "DESCRIPTION"], errors="ignore").dropna(axis=1, how='all')
        if not df_display.empty:
            df_display.insert(0, "STT", range(1, len(df_display) + 1))
            st.markdown(f'<p style="color: green; font-weight: bold;">✅ Tìm thấy {len(df_display)} dòng dữ liệu</p>', unsafe_allow_html=True)
            st.dataframe(df_display)
        else:
            st.warning("📌 Không có dữ liệu phù hợp.")
    except Exception as e:
        st.error(f"Lỗi khi xử lý file Excel: {e}")

# --- CHẠY ---
render_main_interface()
