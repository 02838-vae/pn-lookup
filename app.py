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
# 🎬 VIDEO INTRO FULLSCREEN + HIỆU ỨNG CHỮ NÂNG CẤP
# ======================================================
if "intro_done" not in st.session_state:
    st.session_state.intro_done = False

if not st.session_state.intro_done:
    video_path = "airplane.mp4"

    try:
        video_base64 = get_base64_of_bin_file(video_path)

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
        #intro-video-container {{
            position: fixed;
            top: 0; left: 0;
            width: 100vw;
            height: 100vh;
            background-color: black;
            z-index: 99999;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            animation: fadeOut 1.6s ease-in-out forwards;
            animation-delay: 8s;
        }}
        video {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        /* --- CHỮ DƯỚI MÁY BAY --- */
        .intro-text {{
            position: absolute;
            bottom: 12%;
            width: 100%;
            text-align: center;
            font-family: 'Cinzel', serif;
            font-size: 40px;
            letter-spacing: 3px;
            font-weight: bold;
        }}

        /* Tạo hiệu ứng cho từng từ */
        .intro-text span {{
            display: inline-block;
            opacity: 0;
            background: linear-gradient(90deg, #ff4b1f, #ff9068, #ffd200, #00c3ff, #ff4b1f);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 400%;
            animation: colorShift 3s linear infinite, wordFade 7s ease-in-out forwards;
        }}

        /* Mỗi từ xuất hiện lệch thời gian */
        .intro-text span:nth-child(1) {{ animation-delay: 0.2s, 0.2s; }}
        .intro-text span:nth-child(2) {{ animation-delay: 0.7s, 0.7s; }}
        .intro-text span:nth-child(3) {{ animation-delay: 1.2s, 1.2s; }}
        .intro-text span:nth-child(4) {{ animation-delay: 1.7s, 1.7s; }}
        .intro-text span:nth-child(5) {{ animation-delay: 2.2s, 2.2s; }}

        /* Đổi màu liên tục */
        @keyframes colorShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        /* Xuất hiện từng từ, rồi tan biến */
        @keyframes wordFade {{
            0% {{ opacity: 0; transform: translateY(40px); }}
            20% {{ opacity: 1; transform: translateY(0); }}
            80% {{ opacity: 1; transform: translateY(0); }}
            100% {{ opacity: 0; transform: translateY(-40px); }}
        }}

        /* --- FADEOUT VIDEO --- */
        @keyframes fadeOut {{
            0% {{opacity: 1;}}
            90% {{opacity: 1;}}
            100% {{opacity: 0; visibility: hidden;}}
        }}
        </style>

        <div id="intro-video-container">
            <video autoplay muted playsinline>
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            </video>

            <!-- Chữ chia theo từng từ -->
            <div class="intro-text">
                <span>KHÁM</span>&nbsp;
                <span>PHÁ</span>&nbsp;
                <span>THẾ</span>&nbsp;
                <span>GIỚI</span>&nbsp;
                <span>CÙNG&nbsp;CHÚNG&nbsp;TÔI</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        time.sleep(9)
        st.session_state.intro_done = True
        st.rerun()

    except Exception as e:
        st.error(f"Lỗi phát video: {e}")

# ======================================================
# 🌿 GIAO DIỆN CHÍNH — GIỮ NGUYÊN
# ======================================================
else:
    st.title("🌍 Trang chính (giữ nguyên từ bản trước)")
