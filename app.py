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

# APP
st.title("🔎 Tra cứu Part Number (PN)")

categories = sorted(df["CATEGORY"].dropna().unique())
category = st.selectbox("Bạn muốn tra cứu gì?", categories)

if category:
    descriptions = sorted(df[df["CATEGORY"] == category]["DESCRIPTION"].dropna().unique())
    description = st.selectbox("Bạn muốn tra cứu Description nào?", descriptions)

    if description:
        result = df[(df["CATEGORY"] == category) & (df["DESCRIPTION"] == description)]

        if not result.empty:
            st.success(f"Tìm thấy {len(result)} dòng dữ liệu:")
            cols_to_show = ["PART NUMBER (PN)", "DESCRIPTION"]
            if "NOTE" in df.columns:
                cols_to_show.append("NOTE")
            st.dataframe(result[cols_to_show].reset_index(drop=True))
        else:
            st.error("Rất tiếc, dữ liệu bạn nhập chưa có")
