import streamlit as st
import pandas as pd
import base64
import os

# --- CẤU HÌNH ---
st.set_page_config(page_title="Tổ Bảo Dưỡng Số 1 - Tra Cứu PN", layout="wide")

# --- HÀM HỖ TRỢ ---
def get_base64_encoded_file(file_path):
    # Kiểm tra xem file có tồn tại và không rỗng không
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return ""
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def load_and_clean(excel_file, sheet):
    try:
        df = pd.read_excel(excel_file, sheet_name=sheet)
        df.columns = df.columns.str.strip().str.upper()
        # Loại bỏ các hàng hoàn toàn rỗng và thay thế chuỗi rỗng/chỉ chứa khoảng trắng bằng NA
        df = df.replace(r'^\s*$', pd.NA, regex=True).dropna(how="all")
        # Xử lý cột object (string)
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].fillna("").astype(str).str.strip()
        return df
    except Exception:
        # Trả về DataFrame rỗng nếu có lỗi
        return pd.DataFrame()

# --- NỀN ---
bg_pc_base64 = get_base64_encoded_file("PN_PC.jpg")
bg_mobile_base64 = get_base64_encoded_file("PN_mobile.jpg")

# --- CSS TOÀN BỘ ---
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

/* === TIÊU ĐỀ CHÍNH (PC) - Đã chỉnh lại để scroll hoạt động === */
#main-animated-title-container {{
    width: 100%;
    height: 110px;
    **overflow: hidden;** /* Giữ lại để ẩn phần thừa */
    text-align: center;
    margin-top: 35px;
}}
#main-animated-title-container h1 {{
    font-family: 'Oswald', sans-serif;
    font-size: 4.5rem;
    font-weight: 700;
    letter-spacing: 6px;
    text-transform: uppercase;
    **white-space: nowrap;** /* Rất quan trọng để chữ chạy */
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
        **overflow: hidden;** /* Giữ lại */
        height: auto;
        **white-space: nowrap;** /* Rất quan trọng để chữ chạy */
    }}

    #main-animated-title-container h1 {{
        font-size: 8vw;
        line-height: 1.1;
        letter-spacing: 3px;
        display: inline-block;
        **white-space: nowrap;** /* Đã đảm bảo có */
        animation: colorShift 10s ease infinite, scrollText 10s linear infinite;
        text-shadow: 2px 2px 7px rgba(0,0,0,0.8);
    }}

    #sub-static-title h2 {{
        font-size: 5vw;
        color: #FFD54F;
        margin-top: 10px;
    }}
}}

/* === LABEL SELECTBOX === */
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

/* === BẢNG HTML TÙY CHỈNH === */
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
    **display: table;** /* Giúp hiển thị đúng trên mobile */
}}

.custom-table thead {{
    display: table-header-group;
}}

.custom-table tbody {{
    display: table-row-group;
}}

.custom-table tr {{
    display: table-row;
}}

.custom-table th {{
    background-color: #2E7D32;
    color: white;
    padding: 14px;
    text-align: center !important;
    font-weight: bold;
    border: 1px solid #ddd;
    font-size: 1.05rem;
    display: table-cell;
}}

.custom-table td {{
    padding: 12px;
    text-align: center !important;
    border: 1px solid #ddd;
    vertical-align: middle;
    font-size: 1rem;
    display: table-cell;
}}

.custom-table tr:nth-child(even) {{
    background-color: #f9f9f9;
}}

.custom-table tr:hover {{
    background-color: #f5f5f5;
}}

/* === Mobile optimization - Đã chỉnh lại để kết quả hiển thị === */
@media (max-width: 768px) {{
    .table-container {{
        overflow-x: scroll;
        -webkit-overflow-scrolling: touch;
    }}
    
    .custom-table {{
        font-size: 0.85rem;
        min-width: **100%**; /* Đảm bảo tối thiểu 100% */
        display: table; /* Đã có ở trên, nhưng giữ lại */
    }}
    
    .custom-table th, .custom-table td {{
        padding: 8px 6px;
        font-size: 0.85rem;
        **white-space: normal;** /* Rất quan trọng, cho phép ngắt dòng nếu cần */
        word-wrap: break-word; /* Hỗ trợ ngắt từ */
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

        # --- CANH GIỮA DROPBOX ---
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        # Dropbox 1
        with col1:
            zone = st.selectbox("📂 **Zone**", sheet_names) 
        df = load_and_clean(excel_file, zone)

        # Dropbox 2
        with col2:
            aircrafts = sorted(df["A/C"].dropna().unique().tolist()) if "A/C" in df.columns else []
            aircraft = st.selectbox("✈️ **Loại máy bay**", aircrafts) if aircrafts else None
        df = df[df["A/C"] == aircraft] if aircraft else df

        # Dropbox 3
        with col3:
            descs = sorted(df["DESCRIPTION"].dropna().unique().tolist()) if "DESCRIPTION" in df.columns else []
            desc = st.selectbox("📑 **Mô tả chi tiết**", descs) if descs else None
        df = df[df["DESCRIPTION"] == desc] if desc else df

        # Dropbox 4
        with col4:
            items = sorted(df["ITEM"].dropna().unique().tolist()) if "ITEM" in df.columns else []
            item = st.selectbox("🔢 **Item**", items) if items else None
        df = df[df["ITEM"] == item] if item else df
        st.markdown("</div>", unsafe_allow_html=True)

        # --- HIỂN THỊ KẾT QUẢ ---
        df_display = df.drop(columns=["A/C", "ITEM", "DESCRIPTION"], errors="ignore")
        df_display = df_display.dropna(axis=1, how="all")

        # Chỉ hiển thị nếu có dữ liệu thực sự
        if not df_display.empty and len(df_display) > 0:
            st.markdown("---")
            st.markdown("<h3 style='text-align:center; color:#2E7D32;'>📋 KẾT QUẢ TRA CỨU</h3>", unsafe_allow_html=True)
            
            df_display = df_display.reset_index(drop=True)

            # Thêm cột STT vào trước PART NUMBER
            cols = list(df_display.columns)
            if "PART NUMBER" in cols:
                idx = cols.index("PART NUMBER")
                df_display.insert(idx, "STT", range(1, len(df_display) + 1))
            else:
                df_display.insert(0, "STT", range(1, len(df_display) + 1))

            # Tạo HTML table hoàn toàn custom
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
                    # Đảm bảo convert tất cả giá trị sang string
                    html_parts.append(f'<td>{str(val) if pd.notna(val) else ""}</td>')
                html_parts.append('</tr>')
            html_parts.append('</tbody>')
            
            html_parts.append('</table>')
            html_parts.append('</div>')
            
            # Hiển thị bảng
            st.markdown(''.join(html_parts), unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Lỗi khi đọc file Excel: {e}")
