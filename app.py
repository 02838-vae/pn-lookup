import streamlit as st
import pandas as pd
import base64
import os

# --- CẤU HÌNH CHUNG ---
st.set_page_config(page_title="Tổ Bảo Dưỡng Số 1 - Tra Cứu PN", layout="wide")

# === HÀM PHỤ TRỢ ===
def get_base64_encoded_file(file_path):
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

# === NỀN ===
bg_pc_base64 = get_base64_encoded_file("PN_PC.jpg")
bg_mobile_base64 = get_base64_encoded_file("PN_mobile.jpg")

# === CSS ===
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');

#MainMenu, footer, header {{visibility: hidden;}}
div.block-container {{padding-top: 0;}}

/* --- NỀN PC --- */
.stAppViewContainer, .st-emotion-cache-1r6slb0 {{
    background: url("data:image/jpeg;base64,{bg_pc_base64}") no-repeat center top fixed !important;
    background-size: cover !important;
    font-family: 'Oswald', sans-serif !important;
}}

/* --- TIÊU ĐỀ CHÍNH --- */
@keyframes scrollText {{
  0% {{ transform: translateX(100%); }}
  100% {{ transform: translateX(-100%); }}
}}
@keyframes colorShift {{
  0% {{ background-position: 0% 50%; }}
  50% {{ background-position: 100% 50%; }}
  100% {{ background-position: 0% 50%; }}
}}

#main-animated-title-container {{
  width: 100%;
  overflow: hidden;
  text-align: center;
  margin-top: 25px;
  margin-bottom: 20px;
  height: 90px;
}}
#main-animated-title-container h1 {{
  font-family: 'Oswald', sans-serif;
  font-size: 3.8rem; /* nhỏ hơn 1 chút để tránh mất nét */
  font-weight: 700;
  text-transform: uppercase;
  display: inline-block;
  white-space: nowrap;
  background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3);
  background-size: 400% 400%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: colorShift 10s ease infinite, scrollText 10s linear infinite; /* ⚡ chạy nhanh gấp đôi */
  text-shadow: 2px 2px 8px rgba(0,0,0,0.7);
}}

/* --- TIÊU ĐỀ PHỤ --- */
#sub-static-title h2 {{
  font-family: 'Playfair Display', serif;
  font-size: 2.3rem;
  color: #FFD54F;
  text-align: center;
  text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
  margin-top: 25px;
  margin-bottom: 20px;
}}

/* --- MOBILE --- */
@media (max-width: 768px) {{
  .stAppViewContainer, .st-emotion-cache-1r6slb0 {{
    background: url("data:image/jpeg;base64,{bg_mobile_base64}") no-repeat center top scroll !important;
    background-size: cover !important;
  }}
  #main-animated-title-container h1 {{
    font-size: 8vw;
    animation: colorShift 10s ease infinite, scrollText 8s linear infinite; /* chạy nhanh hơn cả mobile */
    line-height: 1.2;
  }}
  #sub-static-title h2 {{
    font-size: 5vw;
  }}
}}

/* --- LABEL SELECTBOX --- */
.stSelectbox label {{
  color: #FFEB3B !important;
  font-weight: 700;
  text-align: center;
  display: block;
  font-size: 1.6rem; /* to hơn chút */
}}
div[data-baseweb="select"] > div {{
  text-align: center;
}}
div[data-testid="column"] {{
  display: flex;
  justify-content: center;
}}

/* --- BẢNG DỮ LIỆU --- */
.stDataFrame table {{
  width: 100% !important;
  text-align: center !important;
}}
.stDataFrame tbody td, .stDataFrame thead th {{
  text-align: center !important;
  vertical-align: middle !important;
}}
.stDataFrame tbody td {{
  padding: 10px !important;
  white-space: nowrap;
}}
.stDataFrame thead th {{
  background-color: rgba(255,255,255,0.85);
}}
.stDataFrame div[data-testid="stDataFrameContainer"] > div {{
  overflow-x: auto !important;
}}
</style>
""", unsafe_allow_html=True)

# === TIÊU ĐỀ ===
st.markdown('<div id="main-animated-title-container"><h1>TỔ BẢO DƯỠNG SỐ 1</h1></div>', unsafe_allow_html=True)
st.markdown('<div id="sub-static-title"><h2>🔎 TRA CỨU PART NUMBER</h2></div>', unsafe_allow_html=True)
st.markdown("---")

# === TRA CỨU ===
excel_file = "A787.xlsx"
if not os.path.exists(excel_file):
    st.error("❌ Không tìm thấy file A787.xlsx trong thư mục hiện tại.")
else:
    try:
        xls = pd.ExcelFile(excel_file)
        sheet_names = [name for name in xls.sheet_names if not name.startswith("Sheet")]

        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            zone = st.selectbox("📂 Zone", sheet_names)
        df = load_and_clean(excel_file, zone)

        with col2:
            aircrafts = sorted(df["A/C"].dropna().unique().tolist()) if "A/C" in df.columns else []
            aircraft = st.selectbox("✈️ Loại máy bay", aircrafts) if aircrafts else None
        df = df[df["A/C"] == aircraft] if aircraft else df

        with col3:
            descs = sorted(df["DESCRIPTION"].dropna().unique().tolist()) if "DESCRIPTION" in df.columns else []
            desc = st.selectbox("📑 Mô tả chi tiết", descs) if descs else None
        df = df[df["DESCRIPTION"] == desc] if desc else df

        with col4:
            items = sorted(df["ITEM"].dropna().unique().tolist()) if "ITEM" in df.columns else []
            item = st.selectbox("🔢 Item", items) if items else None
        df = df[df["ITEM"] == item] if item else df
        st.markdown("</div>", unsafe_allow_html=True)

        # === KẾT QUẢ ===
        st.markdown("---")
        if not df.empty:
            st.markdown("<h3 style='text-align:center; color:#2E7D32;'>📋 KẾT QUẢ TRA CỨU</h3>", unsafe_allow_html=True)

            df_display = df.drop(columns=["A/C", "ITEM", "DESCRIPTION"], errors="ignore")
            df_display = df_display.dropna(axis=1, how="all")

            if not df_display.empty:
                df_display = df_display.reset_index(drop=True)
                cols = list(df_display.columns)
                if "PART NUMBER" in cols:
                    idx = cols.index("PART NUMBER")
                    df_display.insert(idx, "STT", range(1, len(df_display) + 1))
                else:
                    df_display.insert(0, "STT", range(1, len(df_display) + 1))

                st.dataframe(
                    df_display,
                    hide_index=True,
                    use_container_width=True
                )
    except Exception as e:
        st.error(f"Lỗi khi đọc file Excel: {e}")
