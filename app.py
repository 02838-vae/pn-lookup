import streamlit as st
import pandas as pd
import base64

# ===== CSS: Background + Chat bubble =====
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
    .chat-row {{ display:flex; gap:8px; margin:8px 0; }}
    .chat-user {{
      margin-left:auto;
      max-width:80%;
      padding:10px 14px;
      border-radius:14px;
      background:#0ea5a4;
      color:white;
    }}
    .chat-bot {{
      margin-right:auto;
      max-width:80%;
      padding:10px 14px;
      border-radius:14px;
      background:#f1f5f9;
      color:#0f172a;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ===== Load Data =====
df = pd.read_excel("A787.xlsx")
df = df.dropna(subset=["DESCRIPTION", "PART NUMBER (PN)"])

# ===== Page Config =====
st.set_page_config(page_title="Tra cứu PN", page_icon="🔎", layout="centered")
add_bg_from_local("airplane.jpg")

st.title("✈️ Tra cứu Part Number (PN)")

# ===== Step 1: Chọn Category =====
categories = df["CATEGORY"].dropna().unique()
category = st.selectbox("Bạn muốn tra cứu gì?", ["-- Chọn Category --"] + list(categories))

if category and category != "-- Chọn Category --":
    st.markdown(f'<div class="chat-bot">Bạn đã chọn Category: <b>{category}</b></div>', unsafe_allow_html=True)

    # ===== Step 2: Chọn Description =====
    descriptions = df[df["CATEGORY"] == category]["DESCRIPTION"].dropna().unique()
    description = st.selectbox("Bạn muốn tra cứu Description nào?", ["-- Chọn Description --"] + list(descriptions))

    if description and description != "-- Chọn Description --":
        st.markdown(f'<div class="chat-user">Tôi muốn tra cứu: {description}</div>', unsafe_allow_html=True)

        # ===== Step 3: Trả kết quả PN =====
        result = df[(df["CATEGORY"] == category) & (df["DESCRIPTION"] == description)]
        if not result.empty:
            pn_text = ", ".join(result['PART NUMBER (PN)'].astype(str))
            st.markdown(f'<div class="chat-bot">✅ PN: <b>{pn_text}</b></div>', unsafe_allow_html=True)

            if "NOTE" in result.columns:
                notes = result["NOTE"].dropna().astype(str).unique()
                if len(notes) > 0:
                    st.markdown(f'<div class="chat-bot">📌 Ghi chú: {", ".join(notes)}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="chat-bot">Rất tiếc, dữ liệu bạn nhập chưa có</div>', unsafe_allow_html=True)

