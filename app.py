import streamlit as st
import time
import base64
import pandas as pd

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

# ===== Hàm đọc file nhị phân thành Base64 =====
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        return base64.b64encode(f.read()).decode()


# ======================================================
# ================ PHẦN VIDEO INTRO ====================
# ======================================================
if "intro_done" not in st.session_state:
    st.session_state.intro_done = False

if not st.session_state.intro_done:
    try:
        video_path = "airplane.mp4"
        video_base64 = get_base64_of_bin_file(video_path)

        # Video full màn hình + hiệu ứng fade-out khi kết thúc
        video_html = f"""
        <style>
        html, body {{
            margin: 0; padding: 0; overflow: hidden;
            background-color: black;
        }}
        .stApp {{
            visibility: hidden; /* Ẩn toàn bộ nội dung app */
        }}
        #intro-video {{
            position: fixed; top: 0; left: 0;
            width: 100vw; height: 100vh;
            z-index: 99999;
            background-color: black;
            display: flex; align-items: center; justify-content: center;
            animation: fadeIn 1.2s ease;
        }}
        video {{
            width: 100vw; height: 100vh;
            object-fit: cover;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        @keyframes fadeOut {{
            from {{ opacity: 1; }}
            to {{ opacity: 0; }}
        }}
        </style>

        <div id="intro-video">
            <video autoplay muted playsinline id="intro" onended="fadeOutVideo()">
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            </video>
        </div>

        <script>
        function fadeOutVideo() {{
            const v = document.getElementById('intro-video');
            v.style.animation = 'fadeOut 1.5s ease forwards';
            setTimeout(() => {{
                v.remove();
                const app = window.parent.document.querySelector('.stApp');
                if (app) {{
                    app.style.visibility = 'visible';
                    app.style.animation = 'fadeInApp 1.5s ease forwards';
                }}
            }}, 1500);
        }}
        </script>

        <style>
        @keyframes fadeInApp {{
            from {{ opacity: 0; transform: scale(1.02); }}
            to {{ opacity: 1; transform: scale(1); }}
        }}
        </style>
        """
        st.markdown(video_html, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ Không tìm thấy file airplane.mp4 — vui lòng thêm vào cùng thư mục với app.py")

    # Sau thời gian video (phòng khi JS không hoạt động)
    time.sleep(6)
    st.session_state.intro_done = True


# ======================================================
# ============== PHẦN GIAO DIỆN CHÍNH ==================
# ======================================================
if st.session_state.intro_done:
    img_base64 = get_base64_of_bin_file("airplane.jpg")

    # ===== CSS phong cách vintage =====
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

    .stApp {{
        font-family: 'Special Elite', cursive !important;
        background:
            linear-gradient(rgba(245, 242, 230, 0.88), rgba(245, 242, 230, 0.88)),
            url("data:image/jpeg;base64,{img_base64}") no-repeat center center fixed;
        background-size: cover;
        opacity: 0;
        animation: fadeInApp 1.2s ease forwards;
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

    .stSelectbox label {{
        font-weight: bold !important;
        font-size: 18px !important;
        color: #4e342e !important;
    }}

    .stSelectbox div[data-baseweb="select"] {{
        font-size: 15px !important;
        color: #3e2723 !important;
        background: #fdfbf5 !important;
        border: 1.5px dashed #5d4037 !important;
        border-radius: 6px !important;
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
