import pandas as pd
import streamlit as st
import base64
import glob

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

# ===== Load nhiều ảnh background =====
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_files = sorted(
    glob.glob("airplane*.jpg") +
    glob.glob("airplane*.jpeg") +
    glob.glob("airplane*.png")
)

bg_base64_list = [get_base64(f) for f in bg_files]

# ===== Nhúng Google Fonts vintage =====
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Special+Elite&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ===== CSS Slideshow =====
css_images = ""
for i, img64 in enumerate(bg_base64_list):
    delay = i * 10
    css_images += f"""
    .bg-{i} {{
        background-image: url("data:image/jpeg;base64,{img64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        position: fixed;
        top:0; left:0; right:0; bottom:0;
        opacity: 0;
        animation: fadeinout {len(bg_base64_list)*10}s infinite;
        animation-delay: {delay}s;
        z-index: -9999;
    }}
    """

st.markdown(f"""
    <style>
    {css_images}
    @keyframes fadeinout {{
        0% {{ opacity: 0; }}
        10% {{ opacity: 1; }}
        30% {{ opacity: 1; }}
        40% {{ opacity: 0; }}
        100% {{ opacity: 0; }}
    }}

    /* Overlay làm chữ dễ đọc */
    .bg-overlay {{
        position: fixed;
        top:0; left:0; right:0; bottom:0;
        background: rgba(255,255,255,0.65);
        z-index: -9998;
    }}

    /* Font vintage */
    html, body, [class*="css"]  {{
        font-family: 'Special Elite', cursive !important;
    }}

    /* Header */
    .top-title {{
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        animation: colorchange 5s infinite alternate;
        margin: 15px auto;
        white-space: nowrap;
    }}
    @keyframes colorchange {{
        0% {{color: #e74c3c;}}
        25% {{color: #3498db;}}
        50% {{color: #2ecc71;}}
        75% {{color: #f1c40f;}}
        100% {{color: #9b59b6;}}
    }}

    .main-title {{
        font-size: 28px;
        font-weight: 900;
        text-align: center;
        color: #2c3e50;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        white-space: nowrap;
    }}
    </style>
""", unsafe_allow_html=True)

# Render background layers
for i in range(len(bg_base64_list)):
    st.markdown(f'<div class="bg-{i}"></div>', unsafe_allow_html=True)
st.markdown('<div class="bg-overlay"></div>', unsafe_allow_html=True)

# ===== Header =====
st.markdown('<div class="top-title">Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🔎 Tra cứu Part number</div>', unsafe_allow_html=True)

# ===== Dropdown Zone =====
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
                st.dataframe(df_result, use_container_width=True)
            else:
                st.error("Rất tiếc, không tìm thấy dữ liệu phù hợp.")
