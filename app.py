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

# Nếu chưa chọn Category -> hiển thị dropdown Category
if "category" not in st.session_state:
    categories = sorted(df["CATEGORY"].dropna().unique())
    category = st.selectbox("📂 Bạn muốn tra cứu gì?", categories, key="category_select")

    if category:
        st.session_state["category"] = category
        st.rerun()

# Nếu đã chọn Category nhưng chưa chọn A/C -> hiển thị dropdown A/C
elif "aircraft" not in st.session_state:
    category = st.session_state["category"]
    aircrafts = sorted(df[df["CATEGORY"] == category]["A/C"].dropna().unique())
    aircraft = st.selectbox("✈️ Loại tàu nào?", aircrafts, key="aircraft_select")

    if aircraft:
        st.session_state["aircraft"] = aircraft
        st.rerun()

# Nếu đã chọn Category + A/C nhưng chưa chọn Description -> hiển thị dropdown Description
elif "description" not in st.session_state:
    category = st.session_state["category"]
    aircraft = st.session_state["aircraft"]
    descriptions = sorted(
        df[(df["CATEGORY"] == category) & (df["A/C"] == aircraft)]["DESCRIPTION"].dropna().unique()
    )
    description = st.selectbox("📑 Bạn muốn tra cứu Item nào?", descriptions, key="desc_select")

    if description:
        st.session_state["description"] = description
        st.rerun()

# Nếu đã chọn cả 3 -> hiển thị kết quả
else:
    category = st.session_state["category"]
    aircraft = st.session_state["aircraft"]
    description = st.session_state["description"]

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
        st.dataframe(result[cols_to_show].rese
