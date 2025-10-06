import streamlit as st
import pandas as pd
import base64
import os

# ============ VIDEO INTRO ============

st.set_page_config(page_title="Tổ Bảo Dưỡng Số 1", layout="wide")

video_file = "airplane.mp4"

if os.path.exists(video_file):
    with open(video_file, "rb") as f:
        video_bytes = f.read()
    video_base64 = base64.b64encode(video_bytes).decode()

    st.markdown(f"""
    <style>
    html, body, [data-testid="stAppViewContainer"] {{
        margin: 0;
        padding: 0;
        overflow: hidden;
    }}
    #video-wrapper {{
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        background: black;
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
    }}
    #intro-video {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}
    #intro-text {{
        position: absolute;
        bottom: 12vh;
        width: 100%;
        text-align: center;
        font-family: 'Special Elite', cursive;
        font-size: 42px;
        font-weight: bold;
        color: #fff;
        text-shadow: 0 0 20px #fff, 0 0 40px #0ff;
        opacity: 0;
        animation: fadeInText 3s ease-in-out 1s forwards, fadeOutText 3s ease-in-out 5s forwards;
    }}
    @keyframes fadeInText {{
        from {{ opacity: 0; transform: translateY(20px) scale(0.95); filter: blur(8px); }}
        to {{ opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }}
    }}
    @keyframes fadeOutText {{
        from {{ opacity: 1; filter: blur(0); }}
        to {{ opacity: 0; transform: translateY(-20px) scale(1.05); filter: blur(10px); }}
    }}
    @keyframes fadeOut {{
        from {{ opacity: 1; }}
        to {{ opacity: 0; visibility: hidden; }}
    }}
    </style>

    <div id="video-wrapper">
        <video id="intro-video" autoplay muted playsinline>
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            Video không được hỗ trợ.
        </video>
        <div id="intro-text">KHÁM PHÁ THẾ GIỚI CÙNG CHÚNG TÔI</div>
    </div>

    <script>
    const wrapper = document.getElementById('video-wrapper');
    const video = document.getElementById('intro-video');

    function endIntro() {{
        wrapper.style.animation = 'fadeOut 2s ease forwards';
        setTimeout(() => {{
            wrapper.remove();
            const app = document.querySelector('.stApp');
            if (app) {{
                app.style.visibility = 'visible';
                app.style.opacity = '0';
                app.style.transition = 'opacity 2s ease';
                setTimeout(() => app.style.opacity = '1', 100);
            }}
        }}, 1800);
    }}

    video.addEventListener('ended', endIntro);
    setTimeout(endIntro, 10000);
    </script>
    """, unsafe_allow_html=True)

    st.markdown("<style>.stApp {visibility: hidden;}</style>", unsafe_allow_html=True)

# ============ MAIN PAGE (VINTAGE) ============

def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

if os.path.exists("airplane.jpg"):
    bg_img = get_base64("airplane.jpg")
else:
    bg_img = ""

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
header[data-testid="stHeader"] {{ display: none; }}

h1, h2, h3, label {{
    color: #3e2723 !important;
    text-shadow: 1px 1px 0 #fff;
}}

table.dataframe {{
    width: 100%;
    border-collapse: collapse;
    background: #fbf7ed;
    color: #3e2723 !important;
    border: 2px solid #5d4037;
    animation: fadeIn 1s ease;
}}
@keyframes fadeIn {{
    from {{opacity: 0; transform: scale(0.97);}}
    to {{opacity: 1; transform: scale(1);}}
}}
table.dataframe th {{
    background: #5d4037;
    color: #fff8e1 !important;
    padding: 8px;
    border: 1px solid #3e2723;
}}
table.dataframe td {{
    border: 1px dashed #6d4c41;
    padding: 6px;
}}
table.dataframe tr:nth-child(even) td {{ background: #f3e9d2; }}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>📜 TỔ BẢO DƯỠNG SỐ 1</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>🔍 Tra cứu Part Number</h3>", unsafe_allow_html=True)

# ============ LOAD FILE EXCEL ============
excel_file = "A787.xlsx"
if not os.path.exists(excel_file):
    st.error("❌ Không tìm thấy file A787.xlsx trong thư mục.")
else:
    xls = pd.ExcelFile(excel_file)

    def clean(df):
        df.columns = df.columns.str.strip().str.upper()
        for c in df.columns:
            if df[c].dtype == "object":
                df[c] = df[c].fillna("").astype(str).str.strip()
        return df

    zone = st.selectbox("📂 Chọn Zone", xls.sheet_names)
    if zone:
        df = clean(pd.read_excel(xls, sheet_name=zone))

        if "A/C" in df.columns:
            acs = sorted(df["A/C"].dropna().unique())
            ac = st.selectbox("✈️ Chọn Loại Máy Bay", acs)
            df = df[df["A/C"] == ac]

        if "DESCRIPTION" in df.columns:
            descs = sorted(df["DESCRIPTION"].dropna().unique())
            desc = st.selectbox("📄 Mục Tra Cứu", descs)
            df = df[df["DESCRIPTION"] == desc]

        if not df.empty:
            df = df.reset_index(drop=True)
            if "ITEM" in df.columns:
                items = df["ITEM"].dropna().unique()
                if len(items) > 1:
                    item = st.selectbox("🔢 Item", items)
                    df = df[df["ITEM"] == item]
            df.insert(0, "STT", range(1, len(df) + 1))
            st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
