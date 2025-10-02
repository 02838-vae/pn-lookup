# app.py
import os
import base64
import pandas as pd
import streamlit as st

# -------- CẤU HÌNH FILE --------
EXCEL_FILE = "A787.xlsx"
BG_IMAGE = "airplane.jpg"

st.set_page_config(page_title="Tra cứu PN", layout="wide")

# -------- HELPER: đọc background nếu có --------
def set_background(image_path: str):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: linear-gradient(rgba(250,250,250,0.85), rgba(250,250,250,0.85)),
                            url("data:image/jpg;base64,{b64}") no-repeat center center fixed;
                background-size: cover;
                font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        # nếu không có ảnh thì bỏ qua
        st.info("Không tìm thấy ảnh nền 'airplane.jpg' — nếu muốn background, đặt file vào cùng thư mục.")

set_background(BG_IMAGE)

# -------- CSS cho bảng HTML custom (header rõ ràng) --------
st.markdown(
    """
    <style>
    /* Title */
    .animated-title {
        font-size: 34px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 6px;
        background: linear-gradient(90deg,#ff4d4d,#ff9a4d,#ffd54d,#7fff7f,#4dd0e1,#5c6cff,#b84dff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 10s linear infinite;
    }
    @keyframes gradientShift {
      0% {background-position: 0% 50%;}
      50% {background-position: 100% 50%;}
      100% {background-position: 0% 50%;}
    }

    .main-title {
        font-size: 24px;
        text-align: center;
        color: #003366;
        margin-bottom: 18px;
        font-weight: 700;
    }

    /* custom-table */
    .custom-table {
        border-collapse: separate;
        border-spacing: 0;
        margin: 14px 0;
        border-radius: 12px;
        border: 3px solid #003366;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        width: 100%;
        background-color: #ffffff;
        font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    }
    .custom-table thead th {
        background-color: #003366 !important;   /* header đậm */
        color: #ffffff !important;              /* chữ trắng */
        font-weight: 800 !important;
        font-size: 15px !important;
        padding: 10px 12px !important;
        text-align: center;
        border-bottom: 3px solid #001733 !important;
        white-space: nowrap;
    }
    .custom-table tbody td {
        padding: 8px 10px;
        text-align: center;
        vertical-align: middle;
        border-bottom: 1px solid #e6e6e6;
        color: #000000;
        white-space: nowrap; /* không ngắt dòng */
        background-color: #ffffff;
    }
    .custom-table tbody tr:nth-child(even) td {
        background-color: #fbfcfd;
    }
    .custom-table tbody tr:hover td {
        background-color: #eef7ff;
    }
    .custom-table tr:first-child th:first-child { border-top-left-radius: 10px; }
    .custom-table tr:first-child th:last-child { border-top-right-radius: 10px; }
    .custom-table tr:last-child td:first-child { border-bottom-left-radius: 10px; }
    .custom-table tr:last-child td:last-child { border-bottom-right-radius: 10px; }

    /* container scroll ngang */
    .table-scroll {
        overflow-x: auto;
    }

    /* label dropdown */
    label[for^="stSelectbox"] { font-weight:700; color:#111; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------- Utility: tìm tên cột phù hợp --------
def find_column(df_cols, candidates=None, keywords=None):
    """
    Trả về tên cột đầu tiên khớp trong df_cols.
    - candidates: danh sách tên full khả dĩ (đã uppercase)
    - keywords: danh sách từ khóa; nếu một cột chứa TẤT CẢ keywords sẽ được chọn
    """
    cols = [c.upper().strip() for c in df_cols]
    if candidates:
        for cand in candidates:
            cand_u = cand.upper().strip()
            if cand_u in cols:
                return df_cols[cols.index(cand_u)]
    if keywords:
        key_upper = [k.upper() for k in keywords]
        # ưu tiên cột chứa all keywords
        for i, col in enumerate(cols):
            if all(k in col for k in key_upper):
                return df_cols[i]
        # nếu không có, trả cột chứa bất kỳ keyword (first)
        for i, col in enumerate(cols):
            if any(k in col for k in key_upper):
                return df_cols[i]
    return None

# -------- Kiểm tra file excel tồn tại --------
if not os.path.exists(EXCEL_FILE):
    st.error(f"Không tìm thấy file '{EXCEL_FILE}'. Hãy đặt file A787.xlsx vào cùng thư mục với app.py.")
    uploaded = st.file_uploader("Hoặc upload A787.xlsx ở đây", type=["xlsx"])
    if uploaded is None:
        st.stop()
    else:
        # dùng file upload
        xls = pd.ExcelFile(uploaded)
else:
    xls = pd.ExcelFile(EXCEL_FILE)

# -------- UI chính --------
st.markdown('<div class="animated-title">Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🔎 Tra cứu Part Number (PN)</div>', unsafe_allow_html=True)

# Step 1: chọn sheet (zone)
sheet_name = st.selectbox("📂 Bạn muốn tra cứu zone nào?", xls.sheet_names, key="sheet")

if sheet_name:
    # đọc sheet
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name, dtype=str)
    else:
        # nếu dùng upload
        uploaded = st.session_state.get("uploaded_file", None)
        # fallback: read from xls object
        df = pd.read_excel(xls, sheet_name=sheet_name, dtype=str)

    # chuẩn hóa tên cột: giữ bản gốc nhưng tạo bản upper để dò
    orig_columns = list(df.columns)
    # strip spaces in column names but keep original mapping
    df.columns = [c.strip() if isinstance(c, str) else c for c in df.columns]
    upper_cols = [str(c).strip().upper() for c in df.columns]

    # tìm các cột quan trọng bằng nhiều cách
    # A/C
    ac_col = find_column(df.columns, candidates=["A/C", "AC", "AIRCRAFT", "AIRCRAFT TYPE"], keywords=["A/C", "AC", "AIRCRAFT"])
    # DESCRIPTION
    desc_col = find_column(df.columns, candidates=["DESCRIPTION", "DESC", "ITEM DESCRIPTION", "ITEM/ DESCRIPTION", "ITEM/DESCRIPTION"], keywords=["DESCRIPTION","DESC","ITEM"])
    # ITEM
    item_col = find_column(df.columns, candidates=["ITEM", "ITEM#", "ITEM NO", "ITEM NO."], keywords=["ITEM"])
    # PART NUMBER (PN)
    pn_col = find_column(df.columns, candidates=["PART NUMBER (PN)","PART NUMBER (PN)","PART NUMBER","P/N","PN","PART NUMBER(PN)"], keywords=["PART","NUMBER","PN"])
    # PART INTERCHANGE
    pi_col = find_column(df.columns, candidates=["PART INTERCHANGE","PN INTERCHANGE","P/N INTERCHANGE","PART INTERCHANGE (PN)"], keywords=["INTERCHANGE","INTERCHANGE(N","INTERCHANGE"])
    # NOTE
    note_col = find_column(df.columns, candidates=["NOTE","NOTES","COMMENT","COMMENTS"], keywords=["NOTE","COMMENT"])

    # Nếu không tìm thấy PI, thử tìm cột chứa 'INTER' hoặc 'EXCHANGE'
    if not pi_col:
        for c in df.columns:
            cu = str(c).upper()
            if "INTERCHANGE" in cu or "INTER" in cu or "EXCHANGE" in cu:
                pi_col = c
                break

    # Nếu không tìm thấy PN, cố gắng tìm chứa 'PN' hoặc 'P/N' hoặc 'PART'+'NUMBER'
    if not pn_col:
        for c in df.columns:
            cu = str(c).upper()
            if "PART" in cu and "NUMBER" in cu:
                pn_col = c
                break
            if "PN" in cu or "P/N" in cu:
                pn_col = c
                break

    # Nếu không tìm thấy DESCRIPTION, báo cho user
    if not desc_col:
        st.warning("Không tìm thấy cột DESCRIPTION trong sheet này (tên cột khác). Vui lòng kiểm tra file.")
    if not ac_col:
        st.warning("Không tìm thấy cột A/C trong sheet này (tên cột khác). Vui lòng kiểm tra file.")

    # chuẩn hóa dữ liệu: thay None/NaN/"NAN"/"nan"/"NONE" thành ""
    df = df.fillna("")  # NaN -> ""
    df = df.replace(["NAN", "NaN", "nan", "NONE", "None", "NULL", "null"], "")

    # Build dropdown giá trị, loại bỏ chuỗi rỗng
    if ac_col:
        ac_values = sorted([v for v in df[ac_col].astype(str).unique() if str(v).strip() != ""])
    else:
        ac_values = []

    aircraft = None
    if ac_values:
        aircraft = st.selectbox("✈️ Loại máy bay?", ac_values, key="aircraft_select")

    if aircraft:
        df_ac = df[df[ac_col].astype(str) == str(aircraft)]

        # DESCRIPTION dropdown
        description = None
        if desc_col:
            desc_values = sorted([v for v in df_ac[desc_col].astype(str).unique() if str(v).strip() != ""])
            if desc_values:
                description = st.selectbox("📑 Bạn muốn tra cứu phần nào?", desc_values, key="desc_select")

        if description:
            df_desc = df_ac[df_ac[desc_col].astype(str) == str(description)]

            # ITEM dropdown nếu có
            if item_col and item_col in df_desc.columns:
                item_values = sorted([v for v in df_desc[item_col].astype(str).unique() if str(v).strip() != ""])
                item = None
                if item_values:
                    item = st.selectbox("📌 Bạn muốn tra cứu Item nào?", item_values, key="item_select")
                    if item:
                        df_desc = df_desc[df_desc[item_col].astype(str) == str(item)]

            # Lọc và hiển thị kết quả
            if not df_desc.empty:
                # Tạo bản sao để xử lý hiển thị
                result = df_desc.copy()

                # Thêm STT (bắt đầu từ 1) ở cột đầu
                result.insert(0, "STT", range(1, len(result) + 1))

                # Chọn các cột để hiển thị: đảm bảo lấy đúng tên cột thực tế trong df
                display_cols = ["STT"]
                if pn_col:
                    display_cols.append(pn_col)
                if pi_col:
                    display_cols.append(pi_col)
                if note_col:
                    display_cols.append(note_col)

                # Nếu PN/PI/NOTE không có, vẫn tiếp tục (để user biết thiếu cột)
                # Đổi tên cột hiển thị sang tiêu đề cố định để dễ nhìn
                to_display = result[display_cols].copy()
                rename_map = {}
                if pn_col and pn_col in to_display.columns:
                    rename_map[pn_col] = "PART NUMBER (PN)"
                if pi_col and pi_col in to_display.columns:
                    rename_map[pi_col] = "PART INTERCHANGE"
                if note_col and note_col in to_display.columns:
                    rename_map[note_col] = "NOTE"

                to_display = to_display.rename(columns=rename_map)

                # Xóa giá trị NAN string nếu còn sót
                to_display = to_display.replace(["NAN", "NaN", "nan", "NONE", None], "")

                # Nếu cột PART INTERCHANGE tồn tại, đảm bảo hiển thị nguyên văn (không thay xuống dòng)
                # (Nếu bạn muốn tách xuống dòng, có thể xử lý ở đây)

                # Chuyển DataFrame thành HTML table với class custom-table
                html_table = to_display.to_html(index=False, classes="custom-table", escape=False)

                # Bao 1 div scroll ngang và show
                st.success(f"Tìm thấy {len(to_display)} dòng dữ liệu:")
                st.markdown('<div class="table-scroll">', unsafe_allow_html=True)
                st.markdown(html_table, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            else:
                st.error("Không tìm thấy dữ liệu cho lựa chọn này.")
        else:
            if desc_col:
                st.info("Hãy chọn mục (Description) để hiển thị kết quả.")
    else:
        if ac_col:
            st.info("Hãy chọn loại máy bay (A/C).")
