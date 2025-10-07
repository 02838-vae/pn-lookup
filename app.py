import streamlit as st
import pandas as pd
import base64
import os

st.set_page_config(page_title="Tổ Bảo Dưỡng Số 1", layout="wide")

# ======= VIDEO INTRO =======
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
    #video-container {{
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
        text-shadow: 0 0 20px #fff, 0 0 40px #0ff;
        opacity: 0;
        animation: fadeIn 3s ease-in-out 1s forwards, fadeOut 3s ease-in-out 5s forwards;
    }}
    @keyframes fadeIn {{
        from {{opacity: 0; transform: translateY(40px) scale(0.95) blur(6px);}}
        to {{opacity: 1; transform: translateY(0) scale(1); blur(0);}}
    }}
    @keyframes fadeOut {{
        from {{opacity: 1;}}
        to {{opacity: 0; transform: translateY(-30px) scale(1.05) blur(6px);}}
    }}
    @keyframes fadeOutContainer {{
        from {{opacity: 1;}}
        to {{opacity: 0; visibility: hidden;}}
    }}
    </style>

    <div id="video-container">
        <video id="intro-video" autoplay muted playsinline>
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            Video không hỗ trợ.
        </video>
        <div id="intro-text">KHÁM PHÁ THẾ GIỚI CÙNG CHÚNG TÔI</div>
    </div>

    <script>
    const video = document.getElementById("intro-video");
    const container = document.getElementById("video-container");

    function endIntro() {{
        container.style.animation = "fadeOutContainer 2s ease forwards";
        setTimeout(() => {{
            container.remove();
            const app = document.querySelector('.stApp');
            if (app) {{
                app.style.visibility = 'visible';
                app.style.opacity = '0';
                app.style.transition = 'opacity 2s ease';
                setTimeout(() => app.style.opacity = '1', 100);
            }}
        }}, 1800);
    }}

    video.addEventListener("ended", endIntro);
    setTimeout(endIntro, 9000);
    </script>
    """, unsafe_allow_html=True)

    st.markdown("<style>.stApp {visibility: hidden;}</style>", unsafe_allow_html=True)

# ======= HÀM HỖ TRỢ =======
def get_base64_of_file(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

def load_and_clean(sheet, excel_file):
    df = pd.read_excel(excel_file, sheet_name=sheet)
    df.columns = df.columns.str.strip().str.upper()
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("").astype(str).str.strip()
    return df

# ======= ẢNH NỀN =======
img_base64 = ""
if os.path.exists("airplane.jpg"):
    img_base64 = get_base64_of_file("airplane.jpg")

# ======= CSS PHONG CÁCH VINTAGE =======
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

.stApp {{
    font-family: 'Special Elite', cursive !important;
    background:
        linear-gradient(rgba(245,242,230,0.9), rgba(245,242,230,0.9)),
        url("data:image/jpeg;base64,{img_base64}") no-repeat center center fixed;
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

/* === Bảng Vintage === */
table.dataframe {{
    width: 100%;
    border-collapse: collapse;
    border: 2px solid #5d4037;
    background: #fbf7ed;
    color: #3e2723 !important;
    font-size: 15px;
    text-align: center;
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

# ======= GIAO DIỆN CHÍNH =======
excel_file = "A787.xlsx"
st.markdown('<div class="top-title">📜 Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🔎 Tra cứu Part number</div>', unsafe_allow_html=True)

if not os.path.exists(excel_file):
    st.error("⚠️ Không tìm thấy file A787.xlsx trong thư mục.")
else:
    xls = pd.ExcelFile(excel_file)
    zone = st.selectbox("📂 Bạn muốn tra cứu zone nào?", xls.sheet_names)
    if zone:
        df = load_and_clean(zone, excel_file)

        if "A/C" in df.columns:
            aircrafts = sorted([ac for ac in df["A/C"].dropna().unique() if ac])
            aircraft = st.selectbox("✈️ Loại máy bay?", aircrafts)
            df = df[df["A/C"] == aircraft]

        if "DESCRIPTION" in df.columns:
            descs = sorted([d for d in df["DESCRIPTION"].dropna().unique() if d])
            desc = st.selectbox("📑 Phần mô tả", descs)
            df = df[df["DESCRIPTION"] == desc]

        if not df.empty:
            if "ITEM" in df.columns:
                items = sorted([i for i in df["ITEM"].dropna().unique() if i])
                if len(items) > 1:
                    item = st.selectbox("🔢 Item", items)
                    df = df[df["ITEM"] == item]

            df.insert(0, "STT", range(1, len(df) + 1))
            st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.warning("📌 Không tìm thấy dữ liệu phù hợp.")
