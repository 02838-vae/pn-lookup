import streamlit as st
import pandas as pd
import base64
import os
import time

# --- CẤU HÌNH BAN ĐẦU VÀ LOGIC CHUYỂN TRANG ---

st.set_page_config(
    page_title="Tổ Bảo Dưỡng Số 1",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Khởi tạo session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Hàm Chuyển Trang (Navigation Logic)
def navigate_to(page_name):
    """Chuyển trang đơn giản qua session state"""
    if st.session_state.page != page_name:
        st.session_state.page = page_name
        st.rerun()

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
    try:
        df = pd.read_excel(excel_file, sheet_name=sheet)
        df.columns = df.columns.str.strip().str.upper()
        df = df.replace(r'^\s*$', pd.NA, regex=True).dropna(how="all")
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].fillna("").astype(str).str.strip()
        return df
    except Exception as e:
        # st.error(f"Lỗi khi tải dữ liệu từ sheet '{sheet}': {e}")
        return pd.DataFrame()


# --- TẢI VÀ KIỂM TRA FILE ---
video_pc_base64 = get_base64_encoded_file("airplane.mp4")
video_mobile_base64 = get_base64_encoded_file("mobile.mp4")
audio_base64 = get_base64_encoded_file("plane_fly.mp3")
bg_pc_base64 = get_base64_encoded_file("cabbase.jpg") 
bg_mobile_base64 = get_base64_encoded_file("mobile.jpg")
logo_base64 = get_base64_encoded_file("logo.jpg")

music_files = [get_base64_encoded_file(f"background{i}.mp3") for i in range(1, 7)]
valid_music_files = [music for music in music_files if music != "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="]


# --- PHẦN MUSIC PLAYER (FIXED: Đảm bảo khởi tạo một lần và truy cập DOM) ---
def render_music_player():
    """Render thanh Music Player và CSS/JS liên quan."""
    if not valid_music_files: 
        st.info("ℹ️ Không tìm thấy file nhạc nền. Music player sẽ không hoạt động.")
        return

    music_sources_js = ",\n        ".join([f"'data:audio/mp3;base64,{music}'" for music in valid_music_files]) 

    # --- CSS Music Player ---
    music_player_css = f"""
    <style>
    #music-player-container {{
        position: fixed; bottom: 20px; right: 20px; width: 280px; background: rgba(0, 0, 0, 0.85);
        backdrop-filter: blur(10px); border-radius: 12px; padding: 12px 16px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        z-index: 999; opacity: 0; transform: translateY(100px); 
        transition: opacity 1s ease-out 2s, transform 1s ease-out 2s; border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    .video-finished #music-player-container {{ opacity: 1; transform: translateY(0); }}
    #music-player-container .controls {{ display: flex; align-items: center; justify-content: center; gap: 12px; margin-bottom: 10px; }}
    #music-player-container .control-btn {{
        background: rgba(255, 215, 0, 0.2); border: 2px solid #FFD700; color: #FFD700; width: 32px; height: 32px; 
        border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center;
        transition: all 0.3s ease; font-size: 14px;
    }}
    #music-player-container .control-btn:hover {{ background: rgba(255, 215, 0, 0.4); transform: scale(1.1); }}
    #music-player-container .control-btn.play-pause {{ width: 40px; height: 40px; font-size: 18px; }}
    #music-player-container .progress-container {{
        width: 100%; height: 5px; background: rgba(255, 255, 255, 0.2); border-radius: 3px; cursor: pointer;
        margin-bottom: 6px; position: relative; overflow: hidden;
    }}
    #music-player-container .progress-bar {{
        height: 100%; background: linear-gradient(90deg, #FFD700, #FFA500); border-radius: 3px; width: 0%;
        transition: width 0.1s linear;
    }}
    #music-player-container .time-info {{
        display: flex; justify-content: space-between; color: rgba(255, 255, 255, 0.7); font-size: 10px;
        font-family: monospace;
    }}
    @media (max-width: 768px) {{
        #music-player-container {{ width: calc(100% - 40px); right: 20px; left: 20px; bottom: 15px; }}
    }}
    </style>
    """
    st.markdown(music_player_css, unsafe_allow_html=True)

    # --- HTML Structure ---
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

    # --- JavaScript (Đã FIX: Khởi tạo trên DOM cha và lớp bảo vệ) ---
    music_player_js = f"""
    <script>
        // Dùng window.initMusicPlayer để đảm bảo chỉ chạy 1 lần
        if (!window.musicPlayerInitialized) {{
            console.log("Initializing music player (Single Run)");
            
            const musicSources = [{music_sources_js}];
            const getEl = (id) => window.document.getElementById(id);

            // 1. Tạo hoặc tìm Audio Element toàn cục
            let audio = window.document.getElementById('global-music-audio');
            if (!audio) {{
                audio = window.document.createElement('audio');
                audio.id = 'global-music-audio';
                audio.volume = 0.3;
                window.document.body.appendChild(audio);
                audio.src = musicSources[0]; // Load track đầu tiên
            }}

            const playPauseBtn = getEl('play-pause-btn');
            const progressContainer = getEl('progress-container');
            const nextBtn = getEl('next-btn');
            const prevBtn = getEl('prev-btn');

            if (!playPauseBtn || !progressContainer) return; 

            function formatTime(seconds) {{
                if (isNaN(seconds) || seconds < 0) return '0:00';
                const mins = Math.floor(seconds / 60);
                const secs = Math.floor(seconds % 60);
                return `${{mins}}:${{secs.toString().padStart(2, '0')}}`;
            }}
            
            function updatePlayerUI() {{
                const progressBar = getEl('progress-bar');
                const currentTimeEl = getEl('current-time');
                const durationEl = getEl('duration');

                playPauseBtn.textContent = audio.paused ? '▶' : '⏸';
                
                const progress = (audio.currentTime / audio.duration) * 100;
                if (!isNaN(progress) && progressBar) progressBar.style.width = progress + '%';
                if (currentTimeEl) currentTimeEl.textContent = formatTime(audio.currentTime);
                if (durationEl && audio.duration) durationEl.textContent = formatTime(audio.duration);
            }}

            function togglePlayPause() {{
                if (audio.paused) {{
                    audio.play().then(updatePlayerUI).catch(e => {{
                        console.error("Play Blocked:", e);
                        playPauseBtn.textContent = '🚫';
                        setTimeout(() => playPauseBtn.textContent = '▶', 2000);
                    }});
                }} else {{
                    audio.pause();
                    updatePlayerUI();
                }}
            }}
            
            function changeTrack(direction) {{
                let currentTrack = musicSources.findIndex(src => audio.src === src.replace(/['"]+/g, '')); // Tìm index dựa trên src
                if (currentTrack === -1) currentTrack = 0;
                
                let newIndex = (currentTrack + direction + musicSources.length) % musicSources.length;
                const wasPlaying = !audio.paused;

                audio.src = musicSources[newIndex].replace(/['"]+/g, '');
                audio.load();
                
                if (wasPlaying) {{ 
                    audio.play().catch(e => console.error("Track change blocked:", e)); 
                }}
            }}
            
            // 2. Gắn Event Listeners (Chỉ gắn một lần)
            playPauseBtn.addEventListener('click', togglePlayPause);
            nextBtn.addEventListener('click', () => changeTrack(1));
            prevBtn.addEventListener('click', () => changeTrack(-1));
            
            progressContainer.addEventListener('click', (e) => {{
                if (audio.duration) {{
                    const rect = progressContainer.getBoundingClientRect();
                    const percent = (e.clientX - rect.left) / rect.width;
                    audio.currentTime = percent * audio.duration;
                }}
            }});

            audio.addEventListener('timeupdate', updatePlayerUI);
            audio.addEventListener('loadedmetadata', updatePlayerUI);
            audio.addEventListener('ended', () => changeTrack(1));
            
            window.musicPlayerInitialized = true; // Đánh dấu đã init
            
            // 3. Cập nhật UI ban đầu
            audio.readyState > 0 ? updatePlayerUI() : audio.addEventListener('loadedmetadata', updatePlayerUI, {{ once: true }});
            
        }} else {{
            console.log("Music player already initialized. Skipping.");
        }}
    </script>
    """
    # Dùng height=0 để script chạy ngầm trong DOM chính
    st.components.v1.html(music_player_js, height=0, width=0)


# --- HÀM RENDER TRANG CHỦ ---
def render_home_page():
    
    # 1. CSS & Nút (Đã giữ nguyên và thêm)
    font_links = """
    <link href="https://fonts.googleapis.com/css2?family=Sacramento&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Electrolize&display=swap" rel="stylesheet">
    """
    st.markdown(font_links, unsafe_allow_html=True)
    
    hide_streamlit_style = f"""
    <style>
    /* ... (CSS bạn cung cấp cho .stApp, .main-content-revealed, #main-title-container) ... */
    @import url('https://fonts.googleapis.com/css2?family=Sacramento&family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Electrolize&display=swap');

    #MainMenu, footer, header {{visibility: hidden;}}
    .main {{ padding: 0; margin: 0; }}
    div.block-container {{ padding: 0; margin: 0; max-width: 100% !important; }}

    .stApp {{
        --main-bg-url-pc: url('data:image/jpeg;base64,{bg_pc_base64}');
        --main-bg-url-mobile: url('data:image/jpeg;base64,{bg_mobile_base64}');
        background-color: black; 
    }}
    
    /* Chuyển đổi video/app */
    iframe:first-of-type {{ transition: opacity 1s ease-out, visibility 1s ease-out; opacity: 1; visibility: visible; width: 100vw !important; height: 100vh !important; position: fixed; top: 0; left: 0; z-index: 1000; padding: 0; margin: 0; border: none; }}
    .video-finished iframe:first-of-type {{ opacity: 0; visibility: hidden; pointer-events: none; height: 1px !important;	width: 1px !important; z-index: 1; }}

    .main-content-revealed {{
        background-image: var(--main-bg-url-pc); background-size: cover; background-position: center;
        background-attachment: fixed; filter: sepia(60%) grayscale(20%) brightness(85%) contrast(110%);	
        transition: filter 2s ease-out;	
    }}
    @media (max-width: 768px) {{ .main-content-revealed {{ background-image: var(--main-bg-url-mobile); }} }}
    
    @keyframes scrollText {{ 0% {{ transform: translate(100vw, 0); }} 100% {{ transform: translate(-100%, 0); }} }}
    @keyframes colorShift {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}

    #main-title-container {{ position: fixed; top: 5vh; left: 0; width: 100%; height: 10vh; overflow: hidden; z-index: 20; pointer-events: none; opacity: 0; transition: opacity 2s ease-out 2s; }}
    .video-finished #main-title-container {{ opacity: 1; z-index: 100; }}
    #main-title-container h1 {{
        font-family: 'Playfair Display', serif; font-size: 3.5vw; margin: 0; font-weight: 900;
        letter-spacing: 5px; white-space: nowrap; display: inline-block;
        background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3);
        background-size: 400% 400%; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: colorShift 10s ease infinite, scrollText 15s linear infinite; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }}

    .button-container-fixed {{
        position: fixed; top: 45vh; width: 100%; z-index: 100;
        display: flex; justify-content: center; gap: 60px;
        align-items: center; padding: 0 5vw; 
        box-sizing: border-box;
    }}
    .stApp:not(.video-finished) .button-container-fixed {{ opacity: 0; pointer-events: none; }}
    
    .stButton > button {{
        display: block !important; padding: 8px 12px; text-align: center; text-decoration: none;
        color: #00ffff; font-family: 'Playfair Display', serif; font-size: 1.8rem; font-weight: 700; cursor: pointer; background-color: rgba(0, 0, 0, 0.4);
        border: 2px solid #00ffff; border-radius: 8px; box-sizing: border-box;
        text-shadow: 0 0 4px rgba(0, 255, 255, 0.8), 0 0 10px rgba(34, 141, 255, 0.6);
        box-shadow: 0 0 5px #00ffff, 0 0 15px rgba(0, 255, 255, 0.5);
        transition: transform 0.3s ease, color 0.3s ease, text-shadow 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        white-space: nowrap; flex-grow: 1; max-width: 400px; min-height: 60px; line-height: 1.2;
    }}
    .stButton > button:hover {{
        transform: scale(1.05); color: #ffd700; border-color: #ffd700;
        box-shadow: 0 0 5px #ffd700, 0 0 15px #ff8c00, 0 0 25px rgba(255, 215, 0, 0.7);
        text-shadow: 0 0 3px #ffd700, 0 0 8px #ff8c00;
    }}
    @media (max-width: 768px) {{
        .button-container-fixed {{ flex-direction: column; gap: 15px; top: 50vh; }}
        .stButton > button {{ font-size: 1.4rem; max-width: 90%; }}
    }}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


    # 2. IFRAME VIDEO INTRO (Đã FIX: Cải thiện việc truy cập DOM cha)
    js_callback_video = f"""
    <script>
        // Hàm cập nhật DOM cha
        function sendBackToStreamlit() {{
            try {{
                const stApp = window.parent.document.querySelector('.stApp');
                const mainTitle = window.parent.document.getElementById('main-title-container');
                const musicPlayer = window.parent.document.getElementById('music-player-container');
                
                if (stApp) {{
                    // 1. Kích hoạt hiệu ứng chuyển cảnh
                    stApp.classList.add('video-finished', 'main-content-revealed');
                }}
                
                // 2. Kích hoạt hiệu ứng reveal grid (nếu cần)
                initRevealEffect();

            }} catch (e) {{
                console.error("Error accessing parent DOM:", e);
                // Dù lỗi, vẫn cố gắng ẩn video để hiển thị nội dung chính
                if (window.parent.document.querySelector('.stApp')) {{
                    window.parent.document.querySelector('.stApp').classList.add('video-finished');
                }}
            }}
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
        
        // ... (Giữ nguyên tryToPlay) ...
        function tryToPlay() {{
            const video = document.getElementById('intro-video');
            const audio = document.getElementById('background-audio');
            
            video.play().catch(err => {{ setTimeout(sendBackToStreamlit, 2000); }});
            audio.play().catch(e => {{ console.log("Audio autoplay blocked"); }});
        }}

        document.addEventListener("DOMContentLoaded", function() {{
            // ... (Giữ nguyên logic load video và text animation) ...
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
                    audio.volume = 0.5;

                    video.addEventListener('ended', () => {{
                        video.style.opacity = 0; audio.pause(); audio.currentTime = 0; 
                        introTextContainer.style.opacity = 0;	
                        setTimeout(sendBackToStreamlit, 500);
                    }});
                    video.addEventListener('error', (e) => {{ sendBackToStreamlit(); }});
                    
                    const chars = introTextContainer.querySelectorAll('.intro-char');
                    chars.forEach((char, index) => {{
                        char.style.animationDelay = `${{index * 0.1}}s`;	
                        char.classList.add('char-shown');	
                    }});

                    const clickHandler = () => {{
                        tryToPlay();
                        document.removeEventListener('click', clickHandler);
                        document.removeEventListener('touchstart', clickHandler);
                    }};
                    
                    document.addEventListener('click', clickHandler, {{ once: true }});
                    document.addEventListener('touchstart', clickHandler, {{ once: true }});
                    
                    video.load(); 
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
            
            /* CSS cho Reveal Grid (cần thiết cho initRevealEffect) */
            .reveal-grid {{
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                display: grid; grid-template-columns: repeat(20, 1fr); grid-template-rows: repeat(12, 1fr);
                z-index: 500; pointer-events: none; 
            }}
            .grid-cell {{ background-color: white; opacity: 1; transition: opacity 0.5s ease-out; }}
            @media (max-width: 768px) {{
                .reveal-grid {{ grid-template-columns: repeat(10, 1fr); grid-template-rows: repeat(20, 1fr); }}
            }}
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

    # --- HIỆU ỨNG REVEAL VÀ TIÊU ĐỀ CHÍNH ---
    grid_cells_html = "".join([f'<div class="grid-cell"></div>' for i in range(240)])
    reveal_grid_html = f'<div class="reveal-grid">{grid_cells_html}</div>'
    st.markdown(reveal_grid_html, unsafe_allow_html=True)
    st.markdown(f"""
    <div id="main-title-container">
        <h1>TỔ BẢO DƯỠNG SỐ 1</h1>
    </div>
    """, unsafe_allow_html=True)

    # --- NÚT CHUYỂN TRANG ---
    st.markdown('<div class="button-container-fixed">', unsafe_allow_html=True)
    col_part, col_quiz = st.columns([1, 1])

    with col_part:
        if st.button("Tra cứu Part Number 🔍", key="btn_part_number_home", help="Chuyển đến trang tra cứu"):
            navigate_to('part_number')

    with col_quiz:
        if st.button("Ngân hàng trắc nghiệm 📋✅", key="btn_quiz_bank_home", help="Chuyển đến trang trắc nghiệm"):
            navigate_to('quiz_bank')
    st.markdown('</div>', unsafe_allow_html=True)

    # --- MUSIC PLAYER ---
    render_music_player()


# --- HÀM RENDER TRANG TRA CỨU PART NUMBER ---
def render_part_number_page():
    
    excel_file = "A787.xlsx"
    if not os.path.exists(excel_file):
        st.error("❌ Không tìm thấy file A787.xlsx")
        st.stop()
    
    # === CSS PHONG CÁCH VINTAGE ===
    bg_img_base64 = get_base64_encoded_file("cabbase.jpg")
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');
    
    .stApp {{
        font-family: 'Special Elite', cursive !important;
        background: linear-gradient(rgba(245, 242, 230, 0.5), rgba(245, 242, 230, 0.5)),
            url("data:image/jpeg;base64,{bg_img_base64}") no-repeat center center fixed;
        background-size: cover;
    }}
    .stApp::after {{
        content: ""; position: fixed; inset: 0;
        background: url("https://www.transparenttextures.com/patterns/aged-paper.png");
        opacity: 0.2; pointer-events: none; z-index: -1;
    }}
    .back-to-home-btn {{ position: fixed; top: 20px; left: 20px; z-index: 100; }}
    .main-title {{ font-size: 48px; font-weight: bold; text-align: center; color: #3e2723; margin-top: 25px; text-shadow: 2px 2px 0 #fff, 0 0 25px #f0d49b, 0 0 50px #bca27a; }}
    .sub-title {{ font-size: 34px; text-align: center; color: #6d4c41; margin-top: 5px; margin-bottom: 25px; letter-spacing: 1px; animation: none; }}
    .highlight-msg {{ font-size: 20px; font-weight: bold; color: #3e2723; background: rgba(239, 235, 233, 0.9); padding: 12px 18px; border-left: 6px solid #6d4c41; border-radius: 8px; margin: 18px 0; text-align: center; }}
    </style>
    """, unsafe_allow_html=True)

    # Thêm nút quay lại trang chủ
    if st.button("⬅️ Quay lại Trang Chủ", key="back_home_part", help="Trở về màn hình giới thiệu", type="secondary"):
        navigate_to('home')

    # --- MUSIC PLAYER ---
    render_music_player()

    # ===== TIÊU ĐỀ =====
    st.markdown('<div class="main-title">📜 TỔ BẢO DƯỠNG SỐ 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">🔎 TRA CỨU PART NUMBER</div>', unsafe_allow_html=True)
    
    # ===== NỘI DUNG CHÍNH =====
    try:
        xls = pd.ExcelFile(excel_file)
        # Chỉ lấy các sheet không bắt đầu bằng "Sheet"
        sheet_names = [name for name in xls.sheet_names if not name.startswith("Sheet")]
        
        zone = st.selectbox("📂 Bạn muốn tra cứu zone nào?", sheet_names, key="select_zone")
        
        if zone:
            df = load_and_clean(excel_file, zone)
            
            if "A/C" in df.columns:
                aircrafts = sorted([ac for ac in df["A/C"].dropna().unique().tolist() if ac])
                aircraft = st.selectbox("✈️ Loại máy bay?", aircrafts, key="select_ac")
            else:
                aircraft = None

            df_ac = df[df["A/C"] == aircraft] if aircraft else df

            if "DESCRIPTION" in df_ac.columns:
                desc_list = sorted([d for d in df_ac["DESCRIPTION"].dropna().unique().tolist() if d])
                description = st.selectbox("📑 Bạn muốn tra cứu phần nào?", desc_list, key="select_desc")
            else:
                description = None

            df_desc = df_ac[df_ac["DESCRIPTION"] == description] if description else df_ac

            if "ITEM" in df_desc.columns:
                items = sorted([i for i in df_desc["ITEM"].dropna().unique().tolist() if i])
                item = st.selectbox("🔢 Bạn muốn tra cứu Item nào?", items, key="select_item")
                df_desc = df_desc[df_desc["ITEM"] == item] if item else df_desc

            # Lọc và hiển thị
            df_display = df_desc.drop(columns=["A/C", "ITEM", "DESCRIPTION"], errors="ignore")
            df_display = df_display.dropna(axis=1, how='all')

            if not df_display.empty:
                df_display.insert(0, "STT", range(1, len(df_display) + 1))
                st.markdown(f'<div class="highlight-msg">✅ Tìm thấy {len(df_display)} dòng dữ liệu</div>', unsafe_allow_html=True)
                st.dataframe(df_display)
            else:
                st.warning("📌 Không có dữ liệu phù hợp.")

    except Exception as e:
        st.error(f"Lỗi khi xử lý file Excel: {e}")


# --- HÀM RENDER TRANG QUIZ BANK ---
def render_quiz_bank_page():
    st.markdown("""
    <style>
    .back-to-home-btn { position: fixed; top: 20px; left: 20px; z-index: 100; }
    .stApp { background: #3a3a3a; color: white; transition: background-color 1s; }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("Ngân hàng trắc nghiệm 📋✅")
    
    if st.button("⬅️ Quay lại Trang Chủ", key="back_home_quiz"):
        navigate_to('home')
        
    st.markdown("---")
    st.info("### Trang này đang được xây dựng!")
    
    # Hiển thị thanh nhạc ở trang này (nếu có)
    render_music_player()


# --- LOGIC ĐIỀU HƯỚNG CHÍNH CỦA ỨNG DỤNG ---

if st.session_state.page == 'part_number':
    render_part_number_page() 
elif st.session_state.page == 'quiz_bank':
    render_quiz_bank_page()
else: # st.session_state.page == 'home'
    render_home_page()
