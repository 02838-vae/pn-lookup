import streamlit as st
import pandas as pd
import base64

# ======= Load Excel ==========
excel_file = "A787.xlsx"
xls = pd.ExcelFile(excel_file)

# ======= Set page config =======
st.set_page_config(page_title="PN Lookup", layout="wide")

# ======= Background with airplane (mờ hơn) =======
def set_background(bg_file):
    with open(bg_file, "rb") as f:
        bg_data = f.read()
    bg_encoded = base64.b64encode(bg_data).decode()

    page_bg = f"""
    <style>
    .stApp {{
        background: url("data:image/jpg;base64,{bg_encoded}") no-repeat center center fixed;
        background-size: cover;
        position: relative;
    }}
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background-color: rgba(255,255,255,0.65); /* nền mờ hơn */
        z-index: 0;
    }}
    .stApp > div {{
        position: relative;
        z-index: 1;
    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

set_background("airplane.jpg")

# ======= Animated header =======
st.markdown(
    "<div style='font-size:28px;font-weight:bold;text-align:center;animation:colorchange 6s infinite alternate;'>Tổ bảo dưỡng số 1</div>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    @keyframes colorchange {
        0%   { color: #ff4b5c; }
        25%  { color: #ff914d; }
        50%  { color: #1dd1a1; }
        75%  { color: #54a0ff; }
        100% { color: #f368e0; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ======= Main title =======
st.markdown(
    "<div style='font-size:22px;font-weight:bold;text-align:center;color:#004080;margin-top:10px;margin-bottom:20px;text-shadow:2px 2px 6px rgba(255,255,255,0.8);'>Tra cứu Part number</div>",
    unsafe_allow_html=True,
)

# ======= Dropdown logic =======
sheet_name = st.selectbox("👉 Bạn muốn tra cứu zone nào?", xls.sheet_names)

if sheet_name:
    df = pd.read_excel(xls, sheet_name=sheet_name)
    df = df.dropna(how="all").fillna("")
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # --- Dropdown A/C ---
    ac_select = None
    if "A/C" in df.columns:
        ac_list = sorted([x for x in df["A/C"].unique() if x not in ["", "nan", "NaN"]])
        ac_select = st.selectbox("👉 Loại máy bay?", ac_list)

    if ac_select:
        df_ac = df[df["A/C"] == ac_select]

        # --- Dropdown Description ---
        desc_select = None
        if "Description" in df_ac.columns:
            desc_list = sorted([x for x in df_ac["Description"].unique() if x not in ["", "nan", "NaN"]])
            desc_select = st.selectbox("👉 Bạn muốn tra cứu phần nào?", desc_list)

        if desc_select:
            df_desc = df_ac[df_ac["Description"] == desc_select]

            # --- Dropdown Item nếu có ---
            result = df_desc
            if "Item" in df_desc.columns:
                item_list = sorted([x for x in df_desc["Item"].unique() if x not in ["", "nan", "NaN"]])
                item_select = st.selectbox("👉 Bạn muốn tra cứu Item nào?", item_list)
                if item_select:
                    result = df_desc[df_desc["Item"] == item_select]

            # --- Show result table ---
            if not result.empty:
                result = result.reset_index(drop=True)
                result.index = result.index + 1  # STT từ 1

                cols_to_show = [c for c in ["PART NUMBER (PN)", "PN interchange", "Note"] if c in result.columns]
                result_display = result[cols_to_show].copy()
                result_display.index.name = "STT"

                st.markdown(
                    f"<div style='font-size:20px;font-weight:bold;color:#ff1e56;animation:blink 1s infinite;text-align:center;'>✅ Tìm thấy {len(result_display)} dòng dữ liệu:</div>",
                    unsafe_allow_html=True,
                )

                # Custom CSS cho bảng
                st.markdown(
                    """
                    <style>
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin: 20px 0;
                        font-size: 14px;
                        text-align: center;
                        background-color: #ffffff;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                        border-radius: 10px;
                        overflow: hidden;
                    }
                    thead th {
                        background-color: #004080;
                        color: white !important;
                        font-weight: bold;
                        padding: 10px;
                        border: 2px solid #222222;
                    }
                    tbody td {
                        border: 1px solid #444444;
                        padding: 8px;
                        color: #000000;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(result_display.to_html(escape=False), unsafe_allow_html=True)

# ===== CSS cho label câu hỏi =====
st.markdown(
    """
    <style>
    label[data-testid="stWidgetLabel"] > div {
        font-weight: bold !important;
        color: #002147 !important;
        font-size: 16px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
