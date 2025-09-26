import streamlit as st
import pandas as pd
import base64

# ===== CSS: Background + Chat bubble =====
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
    .chat-user {{
      margin-left:auto; max-width:80%;
      padding:10px 14px; border-radius:14px;
      background:#0ea5a4; color:white; margin-bottom:8px;
    }}
    .chat-bot {{
      margin-right:auto; max-width:80%;
      padding:10px 14px; border-radius:14px;
      background:#f1f5f9; color:#0f172a; margin-bottom:8px;
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

st.title("✈️ Chatbot tra cứu PN")

# ===== Reset button =====
if st.button("🔄 Bắt đầu lại"):
    st.session_state.clear()
    st.experimental_rerun()

# ===== Session State cho hội thoại =====
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "text": "Xin chào! Bạn muốn tra cứu gì? (vd: Overhead, Lavatory...)"}
    ]
if "step" not in st.session_state:
    st.session_state.step = "category"
if "category" not in st.session_state:
    st.session_state.category = None

# ===== Hiển thị hội thoại =====
for msg in st.session_state.messages:
    role_class = "chat-user" if msg["role"] == "user" else "chat-bot"
    st.markdown(f'<div class="{role_class}">{msg["text"]}</div>', unsafe_allow_html=True)

# ===== Ô nhập chat =====
user_input = st.text_input("Nhập tin nhắn:", key="input")

if user_input:
    # Thêm tin nhắn user
    st.session_state.messages.append({"role": "user", "text": user_input})

    if st.session_state.step == "category":
        cats = df["CATEGORY"].dropna().unique()
        if user_input in cats:
            st.session_state.category = user_input
            st.session_state.step = "description"
            st.session_state.messages.append(
                {"role": "bot", "text": f"Bạn đã chọn Category {user_input}. Hãy nhập Description muốn tra cứu:"}
            )
        else:
            st.session_state.messages.append(
                {"role": "bot", "text": "Rất tiếc, Category không hợp lệ. Hãy thử Overhead, Lavatory..."}
            )

    elif st.session_state.step == "description":
        descs = df[df["CATEGORY"] == st.session_state.category]["DESCRIPTION"].dropna().unique()
        if user_input in descs:
            result = df[(df["CATEGORY"] == st.session_state.category) & (df["DESCRIPTION"] == user_input)]
            if not result.empty:
                pn_text = ", ".join(result['PART NUMBER (PN)'].astype(str))
                reply = f"✅ PN cho {user_input} là: {pn_text}"
                if "NOTE" in result.columns:
                    notes = result["NOTE"].dropna().astype(str).unique()
                    if len(notes) > 0:
                        reply += f"\n📌 Ghi chú: {', '.join(notes)}"
                st.session_state.messages.append({"role": "bot", "text": reply})
            else:
                st.session_state.messages.append({"role": "bot", "text": "Rất tiếc, dữ liệu bạn nhập chưa có"})
            st.session_state.step = "done"
        else:
            st.session_state.messages.append({"role": "bot", "text": "Description không hợp lệ, vui lòng thử lại."})

    st.experimental_rerun()


