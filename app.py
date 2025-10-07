import streamlit as st
import pandas as pd
import base64
import os
import time

st.set_page_config(page_title="Tổ Bảo Dưỡng Số 1", layout="wide")

# ====== CẤU HÌNH VIDEO ======
VIDEO_PATH = "airplane.mp4"
VIDEO_DURATION_SEC = 9  # video ~8s, dùng 9s làm an toàn

# ====== HIỆN VIDEO (INTRO) ======
if "show_main" not in st.session_state:
    st.session_state.show_main = False

if not st.session_state.show_main:
    # Nếu file video tồn tại -> hiển thị bằng thẻ <video> (base64) để autoplay muted
    if os.path.exists(VIDEO_PATH):
        with open(VIDEO_PATH, "rb") as f:
            video_b64 = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(f"""
        <style>
        html, body, [data-testid="stAppViewContainer"] {{
            margin:0; padding:0; overflow:hidden; background:black;
        }}
        #intro-wrap {{
            position: fixed;
            inset: 0;
            z-index: 9999;
            display:flex;
            align-items:center;
            justify-content:center;
            background:black;
        }}
        video#introVideo {{
            width:100%;
            height:100%;
            object-fit: contain; /* show full plane on any device */
            background:black;
        }}
        .intro-text {{
            position: absolute;
            bottom: 12vh;
            width:100%;
            text-align:center;
            font-family: 'Special Elite', cursive;
            font-size: 40px;
            color: #ffffff;
            text-shadow: 0 0 25px rgba(255,255,255,0.9), 0 0 40px rgba(0,200,255,0.6);
            opacity: 0;
            animation: fadeIn 2.5s ease 0.8s forwards, fadeOut 3s ease 6s forwards;
            z-index: 10001;
        }}
        @keyframes fadeIn {{
            from {{ opacity:0; transform: translateY(20px) scale(0.98); filter: blur(6px); }}
            to {{ opacity:1; transform: translateY(0) scale(1); filter: blur(0); }}
        }}
        @keyframes fadeOut {{
            from {{ opacity:1; }}
            to {{ opacity:0; transform: translateY(-20px) scale(1.02); filter: blur(8px); }}
        }}
        @keyframes hideWrap {{
            from {{ opacity:1; }}
            to {{ opacity:0; visibility:hidden; }}
        }}
        </style>

        <div id="intro-wrap">
            <video id="introVideo" autoplay muted playsinline>
                <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
            </video>
            <div class="intro-text">KHÁM PHÁ THẾ GIỚI CÙNG CHÚNG TÔI</div>
        </div>

        <script>
        const video = document.getElementById('introVideo');
        const wrap = document.getElementById('intro-wrap');
        function hideIntro() {{
            if (!wrap) return;
            wrap.style.animation = 'hideWrap 1.6s ease forwards';
            setTimeout(() => {{
                try {{ wrap.remove(); }} catch(e){{}}
                const app = document.querySelector('.stApp');
                if (app) {{
                    app.style.visibility = 'visible';
                    app.style.opacity = '0';
                    app.style.transition = 'opacity 1.6s ease';
                    setTimeout(()=> app.style.opacity = '1', 80);
                }}
            }}, 1600);
        }}

        // Khi video kết thúc
        video.addEventListener('ended', () => {{
            // gửi signal bằng cách set location param (fallback handled in python)
            hideIntro();
        }});

        // Fallback: nếu 'ended' không fired, tự hide sau VIDEO_DURATION_SEC
        setTimeout(hideIntro, {VIDEO_DURATION_SEC * 1000});
        </script>
        """, unsafe_allow_html=True)

        # Ẩn app chính trong lúc intro chạy
        st.markdown("<style>.stApp {visibility: hidden;}</style>", unsafe_allow_html=True)

        # Đợi một khoảng an toàn (để video thực sự có thời gian chạy) rồi bật trang chính
        time.sleep(VIDEO_DURATION_SEC)
        st.session_state.show_main = True
        st.experimental_rerun()

    else:
        # nếu ko có file video -> bỏ qua intro
        st.warning("⚠️ Không tìm thấy file airplane.mp4 — bỏ qua intro.")
        st.session_state.show_main = True
        st.experimental_rerun()

# ====== SAU KHI INTRO: TRANG CHÍNH (VINTAGE) ======
# helper đọc base64 ảnh
def _get_b64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

EXCEL_FILE = "A787.xlsx"
BG_FILE = "airplane.jpg"

# vintage CSS (áp dụng cho trang chính)
bg_b64 = _get_b64(BG_FILE) if os.path.exists(BG_FILE) else ""
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

.stApp {{
    font-family: 'Special Elite', cursive !important;
    background:
        linear-gradient(rgba(245,242,230,0.9), rgba(245,242,230,0.9)),
        url("data:image/jpeg;base64,{bg_b64}") no-repeat center center fixed;
    background-size: cover;
}}
.stApp::after {{
    content: "";
    position: fixed;
    inset: 0;
    background: url("https://www.transparenttextures.com/patterns/aged-paper.png");
    opacity: 0.35;
    pointer-events: none;
    z-index: -1;
}}
header[data-testid="stHeader"] {{display:none;}}
.block-container {{padding-top:0rem !important;}}

.top-title {{
    font-size: 34px; font-weight: bold; text-align:center;
    color:#3e2723; margin-top:15px; text-shadow:1px 1px 0 #fff;
}}
.main-title {{
    font-size: 26px; font-weight:900; text-align:center;
    color:#5d4037; margin-bottom:18px; text-shadow:1px 1px 2px rgba(255,255,255,0.8);
}}

/* TABLE vintage */
@keyframes fadeInTable {{
    from {{ opacity:0; transform: scale(0.98) rotate(-0.4deg); filter: blur(4px); }}
    to {{ opacity:1; transform: scale(1) rotate(0); filter: blur(0); }}
}}
table.dataframe {{
    width:100%; border-collapse:collapse;
    border:2px solid #5d4037; background:#fbf7ed; color:#3e2723 !important;
    font-size:15px; text-align:center; animation:fadeInTable .7s ease;
}}
table.dataframe thead th {{
    background: linear-gradient(180deg,#8d6e63,#5d4037);
    color:#fff8e1 !important; font-weight:bold; padding:10px !important;
    border:1.5px solid #3e2723 !important; text-transform:uppercase;
}}
table.dataframe tbody td {{
    padding:8px !important; border:1px dashed #6d4c41 !important;
}}
table.dataframe tbody tr:nth-child(even) td {{ background:#f3e9d2 !important; }}
table.dataframe tbody tr:hover td {{ background:#f1d9b5 !important; transition: all .25s ease; }}

.highlight-msg {{
    font-size:18px; font-weight:bold; color:#3e2723; background:#efebe9;
    padding:10px 15px; border-left:6px solid #6d4c41; border-radius:6px;
    margin:15px 0; display:flex; align-items:center; justify-content:center;
}}
</style>
""", unsafe_allow_html=True)

# ====== Load Excel existence check ======
if not os.path.exists(EXCEL_FILE):
    st.error(f"⚠️ Không tìm thấy file {EXCEL_FILE} trong thư mục. Vui lòng kiểm tra.")
else:
    # helper load & clean
    def load_and_clean(sheet_name):
        df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name, dtype=object)
        # chuẩn hóa header
        df.columns = df.columns.str.strip()
        # giữ nguyên tên cột gốc nhưng dùng bản upper khi so sánh
        # thay thế ô chỉ có space thành NaN
        df = df.replace(r'^\s*$', pd.NA, regex=True)
        # loại bỏ hoàn toàn hàng rỗng
        df = df.dropna(how="all").reset_index(drop=True)
        # trim string values
        for c in df.columns:
            if df[c].dtype == object:
                df[c] = df[c].where(df[c].notna(), None)
                df[c] = df[c].apply(lambda x: x.strip() if isinstance(x, str) else x)
        return df

    st.markdown('<div class="top-title">📜 Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">🔎 Tra cứu Part number</div>', unsafe_allow_html=True)

    xls = pd.ExcelFile(EXCEL_FILE)
    zone = st.selectbox("📂 Bạn muốn tra cứu zone nào?", xls.sheet_names)
    if zone:
        df_all = load_and_clean(zone)

        # --- CHỌN A/C nếu có ---
        ac_col = next((c for c in df_all.columns if c.strip().upper() == "A/C"), None)
        if ac_col:
            ac_choices = sorted([str(x) for x in df_all[ac_col].dropna().unique()])
            aircraft = st.selectbox("✈️ Loại máy bay?", ac_choices)
            df_filtered = df_all[df_all[ac_col] == aircraft].copy()
        else:
            aircraft = None
            df_filtered = df_all.copy()

        # --- CHỌN DESCRIPTION nếu có ---
        desc_col = next((c for c in df_filtered.columns if c.strip().upper() == "DESCRIPTION"), None)
        if desc_col:
            desc_choices = sorted([str(x) for x in df_filtered[desc_col].dropna().unique()])
            description = st.selectbox("📑 Bạn muốn tra cứu phần nào?", desc_choices)
            df_filtered = df_filtered[df_filtered[desc_col] == description].copy()
        else:
            description = None

        # --- CHỌN ITEM nếu có ---
        item_col = next((c for c in df_filtered.columns if c.strip().upper() == "ITEM"), None)
        if item_col:
            item_choices = sorted([str(x) for x in df_filtered[item_col].dropna().unique()])
            if len(item_choices) > 1:
                item = st.selectbox("🔢 Bạn muốn tra cứu Item nào?", item_choices)
                df_filtered = df_filtered[df_filtered[item_col] == item].copy()
        # else: nothing

        # ===== TẠO df_result và chọn cột để hiển thị, giữ nguyên A/C và ITEM nếu có =====
        if df_filtered.empty:
            st.warning("📌 Rất tiếc, không tìm thấy dữ liệu phù hợp.")
        else:
            # giữ nguyên thứ tự cột mong muốn
            cols = []

            # luôn ưu tiên hiển thị cột A/C nếu có trong file
            if ac_col and ac_col in df_filtered.columns:
                cols.append(ac_col)

            # giữ ITEM nếu có
            if item_col and item_col in df_filtered.columns:
                cols.append(item_col)

            # tìm cột PART NUMBER (ưu tiên tên rõ ràng)
            pn_col = None
            for c in df_filtered.columns:
                cu = c.strip().upper()
                if "PART NUMBER" in cu or ("PART" in cu and "NUMBER" in cu):
                    pn_col = c
                    break
            if not pn_col:
                # tìm tên có PN
                for c in df_filtered.columns:
                    cu = c.strip().upper()
                    if cu == "PN" or "(PN)" in cu or cu.endswith(" PN"):
                        pn_col = c
                        break
            if not pn_col:
                # fallback: tìm cột chứa "PART"
                for c in df_filtered.columns:
                    if "PART" in c.strip().upper():
                        pn_col = c
                        break
            if not pn_col:
                # fallback: lấy cột đầu tiên có chữ 'NUMBER' hoặc nếu không, cột đầu tiên (không chèn A/C or ITEM again)
                for c in df_filtered.columns:
                    if "NUMBER" in c.strip().upper():
                        pn_col = c
                        break
            if not pn_col:
                # take first column that's not A/C or ITEM
                for c in df_filtered.columns:
                    if c not in [ac_col, item_col]:
                        pn_col = c
                        break

            if pn_col and pn_col not in cols:
                cols.append(pn_col)

            # tìm cột interchange nếu có
            inter_col = None
            for c in df_filtered.columns:
                if "INTERCHANGE" in c.strip().upper():
                    inter_col = c
                    break
            if inter_col and inter_col not in cols:
                cols.append(inter_col)

            # NOTE
            note_col = next((c for c in df_filtered.columns if c.strip().upper() == "NOTE"), None)
            if note_col and note_col not in cols:
                cols.append(note_col)

            # cuối cùng: nếu vẫn còn cột dữ liệu quan trọng thiếu (ví dụ MODEL / DESCRIPTION), bạn có thể thêm
            # nhưng để nguyên hiện tại

            # đảm bảo cột tồn tại
            cols = [c for c in cols if c and c in df_filtered.columns]

            # chuẩn hóa: thay các chuỗi rỗng hoặc chỉ space bằng NA, sau đó drop rows all NA
            df_work = df_filtered.copy()
            df_work = df_work.replace(r'^\s*$', pd.NA, regex=True)
            df_work = df_work.dropna(how="all").reset_index(drop=True)

            # nếu có ít nhất 1 cột trong cols thì chọn, ngược lại hiển thị toàn bộ df_work
            if cols:
                df_result = df_work[cols].copy()
            else:
                df_result = df_work.copy()

            # loại bỏ hàng rỗng (dựa trên df_result)
            df_result = df_result.replace(r'^\s*$', pd.NA, regex=True).dropna(how="all").reset_index(drop=True)

            # chèn STT
            if not df_result.empty:
                df_result.insert(0, "STT", range(1, len(df_result)+1))
                # hiển thị table (HTML) để CSS table.dataframe áp dụng
                st.markdown(f'<div class="highlight-msg">✅ Tìm thấy {len(df_result)} dòng dữ liệu</div>', unsafe_allow_html=True)
                st.write(df_result.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.warning("📌 Không tìm thấy dữ liệu phù hợp sau khi lọc (các hàng rỗng đã bị loại).")
