import streamlit as st
import pandas as pd
import time
import html
import base64

# ===================== LOAD DATA =====================
df = pd.read_excel("A787.xlsx")

# ===================== BACKGROUND =====================
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    css = f"""
    <style>
    .stApp {{
        background: url(data:image/jpg;base64,{b64});
        background-size: cover;
        background-position: center;
        position: relative;
    }}
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(255, 255, 255, 0.5); /* overlay làm mờ */
        z-index: 0;
    }}
    .stApp > div {{
        position: relative;
        z-index: 1;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

add_bg_from_local("airplane.jpg")

# ===================== MARQUEE TITLE =====================
st.markdown("""
<style>
@keyframes colorchange {
  0%   {color: red;}
  25%  {color: blue;}
  50%  {color: green;}
  75%  {color: orange;}
  100% {color: purple;}
}
.marquee {
  font-size: 32px;
  font-weight: bold;
  animation: colorchange 5s infinite;
  white-space: nowrap;
  overflow: hidden;
  box-sizing: border-box;
}
.marquee span {
  display: inline-block;
  padding-left: 100%;
  animation: marquee 15s linear infinite;
}
@keyframes marquee {
  0%   { transform: translate(0, 0); }
  100% { transform: translate(-100%, 0); }
}
.subtitle {
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  color: #333;
}
.chat-bot {
    background: #e1f5fe;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
    max-width: 80%;
}
.chat-user {
    background: #c8e6c9;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
    text-align: right;
    max-width: 80%;
    margin-left: auto;
}
</style>
<div class="marquee"><span>TỔ BẢO DƯỠNG SỐ 1</span></div>
<div class="subtitle">🤖 CHATBOT TRA CỨU PN</div>
""", unsafe_allow_html=True)

# ===================== SESSION STATE =====================
if "step" not in st.session_state:
    st.session_state.step = "category"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def bot_say(text):
    st.session_state.chat_history.append(("bot", text))

def user_say(text):
    st.session_state.chat_history.append(("user", text))

def render_chat():
    for sender, msg in st.session_state.chat_history:
        if sender == "bot":
            st.markdown(f'<div class="chat-bot">{html.escape(msg).replace("\\n", "<br>")}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-user">{html.escape(msg)}</div>', unsafe_allow_html=True)

def reset_chat():
    st.session_state.clear()
    st.session_state.step = "category"
    st.session_state.chat_history = []

# ===================== UI =====================
render_chat()

st.button("🔄 Tra cứu lại từ đầu", on_click=reset_chat)

# Step 1: chọn Category
if st.session_state.step == "category":
    if not st.session_state.chat_history:
        bot_say("Bạn muốn tra cứu gì?")
    category = st.selectbox("Chọn Category", ["-- Chọn Category --"] + sorted(df["CATEGORY"].dropna().unique().tolist()))
    if category != "-- Chọn Category --":
        if "category" not in st.session_state or st.session_state.category != category:
            user_say(category)
            st.session_state.category = category
            st.session_state.step = "aircraft"
            st.rerun()

# Step 2: chọn A/C
if st.session_state.step == "aircraft" and "category" in st.session_state:
    bot_say("Loại tàu nào?")
    aircrafts = df[df["CATEGORY"] == st.session_state.category]["A/C"].dropna().unique().tolist()
    aircraft = st.selectbox("Chọn A/C", ["-- Chọn A/C --"] + sorted(aircrafts))
    if aircraft != "-- Chọn A/C --":
        if "aircraft" not in st.session_state or st.session_state.aircraft != aircraft:
            user_say(aircraft)
            st.session_state.aircraft = aircraft
            st.session_state.step = "item"
            st.rerun()

# Step 3: chọn Item
if st.session_state.step == "item" and "aircraft" in st.session_state:
    bot_say("Bạn muốn tra cứu Item nào?")
    items = df[(df["CATEGORY"] == st.session_state.category) & (df["A/C"] == st.session_state.aircraft)]["DESCRIPTION"].dropna().unique().tolist()
    item = st.selectbox("Chọn Item", ["-- Chọn Item --"] + sorted(items))
    if item != "-- Chọn Item --":
        if "item" not in st.session_state or st.session_state.item != item:
            user_say(item)
            st.session_state.item = item
            st.session_state.step = "result"
            st.rerun()

# Step 4: hiển thị kết quả
if st.session_state.step == "result" and "item" in st.session_state:
    results = df[
        (df["CATEGORY"] == st.session_state.category) &
        (df["A/C"] == st.session_state.aircraft) &
        (df["DESCRIPTION"] == st.session_state.item)
    ][["PN", "NOTE"]]

    if not results.empty:
        for _, row in results.iterrows():
            bot_say(f"PN: {row['PN']}\nNote: {row['NOTE']}")
    else:
        bot_say("Rất tiếc, dữ liệu bạn nhập chưa có")

    st.session_state.step = "done"
    st.rerun()

# Hiển thị lại hội thoại cuối
render_chat()
