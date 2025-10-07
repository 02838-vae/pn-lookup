import streamlit as st
import pandas as pd
import base64
import os
import time

st.set_page_config(page_title="Tổ Bảo Dưỡng Số 1", layout="wide")

# --- Hàm encode video ---
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# --- Quản lý trạng thái ---
if "show_main" not in st.session_state:
    st.session_state.show_main = False
if "video_played" not in st.session_state:
    st.session_state.video_played = False

video_file = "airplane.mp4"

# --- Màn hình video intro ---
if not st.session_state.show_main:
    if os.path.exists(video_file):
        video_data = get_base64(video_file)

        # Hiển thị video toàn màn hình
        st.markdown(f"""
        <style>
        html, body, [data-testid="stAppViewContainer"] {{
            margin:0; padding:0; background:black; overflow:hidden;
        }}
        video {{
            width:100vw;
            height:100vh;
            object-fit:contain;
        }}
        .intro-text {{
            position:absolute;
            bottom:12vh;
            width:100%;
            text-align:center;
            font-family:'Special Elite', cursive;
            font-size:40px;
            font-weight:bold;
            color:#ffffff;
            text-shadow:
                0 0 20px rgba(255,255,255,0.8),
                0 0 40px rgba(180,220,255,0.6),
                0 0 60px rgba(255,255,255,0.4);
            opacity:0;
            animation:
                appear 3s ease-in forwards,
                floatFade 3s ease-in 5s forwards;
        }}
        @keyframes appear {{
            0% {{ opacity: 0; filter: blur(8px); transform: translateY(40px); }}
            100% {{ opacity: 1; filter: blur(0); transform: translateY(0); }}
        }}
        @keyframes floatFade {{
            0% {{ opacity: 1; filter: blur(0); transform: translateY(0); }}
            100% {{ opacity: 0; filter: blur(12px); transform: translateY(-30px) scale(1.05); }}
        }}
        </style>

        <div style="position:fixed; inset:0; background:black; display:flex; justify-content:center; align-items:center; z-index:9999;">
            <video autoplay muted playsinline>
                <source src="data:video/mp4;base64,{video_data}" type="video/mp4">
            </video>
            <div class="intro-text">KHÁM PHÁ THẾ GIỚI CÙNG CHÚNG TÔI</div>
        </div>
        """, unsafe_allow_html=True)

        # Sau 8.5 giây tự chuyển sang trang chính
        if not st.session_state.video_played:
            st.session_state.video_played = True
            time.sleep(8.5)
            st.session_state.show_main = True
            st.rerun()
        st.stop()
    else:
        st.error("❌ Không tìm thấy file airplane.mp4")
        st.stop()

# --- Trang chính vintage ---
excel_file = "A787.xlsx"
if not os.path.exists(excel_file):
    st.error("❌ Không tìm thấy file A787.xlsx")
    st.stop()

xls = pd.ExcelFile(excel_file)

def load_and_clean(sheet):
    df = pd.read_excel(excel_file, sheet_name=sheet)
    df.columns = df.columns.str.strip().str.upper()
    df = df.replace(r'^\s*$', pd.NA, regex=True).dropna(how="all")
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("").astype(str).str.strip()
    return df

img_base64 = get_base64("airplane.jpg") if os.path.exists("airplane.jpg") else ""

# --- CSS vintage ---
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
    inset: 0;
    background: url("https://www.transparenttextures.com/patterns/aged-paper.png");
    opacity: 0.35;
    pointer-events: none;
}}
header[data-testid="stHeader"] {{display: none;}}
.block-container {{padding-top: 0 !important;}}

.top-title {{
    font-size: 34px;
    text-align: center;
    margin: 15px 0;
    color: #3e2723;
    text-shadow: 2px 2px 0 #fff;
    animation: fadeIn 2s ease;
}}
.main-title {{
    font-size: 26px;
    font-weight: bold;
    text-align: center;
    color: #5d4037;
    margin-top: 5px;
    margin-bottom: 20px;
    text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
    animation: fadeIn 3s ease;
}}
@keyframes fadeIn {{
    from {{opacity:0; transform:translateY(20px);}}
    to {{opacity:1; transform:translateY(0);}}
}}

table.dataframe {{
    width: 100%;
    border-collapse: collapse;
    background: #fdfbf5;
}}
table.dataframe thead th {{
    background: #6d4c41;
    color: #fff8e1;
    padding: 10px;
    border: 2px solid #3e2723;
    font-size: 15px;
}}
table.dataframe tbody td {{
    border: 1px dashed #5d4037;
    padding: 8px;
    font-size: 14px;
    color: #3e2723;
}}
table.dataframe tbody tr:nth-child(even) td {{background: #f8f4ec;}}
table.dataframe tbody tr:hover td {{background: #f1e0c6; transition: 0.3s;}}
</style>
""", unsafe_allow_html=True)

# --- Nội dung trang chính ---
st.markdown('<div class="top-title">📜 Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🔎 Tra cứu Part number</div>', unsafe_allow_html=True)

zone = st.selectbox("📂 Chọn zone:", xls.sheet_names)
if zone:
    df = load_and_clean(zone)
    if "A/C" in df.columns:
        aircrafts = sorted([ac for ac in df["A/C"].dropna().unique().tolist() if ac])
        aircraft = st.selectbox("✈️ Loại máy bay:", aircrafts)
    else:
        aircraft = None

    if aircraft:
        df_ac = df[df["A/C"] == aircraft]
        if "DESCRIPTION" in df_ac.columns:
            descs = sorted(df_ac["DESCRIPTION"].dropna().unique())
            desc = st.selectbox("📑 Phần:", descs)
        else:
            desc = None

        if desc:
            df_filtered = df_ac[df_ac["DESCRIPTION"] == desc].copy()
            df_filtered = df_filtered.drop(columns=["A/C", "ITEM"], errors="ignore")
            df_filtered = df_filtered.replace(r'^\s*$', pd.NA, regex=True).dropna(how="all")
            if not df_filtered.empty:
                df_filtered.insert(0, "STT", range(1, len(df_filtered) + 1))
                st.write(df_filtered.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.warning("📌 Không có dữ liệu phù hợp.")
