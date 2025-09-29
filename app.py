import pandas as pd
import streamlit as st

# Đọc dữ liệu
df = pd.read_excel("A787.xlsx")

# Chuẩn hóa text
for col in ["CATEGORY", "A/C", "DESCRIPTION"]:
    df[col] = (
        df[col].astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.upper()
    )
    df[col] = df[col].replace("NAN", None)  # bỏ chữ NAN giả

st.title("🔎 Tra cứu Part Number (PN)")

# Khởi tạo state
if "step" not in st.session_state:
    st.session_state.step = 1
if "category" not in st.session_state:
    st.session_state.category = None
if "aircraft" not in st.session_state:
    st.session_state.aircraft = None
if "keyword" not in st.session_state:
    st.session_state.keyword = None


# Step 1: chọn Category
if st.session_state.step == 1:
    categories = sorted(df["CATEGORY"].dropna().unique())
    category = st.selectbox("📂 Bạn muốn tra cứu gì?", categories)

    if st.button("Tiếp tục ➡️"):
        st.session_state.category = category
        st.session_state.step = 2
        st.rerun()

# Step 2: chọn A/C
elif st.session_state.step == 2:
    st.write(f"✅ Category: **{st.session_state.category}**")
    aircrafts = sorted(
        df[df["CATEGORY"] == st.session_state.category]["A/C"].dropna().unique()
    )
    aircraft = st.selectbox("✈️ Loại tàu nào?", aircrafts)

    col1, col2 = st.columns(2)
    if col1.button("⬅️ Quay lại"):
        st.session_state.step = 1
        st.rerun()
    if col2.button("Tiếp tục ➡️"):
        st.session_state.aircraft = aircraft
        st.session_state.step = 3
        st.rerun()

# Step 3: chọn từ khóa trong Description
elif st.session_state.step == 3:
    st.write(f"✅ Category: **{st.session_state.category}**")
    st.write(f"✅ A/C: **{st.session_state.aircraft}**")

    # Lấy toàn bộ mô tả theo category + aircraft
    subset = df[
        (df["CATEGORY"] == st.session_state.category)
        & (df["A/C"] == st.session_state.aircraft)
    ]["DESCRIPTION"].dropna()

    # Tách từ khóa (ví dụ: lấy từ đầu tiên trong mô tả)
    keywords = sorted(set(desc.split()[0] for desc in subset if isinstance(desc, str)))

    keyword = st.selectbox("📑 Bạn muốn tra cứu theo từ khóa nào?", keywords)

    col1, col2 = st.columns(2)
    if col1.button("⬅️ Quay lại"):
        st.session_state.step = 2
        st.rerun()
    if col2.button("Xem kết quả ✅"):
        st.session_state.keyword = keyword
        st.session_state.step = 4
        st.rerun()

# Step 4: Hiện kết quả
elif st.session_state.step == 4:
    st.write(f"✅ Category: **{st.session_state.category}**")
    st.write(f"✅ A/C: **{st.session_state.aircraft}**")
    st.write(f"✅ Từ khóa Description: **{st.session_state.keyword}**")

    # Lọc tất cả DESCRIPTION có chứa từ khóa
    result = df[
        (df["CATEGORY"] == st.session_state.category)
        & (df["A/C"] == st.session_state.aircraft)
        & (df["DESCRIPTION"].str.contains(st.session_state.keyword, na=False))
    ]

    if not result.empty:
        st.success(f"Tìm thấy {len(result)} dòng dữ liệu:")
        cols = ["PART NUMBER (PN)", "DESCRIPTION"]
        if "NOTE" in df.columns:
            cols.append("NOTE")
        st.dataframe(result[cols].reset_index(drop=True))
    else:
        st.error("Không tìm thấy dữ liệu!")

    if st.button("🔄 Tra cứu lại"):
        st.session_state.step = 1
        st.rerun()
