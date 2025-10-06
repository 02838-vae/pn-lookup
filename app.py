import streamlit as st
import pandas as pd
import base64
import os

st.set_page_config(page_title="PN Lookup", layout="wide")

# ========== ĐỌC VIDEO ==========
VIDEO_PATH = "airplane.mp4"

def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

video_base64 = None
if os.path.exists(VIDEO_PATH):
    video_base64 = get_base64(VIDEO_PATH)
else:
    st.warning("⚠️ Không tìm thấy file airplane.mp4 — bỏ qua phần video mở đầu.")

# ========== HTML PHÁT VIDEO ==========
if video_base64:
    st.markdown(
        f"""
        <style>
        html, body, [data-testid="stAppViewContainer"] {{
            margin: 0; padding: 0;
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
            font-size: 40px;
            color: white;
            opacity: 0;
            animation: fadeInText 3s ease-in-out 1s forwards, fadeOutText 3s ease-in-out 8s forwards;
            text-shadow: 0 0 20px rgba(255,255,255,0.8);
        }}
        @keyframes fadeInText {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes fadeOutText {{
            from {{ opacity: 1; }}
            to {{ opacity: 0; filter: blur(5px); transform: translateY(-20px); }}
        }}
        @keyframes fadeOut {{
            from {{ opacity: 1; }}
            to {{ opacity: 0; visibility: hidden; }}
        }}
        </style>

        <div id="video-wrapper">
            <video id="intro-video" autoplay muted playsinline>
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                Trình duyệt của bạn không hỗ trợ video.
            </video>
            <div id="intro-text">KHÁM PHÁ THẾ GIỚI CÙNG CHÚNG TÔI</div>
        </div>

        <script>
        const wrapper = document.getElementById('video-wrapper');
        const video = document.getElementById('intro-video');

        function endIntro() {{
            if (wrapper) {{
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
                }}, 2000);
            }}
        }}

        video.addEventListener('ended', endIntro);
        // Trường hợp video lỗi hoặc không phát tự động trên mobile
        setTimeout(endIntro, 10000);
        </script>
        """,
        unsafe_allow_html=True,
    )

# ========== GIAO DIỆN CHÍNH ==========
# Nếu video đang phát, ẩn trang chính
if video_base64:
    st.markdown("<style>.stApp {visibility: hidden;}</style>", unsafe_allow_html=True)

excel_file = "A787.xlsx"
if not os.path.exists(excel_file):
    st.error("❌ Không tìm thấy file A787.xlsx.")
else:
    # Đọc dữ liệu Excel
    xls = pd.ExcelFile(excel_file)

    def load_and_clean(sheet):
        df = pd.read_excel(excel_file, sheet_name=sheet)
        df.columns = df.columns.str.strip().str.upper()
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].fillna("").astype(str).str.strip()
        return df

    # ========== CSS VINTAGE ==========
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');
        .stApp {
            font-family: 'Special Elite', cursive !important;
            background:
                linear-gradient(rgba(245, 242, 230, 0.85), rgba(245, 242, 230, 0.85)),
                url("https://i.imgur.com/XDBQZxv.jpg") no-repeat center center fixed;
            background-size: cover;
        }
        header[data-testid="stHeader"] {display: none;}
        .top-title {
            font-size: 34px; font-weight: bold; text-align: center;
            color: #3e2723; text-shadow: 1px 1px 0px #fff;
        }
        .main-title {
            font-size: 26px; font-weight: 900; text-align: center;
            color: #5d4037; margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="top-title">📜 Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">🔎 Tra cứu Part number</div>', unsafe_allow_html=True)

    zone = st.selectbox("📂 Bạn muốn tra cứu zone nào?", xls.sheet_names)
    if zone:
        df = load_and_clean(zone)
        if "A/C" in df.columns:
            aircrafts = sorted(df["A/C"].dropna().unique())
            aircraft = st.selectbox("✈️ Loại máy bay?", aircrafts)
            if aircraft:
                df_ac = df[df["A/C"] == aircraft]
                if "DESCRIPTION" in df_ac.columns:
                    descs = sorted(df_ac["DESCRIPTION"].dropna().unique())
                    desc = st.selectbox("📑 Phần nào?", descs)
                    if desc:
                        df_result = df_ac[df_ac["DESCRIPTION"] == desc]
                        if not df_result.empty:
                            st.write(df_result)
                        else:
                            st.warning("Không có dữ liệu phù hợp.")
