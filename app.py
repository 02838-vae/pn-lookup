import pandas as pd 
import streamlit as st

# Đọc dữ liệu
df = pd.read_excel("A787.xlsx")
df = df.dropna(subset=["DESCRIPTION", "PART NUMBER (PN)", "CATEGORY"])

# Chuẩn hóa dữ liệu (loại khoảng trắng + viết hoa)
df["DESCRIPTION"] = df["DESCRIPTION"].str.strip().str.upper()
df["CATEGORY"]   = df["CATEGORY"].str.strip().str.upper()

# Tiêu đề app
st.title("🔎 Tra cứu Part Number (PN)")

# Bước 1: chọn Category (không còn NaN)
categories = sorted(df["CATEGORY"].dropna().unique())
category = st.selectbox("Bạn muốn tra cứu gì?", categories)

if category:
    # Bước 2: chọn Description theo Category
    descriptions = sorted(df[df["CATEGORY"] == category]["DESCRIPTION"].dropna().unique())
    description = st.selectbox("Bạn muốn tra cứu Description nào?", descriptions)

    if description:
        # Lọc chính xác theo CATEGORY & DESCRIPTION (đã chuẩn hóa)
        result = df[(df["CATEGORY"] == category) & (df["DESCRIPTION"] == description)]

        if not result.empty:
            st.success(f"Tìm thấy {len(result)} dòng dữ liệu:")

            cols_to_show = ["PART NUMBER (PN)", "DESCRIPTION"]
            if "NOTE" in df.columns:
                cols_to_show.append("NOTE")

            st.dataframe(result[cols_to_show].reset_index(drop=True))
        else:
            st.error("Rất tiếc, dữ liệu bạn nhập chưa có")
