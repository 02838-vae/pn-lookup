import streamlit as st
import pandas as pd
import base64
import os

st.set_page_config(page_title="Tổ Bảo Dưỡng Số 1", layout="wide")

# ================= VIDEO INTRO =================
video_path = "airplane.mp4"

if os.path.exists(video_path):
    with open(video_path, "rb") as f:
        video_bytes = f.read()
    video_base64 = base64.b64encode(video_bytes).decode()

    st.markdown(f"""
    <style>
    html, body, [data-testid="stAppViewContainer"] {{
        margin: 0;
        padding: 0;
        overflow: hidden;
    }}
    #intro {{
        position: fixed;
        inset: 0;
        z-index: 9999;
        background: black;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }}
    video {{
        width: 100vw;
        height: 100vh;
        object-fit: cover;
    }}
    #intro-text {{
        position: absolute;
        bottom: 12vh;
        width: 100%;
        text-align: center;
        font-family: 'Special Elite', cursive;
        font-size: 44px;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 0 0 25px #fff, 0 0 50px #00e6ff;
        opacity: 0;
        animation: fadeIn 3s ease-in-out 1s forwards, fadeOut 3s ease-in-out 5s forwards;
    }}
    @keyframes fadeIn {{
        from {{opacity: 0; transform: translateY(40px) scale(0.95);}}
        to {{opacity: 1; transform: translateY(0) scale(1);}}
    }}
    @keyframes fadeOut {{
        from {{opacity: 1;}}
        to {{opacity: 0; transform: translateY(-40px) scale(1.05);}}
    }}
    @keyframes hideIntro {{
        from {{opacity: 1;}}
        to {{opacity: 0; visibility: hidden;}}
    }}
    </style>

    <div id="intro">
        <video id="introVideo" autoplay muted playsinline>
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>
        <div id="intro-text">KHÁM PHÁ BẦU TRỜI CÙNG CHÚNG TÔI</div>
    </div>

    <script>
    const video = document.getElementById('introVideo');
    const intro = document.getElementById('intro');
    function hideIntro() {{
        intro.style.animation = "hideIntro 2s ease forwards";
        setTimeout(() => {{
            intro.remove();
            const app = document.querySelector('.stApp');
            app.style.visibility = 'visible';
            app.style.opacity = '0';
            app.style.transition = 'opacity 2s ease';
            setTimeout(() => app.style.opacity = '1', 100);
        }}, 1800);
    }}
    video.addEventListener('ended', hideIntro);
    setTimeout(hideIntro, 9000);
    </script>
    """, unsafe_allow_html=True)

    # Ẩn phần app chính trong lúc intro chạy
    st.markdown("<style>.stApp {visibility:hidden;}</style>", unsafe_allow_html=True)

# ================= CHƯƠNG TRÌNH CHÍNH =================

# --- Hàm hỗ trợ ---
def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

def load_and_clean(sheet, excel):
    df = pd.read_excel(excel, sheet_name=sheet)
    df.columns = df.columns.str.strip().str.upper()
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("").astype(str).str.strip()
    return df

# --- Ảnh nền ---
bg_img = get_base64("airplane.jpg") if os.path.exists("airplane.jpg") else ""

# --- CSS vintage chỉ áp dụng sau intro ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

.stApp {{
    font-family: 'Special Elite', cursive !important;
    background:
        linear-gradient(rgba(245,242,230,0.9), rgba(245,242,230,0.9)),
        url("data:image/jpeg;base64,{bg_img}") no-repeat center center fixed;
    background-size: cover;
}}
.stApp::after {{
    content: "";
    position: fixed;
    inset: 0;
    background: url("https://www.transparenttextures.com/patterns/aged-paper.png");
    opacity: 0.35;
    pointer-events: none;
    z-index: -1;
}}
header[data-testid="stHeader"] {{display:none;}}
.block-container {{padding-top:0rem !important;}}

.top-title {{
    font-size: 34px;
    font-weight: bold;
    text-align: center;
    color: #3e2723;
    margin-top: 15px;
    text-shadow: 1px 1px 0px #fff;
}}
.main-title {{
    font-size: 26px;
    font-weight: 900;
    text-align: center;
    color: #5d4037;
    margin-bottom: 20px;
    text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
}}

/* Bảng vintage */
table.dataframe {{
    width: 100%;
    border-collapse: collapse;
    border: 2px solid #5d4037;
    background: #fbf7ed;
    color: #3e2723 !important;
    text-align: center;
    font-size: 15px;
    animation: fadeIn 1s ease;
}}
@keyframes fadeIn {{
    from {{opacity: 0; transform: scale(0.97);}}
    to {{opacity: 1; transform: scale(1);}}
}}
table.dataframe thead th {{
    background: linear-gradient(180deg, #8d6e63, #5d4037);
    color: #fff8e1 !important;
    font-weight: bold;
    padding: 10px !important;
    border: 1.5px solid #3e2723 !important;
}}
table.dataframe tbody td {{
    border: 1px dashed #6d4c41 !important;
    padding: 8px !important;
}}
table.dataframe tbody tr:nth-child(even) td {{background: #f3e9d2 !important;}}
table.dataframe tbody tr:hover td {{
    background: #f1d9b5 !important;
    transition: all 0.3s ease-in-out;
}}
</style>
""", unsafe_allow_html=True)

# --- Giao diện chính ---
excel = "A787.xlsx"
if not os.path.exists(excel):
    st.error("⚠️ Không tìm thấy file A787.xlsx.")
else:
    xls = pd.ExcelFile(excel)
    st.markdown('<div class="top-title">📜 Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">🔎 Tra cứu Part number</div>', unsafe_allow_html=True)

    zone = st.selectbox("📂 Zone", xls.sheet_names)
    if zone:
        df = load_and_clean(zone, excel)
        if "A/C" in df.columns:
            acs = sorted([a for a in df["A/C"].dropna().unique()])
            ac = st.selectbox("✈️ Loại máy bay", acs)
            df = df[df["A/C"] == ac]
        if "DESCRIPTION" in df.columns:
            descs = sorted([d for d in df["DESCRIPTION"].dropna().unique()])
            desc = st.selectbox("📑 Phần mô tả", descs)
            df = df[df["DESCRIPTION"] == desc]
        if not df.empty:
            if "ITEM" in df.columns:
                items = sorted([i for i in df["ITEM"].dropna().unique()])
                if len(items) > 1:
                    item = st.selectbox("🔢 Item", items)
                    df = df[df["ITEM"] == item]
            df.insert(0, "STT", range(1, len(df)+1))
            st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.warning("📌 Không tìm thấy dữ liệu phù hợp.")
