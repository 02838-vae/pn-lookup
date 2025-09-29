import streamlit as st
import pandas as pd
import base64

# ========== LOAD DATA ==========
@st.cache_data
def load_data():
    df = pd.read_excel("A787.xlsx")
    df.columns = df.columns.str.strip().str.upper()  # Chuẩn hóa tên cột
    return df

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

    /* Ẩn sidebar và nút mũi tên */
    section[data-testid="stSidebar"] {{display: none !important;}}
    button[kind="header"] {{display: none !important;}}
    </style>
    <div class="overlay"></div>
    """
    st.markdown(css, unsafe_allow_html=True)

add_bg_from_local("airplane.jpg")

# ========== CSS DECORATION ==========
st.markdown("""
<style>
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
  font-size: 26px;
  font-weight: bold;
  animation: colorchange 6s infinite;
  z-index: 100;
}

.chat-text {
  font-size: 20px;
  line-height: 1.6;
  margin: 5px 0;
}

.stSelectbox > div > div {
    font-size: 18px !important;
    padding: 8px !important;
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

# ========== URL STATE ==========
params = st.query_params
step = params.get("step", "category")
q_cat = params.get("cat", "")
q_ac = params.get("ac", "")
q_item = params.get("item", "")

# ========== APP LOGIC ==========
if step == "category":
    st.markdown("<div class='chat-text'><b>Bot:</b> Bạn muốn tra cứu Category nào?</div>", unsafe_allow_html=True)
    sel = st.selectbox("Chọn Category:", df["CATEGORY"].dropna().unique())
    if sel:
        st.query_params.clear()
        st.query_params["step"] = "aircraft"
        st.query_params["cat"] = sel
        st.rerun()

elif step == "aircraft":
    st.markdown("<div class='chat-text'><b>Bot:</b> Loại tàu nào?</div>", unsafe_allow_html=True)
    aircrafts = df[df["CATEGORY"] == q_cat]["A/C"].dropna().unique()
    sel = st.selectbox("Chọn loại tàu:", aircrafts)
    if sel:
        st.query_params.clear()
        st.query_params["step"] = "item"
        st.query_params["cat"] = q_cat
        st.query_params["ac"] = sel
        st.rerun()

elif step == "item":
    st.markdown("<div class='chat-text'><b>Bot:</b> Bạn muốn tra cứu Item nào?</div>", unsafe_allow_html=True)
    items = df[
        (df["CATEGORY"] == q_cat) &
        (df["A/C"] == q_ac)
    ]["DESCRIPTION"].dropna().unique()
    sel = st.selectbox("Chọn Item:", items)
    if sel:
        st.query_params.clear()
        st.query_params["step"] = "result"
        st.query_params["cat"] = q_cat
        st.query_params["ac"] = q_ac
        st.query_params["item"] = sel
        st.rerun()

elif step == "result":
    results = df[
        (df["CATEGORY"] == q_cat) &
        (df["A/C"] == q_ac) &
        (df["DESCRIPTION"] == q_item)
    ][["PN", "NOTE"]]

    if results.empty:
        st.markdown("<div class='chat-text'><b>Bot:</b> Rất tiếc, dữ liệu bạn nhập chưa có.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='chat-text'><b>Bot:</b> Kết quả tra cứu:</div>", unsafe_allow_html=True)
        st.dataframe(results, use_container_width=True)

# ========== RESET ==========
if st.button("🔄 Tra cứu lại từ đầu"):
    st.query_params.clear()
    st.rerun()
