import pandas as pd
import streamlit as st

# ============ ĐỌC & XỬ LÝ DỮ LIỆU ============
df = pd.read_excel("A787.xlsx")

# Ép cột đầu tiên, thứ hai, thứ ba thành chuẩn
col_map = {
    df.columns[0]: "CATEGORY",
    df.columns[1]: "A/C",
    df.columns[2]: "DESCRIPTION",
}
df = df.rename(columns=col_map)

# Chuẩn hóa text trong các cột chính
for col in ["CATEGORY", "A/C", "DESCRIPTION"]:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .str.upper()
        )
        df[col] = df[col].replace("NAN", None)

# ============ APP ============
st.title("🔎 Tra cứu Part Number (PN)")

# Nút reset
if st.button("🔄 Tra cứu lại"):
    st.session_state.clear()
    st.rerun()

# --- Step 1: chọn Category ---
categories = sorted(df["CATEGORY"].dropna().unique())
category = st.selectbox("📂 Bạn muốn tra cứu gì?", categories, key="category")

if category:
    # --- Step 2: chọn A/C ---
    aircrafts = sorted(
        df[df["CATEGORY"] == category]["A/C"].dropna().unique()
    )
    aircraft = st.selectbox("✈️ Loại tàu nào?", aircrafts, key="aircraft")

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
            key="description",
        )

        if description:
            # --- Step 4: Hiện kết quả ---
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
