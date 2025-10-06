import pandas as pd
import streamlit as st
import base64
import os

# ===== VIDEO INTRO =====
video_file = "airplane.mp4"

if os.path.exists(video_file):
    with open(video_file, "rb") as f:
        video_bytes = f.read()
    video_base64 = base64.b64encode(video_bytes).decode("utf-8")

    st.markdown(f"""
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
        flex-direction: column;
    }}
    #intro-video {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}
    #intro-text {{
        position: absolute;
        bottom: 14vh;
        width: 100%;
        text-align: center;
        font-family: 'Special Elite', cursive;
        font-size: 42px;
        font-weight: bold;
        letter-spacing: 2px;
        color: #fff;
        text-shadow: 0 0 25px rgba(255,255,255,0.9), 0 0 40px rgba(0,150,255,0.6);
        opacity: 0;
        animation: fadeInText 3s ease-in-out 1s forwards, fadeOutText 4s ease-in-out 6s forwards, colorFlow 6s linear infinite;
        background: linear-gradient(90deg, #ffffff, #a8e6ff, #ffd3e0, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-size: 300% 300%;
    }}
    @keyframes colorFlow {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    @keyframes fadeInText {{
        0% {{ opacity: 0; transform: translateY(25px) scale(0.98); filter: blur(8px); }}
        100% {{ opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }}
    }}
    @keyframes fadeOutText {{
        0% {{ opacity: 1; filter: blur(0); }}
        100% {{ opacity: 0; transform: translateY(-30px) scale(1.05); filter: blur(10px); }}
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
    setTimeout(endIntro, 10000);
    </script>
    """, unsafe_allow_html=True)

    st.markdown("<style>.stApp {visibility: hidden;}</style>", unsafe_allow_html=True)

# ===== MAIN PAGE =====

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

# ===== Load ảnh nền =====
img_base64 = get_base64_of_bin_file("airplane.jpg")

# ===== CSS Vintage =====
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

.stApp {{
    font-family: 'Special Elite', cursive !important;
    background:
        linear-gradient(rgba(245, 242, 230, 0.9), rgba(245, 242, 230, 0.9)),
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

/* ======= VINTAGE TABLE ======= */
@keyframes fadeInTable {{
    from {{ opacity: 0; transform: scale(0.97) rotate(-0.5deg); filter: blur(6px); }}
    to {{ opacity: 1; transform: scale(1) rotate(0); filter: blur(0); }}
}}

table.dataframe {{
    width: 100%;
    border-collapse: collapse !important;
    border: 2px solid #5d4037;
    background: #fbf7ed;
    color: #3e2723 !important;
    font-size: 15px;
    text-align: center;
    margin-top: 10px;
    border-radius: 6px;
    animation: fadeInTable 0.8s ease-in-out;
}}
table.dataframe thead th {{
    background: linear-gradient(180deg, #8d6e63, #5d4037);
    color: #fff8e1 !important;
    font-weight: bold;
    padding: 10px !important;
    border: 1.5px solid #3e2723 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}}
table.dataframe tbody td {{
    padding: 8px !important;
    border: 1px dashed #6d4c41 !important;
}}
table.dataframe tbody tr:nth-child(even) td {{
    background: #f3e9d2 !important;
}}
table.dataframe tbody tr:hover td {{
    background: #f1d9b5 !important;
    transition: all 0.3s ease-in-out;
}}

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

# ===== Dropdown logic =====
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
