import streamlit as st
import pandas as pd
import base64
import os

# --- CẤU HÌNH ---
st.set_page_config(page_title="Tổ Bảo Dưỡng Số 1 - Tra Cứu PN", layout="wide")

# --- HÀM HỖ TRỢ ---
def get_base64_encoded_file(file_path):
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return ""
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def load_and_clean(excel_file, sheet):
    try:
        df = pd.read_excel(excel_file, sheet_name=sheet)
        df.columns = df.columns.str.strip().str.upper()
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].fillna("").astype(str).str.strip()
        return df.dropna(how="all")
    except Exception:
        return pd.DataFrame()

# --- BACKGROUND ---
bg_pc_base64 = get_base64_encoded_file("PN_PC.jpg")
bg_mobile_base64 = get_base64_encoded_file("PN_mobile.jpg")

# --- CSS ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');

#MainMenu, footer, header {{ visibility: hidden; }}
div.block-container {{ padding-top: 0; }}

/* ===== BACKGROUND ===== */
.stAppViewContainer, .st-emotion-cache-1r6slb0 {{
  background: url("data:image/jpeg;base64,{bg_pc_base64}") no-repeat center top fixed !important;
  background-size: cover !important;
  font-family: 'Oswald', sans-serif !important;
}}

/* ===== MARQUEE TITLE (seamless, continuous, right->left) ===== */
#main-animated-title-container {{
  width: 100%;
  overflow: hidden;
  text-align: center;
  margin: 18px 0 6px 0;
  height: auto;
}}
.marquee {{
  display: block;
  width: 100%;
  overflow: hidden;
  box-sizing: border-box;
}}
.marquee__inner {{
  display: inline-block;
  white-space: nowrap;
  box-sizing: content-box;
  /* duplicated content technique: width 200% so that translateX(-50%) moves exactly one copy */
  width: 200%;
  animation: marqueeScroll 4s linear infinite; /* faster: 4s for full loop (adjust if needed) */
}}
.marquee__item {{
  display: inline-block;
  padding-right: 4rem; /* spacing between repeats */
  font-family: 'Oswald', sans-serif;
  font-weight: 700;
  text-transform: uppercase;
  font-size: 3.6rem; /* safe size so not clipped */
  letter-spacing: 6px;
  vertical-align: middle;
  background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3);
  background-size: 400% 400%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 2px 2px 8px rgba(0,0,0,0.65);
  box-sizing: border-box;
}
/* Duplicate item style handled by rendering two identical spans */

@keyframes marqueeScroll {{
  0% {{ transform: translateX(0%); }}
  100% {{ transform: translateX(-50%); }} /* move one full copy (200% -> -50% = shift by 100% of viewport) */
}}

/* color shift effect (kept on top of marquee using background position animation) */
@keyframes colorShift {{
  0% {{ background-position: 0% 50%; }}
  50% {{ background-position: 100% 50%; }}
  100% {{ background-position: 0% 50%; }}
}}
.marquee__item {{
  animation: colorShift 8s ease-in-out infinite;
}

/* ===== SUBTITLE ===== */
#sub-static-title h2 {{
  font-family: 'Playfair Display', serif;
  font-size: 2.3rem;
  color: #FFD54F;
  text-align: center;
  text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
  margin-top: 16px;
  margin-bottom: 18px;
}}

/* ===== MOBILE ADJUST ===== */
@media (max-width: 768px) {{
  .marquee__item {{
    font-size: 7.5vw; /* responsive */
    letter-spacing: 3px;
  }}
  #sub-static-title h2 {{
    font-size: 4.8vw;
    margin-top: 8px;
  }}
  .stAppViewContainer, .st-emotion-cache-1r6slb0 {{
    background: url("data:image/jpeg;base64,{bg_mobile_base64}") no-repeat center top scroll !important;
    background-size: cover !important;
  }}
}}

/* ===== SELECTBOX LABELS (bigger + centered) ===== */
.stSelectbox label {{
  color: #FFEB3B !important;
  font-weight: 800;
  text-align: center;
  display: block;
  font-size: 1.6rem; /* larger on PC */
}}
div[data-baseweb="select"] > div {{
  text-align: center;
}}
/* center the column containers */
[data-testid="column"] {{
  display: flex;
  justify-content: center;
  align-items: center;
}}

/* ===== TABLE (center all content, header + cells) ===== */
.stDataFrame table {{
  width: 100% !important;
  border-collapse: collapse;
}}
.stDataFrame thead th, .stDataFrame tbody td {{
  text-align: center !important;
  vertical-align: middle !important;
  padding: 8px !important;
  white-space: nowrap;
}
/* ensure header style readable on image background */
.stDataFrame thead th {{
  background: rgba(255,255,255,0.85) !important;
  font-weight: 700;
}}

/* allow horizontal scroll of table container (mobile) */
.stDataFrame div[data-testid="stDataFrameContainer"] > div {{
  overflow-x: auto !important;
}}

</style>
""", unsafe_allow_html=True)

# --- RENDER TITLES ---
st.markdown(
    """
    <div id="main-animated-title-container">
      <div class="marquee" aria-hidden="true">
        <div class="marquee__inner">
          <span class="marquee__item">TỔ BẢO DƯỠNG SỐ 1</span>
          <span class="marquee__item">TỔ BẢO DƯỠNG SỐ 1</span>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div id="sub-static-title"><h2>🔎 TRA CỨU PART NUMBER</h2></div>', unsafe_allow_html=True)
st.markdown("---")

# === DATA / UI ===
excel_file = "A787.xlsx"
if not os.path.exists(excel_file):
    st.error("❌ Không tìm thấy file A787.xlsx trong thư mục hiện tại.")
else:
    try:
        xls = pd.ExcelFile(excel_file)
        sheet_names = [n for n in xls.sheet_names if not n.startswith("Sheet")]

        # Select boxes centered
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            zone = st.selectbox("📂 Zone", sheet_names, key="zone")
        df = load_and_clean(excel_file, zone)

        with col2:
            if "A/C" in df.columns:
                aircrafts = sorted(df["A/C"].dropna().unique().tolist())
                aircraft = st.selectbox("✈️ Loại máy bay", aircrafts, key="ac")
            else:
                aircraft = None
        df = df[df["A/C"] == aircraft] if aircraft else df

        with col3:
            if "DESCRIPTION" in df.columns:
                descs = sorted(df["DESCRIPTION"].dropna().unique().tolist())
                desc = st.selectbox("📑 Mô tả chi tiết", descs, key="desc")
            else:
                desc = None
        df = df[df["DESCRIPTION"] == desc] if desc else df

        with col4:
            if "ITEM" in df.columns:
                items = sorted(df["ITEM"].dropna().unique().tolist())
                item = st.selectbox("🔢 Item", items, key="item")
            else:
                item = None
        df = df[df["ITEM"] == item] if item else df
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        # Only show result header + table when dataframe has rows
        if not df.empty:
            # prepare display frame (drop internal columns)
            df_display = df.drop(columns=["A/C", "ITEM", "DESCRIPTION"], errors="ignore")
            df_display = df_display.dropna(axis=1, how="all")

            if not df_display.empty:
                # reset index and add STT before PART NUMBER if exists
                df_display = df_display.reset_index(drop=True)
                cols = list(df_display.columns)
                if "PART NUMBER" in cols:
                    idx = cols.index("PART NUMBER")
                    df_display.insert(idx, "STT", range(1, len(df_display) + 1))
                else:
                    df_display.insert(0, "STT", range(1, len(df_display) + 1))

                # center header and cells via CSS above; hide dataframe index
                st.markdown("<h3 style='text-align:center; color:#2E7D32;'>📋 KẾT QUẢ TRA CỨU</h3>", unsafe_allow_html=True)
                st.dataframe(df_display, hide_index=True, use_container_width=True)
        else:
            st.warning("📌 Không có dữ liệu phù hợp với các lựa chọn.")
    except Exception as e:
        st.error(f"Lỗi khi đọc file Excel: {e}")
