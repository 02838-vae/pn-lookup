import streamlit as st
import pandas as pd
import base64
import time

# ====== HÀM CHUYỂN FILE SANG BASE64 ======
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ====== LOAD DỮ LIỆU EXCEL ======
excel_file = "A787.xlsx"
xls = pd.ExcelFile(excel_file)

def load_and_clean(sheet):
    df = pd.read_excel(excel_file, sheet_name=sheet)
    df.columns = df.columns.str.strip().str.upper()
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("").astype(str).str.strip()
    return df


# ======================================================
# 🎬 VIDEO INTRO FULLSCREEN + HIỆU ỨNG CHỮ NHƯ KHÓI TAN
# ======================================================
if "intro_done" not in st.session_state:
    st.session_state.intro_done = False

if not st.session_state.intro_done:
    try:
        video_base64 = get_base64_of_bin_file("airplane.mp4")

        st.markdown(f"""
        <style>
        /* Ẩn giao diện Streamlit */
        [data-testid="stAppViewContainer"], [data-testid="stHeader"],
        [data-testid="stToolbar"], [data-testid="stSidebar"], .block-container {{
            padding: 0 !important;
            margin: 0 !important;
        }}
        header[data-testid="stHeader"], footer, div[data-testid="stDecoration"] {{
            display: none !important;
        }}
        html, body {{
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            height: 100vh !important;
            background: black !important;
        }}

        /* --- VIDEO FULLSCREEN --- */
        #intro-video {{
            position: fixed;
            top: 0; left: 0;
            width: 100vw;
            height: 100vh;
            object-fit: cover;
            z-index: 9999;
            animation: fadeOut 2s ease-in-out forwards;
            animation-delay: 8s;
        }}

        /* --- DÒNG CHỮ TRUNG TÂM DƯỚI MÁY BAY --- */
        #intro-text {{
            position: fixed;
            bottom: 12%;
            width: 100%;
            text-align: center;
            font-family: 'Cinzel', serif;
            font-size: 42px;
            font-weight: bold;
            letter-spacing: 3px;
            color: #fff;
            text-shadow: 0px 0px 15px rgba(255,255,255,0.6);
            opacity: 0;
            z-index: 10000;
            animation: fadeSmoke 7s ease-in-out forwards;
            animation-delay: 1s;
        }}

        /* Hiệu ứng hiện dần rồi tan như khói */
        @keyframes fadeSmoke {{
            0% {{
                opacity: 0;
                filter: blur(10px);
                transform: translateY(40px);
            }}
            30% {{
                opacity: 1;
                filter: blur(0px);
                transform: translateY(0);
            }}
            70% {{
                opacity: 1;
                filter: blur(1px);
            }}
            100% {{
                opacity: 0;
                filter: blur(20px);
                transform: translateY(-30px);
            }}
        }}

        /* Video fade out */
        @keyframes fadeOut {{
            0% {{opacity: 1;}}
            85% {{opacity: 1;}}
            100% {{opacity: 0; visibility: hidden;}}
        }}
        </style>

        <video id="intro-video" autoplay muted playsinline>
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>

        <div id="intro-text">KHÁM PHÁ THẾ GIỚI CÙNG CHÚNG TÔI</div>
        """, unsafe_allow_html=True)

        # Chờ cho video + animation chạy xong
        time.sleep(9)
        st.session_state.intro_done = True
        st.rerun()

    except Exception as e:
        st.error(f"Lỗi phát video: {e}")

# ======================================================
# 🌿 GIAO DIỆN CHÍNH (GIỮ NGUYÊN PHONG CÁCH VINTAGE)
# ======================================================
else:
    img_base64 = get_base64_of_bin_file("airplane.jpg")

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

    .stApp {{
        font-family: 'Special Elite', cursive !important;
        background:
            linear-gradient(rgba(245, 242, 230, 0.85), rgba(245, 242, 230, 0.85)),
            url("data:image/jpeg;base64,{img_base64}") no-repeat center center fixed;
        background-size: cover;
    }}
    .stApp::after {{
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: url("https://www.transparenttextures.com/patterns/aged-paper.png");
        opacity: 0.35;
        pointer-events: none;
        z-index: -1;
    }}
    header[data-testid="stHeader"] {{ display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    </style>
    """, unsafe_allow_html=True)

    # ======= NỘI DUNG CHÍNH =======
    st.markdown('<div class="top-title">📜 Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">🔎 Tra cứu Part number</div>', unsafe_allow_html=True)

    zone = st.selectbox("📂 Chọn zone:", xls.sheet_names)
    if zone:
        df = load_and_clean(zone)
        st.dataframe(df.head(5))
