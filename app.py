import streamlit as st
import pandas as pd
import base64
import os
import time

st.set_page_config(page_title="Tổ Bảo Dưỡng Số 1", layout="wide")

# ===== HÀM PHỤ TRỢ =====
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ===== TRẠNG THÁI =====
if "show_main" not in st.session_state:
    st.session_state.show_main = False
if "video_played" not in st.session_state:
    st.session_state.video_played = False

video_file = "airplane.mp4"

# ===== MÀN HÌNH VIDEO INTRO (FULL SCREEN) =====
if not st.session_state.show_main:
    if os.path.exists(video_file):
        video_data = get_base64(video_file)

        st.markdown(f"""
        <style>
        html, body, [data-testid="stAppViewContainer"] {{
            margin: 0; padding: 0;
            background: black;
            overflow: hidden;
        }}
        .video-bg {{
            position: fixed;
            inset: 0;
            width: 100vw;
            height: 100vh;
            object-fit: cover;
            z-index: 9998;
        }}
        .intro-text {{
            position: absolute;
            bottom: 12vh;
            width: 100%;
            text-align: center;
            font-family: 'Special Elite', cursive;
            font-size: 44px;
            font-weight: bold;
            color: #ffffff;
            text-shadow:
                0 0 20px rgba(255,255,255,0.8),
                0 0 40px rgba(180,220,255,0.6),
                0 0 60px rgba(255,255,255,0.4);
            opacity: 0;
            animation:
                appear 3s ease-in forwards,
                floatFade 3s ease-in 5s forwards;
            z-index: 9999;
        }}
        @keyframes appear {{
            0% {{ opacity: 0; filter: blur(8px); transform: translateY(40px); }}
            100% {{ opacity: 1; filter: blur(0); transform: translateY(0); }}
        }}
        @keyframes floatFade {{
            0% {{ opacity: 1; filter: blur(0); transform: translateY(0); }}
            100% {{ opacity: 0; filter: blur(12px); transform: translateY(-30px) scale(1.05); }}
        }}
        </style>

        <div style="position:fixed; inset:0; background:black; display:flex; justify-content:center; align-items:center; z-index:9999;">
            <video class="video-bg" autoplay muted playsinline>
                <source src="data:video/mp4;base64,{video_data}" type="video/mp4">
            </video>
            <div class="intro-text">KHÁM PHÁ THẾ GIỚI CÙNG CHÚNG TÔI</div>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.video_played:
            st.session_state.video_played = True
            time.sleep(8.5)
            st.session_state.show_main = True
            st.rerun()
        st.stop()
    else:
        st.error("❌ Không tìm thấy file airplane.mp4")
        st.stop()

# ===== TRANG CHÍNH =====
excel_file = "A787.xlsx"
if not os.path.exists(excel_file):
    st.error("❌ Không tìm thấy file A787.xlsx")
    st.stop()

xls = pd.ExcelFile(excel_file)

def load_and_clean(sheet):
    df = pd.read_excel(excel_file, sheet_name=sheet)
    df.columns = df.columns.str.strip().str.upper()
    df = df.replace(r'^\s*$', pd.NA, regex=True).dropna(how="all")
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("").astype(str).str.strip()
    return df

img_base64 = get_base64("airplane.jpg") if os.path.exists("airplane.jpg") else ""

# ===== CSS PHONG CÁCH VINTAGE + PARALLAX + FONT TO =====
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

.stApp {{
    font-family: 'Special Elite', cursive !important;
    background:
        linear-gradient(rgba(245, 242, 230, 0.45), rgba(245, 242, 230, 0.45)),
        url("data:image/jpeg;base64,{img_base64}") no-repeat center center fixed;
    background-size: cover;
    background-attachment: fixed; /* Parallax effect */
}}
.stApp::after {{
    content: "";
    position: fixed;
    inset: 0;
    background: url("https://www.transparenttextures.com/patterns/aged-paper.png");
    opacity: 0.18;
    pointer-events: none;
    z-index: -1;
}}

header[data-testid="stHeader"] {{ display: none; }}
.block-container {{ padding-top: 0 !important; }}

/* ===== TIÊU ĐỀ ===== */
.main-title {{
    font-size: 50px;
    font-weight: bold;
    text-align: center;
    color: #3e2723;
    margin-top: 25px;
    transition: transform 0.3s ease;
    text-shadow: 2px 2px 0 #fff, 0 0 25px #f0d49b, 0 0 50px #bca27a;
}}
.main-title:hover {{
    transform: scale(1.05);
}}

.sub-title {{
    font-size: 36px;
    text-align: center;
    color: #6d4c41;
    margin-top: 5px;
    margin-bottom: 25px;
    letter-spacing: 1px;
    animation: glowTitle 3s ease-in-out infinite alternate;
    transition: transform 0.3s ease;
}}
.sub-title:hover {{
    transform: scale(1.05);
}}

@keyframes glowTitle {{
    from {{ text-shadow: 0 0 10px #bfa67a, 0 0 20px #d2b48c, 0 0 30px #e6d5a8; color: #4e342e; }}
    to {{ text-shadow: 0 0 20px #f8e1b4, 0 0 40px #e0b97d, 0 0 60px #f7e7ce; color: #5d4037; }}
}}

/* ===== FORM ===== */
.stSelectbox label {{
    font-weight: bold !important;
    font-size: 22px !important;
    color: #4e342e !important;
}}

.stSelectbox div[data-baseweb="select"] {{
    font-size: 18px !important;
    color: #3e2723 !important;
    background: #fdfbf5 !important;
    border: 2px dashed #5d4037 !important;
    border-radius: 8px !important;
    min-height: 52px !important;
    transition: transform 0.25s ease, box-shadow 0.3s ease;
}}
.stSelectbox div[data-baseweb="select"]:hover {{
    transform: scale(1.03);
    box-shadow: 0 0 15px rgba(93, 64, 55, 0.3);
}}

.stSelectbox span {{
    font-size: 18px !important;
}}

/* ===== BẢNG KẾT QUẢ ===== */
table.dataframe {{
    width: 100%;
    border-collapse: collapse;
    background: rgba(255,255,255,0.9);
    backdrop-filter: blur(3px);
    font-size: 18px;
}}

table.dataframe thead th {{
    background: #6d4c41;
    color: #fff8e1;
    padding: 14px;
    border: 2px solid #3e2723;
    font-size: 19px;
    text-align: center;
}}

table.dataframe tbody td {{
    border: 1.8px solid #5d4037;
    padding: 12px;
    font-size: 18px;
    color: #3e2723;
    text-align: center;
}}

table.dataframe tbody tr:nth-child(even) td {{
    background: rgba(248, 244, 236, 0.85);
}}

table.dataframe tbody tr:hover td {{
    background: rgba(241, 224, 198, 0.9);
    transition: 0.3s;
}}

.highlight-msg {{
    font-size: 20px;
    font-weight: bold;
    color: #3e2723;
    background: rgba(239, 235, 233, 0.9);
    padding: 12px 18px;
    border-left: 6px solid #6d4c41;
    border-radius: 8px;
    margin: 18px 0;
    text-align: center;
}}
</style>
""", unsafe_allow_html=True)

# ===== TIÊU ĐỀ =====
st.markdown('<div class="main-title">📜 TỔ BẢO DƯỠNG SỐ 1</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">🔎 TRA CỨU PART NUMBER</div>', unsafe_allow_html=True)

# ===== NHẠC NỀN =====
try:
    with open("background.mp3", "rb") as f:
        audio_bytes = f.read()
        st.markdown("""
        <div style='text-align:center; margin-top:5px;'>
            <p style='font-family:Special Elite; color:#3e2723; font-size:17px;'>
                🎵 Nhạc nền (hãy nhấn Play để thưởng thức)
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
except FileNotFoundError:
    st.warning("⚠️ Không tìm thấy file background.mp3 — vui lòng thêm file vào cùng thư mục.")

# ===== NỘI DUNG CHÍNH =====
zone = st.selectbox("📂 Bạn muốn tra cứu zone nào?", xls.sheet_names)
if zone:
    df = load_and_clean(zone)

    if "A/C" in df.columns:
        aircrafts = sorted([ac for ac in df["A/C"].dropna().unique().tolist() if ac])
        aircraft = st.selectbox("✈️ Loại máy bay?", aircrafts)
    else:
        aircraft = None

    if aircraft:
        df_ac = df[df["A/C"] == aircraft]

        if "DESCRIPTION" in df_ac.columns:
            desc_list = sorted([d for d in df_ac["DESCRIPTION"].dropna().unique().tolist() if d])
            description = st.selectbox("📑 Bạn muốn tra cứu phần nào?", desc_list)
        else:
            description = None

        if description:
            df_desc = df_ac[df_ac["DESCRIPTION"] == description]

            if "ITEM" in df_desc.columns:
                items = sorted([i for i in df_desc["ITEM"].dropna().unique().tolist() if i])
                item = st.selectbox("🔢 Bạn muốn tra cứu Item nào?", items)
                df_desc = df_desc[df_desc["ITEM"] == item]

            df_desc = df_desc.drop(columns=["A/C", "ITEM", "DESCRIPTION"], errors="ignore")
            df_desc = df_desc.replace(r'^\s*$', pd.NA, regex=True).dropna(how="all")

            if not df_desc.empty:
                df_desc.insert(0, "STT", range(1, len(df_desc) + 1))
                st.markdown(f'<div class="highlight-msg">✅ Tìm thấy {len(df_desc)} dòng dữ liệu</div>', unsafe_allow_html=True)
                st.write(df_desc.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.warning("📌 Không có dữ liệu phù hợp.")
