# app.py (full) — bản debug + resize GIF + hiển thị fixed overlay
import os
import io
import base64
import pandas as pd
import streamlit as st

# optional pillow for resizing animated GIF
try:
    from PIL import Image, ImageSequence
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

# ====== Config files ======
EXCEL_FILE = "A787.xlsx"
BG_FILE = "airplane.jpg"
GIF_FILE = "airplane.gif"

# ====== Helpers ======
def file_base64(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

def try_resize_gif_bytes(orig_bytes: bytes, target_h: int = 60) -> bytes | None:
    """
    Try to resize animated GIF frames to target height (keeping animation).
    Returns new GIF bytes or None on failure / if PIL not available.
    """
    if not PIL_AVAILABLE:
        return None
    try:
        buf = io.BytesIO(orig_bytes)
        im = Image.open(buf)
        frames = []
        durations = []
        disposals = []
        for frame in ImageSequence.Iterator(im):
            frame = frame.convert("RGBA")
            w, h = frame.size
            new_w = max(1, int(w * (target_h / float(h))))
            frame_resized = frame.resize((new_w, target_h), Image.LANCZOS)
            frames.append(frame_resized)
            durations.append(frame.info.get("duration", 100))
            disposals.append(frame.info.get("disposal", 2))
        out = io.BytesIO()
        # Save with first frame + append_images
        frames[0].save(
            out,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            duration=durations,
            loop=0,
            disposal=2,
            optimize=False,
        )
        return out.getvalue()
    except Exception as e:
        # If anything fails, return None
        return None

# ====== Load / validate files ======
# Excel
if not os.path.exists(EXCEL_FILE):
    st.error(f"❌ Không tìm thấy file Excel: {EXCEL_FILE}. Đặt file vào cùng thư mục với app.py.")
    st.stop()

# read excel (only sheet names initially)
try:
    xls = pd.ExcelFile(EXCEL_FILE)
except Exception as e:
    st.error(f"❌ Lỗi khi đọc Excel '{EXCEL_FILE}': {e}")
    st.stop()

# Background base64 (optional)
bg_b64 = file_base64(BG_FILE)
if not bg_b64:
    # fallback gradient will be used in CSS
    st.warning(f"⚠️ Không tìm thấy '{BG_FILE}'. App chạy với nền vintage gradient thay thế.")

# GIF check + optional resize
gif_exists = os.path.exists(GIF_FILE)
gif_info = {
    "exists": gif_exists,
    "filesize": None,
    "orig_b64_len": None,
    "used_resized": False,
    "final_b64_len": None,
}
gif_b64_final = None

if gif_exists:
    gif_info["filesize"] = os.path.getsize(GIF_FILE)
    orig_b64 = file_base64(GIF_FILE)
    gif_info["orig_b64_len"] = len(orig_b64) if orig_b64 else None

    # try resize to a smaller animated gif if PIL available
    try:
        orig_bytes = base64.b64decode(orig_b64)
        resized = try_resize_gif_bytes(orig_bytes, target_h=60)
        if resized:
            gif_b64_final = base64.b64encode(resized).decode("ascii")
            gif_info["used_resized"] = True
            gif_info["final_b64_len"] = len(gif_b64_final)
        else:
            # fallback to original
            gif_b64_final = orig_b64
            gif_info["used_resized"] = False
            gif_info["final_b64_len"] = len(gif_b64_final)
    except Exception:
        gif_b64_final = orig_b64
        gif_info["used_resized"] = False
        gif_info["final_b64_len"] = len(gif_b64_final)

# ====== CSS (vintage background + fixed gif overlay) ======
# build background CSS: if bg_b64 exists, use it; else use gradient fallback
if bg_b64:
    bg_css = f'linear-gradient(rgba(255,239,186,0.45), rgba(255,239,186,0.45)), url("data:image/jpg;base64,{bg_b64}")'
else:
    bg_css = "linear-gradient(180deg, #f3e5ab, #e6d690, #d6c38c)"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

.stApp {{
    background: {bg_css};
    background-size: cover;
    background-position: center;
    font-family: 'Special Elite', cursive !important;
    /* slight vintage effect */
    filter: sepia(0.15) contrast(1.02) brightness(1.02);
}}

.block-container {{ position: relative; z-index: 1; padding-top: 0.5rem !important; }}
header[data-testid="stHeader"] {{ display: none; }}

/* titles */
.top-title {{ text-align:center; font-size:34px; font-weight:800; margin:10px 0; color:#3e2723; }}
.main-title {{ text-align:center; font-size:22px; margin-bottom:10px; color:#5d4037; }}

/* table styling */
table.dataframe {{ width:100%; border-collapse:collapse; background:#fffaf0; box-shadow:0 6px 14px rgba(0,0,0,0.12); font-family: 'Special Elite', cursive !important; }}
table.dataframe thead th {{ background:#5d4037 !important; color:#f8f1df !important; font-weight:700; padding:8px; border:2px solid #3e2723 !important; }}
table.dataframe tbody td {{ text-align:center !important; padding:8px !important; color:#3e2723; border:1px solid #e6d7c4 !important; }}
table.dataframe tbody tr:nth-child(even) td {{ background:#f6efe0 !important; }}

/* highlight msg */
.highlight-msg {{ display:inline-flex; align-items:center; gap:8px; background:#efe6d5; padding:10px 12px; border-left:6px solid #6d4c41; border-radius:6px; font-weight:700; }}

/* FIXED GIF WRAPPER at bottom (centered) */
#plane-wrapper {{
    position: fixed;
    bottom: 12px;
    left: 0;
    right: 0;
    height: 80px;            /* height of wrapper area */
    pointer-events: none;    /* won't block clicks */
    z-index: 2147483647;     /* very high */
    display: block;
    overflow: visible;
}}

/* the img itself will animate from left to right and back */
.plane-img {{
    position: absolute;
    left: -200px;
    bottom: 0;
    height: 60px;        /* displayed height */
    width: auto;
    transform-origin: center;
    animation: flyLR 12s linear infinite;
    will-change: transform, left;
    -webkit-backface-visibility: hidden;
    backface-visibility: hidden;
}

/* go left -> right and reset (loop). If you prefer back-and-forth, see alt keyframes below. */
@keyframes flyLR {{
    0%   {{ left: -220px; transform: translateX(0) scaleX(1); }}
    49%  {{ left: 50vw; transform: translateX(0) scaleX(1); }}
    50%  {{ left: 50vw; transform: translateX(0) scaleX(-1); }}
    99%  {{ left: 110vw; transform: translateX(0) scaleX(-1); }}
    100% {{ left: -220px; transform: translateX(0) scaleX(1); }}
}}

/* If you prefer smooth back-and-forth (no flip), you can use this alternative:
@keyframes flyBackForth {
  0% { left: -220px; }
  50% { left: calc(100% - 60px); }
  100% { left: -220px; }
}
*/
</style>
""", unsafe_allow_html=True)

# ====== Header ======
st.markdown('<div class="top-title">📜 Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🔎 Tra cứu Part number</div>', unsafe_allow_html=True)

# ====== Debug INFO (visible on app) ======
# Show concise debug info for GIF status so you can see what's happening
if not gif_exists:
    st.info("ℹ️ airplane.gif không tìm thấy trong thư mục. Nếu muốn hiển thị GIF, upload 'airplane.gif' vào cùng thư mục với app.py.")
else:
    st.success(f"✅ Đã phát hiện '{GIF_FILE}' — kích thước file: {gif_info['filesize']:,} bytes. "
               f"resize used: {gif_info['used_resized']}, final base64 len: {gif_info['final_b64_len']:,}")

# ====== Main app logic: dropdowns, search, table (kept simple) ======
def load_and_clean(sheet_name):
    df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name)
    df.columns = df.columns.str.strip().str.upper()
    # fillna for object columns
    for c in df.columns:
        if df[c].dtype == "object":
            df[c] = df[c].fillna("").astype(str).str.strip()
    return df

# dropdowns and display (same logic as before)
zone = st.selectbox("📂 Bạn muốn tra cứu zone nào?", xls.sheet_names)
if zone:
    df = load_and_clean(zone)

    aircraft = None
    if "A/C" in df.columns:
        aircrafts = sorted([ac for ac in df["A/C"].dropna().unique().tolist() if ac and ac.upper() != "NAN"])
        aircraft = st.selectbox("✈️ Loại máy bay?", aircrafts)

    if aircraft:
        df_ac = df[df["A/C"] == aircraft]

        description = None
        if "DESCRIPTION" in df_ac.columns:
            desc_list = sorted([d for d in df_ac["DESCRIPTION"].dropna().unique().tolist() if d and d.upper() != "NAN"])
            description = st.selectbox("📑 Bạn muốn tra cứu phần nào?", desc_list)

        if description:
            df_desc = df_ac[df_ac["DESCRIPTION"] == description]

            if "ITEM" in df_desc.columns:
                items = sorted([i for i in df_desc["ITEM"].dropna().unique().tolist() if i and i.upper() != "NAN"])
                if items:
                    item = st.selectbox("🔢 Bạn muốn tra cứu Item nào?", items)
                    df_desc = df_desc[df_desc["ITEM"] == item]

            if not df_desc.empty:
                df_result = df_desc.copy().reset_index(drop=True)

                # select columns
                cols_to_show = ["PART NUMBER (PN)"]
                for alt in ["PART INTERCHANGE", "PN INTERCHANGE"]:
                    if alt in df_result.columns:
                        cols_to_show.append(alt)
                        break
                if "NOTE" in df_result.columns:
                    cols_to_show.append("NOTE")

                df_result = df_result[cols_to_show]
                df_result.insert(0, "STT", range(1, len(df_result) + 1))

                st.markdown(f'<div class="highlight-msg">✅ Tìm thấy {len(df_result)} dòng dữ liệu</div>', unsafe_allow_html=True)
                st.write(df_result.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.error("❌ Không tìm thấy dữ liệu.")

# ====== Render GIF overlay if available ======
if gif_b64_final:
    # small diagnostic: show a tiny static copy via st.image for quick visual check (non-blocking)
    try:
        gif_bytes_for_st = base64.b64decode(gif_b64_final)
        # show tiny preview in upper-right corner (optional)
        st.sidebar.image(gif_bytes_for_st, width=80)
    except Exception:
        pass

    # Render fixed overlay HTML (centered horizontal area at bottom)
    html_plane = f"""
    <div id="plane-wrapper">
      <img class="plane-img" src="data:image/gif;base64,{gif_b64_final}" alt="plane gif" />
    </div>
    """
    st.markdown(html_plane, unsafe_allow_html=True)
else:
    st.info("ℹ️ airplane.gif chưa được hiển thị (file thiếu hoặc lỗi khi xử lý).")
