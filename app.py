import streamlit as st
import pandas as pd
import base64
import os

st.set_page_config(page_title="Tổ Bảo Dưỡng Số 1", layout="wide")

# ===== HÀM LOAD FILE THÀNH BASE64 =====
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ======== HIỂN THỊ VIDEO INTRO =========
if "show_main" not in st.session_state:
    st.session_state.show_main = False

video_file = "airplane.mp4"

if not st.session_state.show_main:
    if os.path.exists(video_file):
        video_data = get_base64(video_file)
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
        video {{
            width:100%; height:100%;
            object-fit:contain;
        }}
        .intro-text {{
            position:absolute;
            bottom:12vh;
            width:100%;
            text-align:center;
            font-family:'Special Elite', cursive;
            font-size:38px;
            color:#ffffff;
            text-shadow:0 0 30px rgba(255,255,255,0.9);
            opacity:0;
            animation: fadeIn 2.5s ease 1s forwards, fadeOut 2.5s ease 6s forwards;
        }}
        @keyframes fadeIn {{
            from {{opacity:0; transform:translateY(20px) scale(0.98);}}
            to {{opacity:1; transform:translateY(0) scale(1);}}
        }}
        @keyframes fadeOut {{
            from {{opacity:1;}}
            to {{opacity:0; transform:translateY(-20px) scale(1.02); filter:blur(8px);}}
        }}
        </style>

        <div id="intro">
            <video autoplay muted playsinline id="introVideo">
                <source src="data:video/mp4;base64,{video_data}" type="video/mp4">
            </video>
            <div class="intro-text">KHÁM PHÁ THẾ GIỚI CÙNG CHÚNG TÔI</div>
        </div>

        <script>
        const video = document.getElementById("introVideo");
        video.onended = () => {{
            window.location.href = window.location.href + "?main=true";
        }};
        </script>
        """, unsafe_allow_html=True)
        st.stop()
    else:
        st.warning("⚠️ Không tìm thấy file airplane.mp4 trong thư mục app.")
        st.stop()

# ====== XỬ LÝ SAU KHI VIDEO KẾT THÚC ======
query_params = st.query_params
if "main" in query_params:
    st.session_state.show_main = True

# ======== TRANG CHÍNH ========
excel_file = "A787.xlsx"
if not os.path.exists(excel_file):
    st.error("⚠️ Không tìm thấy file A787.xlsx")
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
header[data-testid="stHeader"] {{display: none;}}
.block-container {{padding-top: 0rem !important;}}

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
table.dataframe tbody tr:nth-child(even) td {{background: #f8f4ec !important;}}
table.dataframe tbody tr:hover td {{background: #f1e0c6 !important; transition: 0.3s ease-in-out;}}
</style>
""", unsafe_allow_html=True)

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
