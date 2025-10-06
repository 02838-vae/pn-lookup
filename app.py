import streamlit as st
import time
import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

if "intro_done" not in st.session_state:
    st.session_state.intro_done = False

if not st.session_state.intro_done:
    try:
        video_path = "airplane.mp4"
        video_base64 = get_base64_of_bin_file(video_path)

        # ✅ HTML + CSS + JS đảm bảo video hiển thị full & chuyển cảnh đúng
        video_html = f"""
        <style>
        html, body {{
            margin: 0; padding: 0; overflow: hidden;
            background-color: black;
            height: 100%; width: 100%;
        }}
        #intro-video {{
            position: fixed;
            top: 0; left: 0;
            width: 100vw; height: 100vh;
            background-color: black;
            z-index: 99999;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: fadeIn 1s ease;
        }}
        video {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        @keyframes fadeOut {{
            from {{ opacity: 1; }}
            to {{ opacity: 0; }}
        }}
        </style>

        <div id="intro-video">
            <video id="intro" autoplay muted playsinline onended="fadeOutVideo()">
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                Trình duyệt của bạn không hỗ trợ video.
            </video>
        </div>

        <script>
        function fadeOutVideo() {{
            const videoDiv = document.getElementById('intro-video');
            videoDiv.style.animation = 'fadeOut 1.5s ease forwards';
            setTimeout(() => {{
                videoDiv.remove();
                const app = window.parent.document.querySelector('.stApp');
                if (app) {{
                    app.style.visibility = 'visible';
                    app.style.opacity = '0';
                    app.style.transition = 'opacity 1.5s ease';
                    setTimeout(() => {{ app.style.opacity = '1'; }}, 100);
                }}
            }}, 1500);
        }}

        // Hiện nội dung sau 8 giây nếu video không tự onended
        setTimeout(() => {{
            if (document.getElementById('intro-video')) fadeOutVideo();
        }}, 8000);
        </script>
        """
        st.markdown(video_html, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Lỗi khi load video: {e}")

    # ⏱ Cho phép video phát xong trước khi render trang
    time.sleep(8)
    st.session_state.intro_done = True
