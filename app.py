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

# Gom nhóm: nếu DESCRIPTION chứa từ khóa nào đó, gán về 1 tên chuẩn
# Ví dụ: tất cả chứa "SNUBBER" -> gán thành "SNUBBER"
df.loc[df["DESCRIPTION"].str.contains("SNUBBER", na=False), "DESCRIPTION"] = "SNUBBER"

# Tiêu đề app
st.title("🔎 Tra cứu Part Number (PN)")

# Bước 1: chọn Category
categories = sorted(df["CATEGORY"].dropna().unique())
category = st.selectbox("Bạn muốn tra cứu gì?", categories)

if category:
    # Bước 2: chọn Description theo Category (đã gom nhóm)
    descriptions = sorted(df[df["CATEGORY"] == category]["DESCRIPTION"].dropna().unique())
    description = st.selectbox("Bạn muốn tra cứu Description nào?", descriptions)

    if description:
        # Lọc chính xác theo CATEGORY & DESCRIPTION (đã gom nhóm)
        result = df[(df["CATEGORY"] == category) & (df["DESCRIPTION"] == description)]

        if not result.empty:
            st.success(f"Tìm thấy {len(result)} dòng dữ liệu:")

            cols_to_show = ["PART NUMBER (PN)", "DESCRIPTION"]
            if "NOTE" in df.columns:
                cols_to_show.append("NOTE")

            st.dataframe(result[cols_to_show].reset_index(drop=True))
        else:
            st.error("Rất tiếc, dữ liệu bạn nhập chưa có")
