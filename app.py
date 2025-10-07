import streamlit as st
import pandas as pd
import base64
import os
import time

st.set_page_config(page_title="Tổ Bảo Dưỡng Số 1", layout="wide")

# ====== VIDEO CONFIG ======
VIDEO_PATH = "airplane.mp4"
VIDEO_DURATION = 9  # giây

# ====== KIỂM TRA TRẠNG THÁI INTRO ======
if "show_main" not in st.session_state:
    st.session_state.show_main = False

# ====== HIỂN THỊ VIDEO INTRO ======
if not st.session_state.show_main:
    if os.path.exists(VIDEO_PATH):
        with open(VIDEO_PATH, "rb") as f:
            video_b64 = base64.b64encode(f.read()).decode("utf-8")

        st.markdown(f"""
        <style>
        html, body, [data-testid="stAppViewContainer"] {{
            margin:0; padding:0; overflow:hidden; background:black;
        }}
        #intro {{
            position:fixed; inset:0; background:black;
            display:flex; align-items:center; justify-content:center;
            z-index:9999;
        }}
        video#introVideo {{
            width:100%; height:100%;
            object-fit:contain;
            background:black;
        }}
        .intro-text {{
            position:absolute;
            bottom:12vh;
            width:100%;
            text-align:center;
            font-family:'Special Elite', cursive;
            font-size:38px;
            color:#fff;
            text-shadow:0 0 25px rgba(255,255,255,0.9), 0 0 40px rgba(0,200,255,0.6);
            opacity:0;
            animation: fadeIn 2.5s ease 0.8s forwards, fadeOut 3s ease 6s forwards;
        }}
        @keyframes fadeIn {{
            from {{opacity:0; transform:translateY(20px) scale(0.98); filter:blur(6px);}}
            to {{opacity:1; transform:translateY(0) scale(1); filter:blur(0);}}
        }}
        @keyframes fadeOut {{
            from {{opacity:1;}}
            to {{opacity:0; transform:translateY(-20px) scale(1.02); filter:blur(8px);}}
        }}
        </style>

        <div id="intro">
            <video id="introVideo" autoplay muted playsinline>
                <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
            </video>
            <div class="intro-text">KHÁM PHÁ THẾ GIỚI CÙNG CHÚNG TÔI</div>
        </div>

        <script>
        const intro = document.getElementById('intro');
        const video = document.getElementById('introVideo');
        function hideIntro(){{
            intro.style.transition='opacity 1.5s ease';
            intro.style.opacity='0';
            setTimeout(()=>intro.remove(),1500);
        }}
        video.addEventListener('ended', hideIntro);
        setTimeout(hideIntro, {VIDEO_DURATION*1000});
        </script>
        """, unsafe_allow_html=True)

        st.markdown("<style>.stApp{visibility:hidden;}</style>", unsafe_allow_html=True)
        time.sleep(VIDEO_DURATION)
        st.session_state.show_main = True
        st.experimental_rerun()
    else:
        st.session_state.show_main = True
        st.experimental_rerun()

# ====== TRANG CHÍNH ======
# Background vintage
def b64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

bg_b64 = b64("airplane.jpg") if os.path.exists("airplane.jpg") else ""

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');
.stApp {{
    font-family:'Special Elite', cursive;
    background:
        linear-gradient(rgba(245,242,230,0.9), rgba(245,242,230,0.9)),
        url("data:image/jpeg;base64,{bg_b64}") center/cover no-repeat fixed;
}}
.stApp::after {{
    content:""; position:fixed; inset:0;
    background:url("https://www.transparenttextures.com/patterns/aged-paper.png");
    opacity:0.35; pointer-events:none; z-index:-1;
}}
header[data-testid="stHeader"]{{display:none;}}
.block-container{{padding-top:0rem !important;}}

.title-main {{
    text-align:center; color:#4e342e; font-size:34px; margin-top:10px;
    text-shadow:1px 1px 2px #fff;
}}
.subtitle {{
    text-align:center; color:#5d4037; font-size:22px; margin-bottom:15px;
}}

table.dataframe {{
    width:100%; border-collapse:collapse;
    border:2px solid #5d4037; background:#fbf7ed;
    color:#3e2723 !important; font-size:15px; text-align:center;
}}
table.dataframe thead th {{
    background:linear-gradient(180deg,#8d6e63,#5d4037);
    color:#fff8e1; font-weight:bold; padding:10px;
    border:1.5px solid #3e2723;
}}
table.dataframe tbody td {{
    padding:8px; border:1px dashed #6d4c41;
}}
table.dataframe tbody tr:nth-child(even) td{{background:#f3e9d2;}}
table.dataframe tbody tr:hover td{{background:#f1d9b5; transition:all .25s ease;}}
</style>
""", unsafe_allow_html=True)

EXCEL_FILE = "A787.xlsx"

if not os.path.exists(EXCEL_FILE):
    st.error("⚠️ Không tìm thấy file A787.xlsx")
else:
    xls = pd.ExcelFile(EXCEL_FILE)
    zone = st.selectbox("📂 Chọn zone:", xls.sheet_names)
    df = pd.read_excel(EXCEL_FILE, sheet_name=zone, dtype=object)
    df = df.replace(r'^\s*$', pd.NA, regex=True).dropna(how='all')

    st.markdown('<div class="title-main">📜 Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">🔎 Tra cứu Part number</div>', unsafe_allow_html=True)

    # lọc theo các cột nếu có
    ac_col = next((c for c in df.columns if c.strip().upper() == "A/C"), None)
    desc_col = next((c for c in df.columns if c.strip().upper() == "DESCRIPTION"), None)
    item_col = next((c for c in df.columns if c.strip().upper() == "ITEM"), None)

    df_filtered = df.copy()
    if ac_col:
        ac_list = sorted(df[ac_col].dropna().unique())
        ac_sel = st.selectbox("✈️ Loại máy bay:", ac_list)
        df_filtered = df_filtered[df_filtered[ac_col] == ac_sel]
    if desc_col:
        desc_list = sorted(df_filtered[desc_col].dropna().unique())
        desc_sel = st.selectbox("📑 Phần:", desc_list)
        df_filtered = df_filtered[df_filtered[desc_col] == desc_sel]
    if item_col:
        item_list = sorted(df_filtered[item_col].dropna().unique())
        if len(item_list) > 1:
            item_sel = st.selectbox("🔢 Item:", item_list)
            df_filtered = df_filtered[df_filtered[item_col] == item_sel]

    # chọn các cột cần hiển thị (loại bỏ A/C, ITEM)
    cols = [c for c in df_filtered.columns if c.strip().upper() not in ["A/C", "ITEM"]]
    df_show = df_filtered[cols].replace(r'^\s*$', pd.NA, regex=True).dropna(how='all').reset_index(drop=True)

    if df_show.empty:
        st.warning("Không có dữ liệu để hiển thị.")
    else:
        df_show.insert(0, "STT", range(1, len(df_show)+1))
        st.write(df_show.to_html(escape=False, index=False), unsafe_allow_html=True)
