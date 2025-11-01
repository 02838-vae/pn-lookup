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

# --- CSS TOÀN CỤC ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');

#MainMenu, footer, header {{visibility: hidden;}}
div.block-container {{padding-top: 0; background-color: transparent !important;}}

/* === NỀN === */
.stAppViewContainer, .st-emotion-cache-1r6slb0 {{
    background: url("data:image/jpeg;base64,{bg_pc_base64}") no-repeat center top fixed !important;
    background-size: cover !important;
    font-family: 'Oswald', sans-serif !important;
}}

/* === TIÊU ĐỀ CHÍNH === */
#main-animated-title-container {{
    width: 100%;
    height: auto;
    overflow: hidden;
    text-align: center;
    margin-top: 35px;
}}
#main-animated-title-container h1 {{
    font-family: 'Oswald', sans-serif;
    font-size: 4rem; /* nhỏ hơn trước 1 chút */
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

#sub-static-title h2 {{
    font-family: 'Playfair Display', serif;
    font-size: 2.1rem; /* nhỏ hơn trước */
    color: #FFD54F;
    text-align: center;
    text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
    margin-top: 25px;
    margin-bottom: 15px;
}}

/* === MOBILE === */
@media (max-width: 768px) {{
    .stAppViewContainer, .st-emotion-cache-1r6slb0 {{
        background: url("data:image/jpeg;base64,{bg_mobile_base64}") no-repeat center top scroll !important;
        background-size: cover !important;
    }}

    #main-animated-title-container h1 {{
        font-size: 7vw; /* nhỏ lại để vừa 1 dòng */
        letter-spacing: 3px;
        line-height: 1.1;
        white-space: nowrap;
    }}

    #sub-static-title h2 {{
        font-size: 5vw; /* vừa 1 dòng trên mobile */
        margin-top: 10px;
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
        
        # --- 1️⃣ Zone ---
        with cols[0]:
            st.markdown("<h3 style='color:#FFD700; text-align:center; font-size:2.2rem; font-weight:900;'>📂 Zone</h3>", unsafe_allow_html=True)
            zone_options = ["Chọn Zone..."] + sheet_names
            zone_selected = st.selectbox("", zone_options, label_visibility="collapsed")
            if zone_selected != "Chọn Zone...":
                selection["Zone"] = zone_selected

        if selection["Zone"]:
            current_df = load_and_clean(excel_file, selection["Zone"])
        else:
            current_df = pd.DataFrame() 

        available_cols = [col for col in REQUIRED_COLS if col in current_df.columns]

        # --- 2️⃣ Các cột còn lại ---
        col_labels = {
            "A/C": "✈️ Loại máy bay",
            "DESCRIPTION": "📑 Mô tả chi tiết",
            "ITEM": "🔢 Item"
        }

        for i, col_name in enumerate(REQUIRED_COLS):
            if col_name in available_cols:
                with cols[i + 1]:
                    label_html = f"<h3 style='color:#FFD700; text-align:center; font-size:2.2rem; font-weight:900;'>{col_labels[col_name]}</h3>"
                    st.markdown(label_html, unsafe_allow_html=True)

                    if not current_df.empty:
                        options = current_df[col_name].astype(str).str.strip().unique().tolist()
                        options = [opt for opt in options if opt != ""]
                        options.sort()
                    else:
                        options = []

                    placeholder = f"Chọn {col_labels[col_name].split()[-1]}..."
                    select_options = [placeholder] + options
                    selected = st.selectbox("", select_options, label_visibility="collapsed")
                    if selected != placeholder:
                        selection[col_name] = selected
                    if selection[col_name]:
                        current_df = current_df[current_df[col_name] == selection[col_name]]

        st.markdown("</div>", unsafe_allow_html=True)

        # --- HIỂN THỊ KẾT QUẢ ---
        if selection["Zone"] and all(selection.get(col) for col in available_cols) and not current_df.empty:
            st.markdown("---")
            st.markdown("<h3 style='text-align:center; color:#2E7D32;'>📋 KẾT QUẢ TRA CỨU</h3>", unsafe_allow_html=True)
            
            df_display = current_df.drop(columns=available_cols, errors="ignore")
            df_display = df_display.dropna(axis=1, how="all")
            df_display = df_display.reset_index(drop=True)
            df_display.insert(0, "STT", range(1, len(df_display) + 1))

            html_parts = ['<div class="table-container"><table class="custom-table"><thead><tr>']
            for col in df_display.columns:
                html_parts.append(f'<th>{col}</th>')
            html_parts.append('</tr></thead><tbody>')
            for _, row in df_display.iterrows():
                html_parts.append('<tr>' + ''.join(f'<td>{val}</td>' for val in row) + '</tr>')
            html_parts.append('</tbody></table></div>')
            st.markdown(''.join(html_parts), unsafe_allow_html=True)

        elif selection["Zone"] and all(selection.get(col) for col in available_cols) and current_df.empty:
            st.markdown("---")
            st.info("⚠️ Không tìm thấy kết quả nào phù hợp với lựa chọn của bạn.")
    except Exception as e:
        st.error(f"Lỗi khi xử lý dữ liệu: {e}")
