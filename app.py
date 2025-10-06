import streamlit as st
import pandas as pd
import base64
import os

# ========================= CẤU HÌNH CHUNG =========================
st.set_page_config(page_title="Tổ Bảo Dưỡng Số 1", layout="wide")

# ========================= VIDEO INTRO =========================
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
        top: 0; left: 0;
        width: 100vw;
        height: 100vh;
        background: black;
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
    }}
    video {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}
    #intro-text {{
        position: absolute;
        bottom: 13vh;
        width: 100%;
        text-align: center;
        font-family: 'Special Elite', cursive;
        font-size: 42px;
        font-weight: bold;
        color: #fff;
        text-shadow: 0 0 20px #fff, 0 0 40px #0ff;
        opacity: 0;
        animation: fadeIn 3s ease-in-out 1s forwards, fadeOut 3s ease-in-out 5s forwards;
    }}
    @keyframes fadeIn {{
        from {{opacity: 0; transform: translateY(30px) scale(0.95); filter: blur(8px);}}
        to {{opacity: 1; transform: translateY(0) scale(1); filter: blur(0);}}
    }}
    @keyframes fadeOut {{
        from {{opacity: 1;}}
        to {{opacity: 0; transform: translateY(-20px) scale(1.05); filter: blur(8px);}}
    }}
    @keyframes fadeOutContainer {{
        from {{opacity: 1;}}
        to {{opacity: 0; visibility: hidden;}}
    }}
    </style>

    <div id="video-container">
        <video id="intro-video" autoplay muted playsinline>
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            Video không hỗ trợ trên trình duyệt này.
        </video>
        <div id="intro-text">KHÁM PHÁ THẾ GIỚI CÙNG CHÚNG TÔI</div>
    </div>

    <script>
    const container = document.getElementById("video-container");
    const video = document.getElementById("intro-video");
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

# ========================= HÀM TIỆN ÍCH =========================
def load_and_clean(sheet_name, excel_file):
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    df.columns = df.columns.str.strip().str.upper()
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("").astype(str).str.strip()
    return df

def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ========================= GIAO DIỆN CHÍNH (VINTAGE) =========================
excel_file = "A787.xlsx"
if os.path.exists("airplane.jpg"):
    img_base64 = get_base64("airplane.jpg")
else:
    img_base64 = ""

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
header[data-testid="stHeader"] {{display: none;}}

h1,h2,h3,label {{
    color: #3e2723 !important;
    text-shadow: 1px 1px 0px #fff;
}}

table.dataframe {{
    width: 100%;
    border-collapse: collapse;
    background: #fbf7ed;
    color: #3e2723 !important;
    border: 2px solid #5d4037;
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
table.dataframe tbody tr:nth-child(even) td {{ background: #f3e9d2 !important; }}
table.dataframe tbody tr:hover td {{
    background: #f1d9b5 !important;
    transition: all 0.3s ease-in-out;
}}
</style>
""", unsafe_allow_html=True)

# ========================= GIAO DIỆN TRA CỨU =========================
st.markdown("<h1 style='text-align:center;'>📜 TỔ BẢO DƯỠNG SỐ 1</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>🔍 Tra cứu Part Number</h3>", unsafe_allow_html=True)

if not os.path.exists(excel_file):
    st.error("❌ Không tìm thấy file A787.xlsx trong thư mục!")
else:
    xls = pd.ExcelFile(excel_file)
    zone = st.selectbox("📂 Chọn Zone", xls.sheet_names)
    if zone:
        df = load_and_clean(zone, excel_file)
        if "A/C" in df.columns:
            aircrafts = sorted(df["A/C"].dropna().unique())
            aircraft = st.selectbox("✈️ Loại máy bay", aircrafts)
            df = df[df["A/C"] == aircraft]
        if "DESCRIPTION" in df.columns:
            descs = sorted(df["DESCRIPTION"].dropna().unique())
            desc = st.selectbox("📑 Phần mô tả", descs)
            df = df[df["DESCRIPTION"] == desc]
        if not df.empty:
            if "ITEM" in df.columns:
                items = sorted(df["ITEM"].dropna().unique())
                if len(items) > 1:
                    item = st.selectbox("🔢 Item", items)
                    df = df[df["ITEM"] == item]
            df.insert(0, "STT", range(1, len(df)+1))
            st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
