import streamlit as st
import pandas as pd
import base64
import time

# ===== Hàm load Excel =====
excel_file = "A787.xlsx"
xls = pd.ExcelFile(excel_file)

def load_and_clean(sheet):
    df = pd.read_excel(excel_file, sheet_name=sheet)
    df.columns = df.columns.str.strip().str.upper()
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("").astype(str).str.strip()
    return df

# ===== Hàm load file nhị phân thành Base64 =====
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        return base64.b64encode(f.read()).decode()


# ======================================================
# 🎬 VIDEO INTRO FULLSCREEN + CHỮ ÁNH SÁNG BẠC + KHÓI TAN
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
            width: 100vw !important;
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

        /* --- DÒNG CHỮ PHÍA DƯỚI MÁY BAY --- */
        #intro-text {{
            position: fixed;
            bottom: 15%;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            text-align: center;
            font-family: 'Cinzel', serif;
            font-size: 48px;
            font-weight: bold;
            letter-spacing: 3px;
            color: #ffffff;
            text-shadow: 0px 0px 15px rgba(255,255,255,0.7);
            opacity: 0;
            z-index: 10000;
            background: linear-gradient(90deg, #ffffff, #a3b8ff, #ffffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 200% auto;
            animation: fadeSmoke 7s ease-in-out forwards, shine 3s linear infinite;
            animation-delay: 1s;
        }}

        /* --- Hiệu ứng ánh sáng bạc --- */
        @keyframes shine {{
            0% {{ background-position: 200% center; }}
            100% {{ background-position: -200% center; }}
        }}

        /* --- Hiệu ứng khói tan --- */
        @keyframes fadeSmoke {{
            0% {{
                opacity: 0;
                filter: blur(20px);
                transform: translateX(-50%) translateY(40px);
            }}
            25% {{
                opacity: 1;
                filter: blur(0px);
                transform: translateX(-50%) translateY(0);
            }}
            75% {{
                opacity: 1;
                filter: blur(2px);
            }}
            100% {{
                opacity: 0;
                filter: blur(25px);
                transform: translateX(-50%) translateY(-40px);
            }}
        }}

        /* --- Video mờ dần --- */
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

        time.sleep(9)
        st.session_state.intro_done = True
        st.rerun()

    except Exception as e:
        st.error(f"Lỗi phát video: {e}")

# ======================================================
# 🌿 TRANG CHÍNH — PHONG CÁCH VINTAGE GỐC CỦA BẠN
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
        animation: fadeInPage 2.5s ease-in-out;
    }}
    @keyframes fadeInPage {{
        0% {{ opacity: 0; filter: blur(10px); }}
        100% {{ opacity: 1; filter: blur(0px); }}
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

    .block-container {{ padding-top: 0rem !important; }}
    header[data-testid="stHeader"] {{ display: none; }}

    .top-title {{
        font-size: 34px;
        font-weight: bold;
        text-align: center;
        margin: 20px auto 10px auto;
        color: #3e2723;
        text-shadow: 1px 1px 0px #fff;
    }}
    .main-title {{
        font-size: 26px;
        font-weight: 900;
        text-align: center;
        color: #5d4037;
        margin-top: 5px;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
    }}

    .stSelectbox label {{ font-weight: bold !important; font-size: 18px !important; color: #4e342e !important; }}
    .stSelectbox div[data-baseweb="select"] {{ font-size: 15px !important; color: #3e2723 !important; background: #fdfbf5 !important; border: 1.5px dashed #5d4037 !important; border-radius: 6px !important; }}
    .stSelectbox div[data-baseweb="popover"] {{ font-size: 15px !important; background: #fdfbf5 !important; color: #3e2723 !important; border: 1.5px dashed #5d4037 !important; }}

    table.dataframe {{
        width: 100%;
        border-collapse: collapse !important;
        border: 2px solid #5d4037;
        background: #fdfbf5;
        text-align: center;
    }}
    table.dataframe thead th {{
        background: #795548 !important;
        color: #fff8e1 !important;
        font-weight: bold;
        text-align: center;
        padding: 10px !important;
        font-size: 15px;
        border: 2px solid #5d4037 !important;
    }}
    table.dataframe tbody td {{
        text-align: center !important;
        padding: 8px !important;
        font-size: 14px;
        color: #3e2723 !important;
        border: 1.5px dashed #5d4037 !important;
    }}
    table.dataframe tbody tr:nth-child(even) td {{ background: #f8f4ec !important; }}
    table.dataframe tbody tr:hover td {{ background: #f1e0c6 !important; transition: 0.3s ease-in-out; }}

    .highlight-msg {{
        font-size: 18px;
        font-weight: bold;
        color: #3e2723;
        background: #efebe9;
        padding: 10px 15px;
        border-left: 6px solid #6d4c41;
        border-radius: 6px;
        margin: 15px 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }}
    </style>
    """, unsafe_allow_html=True)

    # ===== Header =====
    st.markdown('<div class="top-title">📜 Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">🔎 Tra cứu Part number</div>', unsafe_allow_html=True)

    # ===== Nhạc nền =====
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
        st.warning("⚠️ Không tìm thấy file background.mp3 — vui lòng thêm file vào cùng thư mục với app.py")

    # ===== Dropdowns & logic =====
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

                    st.markdown(
                        f'<div class="highlight-msg">✅ Tìm thấy {len(df_result)} dòng dữ liệu</div>',
                        unsafe_allow_html=True
                    )
                    st.write(df_result.to_html(escape=False, index=False), unsafe_allow_html=True)
                else:
                    st.error("📌 Rất tiếc, không tìm thấy dữ liệu phù hợp.")
