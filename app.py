import streamlit as st
import pandas as pd
from pathlib import Path

# ---------- CÀI ĐẶT ----------
st.set_page_config(page_title="PN Lookup Chat", layout="centered")

# Đường dẫn file (file airplane.jpg và A787.xlsx phải nằm cùng thư mục với app.py)
DATA_FILE = "A787.xlsx"
BG_IMAGE = "airplane.jpg"  # thay tên nếu bạn dùng tên khác

# ---------- CSS: background mờ + chat style ----------
def local_css_background(image_file: str, opacity: float = 0.12):
    """
    Thêm ảnh nền mờ cho toàn app bằng CSS ::before.
    opacity: 0..1 (0 là trong suốt, 1 là đậm)
    """
    # Convert to path for streamlit cloud (relative path works)
    css = f"""
    <style>
    .stApp {{
      position: relative;
      overflow: visible;
    }}
    .stApp::before {{
      content: "";
      position: absolute;
      inset: 0;
      background-image: url('{image_file}');
      background-size: cover;
      background-position: center;
      opacity: {opacity};
      z-index: -1;
      filter: blur(0px);
    }}
    /* Chat bubbles */
    .chat-row {{ display:flex; gap:8px; margin:8px 0; }}
    .chat-user {{ margin-left:auto; max-width:80%; padding:10px 14px; border-radius:14px; background:#0ea5a4; color:white; }}
    .chat-bot  {{ margin-right:auto; max-width:80%; padding:10px 14px; border-radius:14px; background:#f1f5f9; color:#0f172a; }}
    .muted {{"color: #6b7280; font-size:12px;"}}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ---------- Load Data ----------
@st.cache_data
def load_data(path):
    df = pd.read_excel(path)
    # Chuẩn hoá tên cột để dễ dùng
    df = df.rename(columns={c: c.strip() for c in df.columns})
    # Loại bỏ dòng rỗng
    if "DESCRIPTION" in df.columns and "PART NUMBER (PN)" in df.columns:
        df = df.dropna(subset=["DESCRIPTION", "PART NUMBER (PN)"])
    return df

# ---------- Helper: show chat message ----------
def show_bot(msg):
    st.markdown(f"<div class='chat-row'><div class='chat-bot'>{msg}</div></div>", unsafe_allow_html=True)

def show_user(msg):
    st.markdown(f"<div class='chat-row'><div class='chat-user'>{msg}</div></div>", unsafe_allow_html=True)

# ---------- Init session state ----------
if "step" not in st.session_state:
    st.session_state.step = 0   # 0 = start, 1 = category chosen, 2 = description chosen & show result
if "category" not in st.session_state:
    st.session_state.category = None
if "description" not in st.session_state:
    st.session_state.description = None
if "messages" not in st.session_state:
    st.session_state.messages = []  # list of tuples ("bot"|"user", text)

# ---------- Apply background CSS ----------
# If file exists locally, use it; else fallback to nothing (or a remote url)
if Path(BG_IMAGE).exists():
    local_css_background(BG_IMAGE, opacity=0.12)
else:
    # If background image not present, still inject minimal CSS for chat bubbles
    st.markdown(
        """
        <style>
        .chat-row { display:flex; gap:8px; margin:8px 0; }
        .chat-user { margin-left:auto; max-width:80%; padding:10px 14px; border-radius:14px; background:#0ea5a4; color:white; }
        .chat-bot  { margin-right:auto; max-width:80%; padding:10px 14px; border-radius:14px; background:#f1f5f9; color:#0f172a; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---------- App layout ----------
st.title("🔎 Chat PN Lookup")
st.write("Giao diện kiểu hội thoại — chọn từng bước để tra cứu Part Number (PN).")

# Load data (file must be in repo)
try:
    df = load_data(DATA_FILE)
except Exception as e:
    st.error(f"Không thể đọc file dữ liệu `{DATA_FILE}`. Vui lòng kiểm tra file có trong repo. Lỗi: {e}")
    st.stop()

# Lấy danh sách category (unique non-null)
if "CATEGORY" not in df.columns:
    st.error("Dữ liệu không có cột 'CATEGORY'. Vui lòng thêm cột Category vào file Excel.")
    st.stop()

categories = [str(x).strip() for x in df["CATEGORY"].dropna().unique()]

# ---------- Show chat history ----------
for who, text in st.session_state.messages:
    if who == "bot":
        show_bot(text)
    else:
        show_user(text)

# ---------- Step UI ----------
# Step 0: show only Category select + confirm button
if st.session_state.step == 0:
    show_bot("Bạn muốn tra cứu gì? (Chọn Category)")
    col1, col2 = st.columns([3,1])
    with col1:
        selected_cat = st.selectbox("Chọn Category", ["-- Chọn --"] + categories, index=0, key="sel_cat")
    with col2:
        if st.button("Chọn", key="btn_choose_cat"):
            if selected_cat and selected_cat != "-- Chọn --":
                st.session_state.category = selected_cat
                st.session_state.messages.append(("user", selected_cat))
                st.session_state.messages.append(("bot", f"Đã chọn *{selected_cat}*. Bạn muốn tra cứu Description nào?"))
                st.session_state.step = 1
                st.experimental_rerun()
            else:
                st.warning("Vui lòng chọn một Category hợp lệ.")

# Step 1: show Description select + confirm + back
elif st.session_state.step == 1:
    # Back button
    back_col, title_col = st.columns([1,9])
    with back_col:
        if st.button("← Back", key="btn_back_to_cat"):
            st.session_state.step = 0
            # remove last messages related to category
            if st.session_state.messages and st.session_state.messages[-1][0] == "bot":
                st.session_state.messages.pop()
            if st.session_state.messages and st.session_state.messages[-1][0] == "user":
                st.session_state.messages.pop()
            st.experimental_rerun()
    with title_col:
        st.markdown(f"**Category:** {st.session_state.category}")

    # Get descriptions for this category
    descs = df[df["CATEGORY"].astype(str).str.strip() == st.session_state.category]["DESCRIPTION"].dropna().astype(str).unique().tolist()
    if not descs:
        st.info("Không có Description trong category này.")
    else:
        show_bot("Bạn muốn tra cứu Description nào?")

        col1, col2 = st.columns([3,1])
        with col1:
            selected_desc = st.selectbox("Chọn Description", ["-- Chọn --"] + descs, key="sel_desc")
        with col2:
            if st.button("Tra cứu", key="btn_choose_desc"):
                if selected_desc and selected_desc != "-- Chọn --":
                    st.session_state.description = selected_desc
                    st.session_state.messages.append(("user", selected_desc))
                    st.session_state.step = 2
                    st.experimental_rerun()
                else:
                    st.warning("Vui lòng chọn Description hợp lệ.")

# Step 2: show result, allow restart or back to descriptions
elif st.session_state.step == 2:
    # Top controls
    c_back, c_restart = st.columns([1,1])
    with c_back:
        if st.button("← Back to Descriptions", key="btn_back_desc"):
            # remove last user message (description)
            if st.session_state.messages and st.session_state.messages[-1][0] == "user":
                st.session_state.messages.pop()
            # re-add bot prompt for descriptions
            st.session_state.messages.append(("bot", "Bạn muốn tra cứu Description nào?"))
            st.session_state.step = 1
            st.experimental_rerun()
    with c_restart:
        if st.button("Start Over", key="btn_restart"):
            st.session_state.step = 0
            st.session_state.category = None
            st.session_state.description = None
            st.session_state.messages = []
            st.experimental_rerun()

    st.markdown(f"**Category:** {st.session_state.category}  \n**Description:** {st.session_state.description}")

    # Find PN
    result = df[
        (df["CATEGORY"].astype(str).str.strip() == st.session_state.category) &
        (df["DESCRIPTION"].astype(str).str.strip() == st.session_state.description)
    ]

    if not result.empty:
        pn_list = result["PART NUMBER (PN)"].dropna().astype(str).unique().tolist()
        notes = result["NOTE"].dropna().astype(str).unique().tolist() if "NOTE" in result.columns else []
        show_bot("Kết quả tìm được:")
        st.markdown(f"<div class='chat-row'><div class='chat-bot'><strong>✅ PN:</strong> {', '.join(pn_list)}</div></div>", unsafe_allow_html=True)
        if notes:
            st.markdown(f"<div class='chat-row'><div class='chat-bot'><strong>📌 Ghi chú:</strong> {', '.join(notes)}</div></div>", unsafe_allow_html=True)
    else:
        show_bot("Rất tiếc, dữ liệu bạn nhập chưa có")

# ---------- Footer hint ----------
st.write("")
st.markdown("<div class='muted'>Ghi chú: Để background hiển thị, hãy upload file ảnh (ví dụ airplane.jpg) vào cùng thư mục repo.</div>", unsafe_allow_html=True)
