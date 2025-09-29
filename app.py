import streamlit as st
import pandas as pd
import base64
import os
import html

# ------------------ Helpers: load & normalize ------------------
@st.cache_data
def load_and_normalize(excel_path="A787.xlsx"):
    df = pd.read_excel(excel_path, dtype=str)  # đọc mọi thứ thành string để tránh NaN type issues
    # chuẩn hoá tên cột
    cols = [c.strip().upper() for c in df.columns.astype(str)]
    df.columns = cols

    # map một số tên cột thường gặp về tên tiêu chuẩn
    rename_map = {}
    for c in df.columns:
        if any(k in c for k in ["PART NUMBER", "PARTNUMBER", "PARTNO", "P/N", "P N", "PART"]):
            # tránh đổi DESCRIPTION/CATEGORY do chứa chữ PART? (hiếm) — ưu tiên map nếu rõ ràng
            if "DESCRIPTION" not in c and "CATEGORY" not in c:
                rename_map[c] = "PN"
        if any(k in c for k in ["NOTE", "NOTES", "REMARK", "REMARKS", "COMMENT", "GHI CHÚ", "GHI_CHU"]):
            rename_map[c] = "NOTE"
        if any(k in c for k in ["DESCRIPTION", "DESC", "ITEM", "MÔ TẢ"]):
            rename_map[c] = "DESCRIPTION"
        if any(k in c for k in ["CATEGORY", "CAT"]):
            rename_map[c] = "CATEGORY"
        if any(k in c for k in ["A/C", "AC", "AIRCRAFT", "TÀU", "TYPE"]):
            rename_map[c] = "A/C"

    if rename_map:
        df = df.rename(columns=rename_map)

    # đảm bảo các cột cần thiết tồn tại
    for col in ["CATEGORY", "A/C", "DESCRIPTION", "PN", "NOTE"]:
        if col not in df.columns:
            df[col] = ""

    # strip values
    df["CATEGORY"] = df["CATEGORY"].astype(str).str.strip()
    df["A/C"] = df["A/C"].astype(str).str.strip()
    df["DESCRIPTION"] = df["DESCRIPTION"].astype(str).str.strip()
    df["PN"] = df["PN"].astype(str).str.strip()
    df["NOTE"] = df["NOTE"].astype(str).str.strip()

    return df

# load
df = load_and_normalize("A787.xlsx")

# ------------------ Background helper (safe) ------------------
def add_bg_from_local(image_file):
    if not os.path.exists(image_file):
        return  # không bắt buộc
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
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(255,255,255,0.78); /* mờ nền, tăng/giảm % nếu cần */
        z-index: -1;
    }}
    /* ẩn sidebar toggle (nút mũi tên) */
    section[data-testid="stSidebar"] {{display: none !important;}}
    button[kind="header"] {{display: none !important;}}
    </style>
    <div class="overlay"></div>
    """
    st.markdown(css, unsafe_allow_html=True)

add_bg_from_local("airplane.jpg")  # nếu không có file sẽ im lặng

# ------------------ CSS (raw string để tránh SyntaxError) ------------------
st.markdown(r"""
<style>
@keyframes colorchange {
  0% {color: #ef4444;}
  25% {color: #f59e0b;}
  50% {color: #10b981;}
  75% {color: #3b82f6;}
  100% {color: #8b5cf6;}
}
.marquee { width:100%; overflow:hidden; white-space:nowrap; box-sizing:border-box; font-size:36px; font-weight:bold; animation: colorchange 6s infinite; text-align:center; }
.marquee span { display:inline-block; padding-left:100%; animation: marquee 20s linear infinite; }
@keyframes marquee { 0% { transform: translate(0,0);} 100% { transform: translate(-100%,0);} }

.sub-header { font-size:22px; font-weight:bold; text-align:center; margin-bottom:14px; color:#0f172a; }

.footer-text { position:fixed; bottom:12px; left:12px; font-size:26px; font-weight:bold; animation: colorchange 6s infinite; z-index:100; }

.chat-text { font-size:18px; line-height:1.6; margin:6px 0; padding:2px 4px; }

.stSelectbox > div > div { font-size:16px !important; padding:8px !important; }
.stSelectbox [data-baseweb="select"] { border-radius:10px !important; border:2px solid #4a90e2 !important; box-shadow: 0 4px 10px rgba(0,0,0,0.15) !important; }
</style>

<div class="marquee"><span>TỔ BẢO DƯỠNG SỐ 1</span></div>
<div class="sub-header">CHATBOT TRA CỨU PN</div>
<div class="footer-text">PHAN VIỆT THẮNG</div>
""", unsafe_allow_html=True)

# ------------------ Read current state from URL query params ------------------
params = st.experimental_get_query_params()
step = params.get("step", ["category"])[0]  # 'category' | 'aircraft' | 'item' | 'result'
q_cat = params.get("cat", [""])[0]
q_ac = params.get("ac", [""])[0]
q_item = params.get("item", [""])[0]

# ------------------ Function: render deterministic "chat history" from params ------------------
def render_conversation(step, cat, ac, item):
    # deterministic conversation built from URL params (no session_state)
    messages = []
    # initial bot greeting
    messages.append(("Bot", "Xin chào!"))
    # first question (always present)
    messages.append(("Bot", "Bạn muốn tra cứu gì?"))

    if step in ("aircraft", "item", "result") and cat:
        messages.append(("Bạn", cat))
        messages.append(("Bot", "Loại tàu nào?"))

    if step in ("item", "result") and ac:
        messages.append(("Bạn", ac))
        messages.append(("Bot", "Bạn muốn tra cứu Item nào?"))

    if step == "result" and item:
        messages.append(("Bạn", item))
        # results will be shown separately below
    # render
    for sender, text in messages:
        # escape text
        safe = html.escape(text).replace("\n", "<br>")
        if sender == "Bot":
            st.markdown(f"<div class='chat-text'><b>🤖 {sender}:</b> {safe}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-text' style='text-align:right'><b>🧑 {sender}:</b> {safe}</div>", unsafe_allow_html=True)

# Render current deterministic conversation
render_conversation(step, q_cat, q_ac, q_item)

st.markdown("---")

# ------------------ UI FLOW (stateless via query params) ------------------
# RESET button (clears query params -> returns to initial state)
if st.button("🔄 Tra cứu lại từ đầu"):
    st.experimental_set_query_params()  # clear params
    st.experimental_rerun()  # rerun to pick up cleared params

# Step: choose Category
if step == "category":
    categories = sorted(df["CATEGORY"].replace("", pd.NA).dropna().unique().tolist())
    sel = st.selectbox("Chọn Category:", ["-- Chọn --"] + categories, key="sel_cat")
    if sel != "-- Chọn --":
        # update URL -> go to next step
        st.experimental_set_query_params(step="aircraft", cat=sel)
        st.experimental_rerun()

# Step: choose A/C
elif step == "aircraft":
    # guard: if no cat in params, redirect to category
    if not q_cat:
        st.experimental_set_query_params()  # go back to start
        st.experimental_rerun()

    aircrafts = sorted(df[df["CATEGORY"] == q_cat]["A/C"].replace("", pd.NA).dropna().unique().tolist())
    sel = st.selectbox("Chọn loại tàu (A/C):", ["-- Chọn --"] + aircrafts, key="sel_ac")
    if sel != "-- Chọn --":
        st.experimental_set_query_params(step="item", cat=q_cat, ac=sel)
        st.experimental_rerun()

# Step: choose Item (Description)
elif step == "item":
    if not (q_cat and q_ac):
        st.experimental_set_query_params()  # fallback to start
        st.experimental_rerun()

    items = sorted(df[(df["CATEGORY"] == q_cat) & (df["A/C"] == q_ac)]["DESCRIPTION"].replace("", pd.NA).dropna().unique().tolist())
    sel = st.selectbox("Chọn Item (mục cần tra):", ["-- Chọn --"] + items, key="sel_item")
    if sel != "-- Chọn --":
        st.experimental_set_query_params(step="result", cat=q_cat, ac=q_ac, item=sel)
        st.experimental_rerun()

# Step: result
elif step == "result":
    if not (q_cat and q_ac and q_item):
        st.experimental_set_query_params()  # fallback
        st.experimental_rerun()

    # prepare results safely (columns normalized to uppercase)
    # ensure PN & NOTE exist (we normalized earlier)
    try:
        results = df[
            (df["CATEGORY"] == q_cat) &
            (df["A/C"] == q_ac) &
            (df["DESCRIPTION"] == q_item)
        ][["PN", "NOTE"]].copy()
    except KeyError:
        st.error("⚠️ File Excel thiếu cột PN hoặc NOTE (hoặc tên cột khác). Mình đã chuẩn hoá nhưng vẫn không tìm thấy.")
        st.stop()

    if results.empty:
        st.info("Rất tiếc, dữ liệu bạn nhập chưa có.")
    else:
        st.success("Kết quả tra cứu:")
        # show as dataframe (nice)
        st.dataframe(results.reset_index(drop=True), use_container_width=True)

    # show a button to go back to category if user wants to look more
    if st.button("🔙 Tra cứu mục khác"):
        st.experimental_set_query_params()  # clear -> back to category
        st.experimental_rerun()
