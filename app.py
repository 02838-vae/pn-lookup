import streamlit as st
import base64
import os

# --- CẤU HÌNH BAN ĐẦU ---
st.set_page_config(
    page_title="Tổ Bảo Dưỡng Số 1",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Khởi tạo session state
if 'video_ended' not in st.session_state:
    st.session_state.video_ended = False

# --- CÁC HÀM TIỆN ÍCH ---

def get_base64_encoded_file(file_path):
    """Đọc file và trả về Base64 encoded string."""
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return None
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode("utf-8")
    except Exception as e:
        st.error(f"Lỗi khi đọc file {file_path}: {str(e)}")
        return None


# Mã hóa các file media chính (bắt buộc)
try:
    # Đảm bảo các file này nằm cùng thư mục với app.py
    video_pc_base64 = get_base64_encoded_file("airplane.mp4")
    video_mobile_base64 = get_base64_encoded_file("mobile.mp4")
    audio_base64 = get_base64_encoded_file("plane_fly.mp3")
    bg_pc_base64 = get_base64_encoded_file("cabbase.jpg") 
    bg_mobile_base64 = get_base64_encoded_file("mobile.jpg")
    
    # MÃ HÓA CHO LOGO
    logo_base64 = get_base64_encoded_file("logo.jpg")

    # Kiểm tra file bắt buộc
    if not all([video_pc_base64, video_mobile_base64, audio_base64, bg_pc_base64, bg_mobile_base64]):
        missing_files = []
        if not video_pc_base64: missing_files.append("airplane.mp4")
        if not video_mobile_base64: missing_files.append("mobile.mp4")
        if not audio_base64: missing_files.append("plane_fly.mp3")
        if not bg_pc_base64: missing_files.append("cabbase.jpg")
        if not bg_mobile_base64: missing_files.append("mobile.jpg")
        
        st.error(f"⚠️ Thiếu các file media cần thiết hoặc file rỗng. Vui lòng kiểm tra lại các file sau trong thư mục:")
        st.write(" - " + "\n - ".join(missing_files))
        st.stop()
        
except Exception as e:
    st.error(f"❌ Lỗi khi đọc file: {str(e)}")
    st.stop()

# Đảm bảo logo_base64 được khởi tạo nếu file không tồn tại
if not 'logo_base64' in locals() or not logo_base64:
    logo_base64 = "" 
    st.info("ℹ️ Không tìm thấy file logo.jpg. Music player sẽ không có hình nền logo.")


# Mã hóa các file nhạc nền (không bắt buộc)
music_files = []
for i in range(1, 7):
    music_base64 = get_base64_encoded_file(f"background{i}.mp3")
    if music_base64:
        music_files.append(music_base64)

if len(music_files) == 0:
    st.info("ℹ️ Không tìm thấy file nhạc nền (background1.mp3 - background6.mp3). Music player sẽ không hoạt động.")


# --- PHẦN 1: NHÚNG FONT BẰNG THẺ LINK TRỰC TIẾP VÀO BODY ---
font_links = """
<link href="https://fonts.googleapis.com/css2?family=Sacramento&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap" rel="stylesheet">
"""
st.markdown(font_links, unsafe_allow_html=True)

# --- PHẦN 2: CSS CHÍNH (STREAMLIT APP) ---
hide_streamlit_style = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sacramento&family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap');

/* Ẩn các thành phần mặc định của Streamlit */
#MainMenu, footer, header {{visibility: hidden;}}

.main {{
    padding: 0;
    margin: 0;
}}

div.block-container {{
    padding: 0;
    margin: 0;
    max-width: 100% !important;
}}

/* Iframe Video Intro */
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
}}

.video-finished iframe:first-of-type {{
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
    height: 1px !important;
    width: 1px !important;
}}

.stApp {{
    --main-bg-url-pc: url('data:image/jpeg;base64,{bg_pc_base64}');
    --main-bg-url-mobile: url('data:image/jpeg;base64,{bg_mobile_base64}');
    --logo-bg-url: url('data:image/jpeg;base64,{logo_base64}');
}}

.reveal-grid {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    display: grid;
    grid-template-columns: repeat(20, 1fr);
    grid-template-rows: repeat(12, 1fr);
    z-index: 500;
    pointer-events: none;
}}

.grid-cell {{
    background-color: white;
    opacity: 1;
    transition: opacity 0.5s ease-out;
}}

.main-content-revealed {{
    background-image: var(--main-bg-url-pc);
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    filter: sepia(60%) grayscale(20%) brightness(85%) contrast(110%);
    transition: filter 2s ease-out;
}}

@media (max-width: 768px) {{
    .main-content-revealed {{
        background-image: var(--main-bg-url-mobile);
    }}
    .reveal-grid {{
        grid-template-columns: repeat(10, 1fr);
        grid-template-rows: repeat(20, 1fr);
    }}
}}

/* Keyframes cho hiệu ứng chữ chạy đơn */
@keyframes scrollText {{
    0% {{ transform: translate(100vw, 0); }}
    100% {{ transform: translate(-100%, 0); }}
}}

/* Keyframes cho hiệu ứng Đổi Màu Gradient */
@keyframes colorShift {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

/* === TIÊU ĐỀ TRANG CHÍNH === */
#main-title-container {{
    position: fixed;
    top: 5vh;
    left: 0;
    width: 100%;
    height: 10vh;
    overflow: hidden;
    z-index: 20;
    pointer-events: none;
    opacity: 0;
    transition: opacity 2s;
}}

.video-finished #main-title-container {{
    opacity: 1;
}}

#main-title-container h1 {{
    font-family: 'Playfair Display', serif;
    font-size: 3.5vw;
    margin: 0;
    font-weight: 900;
    font-feature-settings: "lnum" 1;
    letter-spacing: 5px;
    white-space: nowrap;
    display: inline-block;
    animation: scrollText 15s linear infinite;
    background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3);
    background-size: 400% 400%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent;
    animation: colorShift 10s ease infinite, scrollText 15s linear infinite;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}}

@media (max-width: 768px) {{
    #main-title-container {{
        height: 8vh;
        width: 100%;
        left: 0;
    }}
    
    #main-title-container h1 {{
        font-size: 6.5vw;
        animation-duration: 8s;
    }}
}}


/* 🌟 KEYFRAMES: HIỆU ỨNG TỎA SÁNG MÀU NGẪU NHIÊN */
@keyframes glow-random-color {{
    /* TRẠNG THÁI NGHỈ/TẮT */
    0%, 57.14% /* 4s / 7s = 57.14% */, 100% {{
        box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.3); /* Viền mờ/cơ bản */
    }}
    
    /* TRẠNG THÁI SÁNG (Chuyển màu từ 0% đến 57.14%) */
    0% {{
        /* Màu ban đầu - Ví dụ: Đỏ */
        box-shadow: 
            0 0 10px 4px rgba(255, 0, 0, 0.9), 
            0 0 20px 8px rgba(255, 0, 0, 0.6), 
            inset 0 0 5px 2px rgba(255, 0, 0, 0.9); 
    }}
    
    14.28% /* 1s / 7s = 14.28% */ {{ 
        /* Màu 1s - Ví dụ: Xanh lá */
        box-shadow: 
            0 0 10px 4px rgba(0, 255, 0, 0.9), 
            0 0 20px 8px rgba(0, 255, 0, 0.6), 
            inset 0 0 5px 2px rgba(0, 255, 0, 0.9);
    }}
    
    28.56% /* 2s / 7s = 28.56% */ {{ 
        /* Màu 2s - Ví dụ: Xanh dương */
        box-shadow: 
            0 0 10px 4px rgba(0, 0, 255, 0.9), 
            0 0 20px 8px rgba(0, 0, 255, 0.6), 
            inset 0 0 5px 2px rgba(0, 0, 255, 0.9);
    }}

    42.84% /* 3s / 7s = 42.84% */ {{ 
        /* Màu 3s - Ví dụ: Vàng */
        box-shadow: 
            0 0 10px 4px rgba(255, 255, 0, 0.9), 
            0 0 20px 8px rgba(255, 255, 0, 0.6), 
            inset 0 0 5px 2px rgba(255, 255, 0, 0.9);
    }}
    
    57.14% /* 4s / 7s = 57.14% */ {{ 
        /* Màu 4s - Ví dụ: Hồng - Kết thúc hiệu ứng sáng */
        box-shadow: 
            0 0 10px 4px rgba(255, 0, 255, 0.9), 
            0 0 20px 8px rgba(255, 0, 255, 0.6), 
            inset 0 0 5px 2px rgba(255, 0, 255, 0.9);
    }}
}}


/* === MUSIC PLAYER STYLES (Giữ nguyên) === */
#music-player-container {{
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 350px; 
    padding: 8px 16px; 
    background: rgba(0, 0, 0, 0.7); 
    border-radius: 12px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.7); 
    z-index: 999;
    opacity: 0;
    transform: translateY(100px);
    transition: opacity 1s ease-out 2s, transform 1s ease-out 2s;
    position: fixed;
}}

/* LỚP GIẢ (::before) CHO HÌNH NỀN LOGO VÀ HIỆU ỨNG TỎA SÁNG */
#music-player-container::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    /* Thêm padding/margin âm để mở rộng lớp giả ra ngoài một chút */
    margin: -3px; 
    width: calc(100% + 6px);
    height: calc(100% + 6px);
    
    background-image: var(--logo-bg-url);
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    filter: contrast(110%) brightness(90%); 
    opacity: 0.4; 
    z-index: -1; 
    
    border-radius: 12px;
    
    /* ÁP DỤNG HIỆU ỨNG TỎA SÁNG */
    box-sizing: border-box; 
    animation: glow-random-color 7s linear infinite; 
}}


/* Đảm bảo các thành phần con ở trên lớp giả */
#music-player-container * {{
    position: relative;
    z-index: 5; 
}}

.video-finished #music-player-container {{
    opacity: 1;
    transform: translateY(0);
}}

/* Các style khác của player (giữ nguyên) */
#music-player-container .controls,
#music-player-container .time-info {{
    color: #fff; 
    text-shadow: 0 0 7px #000;
}}

#music-player-container .controls {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    margin-bottom: 6px; 
}}

#music-player-container .control-btn {{
    background: rgba(255, 255, 255, 0.2);
    border: 2px solid #FFFFFF; 
    color: #FFD700;
    width: 32px; 
    height: 32px;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
    font-size: 14px; 
}}

#music-player-container .control-btn:hover {{
    background: rgba(255, 215, 0, 0.5);
    transform: scale(1.15);
}}

#music-player-container .control-btn.play-pause {{
    width: 40px; 
    height: 40px;
    font-size: 18px;
}}

#music-player-container .progress-container {{
    width: 100%;
    height: 5px; 
    background: rgba(0, 0, 0, 0.5);
    border-radius: 3px;
    cursor: pointer;
    margin-bottom: 4px; 
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.4); 
}}

#music-player-container .progress-bar {{
    height: 100%;
    background: linear-gradient(90deg, #FFD700, #FFA500); 
    border-radius: 3px;
    width: 0%;
    transition: width 0.1s linear;
}}

#music-player-container .time-info {{
    display: flex;
    justify-content: space-between;
    color: rgba(255, 255, 255, 1);
    font-size: 10px; 
    font-family: monospace;
}}

@media (max-width: 768px) {{
    #music-player-container {{
        width: calc(100% - 40px);
        right: 20px;
        left: 20px;
        bottom: 15px;
        padding: 8px 12px;
    }}
    #music-player-container .control-btn,
    #music-player-container .control-btn.play-pause {{
        width: 36px;
        height: 36px;
        font-size: 16px;
    }}
    #music-player-container .control-btn.play-pause {{
        width: 44px;
        height: 44px;
        font-size: 20px;
    }}
}}

/* === CSS CHO NAVIGATION BUTTON (ĐÃ CHỈNH SỬA) === */
.nav-container {{
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 40px;
    opacity: 0;
    transition: opacity 2s ease-out 3s;
    z-index: 50;
}}

.video-finished .nav-container {{
    opacity: 1;
}}

.nav-btn {{
    position: relative;
    /* ✅ 1. THU NHỎ: Giảm padding đáng kể */
    padding: 20px 35px; 
    /* ✅ 3. BỎ BLUR: Giảm alpha (0.1 -> 0.4) cho nền để nổi hơn so với nền. */
    background: linear-gradient(135deg, rgba(255, 215, 0, 0.4), rgba(255, 165, 0, 0.4));
    border: 4px solid #FFD700;
    border-radius: 20px;
    color: #FFD700;
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 900;
    text-align: center;
    cursor: pointer;
    transition: all 0.4s ease;
    text-decoration: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 5px; /* Giảm khoảng cách tối đa */
    overflow: hidden;
    box-shadow: 
        0 10px 40px rgba(255, 215, 0, 0.3),
        inset 0 0 30px rgba(255, 215, 0, 0.1);
    /* ❌ 3. BỎ BLUR: Xóa bỏ dòng này để loại bỏ hiệu ứng làm mờ */
    /* backdrop-filter: blur(10px); */
}}

.nav-btn::before {{
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.3), transparent);
    transition: left 0.5s ease;
}}

.nav-btn:hover::before {{
    left: 100%;
}}

.nav-btn:hover {{
    background: linear-gradient(135deg, rgba(255, 215, 0, 0.6), rgba(255, 165, 0, 0.6));
    border-color: #FFA500;
    /* Giảm hiệu ứng hover để tránh khung quá to */
    transform: translateY(-5px) scale(1.05); 
    box-shadow: 
        0 15px 40px rgba(255, 215, 0, 0.6),
        0 0 30px rgba(255, 215, 0, 0.5),
        inset 0 0 30px rgba(255, 215, 0, 0.3);
}}

.nav-btn:active {{
    transform: translateY(-2px) scale(1.03); /* Giảm hiệu ứng active */
}}

.nav-btn-icon {{
    font-size: 3rem; /* Giảm kích thước icon */
    margin-bottom: 5px;
    filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.5));
}}

.nav-btn-text {{
    font-size: 1.3rem; /* Giảm kích thước chữ */
    letter-spacing: 3px;
    text-transform: uppercase;
    white-space: nowrap; /* Đảm bảo chữ không bị xuống dòng */
}}

.nav-btn-desc {{
    /* ✅ 2. XÓA CHỮ PHỤ: Ẩn hoàn toàn phần mô tả phụ */
    display: none;
}}

@media (max-width: 768px) {{
    .nav-container {{
        padding: 20px;
        width: calc(100vw - 40px);
    }}
    
    .nav-btn {{
        padding: 20px 30px; /* Điều chỉnh responsive padding */
        font-size: 1.2rem;
        min-width: unset;
        width: 100%;
        gap: 5px;
    }}
    
    .nav-btn-icon {{
        font-size: 2.5rem;
    }}
    
    .nav-btn-text {{
        font-size: 1.1rem;
    }}
    
    .nav-btn-desc {{
        display: none;
    }}
}}

@keyframes fadeInUp {{
    from {{
        opacity: 0;
        transform: translateY(50px) scale(0.9);
    }}
    to {{
        opacity: 1;
        transform: translateY(0) scale(1);
    }}
}}

.video-finished .nav-btn {{
    animation: fadeInUp 1s ease-out forwards;
    animation-delay: 3.2s;
    opacity: 0;
}}

</style>
"""

# Thêm CSS vào trang chính
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# --- PHẦN 3: MÃ HTML/CSS/JavaScript IFRAME CHO VIDEO INTRO (Giữ nguyên) ---
# ... (Phần code này không thay đổi)

# Tạo danh sách music sources cho JavaScript 
if len(music_files) > 0:
    music_sources_js = ",\n        ".join([f"'data:audio/mp3;base64,{music}'" for music in music_files])
else:
    music_sources_js = ""

# JavaScript 
js_callback_video = f"""
<script>
    console.log("Script loaded");
    
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
            setTimeout(() => {{
                cell.style.opacity = 0;
            }}, index * 10);
        }});
        
        setTimeout(() => {{
             revealGrid.remove();
        }}, shuffledCells.length * 10 + 1000);
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
            console.error("Music player elements not found in parent document");
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

    document.addEventListener("DOMContentLoaded", function() {{
        console.log("DOM loaded, waiting for elements...");
        
        const waitForElements = setInterval(() => {{
            const video = document.getElementById('intro-video');
            const audio = document.getElementById('background-audio');
            const introTextContainer = document.getElementById('intro-text-container');
            
            if (video && audio && introTextContainer) {{
                clearInterval(waitForElements);
                console.log("All elements found, initializing...");
                
                const isMobile = window.innerWidth <= 768;
                const videoSource = isMobile ? 'data:video/mp4;base64,{video_mobile_base64}' : 'data:video/mp4;base64,{video_pc_base64}';

                video.src = videoSource;
                audio.src = 'data:audio/mp3;base64,{audio_base64}';

                console.log("Video/Audio source set. Loading metadata...");
                
                const tryToPlay = () => {{
                    console.log("Attempting to play video (User interaction or Canplay event)");
                    
                    video.play().then(() => {{
                        console.log("✅ Video is playing!");
                    }}).catch(err => {{
                        console.error("❌ Still can't play video, skipping intro (Error/File issue):", err);
                        setTimeout(sendBackToStreamlit, 2000);
                    }});

                    audio.play().catch(e => {{
                        console.log("Audio autoplay blocked (normal), waiting for video end.");
                    }});
                }};

                video.addEventListener('canplaythrough', tryToPlay, {{ once: true }});
                
                video.addEventListener('ended', () => {{
                    console.log("Video ended, transitioning...");
                    video.style.opacity = 0;
                    audio.pause();
                    audio.currentTime = 0;
                    introTextContainer.style.opacity = 0;
                    setTimeout(sendBackToStreamlit, 500);
                }});

                video.addEventListener('error', (e) => {{
                    console.error("Video error detected (Codec/Base64/File corrupted). Skipping intro:", e);
                    sendBackToStreamlit();
                }});

                const clickHandler = () => {{
                    console.log("User interaction detected, forcing play attempt.");
                    tryToPlay();
                    document.removeEventListener('click', clickHandler);
                    document.removeEventListener('touchstart', clickHandler);
                }};
                
                document.addEventListener('click', clickHandler, {{ once: true }});
                document.addEventListener('touchstart', clickHandler, {{ once: true }});
                
                video.load();
                
                const chars = introTextContainer.querySelectorAll('.intro-char');
                chars.forEach((char, index) => {{
                    char.style.animationDelay = `${{index * 0.1}}s`;
                    char.classList.add('char-shown');
                }});
            }}
        }}, 100);
        
        setTimeout(() => {{
            clearInterval(waitForElements);
            const video = document.getElementById('intro-video');
            if (video && !video.src) {{
                console.warn("Timeout before video source set. Force transitioning to main content.");
                sendBackToStreamlit();
            }}
        }}, 5000);
    }});
</script>
"""

html_content_modified = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        html, body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            height: 100vh;
            width: 100vw;
            background-color: #000;
        }}
        
        #intro-video {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            z-index: 0;
            transition: opacity 1s;
        }}

        #intro-text-container {{
            position: fixed;
            top: 5vh;
            width: 100%;
            text-align: center;
            color: #FFD700;
            font-size: 3vw;
            font-family: 'Sacramento', cursive;
            font-weight: 400;
            text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.8);
            z-index: 100;
            pointer-events: none;
            display: flex;
            justify-content: center;
            opacity: 1;
            transition: opacity 0.5s;
        }}
        
        .intro-char {{
            display: inline-block;
            opacity: 0;
            transform: translateY(-50px);
            animation-fill-mode: forwards;
            animation-duration: 0.8s;
            animation-timing-function: ease-out;
        }}

        @keyframes charDropIn {{
            from {{
                opacity: 0;
                transform: translateY(-50px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .intro-char.char-shown {{
            animation-name: charDropIn;
        }}

        @media (max-width: 768px) {{
            #intro-text-container {{
                font-size: 6vw;
            }}
        }}
    </style>
</head>
<body>
    <div id="intro-text-container">KHÁM PHÁ THẾ GIỚI CÙNG CHÚNG TÔI</div>
    <video id="intro-video" muted playsinline></video>
    <audio id="background-audio"></audio>
    {js_callback_video}
</body>
</html>
"""

# Xử lý nội dung của tiêu đề video intro để thêm hiệu ứng chữ thả
intro_title = "KHÁM PHÁ THẾ GIỚI CÙNG CHÚNG TÔI"
intro_chars_html = ''.join([
    f'<span class="intro-char">{char}</span>' if char != ' ' else '<span class="intro-char">&nbsp;</span>'
    for char in intro_title
])
html_content_modified = html_content_modified.replace(
    "<div id=\"intro-text-container\">KHÁM PHÁ THẾ GIỚI CÙNG CHÚNG TÔI</div>",
    f"<div id=\"intro-text-container\">{intro_chars_html}</div>"
)

# --- HIỂN THỊ IFRAME VIDEO ---
st.components.v1.html(html_content_modified, height=1080, scrolling=False)

# --- HIỆU ỨNG REVEAL VÀ NỘI DUNG CHÍNH ---

# Tạo Lưới Reveal
grid_cells_html = ""
for i in range(240):
    grid_cells_html += f'<div class="grid-cell"></div>'

reveal_grid_html = f"""
<div class="reveal-grid">
    {grid_cells_html}
</div>
"""
st.markdown(reveal_grid_html, unsafe_allow_html=True)

# --- NỘI DUNG CHÍNH (TIÊU ĐỀ ĐƠN, ĐỔI MÀU) ---
main_title_text = "TỔ BẢO DƯỠNG SỐ 1"

# Nhúng tiêu đề
st.markdown(f"""
<div id="main-title-container">
    <h1>{main_title_text}</h1>
</div>
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

# --- NAVIGATION BUTTON (ĐÃ CHỈNH SỬA HTML) ---
# Dòng nav-btn-desc phải tồn tại trong HTML, nhưng đã bị ẩn bằng CSS
st.markdown("""
<div class="nav-container">
    <a href="/partnumber" target="_self" class="nav-btn">
        <div class="nav-btn-icon">🔍</div>
        <div class="nav-btn-text">TRA CỨU PART NUMBER</div>
        <div class="nav-btn-desc"></div>
    </a>
</div>
""", unsafe_allow_html=True)
