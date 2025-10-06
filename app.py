import streamlit as st
import pandas as pd
import base64

# ===================== HÀM HỖ TRỢ =====================
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ===================== VIDEO INTRO =====================
video_file = "airplane.mp4"
try:
    video_base64 = get_base64_of_bin_file(video_file)
except FileNotFoundError:
    video_base64 = None
    st.warning("⚠️ Không tìm thấy file airplane.mp4 — sẽ bỏ qua phần video mở đầu.")

# ===================== NẾU CÓ VIDEO =====================
if video_base64 and "show_main" not in st.session_state:
    st.markdown(
        f"""
        <style>
        html, body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: black;
        }}
        video {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            object-fit: contain; /* đảm bảo full hình máy bay */
            z-index: 1;
            background-color: black;
        }}
        .fade-text {{
            position: fixed;
            bottom: 12%;
            width: 100%;
            text-align: center;
            font-family: 'Special Elite', cursive;
            font-size: 2.2em;
            font-weight: bold;
            color: #ffffff;
            text-shadow: 0 0 15px rgba(255,255,255,0.8);
            opacity: 0;
            animation: fadeText 8s ease-in-out forwards;
            z-index: 2;
        }}
        @keyframes fadeText {{
            0% {{ opacity: 0; filter: blur(10px); transform: translateY(20px); }}
            20% {{ opacity: 1; filter: blur(0px); transform: translateY(0); }}
            70% {{ opacity: 1; }}
            100% {{ opacity: 0; filter: blur(20px); transform: translateY(-20px); }}
        }}
        @keyframes shimmer {{
            0% {{ color: #f5f5f5; text-shadow: 0 0 10px #fff; }}
            50% {{ color: #b3e5fc; text-shadow: 0 0 20px #81d4fa; }}
            100% {{ color: #f5f5f5; text-shadow: 0 0 10px #fff; }}
        }}
        .fade-text span {{
            display: inline-block;
            animation: shimmer 3s infinite alternate;
        }}
        </style>

        <video autoplay muted playsinline id="introVideo">
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>
        <div class="fade-text"><span>KHÁM PHÁ THẾ GIỚI CÙNG CHÚNG TÔI</span></div>

        <script>
        const video = document.getElementById("introVideo");
        video.addEventListener("ended", () => {{
            window.parent.postMessage("videoEnded", "*");
        }});
        </script>
        """,
        unsafe_allow_html=True,
    )

    # Script nhận tín hiệu từ video -> chuyển sang giao diện chính
    st.markdown(
        """
        <script>
        window.addEventListener("message", (event) => {
            if (event.data === "videoEnded") {
                window.location.href = "?show_main=true";
            }
        });
        </script>
        """,
        unsafe_allow_html=True,
    )

    st.stop()

# ===================== GIAO DIỆN CHÍNH (VINTAGE) =====================
excel_file = "A787.xlsx"
xls = pd.ExcelFile(excel_file)

def load_and_clean(sheet):
    df = pd.read_excel(excel_file, sheet_name=sheet)
    df.columns = df.columns.str.strip().str.upper()
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("").astype(str).str.strip()
    return df

img_base64 = get_base64_of_bin_file("airplane.jpg")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');
.stApp {{
    font-family: 'Special Elite', cursive !important;
    background: linear-gradient(rgba(245,242,230,0.85), rgba(245,242,230,0.85)),
                url("data:image/jpeg;base64,{img_base64}") no-repeat center center fixed;
    background-size: cover;
}}
.stApp::after {{
    content: "";
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: url("https://www.transparenttextures.com/patterns/aged-paper.png");
    opacity: 0.35; pointer-events: none; z-index: -1;
}}
.block-container {{ padding-top: 0rem !important; }}
header[data-testid="stHeader"] {{ display: none; }}
.top-title {{
    font-size: 34px; font-weight: bold; text-align: center;
    margin: 20px auto 10px auto; color: #3e2723; text-shadow: 1px 1px 0px #fff;
}}
.main-title {{
    font-size: 26px; font-weight: 900; text-align: center;
    color: #5d4037; margin-top: 5px; margin-bottom: 20px;
    text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="top-title">📜 Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🔎 Tra cứu Part number</div>', unsafe_allow_html=True)

zone = st.selectbox("📂 Bạn muốn tra cứu zone nào?", xls.sheet_names)
if zone:
    df = load_and_clean(zone)
    if "A/C" in df.columns:
        aircrafts = sorted([ac for ac in df["A/C"].dropna().unique().tolist() if ac and ac.upper() != "NAN"])
        aircraft = st.selectbox("✈️ Loại máy bay?", aircrafts)
    else:
        aircraft = None

    if aircraft:
        df_ac = df[df["A/C"] == aircraft]
        if "DESCRIPTION" in df_ac.columns:
            desc_list = sorted([d for d in df_ac["DESCRIPTION"].dropna().unique().tolist() if d and d.upper() != "NAN"])
            description = st.selectbox("📑 Bạn muốn tra cứu phần nào?", desc_list)
        else:
            description = None

        if description:
            df_desc = df_ac[df_ac["DESCRIPTION"] == description]
            if "ITEM" in df_desc.columns:
                items = sorted([i for i in df_desc["ITEM"].dropna().unique().tolist() if i and i.upper() != "NAN"])
                if items:
                    item = st.selectbox("🔢 Bạn muốn tra cứu Item nào?", items)
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

                st.success(f"✅ Tìm thấy {len(df_result)} dòng dữ liệu")
                st.write(df_result.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.error("📌 Rất tiếc, không tìm thấy dữ liệu phù hợp.")
