import streamlit as st
import pandas as pd
import base64
import time

# ===================== VIDEO INTRO =====================
video_file = "airplane.mp4"
with open(video_file, "rb") as f:
    video_bytes = f.read()
video_base64 = base64.b64encode(video_bytes).decode()

st.markdown(f"""
<style>
html, body {{
    margin: 0;
    padding: 0;
    height: 100%;
    overflow: hidden;
}}

#video-container {{
    position: fixed;
    top: 0; left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 9999;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: black;
}}

#intro-video {{
    width: 100%;
    height: 100%;
    object-fit: cover;
}}

@keyframes fadeInText {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes smokeFade {{
    0% {{ opacity: 1; filter: blur(0px); }}
    100% {{ opacity: 0; filter: blur(15px); }}
}}

#intro-text {{
    position: absolute;
    bottom: 12%;
    width: 100%;
    text-align: center;
    font-family: 'Special Elite', cursive;
    font-size: 32px;
    font-weight: bold;
    color: #f5f5f5;
    text-shadow: 0 0 15px #c0c0c0, 0 0 25px #a0a0a0, 0 0 35px #ffffff;
    opacity: 0;
    animation: fadeInText 2.5s ease-out 1s forwards, smokeFade 3s ease-in 6s forwards, shimmer 4s infinite;
    background: linear-gradient(90deg, #fff, #b0b0b0, #d0d0d0, #fff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

@keyframes shimmer {{
    0% {{ background-position: -200px; }}
    100% {{ background-position: 200px; }}
}}

@keyframes fadeOut {{
    from {{ opacity: 1; }}
    to {{ opacity: 0; }}
}}
</style>

<div id="video-container">
    <video id="intro-video" autoplay playsinline muted>
        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
    </video>
    <div id="intro-text">KHÁM PHÁ THẾ GIỚI CÙNG CHÚNG TÔI</div>
</div>

<script>
function showApp() {{
    const videoContainer = document.getElementById('video-container');
    if (!videoContainer) return;

    videoContainer.style.animation = 'fadeOut 2s ease-in-out forwards';

    setTimeout(() => {{
        videoContainer.remove();
        const app = document.querySelector('.stApp');
        if (app) {{
            app.style.visibility = 'visible';
            app.style.opacity = '0';
            app.style.transition = 'opacity 2s ease';
            setTimeout(() => {{ app.style.opacity = '1'; }}, 100);
        }}
    }}, 2000);
}}

const vid = document.getElementById('intro-video');
if (vid) {{
    vid.addEventListener('ended', showApp);
}}

setTimeout(() => {{
    const videoContainer = document.getElementById('video-container');
    if (videoContainer) {{
        showApp();
    }}
}}, 9500);
</script>
""", unsafe_allow_html=True)

# ===================== HIDE MAIN APP INITIALLY =====================
st.markdown(
    """
    <style>
    .stApp {
        visibility: hidden;
        opacity: 0;
        transition: opacity 1s ease;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ===================== VINTAGE MAIN APP =====================
excel_file = "A787.xlsx"
xls = pd.ExcelFile(excel_file)

def load_and_clean(sheet):
    df = pd.read_excel(excel_file, sheet_name=sheet)
    df.columns = df.columns.str.strip().str.upper()
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("").astype(str).str.strip()
    return df

def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

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

# ===================== APP MAIN CONTENT =====================
st.markdown('<div class="top-title">📜 Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🔎 Tra cứu Part number</div>', unsafe_allow_html=True)

zone = st.selectbox("📂 Bạn muốn tra cứu zone nào?", xls.sheet_names)
if zone:
    df = load_and_clean(zone)
    if "A/C" in df.columns:
        aircrafts = sorted([ac for ac in df["A/C"].dropna().unique().tolist() if ac])
        aircraft = st.selectbox("✈️ Loại máy bay?", aircrafts)
        if aircraft:
            df_ac = df[df["A/C"] == aircraft]
            if "DESCRIPTION" in df_ac.columns:
                descs = sorted([d for d in df_ac["DESCRIPTION"].dropna().unique().tolist() if d])
                desc = st.selectbox("📑 Bạn muốn tra cứu phần nào?", descs)
                if desc:
                    df_desc = df_ac[df_ac["DESCRIPTION"] == desc]
                    if "ITEM" in df_desc.columns:
                        items = sorted([i for i in df_desc["ITEM"].dropna().unique().tolist() if i])
                        item = st.selectbox("🔢 Item nào?", items)
                        if item:
                            df_desc = df_desc[df_desc["ITEM"] == item]
                    if not df_desc.empty:
                        df_res = df_desc.copy().reset_index(drop=True)
                        cols = ["PART NUMBER (PN)"]
                        for alt in ["PART INTERCHANGE", "PN INTERCHANGE"]:
                            if alt in df_res.columns:
                                cols.append(alt)
                                break
                        if "NOTE" in df_res.columns:
                            cols.append("NOTE")
                        df_res = df_res[cols]
                        df_res.insert(0, "STT", range(1, len(df_res) + 1))
                        st.markdown(f'<div class="highlight-msg">✅ Tìm thấy {len(df_res)} dòng dữ liệu</div>', unsafe_allow_html=True)
                        st.write(df_res.to_html(escape=False, index=False), unsafe_allow_html=True)
                    else:
                        st.error("📌 Rất tiếc, không tìm thấy dữ liệu phù hợp.")

