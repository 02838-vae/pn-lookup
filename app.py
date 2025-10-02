import pandas as pd
import streamlit as st
import base64
import os

# ===== Đọc file Excel =====
excel_file = "A787.xlsx"
xls = pd.ExcelFile(excel_file)

def load_and_clean(sheet):
    df = pd.read_excel(excel_file, sheet_name=sheet)
    df.columns = df.columns.str.strip().str.upper()
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("").astype(str).str.strip()
    return df

# ===== Load tất cả ảnh airplane*.jpg/jpeg/png =====
def get_base64_of_bin_file(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_files = [
    os.path.join(os.getcwd(), f)
    for f in os.listdir(".")
    if f.lower().startswith("airplane") and f.lower().endswith((".jpg", ".jpeg", ".png"))
]
bg_files.sort()

if not bg_files:
    st.error("⚠️ Không tìm thấy hình nền airplane trong thư mục!")
    img_base64_list = []
else:
    img_base64_list = [get_base64_of_bin_file(f) for f in bg_files]

# ===== CSS Vintage + Slideshow Background =====
css_images = ""
for i, img64 in enumerate(img_base64_list):
    css_images += f"""
    .bg-{i} {{
        background-image: url("data:image/jpg;base64,{img64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        position: fixed;
        top:0; left:0; right:0; bottom:0;
        opacity: 0;
        animation: fadeinout {len(img_base64_list)*10}s infinite;
        animation-delay: {i*10}s;
        z-index: -2;
    }}
    """

st.markdown(f"""
    <style>
    /* Slideshow nền */
    {css_images}
    @keyframes fadeinout {{
        0% {{ opacity: 0; }}
        10% {{ opacity: 1; }}
        30% {{ opacity: 1; }}
        40% {{ opacity: 0; }}
        100% {{ opacity: 0; }}
    }}

    .bg-overlay {{
        position: fixed;
        top:0; left:0; right:0; bottom:0;
        background: rgba(255,255,255,0.6);  /* làm mờ background */
        z-index: -1;
    }}

    /* Vintage style */
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

    body, .stApp {{
        font-family: 'Special Elite', cursive !important;
    }}

    .top-title {{
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        margin: 15px auto;
        color: #3b2f2f;
        text-shadow: 1px 1px 3px #f1e1a6;
    }}

    .main-title {{
        font-size: 28px;
        font-weight: 900;
        text-align: center;
        color: #5e3a1e;
        margin-top: 5px;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px #d9c07e;
    }}

    /* Label câu hỏi */
    .stSelectbox label {{
        font-weight: 900 !important;
        font-size: 18px !important;
        color: #2d1b04 !important;
        text-shadow: 1px 1px 1px #f4e1b3;
    }}

    /* Bảng kết quả */
    table.dataframe {{
        width: 100%;
        border-collapse: collapse !important;
        border: 2px solid #5e3a1e !important;
        background: #fffdf5;
        font-size: 15px;
    }}
    table.dataframe thead th {{
        background: #8b5a2b !important;
        color: #fffce8 !important;
        padding: 8px;
        font-weight: bold;
    }}
    table.dataframe tbody td {{
        border: 1.5px solid #8b5a2b !important;
        padding: 6px;
        color: #2d1b04;
    }}
    table.dataframe tbody tr:nth-child(even) td {{
        background: #fdf6e3 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# Render slideshow layers
for i in range(len(img_base64_list)):
    st.markdown(f'<div class="bg-{i}"></div>', unsafe_allow_html=True)
st.markdown('<div class="bg-overlay"></div>', unsafe_allow_html=True)

# ===== Header =====
st.markdown('<div class="top-title">Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🔎 Tra cứu Part number</div>', unsafe_allow_html=True)

# ===== Dropdown 1: Zone (sheet name) =====
zone = st.selectbox("📂 Bạn muốn tra cứu zone nào?", xls.sheet_names, key="zone")
if zone:
    df = load_and_clean(zone)

    # Dropdown 2: A/C
    if "A/C" in df.columns:
        aircrafts = sorted([ac for ac in df["A/C"].dropna().unique().tolist() if ac and ac.upper() != "NAN"])
        aircraft = st.selectbox("✈️ Loại máy bay?", aircrafts, key="aircraft")
    else:
        aircraft = None

    if aircraft:
        df_ac = df[df["A/C"] == aircraft]

        # Dropdown 3: Description
        if "DESCRIPTION" in df_ac.columns:
            desc_list = sorted([d for d in df_ac["DESCRIPTION"].dropna().unique().tolist() if d and d.upper() != "NAN"])
            description = st.selectbox("📑 Bạn muốn tra cứu phần nào?", desc_list, key="desc")
        else:
            description = None

        if description:
            df_desc = df_ac[df_ac["DESCRIPTION"] == description]

            # Dropdown 4: Item
            if "ITEM" in df_desc.columns:
                items = sorted([i for i in df_desc["ITEM"].dropna().unique().tolist() if i and i.upper() != "NAN"])
                if items:
                    item = st.selectbox("🔢 Bạn muốn tra cứu Item nào?", items, key="item")
                    df_desc = df_desc[df_desc["ITEM"] == item]

            # Hiển thị kết quả
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
                st.error("Rất tiếc, không tìm thấy dữ liệu phù hợp.")
