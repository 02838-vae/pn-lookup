import streamlit as st
import pandas as pd
import base64
import os

# --- CẤU HÌNH BAN ĐẦU ---
st.set_page_config(page_title="Tổ Bảo Dưỡng Số 1 - Tra Cứu PN", layout="wide")

# --- HÀM HỖ TRỢ ---
def get_base64_encoded_file(file_path):
    """Đọc file và trả về base64 encoded string."""
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return ""
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def load_and_clean(excel_file, sheet):
    try:
        df = pd.read_excel(excel_file, sheet_name=sheet)
        df.columns = df.columns.str.strip().str.upper()
        df = df.replace(r'^\s*$', pd.NA, regex=True).dropna(how="all")
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].fillna("").astype(str).str.strip()
        return df
    except Exception:
        return pd.DataFrame()

# --- ẢNH NỀN (chú ý: tên file đúng là PN_MOBILE.jpg) ---
bg_pc_base64 = get_base64_encoded_file("PN_PC.jpg")
bg_mobile_base64 = get_base64_encoded_file("PN_mobile.jpg")

# --- CSS CHÍNH (tăng size title, đổi màu subtitle) ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');

#MainMenu, footer, header {{visibility: hidden;}}
div.block-container {{padding-top: 20px;}}

/* Gắn background lên container chính để tránh bị override */
.stAppViewContainer, .st-emotion-cache-1r6slb0 {{
    background: url("data:image/jpeg;base64,{bg_pc_base64}") no-repeat center center fixed !important;
    background-size: cover !important;
    font-family: 'Oswald', sans-serif !important;
}}

/* Hiệu ứng chữ */
@keyframes scrollText {{
  0% {{ transform: translateX(100vw); }}
  100% {{ transform: translateX(-100%); }}
}}
@keyframes colorShift {{
  0% {{ background-position: 0% 50%; }}
  50% {{ background-position: 100% 50%; }}
  100% {{ background-position: 0% 50%; }}
}}

/* TIÊU ĐỀ CHÍNH (PC) - Tăng kích cỡ */
#main-animated-title-container {{
  width: 100%;
  height: 90px;
  overflow: hidden;
  text-align: center;
  margin-top: 30px;
}}
#main-animated-title-container h1 {{
  font-family: 'Oswald', sans-serif;
  font-size: 5rem;                 /* Tăng to hơn */
  font-weight: 700;
  letter-spacing: 6px;
  text-transform: uppercase;
  display: inline-block;
  background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3);
  background-size: 400% 400%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: colorShift 10s ease infinite, scrollText 18s linear infinite;
  text-shadow: 2px 2px 8px rgba(0,0,0,0.65);
}

/* TIÊU ĐỀ PHỤ - màu vàng sáng, shadow dày để nổi trên nền */
#sub-static-title h2 {{
  font-family: 'Playfair Display', serif;
  font-size: 2.4rem;
  color: #FFD54F;                  /* vàng sáng (đỡ lẫn với nền xanh nước biển) */
  text-align: center;
  text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
  margin: 12px 0 22px 0;
}}

/* MOBILE */
@media (max-width: 768px) {{
  .stAppViewContainer, .st-emotion-cache-1r6slb0 {{
    background: url("data:image/jpeg;base64,{bg_mobile_base64}") no-repeat center center scroll !important;
    background-size: cover !important;
  }}

  #main-animated-title-container {{
    margin-top: 110px !important;   /* vẫn đảm bảo không bị che; có thể điều chỉnh nhỏ nếu cần */
    overflow: hidden;
    height: auto;
    white-space: nowrap;
  }}

  #main-animated-title-container h1 {{
    font-size: 9.5vw;                /* tăng chút so với trước, nhưng vẫn an toàn với margin-top */
    line-height: 1.15;
    letter-spacing: 3px;
    display: inline-block;
    white-space: nowrap;
    animation: colorShift 10s ease infinite, scrollText 15s linear infinite;
    text-shadow: 2px 2px 6px rgba(0,0,0,0.75);
  }}

  #sub-static-title h2 {{
    font-size: 5.2vw;
    color: #FFD54F;                  /* giữ màu nổi trên mobile */
    margin-top: 40px;
  }}
}}
</style>
""", unsafe_allow_html=True)

# --- TIÊU ĐỀ ---
st.markdown('<div id="main-animated-title-container"><h1>TỔ BẢO DƯỠNG SỐ 1</h1></div>', unsafe_allow_html=True)
st.markdown('<div id="sub-static-title"><h2>🔎 TRA CỨU PART NUMBER</h2></div>', unsafe_allow_html=True)
st.markdown("---")

# --- TRA CỨU DỮ LIỆU ---
excel_file = "A787.xlsx"
if not os.path.exists(excel_file):
    st
