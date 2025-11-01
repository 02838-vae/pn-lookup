import streamlit as st
import pandas as pd
import time

# ==============================
# 1️⃣ CẤU HÌNH PAGE
# ==============================
st.set_page_config(
    page_title="PN Lookup",
    page_icon="✈️",
    layout="wide",
)

# ==============================
# 2️⃣ CSS GIAO DIỆN
# ==============================
st.markdown(f"""
<style>
/* Nền tổng thể */
[data-testid="stAppViewContainer"] {{
    background: radial-gradient(circle at center, #001a33 0%, #000000 100%);
    color: white !important;
}}

/* Tiêu đề marquee */
.marquee {{
    font-size: 3.5rem;
    font-weight: 900;
    color: #FFEB3B;
    white-space: nowrap;
    overflow: hidden;
    display: block;
    width: 100%;
    text-align: center;
    animation: marquee 25s linear infinite;
}}
@keyframes marquee {{
    0%   {{ transform: translateX(100%); }}
    100% {{ transform: translateX(-100%); }}
}}

/* === SELECTBOX LABEL PHÓNG TO === */
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

/* === CANH GIỮA BẢNG === */
table {{
    width: 100% !important;
    text-align: center !important;
}}
thead th {{
    text-align: center !important;
}}
</style>
""", unsafe_allow_html=True)

# ==============================
# 3️⃣ VIDEO INTRO
# ==============================
import platform
if st.session_state.get("video_shown") != True:
    if "Mobile" in st.user_agent or "Android" in st.user_agent or "iPhone" in st.user_agent:
        video_file = open("mobile.mp4", "rb")
    else:
        video_file = open("airplane.mp4", "rb")
    video_bytes = video_file.read()
    st.video(video_bytes)
    time.sleep(3)
    st.session_state["video_shown"] = True

# ==============================
# 4️⃣ TIÊU ĐỀ CHẠY NGANG
# ==============================
st.markdown('<div class="marquee">TRA CỨU PART NUMBER - HỆ THỐNG PN LOOKUP ✈️</div>', unsafe_allow_html=True)
st.write("")  # khoảng cách

# ==============================
# 5️⃣ KHU VỰC LỌC DỮ LIỆU
# ==============================
col1, col2, col3, col4 = st.columns(4)

with col1:
    zone = st.selectbox("📂 Zone", ["A", "B", "C", "D", "E"])
with col2:
    aircraft = st.selectbox("✈️ Loại máy bay", ["A320", "A321", "A350", "B787"])
with col3:
    desc = st.selectbox("📑 Mô tả chi tiết", ["Wing", "Engine", "Cabin", "Landing Gear"])
with col4:
    item = st.selectbox("🔢 Item", ["001", "002", "003", "004", "005"])

# ==============================
# 6️⃣ BẢNG KẾT QUẢ (ví dụ mẫu)
# ==============================
data = {
    "Zone": [zone],
    "Loại máy bay": [aircraft],
    "Mô tả": [desc],
    "Item": [item],
    "Part Number": ["PN-" + item + "-XYZ"],
    "Tình trạng": ["✅ Có sẵn"]
}

df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)
