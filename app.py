import pandas as pd
import streamlit as st

# =================== PAGE CONFIG ===================
st.set_page_config(page_title="PN Lookup", layout="wide")

# =================== CUSTOM CSS ===================
st.markdown(
    """
    <style>
    /* Tiêu đề trên cùng đổi màu liên tục */
    .rainbow-text {
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        animation: rainbow 6s infinite;
    }
    @keyframes rainbow {
        0% {color: red;}
        20% {color: orange;}
        40% {color: yellow;}
        60% {color: green;}
        80% {color: blue;}
        100% {color: violet;}
    }

    /* Tiêu đề chính */
    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 30px;
        color: #003366;
    }

    /* Label dropdown (câu hỏi) */
    label, .stSelectbox label {
        font-weight: 700 !important;
        color: #222 !important;
    }

    /* Bảng kết quả */
    table {
        border-collapse: collapse;
        margin: 0 auto;
        font-size: 14px;
        width: 100%;
    }
    th {
        background-color: #d9eaf7 !important;
        color: #000 !important;
        text-align: center !important;
        font-weight: bold !important;
        padding: 8px !important;
    }
    td {
        text-align: center !important;
        vertical-align: middle !important;
        color: #000 !important;
        padding: 6px !important;
        white-space: nowrap !important;  /* không xuống dòng */
    }
    .dataframe {
        border: 2px solid #666 !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =================== HEADER ===================
st.markdown('<div class="rainbow-text">Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🔎 Tra cứu Part Number (PN)</div>', unsafe_allow_html=True)

# =================== LOAD EXCEL ===================
file_path = "A787.xlsx"
xls = pd.ExcelFile(file_path)
sheet_names = xls.sheet_names

# =================== APP ===================
zone = st.selectbox("📂 Bạn muốn tra cứu zone nào?", sheet_names)

if zone:
    df = pd.read_excel(file_path, sheet_name=zone)

    # Chuẩn hóa text
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
                .str.upper()
            )

    # Loại bỏ NaN
    df = df.dropna(how="all")

    # Hỏi loại máy bay
    if "A/C" in df.columns:
        aircrafts = sorted(df["A/C"].dropna().unique())
        aircraft = st.selectbox("✈️ Loại máy bay?", aircrafts)
    else:
        aircraft = None

    if aircraft:
        df = df[df["A/C"] == aircraft]

        # Hỏi phần nào
        desc_col = "DESCRIPTION" if "DESCRIPTION" in df.columns else "ITEM"
        descriptions = sorted(df[desc_col].dropna().unique())
        description = st.selectbox("📑 Bạn muốn tra cứu phần nào?", descriptions)

        if description:
            df = df[df[desc_col] == description]

            # Nếu có cột Item riêng
            item = None
            if "ITEM" in df.columns and desc_col != "ITEM":
                items = sorted(df["ITEM"].dropna().unique())
                item = st.selectbox("🧾 Bạn muốn tra cứu Item nào?", items)
                if item:
                    df = df[df["ITEM"] == item]

            if not df.empty:
                st.success(f"Tìm thấy {len(df)} dòng dữ liệu:")

                # Cột hiển thị (không hiển thị Description như bạn yêu cầu)
                cols = []
                if "PART NUMBER (PN)" in df.columns:
                    cols.append("PART NUMBER (PN)")
                if "PART INTERCHANGE" in df.columns:
                    cols.append("PART INTERCHANGE")
                if "ITEM" in df.columns and item:
                    cols.append("ITEM")
                if "NOTE" in df.columns:
                    cols.append("NOTE")

                result_display = df[cols].reset_index(drop=True)

                # Index 1,2,3 thay vì 0,1,2
                result_display.index = result_display.index + 1

                # Format PN Interchange xuống dòng
                if "PART INTERCHANGE" in result_display.columns:
                    result_display["PART INTERCHANGE"] = (
                        result_display["PART INTERCHANGE"]
                        .astype(str)
                        .str.replace(" ", "<br>")
                    )

                # Render đẹp bằng to_html
                st.markdown(
                    result_display.to_html(escape=False),
                    unsafe_allow_html=True
                )
            else:
                st.error("Rất tiếc, không tìm thấy dữ liệu phù hợp.")
