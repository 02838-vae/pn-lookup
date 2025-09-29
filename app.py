import pandas as pd
import streamlit as st

# Đọc dữ liệu
df = pd.read_excel("A787.xlsx")
df = df.dropna(subset=["DESCRIPTION", "PART NUMBER (PN)", "CATEGORY"])

# Chuẩn hóa dữ liệu
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

# Tạo cột nhóm (DESCRIPTION_GROUP)
df["DESCRIPTION_GROUP"] = df["DESCRIPTION"]

# Gom nhóm SNUBBER
df.loc[df["DESCRIPTION"].str.contains("SNUBBER", na=False), "DESCRIPTION_GROUP"] = "SNUBBER"

# --- APP ---
st.title("🔎 Tra cứu Part Number (PN)")

# Bước 1: chọn Category
categories = sorted(df["CATEGORY"].dropna().unique())
category = st.selectbox("Bạn muốn tra cứu gì?", categories)

if category:
    # Bước 2: chọn Description group theo Category
    descriptions = sorted(df[df["CATEGORY"] == category]["DESCRIPTION_GROUP"].dropna().unique())
    description = st.selectbox("Bạn muốn tra cứu Description nào?", descriptions)

    if description:
        # Lọc theo CATEGORY & DESCRIPTION_GROUP
        result = df[(df["CATEGORY"] == category) & (df["DESCRIPTION_GROUP"] == description)]

        if not result.empty:
            st.success(f"Tìm thấy {len(result)} dòng dữ liệu:")

            cols_to_show = ["PART NUMBER (PN)", "DESCRIPTION"]
            if "NOTE" in df.columns:
                cols_to_show.append("NOTE")

            # Hiển thị DESCRIPTION gốc để phân biệt các dòng khác nhau
            st.dataframe(result[cols_to_show].reset_index(drop=True))
        else:
            st.error("Rất tiếc, dữ liệu bạn nhập chưa có")
