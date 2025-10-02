import os
import base64
import random
import pandas as pd
import streamlit as st

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

# ===== Hàm encode ảnh thành base64 =====
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ===== Quét thư mục, lấy tất cả file airplane*.jpg/jpeg/png =====
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

# ===== Inject CSS + JS để tạo slideshow background =====
if img_base64_list:
    images_js = ",".join([f"'data:image/jpg;base64,{img}'" for img in img_base64_list])
    st.markdown(f"""
        <style>
        body, .stApp {{
            margin: 0;
            padding: 0;
            height: 100%;
            width: 100%;
            overflow-x: hidden;
        }}
        #bg {{
            position: fixed;
            top: 0; left: 0;
            width: 100%;
            height: 100%;
            z-index: -2;
        }}
        #bg img {{
            position: absolute;
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0;
            transition: opacity 3s ease-in-out;
        }}
        </style>

        <div id="bg"></div>

        <script>
        const images = [{images_js}];
        let idx = 0;
        const bgDiv = document.getElementById("bg");

        function showImage(i) {{
            let img = document.createElement("img");
            img.src = images[i];
            bgDiv.appendChild(img);
            setTimeout(() => {{
                img.style.opacity = 1;
            }}, 100);

            // Xóa ảnh cũ sau khi fade out
            if (bgDiv.children.length > 1) {{
                let oldImg = bgDiv.children[0];
                oldImg.style.opacity = 0;
                setTimeout(() => {{
                    if (oldImg.parentNode) {{
                        oldImg.parentNode.removeChild(oldImg);
                    }}
                }}, 3000);
            }}
        }}

        showImage(idx);
        setInterval(() => {{
            idx = (idx + 1) % images.length;
            showImage(idx);
        }}, 10000); // đổi ảnh mỗi 10 giây
        </script>
    """, unsafe_allow_html=True)

# ===== CSS khác =====
st.markdown("""
    <style>
    .top-title {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        animation: colorchange 5s infinite alternate;
        margin: 15px auto;
        white-space: nowrap;
    }
    @keyframes colorchange {
        0% {color: #e74c3c;}
        25% {color: #3498db;}
        50% {color: #2ecc71;}
        75% {color: #f1c40f;}
        100% {color: #9b59b6;}
    }
    .main-title {
        font-size: 28px;
        font-weight: 900;
        text-align: center;
        color: #2c3e50;
        margin-top: 5px;
        margin-bottom: 20px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    table.dataframe {
        width: 100%;
        border-collapse: collapse !important;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        background: white;
    }
    table.dataframe thead th {
        background: #2c3e50 !important;
        color: white !important;
        font-weight: bold;
        text-align: center;
        padding: 10px !important;
        font-size: 15px;
        border: 2px solid #2c3e50 !important;
    }
    table.dataframe tbody td {
        text-align: center !important;
        padding: 8px !important;
        font-size: 14px;
        color: #2c3e50;
        border: 1.5px solid #2c3e50 !important;
    }
    .stSelectbox label {
        font-weight: 900 !important;
        font-size: 18px !important;
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ===== Header =====
st.markdown('<div class="top-title">Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🔎 Tra cứu Part number</div>', unsafe_allow_html=True)

# ===== Dropdown 1: Zone (sheet name) =====
zone = st.selectbox("📂 Bạn muốn tra cứu zone nào?", xls.sheet_names, key="zone")
if zone:
    df = load_and_clean(zone)

    # ===== Dropdown 2: A/C =====
    if "A/C" in df.columns:
        aircrafts = sorted([ac for ac in df["A/C"].dropna().unique().tolist() if ac and ac.upper() != "NAN"])
        aircraft = st.selectbox("✈️ Loại máy bay?", aircrafts, key="aircraft")
    else:
        aircraft = None

    if aircraft:
        df_ac = df[df["A/C"] == aircraft]

        # ===== Dropdown 3: Description =====
        if "DESCRIPTION" in df_ac.columns:
            desc_list = sorted([d for d in df_ac["DESCRIPTION"].dropna().unique().tolist() if d and d.upper() != "NAN"])
            description = st.selectbox("📑 Bạn muốn tra cứu phần nào?", desc_list, key="desc")
        else:
            description = None

        if description:
            df_desc = df_ac[df_ac["DESCRIPTION"] == description]

            # Nếu có cột ITEM thì hỏi thêm
            if "ITEM" in df_desc.columns:
                items = sorted([i for i in df_desc["ITEM"].dropna().unique().tolist() if i and i.upper() != "NAN"])
                if items:
                    item = st.selectbox("🔢 Bạn muốn tra cứu Item nào?", items, key="item")
                    df_desc = df_desc[df_desc["ITEM"] == item]

            # Hiển thị kết quả
            if not df_desc.empty:
                df_result = df_desc.copy().reset_index(drop=True)

                # Giữ cột mong muốn
                cols_to_show = ["PART NUMBER (PN)"]
                for alt_col in ["PART INTERCHANGE", "PN INTERCHANGE"]:
                    if alt_col in df_result.columns:
                        cols_to_show.append(alt_col)
                        break
                if "NOTE" in df_result.columns:
                    cols_to_show.append("NOTE")

                df_result = df_result[cols_to_show]

                # Thêm cột STT
                df_result.insert(0, "STT", range(1, len(df_result) + 1))

                st.markdown(
                    f'<div style="font-size:18px;font-weight:bold;color:#154360;background:#d6eaf8;'
                    f'padding:10px 15px;border-left:6px solid #154360;border-radius:6px;'
                    f'margin:15px 0;text-align:center;">✅ Tìm thấy {len(df_result)} dòng dữ liệu</div>',
                    unsafe_allow_html=True
                )
                st.write(df_result.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.error("Rất tiếc, không tìm thấy dữ liệu phù hợp.")

