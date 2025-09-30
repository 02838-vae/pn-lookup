import pandas as pd
import streamlit as st


# ================== ĐỌC FILE EXCEL ==================
def load_data(file_path: str) -> pd.DataFrame:
    # Đọc tất cả sheet
    all_sheets = pd.read_excel(file_path, sheet_name=None)

    df_list = []
    for sheet_name, sheet_df in all_sheets.items():
        if not sheet_df.empty:
            # Thêm cột CATEGORY = tên sheet
            sheet_df["CATEGORY"] = sheet_name.upper().strip()
            df_list.append(sheet_df)
        else:
            print(f"⚠️ Sheet {sheet_name} trống!")

    # Ghép tất cả sheet lại
    df = pd.concat(df_list, ignore_index=True)

    # Chuẩn hóa text
    for col in ["CATEGORY", "A/C", "DESCRIPTION", "ITEM"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
                .str.upper()
            )
            df[col] = df[col].replace("NAN", None)

    # Debug: hiển thị danh sách CATEGORY
    st.sidebar.write("📑 Categories hiện có:", df["CATEGORY"].unique())
    return df


# ================== HÀM HIỂN THỊ THEO BƯỚC ==================
def step_category(df):
    categories = sorted(df["CATEGORY"].dropna().unique())
    category = st.selectbox("📂 Bạn muốn tra cứu gì?", categories)
    if st.button("Tiếp tục ➡️"):
        st.session_state.category = category
        st.session_state.step = 2
        st.rerun()


def step_aircraft(df):
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


def step_description(df):
    st.write(f"✅ Category: **{st.session_state.category}**")
    st.write(f"✅ A/C: **{st.session_state.aircraft}**")

    descriptions = sorted(
        df[
            (df["CATEGORY"] == st.session_state.category)
            & (df["A/C"] == st.session_state.aircraft)
        ]["DESCRIPTION"].dropna().unique()
    )
    description = st.selectbox("📑 Bạn muốn tra cứu Item nào?", descriptions)

    col1, col2 = st.columns(2)
    if col1.button("⬅️ Quay lại"):
        st.session_state.step = 2
        st.rerun()
    if col2.button("Tiếp tục ➡️"):
        st.session_state.description = description

        # Nếu có cột Item trong sheet → sang bước 3.5
        df_filtered = df[
            (df["CATEGORY"] == st.session_state.category)
            & (df["A/C"] == st.session_state.aircraft)
            & (df["DESCRIPTION"] == description)
        ]
        if "ITEM" in df_filtered.columns and df_filtered["ITEM"].notna().any():
            st.session_state.step = 3.5
        else:
            st.session_state.step = 4
        st.rerun()


def step_item(df):
    st.write(f"✅ Category: **{st.session_state.category}**")
    st.write(f"✅ A/C: **{st.session_state.aircraft}**")
    st.write(f"✅ Description: **{st.session_state.description}**")

    items = sorted(
        df[
            (df["CATEGORY"] == st.session_state.category)
            & (df["A/C"] == st.session_state.aircraft)
            & (df["DESCRIPTION"] == st.session_state.description)
        ]["ITEM"].dropna().unique()
    )
    item = st.selectbox("🔢 Bạn muốn chọn loại nào?", items)

    col1, col2 = st.columns(2)
    if col1.button("⬅️ Quay lại"):
        st.session_state.step = 3
        st.rerun()
    if col2.button("Xem kết quả ✅"):
        st.session_state.item = item
        st.session_state.step = 4
        st.rerun()


def step_result(df):
    st.write(f"✅ Category: **{st.session_state.category}**")
    st.write(f"✅ A/C: **{st.session_state.aircraft}**")
    st.write(f"✅ Description: **{st.session_state.description}**")
    if "item" in st.session_state and st.session_state.item:
        st.write(f"✅ Item: **{st.session_state.item}**")

    # Filter kết quả
    result = df[
        (df["CATEGORY"] == st.session_state.category)
        & (df["A/C"] == st.session_state.aircraft)
        & (df["DESCRIPTION"] == st.session_state.description)
    ]
    if "item" in st.session_state and st.session_state.item:
        result = result[result["ITEM"] == st.session_state.item]

    if not result.empty:
        st.success(f"Tìm thấy {len(result)} dòng dữ liệu:")
        cols = [c for c in ["PART NUMBER (PN)", "DESCRIPTION", "ITEM", "PN INTERCHANGE", "NOTE"] if c in result.columns]
        st.dataframe(result[cols].reset_index(drop=True))
    else:
        st.error("Không tìm thấy dữ liệu!")

    if st.button("🔄 Tra cứu lại"):
        st.session_state.step = 1
        st.session_state.category = None
        st.session_state.aircraft = None
        st.session_state.description = None
        st.session_state.item = None
        st.rerun()


# ================== MAIN APP ==================
def main():
    st.title("🔎 Tra cứu Part Number (PN)")

    df = load_data("A787.xlsx")

    # Khởi tạo session state
    if "step" not in st.session_state:
        st.session_state.step = 1
        st.session_state.category = None
        st.session_state.aircraft = None
        st.session_state.description = None
        st.session_state.item = None

    # Điều hướng theo step
    if st.session_state.step == 1:
        step_category(df)
    elif st.session_state.step == 2:
        step_aircraft(df)
    elif st.session_state.step == 3:
        step_description(df)
    elif st.session_state.step == 3.5:
        step_item(df)
    elif st.session_state.step == 4:
        step_result(df)


if __name__ == "__main__":
    main()
