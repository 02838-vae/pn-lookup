import streamlit as st
import pandas as pd
import base64

# ========== LOAD DATA ==========
@st.cache_data
def load_data():
    return pd.read_excel("A787.xlsx")

df = load_data()

# ========== BACKGROUND ==========
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    css = f"""
    <style>
    .stApp {{
        background: url("data:image/png;base64,{b64}") no-repeat center center fixed;
        background-size: cover;
    }}
    .overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.75); /* làm mờ */
        z-index: -1;
    }}
    </style>
    <div class="overlay"></div>
    """
    st.markdown(css, unsafe_allow_html=True)

add_bg_from_local("airplane.jpg")

# ========== CSS DECORATION ==========
st.markdown("""
<style>
/* ================= MARQUEE HEADER ================= */
@keyframes colorchange {
  0% {color: red;}
  25% {color: orange;}
  50% {color: green;}
  75% {color: blue;}
  100% {color: red;}
}

.marquee {
  width: 100%;
  overflow: hidden;
  white-space: nowrap;
  box-sizing: border-box;
  animation: colorchange 6s infinite;
  font-size: 36px;
  font-weight: bold;
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

/* ================= SUB HEADER ================= */
.sub-header {
  font-size: 22px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
}

/* ================= FOOTER ================= */
.footer-text {
  position: fixed;
  bottom: 10px;
  left: 10px;
  font-size: 20px; /* to hơn */
  font-weight: bold;
  animation: colorchange 6s infinite;
  z-index: 100;
}

/* ================= CHAT FONT ================= */
.chat-text {
  font-size: 18px;
  line-height: 1.6;
  margin: 5px 0;
}

/* ================= DROPDOWN STYLE ================= */
.stSelectbox > div > div {
    font-size: 16px !important;
    padding: 6px !important;
}
.stSelectbox [data-baseweb="select"] {
    border-radius: 10px !important;
    border: 2px solid #4a90e2 !important;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.2) !important;
}
</style>

<div class="marquee"><span>TỔ BẢO DƯỠNG SỐ 1</span></div>
<div class="sub-header">CHATBOT TRA CỨU PN</div>
<div class="footer-text">PHAN VIỆT THẮNG</div>
""", unsafe_allow_html=True)

# ========== INIT SESSION ==========
if "history" not in st.session_state:
    st.session_state.history = []
if "category" not in st.session_state:
    st.session_state.category = None
if "aircraft" not in st.session_state:
    st.session_state.aircraft = None
if "item" not in st.session_state:
    st.session_state.item = None

# ========== RESET FUNCTION ==========
def reset_chat():
    st.session_state.history = []
    st.session_state.category = None
    st.session_state.aircraft = None
    st.session_state.item = None

# ========== CHATBOT LOGIC ==========
# Hỏi CATEGORY
if st.session_state.category is None:
    st.session_state.history.append(("Bot", "Bạn muốn tra cứu Category nào?"))
    category = st.selectbox("Chọn Category:", df["CATEGORY"].dropna().unique())
    if category:
        st.session_state.category = category
        st.session_state.history.append(("User", category))
        st.rerun()

# Hỏi A/C
elif st.session_state.aircraft is None:
    st.session_state.history.append(("Bot", "Loại tàu nào?"))
    aircrafts = df[df["CATEGORY"] == st.session_state.category]["A/C"].dropna().unique()
    aircraft = st.selectbox("Chọn loại tàu:", aircrafts)
    if aircraft:
        st.session_state.aircraft = aircraft
        st.session_state.history.append(("User", aircraft))
        st.rerun()

# Hỏi Item
elif st.session_state.item is None:
    st.session_state.history.append(("Bot", "Bạn muốn tra cứu Item nào?"))
    items = df[
        (df["CATEGORY"] == st.session_state.category) &
        (df["A/C"] == st.session_state.aircraft)
    ]["DESCRIPTION"].dropna().unique()
    item = st.selectbox("Chọn Item:", items)
    if item:
        st.session_state.item = item
        st.session_state.history.append(("User", item))
        st.rerun()

# Hiển thị kết quả
else:
    results = df[
        (df["CATEGORY"] == st.session_state.category) &
        (df["A/C"] == st.session_state.aircraft) &
        (df["DESCRIPTION"] == st.session_state.item)
    ][["PN", "NOTE"]]

    st.session_state.history.append(("Bot", f"Kết quả tra cứu:\n{results.to_string(index=False)}"))

# ========== HIỂN THỊ HỘI THOẠI ==========
st.markdown("---")
st.subheader("📜 Lịch sử hội thoại")
for sender, msg in st.session_state.history:
    st.markdown(f"<div class='chat-text'><b>{sender}:</b> {msg}</div>", unsafe_allow_html=True)

# Nút reset
st.button("🔄 Tra cứu lại từ đầu", on_click=reset_chat)
