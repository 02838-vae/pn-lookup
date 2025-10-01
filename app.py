import pandas as pd
import streamlit as st
import base64

# ===== CSS: Background với hình airplane.jpg =====
def set_background(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/jpg;base64,{b64}") no-repeat center center fixed;
            background-size: cover;
            position: relative;
        }}
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: url("data:image/jpg;base64,{b64}") no-repeat center center fixed;
            background-size: cover;
            filter: blur(8px) brightness(0.4);   /* mờ + tối nhẹ */
            z-index: -2;
        }}
        .stApp::after {{
            content: "";
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(255,255,255,0.6);   /* overlay trắng mờ */
            z-index: -1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("airplane.jpg")

# ===== ĐỌC FILE & DANH SÁCH SHEET =====
excel_file = "A787.xlsx"
xls = pd.ExcelFile(excel_file)

# ===== APP =====
st.title("🔎 Tra cứu Part Number (PN)")

# --- Bước 1: chọn sheet (zone) ---
sheet_name = st.selectbox("📂 Bạn muốn tra cứu zone nào?", xls.sheet_names, key="sheet")

if sheet_name:
    # Đọc dữ liệu từ sheet đã chọn
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    # Chuẩn hóa tên cột
    df.columns = df.columns.str.strip().str.upper()

    # Map tên cột không đồng nhất
    rename_map = {
        "PN INTERCHANGE": "PART INTERCHANGE",
        "P/N INTERCHANGE": "PART INTERCHANGE",
        "INTERCHANGE": "PART INTERCHANGE",
    }
    df = df.rename(columns=lambda x: rename_map.get(x, x))

    # Chuẩn hóa dữ liệu text
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
                .str.upper()
            )
            df[col] = df[col].replace("NAN", None)

    # --- Bước 2: chọn A/C ---
    if "A/C" in df.columns:
        aircrafts = sorted(df["A/C"].dropna().unique())
        aircraft = st.selectbox("✈️ Loại máy bay?", aircrafts, key="aircraft")

        if aircraft:
            # --- Bước 3: chọn Description ---
            if "DESCRIPTION" in df.columns:
                descriptions = sorted(
                    df[df["A/C"] == aircraft]["DESCRIPTION"].dropna().unique()
                )
                description = st.selectbox(
                    "📑 Bạn muốn tra cứu phần nào?",
                    descriptions,
                    key="description"
                )

                if description:
                    # --- Nếu có cột ITEM thì hỏi thêm ---
                    if "ITEM" in df.columns:
                        items = sorted(
                            df[
                                (df["A/C"] == aircraft)
                                & (df["DESCRIPTION"] == description)
                            ]["ITEM"].dropna().unique()
                        )
                        if items:
                            item = st.selectbox("📌 Bạn muốn tra cứu Item nào?", items, key="item")
                        else:
                            item = None
                    else:
                        item = None

                    # --- Lọc kết quả ---
                    result = df[
                        (df["A/C"] == aircraft)
                        & (df["DESCRIPTION"] == description)
                    ]
                    if item:
                        result = result[result["ITEM"] == item]

                    # --- Hiển thị kết quả ---
                    if not result.empty:
                        st.success(f"Tìm thấy {len(result)} dòng dữ liệu:")

                        # Chọn cột hiển thị
                        cols = []
                        if "PART NUMBER (PN)" in df.columns:
                            cols.append("PART NUMBER (PN)")
                        if "PART INTERCHANGE" in df.columns:
                            cols.append("PART INTERCHANGE")
                        if "DESCRIPTION" in df.columns:
                            cols.append("DESCRIPTION")
                        if "ITEM" in df.columns and item:
                            cols.append("ITEM")
                        if "NOTE" in df.columns:
                            cols.append("NOTE")

                        # ✅ Style bảng: căn giữa, font đẹp, màu nền xen kẽ, bo góc + đổ bóng
                        styled = (
                            result[cols].reset_index(drop=True)
                            .style.set_properties(
                                **{
                                    "text-align": "center",
                                    "vertical-align": "middle",
                                    "font-family": "'Segoe UI','Helvetica Neue',Arial,sans-serif",
                                    "font-size": "14px",
                                }
                            )
                            .set_table_styles(
                                [
                                    {"selector": "tbody tr:nth-child(even)",
                                     "props": [("background-color", "#f9f9f9")]},
                                    {"selector": "tbody tr:nth-child(odd)",
                                     "props": [("background-color", "#ffffff")]},
                                    {"selector": "thead th",
                                     "props": [("background-color", "#e6f2ff"),
                                               ("font-weight", "bold"),
                                               ("text-align", "center")]},
                                    {"selector": "table",
                                     "props": [("border-collapse", "collapse"),
                                               ("border-radius", "12px"),
                                               ("box-shadow", "0 4px 12px rgba(0,0,0,0.15)"),
                                               ("overflow", "hidden")]}
                                ]
                            )
                        )

                        st.dataframe(styled, use_container_width=True)

                    else:
                        st.error("Không tìm thấy dữ liệu!")
            else:
                st.warning("Sheet này không có cột DESCRIPTION!")
    else:
        st.warning("Sheet này không có cột A/C!")
