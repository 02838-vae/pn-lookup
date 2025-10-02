import pandas as pd
import streamlit as st
import base64
import glob
import os

# ===== Đọc file Excel =====
excel_file = "A787.xlsx"
xls = pd.ExcelFile(excel_file)

def load_and_clean(sheet):
    df = pd.read_excel(excel_file, sheet_name=sheet)
    df.columns = df.columns.str.strip().str.upper()
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("").astype(str).str.strip()
    return df

# ===== Load nhiều ảnh background =====
def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Tìm tất cả file airplane*
bg_files = sorted(
    glob.glob("airplane*.jpg") +
    glob.glob("airplane*.jpeg") +
    glob.glob("airplane*.png")
)

# Nếu không có → fallback 1 ảnh mặc định
if not bg_files and os.path.exists("airplane.jpg"):
    bg_files = ["airplane.jpg"]

bg64 = [get_base64(f) for f in bg_files]

# Nếu có nhiều ảnh → tạo keyframes slideshow
keyframes = ""
if len(bg64) > 1:
    step = 100 // len(bg64)
    for i, img in enumerate(bg64):
        pct1 = i * step
        pct2 = (i + 1) * step
        keyframes += f"""
        {pct1}% {{ background-image: url("data:image/jpeg;base64,{img}"); opacity: 0; }}
        {pct1+5}% {{ background-image: url("data:image/jpeg;base64,{img}"); opacity: 1; }}
        {pct2-5}% {{ background-image: url("data:image/jpeg;base64,{img}"); opacity: 1; }}
        {pct2}% {{ background-image: url("data:image/jpeg;base64,{img}"); opacity: 0; }}
        """
else:
    # Nếu chỉ có 1 ảnh → giữ nguyên
    keyframes = f"""
    0% {{ background-image: url("data:image/jpeg;base64,{bg64[0]}"); opacity:1; }}
    100% {{ background-image: url("data:image/jpeg;base64,{bg64[0]}"); opacity:1; }}
    """

# ===== CSS =====
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

    /* Background slideshow */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        animation: bgslide {len(bg64)*10 if len(bg64)>1 else 60}s infinite;
        z-index: -2;
    }}

    @keyframes bgslide {{
        {keyframes}
    }}

    /* Overlay làm mờ */
    .stApp::after {{
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(255,255,255,0.7);
        z-index: -1;
    }}

    /* Font vintage */
    .stApp {{
        font-family: 'Special Elite', cursive !important;
    }}

    /* Dòng chữ Tổ bảo dưỡng số 1 */
    .top-title {{
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        animation: colorchange 5s infinite alternate;
        margin: 15px auto;
    }}
    @keyframes colorchange {{
        0% {{color: #e74c3c;}}
        25% {{color: #3498db;}}
        50% {{color: #2ecc71;}}
        75% {{color: #f1c40f;}}
        100% {{color: #9b59b6;}}
    }}

    /* Tiêu đề chính */
    .main-title {{
        font-size: 28px;
        font-weight: 900;
        text-align: center;
        color: #2c3e50;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }}

    /* Label câu hỏi */
    .stSelectbox label {{
        font-weight: 900 !important;
        font-size: 18px !important;
        color: #000 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ===== Header =====
st.markdown('<div class="top-title">Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🔎 Tra cứu Part number</div>', unsafe_allow_html=True)

# ===== Dropdown Zone =====
zone = st.selectbox("📂 Bạn muốn tra cứu zone nào?", xls.sheet_names, key="zone")
if zone:
    df = load_and_clean(zone)

    if "A/C" in df.columns:
        aircrafts = sorted([ac for ac in df["A/C"].dropna().unique().tolist() if ac and ac.upper() != "NAN"])
        aircraft = st.selectbox("✈️ Loại máy bay?", aircrafts, key="aircraft")
    else:
        aircraft = None

    if aircraft:
        df_ac = df[df["A/C"] == aircraft]

        if "DESCRIPTION" in df_ac.columns:
            desc_list = sorted([d for d in df_ac["DESCRIPTION"].dropna().unique().tolist() if d and d.upper() != "NAN"])
            description = st.selectbox("📑 Bạn muốn tra cứu phần nào?", desc_list, key="desc")
        else:
            description = None

        if description:
            df_desc = df_ac[df_ac["DESCRIPTION"] == description]

            if "ITEM" in df_desc.columns:
                items = sorted([i for i in df_desc["ITEM"].dropna().unique().tolist() if i and i.upper() != "NAN"])
                if items:
                    item = st.selectbox("🔢 Bạn muốn tra cứu Item nào?", items, key="item")
                    df_desc = df_desc[df_desc["ITEM"] == item]

            if not df_desc.empty:
                df_result = df_desc.copy().reset_index(drop=True)
                cols_to_show = ["PART NUMBER (PN)"]
                for alt_col in ["PART INTERCHANGE", "PN INTERCHANGE"]:
                    if alt_col in df_result.columns:
                        cols_to_show.append(alt_col)
                        break
                if "NOTE" in df_result.columns:
                    cols_to_show.append("NOTE")

                df_result = df_result[cols_to_show]
                df_result.insert(0, "STT", range(1, len(df_result) + 1))

                st.success(f"✅ Tìm thấy {len(df_result)} dòng dữ liệu")
                st.dataframe(df_result, use_container_width=True)
            else:
                st.error("Rất tiếc, không tìm thấy dữ liệu phù hợp.")
