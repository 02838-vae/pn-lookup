import pandas as pd
import streamlit as st

# ============ ĐỌC FILE & LẤY DANH SÁCH SHEET ============
excel_file = "A787.xlsx"
xls = pd.ExcelFile(excel_file)

# ============ APP ============
st.title("🔎 Tra cứu Part Number (PN)")

# --- Bước 1: chọn sheet ---
sheet_name = st.selectbox("📂 Bạn muốn tra cứu zone nào?", xls.sheet_names, key="sheet")

if sheet_name:
    # Đọc dữ liệu từ sheet đã chọn
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    # Chuẩn hóa tên cột
    df.columns = df.columns.str.strip().str.upper()

    # Map tên cột không đồng nhất về chuẩn
    rename_map = {
        "PN INTERCHANGE": "PART INTERCHANGE",
        "P/N INTERCHANGE": "PART INTERCHANGE",
        "INTERCHANGE": "PART INTERCHANGE",
    }
    df = df.rename(columns=lambda x: rename_map.get(x, x))

    # Chuẩn hóa text các cột dạng chuỗi
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
                .str.upper()
            )
            df[col] = df[col].replace("NAN", None)

    # --- Bước 2: chọn A/C ---
    if "A/C" in df.columns:
        aircrafts = sorted(df["A/C"].dropna().unique())
        aircraft = st.selectbox("✈️ Loại máy bay?", aircrafts, key="aircraft")

        if aircraft:
            # --- Bước 3: chọn Description ---
            if "DESCRIPTION" in df.columns:
                descriptions = sorted(
                    df[df["A/C"] == aircraft]["DESCRIPTION"].dropna().unique()
                )
                description = st.selectbox(
                    "📑 Bạn muốn tra cứu phần nào?",
                    descriptions,
                    key="description"
                )

                if description:
                    # --- Nếu có cột ITEM thì hỏi thêm ---
                    if "ITEM" in df.columns:
                        items = sorted(
                            df[
                                (df["A/C"] == aircraft)
                                & (df["DESCRIPTION"] == description)
                            ]["ITEM"].dropna().unique()
                        )
                        if items:
                            item = st.selectbox("📌 Bạn muốn tra cứu Item nào?", items, key="item")
                        else:
                            item = None
                    else:
                        item = None

                    # --- Lọc kết quả ---
                    result = df[
                        (df["A/C"] == aircraft)
                        & (df["DESCRIPTION"] == description)
                    ]
                    if item:
                        result = result[result["ITEM"] == item]

                    # --- Hiển thị kết quả ---
                    if not result.empty:
                        st.success(f"Tìm thấy {len(result)} dòng dữ liệu:")

                        # Chọn các cột cần hiển thị
                        cols = []
                        if "PART NUMBER (PN)" in df.columns:
                            cols.append("PART NUMBER (PN)")
                        if "PART INTERCHANGE" in df.columns:
                            cols.append("PART INTERCHANGE")
                        if "DESCRIPTION" in df.columns:
                            cols.append("DESCRIPTION")
                        if "ITEM" in df.columns and item:
                            cols.append("ITEM")
                        if "NOTE" in df.columns:
                            cols.append("NOTE")

                        # Xử lý xuống dòng trong PART INTERCHANGE
                        if "PART INTERCHANGE" in result.columns:
                            result["PART INTERCHANGE"] = (
                                result["PART INTERCHANGE"]
                                .astype(str)
                                .apply(lambda x: x.replace(";", "\n").replace(",", "\n").replace("/", "\n"))
                            )

                        # Xuất bảng HTML có CSS căn giữa & hỗ trợ xuống dòng
                        html_table = result[cols].reset_index(drop=True).to_html(
                            escape=False,
                            index=False
                        )
                        html_table = f"""
                        <style>
                        table {{
                          width: 100%;
                          border-collapse: collapse;
                        }}
                        th, td {{
                          border: 1px solid #ddd;
                          padding: 8px;
                          text-align: center;
                          vertical-align: middle;
                          white-space: pre-line;
                        }}
                        th {{
                          background-color: #f2f2f2;
                        }}
                        </style>
                        {html_table}
                        """
                        st.markdown(html_table, unsafe_allow_html=True)
                    else:
                        st.error("Không tìm thấy dữ liệu!")
            else:
                st.warning("Sheet này không có cột DESCRIPTION!")
    else:
        st.warning("Sheet này không có cột A/C!")
