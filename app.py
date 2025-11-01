import streamlit as st
import pandas as pd
import base64
import os

# ======== HÀM ĐỌC ẢNH NỀN ========
def load_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# ======== ẢNH NỀN PC & MOBILE ========
bg_pc_path = "PN_PC.jpg"
bg_mobile_path = "PN_mobile.jpg"

bg_pc_base64 = load_image_base64(bg_pc_path) if os.path.exists(bg_pc_path) else ""
bg_mobile_base64 = load_image_base64(bg_mobile_path) if os.path.exists(bg_mobile_path) else ""

# ======== TIÊU ĐỀ CHẠY & CSS ========
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');

#MainMenu, footer, header {{visibility: hidden;}}
div.block-container {{padding-top: 0; background-color: transparent !important;}}

/* === NỀN PC === */
.stAppViewContainer, .st-emotion-cache-1r6slb0 {{
    background: url("data:image/jpeg;base64,{bg_pc_base64}") no-repeat center top fixed !important;
    background-size: cover !important;
    font-family: 'Oswald', sans-serif !important;
}}

/* === HIỆU ỨNG CHẠY === */
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
    height: 100px;
    overflow: hidden;
    text-align: center;
    margin-top: 25px;
}}
#main-animated-title-container h1 {{
    font-family: 'Oswald', sans-serif;
    font-size: 3.5rem;
    font-weight: 700;
    letter-spacing: 5px;
    text-transform: uppercase;
    white-space: nowrap;
    display: inline-block;
    background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3);
    background-size: 400% 400%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: colorShift 10s ease infinite, scrollText 16s linear infinite;
    text-shadow: 2px 2px 6px rgba(0,0,0,0.7);
}}

/* === TIÊU ĐỀ PHỤ (PC) === */
#sub-static-title h2 {{
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    color: #FFD54F;
    text-align: center;
    text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
    margin-top: 25px;
    margin-bottom: 20px;
}}

/* === DROPDOWN LABEL === */
h3.dropdown-label {{
    color: #FFD700;
    text-align: center;
    font-size: 2.2rem;
    font-weight: 800;
    text-shadow: 2px 2px 6px rgba(0,0,0,0.7);
    letter-spacing: 0.5px;
    margin-bottom: 0.5rem;
}}

/* === MOBILE === */
@media (max-width: 768px) {{
    .stAppViewContainer, .st-emotion-cache-1r6slb0 {{
        background: url("data:image/jpeg;base64,{bg_mobile_base64}") no-repeat center top scroll !important;
        background-size: cover !important;
    }}

    #main-animated-title-container h1 {{
        font-size: 7vw;
        letter-spacing: 2px;
        animation: colorShift 10s ease infinite, scrollText 14s linear infinite;
        text-shadow: 2px 2px 7px rgba(0,0,0,0.8);
    }}

    #sub-static-title h2 {{
        font-size: 4.2vw;
        margin-top: 10px;
    }}

    h3.dropdown-label {{
        font-size: 4.5vw;
        line-height: 1.2;
        margin-bottom: 0.4rem;
    }}
}}

/* === BẢNG === */
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
.custom-table tr:nth-child(even) {{ background-color: #f9f9f9; }}
.custom-table tr:hover {{ background-color: #e0e0e0; }}
</style>
""", unsafe_allow_html=True)

# ======== TIÊU ĐỀ CHẠY + PHỤ ========
st.markdown("""
<div id="main-animated-title-container">
  <h1>✈️ TỔ BẢO DƯỠNG SỐ 1 ✈️</h1>
</div>
<div id="sub-static-title">
  <h2>🔍 TRA CỨU PART NUMBER</h2>
</div>
""", unsafe_allow_html=True)

# ======== HÀM XỬ LÝ EXCEL ========
def load_and_clean(file_path, sheet_name):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    df = df.dropna(how="all")
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    return df

# ======== TRA CỨU ========
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
            st.markdown("<h3 class='dropdown-label'>📂 Zone</h3>", unsafe_allow_html=True)
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
                    st.markdown(f"<h3 class='dropdown-label'>{col_labels[col_name]}</h3>", unsafe_allow_html=True)

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

        # --- KẾT QUẢ ---
        if selection["Zone"] and all(selection.get(col) for col in available_cols) and not current_df.empty:
            st.markdown("---")
            st.markdown("<h3 style='text-align:center; color:#2E7D32;'>📋 KẾT QUẢ TRA CỨU</h3>", unsafe_allow_html=True)
            
            df_display = current_df.drop(columns=available_cols, errors="ignore")
            df_display = df_display.dropna(axis=1, how="all")
            df_display = df_display.reset_index(drop=True)
            df_display.insert(0, "STT", range(1, len(df_display) + 1))

            st.dataframe(df_display, use_container_width=True)
        elif selection["Zone"] and all(selection.get(col) for col in available_cols) and current_df.empty:
            st.markdown("---")
            st.info("⚠️ Không tìm thấy kết quả nào phù hợp với lựa chọn của bạn.")
    except Exception as e:
        st.error(f"Lỗi khi xử lý dữ liệu: {e}")

