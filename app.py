import streamlit as st
import pandas as pd
import base64
import os

# --- CẤU HÌNH BAN ĐẦU & TRẠNG THÁI ---
st.set_page_config(
    page_title="Tổ Bảo Dưỡng Số 1",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Khởi tạo session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'video_ended' not in st.session_state:
    st.session_state.video_ended = False

# --- CÁC HÀM TIỆN ÍCH DÙNG CHUNG ---
def get_base64_encoded_file(file_path):
    """Đọc file và trả về Base64 encoded string."""
    fallback_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" 
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return fallback_base64
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode("utf-8")
    except Exception as e:
        return fallback_base64

def load_and_clean(excel_file, sheet):
    """Tải và làm sạch DataFrame từ Excel sheet."""
    df = pd.read_excel(excel_file, sheet_name=sheet)
    df.columns = df.columns.str.strip().str.upper()
    df = df.replace(r'^\s*$', pd.NA, regex=True).dropna(how="all")
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("").astype(str).str.strip()
    return df

# --- HÀM RENDER TRANG CHỦ ---
def render_home_page():
    
    video_pc_base64 = get_base64_encoded_file("airplane.mp4")
    video_mobile_base64 = get_base64_encoded_file("mobile.mp4")
    audio_base64 = get_base64_encoded_file("plane_fly.mp3") 
    bg_pc_base64 = get_base64_encoded_file("cabbase.jpg") 
    bg_mobile_base64 = get_base64_encoded_file("mobile.jpg")
    logo_base64 = get_base64_encoded_file("logo.jpg")

    if logo_base64.startswith("iVBORw0KGgo"):
        st.error("⚠️ Lỗi: Không tìm thấy file 'logo.jpg' hoặc các file media khác.")
        st.stop()
    
    # Mã hóa các file nhạc nền
    music_files = []
    for i in range(1, 7):
        music_base64 = get_base64_encoded_file(f"background{i}.mp3")
        if music_base64 and not music_base64.startswith("iVBORw0KGgo"):
            music_files.append(music_base64)
    
    if len(music_files) > 0:
        music_sources_js = ",\n        ".join([f"'data:audio/mp3;base64,{music}'" for music in music_files])
    else:
        music_sources_js = ""
            
    # --- CSS CHUNG ---
    font_links = """
    <link href="https://fonts.googleapis.com/css2?family=Sacramento&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap" rel="stylesheet">
    """
    st.markdown(font_links, unsafe_allow_html=True)

    hide_streamlit_style = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sacramento&family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap');

    #MainMenu, footer, header {{visibility: hidden;}}
    .main {{ padding: 0; margin: 0; }}
    div.block-container {{ padding: 0; margin: 0; max-width: 100% !important; }}

    .stApp {{
        --main-bg-url-pc: url('data:image/jpeg;base64,{bg_pc_base64}');
        --main-bg-url-mobile: url('data:image/jpeg;base64,{bg_mobile_base64}');
        background-color: black; 
    }}

    iframe:first-of-type {{
        transition: opacity 1s ease-out, visibility 1s ease-out;
        opacity: 1;
        visibility: visible;
        width: 100vw !important;
        height: 100vh !important;	
        position: fixed;
        top: 0;
        left: 0;
        z-index: 1000;
        padding: 0;
        margin: 0;
        border: none;
    }}

    .video-finished iframe:first-of-type {{
        opacity: 0;
        visibility: hidden;
        pointer-events: none;
        height: 1px !important;	
        width: 1px !important;
        z-index: 1;
    }}

    .reveal-grid {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        display: grid; grid-template-columns: repeat(20, 1fr);	grid-template-rows: repeat(12, 1fr);
        z-index: 500; pointer-events: none;	
    }}
    .grid-cell {{ background-color: white; opacity: 1; transition: opacity 0.5s ease-out; }}
    
    .main-content-revealed {{
        background-image: var(--main-bg-url-pc); background-size: cover; background-position: center;
        background-attachment: fixed; filter: sepia(60%) grayscale(20%) brightness(85%) contrast(110%);	
        transition: filter 2s ease-out;	
    }}

    @media (max-width: 768px) {{
        .main-content-revealed {{ background-image: var(--main-bg-url-mobile); }}
        .reveal-grid {{ grid-template-columns: repeat(10, 1fr); grid-template-rows: repeat(20, 1fr); }}
    }}

    @keyframes scrollText {{ 0% {{ transform: translate(100vw, 0); }} 100% {{ transform: translate(-100%, 0); }} }}
    @keyframes colorShift {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}

    #main-title-container {{
        position: fixed; top: 5vh; left: 0; width: 100%; height: 10vh;
        overflow: hidden; z-index: 20; pointer-events: none; opacity: 0; 
        transition: opacity 2s ease-out 2s; 
    }}
    .video-finished #main-title-container {{ opacity: 1; z-index: 100; }}

    #main-title-container h1 {{
        font-family: 'Playfair Display', serif; font-size: 3.5vw; margin: 0; font-weight: 900;
        letter-spacing: 5px; white-space: nowrap; display: inline-block;
        background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3);
        background-size: 400% 400%; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: colorShift 10s ease infinite, scrollText 15s linear infinite; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }}

    @media (max-width: 768px) {{
        #main-title-container h1 {{ font-size: 6.5vw; animation-duration: 8s; }}
    }}
    
    /* Music Player Styles */
    #music-player-container {{
        position: fixed; bottom: 20px; right: 20px; width: 280px;
        background: rgba(0, 0, 0, 0.85); backdrop-filter: blur(10px);
        border-radius: 12px; padding: 12px 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        z-index: 999; opacity: 0; transform: translateY(100px);
        transition: opacity 1s ease-out 2s, transform 1s ease-out 2s;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    .video-finished #music-player-container {{ opacity: 1; transform: translateY(0); }}
    
    #music-player-container .controls {{
        display: flex; align-items: center; justify-content: center; gap: 12px; margin-bottom: 10px;
    }}
    
    #music-player-container .control-btn {{
        background: rgba(255, 215, 0, 0.2); border: 2px solid #FFD700; color: #FFD700;
        width: 32px; height: 32px; border-radius: 50%; cursor: pointer;
        display: flex; align-items: center; justify-content: center;
        transition: all 0.3s ease; font-size: 14px;
    }}
    
    #music-player-container .control-btn:hover {{
        background: rgba(255, 215, 0, 0.4); transform: scale(1.1);
    }}
    
    #music-player-container .control-btn.play-pause {{ width: 40px; height: 40px; font-size: 18px; }}
    
    #music-player-container .progress-container {{
        width: 100%; height: 5px; background: rgba(255, 255, 255, 0.2);
        border-radius: 3px; cursor: pointer; margin-bottom: 6px;
        position: relative; overflow: hidden;
    }}
    
    #music-player-container .progress-bar {{
        height: 100%; background: linear-gradient(90deg, #FFD700, #FFA500);
        border-radius: 3px; width: 0%; transition: width 0.1s linear;
    }}
    
    #music-player-container .time-info {{
        display: flex; justify-content: space-between;
        color: rgba(255, 255, 255, 0.7); font-size: 10px; font-family: monospace;
    }}
    
    @media (max-width: 768px) {{
        #music-player-container {{
            width: calc(100% - 40px); right: 20px; left: 20px; bottom: 15px;
        }}
    }}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


    # JavaScript (Kết hợp từ code cũ - HOẠT ĐỘNG TỐT)
    js_callback_video = f"""
    <script>
        console.log("Home Script loaded");
        
        function sendBackToStreamlit() {{
            console.log("Video ended or skipped, revealing main content");
            const stApp = window.parent.document.querySelector('.stApp');
            if (stApp) {{
                stApp.classList.add('video-finished', 'main-content-revealed');
            }}
            initRevealEffect();
            setTimeout(initMusicPlayer, 100);
        }}
        
        function initRevealEffect() {{
            const revealGrid = window.parent.document.querySelector('.reveal-grid');
            if (!revealGrid) {{ return; }}
            const cells = revealGrid.querySelectorAll('.grid-cell');
            const shuffledCells = Array.from(cells).sort(() => Math.random() - 0.5);
            shuffledCells.forEach((cell, index) => {{
                setTimeout(() => {{ cell.style.opacity = 0; }}, index * 10);
            }});
            setTimeout(() => {{ revealGrid.remove(); }}, shuffledCells.length * 10 + 1000);
        }}
        
        function initMusicPlayer() {{
            console.log("Initializing music player");
            
            const musicSources = [{music_sources_js}];
            
            if (musicSources.length === 0) {{
                console.log("No music files available");
                return;
            }}
            
            let currentTrack = 0;
            let isPlaying = false;
            
            const audio = new Audio();
            audio.volume = 0.3;
            
            const playPauseBtn = window.parent.document.getElementById('play-pause-btn');
            const prevBtn = window.parent.document.getElementById('prev-btn');
            const nextBtn = window.parent.document.getElementById('next-btn');
            const progressBar = window.parent.document.getElementById('progress-bar');
            const progressContainer = window.parent.document.getElementById('progress-container');
            const currentTimeEl = window.parent.document.getElementById('current-time');
            const durationEl = window.parent.document.getElementById('duration');
            
            if (!playPauseBtn || !prevBtn || !nextBtn) {{
                console.error("Music player elements not found");
                return;
            }}
            
            function loadTrack(index) {{
                console.log("Loading track", index + 1);
                audio.src = musicSources[index];
                audio.load();
            }}
            
            function togglePlayPause() {{
                if (isPlaying) {{
                    audio.pause();
                    playPauseBtn.textContent = '▶';
                }} else {{
                    audio.play().catch(e => console.error("Play error:", e));
                    playPauseBtn.textContent = '⏸';
                }}
                isPlaying = !isPlaying;
            }}
            
            function nextTrack() {{
                currentTrack = (currentTrack + 1) % musicSources.length;
                loadTrack(currentTrack);
                if (isPlaying) {{
                    audio.play().catch(e => console.error("Play error:", e));
                }}
            }}
            
            function prevTrack() {{
                currentTrack = (currentTrack - 1 + musicSources.length) % musicSources.length;
                loadTrack(currentTrack);
                if (isPlaying) {{
                    audio.play().catch(e => console.error("Play error:", e));
                }}
            }}
            
            function formatTime(seconds) {{
                if (isNaN(seconds)) return '0:00';
                const mins = Math.floor(seconds / 60);
                const secs = Math.floor(seconds % 60);
                return `${{mins}}:${{secs.toString().padStart(2, '0')}}`;
            }}
            
            audio.addEventListener('timeupdate', () => {{
                const progress = (audio.currentTime / audio.duration) * 100;
                progressBar.style.width = progress + '%';
                currentTimeEl.textContent = formatTime(audio.currentTime);
            }});
            
            audio.addEventListener('loadedmetadata', () => {{
                durationEl.textContent = formatTime(audio.duration);
            }});
            
            audio.addEventListener('ended', () => {{
                nextTrack();
            }});
            
            playPauseBtn.addEventListener('click', togglePlayPause);
            nextBtn.addEventListener('click', nextTrack);
            prevBtn.addEventListener('click', prevTrack);
            
            progressContainer.addEventListener('click', (e) => {{
                const rect = progressContainer.getBoundingClientRect();
                const percent = (e.clientX - rect.left) / rect.width;
                audio.currentTime = percent * audio.duration;
            }});
            
            loadTrack(0);
            console.log("Music player initialized successfully");
        }}

        function tryToPlayMedia() {{
            const video = document.getElementById('intro-video');
            const audio = document.getElementById('background-audio');
            
            video.play().catch(e => {{
                console.warn("Video Play Blocked:", e);
                setTimeout(sendBackToStreamlit, 5000);
            }});
            audio.play().catch(e => console.warn("Audio Play Blocked:", e));
        }}
        
        document.addEventListener("DOMContentLoaded", function() {{
            const waitForElements = setInterval(() => {{
                const video = document.getElementById('intro-video');
                const audio = document.getElementById('background-audio');
                const introTextContainer = document.getElementById('intro-text-container');
                
                if (video && audio && introTextContainer) {{
                    clearInterval(waitForElements);
                    
                    const isMobile = window.innerWidth <= 768;
                    const videoSource = isMobile ? 'data:video/mp4;base64,{video_mobile_base64}' : 'data:video/mp4;base64,{video_pc_base64}';

                    video.src = videoSource;
                    audio.src = 'data:audio/mp3;base64,{audio_base64}';

                    video.load();	
                    audio.load();

                    video.addEventListener('ended', () => {{
                        video.style.opacity = 0; 
                        audio.pause(); 
                        audio.currentTime = 0; 
                        introTextContainer.style.opacity = 0;	
                        setTimeout(sendBackToStreamlit, 500);
                    }});
                    video.addEventListener('error', (e) => {{ 
                        console.error("Video error:", e);
                        sendBackToStreamlit(); 
                    }});

                    const chars = introTextContainer.querySelectorAll('.intro-char');
                    chars.forEach((char, index) => {{
                        char.style.animationDelay = `${{index * 0.1}}s`;	
                        char.classList.add('char-shown');	
                    }});

                    setTimeout(tryToPlayMedia, 500);
                    document.addEventListener('click', tryToPlayMedia, {{ once: true }});
                    document.addEventListener('touchstart', tryToPlayMedia, {{ once: true }});
                }}
            }}, 100);
        }});
    </script>
    """
    
    intro_title = "KHÁM PHÁ THẾ GIỚI CÙNG CHÚNG TÔI"
    intro_chars_html = ''.join([
        f'<span class="intro-char">{char}</span>' if char != ' ' else '<span class="intro-char">&nbsp;</span>'	
        for char in intro_title
    ])

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            html, body {{ margin: 0; padding: 0; overflow: hidden; height: 100vh; width: 100vw; background-color: #000; }}
            #intro-video {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0; transition: opacity 1s; }}
            #intro-text-container {{	position: fixed; top: 5vh; width: 100%; text-align: center; color: #FFD700; font-size: 3vw; font-family: 'Sacramento', cursive; text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.8); z-index: 100; pointer-events: none; display: flex; justify-content: center; opacity: 1; transition: opacity 0.5s; }}
            .intro-char {{ display: inline-block; opacity: 0; transform: translateY(-50px); animation-fill-mode: forwards; animation-duration: 0.8s; animation-timing-function: ease-out; }}
            @keyframes charDropIn {{ from {{ opacity: 0; transform: translateY(-50px); }} to {{ opacity: 1; transform: translateY(0); }} }}
            .intro-char.char-shown {{ animation-name: charDropIn; }}
            @media (max-width: 768px) {{ #intro-text-container {{ font-size: 6vw; }} }}
        </style>
    </head>
    <body>
        <div id="intro-text-container">{intro_chars_html}</div>
        <video id="intro-video" muted playsinline></video>
        <audio id="background-audio"></audio>
        {js_callback_video}
    </body>
    </html>
    """

    st.components.v1.html(html_content, height=1080, scrolling=False)

    # --- HIỆU ỨNG REVEAL ---
    grid_cells_html = "".join([f'<div class="grid-cell"></div>' for i in range(240)])
    reveal_grid_html = f'<div class="reveal-grid">{grid_cells_html}</div>'
    st.markdown(reveal_grid_html, unsafe_allow_html=True)

    # --- TIÊU ĐỀ CHÍNH ---
    st.markdown(f"""
    <div id="main-title-container">
        <h1>TỔ BẢO DƯỠNG SỐ 1</h1>
    </div>
    """, unsafe_allow_html=True)

    # --- NÚT CHUYỂN TRANG (Dùng Streamlit button) ---
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div style="height: 35vh;"></div>', unsafe_allow_html=True)
        sub_col1, sub_col2 = st.columns(2)
        
        with sub_col1:
            if st.button("🔍 Tra cứu part number", key="btn_part_number", use_container_width=True):
                st.session_state.page = 'part_number'
                st.rerun()
        
        with sub_col2:
            if st.button("📋 Ngân hàng trắc nghiệm", key="btn_quiz_bank", use_container_width=True):
                st.toast("Trang đang được xây dựng!", icon="🚧")
    
    # CSS cho các button
    st.markdown("""
    <style>
    div[data-testid="column"] button {
        font-family: 'Playfair Display', serif !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: #00ffff !important;
        background-color: rgba(0, 0, 0, 0.6) !important;
        border: 2px solid #00ffff !important;
        border-radius: 8px !important;
        padding: 20px !important;
        text-shadow: 0 0 4px rgba(0, 255, 255, 0.8) !important;
        box-shadow: 0 0 5px #00ffff, 0 0 15px rgba(0, 255, 255, 0.5) !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="column"] button:hover {
        color: #ffd700 !important;
        border-color: #ffd700 !important;
        box-shadow: 0 0 5px #ffd700, 0 0 15px #ff8c00 !important;
        text-shadow: 0 0 3px #ffd700 !important;
        transform: scale(1.05) !important;
    }
    
    @media (max-width: 768px) {
        div[data-testid="column"] button {
            font-size: 1.2rem !important;
            padding: 15px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # --- MUSIC PLAYER ---
    if len(music_files) > 0:
        st.markdown("""
    <div id="music-player-container">
        <div class="controls">
            <button class="control-btn" id="prev-btn">⏮</button>
            <button class="control-btn play-pause" id="play-pause-btn">▶</button>
            <button class="control-btn" id="next-btn">⏭</button>
        </div>
        <div class="progress-container" id="progress-container">
            <div class="progress-bar" id="progress-bar"></div>
        </div>
        <div class="time-info">
            <span id="current-time">0:00</span>
            <span id="duration">0:00</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# --- HÀM RENDER TRANG TRA CỨU PART NUMBER ---
def render_part_number_page():
    
    excel_file = "A787.xlsx"
    if not os.path.exists(excel_file):
        st.error("❌ Không tìm thấy file A787.xlsx")
        st.stop()

    xls = pd.ExcelFile(excel_file)
    bg_img_base64 = get_base64_encoded_file("partnumber.jpg")
    
    # === CSS PHONG CÁCH VINTAGE ===
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');
    
    .stApp {{
        font-family: 'Special Elite', cursive !important;
        background:
            linear-gradient(rgba(245, 242, 230, 0.5), rgba(245, 242, 230, 0.5)),
            url("data:image/jpeg;base64,{bg_img_base64}") no-repeat center center fixed;
        background-size: cover;
    }}
    
    .stApp::after {{
        content: ""; position: fixed; inset: 0;
        background: url("https://www.transparenttextures.com/patterns/aged-paper.png");
        opacity: 0.2; pointer-events: none; z-index: -1;
    }}

    header[data-testid="stHeader"] {{ display: none; }}
    .block-container {{ padding-top: 0 !important; }}

    .main-title {{ font-size: 48px; font-weight: bold; text-align: center; color: #3e2723; margin-top: 25px; text-shadow: 2px 2px 0 #fff, 0 0 25px #f0d49b, 0 0 50px #bca27a; }}
    .sub-title {{ font-size: 34px; text-align: center; color: #6d4c41; margin-top: 5px; margin-bottom: 25px; letter-spacing: 1px; }}

    .stSelectbox label {{ font-weight: bold !important; font-size: 22px !important; color: #4e342e !important; }}
    .highlight-msg {{ font-size: 20px; font-weight: bold; color: #3e2723; background: rgba(239, 235, 233, 0.9); padding: 12px 18px; border-left: 6px solid #6d4c41; border-radius: 8px; margin: 18px 0; text-align: center; }}
    </style>
    """, unsafe_allow_html=True)

    
    # Thêm nút quay lại trang chủ
    if st.button("⬅️ Quay lại Trang Chủ", key="back_home_part", help="Trở về màn hình giới thiệu", type="secondary"):
        st.session_state.page = 'home'
        st.rerun()

    # ===== TIÊU ĐỀ =====
    st.markdown('<div class="main-title">📜 TỔ BẢO DƯỠNG SỐ 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">🔎 TRA CỨU PART NUMBER</div>', unsafe_allow_html=True)

    # ===== NỘI DUNG CHÍNH =====
    zone = st.selectbox("📂 Bạn muốn tra cứu zone nào?", xls.sheet_names)
    if zone:
        df = load_and_clean(excel_file, zone)

        if "A/C" in df.columns:
            aircrafts = sorted([ac for ac in df["A/C"].dropna().unique().tolist() if ac])
            aircraft = st.selectbox("✈️ Loại máy bay?", aircrafts)
        else:
            aircraft = None

        if aircraft:
            df_ac = df[df["A/C"] == aircraft]

            if "DESCRIPTION" in df_ac.columns:
                desc_list = sorted([d for d in df_ac["DESCRIPTION"].dropna().unique().tolist() if d])
                description = st.selectbox("📑 Bạn muốn tra cứu phần nào?", desc_list)
            else:
                description = None

            if description:
                df_desc = df_ac[df_ac["DESCRIPTION"] == description]

                if "ITEM" in df_desc.columns:
                    items = sorted([i for i in df_desc["ITEM"].dropna().unique().tolist() if i])
                    item = st.selectbox("🔢 Bạn muốn tra cứu Item nào?", items)
                    df_desc = df_desc[df_desc["ITEM"] == item]

                df_desc = df_desc.drop(columns=["A/C", "ITEM", "DESCRIPTION"], errors="ignore")
                empty_pattern = r'^\s*$'
                df_desc = df_desc.replace(empty_pattern, pd.NA, regex=True).dropna(how="all")

                if not df_desc.empty:
                    df_desc.insert(0, "STT", range(1, len(df_desc) + 1))
                    st.markdown(f'<div class="highlight-msg">✅ Tìm thấy {len(df_desc)} dòng dữ liệu</div>', unsafe_allow_html=True)
                    st.write(df_desc.to_html(escape=False, index=False), unsafe_allow_html=True)
                else:
                    st.warning("📌 Không có dữ liệu phù hợp.")


# --- LOGIC ĐIỀU HƯỚNG CHÍNH CỦA ỨNG DỤNG ---

# Hiển thị trang tương ứng
if st.session_state.page == 'part_number':
    render_part_number_page() 
elif st.session_state.page == 'quiz_bank':
    st.title("Ngân hàng trắc nghiệm 📋✅")
    st.markdown("---")
    st.markdown("### Trang này đang được xây dựng!")
    if st.button("⬅️ Quay lại Trang Chủ", key="back_home_quiz"):
        st.session_state.page = 'home'
        st.rerun()
else: # st.session_state.page == 'home'
    render_home_page()
