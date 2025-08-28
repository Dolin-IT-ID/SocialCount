#!/usr/bin/env python3
"""
Streamlit Video Extractor - Antarmuka Web untuk Ekstraksi Detail Video
Terintegrasi dengan VLM (Vision-Language Model) untuk analisis tambahan

Author: Social Media Scraper
Date: 2024
"""

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from typing import Optional, Dict, Any
import base64
import io

# Import fungsi dari extract_video_details.py
from extract_video_details import (
    extract_video_details,
    get_scraper,
    format_number,
    validate_upload_date,
    calculate_completeness_score
)
from utils.url_detector import URLDetector
from services.ollama_service import OllamaService
from vlm_metrics_analyzer import analyze_video_with_vlm, VLMAnalysisResult

# Import untuk MongoDB dan export
from database.mongodb_config import mongo_db
from utils.export_utils import data_exporter

# Import sistem internasionalisasi
from i18n import (
    init_language, get_text, t, create_language_switcher,
    get_tab_names, show_success_message, show_error_message,
    show_warning_message, show_info_message, get_current_language
)

def detect_platform(url: str) -> str:
    """Deteksi platform dari URL"""
    url_lower = url.lower()
    if 'youtube.com' in url_lower or 'youtu.be' in url_lower:
        return 'youtube'
    elif 'tiktok.com' in url_lower:
        return 'tiktok'
    elif 'facebook.com' in url_lower or 'fb.watch' in url_lower:
        return 'facebook'
    else:
        return 'unknown'

# Konfigurasi halaman
st.set_page_config(
    page_title="🎬 Video Extractor Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk styling yang menarik
st.markdown("""
<style>
.main-header {
    font-size: 3.5rem;
    font-weight: bold;
    text-align: center;
    background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 2rem;
}

.platform-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1rem 0;
    color: white;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
}

.metric-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    padding: 1.5rem;
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    margin: 0.5rem 0;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
}

.success-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    margin: 1rem 0;
}

.error-card {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    margin: 1rem 0;
}

.info-card {
    background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    margin: 1rem 0;
}

.stButton > button {
    background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 0.5rem 2rem;
    font-weight: bold;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.sidebar .sidebar-content {
    background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
}
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Inisialisasi session state"""
    if 'extraction_history' not in st.session_state:
        st.session_state.extraction_history = []
    if 'ollama_service' not in st.session_state:
        st.session_state.ollama_service = None
    if 'vlm_enabled' not in st.session_state:
        st.session_state.vlm_enabled = False

def setup_vlm_service():
    """Setup VLM service"""
    try:
        if st.session_state.ollama_service is None:
            st.session_state.ollama_service = OllamaService()
        
        # Test koneksi
        health = st.session_state.ollama_service.health_check()
        if health.get('service_available', False):
            st.session_state.vlm_enabled = True
            return True
        else:
            st.session_state.vlm_enabled = False
            return False
    except Exception as e:
        st.session_state.vlm_enabled = False
        return False

def display_header():
    """Tampilkan header aplikasi"""
    # Initialize language system
    init_language()
    
    # Dynamic header based on language
    app_title = get_text('app_title')
    app_subtitle = get_text('app_subtitle')
    
    st.markdown(f'<h1 class="main-header">{app_title}</h1>', unsafe_allow_html=True)
    st.markdown(
        f"<p style='text-align: center; font-size: 1.3rem; color: #666; margin-bottom: 2rem;'>"
        f"{app_subtitle}"
        "</p>", 
        unsafe_allow_html=True
    )
    st.markdown("---")

def display_sidebar():
    """Tampilkan sidebar dengan informasi dan konfigurasi"""
    # Language switcher at the top
    create_language_switcher()
    
    st.sidebar.markdown(
        f"<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); "
        "padding: 1rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 1rem;'>"
        f"<h2>⚙️ {get_text('sidebar_title')}</h2></div>", 
        unsafe_allow_html=True
    )
    
    # VLM Status
    st.sidebar.subheader(f"🤖 {get_text('sidebar_vlm')}")
    if st.sidebar.button("🔍 Cek Status VLM"):
        with st.sidebar:
            with st.spinner(get_text('analyzing')):
                vlm_available = setup_vlm_service()
                if vlm_available:
                    st.success(get_text('vlm_active'))
                    st.info(get_text('ai_ready'))
                else:
                    st.error(get_text('vlm_inactive'))
                    st.warning(get_text('ai_unavailable'))
    
    # Platform yang didukung
    st.sidebar.markdown("---")
    st.sidebar.subheader(f"📱 {get_text('sidebar_title')}")
    platforms = {
        "YouTube": {"icon": "🎥", "features": get_text('youtube_features', [])},
        "TikTok": {"icon": "🎵", "features": get_text('tiktok_features', [])}, 
        "Facebook": {"icon": "👥", "features": get_text('facebook_features', [])}
    }
    
    for platform, info in platforms.items():
        with st.sidebar.expander(f"{info['icon']} {platform}"):
            for feature in info['features']:
                st.markdown(f"• {feature}")
    
    # Fitur VLM
    st.sidebar.markdown("---")
    st.sidebar.subheader(f"🧠 {get_text('sidebar_vlm')}")
    vlm_features = get_text('vlm_features', [])
    for feature in vlm_features:
        st.sidebar.markdown(f"• {feature}")
    
    # Instruksi penggunaan
    st.sidebar.markdown("---")
    st.sidebar.subheader(f"📋 {get_text('sidebar_usage')}")
    usage_steps = get_text('usage_steps', [])
    for i, step in enumerate(usage_steps, 1):
        st.sidebar.markdown(f"{i}. {step}")

def validate_url_input(url: str) -> tuple[bool, str, str]:
    """Validasi input URL"""
    if not url or not url.strip():
        return False, "", "URL tidak boleh kosong"
    
    url = url.strip()
    platform = URLDetector.detect_platform(url)
    
    if not platform:
        return False, "", "Platform tidak dapat dideteksi. Pastikan URL dari YouTube, TikTok, atau Facebook"
    
    return True, platform, ""

def generate_vlm_analysis(video_data: Dict[str, Any]) -> str:
    """Generate analisis VLM untuk data video"""
    if not st.session_state.vlm_enabled or not st.session_state.ollama_service:
        return "VLM tidak tersedia untuk analisis"
    
    try:
        # Siapkan prompt untuk VLM
        stats = video_data.get('stats', {})
        prompt = f"""
        Analisis data video berikut dan berikan insight mendalam:
        
        Judul: {stats.get('title', 'N/A')}
        Platform: {stats.get('platform', 'N/A')}
        Views: {stats.get('views', 0):,}
        Likes: {stats.get('likes', 0):,}
        Comments: {stats.get('comments', 0):,}
        Shares: {stats.get('shares', 0):,}
        Upload Date: {stats.get('upload_date', 'N/A')}
        
        Berikan analisis dalam bahasa Indonesia yang mencakup:
        1. Performa engagement (engagement rate, rasio like/view, dll)
        2. Prediksi tren dan potensi viral
        3. Rekomendasi untuk meningkatkan performa
        4. Insight tentang audience behavior
        5. Perbandingan dengan standar industri
        
        Format jawaban dalam markdown dengan emoji yang sesuai.
        """
        
        # Panggil VLM
        response = st.session_state.ollama_service.generate_response(prompt)
        return response
        
    except Exception as e:
        return f"Error dalam analisis VLM: {str(e)}"

def display_video_stats(video_data: Dict[str, Any], vlm_result: VLMAnalysisResult = None):
    """Tampilkan statistik video dengan visualisasi dan integrasi VLM"""
    if 'error' in video_data:
        st.markdown(
            f"<div class='error-card'>❌ Error: {video_data['error']}</div>", 
            unsafe_allow_html=True
        )
        return
    
    stats = video_data.get('stats')
    if not stats:
        st.error(get_text('stats_unavailable'))
        return
    
    # VLM Analysis Section
    if vlm_result:
        st.subheader("🤖 VLM Analysis Results")
        
        if vlm_result.analysis_successful:
            # Overall confidence indicator
            confidence_color = "green" if vlm_result.overall_confidence > 0.8 else "orange" if vlm_result.overall_confidence > 0.6 else "red"
            st.markdown(f"**Overall Confidence:** <span style='color: {confidence_color}'>{vlm_result.overall_confidence:.1%}</span>", unsafe_allow_html=True)
            
            # Comparison view toggle
            show_comparison = st.checkbox("Show Scraped vs VLM Comparison", value=True)
            
            if show_comparison:
                st.subheader("📊 Metrics Comparison")
                
                # Create comparison table
                comparison_data = []
                for metric_name, analysis in vlm_result.metrics.items():
                     scraped_val = video_data.get(metric_name, None)
                     comparison_data.append({
                         'Metric': metric_name.title(),
                         'Scraped': f"{scraped_val:,}" if scraped_val else "N/A",
                         'VLM Detected': f"{analysis.vlm_detected_value:,}" if analysis.vlm_detected_value else "N/A",
                         'Final Value': f"{analysis.final_value:,}" if analysis.final_value else "N/A",
                         'Confidence': f"{analysis.confidence_score:.1%}",
                         'Status': "✅ Verified" if analysis.is_verified else "⚠️ Unverified"
                     })
                
                df_comparison = pd.DataFrame(comparison_data)
                st.dataframe(df_comparison, use_container_width=True)
        else:
            st.error(f"❌ VLM Analysis failed: {vlm_result.error_message}")
    
    # Header informasi video
    st.subheader("📹 Informasi Video")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**🎬 Judul:** {stats.title or 'Tidak ditemukan'}")
        st.markdown(f"**👤 Author:** {stats.author or 'Tidak ditemukan'}")
        st.markdown(f"**🌐 Platform:** {stats.platform.upper() if stats.platform else 'Unknown'}")
        if stats.upload_date:
            date_analysis = validate_upload_date(stats.upload_date)
            if date_analysis['is_valid']:
                st.markdown(f"**📅 Upload:** {date_analysis['formatted_date']} ({date_analysis['age_years']} tahun lalu)")
            else:
                st.markdown(f"**📅 Upload:** {stats.upload_date}")
    
    with col2:
        # Skor kelengkapan
        completeness = calculate_completeness_score(stats)
        score_color = "green" if completeness['score'] >= 80 else "orange" if completeness['score'] >= 60 else "red"
        st.markdown(
            f"<div style='text-align: center; padding: 1rem; background: {score_color}; "
            f"border-radius: 10px; color: white;'>"
            f"<h3>📊 Skor Kelengkapan</h3>"
            f"<h2>{completeness['score']}%</h2>"
            f"<p>{completeness['found_count']}/{completeness['total_count']} field</p>"
            f"</div>", 
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # Metrics dalam grid
    st.subheader("📊 Statistik Engagement")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Determine which values to show (VLM final values if available, otherwise scraped)
    display_values = {}
    if vlm_result and vlm_result.analysis_successful:
        for metric in ['views', 'likes', 'comments', 'shares']:
            if metric in vlm_result.metrics and vlm_result.metrics[metric].final_value:
                display_values[metric] = vlm_result.metrics[metric].final_value
            else:
                display_values[metric] = video_data.get(metric, None)
    else:
        display_values = {
            'views': video_data.get('views', None),
            'likes': video_data.get('likes', None),
            'comments': video_data.get('comments', None),
            'shares': video_data.get('shares', None)
        }
    
    metrics = [
        ("👀 Views", display_values['views'], col1, 'views'),
        ("👍 Likes", display_values['likes'], col2, 'likes'),
        ("💬 Comments", display_values['comments'], col3, 'comments'),
        ("📤 Shares", display_values['shares'], col4, 'shares')
    ]
    
    for label, value, col, metric_key in metrics:
        with col:
            formatted_value = format_number(value) if value is not None else "N/A"
            confidence_indicator = ""
            if vlm_result and vlm_result.analysis_successful and metric_key in vlm_result.metrics:
                conf = vlm_result.metrics[metric_key].confidence_score
                confidence_indicator = f" ({conf:.0%})" if conf > 0 else ""
            st.metric(label=f"{label}{confidence_indicator}", value=formatted_value)
    
    # Visualisasi data
    st.subheader("📈 Visualisasi Data")
    
    # Siapkan data untuk chart menggunakan display_values
    chart_data = []
    for metric_name, value in [("Views", display_values['views']), ("Likes", display_values['likes']), 
                              ("Comments", display_values['comments']), ("Shares", display_values['shares'])]:
        if value is not None and value > 0:
            chart_data.append({"Metric": metric_name, "Value": value})
    
    if chart_data:
        df = pd.DataFrame(chart_data)
        
        # Bar chart
        fig_bar = px.bar(
            df, x="Metric", y="Value",
            title="Statistik Engagement",
            color="Value",
            color_continuous_scale="viridis"
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Pie chart untuk distribusi engagement
        if len(chart_data) > 1:
            fig_pie = px.pie(
                df, values="Value", names="Metric",
                title="Distribusi Engagement"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    # Engagement rate calculation using display_values
    if display_values['views'] and display_values['likes']:
        engagement_rate = (display_values['likes'] / display_values['views']) * 100
        st.subheader("🎯 Analisis Engagement")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📈 Engagement Rate", f"{engagement_rate:.2f}%")
        
        with col2:
            if display_values['comments'] and display_values['views']:
                comment_rate = (display_values['comments'] / display_values['views']) * 100
                st.metric("💬 Comment Rate", f"{comment_rate:.2f}%")
        
        with col3:
            if display_values['shares'] and display_values['views']:
                share_rate = (display_values['shares'] / display_values['views']) * 100
                st.metric("📤 Share Rate", f"{share_rate:.2f}%")

def save_extraction_data(video_data: Dict[str, Any], filename: str = None):
    """Simpan data ekstraksi ke file JSON"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"video_extraction_{timestamp}.json"
    
    # Tambahkan timestamp
    video_data['extraction_timestamp'] = datetime.now().isoformat()
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(video_data, f, indent=2, ensure_ascii=False, default=str)
        return filename
    except Exception as e:
        st.error(f"Error menyimpan file: {str(e)}")
        return None

def create_download_link(video_data: Dict[str, Any]):
    """Buat link download untuk data ekstraksi"""
    # Convert to JSON string
    json_str = json.dumps(video_data, indent=2, ensure_ascii=False, default=str)
    
    # Encode to base64
    b64 = base64.b64encode(json_str.encode()).decode()
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"video_extraction_{timestamp}.json"
    
    # Create download link
    href = f'<a href="data:application/json;base64,{b64}" download="{filename}">📥 Download Data JSON</a>'
    return href

def display_extraction_history():
    """Tampilkan riwayat ekstraksi"""
    if not st.session_state.extraction_history:
        st.info(get_text('history_empty'))
        return
    
    st.subheader(f"{get_text('history_title')} ({len(st.session_state.extraction_history)} {get_text('video_count')})")
    
    # Summary statistics
    total_views = sum(item.get('stats', {}).get('views', 0) or 0 for item in st.session_state.extraction_history if 'stats' in item)
    total_likes = sum(item.get('stats', {}).get('likes', 0) or 0 for item in st.session_state.extraction_history if 'stats' in item)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(get_text('total_videos'), len(st.session_state.extraction_history))
    with col2:
        st.metric(get_text('total_views'), format_number(total_views))
    with col3:
        st.metric(get_text('total_likes'), format_number(total_likes))
    
    st.markdown("---")
    
    # Display history items
    for i, item in enumerate(reversed(st.session_state.extraction_history), 1):
        with st.expander(f"Video #{len(st.session_state.extraction_history) - i + 1} - {item.get('timestamp', 'Unknown time')}"):
            if 'error' not in item:
                stats = item.get('stats', {})
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**{get_text('title_label')}:** {stats.get('title', 'N/A')[:50]}...")
                    st.markdown(f"**{get_text('platform_label')}:** {stats.get('platform', 'N/A').upper()}")
                    st.markdown(f"**URL:** {item.get('url', 'N/A')[:50]}...")
                
                with col2:
                    st.markdown(f"**Views:** {format_number(stats.get('views'))}")
                    st.markdown(f"**Likes:** {format_number(stats.get('likes'))}")
                    st.markdown(f"**Comments:** {format_number(stats.get('comments'))}")
            else:
                st.error(f"Error: {item['error']}")
    
    # Clear history button
    if st.button(get_text('clear_history'), type="secondary"):
        st.session_state.extraction_history = []
        st.success(get_text('history_cleared'))
        st.rerun()

def main():
    """Fungsi utama aplikasi"""
    initialize_session_state()
    display_header()
    display_sidebar()
    
    # Setup VLM service
    setup_vlm_service()
    
    # Main tabs with dynamic names
    tab_names = get_tab_names()
    tab1, tab2, tab3, tab4 = st.tabs(tab_names)
    
    with tab1:
        st.subheader(get_text('tab_extract'))
        
        # Input fields untuk informasi tambahan
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            nama_pembuat = st.text_input(
                get_text('creator_name'),
                placeholder=get_text('creator_placeholder'),
                help=get_text('creator_help')
            )
        
        with col_info2:
            waktu_penghitungan = st.date_input(
                get_text('calculation_date'),
                value=datetime.now().date(),
                help=get_text('date_help')
            )
            waktu_jam = st.time_input(
                get_text('calculation_time'),
                value=datetime.now().time(),
                help=get_text('time_help')
            )
            # Gabungkan tanggal dan jam menjadi datetime
            waktu_penghitungan = datetime.combine(waktu_penghitungan, waktu_jam)
        
        # URL input dan nama akun dalam satu baris
        col_url1, col_url2 = st.columns([3, 1])
        
        with col_url1:
            url_input = st.text_input(
                get_text('url_input'),
                placeholder=get_text('url_placeholder'),
                help=get_text('url_help')
            )
        
        with col_url2:
            nama_akun = st.text_input(
                "📱 Nama Akun:",
                placeholder="@username",
                help="Nama akun/username dari platform"
            )
        
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            extract_button = st.button(get_text('extract_button'), type="primary")
        
        with col2:
            vlm_analysis = st.checkbox("🤖 Analisis VLM", value=st.session_state.vlm_enabled, disabled=not st.session_state.vlm_enabled)
        
        with col3:
            save_data = st.checkbox("💾 Simpan Data", value=False)
        
        with col4:
            save_to_db = st.button("💾 Tambahkan ke Database", help="Simpan data ke MongoDB")
        
        if extract_button and url_input:
            # Validasi URL
            is_valid, platform, error_msg = validate_url_input(url_input)
            
            if not is_valid:
                st.markdown(
                    f"<div class='error-card'>❌ {error_msg}</div>", 
                    unsafe_allow_html=True
                )
            else:
                # Tampilkan info platform
                platform_icons = {'youtube': '🎥', 'tiktok': '🎵', 'facebook': '👥'}
                icon = platform_icons.get(platform, '📱')
                
                st.markdown(
                    f"<div class='success-card'>✅ Platform terdeteksi: {icon} {platform.upper()}</div>", 
                    unsafe_allow_html=True
                )
                
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Ekstraksi data
                    status_text.text("🔍 Menganalisis URL...")
                    progress_bar.progress(25)
                    
                    status_text.text("📊 Mengekstrak metadata...")
                    progress_bar.progress(50)
                    
                    # Panggil fungsi ekstraksi
                    video_data = extract_video_details(url_input, save_to_file=False)
                    progress_bar.progress(75)
                    
                    if 'error' not in video_data:
                        status_text.text("✅ Ekstraksi berhasil!")
                        progress_bar.progress(100)
                        
                        # Tambahkan informasi tambahan
                        video_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        video_data['url'] = url_input
                        video_data['nama_pembuat'] = nama_pembuat
                        video_data['nama_akun'] = nama_akun
                        video_data['waktu_penghitungan'] = waktu_penghitungan
                        video_data['platform'] = platform
                        
                        # Simpan ke history
                        st.session_state.extraction_history.append(video_data.copy())
                        
                        # VLM Analysis jika diminta
                        vlm_analysis_result = None
                        if vlm_analysis and st.session_state.vlm_enabled:
                            with st.spinner("🤖 Melakukan analisis VLM..."):
                                try:
                                    # Deteksi platform dari URL
                                    platform = detect_platform(url_input)
                                    vlm_analysis_result = analyze_video_with_vlm(
                                        url_input, 
                                        video_data, 
                                        platform
                                    )
                                except Exception as e:
                                    st.warning(f"⚠️ VLM analysis gagal: {str(e)}")
                        
                        # Tampilkan hasil
                        st.success(get_text('extraction_success'))
                        display_video_stats(video_data, vlm_analysis_result)
                        
                        # Download link
                        st.subheader("💾 Download Data")
                        download_link = create_download_link(video_data)
                        st.markdown(download_link, unsafe_allow_html=True)
                        
                        # Save to file if requested
                        if save_data:
                            filename = save_extraction_data(video_data)
                            if filename:
                                st.success(f"✅ Data disimpan ke: {filename}")
                        
                        # Simpan ke database jika diminta
                        if save_to_db:
                            if not nama_pembuat or not nama_akun:
                                st.warning(get_text('fill_creator_warning'))
                            else:
                                with st.spinner("💾 Menyimpan ke database..."):
                                    success = mongo_db.insert_video_data(video_data)
                                    if success:
                                        st.success(get_text('data_saved_success'))
                                    else:
                                        st.error(get_text('data_save_failed'))
                    
                    else:
                        status_text.text("❌ Ekstraksi gagal")
                        progress_bar.progress(100)
                        st.markdown(
                            f"<div class='error-card'>❌ {video_data['error']}</div>", 
                            unsafe_allow_html=True
                        )
                
                except Exception as e:
                    status_text.text("❌ Error")
                    progress_bar.progress(100)
                    st.error(f"Error: {str(e)}")
                
                finally:
                    # Clear progress indicators after 2 seconds
                    import time
                    time.sleep(2)
                    progress_bar.empty()
                    status_text.empty()
        
        elif extract_button and not url_input:
            st.warning(get_text('enter_url_warning'))
    
    with tab2:
        st.subheader(get_text('tab_batch'))
        
        st.markdown(
            f"<div class='info-card'>💡 {get_text('batch_info')}</div>", 
            unsafe_allow_html=True
        )
        
        # Multiple URL input
        urls_text = st.text_area(
            get_text('batch_urls'),
            height=200,
            placeholder=get_text('batch_placeholder')
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            batch_extract = st.button(get_text('batch_extract'), type="primary")
        
        with col2:
            batch_vlm = st.checkbox(get_text('batch_vlm'), value=False, disabled=not st.session_state.vlm_enabled)
        
        if batch_extract and urls_text.strip():
            urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
            
            if urls:
                st.info(f"📊 Memproses {len(urls)} URL...")
                
                # Progress tracking
                progress_bar = st.progress(0)
                results = []
                
                for i, url in enumerate(urls):
                    st.write(f"🔍 Memproses URL {i+1}/{len(urls)}: {url[:50]}...")
                    
                    try:
                        video_data = extract_video_details(url, save_to_file=False)
                        video_data['url'] = url
                        video_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        results.append(video_data)
                        
                        # Add to history
                        st.session_state.extraction_history.append(video_data.copy())
                        
                    except Exception as e:
                        results.append({
                            'error': str(e),
                            'url': url,
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                    
                    progress_bar.progress((i + 1) / len(urls))
                
                # Display batch results
                st.success(f"✅ Batch processing selesai! {len(results)} URL diproses.")
                
                # Summary statistics
                successful = [r for r in results if 'error' not in r]
                failed = [r for r in results if 'error' in r]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📊 Total URL", len(results))
                with col2:
                    st.metric("✅ Berhasil", len(successful))
                with col3:
                    st.metric("❌ Gagal", len(failed))
                
                # Display individual results
                for i, result in enumerate(results, 1):
                    with st.expander(f"URL {i}: {result['url'][:50]}..."):
                        if 'error' not in result:
                            display_video_stats(result)
                        else:
                            st.error(f"Error: {result['error']}")
                
                # Batch VLM analysis
                if batch_vlm and st.session_state.vlm_enabled and successful:
                    st.subheader("🤖 Analisis VLM Batch")
                    with st.spinner("🧠 Menganalisis semua video dengan AI..."):
                        for i, result in enumerate(successful, 1):
                            st.write(f"**Video {i}:**")
                            ai_analysis = generate_vlm_analysis(result)
                            st.markdown(ai_analysis)
                            st.markdown("---")
            
            else:
                st.warning(get_text('no_valid_urls'))
        
        elif batch_extract and not urls_text.strip():
            st.warning(get_text('enter_urls_first'))
    
    with tab3:
        display_extraction_history()
    
    with tab4:
        st.subheader(get_text('tab_database'))
        
        # Database connection status
        col_status1, col_status2 = st.columns(2)
        
        with col_status1:
            if st.button(get_text('check_db_connection')):
                with st.spinner(get_text('checking_mongodb')):
                    if mongo_db.connect():
                        st.success(get_text('mongodb_success'))
                        total_videos = mongo_db.get_video_count()
                        st.info(f"{get_text('total_db_videos')}: {total_videos}")
                    else:
                        st.error(get_text('mongodb_failed'))
        
        with col_status2:
            st.info(f"💡 **{get_text('tips_label')}:** {get_text('mongodb_tips')}")
        
        st.markdown("---")
        
        # Filter data berdasarkan tanggal
        st.subheader(get_text('filter_data'))
        
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        
        with col_filter1:
            start_date = st.date_input(
                get_text('start_date'),
                value=datetime.now().date().replace(day=1),  # Awal bulan
                help=get_text('start_date_help')
            )
        
        with col_filter2:
            end_date = st.date_input(
                get_text('end_date'),
                value=datetime.now().date(),
                help=get_text('end_date_help')
            )
        
        with col_filter3:
            load_data_btn = st.button(get_text('load_data'), type="primary")
        
        # Load dan tampilkan data
        if load_data_btn or 'db_video_data' not in st.session_state:
            with st.spinner(get_text('loading_data')):
                start_datetime = datetime.combine(start_date, datetime.min.time())
                end_datetime = datetime.combine(end_date, datetime.max.time())
                
                video_data = mongo_db.get_all_videos(start_datetime, end_datetime)
                st.session_state.db_video_data = video_data
        
        if 'db_video_data' in st.session_state and st.session_state.db_video_data:
            video_data = st.session_state.db_video_data
            
            # Tampilkan ringkasan data
            st.subheader(get_text('data_summary'))
            data_exporter.display_export_summary(video_data)
            
            st.markdown("---")
            
            # Preview data dalam tabel
            st.subheader(get_text('data_preview'))
            
            if st.checkbox(get_text('show_data_table')):
                df = data_exporter.prepare_data_for_export(video_data)
                if not df.empty:
                    # Pilih kolom yang akan ditampilkan
                    display_columns = st.multiselect(
                        get_text('select_columns'),
                        options=df.columns.tolist(),
                        default=['Nama Pembuat Video', 'Nama Akun', 'Platform', 'Judul Video', 'Views', 'Waktu Penghitungan']
                    )
                    
                    if display_columns:
                        st.dataframe(
                            df[display_columns],
                            use_container_width=True,
                            height=400
                        )
                    else:
                        st.warning(get_text('select_min_column'))
                else:
                    st.info(get_text('no_data_display'))
            
            st.markdown("---")
            
            # Ekspor data
            st.subheader(get_text('export_data'))
            
            col_export1, col_export2, col_export3 = st.columns(3)
            
            with col_export1:
                st.write(f"**{get_text('export_format')}:**")
                export_format = st.radio(
                    get_text('select_export_format'),
                    options=["CSV", "Excel Detail", "Excel Ringkasan"],
                    horizontal=False,
                    help=get_text('export_format_help')
                )
            
            with col_export2:
                st.write(f"**{get_text('format_preview')}:**")
                if export_format == "Excel Ringkasan":
                    st.info(get_text('summary_format_info'))
                elif export_format == "Excel Detail":
                    st.info(get_text('detail_format_info'))
                else:
                    st.info(get_text('csv_format_info'))
            
            with col_export3:
                st.write("**Aksi Ekspor:**")
                if st.button(f"📥 Ekspor ke {export_format}", use_container_width=True):
                    with st.spinner(f"📦 Menyiapkan file {export_format}..."):
                        try:
                            if export_format == "CSV":
                                file_data = data_exporter.export_to_csv(video_data)
                                filename = data_exporter.generate_filename("csv")
                            elif export_format == "Excel Detail":
                                file_data = data_exporter.export_to_excel(video_data)
                                filename = data_exporter.generate_filename("excel", "video_detail")
                            else:  # Excel Ringkasan
                                file_data = data_exporter.export_summary_to_excel(video_data)
                                filename = data_exporter.generate_filename("excel", "ringkasan_statistik")
                            
                            if file_data:
                                format_name = export_format if export_format == "CSV" else "Excel"
                                data_exporter.create_download_link(file_data, filename, format_name)
                                st.success(f"✅ File {export_format} siap untuk diunduh!")
                            else:
                                st.error(get_text('export_failed'))
                        except Exception as e:
                            st.error(f"❌ Error saat ekspor: {str(e)}")
            
            # Statistik tambahan
            st.markdown("---")
            st.subheader("📊 Statistik Platform")
            
            if video_data:
                # Hitung statistik per platform
                platform_stats = {}
                for video in video_data:
                    platform = video.get('platform', 'Unknown')
                    if platform not in platform_stats:
                        platform_stats[platform] = {'count': 0, 'total_views': 0}
                    platform_stats[platform]['count'] += 1
                    platform_stats[platform]['total_views'] += video.get('views', 0)
                
                # Tampilkan dalam kolom
                cols = st.columns(len(platform_stats))
                for i, (platform, stats) in enumerate(platform_stats.items()):
                    with cols[i]:
                        st.metric(
                            f"📱 {platform.upper()}",
                            f"{stats['count']} video",
                            f"{format_number(stats['total_views'])} views"
                        )
        
        elif 'db_video_data' in st.session_state:
            st.info(get_text('no_data_range'))
        else:
            st.info(get_text('click_load_data'))

if __name__ == "__main__":
    main()