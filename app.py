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
# 🎬 VIDEO INTRO FULLSCREEN + CHUYỂN CẢNH MƯỢT
# ======================================================
if "intro_done" not in st.session_state:
    st.session_state.intro_done = False

if not st.session_state.intro_done:
    video_path = "airplane.mp4"

    try:
        video_base64 = get_base64_of_bin_file(video_path)

        st.markdown(f"""
        <style>
        /* Ẩn header, sidebar, padding Streamlit */
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

        /* --- VÙNG VIDEO FULLSCREEN --- */
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
            animation-delay: 7s; /* thời gian video */
        }}
        video {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        /* --- LỚP MỜ DẦN KHI KẾT THÚC VIDEO --- */
        @keyframes fadeOut {{
            0% {{opacity: 1;}}
            90% {{opacity: 1;}}
            100% {{opacity: 0; visibility: hidden;}}
        }}

        /* --- CHỮ INTRO CINE STYLE --- */
        .intro-text {{
            position: absolute;
            color: white;
            font-family: 'Cinzel', serif;
            font-size: 42px;
            letter-spacing: 3px;
            text-shadow: 0px 0px 25px rgba(255,255,255,0.8);
            animation: fadeText 5s ease-in-out forwards;
        }}
        @keyframes fadeText {{
            0% {{opacity: 0; transform: scale(0.9);}}
            30% {{opacity: 1; transform: scale(1);}}
            70% {{opacity: 1; transform: scale(1);}}
            100% {{opacity: 0; transform: scale(1.1);}}
        }}
        </style>

        <div id="intro-video-container">
            <video autoplay muted playsinline>
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            </video>
            <div class="intro-text">TỔ BẢO DƯỠNG SỐ 1 ✈️</div>
        </div>
        """, unsafe_allow_html=True)

        time.sleep(8)
        st.session_state.intro_done = True
        st.rerun()

    except Exception as e:
        st.error(f"Lỗi phát video: {e}")


# ======================================================
# 🌿 GIAO DIỆN CHÍNH — PHONG CÁCH VINTAGE
# ======================================================
else:
    img_base64 = get_base64_of_bin_file("airplane.jpg")

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&display=swap');

    header[data-testid="stHeader"], div[data-testid="stToolbar"], footer {{
        display: none !important;
    }}

    .stApp {{
        font-family: 'Special+Elite', cursive !important;
        background:
            linear-gradient(rgba(245, 242, 230, 0.9), rgba(245, 242, 230, 0.9)),
            url("data:image/jpeg;base64,{img_base64}") no-repeat center center fixed;
        background-size: cover;
        animation: fadeInMain 1.5s ease-in-out;
    }}
    @keyframes fadeInMain {{
        from {{opacity: 0; filter: blur(6px);}}
        to {{opacity: 1; filter: blur(0);}}
    }}

    .block-container {{
        padding-top: 1rem !important;
    }}
    .top-title {{
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        color: #3e2723;
        text-shadow: 2px 2px 4px #fff;
        margin-top: 15px;
    }}
    .main-title {{
        font-size: 26px;
        text-align: center;
        color: #5d4037;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
    }}
    .stSelectbox label {{
        font-weight: bold;
        font-size: 18px;
        color: #4e342e;
    }}
    .stSelectbox div[data-baseweb="select"] {{
        background: #fdfbf5 !important;
        border: 1.5px dashed #5d4037 !important;
        border-radius: 6px !important;
    }}
    table.dataframe {{
        width: 100%;
        border-collapse: collapse;
        border: 2px solid #5d4037;
        background: #fdfbf5;
        text-align: center;
    }}
    table.dataframe thead th {{
        background: #795548;
        color: #fff8e1;
        font-weight: bold;
        padding: 10px;
        border: 2px solid #5d4037;
    }}
    table.dataframe tbody td {{
        padding: 8px;
        color: #3e2723;
        border: 1.5px dashed #5d4037;
    }}
    table.dataframe tbody tr:nth-child(even) td {{ background: #f8f4ec; }}
    table.dataframe tbody tr:hover td {{ background: #f1e0c6; transition: 0.3s; }}
    .highlight-msg {{
        font-size: 18px;
        font-weight: bold;
        color: #3e2723;
        background: #efebe9;
        padding: 10px;
        border-left: 6px solid #6d4c41;
        border-radius: 6px;
        margin: 15px 0;
        text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True)

    # ===== HEADER =====
    st.markdown('<div class="top-title">📜 Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">🔎 Tra cứu Part number</div>', unsafe_allow_html=True)

    # ===== NHẠC NỀN =====
    try:
        with open("background.mp3", "rb") as f:
            audio_bytes = f.read()
            st.markdown("<p style='text-align:center;'>🎵 Nhạc nền — nhấn Play để nghe</p>", unsafe_allow_html=True)
            st.audio(audio_bytes, format="audio/mp3")
    except FileNotFoundError:
        st.warning("⚠️ Thiếu file background.mp3")

    # ===== DROPDOWN TRA CỨU =====
    zone = st.selectbox("📂 Chọn zone muốn tra cứu", xls.sheet_names, key="zone")

    if zone:
        df = load_and_clean(zone)
        if "A/C" in df.columns:
            aircrafts = sorted(df["A/C"].dropna().unique())
            aircraft = st.selectbox("✈️ Loại máy bay", aircrafts)
        else:
            aircraft = None

        if aircraft:
            df_ac = df[df["A/C"] == aircraft]
            if "DESCRIPTION" in df_ac.columns:
                descs = sorted(df_ac["DESCRIPTION"].dropna().unique())
                description = st.selectbox("📑 Phần cần tra cứu", descs)
            else:
                description = None

            if description:
                df_desc = df_ac[df_ac["DESCRIPTION"] == description]
                if "ITEM" in df_desc.columns:
                    items = sorted(df_desc["ITEM"].dropna().unique())
                    item = st.selectbox("🔢 Item", items)
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
                    st.error("❌ Không tìm thấy dữ liệu phù hợp.")
