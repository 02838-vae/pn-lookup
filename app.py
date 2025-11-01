import streamlit as st
import pandas as pd
import base64
import os
import time

# --- CẤU HÌNH BAN ĐẦU VÀ LOGIC CHUYỂN TRANG ---

st.set_page_config(
    page_title="Tổ Bảo Dưỡng Số 1",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Khởi tạo session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Hàm Chuyển Trang (Navigation Logic)
def navigate_to(page_name):
    """Chuyển trang đơn giản qua session state"""
    if st.session_state.page != page_name:
        st.session_state.page = page_name
        st.rerun()

# --- CÁC HÀM TIỆN ÍCH DÙNG CHUNG (Giữ nguyên) ---

def get_base64_encoded_file(file_path, mime_type=""):
    """Đọc file và trả về Base64 encoded string."""
    fallback_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" 
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return fallback_base64
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode("utf-8")
    except Exception as e:
        return fallback_base64

def load_and_clean(excel_file, sheet):
    """Tải và làm sạch DataFrame từ Excel sheet."""
    try:
        df = pd.read_excel(excel_file, sheet_name=sheet)
        df.columns = df.columns.str.strip().str.upper()
        df = df.replace(r'^\s*$', pd.NA, regex=True).dropna(how="all")
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].fillna("").astype(str).str.strip()
        return df
    except Exception as e:
        return pd.DataFrame()


# --- TẢI FILE ẢNH NỀN ---
bg_pc_base64 = get_base64_encoded_file("cabbase.jpg") 
bg_mobile_base64 = get_base64_encoded_file("mobile.jpg")


# --- HÀM RENDER TRANG CHỦ (Tĩnh hoàn toàn) ---
def render_home_page():
    
    # 1. CSS CHUNG (Đã tinh giản tối đa)
    hide_streamlit_style = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap');
    
    /* Ẩn Streamlit mặc định */
    #MainMenu, footer, header {{visibility: hidden;}}
    .main {{ padding: 0; margin: 0; }}
    div.block-container {{ padding: 0; margin: 0; max-width: 100% !important; }}

    /* Nền tĩnh */
    .stApp {{
        --main-bg-url-pc: url('data:image/jpeg;base64,{bg_pc_base64}');
        --main-bg-url-mobile: url('data:image/jpeg;base64,{bg_mobile_base64}');
        background-color: black;
        background-image: var(--main-bg-url-pc); 
        background-size: cover; 
        background-position: center;
        background-attachment: fixed; 
        /* Hiệu ứng màu nền */
        filter: sepia(60%) grayscale(20%) brightness(85%) contrast(110%);
    }}
    @media (max-width: 768px) {{ .stApp {{ background-image: var(--main-bg-url-mobile); }} }}
    
    /* Animation cho tiêu đề chính */
    @keyframes scrollText {{ 0% {{ transform: translate(100vw, 0); }} 100% {{ transform: translate(-100%, 0); }} }}
    @keyframes colorShift {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}

    /* Tiêu đề: Luôn hiển thị */
    #main-title-container {{ 
        position: fixed; top: 5vh; left: 0; width: 100%; height: 10vh; 
        overflow: hidden; z-index: 100; pointer-events: none; opacity: 1; 
    }}
    #main-title-container h1 {{
        font-family: 'Playfair Display', serif; font-size: 3.5vw; margin: 0; font-weight: 900;
        letter-spacing: 5px; white-space: nowrap; display: inline-block;
        background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3);
        background-size: 400% 400%; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: colorShift 10s ease infinite, scrollText 15s linear infinite; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }}
    
    /* Container nút: Luôn hiển thị */
    .button-container-fixed {{
        position: fixed; top: 45vh; width: 100%; z-index: 100;
        display: flex; justify-content: center; gap: 60px;
        align-items: center; padding: 0 5vw; 
        box-sizing: border-box; opacity: 1; 
    }}
    
    /* Phong cách nút */
    .stButton > button {{
        display: block !important; padding: 8px 12px; text-align: center; text-decoration: none;
        color: #00ffff; font-family: 'Playfair Display', serif; font-size: 1.8rem; font-weight: 700; cursor: pointer; background-color: rgba(0, 0, 0, 0.4);
        border: 2px solid #00ffff; border-radius: 8px; box-sizing: border-box;
        text-shadow: 0 0 4px rgba(0, 255, 255, 0.8), 0 0 10px rgba(34, 141, 255, 0.6);
        box-shadow: 0 0 5px #00ffff, 0 0 15px rgba(0, 255, 255, 0.5);
        transition: transform 0.3s ease, color 0.3s ease, text-shadow 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        white-space: nowrap; flex-grow: 1; max-width: 400px; min-height: 60px; line-height: 1.2;
    }}
    .stButton > button:hover {{
        transform: scale(1.05); color: #ffd700; border-color: #ffd700;
        box-shadow: 0 0 5px #ffd700, 0 0 15px #ff8c00, 0 0 25px rgba(255, 215, 0, 0.7);
        text-shadow: 0 0 3px #ffd700, 0 0 8px #ff8c00;
    }}
    
    @media (max-width: 768px) {{
        .button-container-fixed {{ flex-direction: column; gap: 15px; top: 50vh; }}
        .stButton > button {{ font-size: 1.4rem; max-width: 90%; }}
        #main-title-container h1 {{ font-size: 6vw; }}
    }}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # --- TIÊU ĐỀ CHÍNH ---
    st.markdown(f"""
    <div id="main-title-container">
        <h1>TỔ BẢO DƯỠNG SỐ 1</h1>
    </div>
    """, unsafe_allow_html=True)

    # --- NÚT CHUYỂN TRANG ---
    st.markdown('<div class="button-container-fixed">', unsafe_allow_html=True)
    col_part, col_quiz = st.columns([1, 1])

    with col_part:
        if st.button("Tra cứu Part Number 🔍", key="btn_part_number_home", help="Chuyển đến trang tra cứu"):
            navigate_to('part_number')

    with col_quiz:
        if st.button("Ngân hàng trắc nghiệm 📋✅", key="btn_quiz_bank_home", help="Chuyển đến trang trắc nghiệm"):
            navigate_to('quiz_bank')
    st.markdown('</div>', unsafe_allow_html=True)


# --- HÀM RENDER TRANG TRA CỨU PART NUMBER (Giữ nguyên logic) ---
def render_part_number_page():
    
    excel_file = "A787.xlsx"
    if not os.path.exists(excel_file):
        st.error("❌ Không tìm thấy file A787.xlsx")
        st.stop()
    
    # === CSS PHONG CÁCH VINTAGE ===
    bg_img_base64 = get_base64_encoded_file("cabbase.jpg")
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');
    
    .stApp {{
        font-family: 'Special Elite', cursive !important;
        background: linear-gradient(rgba(245, 242, 230, 0.5), rgba(245, 242, 230, 0.5)),
            url("data:image/jpeg;base64,{bg_img_base64}") no-repeat center center fixed;
        background-size: cover;
    }}
    .stApp::after {{
        content: ""; position: fixed; inset: 0;
        background: url("https://www.transparenttextures.com/patterns/aged-paper.png");
        opacity: 0.2; pointer-events: none; z-index: -1;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Thêm nút quay lại trang chủ
    if st.button("⬅️ Quay lại Trang Chủ", key="back_home_part", help="Trở về màn hình giới thiệu", type="secondary"):
        navigate_to('home')

    # ===== TIÊU ĐỀ =====
    st.markdown('<div class="main-title">📜 TỔ BẢO DƯỠNG SỐ 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">🔎 TRA CỨU PART NUMBER</div>', unsafe_allow_html=True)
    
    # ===== NỘI DUNG CHÍNH (Tra cứu Excel) =====
    try:
        xls = pd.ExcelFile(excel_file)
        sheet_names = [name for name in xls.sheet_names if not name.startswith("Sheet")]
        
        zone = st.selectbox("📂 Bạn muốn tra cứu zone nào?", sheet_names, key="select_zone")
        
        if zone:
            df = load_and_clean(excel_file, zone)
            
            # Logic lọc dữ liệu...
            if "A/C" in df.columns:
                aircrafts = sorted([ac for ac in df["A/C"].dropna().unique().tolist() if ac])
                aircraft = st.selectbox("✈️ Loại máy bay?", aircrafts, key="select_ac")
            else:
                aircraft = None

            df_ac = df[df["A/C"] == aircraft] if aircraft else df

            if "DESCRIPTION" in df_ac.columns:
                desc_list = sorted([d for d in df_ac["DESCRIPTION"].dropna().unique().tolist() if d])
                description = st.selectbox("📑 Bạn muốn tra cứu phần nào?", desc_list, key="select_desc")
            else:
                description = None

            df_desc = df_ac[df_ac["DESCRIPTION"] == description] if description else df_ac

            if "ITEM" in df_desc.columns:
                items = sorted([i for i in df_desc["ITEM"].dropna().unique().tolist() if i])
                item = st.selectbox("🔢 Bạn muốn tra cứu Item nào?", items, key="select_item")
                df_desc = df_desc[df_desc["ITEM"] == item] if item else df_desc

            # Lọc và hiển thị
            df_display = df_desc.drop(columns=["A/C", "ITEM", "DESCRIPTION"], errors="ignore")
            df_display = df_display.dropna(axis=1, how='all')

            if not df_display.empty:
                df_display.insert(0, "STT", range(1, len(df_display) + 1))
                st.markdown(f'<div class="highlight-msg">✅ Tìm thấy {len(df_display)} dòng dữ liệu</div>', unsafe_allow_html=True)
                st.dataframe(df_display)
            else:
                st.warning("📌 Không có dữ liệu phù hợp.")

    except Exception as e:
        st.error(f"Lỗi khi xử lý file Excel: {e}")


# --- HÀM RENDER TRANG QUIZ BANK (Giữ nguyên logic) ---
def render_quiz_bank_page():
    st.markdown("""
    <style>
    .back-to-home-btn { position: fixed; top: 20px; left: 20px; z-index: 100; }
    .stApp { background: #3a3a3a; color: white; transition: background-color 1s; }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("Ngân hàng trắc nghiệm 📋✅")
    
    if st.button("⬅️ Quay lại Trang Chủ", key="back_home_quiz"):
        navigate_to('home')
        
    st.markdown("---")
    st.info("### Trang này đang được xây dựng!")


# --- LOGIC ĐIỀU HƯỚNG CHÍNH CỦA ỨNG DỤNG ---

if st.session_state.page == 'part_number':
    render_part_number_page() 
elif st.session_state.page == 'quiz_bank':
    render_quiz_bank_page()
else: # st.session_state.page == 'home'
    render_home_page()
