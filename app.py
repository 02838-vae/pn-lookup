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
    st.session_state = {'video_ended': False}

# --- CÁC HÀM TIỆN ÍCH (Giữ nguyên) ---

def get_base64_encoded_file(file_path):
    """Đọc file và trả về Base64 encoded string."""
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return None
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode("utf-8")
    except Exception as e:
        return None

# MÃ HÓA TẤT CẢ CÁC FILE (Giữ nguyên logic)
try:
    video_pc_base64 = get_base64_encoded_file("airplane.mp4")
    video_mobile_base64 = get_base64_encoded_file("mobile.mp4")
    audio_base64 = get_base64_encoded_file("plane_fly.mp3")
    bg_pc_base64 = get_base64_encoded_file("cabbase.jpg") 
    bg_mobile_base64 = get_base64_encoded_file("mobile.jpg")
    logo_base64 = get_base64_encoded_file("logo.jpg")

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

if not 'logo_base64' in locals() or not logo_base64:
    logo_base64 = "" 
    st.info("ℹ️ Không tìm thấy file logo.jpg. Music player sẽ không có hình nền logo.")

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
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
}}

/* Ghi đè CSS Streamlit mặc định bọc quanh button */
/* Buộc thẻ p cha của button không có padding/margin và cho phép button nằm giữa */
.nav-container + div > p {{
    margin: 0 !important;
    padding: 0 !important;
    line-height: 0; /* Loại bỏ khoảng trắng do line-height */
}}
.nav-container + div {{
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%; /* Cần thiết để button nằm giữa màn hình */
    width: 100%;
}}


/* Iframe Video Intro và Main Content Styles (Giữ nguyên) */
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
}}

/* TIÊU ĐỀ CHÍNH (Giữ nguyên) */
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
    letter-spacing: 5px;
    white-space: nowrap;
    display: inline-block;
    background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3);
    background-size: 400% 400%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent;
    animation: colorShift 10s ease infinite, scrollText 15s linear infinite;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}}

/* Music Player Styles (Giữ nguyên) */
/* ... */


/* === CSS CHO NAVIGATION BUTTON (ĐÃ GHI ĐÈ MẠNH) === */
.nav-container {{
    /* Đã được điều chỉnh để chỉ là điểm neo, các CSS quan trọng nằm ở a.nav-btn */
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 50;
    opacity: 0;
    transition: opacity 2s ease-out 3s;
    /* Kích thước full để chiếm trọn vị trí cần thiết */
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0; 
}}

.video-finished .nav-container {{
    opacity: 1;
}}

/* Nhắm mục tiêu thẻ a */
.stApp a.nav-btn {{
    position: relative;
    
    /* ✅ 1. THU NHỎ KHUNG */
    padding: 15px 30px !important; /* Ghi đè padding */
    
    /* ❌ 3. BỎ BLUR: Dùng nền trong suốt */
    background: linear-gradient(135deg, rgba(255, 215, 0, 0.4), rgba(255, 165, 0, 0.4));
    
    border: 4px solid #FFD700;
    border-radius: 20px;
    color: #FFD700;
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem; 
    font-weight: 900;
    text-align: center;
    cursor: pointer;
    transition: all 0.4s ease;
    text-decoration: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 5px; 
    overflow: hidden;
    box-shadow: 
        0 10px 40px rgba(255, 215, 0, 0.3),
        inset 0 0 30px rgba(255, 215, 0, 0.1);
    
    /* Quan trọng: Thu hẹp kích thước theo nội dung */
    width: fit-content !important; 
    max-width: 90%;
    
    /* Loại bỏ margin/khoảng cách dư thừa */
    margin: 0 !important;
}}

.stApp a.nav-btn:hover {{
    background: linear-gradient(135deg, rgba(255, 215, 0, 0.6), rgba(255, 165, 0, 0.6));
    border-color: #FFA500;
    transform: translateY(-5px) scale(1.05); 
    box-shadow: 
        0 15px 40px rgba(255, 215, 0, 0.6),
        0 0 30px rgba(255, 215, 0, 0.5),
        inset 0 0 30px rgba(255, 215, 0, 0.3);
}}

.nav-btn-icon {{
    font-size: 2.5rem; 
    margin-bottom: 5px;
    filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.5));
}}

.nav-btn-text {{
    font-size: 1.1rem; 
    letter-spacing: 3px;
    text-transform: uppercase;
    white-space: nowrap; 
}}

.nav-btn-desc {{
    /* ✅ 2. XÓA CHỮ PHỤ */
    display: none !important;
}}

/* Responsive cho mobile */
@media (max-width: 768px) {{
    .stApp a.nav-btn {{
        padding: 15px 25px !important; 
        font-size: 1rem;
        width: 80% !important; 
    }}
    
    .nav-btn-icon {{
        font-size: 2rem;
    }}
    
    .nav-btn-text {{
        font-size: 1rem;
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
             const revealGridParent = revealGrid.parentElement;
             if (revealGridParent) {{
                 revealGridParent.style.display = 'none';
             }}
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
                
                const isMobile = window.innerWidth <= 768;
                const videoSource = isMobile ? 'data:video/mp4;base64,{video_mobile_base64}' : 'data:video/mp4;base64,{video_pc_base64}';

                video.src = videoSource;
                audio.src = 'data:audio/mp3;base64,{audio_base64}';
                
                const tryToPlay = () => {{
                    video.play().then(() => {{
                    }}).catch(err => {{
                        setTimeout(sendBackToStreamlit, 2000);
                    }});

                    audio.play().catch(e => {{
                    }});
                }};

                video.addEventListener('canplaythrough', tryToPlay, {{ once: true }});
                
                video.addEventListener('ended', () => {{
                    video.style.opacity = 0;
                    audio.pause();
                    audio.currentTime = 0;
                    introTextContainer.style.opacity = 0;
                    setTimeout(sendBackToStreamlit, 500);
                }});

                video.addEventListener('error', (e) => {{
                    sendBackToStreamlit();
                }});

                const clickHandler = () => {{
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

# --- NAVIGATION BUTTON (ĐÃ GHI ĐÈ CSS) ---
# Thẻ nav-btn-desc vẫn phải tồn tại trong HTML.
st.markdown("""
<div class="nav-container">
    <a href="/partnumber" target="_self" class="nav-btn">
        <div class="nav-btn-icon">🔍</div>
        <div class="nav-btn-text">TRA CỨU PART NUMBER</div>
        <div class="nav-btn-desc">Tìm kiếm thông tin chi tiết phụ tùng</div>
    </a>
</div>
""", unsafe_allow_html=True)
