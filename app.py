import streamlit as st
import pandas as pd

# Đọc toàn bộ file Excel
excel_file = "data.xlsx"
xls = pd.ExcelFile(excel_file)

# CSS tuỳ chỉnh
st.markdown("""
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
        }
        .main-title {
            font-size: 26px;
            font-weight: bold;
            text-align: center;
            margin-top: 10px;
            margin-bottom: 20px;
        }
        .sub-title {
            font-size: 22px;
            font-weight: bold;
            text-align: center;
            animation: color-change 4s infinite;
        }
        @keyframes color-change {
            0% {color: #ff4d4d;}
            25% {color: #ffa64d;}
            50% {color: #4dff4d;}
            75% {color: #4da6ff;}
            100% {color: #ff4dff;}
        }
        table.dataframe {
            width: 100% !important;
            border-collapse: collapse;
            border-radius: 12px;
            overflow: hidden;
            background-color: white;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
        }
        table.dataframe th {
            background-color: #2c3e50;
            color: white !important;
            font-weight: bold;
            text-align: center !important;
            padding: 10px;
            font-size: 14px;
        }
        table.dataframe td {
            text-align: center !important;
            padding: 8px;
            font-size: 13px;
            color: #2c3e50;
        }
    </style>
""", unsafe_allow_html=True)

# Tiêu đề động
st.markdown('<div class="sub-title">✈️ Tổ bảo dưỡng số 1</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🔎 Tra cứu Part number (PN)</div>', unsafe_allow_html=True)

# Dropdown chọn sheet
sheet_name = st.selectbox("🌍 Bạn muốn tra cứu zone nào?", xls.sheet_names)

if sheet_name:
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    # Bỏ NaN
    df = df.fillna("")

    # Dropdown chọn A/C
    ac_list = sorted(df["A/C"].unique().tolist())
    ac_list = [x for x in ac_list if x != ""]
    selected_ac = st.selectbox("🛫 Loại máy bay?", ac_list)

    if selected_ac:
        df_ac = df[df["A/C"] == selected_ac]

        # Dropdown chọn Description
        desc_list = sorted(df_ac["Description"].unique().tolist())
        desc_list = [x for x in desc_list if x != ""]
        selected_desc = st.selectbox("📘 Bạn muốn tra cứu phần nào?", desc_list)

        if selected_desc:
            df_desc = df_ac[df_ac["Description"] == selected_desc]

            # Nếu có cột Item thì hỏi tiếp
            if "Item" in df_desc.columns:
                item_list = sorted(df_desc["Item"].unique().tolist())
                item_list = [x for x in item_list if x != ""]
                if item_list:
                    selected_item = st.selectbox("📌 Bạn muốn tra cứu Item nào?", item_list)
                    result = df_desc[df_desc["Item"] == selected_item]
                else:
                    result = df_desc
            else:
                result = df_desc

            if not result.empty:
                st.success(f"Tìm thấy {len(result)} dòng dữ liệu:")

                # Chỉ giữ cột PN, PN interchange, Note
                cols_to_show = ["PART NUMBER (PN)", "PART INTERCHANGE", "NOTE"]
                available_cols = [c for c in cols_to_show if c in result.columns]
                result = result[available_cols]

                # Reset index để thêm STT bắt đầu từ 1
                result = result.reset_index(drop=True)
                result.index = result.index + 1
                result.index.name = "STT"

                # Xuống dòng PN interchange nếu có nhiều
                if "PART INTERCHANGE" in result.columns:
                    result["PART INTERCHANGE"] = result["PART INTERCHANGE"].apply(
                        lambda x: "<br>".join([s.strip() for s in str(x).split("/")])
                    )

                # Xuất bảng
                st.markdown(result.to_html(escape=False), unsafe_allow_html=True)
            else:
                st.error("Không tìm thấy dữ liệu phù hợp.")
