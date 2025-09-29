import pandas as pd 
import streamlit as st

# Đọc dữ liệu
df = pd.read_excel("A787.xlsx")
df = df.dropna(subset=["DESCRIPTION", "PART NUMBER (PN)"])

# Chuẩn hóa dữ liệu (xóa khoảng trắng thừa, đồng bộ chữ hoa/thường)
df["DESCRIPTION"] = df["DESCRIPTION"].astype(str).str.strip()
df["CATEGORY"] = df["CATEGORY"].astype(str).str.strip()

# Tiêu đề app
st.title("🔎 Tra cứu Part Number (PN)")

# Bước 1: chọn Category
categories = sorted(df["CATEGORY"].dropna().unique())
category = st.selectbox("Bạn muốn tra cứu gì?", categories)

if category:
    # Bước 2: chọn Description theo Category (lọc sạch NaN + sort)
    descriptions = sorted(df[df["CATEGORY"] == category]["DESCRIPTION"].dropna().unique())
    description = st.selectbox("Bạn muốn tra cứu Description nào?", descriptions)

    if description:
        # Lọc tất cả dòng có DESCRIPTION chứa text description (không chỉ exact match)
        result = df[(df["CATEGORY"] == category) & (df["DESCRIPTION"].str.contains(description, case=False, na=False))]

        if not result.empty:
            st.success(f"Tìm thấy {len(result)} dòng dữ liệu:")

            cols_to_show = ["PART NUMBER (PN)", "DESCRIPTION"]
            if "NOTE" in df.columns:
                cols_to_show.append("NOTE")

            st.dataframe(result[cols_to_show].reset_index(drop=True))
        else:
            st.error("Rất tiếc, dữ liệu bạn nhập chưa có")
