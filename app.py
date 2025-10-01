import pandas as pd
import streamlit as st

# ============ ĐỌC & XỬ LÝ DỮ LIỆU ============
df = pd.read_excel("A787.xlsx")

# Chuẩn hóa tên cột
df.columns = df.columns.str.strip().str.upper()

# Map tên cột nếu trong Excel khác chuẩn
rename_map = {
    "CAT": "CATEGORY",
    "CATEGORY ": "CATEGORY",
    "AC": "A/C",
    "AIRCRAFT": "A/C",
    "DESC": "DESCRIPTION",
    "DESCRIPTIONS": "DESCRIPTION",
    "PN": "PART NUMBER (PN)",
    "PART NUMBER": "PART NUMBER (PN)",
}
df = df.rename(columns=lambda x: rename_map.get(x, x))

# Debug: hiện tên cột (giúp check lần đầu, có thể tắt đi sau)
st.write("📑 Các cột sau khi chuẩn hóa:", df.columns.tolist())

# Chuẩn hóa text trong các cột quan trọng
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


# ============ APP ============
st.title("🔎 Tra cứu Part Number (PN)")

# Reset nút
if st.button("🔄 Tra cứu lại"):
    st.session_state.clear()
    st.rerun()

# --- Step 1: chọn Category ---
if "CATEGORY" not in df.columns:
    st.error("⚠️ File Excel không có cột CATEGORY (hoặc chưa map đúng).")
else:
    categories = sorted(df["CATEGORY"].dropna().unique())
    category = st.selectbox("📂 Bạn muốn tra cứu gì?", categories, key="category")

    if category:
        # --- Step 2: chọn A/C ---
        if "A/C" not in df.columns:
            st.error("⚠️ File Excel không có cột A/C (hoặc chưa map đúng).")
        else:
            aircrafts = sorted(
                df[df["CATEGORY"] == category]["A/C"].dropna().unique()
            )
            aircraft = st.selectbox("✈️ Loại tàu nào?", aircrafts, key="aircraft")

            if aircraft:
                # --- Step 3: chọn Description ---
                if "DESCRIPTION" not in df.columns:
                    st.error("⚠️ File Excel không có cột DESCRIPTION (hoặc chưa map đúng).")
                else:
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
