import pandas as pd 
import streamlit as st

# Đọc dữ liệu
df = pd.read_excel("A787.xlsx")
df = df.dropna(subset=["DESCRIPTION", "PART NUMBER (PN)"])

# Tiêu đề app
st.title("🔎 Tra cứu Part Number (PN)")

# Bước 1: chọn Category
categories = df["CATEGORY"].dropna().unique()
category = st.selectbox("Bạn muốn tra cứu gì?", categories)

if category:
    # Bước 2: chọn Description theo Category
    descriptions = df[df["CATEGORY"] == category]["DESCRIPTION"].dropna().unique()
    description = st.selectbox("Bạn muốn tra cứu Description nào?", descriptions)

    if description:
        # Bước 3: tìm PN + Note
        result = df[(df["CATEGORY"] == category) & (df["DESCRIPTION"] == description)]
        if not result.empty:
            st.success(f"Tìm thấy {len(result)} dòng dữ liệu:")

            # Chỉ hiển thị các cột quan trọng
            cols_to_show = ["PART NUMBER (PN)", "DESCRIPTION", "NOTE"] if "NOTE" in df.columns else ["PART NUMBER (PN)", "DESCRIPTION"]
            st.dataframe(result[cols_to_show].reset_index(drop=True))
        else:
            st.error("Rất tiếc, dữ liệu bạn nhập chưa có")
