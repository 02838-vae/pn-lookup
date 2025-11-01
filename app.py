import streamlit as st
import pandas as pd
import base64
import os
import time

# --- CẤU HÌNH BAN ĐẦU ---

st.set_page_config(
    page_title="Tổ Bảo Dưỡng Số 1 - Tra Cứu PN",
    layout="wide",
)

# --- CÁC HÀM TIỆN ÍCH DÙNG CHUNG ---

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
bg_pc_base64 = get_base64_encoded_file("PN_PC.jpg") 
bg_mobile_base64 = get_base64_encoded_file("PN_MOBILE.jpg") 


# --- HÀM RENDER GIAO DIỆN CHÍNH (Part Number Lookup) ---
def render_main_interface():
    
    excel_file = "A787.xlsx"
    if not os.path.exists(excel_file):
        st.error("❌ Không tìm thấy file A787.xlsx. Vui lòng đặt file này vào cùng thư mục với script.")
        st.stop()
    
    # === CSS PHONG CÁCH VINTAGE VÀ BACKGROUND MẶC ĐỊNH (Đã điều chỉnh Mobile CSS) ===
    bg_img_base64 = get_base64_encoded_file("PN_PC.jpg")
    bg_mobile_img_base64 = get_base64_encoded_file("PN_MOBILE.jpg")
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&display=swap');
    
    /* Ẩn Streamlit mặc định */
    #MainMenu, footer, header {{visibility: hidden;}}
    .main {{ padding: 0; margin: 0; }}
    div.block-container {{ padding-top: 20px; }} 

    /* Nền tĩnh PC */
    .stApp {{
        font-family: 'Special Elite', cursive !important;
        --main-bg-url-pc: url("data:image/jpeg;base64,{bg_img_base64}");
        --main-bg-url-mobile: url("data:image/jpeg;base64,{bg_mobile_img_base64}");
        
        background: linear-gradient(rgba(245, 242, 230, 0.5), rgba(245, 242, 230, 0.5)),
            var(--main-bg-url-pc) no-repeat center center fixed;
        background-size: cover;
    }}
    .stApp::after {{
        content: ""; position: fixed; inset: 0;
        background: url("https://www.transparenttextures.com/patterns/aged-paper.png");
        opacity: 0.2; pointer-events: none; z-index: -1;
    }}
    
    /* Animations cho tiêu đề chạy */
    @keyframes scrollText {{ 0% {{ transform: translate(100vw, 0); }} 100% {{ transform: translate(-100%, 0); }} }}
    @keyframes colorShift {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}

    /* Tiêu đề 1: TỔ BẢO DƯỠNG SỐ 1 - Chạy và Đổi màu */
    #main-animated-title-container {{ 
        width: 100%; height: 60px; overflow: hidden; white-space: nowrap; 
        margin: 0 auto; padding: 0; 
    }}
    #main-animated-title-container h1 {{
        font-family: 'Playfair Display', serif; font-size: 3.5rem; font-weight: 900;
        letter-spacing: 5px; margin: 0; padding: 0 50px; 
        display: inline-block; 
        
        background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3);
        background-size: 400% 400%; 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        
        animation: colorShift 10s ease infinite, scrollText 20s linear infinite; 
        text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.7);
    }}

    /* Tiêu đề 2: TRA CỨU PART NUMBER - Căn giữa */
    #sub-static-title h2 {{
        font-family: 'Playfair Display', serif; font-size: 2.2rem; font-weight: 700;
        color: #1f77b4; 
        text-align: center;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
        margin: 10px 0 20px 0;
        white-space: nowrap; 
    }}
    
    /* Điều chỉnh font và màu cho các lựa chọn tra cứu */
    .stSelectbox label, .stMarkdown h3 {{
        color: #000080; 
        font-weight: bold;
    }}

    /* === MEDIA QUERY CHO MOBILE (<= 768px) === */
    @media (max-width: 768px) {{
        /* Đảm bảo dùng PN_MOBILE.jpg */
        .stApp {{ 
            background: linear-gradient(rgba(245, 242, 230, 0.5), rgba(245, 242, 230, 0.5)),
                var(--main-bg-url-mobile) no-repeat center center fixed;
            background-size: cover;
        }}

        /* Khắc phục lỗi thu nhỏ số 1 (Tăng font size) */
        #main-animated-title-container h1 {{ 
            font-size: 10vw; 
            letter-spacing: 3px; 
            height: 10vw; /* Tăng chiều cao container để chứa đủ font */
        }}

        /* Đẩy tiêu đề Tra Cứu Part Number xuống dưới */
        #sub-static-title h2 {{ 
            font-size: 6vw; 
            margin-top: 30px; /* Thêm khoảng cách phía trên */
            margin-bottom: 20px;
        }}
    }}
    
    </style>
    """, unsafe_allow_html=True)
    
    # ===== TIÊU ĐỀ 1: CHẠY VÀ ĐỔI MÀU =====
    st.markdown('<div id="main-animated-title-container"><h1>TỔ BẢO DƯỠNG SỐ 1</h1></div>', unsafe_allow_html=True)
    
    # ===== TIÊU ĐỀ 2: CĂN GIỮA VÀ TĨNH =====
    st.markdown('<div id="sub-static-title"><h2>🔎 TRA CỨU PART NUMBER</h2></div>', unsafe_allow_html=True)
    
    st.markdown("---") # Đường phân cách
    
    # ===== NỘI DUNG CHÍNH (Tra cứu Excel) =====
    try:
        xls = pd.ExcelFile(excel_file)
        sheet_names = [name for name in xls.sheet_names if not name.startswith("Sheet")]
        
        selection_container = st.container()
        
        with selection_container:
            st.markdown("### Chọn thông số để tra cứu:")
            
            # Chia cột cho selectbox (trên mobile sẽ tự động xếp chồng)
            col1, col2, col3, col4 = st.columns(4)
            
            # Chọn Zone
            with col1:
                zone = st.selectbox("📂 Zone", sheet_names, key="select_zone")
            
            df = load_and_clean(excel_file, zone)
            
            # Chọn Aircraft (A/C)
            with col2:
                if "A/C" in df.columns:
                    aircrafts = sorted([ac for ac in df["A/C"].dropna().unique().tolist() if ac])
                    aircraft = st.selectbox("✈️ Loại máy bay", aircrafts, key="select_ac")
                else:
                    aircraft = None
            
            df_ac = df[df["A/C"] == aircraft] if aircraft else df

            # Chọn Description
            with col3:
                if "DESCRIPTION" in df_ac.columns:
                    desc_list = sorted([d for d in df_ac["DESCRIPTION"].dropna().unique().tolist() if d])
                    description = st.selectbox("📑 Mô tả chi tiết", desc_list, key="select_desc")
                else:
                    description = None

            df_desc = df_ac[df_ac["DESCRIPTION"] == description] if description else df_ac

            # Chọn Item
            with col4:
                if "ITEM" in df_desc.columns:
                    items = sorted([i for i in df_desc["ITEM"].dropna().unique().tolist() if i])
                    item = st.selectbox("🔢 Item", items, key="select_item")
                    df_desc = df_desc[df_desc["ITEM"] == item] if item else df_desc
                else:
                    item = None


        # Hiển thị kết quả
        st.markdown("---") 
        st.markdown("### Kết quả tra cứu:")
        
        df_display = df_desc.drop(columns=["A/C", "ITEM", "DESCRIPTION"], errors="ignore")
        df_display = df_display.dropna(axis=1, how='all')

        if not df_display.empty:
            df_display.insert(0, "STT", range(1, len(df_display) + 1))
            st.markdown(f'<p style="color: green; font-weight: bold;">✅ Tìm thấy {len(df_display)} dòng dữ liệu</p>', unsafe_allow_html=True)
            st.dataframe(df_display)
        else:
            st.warning("📌 Không có dữ liệu phù hợp với các lựa chọn trên.")

    except Exception as e:
        st.error(f"Lỗi khi xử lý file Excel: {e}")


# --- LOGIC CHÍNH CỦA ỨNG DỤNG ---
render_main_interface()
