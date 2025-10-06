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

        # Hiển thị video full màn hình
        video_html = f"""
        <div style="
            position: fixed; top: 0; left: 0;
            width: 100%; height: 100%;
            background: black; z-index: 9999;
            display: flex; align-items: center; justify-content: center;">
            <video autoplay muted playsinline style="width:100%; height:100%; object-fit:cover;">
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            </video>
        </div>
        """
        video_container = st.empty()
        video_container.markdown(video_html, unsafe_allow_html=True)

        # ⏱️ Thời gian video chạy (thay đổi cho đúng độ dài file mp4 của bạn)
        time.sleep(6)  # ví dụ: video dài 6 giây

        # Ẩn video và đánh dấu là đã xong
        video_container.empty()
        st.session_state.intro_done = True

    except FileNotFoundError:
        st.warning("⚠️ Không tìm thấy file airplane.mp4 — vui lòng thêm vào cùng thư mục với app.py")

# ======================================================
# ============== PHẦN GIAO DIỆN CHÍNH ==================
# ======================================================

if st.session_state.intro_done:
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
        opacity: 0;
        animation: fadeIn 1s forwards;
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    header[data-testid="stHeader"] {{ display: none; }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="top-title" style="font-size:34px; text-align:center;">📜 Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title" style="font-size:26px; text-align:center;">🔎 Tra cứu Part number</div>', unsafe_allow_html=True)

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

                    st.success(f"✅ Tìm thấy {len(df_result)} dòng dữ liệu")
                    st.write(df_result)
                else:
                    st.error("📌 Rất tiếc, không tìm thấy dữ liệu phù hợp.")
