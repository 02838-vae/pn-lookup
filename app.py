import pandas as pd
... import streamlit as st
... 
... # Đọc dữ liệu
... df = pd.read_excel("A787.xlsx")
... df = df.dropna(subset=["DESCRIPTION", "PART NUMBER (PN)"])
... 
... # Tiêu đề app
... st.title("🔎 Tra cứu Part Number (PN)")
... 
... # Bước 1: chọn Category
... categories = df["CATEGORY"].dropna().unique()
... category = st.selectbox("Bạn muốn tra cứu gì?", categories)
... 
... if category:
...     # Bước 2: chọn Description theo Category
...     descriptions = df[df["CATEGORY"] == category]["DESCRIPTION"].dropna().unique()
...     description = st.selectbox("Bạn muốn tra cứu Description nào?", descriptions)
... 
...     if description:
...         # Bước 3: tìm PN
...         result = df[(df["CATEGORY"] == category) & (df["DESCRIPTION"] == description)]
...         if not result.empty:
...             st.success(f"✅ PN: {', '.join(result['PART NUMBER (PN)'].astype(str))}")
...             if "NOTE" in result.columns:
...                 notes = result["NOTE"].dropna().astype(str).unique()
...                 if len(notes) > 0:
...                     st.info(f"📌 Ghi chú: {', '.join(notes)}")
...         else:


