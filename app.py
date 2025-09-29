import pandas as pd
import streamlit as st

# Đọc dữ liệu
df = pd.read_excel("A787.xlsx")

# Điền CATEGORY và A/C còn thiếu bằng giá trị trước đó
df["CATEGORY"] = df["CATEGORY"].ffill()
df["A/C"] = df["A/C"].ffill()

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

# Bước 1: chọn Category
categories = sorted(df["CATEGORY"].dropna().unique())
category = st.selectbox("📂 Bạn muốn tra cứu gì?", categories)

if category:
    # Bước 2: chọn loại tàu theo Category
    aircrafts = sorted(df[df["CATEGORY"] == category]["A/C"].dropna().unique())
    aircraft = st.selectbox("✈️ Loại tàu nào?", aircrafts)

    if aircraft:
        # Bước 3: chọn Description theo Category + loại tàu
        descriptions = sorted(
            df[(df["CATEGORY"] == category) & (df["A/C"] == aircraft)]["DESCRIPTION"].dropna().unique()
        )
        description = st.selectbox("📑 Bạn muốn tra cứu Item nào?", descriptions)

        if description:
            # Lọc kết quả
            result = df[
                (df["CATEGORY"] == category)
                & (df["A/C"] == aircraft)
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
