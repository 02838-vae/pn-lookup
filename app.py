import os
import base64
import pandas as pd
import streamlit as st

# ====== Cấu hình ======
excel_file = "A787.xlsx"   # file Excel của bạn (giữ nguyên)
bg_image_file = "airplane.jpg"  # nền (phải có)

# ====== Hàm đọc và dọn dữ liệu ======
def load_and_clean(sheet):
    df = pd.read_excel(excel_file, sheet_name=sheet)
    df.columns = df.columns.str.strip().str.upper()
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("").astype(str).str.strip()
    return df

# ====== Hàm encode ảnh thành base64 ======
def get_base64_of_bin_file(bin_file):
    if not os.path.exists(bin_file):
        return None
    with open(bin_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ====== Tạo SVG noise (base64) để dùng offline, tránh image not found ======
def generate_noise_data_uri(opacity=0.12, base_freq=0.9):
    # SVG nhỏ sinh nhiễu (feTurbulence). Sẽ base64 encode để an toàn.
    svg = f"""
    <svg xmlns='http://www.w3.org/2000/svg' width='800' height='600'>
      <filter id='noise'>
        <feTurbulence type='fractalNoise' baseFrequency='{base_freq}' numOctaves='1' stitchTiles='stitch'/>
        <feColorMatrix type='saturate' values='0'/>
        <feComponentTransfer>
          <feFuncA type='table' tableValues='0 {opacity}'/>
        </feComponentTransfer>
      </filter>
      <rect width='100%' height='100%' filter='url(#noise)' />
    </svg>
    """.strip()
    svg_b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{svg_b64}"

# ====== Chuẩn bị dữ liệu base64 ======
# Excel
if not os.path.exists(excel_file):
    st.error(f"⚠️ Không tìm thấy file Excel: {excel_file}. Xin kiểm tra lại.")
    st.stop()

xls = pd.ExcelFile(excel_file)

# Background image
img_base64 = get_base64_of_bin_file(bg_image_file)
if img_base64 is None:
    st.warning(f"⚠️ Không tìm thấy '{bg_image_file}' trong thư mục. Ứng dụng vẫn chạy nhưng nền mặc định sẽ trống.")
    img_url_css = ""
else:
    img_url_css = f'url("data:image/jpg;base64,{img_base64}")'

# Noise SVG data URI (offline)
noise_data_uri = generate_noise_data_uri(opacity=0.12, base_freq=0.9)

# ====== CSS (vintage + noise offline) ======
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

    /* Toàn trang - vintage sepia blend */
    .stApp {{
        background:
            linear-gradient(rgba(94,38,18,0.55), rgba(250,240,202,0.7)),
            {img_url_css if img_url_css else 'none'};
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-blend-mode: multiply;
        font-family: 'Special Elite', cursive !important;
        position: relative;
        overflow: visible;
    }}

    /* Grain/noise overlay (SVG base64 nhúng) - offline */
    .stApp::after {{
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: url("{noise_data_uri}");
        background-size: 100% 100%;
        opacity: 0.12; /* bạn có thể chỉnh nhỏ hơn/nhiều hơn */
        pointer-events: none;
        z-index: 0;
        mix-blend-mode: overlay;
    }}

    /* Nội dung nổi trên noise */
    .block-container {{
        position: relative;
        z-index: 1;
        padding-top: 0.5rem !important;
    }}

    header[data-testid="stHeader"] {{ display: none; }}

    /* Tiêu đề */
    .top-title {{
        font-size: 34px;
        font-weight: 900;
        text-align: center;
        margin: 18px auto 6px auto;
        color: #3e2723;
        text-shadow: 1px 1px 0px #fff;
        font-family: 'Special Elite', cursive !important;
    }}

    .main-title {{
        font-size: 24px;
        font-weight: 800;
        text-align: center;
        color: #5d4037;
        margin: 6px 0 18px 0;
        font-family: 'Special Elite', cursive !important;
    }}

    /* Label câu hỏi (bắt chặt selector để chắc chắn áp dụng) */
    div[role="group"] label, label[data-testid="stWidgetLabel"], div[data-testid="stMarkdownContainer"] > p {{
        font-family: 'Special Elite', cursive !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #2c1a0c !important;
        text-shadow: 0.6px 0.6px 0.8px #fff !important;
    }}

    /* Hộp selectbox - nội dung + dropdown */
    .stSelectbox div[data-baseweb="select"],
    .stSelectbox div[data-baseweb="popover"] {{
        font-family: 'Special Elite', cursive !important;
        font-size: 15px !important;
        color: #2c1a0c !important;
        background: #fdf6e3 !important;
        border: 1.2px dashed #5d4037 !important;
        border-radius: 6px !important;
    }}

    /* Bảng vintage */
    table.dataframe {{
        width: 100%;
        border-collapse: collapse !important;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 6px 14px rgba(0,0,0,0.2);
        background: #fffaf0;
        font-family: 'Special Elite', cursive !important;
    }}
    table.dataframe thead th {{
        background: #5d4037 !important;
        color: #f8f1df !important;
        font-weight: 800;
        text-align: center;
        padding: 10px !important;
        font-size: 15px;
        border: 2px solid #3e2723 !important;
    }}
    table.dataframe tbody td {{
        text-align: center !important;
        padding: 8px !important;
        font-size: 14px;
        color: #3e2723 !important;
        border: 1px solid #e6d7c4 !important;
    }}
    table.dataframe tbody tr:nth-child(even) td {{ background: #f6efe0 !important; }}
    table.dataframe tbody tr:hover td {{ background: #fceec8 !important; transition: 0.2s ease-in-out; }}

    /* Thông báo */
    .highlight-msg {{
        font-size: 18px;
        font-weight: 800;
        color: #3e2723;
        background: #e9decf;
        padding: 10px 14px;
        border-left: 6px solid #3e2723;
        border-radius: 6px;
        margin: 14px 0;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-family: 'Special Elite', cursive !important;
    }}

    .shake {{ display: inline-block; animation: shake 1s infinite; }}
    @keyframes shake {{
        0% {{ transform: translate(1px, 1px) rotate(0deg); }}
        25% {{ transform: translate(-1px, -1px) rotate(-1deg); }}
        50% {{ transform: translate(-2px, 2px) rotate(1deg); }}
        75% {{ transform: translate(2px, -2px) rotate(1deg); }}
        100% {{ transform: translate(1px, 1px) rotate(0deg); }}
    }}
    </style>
""", unsafe_allow_html=True)

# ====== Header ======
st.markdown('<div class="top-title">📜 Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🔎 Tra cứu Part number</div>', unsafe_allow_html=True)

# ====== Logic dropdowns & result display ======
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

                # các cột hiển thị
                cols_to_show = ["PART NUMBER (PN)"]
                for alt_col in ["PART INTERCHANGE", "PN INTERCHANGE"]:
                    if alt_col in df_result.columns:
                        cols_to_show.append(alt_col)
                        break
                if "NOTE" in df_result.columns:
                    cols_to_show.append("NOTE")

                df_result = df_result[cols_to_show]
                df_result.insert(0, "STT", range(1, len(df_result) + 1))

                st.markdown(f'<div class="highlight-msg"><span class="shake">✅</span> Tìm thấy {len(df_result)} dòng dữ liệu</div>', unsafe_allow_html=True)
                st.write(df_result.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.error("Rất tiếc, không tìm thấy dữ liệu phù hợp.")
