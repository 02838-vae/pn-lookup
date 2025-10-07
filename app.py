# ===== CSS PHONG CÁCH VINTAGE (NỀN RÕ HƠN) =====
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

.stApp {{
    font-family: 'Special Elite', cursive !important;
    background:
        linear-gradient(rgba(245, 242, 230, 0.5), rgba(245, 242, 230, 0.5)),
        url("data:image/jpeg;base64,{img_base64}") no-repeat center center fixed;
    background-size: cover;
}}
.stApp::after {{
    content: "";
    position: fixed;
    inset: 0;
    background: url("https://www.transparenttextures.com/patterns/aged-paper.png");
    opacity: 0.2;  /* Giảm mờ để ảnh nền rõ hơn */
    pointer-events: none;
    z-index: -1;
}}

header[data-testid="stHeader"] {{ display: none; }}
.block-container {{ padding-top: 0 !important; }}

/* ===== TIÊU ĐỀ ===== */
.main-title {{
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    color: #3e2723;
    margin-top: 25px;
    text-shadow: 2px 2px 0 #fff, 0 0 25px #f0d49b, 0 0 50px #bca27a;
}}

.sub-title {{
    font-size: 30px;
    text-align: center;
    color: #6d4c41;
    margin-top: 5px;
    margin-bottom: 20px;
    letter-spacing: 1px;
    animation: glowTitle 3s ease-in-out infinite alternate;
}}

@keyframes glowTitle {{
    from {{ text-shadow: 0 0 10px #bfa67a, 0 0 20px #d2b48c, 0 0 30px #e6d5a8; color: #4e342e; }}
    to {{ text-shadow: 0 0 20px #f8e1b4, 0 0 40px #e0b97d, 0 0 60px #f7e7ce; color: #5d4037; }}
}}

/* ===== FORM ===== */
.stSelectbox label {{
    font-weight: bold !important;
    font-size: 18px !important;
    color: #4e342e !important;
}}
.stSelectbox div[data-baseweb="select"] {{
    font-size: 15px !important;
    color: #3e2723 !important;
    background: #fdfbf5 !important;
    border: 1.5px dashed #5d4037 !important;
    border-radius: 6px !important;
}}

/* ===== BẢNG KẾT QUẢ ===== */
table.dataframe {{
    width: 100%;
    border-collapse: collapse;
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(2px);
}}
table.dataframe thead th {{
    background: #6d4c41;
    color: #fff8e1;
    padding: 10px;
    border: 2px solid #3e2723;
    font-size: 15px;
    text-align: center;
}}
table.dataframe tbody td {{
    border: 1.5px solid #5d4037;
    padding: 10px;
    font-size: 14px;
    color: #3e2723;
    text-align: center;
}}
table.dataframe tbody tr:nth-child(even) td {{
    background: rgba(248, 244, 236, 0.8);
}}
table.dataframe tbody tr:hover td {{
    background: rgba(241, 224, 198, 0.9);
    transition: 0.3s;
}}

.highlight-msg {{
    font-size: 18px;
    font-weight: bold;
    color: #3e2723;
    background: rgba(239, 235, 233, 0.9);
    padding: 10px 15px;
    border-left: 6px solid #6d4c41;
    border-radius: 6px;
    margin: 15px 0;
    text-align: center;
}}
</style>
""", unsafe_allow_html=True)
