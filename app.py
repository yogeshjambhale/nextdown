import streamlit as st
import yt_dlp

# --- NEXT-LEVEL SEO CONFIGURATION ---
st.set_page_config(
    page_title="Free Video Downloader - Download YouTube, Instagram, TikTok & FB Videos",
    page_icon="📥",
    layout="centered"
)

# Invisible Meta Tags & Schema Markup Injection for Search Engine Crawlers (Googlebot)
st.markdown("""
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebApplication",
      "name": "NexDown Video Downloader",
      "url": "https://nexdown.streamlit.app/",
      "description": "The ultimate free online video downloader. Download MP4 and MP3 from YouTube, Instagram Reels, TikTok (no watermark), Facebook, and Twitter instantly.",
      "applicationCategory": "MultimediaApplication",
      "operatingSystem": "All"
    }
    </script>
    <style>
        /* Hidden meta-data for bots if needed, though Schema is better */
        .seo-hidden { display: none; }
    </style>
""", unsafe_allow_html=True)


# Custom CSS for dark-mode aesthetic
st.markdown("""
<style>
    /* Dark layout configuration */
    .stApp { background-color: #0f172a; }
    .stApp header { background-color: transparent !important; }
    
    .stTextInput>div>div>input {
        background-color: rgba(30, 41, 59, 0.7);
        color: #ffffff;
        border-radius: 12px;
        padding: 14px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        font-size: 1.1rem;
    }
    .stTextInput>div>div>input:focus {
        border-color: #8b5cf6;
        box-shadow: 0 0 0 1px #8b5cf6;
    }
    
    .title-highlight { color: #8b5cf6; }
    .h1-seo {
        text-align: center;
        font-size: 4rem;
        margin-bottom: 0px;
        color: #f8fafc;
        font-weight: 800;
    }
    .subtitle-seo {
        text-align: center;
        color: #94a3b8;
        font-size: 1.2rem;
        margin-top: 5px;
        margin-bottom: 30px;
    }
    
    .stButton>button {
        background-color: #8b5cf6;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        border: none;
        width: 100%;
        transition: all 0.2s;
        margin-top: 10px;
    }
    .stButton>button:hover {
        background-color: #7c3aed;
        color: white;
        transform: translateY(-2px);
    }
    
    .download-btn {
        background-color: #10b981;
        color: white !important;
        padding: 8px 24px;
        border-radius: 8px;
        text-decoration: none !important;
        display: inline-block;
        font-weight: 600;
        transition: all 0.2s;
    }
    .download-btn:hover {
        background-color: #0ea5e9;
        transform: translateY(-2px);
    }
    
    .format-row {
        background: rgba(255, 255, 255, 0.05);
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .badge {
        background: rgba(139, 92, 246, 0.3);
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        color: white;
    }
    .size-text { color: #94a3b8; font-size: 0.9rem; }
    
    /* SEO Text Box at Bottom */
    .seo-article {
        margin-top: 60px;
        padding: 30px;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        color: #94a3b8;
    }
    .seo-article h2, .seo-article h3 { color: #e2e8f0; }
    .seo-article p { line-height: 1.6; font-size: 1rem; }
</style>
""", unsafe_allow_html=True)

# Optimized H1 Tag for Primary Keywords
st.markdown("<h1 class='h1-seo'>Nex<span class='title-highlight'>Down</span></h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-seo'>The #1 Free Universal Video Downloader</div>", unsafe_allow_html=True)

with st.form("download_form", clear_on_submit=False):
    url = st.text_input("Video URL", label_visibility="collapsed", placeholder="Paste YouTube, Instagram, or TikTok link here...")
    submitted = st.form_submit_button("Download Video 🚀")

def format_bytes(bytes_num):
    if not bytes_num:
        return "? MB"
    for x in ['Bytes', 'KB', 'MB', 'GB', 'TB']:
        if bytes_num < 1024.0:
            return f"{bytes_num:3.1f} {x}"
        bytes_num /= 1024.0
    return "Unknown"

if submitted and url:
    with st.spinner("Crunching media streams..."):
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'youtube_skip_dash_manifest': True
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
            col1, col2 = st.columns([1, 1.5], gap="large")
            
            with col1:
                st.markdown("<div style='margin-top: 20px;'>", unsafe_allow_html=True)
                if info.get('thumbnail'):
                    st.image(info['thumbnail'], use_column_width=True)
                if info.get('duration_string'):
                    st.caption(f"⏱️ Duration: {info['duration_string']}")
                st.markdown("</div>", unsafe_allow_html=True)
                    
            with col2:
                st.markdown(f"### {info.get('title', 'Unknown Media')}")
                
                formats = info.get('formats', [])
                good_formats = [f for f in formats if f.get('url') and 'http' in str(f.get('protocol', ''))]
                
                if not good_formats:
                    st.warning("No downloadable formats found.")
                else:
                    good_formats = list(reversed(good_formats))[:15]
                    unique_formats = {}
                    for f in good_formats:
                        res = f.get('resolution') or f.get('height') or ('Audio' if f.get('vcodec') == 'none' else 'Unknown')
                        if isinstance(res, int):
                            res = f"{res}p"
                        ext = f.get('ext', 'unknown')
                        key = f"{res}-{ext}"
                        if key not in unique_formats:
                            unique_formats[key] = f
                            
                    st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
                    
                    for f in unique_formats.values():
                        res = f.get('resolution') or f.get('height') or ('Audio' if f.get('vcodec') == 'none' else 'Unknown')
                        if isinstance(res, int):
                            res = f"{res}p"
                        ext = str(f.get('ext', 'unk')).upper()
                        size = format_bytes(f.get('filesize') or f.get('filesize_approx'))
                        is_video_only = f.get('vcodec') != 'none' and (not f.get('acodec') or f.get('acodec') == 'none')
                        warning = "<span style='color: #fbbf24; font-size: 0.8rem;'>(Video Only)</span>" if is_video_only else ""
                        
                        dl_url = f.get('url')
                        
                        st.markdown(f"""
                        <div class="format-row">
                            <div class="format-info">
                                <span class="badge">{res}</span>
                                <span class="size-text">{ext} • {size} {warning}</span>
                            </div>
                            <a href="{dl_url}" target="_blank" class="download-btn">⬇️ Download File</a>
                        </div>
                        """, unsafe_allow_html=True)
                        
        except Exception as e:
            st.error(f"Failed to fetch media. Make sure it's public. details: {str(e)}")

# --- SEARCH ENGINE OPTIMIZATION CONTENT ---
st.markdown("""
<div class="seo-article">
<h2>The Ultimate Free Online Video Downloader</h2>
<p>
NexDown is your all-in-one solution to save videos from across the web. Whether you are looking for a reliable <b>YouTube Video Downloader</b> to save 4K and 1080p MP4 files, or you need to save viral clips using an <b>Instagram Reels Downloader</b> or a <b>TikTok Downloader without watermark</b>, NexDown works instantly directly in your browser. 
</p>

<h3>Features Designed for Speed</h3>
<ul style="color: #94a3b8; font-size: 1rem; line-height: 1.6;">
<li><b>100% Free & No Ads:</b> Enjoy unrestricted downloads without annoying popups.</li>
<li><b>Universal Support:</b> Functions seamlessly as a Facebook video saver, X (Twitter) media downloader, Reddit video extractor, and supports over 1,000+ other websites.</li>
<li><b>High Quality Formats:</b> Export instantly in MP4 HD, WebM, or extract High-Bitrate Audio (MP3/M4A).</li>
<li><b>Privacy-First:</b> No registration required. We do not store, track, or maintain a database of your downloaded video histories.</li>
</ul>

<h3>How to Download Any Video</h3>
<p>
Using NexDown is incredibly simple. Just copy the shareable link of the media from the app or website. Paste the URL into our search bar above and click "Download Video". Our advanced extractors will locate the highest quality streams and provide you with instant, direct download buttons to save them locally to your Mac, Windows, iPhone, or Android device.
</p>

<p style="font-size: 0.8rem; margin-top: 20px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 20px;">
Disclaimer: Please respect copyright laws and the terms of service of the respective platforms. This tool is designed only for downloading publicly available materials for personal use.
</p>
</div>
""", unsafe_allow_html=True)
