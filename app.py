import streamlit as st
import pandas as pd
import base64

# ===================== CONFIG =====================
st.set_page_config(page_title="PN Lookup", layout="wide")

# ===================== BACKGROUND =====================
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    css = f"""
    <style>
    .stApp {{
        background: url("data:image/jpg;base64,{b64}") no-repeat center fixed;
        background-size: cover;
    }}
    .overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.6); /* mờ nền */
        z-index: -1;
    }}
    </style>
    <div class="overlay"></div>
    """
    st.markdown(css, unsafe_allow_html=True)

add_bg_from_local("airplane.jpg")

# ===================== CSS DECOR =====================
st.markdown("""
<style>
@keyframes colorchange {
  0% {color: red;}
  25% {color: orange;}
  50% {color: green;}
  75% {color: blue;}
  100% {color: red;}
}

.header-text {
  font-size: 32px;
  font-weight: bold;
  text-align: center;
  animation: colorchange 6s infinite;
}

.sub-header {
  font-size: 22px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
}

.footer-text {
  position: fixed;
  bottom: 10px;
  left: 10px;
  font-size: 14px;
  font-weight: bold;
  animation: colorchange 6s infinite;
  z-index: 100;
}
</style>
<div class="header-text">TỔ BẢO DƯỠNG SỐ 1</div>
<div class="sub-header">CHATBOT TRA CỨU PN</div>
<div class="footer-text">PHAN VIỆT THẮNG</div>
""", unsafe_allow_html=True)

# ===================== DATA =====================
@st.cache_data
def load_data():
    df = pd.read_excel("A787.xlsx")

    # Chuẩn hóa tên cột: bỏ khoảng trắng, đổi về chữ hoa
    df.columns = df.columns.str.strip().str.upper()

    # Đảm bảo các cột cần thiết luôn tồn tại
    for col in ["PN", "NOTE", "CATEGORY", "A/C", "DESCRIPTION"]:
        if col not in df.columns:
            df[col] = ""

    return df

df = load_data()

# ===================== SESSION STATE =====================
if "history" not in st.session_state:
    st.session_state.history = []
if "step" not in st.session_state:
    st.session_state.step = "category"
if "category" not in st.session_state:
    st.session_state.category = None
if "aircraft" not in st.session_state:
    st.session_state.aircraft = None
if "item" not in st.session_state:
    st.session_state.item = None

# ===================== CHAT FUNCTIONS =====================
def bot_say(msg):
    st.session_state.history.append(("🤖 Bot", msg))

def user_say(msg):
    st.session_state.history.append(("🧑 Bạn", msg))

# ===================== MAIN FLOW =====================
# Step 1: chọn Category
if st.session_state.step == "category":
    category = st.selectbox("Bạn muốn tra cứu gì?", [""] + sorted(df["CATEGORY"].dropna().unique().tolist()))
    if category:
        user_say(category)
        st.session_state.category = category
        st.session_state.step = "aircraft"
        st.rerun()

# Step 2: chọn A/C
elif st.session_state.step == "aircraft":
    ac = st.selectbox("Loại tàu nào?", [""] + sorted(df["A/C"].dropna().unique().tolist()))
    if ac:
        user_say(ac)
        st.session_state.aircraft = ac
        st.session_state.step = "item"
        st.rerun()

# Step 3: chọn Item
elif st.session_state.step == "item":
    items = df[
        (df["CATEGORY"] == st.session_state.category) &
        (df["A/C"] == st.session_state.aircraft)
    ]["DESCRIPTION"].dropna().unique().tolist()

    item = st.selectbox("Bạn muốn tra cứu Item nào?", [""] + sorted(items))
    if item:
        user_say(item)
        st.session_state.item = item
        st.session_state.step = "result"
        st.rerun()

# Step 4: hiển thị kết quả
elif st.session_state.step == "result":
    results = df[
        (df["CATEGORY"] == st.session_state.category) &
        (df["A/C"] == st.session_state.aircraft) &
        (df["DESCRIPTION"] == st.session_state.item)
    ][["PN", "NOTE"]]

    if not results.empty:
        for _, row in results.iterrows():
            pn = row["PN"] if pd.notna(row["PN"]) else "—"
            note = row["NOTE"] if pd.notna(row["NOTE"]) else "—"
            bot_say(f"PN: {pn}\nNote: {note}")
    else:
        bot_say("Rất tiếc, dữ liệu bạn nhập chưa có.")

    st.session_state.step = "done"

# ===================== HIỂN THỊ LỊCH SỬ CHAT =====================
for sender, msg in st.session_state.history:
    st.markdown(f"**{sender}:** {msg}")

# ===================== RESET BUTTON =====================
if st.button("🔄 Tra cứu lại từ đầu"):
    for key in ["history", "step", "category", "aircraft", "item"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
