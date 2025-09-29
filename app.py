import pandas as pd
import streamlit as st

# Đọc dữ liệu
df = pd.read_excel("A787.xlsx")

# Điền CATEGORY còn thiếu bằng giá trị trước đó
df["CATEGORY"] = df["CATEGORY"].ffill()

# Xóa dòng không có DESCRIPTION hoặc PN
df = df.dropna(subset=["DESCRIPTION", "PART NUMBER (PN)"])

# Chuẩn hóa text
df["DESCRIPTION"] = (
    df["DESCRIPTION"]
    .astype(str)
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .str.upper()
)
df["CATEGORY"] = (
    df["CATEGORY"]
    .astype(str)
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .str.upper()
)
df["A/C"] = (
    df["A/C"]
    .astype(str)
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .str.upper()
)

# APP
st.title("🔎 Tra cứu Part Number (PN)")

# Bước 0: chọn loại tàu
aircrafts = sorted(df["A/C"].dropna().unique())
aircraft = st.selectbox("✈️ Loại tàu nào?", aircrafts)

if aircraft:
    # Bước 1: chọn Category
    categories = sorted(df[df["A/C"] == aircraft]["CATEGORY"].dropna().unique())
    category = st.selectbox("📂 Bạn muốn tra cứu gì?", categories)

    if category:
        # Bước 2: chọn Description theo Category
        descriptions = sorted(
            df[(df["A/C"] == aircraft) & (df["CATEGORY"] == category)]["DESCRIPTION"].dropna().unique()
        )
        description = st.selectbox("📑 Bạn muốn tra cứu Description nào?", descriptions)

        if description:
            # Lọc kết quả
            result = df[
                (df["A/C"] == aircraft)
                & (df["CATEGORY"] == category)
                & (df["DESCRIPTION"] == description)
            ]

            if not result.empty:
                st.success(f"Tìm thấy {len(result)} dòng dữ liệu:")
                cols_to_show = ["PART NUMBER (PN)", "DESCRIPTION"]
                if "NOTE" in df.columns:
                    cols_to_show.append("NOTE")
                st.dataframe(result[cols_to_show].reset_index(drop=True))
            else:
                st.error("Rất tiếc, dữ liệu bạn nhập chưa có")
