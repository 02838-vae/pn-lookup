import streamlit as st
import pandas as pd
import base64

# ===== CSS: Background + Bubble style (nếu cần sau này) =====
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    css = f"""
    <style>
    .stApp {{
      position: relative;
      background: none;
    }}
    .stApp::before {{
      content: "";
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background-image: url("data:image/jpg;base64,{encoded}");
      background-size: cover;
      background-position: center;
      opacity: 0.15;
      z-index: -1;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ===== Page Config =====
st.set_page_config(page_title="Tra cứu PN", page_icon="🔎", layout="centered")

# ===== Gọi hàm thêm background (đảm bảo file airplane.jpg có trong repo) =====
add_bg_from_local("airplane.jpg")

# ===== Load Data =====
df = pd.read_excel("A787.xlsx")
df = df.dropna(subset=["DESCRIPTION", "PART NUMBER (PN)"])

st.title("✈️ Tra cứu Part Number (PN)")

# ===== Step 1: Chọn Category =====
categories = df["CATEGORY"].dropna().unique()
category = st.selectbox("Bạn muốn tra cứu gì?", ["-- Chọn Category --"] + list(categories))

# ===== Step 2: Chỉ hiện khi có Category =====
if category and category != "-- Chọn Category --":
    descriptions = df[df["CATEGORY"] == category]["DESCRIPTION"].dropna().unique()
    description = st.selectbox("Bạn muốn tra cứu Description nào?", ["-- Chọn Description --"] + list(descriptions))

    # ===== Step 3: Chỉ hiện khi có Description =====
    if description and description != "-- Chọn Description --":
        result = df[(df["CATEGORY"] == category) & (df["DESCRIPTION"] == description)]
        if not result.empty:
            pn_text = ", ".join(result['PART NUMBER (PN)'].astype(str))
            st.success(f"✅ PN: {pn_text}")
            if "NOTE" in result.columns:
                notes = result["NOTE"].dropna().astype(str).unique()
                if len(notes) > 0:
                    st.info(f"📌 Ghi chú: {', '.join(notes)}")
        else:
            st.error("Rất tiếc, dữ liệu bạn nhập chưa có")



