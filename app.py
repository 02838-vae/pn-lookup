import streamlit as st
import pandas as pd
import base64
import os
import time

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

# --- CSS TOÀN BỘ (bao gồm chỉnh label selectbox) ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');

#MainMenu, footer, header {{visibility: hidden;}}
div.block-container {{padding-top: 0; background-color: transparent !important;}} 
[data-testid="stVerticalBlock"] > div:first-child {{background-color: transparent !important;}}

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

/* === TIÊU ĐỀ CHÍNH (PC) === */
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
    white-space: nowrap; 
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
    .main > div {{
        background-color: transparent !important;
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
        white-space: nowrap; 
        animation: colorShift 10s ease infinite, scrollText 10s linear infinite;
        text-shadow: 2px 2px 7px rgba(0,0,0,0.8);
    }}
    #sub-static-title h2 {{
        font-size: 5vw;
        color: #FFD54F;
        margin-top: 10px;
    }}
}}

/* === LABEL SELECTBOX (ép thật sâu để chắc ăn) === */
div[data-testid="stSelectbox"] > label,
[data-testid="stSelectbox"] label,
[data-testid="stWidgetLabel"],
[data-testid="stSelectboxLabel"],
.css-16idsys.e16nr0p33,
.css-1offfwp.e1fqkh3o4
{{
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    color: #FFEB3B !important;
    text-align: center !important;
    text-shadow: 2px 2px 6px rgba(0,0,0,0.7) !important;
    line-height: 3.2rem !important;
    display: block !important;
    margin-bottom: 0.6rem !important;
    letter-spacing: 1px !important;
}}

@media (max-width: 768px) {{
    div[data-testid="stSelectbox"] > label,
    [data-testid="stWidgetLabel"],
    .css-16idsys.e16nr0p33,
    .css-1offfwp.e1fqkh3o4 {{
        font-size: 1.8rem !important;
        line-height: 2rem !important;
    }}
}}

/* === CANH GIỮA DROPBOX CONTAINER === */
.element-container:has(.stSelectbox) {{
    display: flex;
    justify-content: center;
    background-color: transparent !important; 
}}
[data-testid^="stHorizontalBlock"] {{
    background-color: transparent !important;
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
    box-shadow: 0 0 15px rgba(0,0,0,0.3); 
    border-radius: 8px; 
    overflow: hidden; 
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
    color: #000000;
}}

.custom-table tr:nth-child(even) {{
    background-color: #f9f9f9;
}}

.custom-table tr:hover {{
    background-color: #e0e0e0;
}}

@media (max-width: 768px) {{
    .custom-table {{
        font-size: 0.85rem;
        min-width: 100%;
        box-shadow: 0 0 10px rgba(0,0,0,0.5); 
    }}
    .custom-table th, .custom-table td {{
        padding: 8px 6px;
        font-size: 0.85rem;
        white-space: normal; 
        word-wrap: break-word; 
        color: #000000; 
    }}
}}
</style>
""", unsafe_allow_html=True)

# --- VIDEO INTRO ---
# Thay vì dùng st.user_agent (không tồn tại), ta cho 3 lựa chọn:
# 1) Nếu URL có ?mobile=1 => xem mobile.mp4
# 2) Ngược lại: ưu tiên airplane.mp4 nếu tồn tại, nếu không thì mobile.mp4
# 3) Nếu không có file nào, bỏ qua và không crash app

if st.session_state.get("video_shown") != True:
    try:
        params = st.experimental_get_query_params()
        force_mobile = False
        if params.get("mobile", ["0"])[0] in ("1", "true", "True"):
            force_mobile = True

        video_path = None
        if force_mobile:
            if os.path.exists("mobile.mp4"):
                video_path = "mobile.mp4"
        else:
            if os.path.exists("airplane.mp4"):
                video_path = "airplane.mp4"
            elif os.path.exists("mobile.mp4"):
                video_path = "mobile.mp4"

        if video_path:
            with open(video_path, "rb") as vf:
                video_bytes = vf.read()
                st.video(video_bytes)
                # ngắn ngủi, tránh block quá lâu
                time.sleep(1.2)
        # đánh dấu đã show (hoặc đã cố show)
        st.session_state["video_shown"] = True
    except Exception as e:
        # không để crash app - chỉ log lỗi và tiếp tục
        st.error(f"Lỗi phát video (bị ẩn): {e}")

# --- TIÊU ĐỀ ---
st.markdown('<div id="main-animated-title-container"><h1>TỔ BẢO DƯỠNG SỐ 1</h1></div>', unsafe_allow_html=True)
st.markdown('<div id="sub-static-title"><h2>🔎 TRA CỨU PART NUMBER</h2></div>', unsafe_allow_html=True)
st.markdown("---")

# --- TRA CỨU ---
excel_file = "A787.xlsx"
REQUIRED_COLS = ["A/C", "DESCRIPTION", "ITEM"] # Các cột cần cho Selectbox

if not os.path.exists(excel_file):
    st.error("❌ Không tìm thấy file A787.xlsx trong thư mục hiện tại.")
else:
    try:
        xls = pd.ExcelFile(excel_file)
        sheet_names = [name for name in xls.sheet_names if not name.startswith("Sheet")]

        selection = {"Zone": None, "A/C": None, "DESCRIPTION": None, "ITEM": None}
        current_df = pd.DataFrame()
        
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        cols = st.columns(4)
        
        with cols[0]:
            zone_options = ["Chọn Zone..."] + sheet_names
            zone_selected = st.selectbox("📂 **Zone**", zone_options)
            if zone_selected != "Chọn Zone...":
                selection["Zone"] = zone_selected
        
        if selection["Zone"]:
            current_df = load_and_clean(excel_file, selection["Zone"])
        else:
            current_df = pd.DataFrame() 

        available_cols = [col for col in REQUIRED_COLS if col in current_df.columns]
        selectbox_count = 1
        
        for i, col_name in enumerate(REQUIRED_COLS):
            if col_name in available_cols:
                selectbox_count += 1
                with cols[i + 1]:
                    if not current_df.empty:
                        options = current_df[col_name].astype(str).str.strip().unique().tolist()
                        options = [opt for opt in options if opt != ""]
                        options.sort()
                    else:
                        options = []
                    
                    label = ""
                    placeholder = ""
                    if col_name == "A/C":
                        label = "✈️ **Loại máy bay**"
                        placeholder = "Chọn Loại máy bay..."
                    elif col_name == "DESCRIPTION":
                        label = "📑 **Mô tả chi tiết**"
                        placeholder = "Chọn Mô tả..."
                    elif col_name == "ITEM":
                        label = "🔢 **Item**"
                        placeholder = "Chọn Item..."
                        
                    select_options = [placeholder] + options
                    selected = st.selectbox(label, select_options)
                    if selected != placeholder:
                        selection[col_name] = selected
                    if selection[col_name]:
                        current_df = current_df[current_df[col_name] == selection[col_name]]

        st.markdown("</div>", unsafe_allow_html=True)
        
        selected_count = sum(1 for key, value in selection.items() if key == "Zone" and value is not None)
        selected_count += sum(1 for col in available_cols if selection[col] is not None)
        is_fully_selected = (selected_count == selectbox_count)
        is_result_available = not current_df.empty and len(current_df) > 0

        if is_fully_selected and is_result_available:
            st.markdown("---")
            st.markdown("<h3 style='text-align:center; color:#2E7D32;'>📋 KẾT QUẢ TRA CỨU</h3>", unsafe_allow_html=True)
            
            df_display = current_df.drop(columns=available_cols, errors="ignore")
            df_display = df_display.dropna(axis=1, how="all")
            df_display = df_display.reset_index(drop=True)

            cols_display = list(df_display.columns)
            if "PART NUMBER" in cols_display:
                idx = cols_display.index("PART NUMBER")
                df_display.insert(idx, "STT", range(1, len(df_display) + 1))
            else:
                df_display.insert(0, "STT", range(1, len(df_display) + 1))

            html_parts = ['<div class="table-container">']
            html_parts.append('<table class="custom-table">')
            html_parts.append('<thead><tr>')
            for col in df_display.columns:
                html_parts.append(f'<th>{str(col)}</th>')
            html_parts.append('</tr></thead>')
            html_parts.append('<tbody>')
            for idx, row in df_display.iterrows():
                html_parts.append('<tr>')
                for val in row:
                    html_parts.append(f'<td>{str(val) if pd.notna(val) else ""}</td>')
                html_parts.append('</tr>')
            html_parts.append('</tbody>')
            html_parts.append('</table>')
            html_parts.append('</div>')
            st.markdown(''.join(html_parts), unsafe_allow_html=True)
        
        elif is_fully_selected and not is_result_available:
             st.markdown("---")
             st.info("⚠️ **Không tìm thấy kết quả** nào phù hợp với tất cả các lựa chọn của bạn.")

    except Exception as e:
        st.error(f"Lỗi khi xử lý dữ liệu: {e}")
