import streamlit as st
import pandas as pd
import base64
import os
import time

# ===== CSS: Background + Chat bubble + Animation + Gradient Banner =====
def add_bg_from_local(image_file):
    if not os.path.exists(image_file):
        st.warning("⚠️ Không tìm thấy file background, sẽ dùng màu nền trắng.")
        return
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    css = f"""
    <style>
    .stApp {{
      background: none;
    }}
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
    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(10px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    .chat-bot {{
      margin-right:auto; max-width:80%;
      padding:10px 14px; border-radius:14px;
      background:#f1f5f9; color:#0f172a; margin-bottom:8px;
      animation: fadeIn 0.6s ease-out;
    }}
    .chat-user {{
      margin-left:auto; max-width:80%;
      padding:10px 14px; border-radius:14px;
      background:#0ea5a4; color:white; margin-bottom:8px;
      animation: fadeIn 0.6s ease-out;
    }}
    .marquee {{
      width: 100%;
      overflow: hidden;
      white-space: nowrap;
      box-sizing: border-box;
      animation: marquee 12s linear infinite;
      font-size: 28px;
      font-weight: bold;
      background: linear-gradient(90deg, #ef4444, #f59e0b, #10b981, #3b82f6, #8b5cf6);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      text-shadow: 1px 1px 2px rgba(255,255,255,0.3);
      margin-bottom: 15px;
    }}
    @keyframes marquee {{
      0%   {{ transform: translateX(100%); }}
      100% {{ transform: translateX(-100%); }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ===== Typing Effect cho bot =====
import html

def bot_say(text):
    placeholder = st.empty()
    full_text = ""
    for char in text:
        full_text += char
        # Escape HTML để tránh lỗi <b< ... >
        safe_text = html.escape(full_text).replace("\n", "<br>")
        placeholder.markdown(f'<div class="chat-bot">{safe_text}</div>', unsafe_allow_html=True)
        time.sleep(0.02)
    return placeholder

# ===== Page config =====
st.set_page_config(page_title="Tra cứu PN", page_icon="🔎", layout="centered")

# ===== Thêm background =====
add_bg_from_local("airplane.jpg")

# ===== Banner chạy chữ =====
st.markdown('<div class="marquee">✈️ TỔ BẢO DƯỠNG SỐ 1 ✈️</div>', unsafe_allow_html=True)

st.title("🔎 Chatbot Tra cứu PN")

# ===== Load Data =====
df = pd.read_excel("A787.xlsx")
df = df.dropna(subset=["DESCRIPTION", "PART NUMBER (PN)"])

# ===== Khởi tạo session state =====
if "step" not in st.session_state:
    st.session_state.step = "category"
if "category" not in st.session_state:
    st.session_state.category = None
if "aircraft" not in st.session_state:
    st.session_state.aircraft = None
if "description" not in st.session_state:
    st.session_state.description = None

# ===== Hội thoại =====
bot_say("Xin chào! Bạn muốn tra cứu gì?")

# Step 1: chọn Category
if st.session_state.step == "category":
    categories = df["CATEGORY"].dropna().unique()
    category = st.selectbox("Chọn Category:", ["-- Chọn --"] + list(categories), key="cat_select")
    if category != "-- Chọn --":
        st.session_state.category = category
        st.session_state.step = "aircraft"

# Step 2: chọn Loại tàu (A/C)
if st.session_state.step == "aircraft" and st.session_state.category:
    st.markdown(f'<div class="chat-user">{st.session_state.category}</div>', unsafe_allow_html=True)
    bot_say("Loại tàu nào?")

    aircrafts = df[df["CATEGORY"] == st.session_state.category]["A/C"].dropna().unique()
    aircraft = st.selectbox("Chọn A/C:", ["-- Chọn --"] + list(aircrafts), key="ac_select")
    if aircraft != "-- Chọn --":
        st.session_state.aircraft = aircraft
        st.session_state.step = "description"

# Step 3: chọn Item (Description)
if st.session_state.step == "description" and st.session_state.aircraft:
    st.markdown(f'<div class="chat-user">{st.session_state.aircraft}</div>', unsafe_allow_html=True)
    bot_say("Bạn muốn tra cứu Item nào?")

    descriptions = df[(df["CATEGORY"] == st.session_state.category) & (df["A/C"] == st.session_state.aircraft)]["DESCRIPTION"].dropna().unique()
    description = st.selectbox("Chọn Item:", ["-- Chọn --"] + list(descriptions), key="desc_select")
    if description != "-- Chọn --":
        st.session_state.description = description
        st.session_state.step = "result"

# Step 4: hiển thị kết quả
if st.session_state.step == "result" and st.session_state.description:
    st.markdown(f'<div class="chat-user">{st.session_state.description}</div>', unsafe_allow_html=True)

    result = df[(df["CATEGORY"] == st.session_state.category) &
                (df["A/C"] == st.session_state.aircraft) &
                (df["DESCRIPTION"] == st.session_state.description)]
    if not result.empty:
        pn_list = result['PART NUMBER (PN)'].astype(str).tolist()
        note_list = []
        if "NOTE" in result.columns:
            note_list = result["NOTE"].dropna().astype(str).tolist()

        reply = f"✅ PN cho {st.session_state.description}:\n" + "\n".join([f"• {pn}" for pn in pn_list])
        if note_list:
            reply += "\n📌 Ghi chú:\n" + "\n".join([f"- {note}" for note in note_list])

        # chuyển \n thành <br> để hiển thị đẹp
        bot_say(reply.replace("\n", "<br>"))
    else:
        bot_say("Rất tiếc, dữ liệu bạn nhập chưa có.")

    if st.button("🔄 Bắt đầu lại"):
        st.session_state.clear()
        st.rerun()

