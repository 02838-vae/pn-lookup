import base64

def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    css = f"""
    <style>
    .stApp {{
      position: relative;
      background: none;
    }}
    .stApp::before {{
      content: "";
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background-image: url("data:image/jpg;base64,{encoded}");
      background-size: cover;
      background-position: center;
      opacity: 0.15;
      z-index: -1;
    }}
    /* Chat bubbles */
    .chat-row {{ display:flex; gap:8px; margin:8px 0; }}
    .chat-user {{ margin-left:auto; max-width:80%; padding:10px 14px; border-radius:14px; background:#0ea5a4; color:white; }}
    .chat-bot  {{ margin-right:auto; max-width:80%; padding:10px 14px; border-radius:14px; background:#f1f5f9; color:#0f172a; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Gọi hàm ngay sau st.set_page_config:
add_bg_from_local("airplane.jpg")


