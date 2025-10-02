import pandas as pd
import streamlit as st
import base64

# ===== CSS: Background airplane.jpg + Hiệu ứng =====
def set_background(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(240,248,255,0.85), rgba(255,255,255,0.9)),
                        url("data:image/jpg;base64,{b64}") no-repeat center center fixed;
            background-size: cover;
            font-family: "Segoe UI", Helvetica, Arial, sans-serif;
        }}

        @keyframes gradientShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        @keyframes neonPulse {{
            0%, 100% {{ text-shadow: 0 0 5px #fff, 0 0 10px #0ff; }}
            50% {{ text-shadow: 0 0 20px #0ff, 0 0 30px #0ff; }}
        }}

        /* Tiêu đề trên cùng */
        .animated-title {{
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
            background: linear-gradient(-45deg,#ff0000,#ff7300,#ffeb00,#47ff00,#00ffee,#2b65ff,#8000ff,#ff0080);
            background-size: 600% 600%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradientShift 10s ease infinite, neonPulse 2s ease-in-out infinite;
        }}

        /* Tiêu đề chính */
        .main-title {{
            margin-top: 40px;
            font-size: 28px;
            text-align: center;
            font-weight: bold;
            color: #003366;
        }}

        /* Style cho label (câu hỏi) */
        .stSelectbox label, .stMarkdown p {{
            font-weight: bold !important;
            color: #111111 !important;
        }}

        /* Bảng kết quả */
        .scroll-container {{
            overflow-x: auto;
        }}
        table.dataframe {{
            border-collapse: separate;
            border-spacing: 0;
            margin: 15px auto;
            border-radius: 12px;
            border: 3px solid #003366;
            overflow: hidden;
            box-shadow: 0 4px 25px rgba(0,0,0,0.15);
            width: 100% !important;
            font-size: 13px !important;
            table-layout: auto;
            background-color: #ffffff !important;
            color: #000000 !important;
        }}
        table.dataframe th, table.dataframe td {{
            text-align: center !important;
            vertical-align: middle !important;
            padding: 8px 12px;
            white-space: nowrap !important;
            color: #000000 !important;
            background-color: #ffffff !important;
        }}
        table.dataframe thead th {{
            background-color: #002244 !important;  /* Xanh đậm hơn */
            color: #ffffff !important;             /* Chữ trắng nổi bật */
            font-weight: 900 !important;           /* Đậm hẳn */
            font-size: 14px !important;            /* To hơn một chút */
        }}
        table.dataframe tbody tr:hover {{
            background-color: #f0f8ff !important;
        }}
        table.dataframe tr:first-child th:first-child {{
            border-top-left-radius: 12px;
        }}
        table.dataframe tr:first-child th:last-child {{
            border-top-right-radius: 12px;
        }}
        table.dataframe tr:last-child td:first-child {{
            border-bottom-left-radius: 12px;
        }}
        table.dataframe tr:last-child td:last-child {{
            border-bottom-right-radius: 12px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("airplane.jpg")

# ===== ĐỌC FILE EXCEL =====
excel_file = "A787.xlsx"
xls = pd.ExcelFile(excel_file)

# ===== APP =====
st.markdown('<div class="animated-title">Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🔎 Tra cứu Part Number (PN)</div>', unsafe_allow_html=True)

# --- Bước 1: chọn sheet (zone) ---
sheet_name = st.selectbox("📂 Bạn muốn tra cứu zone nào?", xls.sheet_names, key="sheet")

if sheet_name:
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    df.columns = df.columns.str.strip().str.upper()

    # Map cột không đồng nhất
    rename_map = {
        "PN INTERCHANGE": "PART INTERCHANGE",
        "P/N INTERCHANGE": "PART INTERCHANGE",
        "INTERCHANGE": "PART INTERCHANGE",
    }
    df = df.rename(columns=lambda x: rename_map.get(x, x))

    # Chuẩn hóa dữ liệu text
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
                .str.upper()
            )
            df[col] = df[col].replace(["NAN", "NaN", "nan", "NONE"], None)

    # --- Bước 2: chọn A/C ---
    if "A/C" in df.columns:
        aircrafts = sorted([x for x in df["A/C"].dropna().unique() if str(x).strip() != ""])
        aircraft = st.selectbox("✈️ Loại máy bay?", aircrafts, key="aircraft")

        if aircraft:
            # --- Bước 3: chọn Description ---
            if "DESCRIPTION" in df.columns:
                descriptions = sorted([x for x in df[df["A/C"] == aircraft]["DESCRIPTION"].dropna().unique() if str(x).strip() != ""])
                description = st.selectbox("📑 Bạn muốn tra cứu phần nào?", descriptions, key="description")

                if description:
                    # --- Nếu có cột ITEM thì hỏi thêm ---
                    if "ITEM" in df.columns:
                        items = sorted(
                            [x for x in df[(df["A/C"] == aircraft) & (df["DESCRIPTION"] == description)]["ITEM"].dropna().unique() if str(x).strip() != ""]
                        )
                        if items:
                            item = st.selectbox("📌 Bạn muốn tra cứu Item nào?", items, key="item")
                        else:
                            item = None
                    else:
                        item = None

                    # --- Lọc kết quả ---
                    result = df[(df["A/C"] == aircraft) & (df["DESCRIPTION"] == description)]
                    if item:
                        result = result[result["ITEM"] == item]

                    # --- Hiển thị kết quả ---
                    if not result.empty:
                        st.success(f"Tìm thấy {len(result)} dòng dữ liệu:")

                        # Chỉ hiển thị PN, PN Interchange, Note
                        cols = []
                        if "PART NUMBER (PN)" in df.columns:
                            cols.append("PART NUMBER (PN)")
                        if "PART INTERCHANGE" in df.columns:
                            cols.append("PART INTERCHANGE")
                        if "NOTE" in df.columns:
                            cols.append("NOTE")

                        result_display = result[cols].reset_index(drop=True)
                        result_display.index = result_display.index + 1
                        result_display.index.name = "STT"

                        # Bỏ NAN trong bảng kết quả
                        result_display = result_display.replace(["NAN", "NaN", "nan", "NONE"], "")

                        styled = (
                            result_display.style
                            .set_properties(**{
                                "text-align": "center",
                                "vertical-align": "middle",
                                "white-space": "nowrap",
                                "color": "black",
                                "background-color": "white"
                            })
                        )

                        st.markdown('<div class="scroll-container">', unsafe_allow_html=True)
                        st.table(styled)
                        st.markdown('</div>', unsafe_allow_html=True)

                    else:
                        st.error("Không tìm thấy dữ liệu!")
            else:
                st.warning("Sheet này không có cột DESCRIPTION!")
    else:
        st.warning("Sheet này không có cột A/C!")
