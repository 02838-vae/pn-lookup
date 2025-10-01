import pandas as pd
import streamlit as st

# ============ ĐỌC FILE & LẤY DANH SÁCH SHEET ============
excel_file = "A787.xlsx"
xls = pd.ExcelFile(excel_file)

# ============ APP ============
st.title("🔎 Tra cứu Part Number (PN)")

# --- Bước 1: chọn sheet ---
sheet_name = st.selectbox("📂 Bạn muốn tra cứu gì?", xls.sheet_names, key="sheet")

if sheet_name:
    # Đọc dữ liệu từ sheet đã chọn
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    # Chuẩn hóa tên cột
    df.columns = df.columns.str.strip().str.upper()

    # Map các cột cần thiết
    col_map = {}
    if "DESCRIPTION" in df.columns:
        col_map = {
            "A/C": "A/C",
            "DESCRIPTION": "DESCRIPTION",
        }
    elif "ITEM" in df.columns:
        col_map = {
            "A/C": "A/C",
            "ITEM": "DESCRIPTION",   # ép ITEM thành DESCRIPTION để xử lý chung
        }

    # Đổi tên cột theo chuẩn
    df = df.rename(columns=col_map)

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
            df[col] = df[col].replace("NAN", None)

    # --- Bước 2: chọn A/C ---
    if "A/C" in df.columns:
        aircrafts = sorted(df["A/C"].dropna().unique())
        aircraft = st.selectbox("✈️ Loại tàu nào?", aircrafts, key="aircraft")

        if aircraft:
            # --- Bước 3: chọn Description / Item ---
            if "DESCRIPTION" in df.columns:
                descriptions = sorted(
                    df[df["A/C"] == aircraft]["DESCRIPTION"].dropna().unique()
                )
                description = st.selectbox("📑 Bạn muốn tra cứu Item nào?", descriptions, key="description")

                if description:
                    result = df[(df["A/C"] == aircraft) & (df["DESCRIPTION"] == description)]

                    if not result.empty:
                        st.success(f"Tìm thấy {len(result)} dòng dữ liệu:")
                        cols = []
                        if "PART NUMBER (PN)" in df.columns:
                            cols.append("PART NUMBER (PN)")
                        if "DESCRIPTION" in df.columns:
                            cols.append("DESCRIPTION")
                        if "NOTE" in df.columns:
                            cols.append("NOTE")

                        st.dataframe(result[cols].reset_index(drop=True))
                    else:
                        st.error("Không tìm thấy dữ liệu!")
            else:
                st.warning("Sheet này không có cột DESCRIPTION hoặc ITEM!")
    else:
        st.warning("Sheet này không có cột A/C!")
