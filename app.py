import streamlit as st
import pandas as pd
import base64

# ===== CSS cho background + chat bubble =====
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    css = f"""
    <style>
    .stApp::before {{
      content: "";
      position: fixed;
      top:0; left:0; right:0; bottom:0;
      background-image: url("data:image/jpg;base64,{encoded}");
      background-size: cover;
      background-position: center;
      opacity: 0.15;
      z-index: -1;
    }}
    .chat-bot {{
      margin-right:auto; max-width:80%;
      padding:10px 14px; border-radius:14px;
      background:#f1f5f9; color:#0f172a; margin-bottom:8px;
    }}
    .chat-user {{
      margin-left:auto; max-width:80%;
      padding:10px 14px; border-radius:14px;
      background:#0ea5a4; color:white; margin-bottom:8px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ===== Page config =====
st.set_page_config(page_title="Tra cứu PN", page_icon="🔎", layout="centered")
add_bg_from_local("airplane.jpg")

st.title("✈️ Chatbot Tra cứu PN")

# ===== Load Data =====
df = pd.read_excel("A787.xlsx")
df = df.dropna(subset=["DESCRIPTION", "PART NUMBER (PN)"])

# ===== Khởi tạo session state =====
if "step" not in st.session_state:
    st.session_state.step = "category"
if "category" not in st.session_state:
    st.session_state.category = None
if "description" not in st.session_state:
    st.session_state.description = None

# ===== Hội thoại =====
st.markdown('<div class="chat-bot">Xin chào! Bạn muốn tra cứu gì?</div>', unsafe_allow_html=True)

# Step 1: chọn Category
if st.session_state.step == "category":
    categories = df["CATEGORY"].dropna().unique()
    category = st.selectbox("Chọn Category:", ["-- Chọn --"] + list(categories))
    if category != "-- Chọn --":
        st.session_state.category = category
        st.session_state.step = "description"
        st.experimental_rerun()

# Step 2: chọn Description
elif st.session_state.step == "description":
    st.markdown(f'<div class="chat-user">{st.session_state.category}</div>', unsafe_allow_html=True)
    st.markdown('<div class="chat-bot">Bạn muốn tra cứu Description nào?</div>', unsafe_allow_html=True)

    descriptions = df[df["CATEGORY"] == st.session_state.category]["DESCRIPTION"].dropna().unique()
    description = st.selectbox("Chọn Description:", ["-- Chọn --"] + list(descriptions))
    if description != "-- Chọn --":
        st.session_state.description = description
        st.session_state.step = "result"
        st.experimental_rerun()

# Step 3: hiển thị kết quả
elif st.session_state.step == "result":
    st.markdown(f'<div class="chat-user">{st.session_state.description}</div>', unsafe_allow_html=True)

    result = df[(df["CATEGORY"] == st.session_state.category) & (df["DESCRIPTION"] == st.session_state.description)]
    if not result.empty:
        pn_text = ", ".join(result['PART NUMBER (PN)'].astype(str))
        reply = f"✅ PN cho {st.session_state.description} là: {pn_text}"
        if "NOTE" in result.columns:
            notes = result["NOTE"].dropna().astype(str).unique()
            if len(notes) > 0:
                reply += f"<br>📌 Ghi chú: {', '.join(notes)}"
        st.markdown(f'<div class="chat-bot">{reply}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="chat-bot">Rất tiếc, dữ liệu bạn nhập chưa có.</div>', unsafe_allow_html=True)

    if st.button("🔄 Bắt đầu lại"):
        st.session_state.clear()
        st.experimental_rerun()
