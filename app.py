import streamlit as st
import pandas as pd
import base64
import os

# --- CẤU HÌNH ---
st.set_page_config(page_title="Tổ Bảo Dưỡng Số 1 - Tra Cứu PN", layout="wide")

# --- HÀM HỖ TRỢ ---
def get_base64_encoded_file(file_path):
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return ""
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def load_and_clean(excel_file, sheet):
    try:
        df = pd.read_excel(excel_file, sheet_name=sheet)
        df.columns = df.columns.str.strip().str.upper()
        df = df.replace(r'^\s*$', pd.NA, regex=True).dropna(how="all")
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].fillna("").astype(str).str.strip()
        return df
    except Exception:
        return pd.DataFrame()

# --- NỀN ---
bg_pc_base64 = get_base64_encoded_file("PN_PC.jpg")
bg_mobile_base64 = get_base64_encoded_file("PN_mobile.jpg")

# --- CSS TOÀN BỘ ---
# Đã điều chỉnh CSS mobile để hiển thị kết quả tốt hơn
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');

#MainMenu, footer, header {{visibility: hidden;}}
div.block-container {{padding-top: 0;}}

/* === NỀN PC === */
.stAppViewContainer, .st-emotion-cache-1r6slb0 {{
    background: url("data:image/jpeg;base64,{bg_pc_base64}") no-repeat center top fixed !important;
    background-size: cover !important;
    font-family: 'Oswald', sans-serif !important;
}}

/* === HIỆU ỨNG CHỮ === */
@keyframes scrollText {{
    0% {{ transform: translateX(100vw); }}
    100% {{ transform: translateX(-100%); }}
}}
@keyframes colorShift {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

/* === TIÊU ĐỀ CHÍNH (PC) - Đã thêm white-space: nowrap để khôi phục chạy === */
#main-animated-title-container {{
    width: 100%;
    height: 110px;
    overflow: hidden;
    text-align: center;
    margin-top: 35px;
}}
#main-animated-title-container h1 {{
    font-family: 'Oswald', sans-serif;
    font-size: 4.5rem;
    font-weight: 700;
    letter-spacing: 6px;
    text-transform: uppercase;
    white-space: nowrap; /* Khôi phục chạy */
    display: inline-block;
    background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3);
    background-size: 400% 400%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: colorShift 10s ease infinite, scrollText 12s linear infinite;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.7);
    line-height: 1.3;
    padding-bottom: 10px;
}}

/* === TIÊU ĐỀ PHỤ === */
#sub-static-title h2 {{
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    color: #FFD54F;
    text-align: center;
    text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
    margin-top: 35px;
    margin-bottom: 20px;
}}

/* === MOBILE === */
@media (max-width: 768px) {{
    .stAppViewContainer, .st-emotion-cache-1r6slb0 {{
        background: url("data:image/jpeg;base64,{bg_mobile_base64}") no-repeat center top scroll !important;
        background-size: cover !important;
    }}

    #main-animated-title-container {{
        margin-top: 10px !important;
        overflow: hidden;
        height: auto;
    }}

    #main-animated-title-container h1 {{
        font-size: 8vw;
        line-height: 1.1;
        letter-spacing: 3px;
        display: inline-block;
        white-space: nowrap; /* Khôi phục chạy */
        animation: colorShift 10s ease infinite, scrollText 10s linear infinite;
        text-shadow: 2px 2px 7px rgba(0,0,0,0.8);
    }}

    #sub-static-title h2 {{
        font-size: 5vw;
        color: #FFD54F;
        margin-top: 10px;
    }}
}}

/* === LABEL SELECTBOX (Dropdown to hơn) === */
.stSelectbox label {{
    color: #FFEB3B !important;
    font-weight: 700 !important;
    text-align: center;
    display: block;
    font-size: 2.2rem !important; 
    line-height: 2.5rem !important;
}}

/* Force override Streamlit default */
[data-testid="stWidgetLabel"] {{
    font-size: 2.2rem !important;
    color: #FFEB3B !important;
    font-weight: 700 !important;
}}

div[data-baseweb="select"] {{
    min-width: 250px !important;
}}
div[data-baseweb="select"] > div {{
    text-align: center;
    font-size: 1.1rem;
}}

/* Mobile label size */
@media (max-width: 768px) {{
    .stSelectbox label, [data-testid="stWidgetLabel"] {{
        font-size: 1.2rem !important;
    }}
}}

/* === CANH GIỮA DROPBOX CONTAINER === */
.element-container:has(.stSelectbox) {{
    display: flex;
    justify-content: center;
}}

/* === BẢNG HTML TÙY CHỈNH (Điều chỉnh để khắc phục lỗi Mobile) === */
.table-container {{
    overflow-x: auto;
    margin: 20px 0;
    width: 100%;
}}

.custom-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 20px auto;
    background-color: white;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}}

.custom-table th {{
    background-color: #2E7D32;
    color: white;
    padding: 14px;
    text-align: center !important;
    font-weight: bold;
    border: 1px solid #ddd;
    font-size: 1.05rem;
}}

.custom-table td {{
    padding: 12px;
    text-align: center !important;
    border: 1px solid #ddd;
    vertical-align: middle;
    font-size: 1rem;
}}

.custom-table tr:nth-child(even) {{
    background-color: #f9f9f9;
}}

.custom-table tr:hover {{
    background-color: #f5f5f5;
}}

/* === Mobile optimization === */
@media (max-width: 768px) {{
    .table-container {{
        overflow-x: scroll;
        -webkit-overflow-scrolling: touch;
    }}
    
    .custom-table {{
        font-size: 0.85rem;
        min-width: 100%;
    }}
    
    .custom-table th, .custom-table td {{
        padding: 8px 6px;
        font-size: 0.85rem;
        white-space: normal; 
        word-wrap: break-word; 
    }}
}}
</style>
""", unsafe_allow_html=True)

# --- TIÊU ĐỀ ---
st.markdown('<div id="main-animated-title-container"><h1>TỔ BẢO DƯỠNG SỐ 1</h1></div>', unsafe_allow_html=True)
st.markdown('<div id="sub-static-title"><h2>🔎 TRA CỨU PART NUMBER</h2></div>', unsafe_allow_html=True)
st.markdown("---")

# --- TRA CỨU ---
excel_file = "A787.xlsx"
if not os.path.exists(excel_file):
    st.error("❌ Không tìm thấy file A787.xlsx trong thư mục hiện tại.")
else:
    try:
        xls = pd.ExcelFile(excel_file)
        sheet_names = [name for name in xls.sheet_names if not name.startswith("Sheet")]

        # --- KHỞI TẠO GIÁ TRỊ BAN ĐẦU ---
        zone = None
        aircraft = None
        desc = None
        item = None
        df = pd.DataFrame()

        # --- CANH GIỮA DROPBOX ---
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        # Dropbox 1 (Zone)
        with col1:
            # Tạo list zone và thêm một giá trị placeholder nếu cần
            zone_options = ["Chọn Zone..."] + sheet_names
            zone_selected = st.selectbox("📂 **Zone**", zone_options)
            if zone_selected != "Chọn Zone...":
                zone = zone_selected
        
        if zone:
            df = load_and_clean(excel_file, zone)
        else:
            df = pd.DataFrame() # Đảm bảo df rỗng nếu chưa chọn zone

        # Dropbox 2 (Loại máy bay)
        with col2:
            aircrafts = sorted(df["A/C"].dropna().unique().tolist()) if "A/C" in df.columns and not df.empty else []
            aircraft_options = ["Chọn Loại máy bay..."] + aircrafts
            aircraft_selected = st.selectbox("✈️ **Loại máy bay**", aircraft_options)
            if aircraft_selected != "Chọn Loại máy bay...":
                aircraft = aircraft_selected
        df = df[df["A/C"] == aircraft] if aircraft and "A/C" in df.columns and not df.empty else df

        # Dropbox 3 (Mô tả chi tiết)
        with col3:
            descs = sorted(df["DESCRIPTION"].dropna().unique().tolist()) if "DESCRIPTION" in df.columns and not df.empty else []
            desc_options = ["Chọn Mô tả..."] + descs
            desc_selected = st.selectbox("📑 **Mô tả chi tiết**", desc_options)
            if desc_selected != "Chọn Mô tả...":
                desc = desc_selected
        df = df[df["DESCRIPTION"] == desc] if desc and "DESCRIPTION" in df.columns and not df.empty else df

        # Dropbox 4 (Item)
        with col4:
            items = sorted(df["ITEM"].dropna().unique().tolist()) if "ITEM" in df.columns and not df.empty else []
            item_options = ["Chọn Item..."] + items
            item_selected = st.selectbox("🔢 **Item**", item_options)
            if item_selected != "Chọn Item...":
                item = item_selected
        df = df[df["ITEM"] == item] if item and "ITEM" in df.columns and not df.empty else df
        
        st.markdown("</div>", unsafe_allow_html=True)

        # --- HIỂN THỊ KẾT QUẢ ---
        
        # Điều kiện hiển thị bảng kết quả: 
        # 1. Cần chọn cả 4 dropbox (zone, aircraft, desc, item) KHÔNG rỗng/None.
        # 2. DataFrame kết quả (df) phải không rỗng.
        
        is_fully_selected = bool(zone and aircraft and desc and item)
        is_result_available = not df.empty and len(df) > 0

        if is_fully_selected and is_result_available:
            st.markdown("---")
            st.markdown("<h3 style='text-align:center; color:#2E7D32;'>📋 KẾT QUẢ TRA CỨU</h3>", unsafe_allow_html=True)
            
            df_display = df.drop(columns=["A/C", "ITEM", "DESCRIPTION"], errors="ignore")
            df_display = df_display.dropna(axis=1, how="all")
            df_display = df_display.reset_index(drop=True)

            # Thêm cột STT
            cols = list(df_display.columns)
            if "PART NUMBER" in cols:
                idx = cols.index("PART NUMBER")
                df_display.insert(idx, "STT", range(1, len(df_display) + 1))
            else:
                df_display.insert(0, "STT", range(1, len(df_display) + 1))

            # Tạo HTML table
            html_parts = ['<div class="table-container">']
            html_parts.append('<table class="custom-table">')
            
            # Header
            html_parts.append('<thead><tr>')
            for col in df_display.columns:
                html_parts.append(f'<th>{str(col)}</th>')
            html_parts.append('</tr></thead>')
            
            # Body
            html_parts.append('<tbody>')
            for idx, row in df_display.iterrows():
                html_parts.append('<tr>')
                for val in row:
                    html_parts.append(f'<td>{str(val) if pd.notna(val) else ""}</td>')
                html_parts.append('</tr>')
            html_parts.append('</tbody>')
            
            html_parts.append('</table>')
            html_parts.append('</div>')
            
            # Hiển thị bảng
            st.markdown(''.join(html_parts), unsafe_allow_html=True)
        
        elif is_fully_selected and not is_result_available:
             st.markdown("---")
             st.info("⚠️ **Không tìm thấy kết quả** nào phù hợp với tất cả các lựa chọn của bạn.")

        # Xử lý trường hợp chưa chọn đủ 4 dropbox (không hiển thị gì)
        
    except Exception as e:
        st.error(f"Lỗi khi đọc file Excel: {e}")
