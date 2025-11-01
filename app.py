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
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');

#MainMenu, footer, header {{visibility: hidden;}}
div.block-container {{padding-top: 0; background-color: transparent !important;}} 
[data-testid="stVerticalBlock"] > div:first-child {{background-color: transparent !important;}}

/* === NỀN PC === */
.stAppViewContainer {{
    background: url("data:image/jpeg;base64,{bg_pc_base64}") no-repeat center top fixed !important;
    background-size: cover !important;
    font-family: 'Oswald', sans-serif !important;
}}

/* === TIÊU ĐỀ CHÍNH === */
@keyframes scrollText {{
    0% {{ transform: translateX(100vw); }}
    100% {{ transform: translateX(-100%); }}
}}
@keyframes colorShift {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}
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
    .stAppViewContainer {{
        background: url("data:image/jpeg;base64,{bg_mobile_base64}") no-repeat center top scroll !important;
        background-size: cover !important;
    }}
    #main-animated-title-container h1 {{
        font-size: 8vw;
        line-height: 1.1;
        letter-spacing: 3px;
        animation: colorShift 10s ease infinite, scrollText 10s linear infinite;
    }}
    #sub-static-title h2 {{
        font-size: 5vw;
        color: #FFD54F;
        margin-top: 10px;
    }}
}}

/* === LABEL SELECTBOX (ép cực mạnh) === */
div[data-testid="stSelectbox"] label span,
div[data-testid="stSelectbox"] label,
div[data-testid="stWidgetLabel"],
[data-testid="stSelectboxLabel"],
.css-1offfwp.e1fqkh3o4,
.css-16idsys.e16nr0p33,
.css-1pahdxg-control
{{
    font-size: 2.8rem !important;
    font-weight: 900 !important;
    color: #FFEB3B !important;
    text-align: center !important;
    text-shadow: 3px 3px 6px rgba(0,0,0,0.8) !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}}

@media (max-width: 768px) {{
    div[data-testid="stSelectbox"] label span,
    div[data-testid="stSelectbox"] label,
    div[data-testid="stWidgetLabel"] {{
        font-size: 1.8rem !important;
    }}
}}

/* === CANH GIỮA DROPBOX === */
.element-container:has(.stSelectbox) {{
    display: flex;
    justify-content: center;
    background-color: transparent !important; 
}}
[data-testid^="stHorizontalBlock"] {{
    background-color: transparent !important;
}}

/* === BẢNG HTML === */
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
</style>
""", unsafe_allow_html=True)

# --- TIÊU ĐỀ ---
st.markdown('<div id="main-animated-title-container"><h1>TỔ BẢO DƯỠNG SỐ 1</h1></div>', unsafe_allow_html=True)
st.markdown('<div id="sub-static-title"><h2>🔎 TRA CỨU PART NUMBER</h2></div>', unsafe_allow_html=True)
st.markdown("---")

# --- TRA CỨU ---
excel_file = "A787.xlsx"
REQUIRED_COLS = ["A/C", "DESCRIPTION", "ITEM"]

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

            if "PART NUMBER" in df_display.columns:
                idx = df_display.columns.get_loc("PART NUMBER")
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
            for _, row in df_display.iterrows():
                html_parts.append('<tr>')
                for val in row:
                    html_parts.append(f'<td>{str(val) if pd.notna(val) else ""}</td>')
                html_parts.append('</tr>')
            html_parts.append('</tbody></table></div>')
            st.markdown(''.join(html_parts), unsafe_allow_html=True)
        
        elif is_fully_selected and not is_result_available:
            st.markdown("---")
            st.info("⚠️ **Không tìm thấy kết quả** nào phù hợp với tất cả các lựa chọn của bạn.")

    except Exception as e:
        st.error(f"Lỗi khi xử lý dữ liệu: {e}")
