import streamlit as st
import pandas as pd
import time
import html
import base64

# ===================== CONFIG =====================
st.set_page_config(page_title="PN Lookup", layout="centered")

# ===================== BACKGROUND =====================
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{b64}");
        background-size: cover;
        background-position: center;
        position: relative;
    }}
    /* lớp phủ mờ */
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.55); /* chỉnh độ mờ */
        z-index: 0;
    }}
    .stApp > div {{
        position: relative;
        z-index: 1;
    }}
    .chat-bot {{
        background-color: rgba(240, 240, 240, 0.85);
        color: black;
        padding: 10px;
        border-radius: 15px;
        margin: 10px 0;
        max-width: 70%;
    }}
    .chat-user {{
        background-color: rgba(0, 123, 255, 0.85);
        color: white;
        padding: 10px;
        border-radius: 15px;
        margin: 10px 0;
        margin-left: auto;
        max-width: 70%;
    }}
    .title-banner {{
        position: absolute;
        top: 20px;
        width: 100%;
        text-align: center;
        font-size: 38px;
        font-weight: bold;
        color: yellow;
        animation: move 10s linear infinite;
        z-index: 2;
    }}
    @keyframes move {{
        0% {{ transform: translateX(-100%); }}
        100% {{ transform: translateX(100%); }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

add_bg_from_local("airplane.jpg")

# ===================== TIÊU ĐỀ CHẠY =====================
st.markdown('<div class="title-banner">TỔ BẢO DƯỠNG SỐ 1</div>', unsafe_allow_html=True)

# ===================== LOAD DATA =====================
df = pd.read_excel("A787.xlsx")

# ===================== SESSION STATE =====================
if "step" not in st.session_state:
    st.session_state.step = "category"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ===================== CHAT FUNCTIONS =====================
def bot_say(text):
    st.session_state.chat_history.append(("bot", text))

def user_say(text):
    st.session_state.chat_history.append(("user", text))

def render_chat():
    for sender, msg in st.session_state.chat_history:
        if sender == "bot":
            st.markdown(f'<div class="chat-bot">{html.escape(msg).replace("\n", "<br>")}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-user">{html.escape(msg)}</div>', unsafe_allow_html=True)

# ===================== APP LOGIC =====================
st.button("🔄 Tra cứu lại từ đầu", on_click=lambda: [st.session_state.clear(), st.rerun()])

render_chat()

# Bước 1: chọn Category
if st.session_state.step == "category":
    if not st.session_state.chat_history:
        bot_say("Bạn muốn tra cứu gì?")
    category = st.selectbox("Chọn Category", ["-- Chọn Category --"] + sorted(df["CATEGORY"].dropna().unique().tolist()))
    if category != "-- Chọn Category --":
        user_say(category)
        st.session_state.category = category
        st.session_state.step = "aircraft"
        st.rerun()

# Bước 2: chọn loại tàu (A/C)
elif st.session_state.step == "aircraft":
    if ("bot", "Loại tàu nào?") not in st.session_state.chat_history:
        bot_say("Loại tàu nào?")
    aircrafts = df[df["CATEGORY"] == st.session_state.category]["A/C"].dropna().unique()
    aircraft = st.selectbox("Chọn loại tàu", ["-- Chọn A/C --"] + list(aircrafts))
    if aircraft != "-- Chọn A/C --":
        user_say(aircraft)
        st.session_state.aircraft = aircraft
        st.session_state.step = "item"
        st.rerun()

# Bước 3: chọn Item (Description)
elif st.session_state.step == "item":
    if ("bot", "Bạn muốn tra cứu Item nào?") not in st.session_state.chat_history:
        bot_say("Bạn muốn tra cứu Item nào?")
    items = df[
        (df["CATEGORY"] == st.session_state.category)
        & (df["A/C"] == st.session_state.aircraft)
    ]["DESCRIPTION"].dropna().unique()
    item = st.selectbox("Chọn Item", ["-- Chọn Item --"] + list(items))
    if item != "-- Chọn Item --":
        user_say(item)
        st.session_state.item = item
        st.session_state.step = "result"
        st.rerun()

# Bước 4: kết quả PN + Note
elif st.session_state.step == "result":
    result = df[
        (df["CATEGORY"] == st.session_state.category)
        & (df["A/C"] == st.session_state.aircraft)
        & (df["DESCRIPTION"] == st.session_state.item)
    ]

    if not result.empty:
        pn_list = result['PART NUMBER (PN)'].dropna().astype(str).unique().tolist()
        note_list = result['NOTE'].dropna().astype(str).unique().tolist()

        reply = f"✅ PN cho {st.session_state.item}:\n" + "\n".join([f"• {pn}" for pn in pn_list])
        if note_list:
            reply += "\n📌 Ghi chú:\n" + "\n".join([f"- {note}" for note in note_list])

        if ("bot", reply) not in st.session_state.chat_history:
            bot_say(reply)
        render_chat()
    else:
        if ("bot", "Rất tiếc, dữ liệu bạn nhập chưa có.") not in st.session_state.chat_history:
            bot_say("Rất tiếc, dữ liệu bạn nhập chưa có.")
        render_chat()
