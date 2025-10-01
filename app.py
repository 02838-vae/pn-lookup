import pandas as pd
import streamlit as st

# Đọc dữ liệu
df = pd.read_excel("A787.xlsx")

# Chuẩn hóa tên cột
df.columns = df.columns.str.strip().str.upper()

st.write("📑 Các cột trong file:", df.columns.tolist())  # Debug: xem cột thực tế

# Chuẩn hóa text ở các cột cần thiết (chỉ nếu cột có tồn tại)
for col in ["CATEGORY", "A/C", "DESCRIPTION"]:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .str.upper()
        )
        df[col] = df[col].replace("NAN", None)  # bỏ chữ NAN giả

st.title("🔎 Tra cứu Part Number (PN)")

# --- STATE ---
if "category" not in st.session_state:
    st.session_state.category = None
if "aircraft" not in st.session_state:
    st.session_state.aircraft = None
if "description" not in st.session_state:
    st.session_state.description = None


# --- Step 1: chọn Category ---
categories = sorted(df["CATEGORY"].dropna().unique())
category = st.selectbox(
    "📂 Bạn muốn tra cứu gì?",
    categories,
    index=categories.index(st.session_state.category) if st.session_state.category else 0,
    key="category",
)

if category:
    # --- Step 2: chọn A/C ---
    aircrafts = sorted(
        df[df["CATEGORY"] == category]["A/C"].dropna().unique()
    )
    aircraft = st.selectbox(
        "✈️ Loại tàu nào?",
        aircrafts,
        index=aircrafts.index(st.session_state.aircraft) if st.session_state.aircraft else 0,
        key="aircraft",
    )

    if aircraft:
        # --- Step 3: chọn Description ---
        descriptions = sorted(
            df[
                (df["CATEGORY"] == category)
                & (df["A/C"] == aircraft)
            ]["DESCRIPTION"].dropna().unique()
        )

        description = st.selectbox(
            "📑 Bạn muốn tra cứu Item nào?",
            descriptions,
            index=descriptions.index(st.session_state.description) if st.session_state.description else 0,
            key="description",
        )

        if description:
            # --- Step 4: Kết quả ---
            result = df[
                (df["CATEGORY"] == category)
                & (df["A/C"] == aircraft)
                & (df["DESCRIPTION"] == description)
            ]

            if not result.empty:
                st.success(f"Tìm thấy {len(result)} dòng dữ liệu:")
                cols = ["PART NUMBER (PN)", "DESCRIPTION"]
                if "NOTE" in df.columns:
                    cols.append("NOTE")
                st.dataframe(result[cols].reset_index(drop=True))
            else:
                st.error("Không tìm thấy dữ liệu!")


