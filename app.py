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
    for sender, msg in st.session_state_
