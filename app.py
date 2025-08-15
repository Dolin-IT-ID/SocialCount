import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from services import CrewService, OllamaService
from utils import URLDetector
from config import Config

# Page configuration
st.set_page_config(
    page_title="SocialCount - Social Media Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    color: #1f77b4;
    margin-bottom: 2rem;
}
.platform-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
}
.metric-card {
    background-color: #ffffff;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #1f77b4;
    margin: 0.5rem 0;
}
.success-message {
    background-color: #d4edda;
    color: #155724;
    padding: 1rem;
    border-radius: 5px;
    border: 1px solid #c3e6cb;
}
.error-message {
    background-color: #f8d7da;
    color: #721c24;
    padding: 1rem;
    border-radius: 5px;
    border: 1px solid #f5c6cb;
}
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = []
    if 'crew_service' not in st.session_state:
        st.session_state.crew_service = None
    if 'ollama_service' not in st.session_state:
        st.session_state.ollama_service = None

def setup_services():
    """Setup and initialize services"""
    try:
        if st.session_state.crew_service is None:
            st.session_state.crew_service = CrewService()
        if st.session_state.ollama_service is None:
            st.session_state.ollama_service = OllamaService()
        return True
    except Exception as e:
        st.error(f"Error initializing services: {str(e)}")
        return False

def display_header():
    """Display application header"""
    st.markdown('<h1 class="main-header">📊 SocialCount</h1>', unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; font-size: 1.2rem; color: #666;'>"
        "Analisis Statistik Media Sosial dengan AI - YouTube, TikTok & Facebook"
        "</p>", 
        unsafe_allow_html=True
    )
    st.markdown("---")

def display_sidebar():
    """Display sidebar with configuration and info"""
    st.sidebar.header("⚙️ Konfigurasi")
    
    # Service status
    st.sidebar.subheader("Status Layanan")
    
    if st.sidebar.button("🔍 Cek Status Layanan"):
        with st.sidebar:
            with st.spinner("Memeriksa status layanan..."):
                if st.session_state.crew_service:
                    health_status = st.session_state.crew_service.health_check()
                    
                    # Ollama status
                    ollama_status = health_status.get('ollama_service', {})
                    if ollama_status.get('service_available', False):
                        st.success("✅ Ollama: Aktif")
                        if ollama_status.get('model_loaded', False):
                            st.success(f"✅ Model: {Config.OLLAMA_MODEL}")
                        else:
                            st.warning(f"⚠️ Model {Config.OLLAMA_MODEL} tidak ditemukan")
                    else:
                        st.error("❌ Ollama: Tidak aktif")
                    
                    # CrewAI status
                    if health_status.get('crew_agents_ready', False):
                        st.success("✅ CrewAI: Siap")
                    else:
                        st.error("❌ CrewAI: Tidak siap")
                else:
                    st.error("❌ Layanan belum diinisialisasi")
    
    st.sidebar.markdown("---")
    
    # Platform info
    st.sidebar.subheader("📱 Platform yang Didukung")
    platforms = {
        "YouTube": "🎥",
        "TikTok": "🎵", 
        "Facebook": "👥"
    }
    
    for platform, icon in platforms.items():
        st.sidebar.markdown(f"{icon} {platform}")
    
    st.sidebar.markdown("---")
    
    # Instructions
    st.sidebar.subheader("📋 Cara Penggunaan")
    st.sidebar.markdown("""
    1. Masukkan URL postingan media sosial
    2. Klik tombol "Analisis"
    3. Tunggu proses scraping dan analisis
    4. Lihat hasil statistik dan insights
    5. Bandingkan multiple URL jika diperlukan
    """)

def validate_and_display_url_info(url):
    """Validate URL and display platform info"""
    url_info = URLDetector.validate_url(url)
    
    if url_info['valid']:
        platform = url_info['platform']
        platform_icons = {'youtube': '🎥', 'tiktok': '🎵', 'facebook': '👥'}
        icon = platform_icons.get(platform, '📱')
        
        st.success(f"✅ URL Valid - Platform: {icon} {platform.title()}")
        return True, platform
    else:
        st.error(f"❌ URL Tidak Valid: {url_info['error']}")
        return False, None

def calculate_total_views(results):
    """Calculate total views from all social media platforms"""
    total_views = 0
    platform_views = {'youtube': 0, 'tiktok': 0, 'facebook': 0}
    
    for result in results:
        if result.get('success', False):
            stats = result.get('stats', {})
            platform = stats.get('platform', '').lower()
            views = stats.get('views', 0)
            
            if views and isinstance(views, (int, float)) and views > 0:
                total_views += views
                if platform in platform_views:
                    platform_views[platform] += views
    
    return total_views, platform_views

def display_total_views_summary(results):
    """Display total views summary across all platforms"""
    total_views, platform_views = calculate_total_views(results)
    
    if total_views > 0:
        # Header with reset button
        col_header1, col_header2 = st.columns([3, 1])
        with col_header1:
            st.subheader("🌟 Total Views Semua Platform")
        with col_header2:
            if st.button("🔄 Reset Total Views", help="Hapus semua data analisis dan reset total views", type="secondary"):
                st.session_state.analysis_results = []
                st.success("✅ Total views berhasil direset!")
                st.rerun()
        
        # Main total views metric
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📊 Total Views",
                value=f"{total_views:,}",
                help="Total views dari semua platform sosial media"
            )
        
        # Platform breakdown
        platform_icons = {'youtube': '🎥', 'tiktok': '🎵', 'facebook': '👥'}
        platform_names = {'youtube': 'YouTube', 'tiktok': 'TikTok', 'facebook': 'Facebook'}
        
        cols = [col2, col3, col4]
        for i, (platform, views) in enumerate(platform_views.items()):
            if i < len(cols) and views > 0:
                with cols[i]:
                    icon = platform_icons.get(platform, '📱')
                    name = platform_names.get(platform, platform.title())
                    percentage = (views / total_views * 100) if total_views > 0 else 0
                    st.metric(
                        label=f"{icon} {name}",
                        value=f"{views:,}",
                        delta=f"{percentage:.1f}%",
                        help=f"Views dari {name}"
                    )
        
        # Create pie chart for platform distribution
        if len([v for v in platform_views.values() if v > 0]) > 1:
            st.subheader("📈 Distribusi Views per Platform")
            
            # Prepare data for pie chart
            chart_data = []
            for platform, views in platform_views.items():
                if views > 0:
                    icon = platform_icons.get(platform, '📱')
                    name = platform_names.get(platform, platform.title())
                    chart_data.append({
                        'Platform': f"{icon} {name}",
                        'Views': views,
                        'Percentage': (views / total_views * 100) if total_views > 0 else 0
                    })
            
            if chart_data:
                df_pie = pd.DataFrame(chart_data)
                fig_pie = px.pie(
                    df_pie, 
                    values='Views', 
                    names='Platform',
                    title="Distribusi Views per Platform",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_pie.update_traces(
                    textposition='inside', 
                    textinfo='percent+label',
                    hovertemplate='<b>%{label}</b><br>Views: %{value:,}<br>Persentase: %{percent}<extra></extra>'
                )
                st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown("---")

def display_analysis_results(result, chart_key=None):
    """Display analysis results in a formatted way"""
    if not result.get('success', False):
        st.error(f"❌ Analisis gagal: {result.get('error', 'Unknown error')}")
        return
    
    stats = result.get('stats', {})
    
    if stats.get('error'):
        st.error(f"❌ Error dalam scraping: {stats['error']}")
        return
    
    # Display basic info
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Informasi Dasar")
        platform_icons = {'youtube': '🎥', 'tiktok': '🎵', 'facebook': '👥'}
        platform = stats.get('platform', 'unknown')
        icon = platform_icons.get(platform, '📱')
        
        st.markdown(f"**Platform:** {icon} {platform.title()}")
        if stats.get('title'):
            st.markdown(f"**Judul:** {stats['title'][:100]}..." if len(stats.get('title', '')) > 100 else f"**Judul:** {stats['title']}")
        if stats.get('author'):
            st.markdown(f"**Author:** {stats['author']}")
        if stats.get('upload_date'):
            st.markdown(f"**Tanggal Upload:** {stats['upload_date']}")
    
    with col2:
        st.subheader("📊 Statistik")
        
        # Create metrics - always show all 4 metrics, use 0 if data not available
        metrics_data = [
            ('Views', stats.get('views', 0), '👁️'),
            ('Likes', stats.get('likes', 0), '👍'),
            ('Shares', stats.get('shares', 0), '🔄'),
            ('Comments', stats.get('comments', 0), '💬')
        ]
        
        # Display metrics in a grid
        for i in range(0, len(metrics_data), 2):
            metric_cols = st.columns(2)
            for j, (label, value, icon) in enumerate(metrics_data[i:i+2]):
                with metric_cols[j]:
                    # Ensure value is numeric, default to 0 if not
                    if value is None or (isinstance(value, str) and not value.isdigit()):
                        value = 0
                    formatted_value = f"{value:,}" if isinstance(value, (int, float)) else "0"
                    st.metric(label=f"{icon} {label}", value=formatted_value)
    
    # Display analysis if available
    if 'analysis' in result and result['analysis']:
        st.subheader("🤖 Analisis AI")
        st.markdown(result['analysis'])
    
    # Create visualization - always show all 4 metrics
    numeric_data = {
        'views': stats.get('views', 0),
        'likes': stats.get('likes', 0), 
        'shares': stats.get('shares', 0),
        'comments': stats.get('comments', 0)
    }
    
    # Ensure all values are numeric
    for key, value in numeric_data.items():
        if value is None or (isinstance(value, str) and not value.isdigit()):
            numeric_data[key] = 0
    
    if any(v > 0 for v in numeric_data.values()):
        st.subheader("📈 Visualisasi")
        
        # Create bar chart
        df_viz = pd.DataFrame(list(numeric_data.items()), columns=['Metric', 'Value'])
        fig = px.bar(df_viz, x='Metric', y='Value', 
                    title=f"Statistik {platform.title()}",
                    color='Value',
                    color_continuous_scale='viridis')
        fig.update_layout(showlegend=False)
        # Generate unique key for chart if not provided
        if chart_key is None:
            chart_key = f"chart_{hash(str(result.get('url', '')) + str(result.get('timestamp', '')))}"
        st.plotly_chart(fig, use_container_width=True, key=chart_key)

def main():
    """Main application function"""
    initialize_session_state()
    display_header()
    display_sidebar()
    
    # Initialize services
    if not setup_services():
        st.stop()
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["🔍 Analisis Tunggal", "📊 Analisis Multiple", "📈 Riwayat"])
    
    with tab1:
        st.subheader("Analisis URL Tunggal")
        
        # URL input
        url_input = st.text_input(
            "Masukkan URL postingan media sosial:",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Mendukung URL dari YouTube, TikTok, dan Facebook"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            analyze_button = st.button("🚀 Analisis", type="primary")
        
        if analyze_button and url_input:
            # Validate URL
            is_valid, platform = validate_and_display_url_info(url_input)
            
            if is_valid:
                with st.spinner(f"Menganalisis {platform} URL... Mohon tunggu..."):
                    try:
                        result = st.session_state.crew_service.analyze_single_url(url_input)
                        
                        # Add timestamp
                        result['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Store in session state
                        st.session_state.analysis_results.append(result)
                        
                        # Display total views if there are multiple results
                        if len(st.session_state.analysis_results) > 1:
                            st.subheader("🌟 Total Views Semua Analisis")
                            total_views, platform_views = calculate_total_views(st.session_state.analysis_results)
                            if total_views > 0:
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric(
                                        label="📊 Total Views Keseluruhan",
                                        value=f"{total_views:,}",
                                        help="Total views dari semua analisis yang pernah dilakukan"
                                    )
                                with col2:
                                    current_views = result.get('stats', {}).get('views', 0)
                                    if current_views and isinstance(current_views, (int, float)):
                                        contribution = (current_views / total_views * 100) if total_views > 0 else 0
                                        st.metric(
                                            label="📈 Kontribusi Analisis Ini",
                                            value=f"{current_views:,}",
                                            delta=f"{contribution:.1f}% dari total",
                                            help="Views dari analisis saat ini"
                                        )
                                st.markdown("---")
                        
                        # Display results
                        display_analysis_results(result)
                        
                    except Exception as e:
                        st.error(f"Error during analysis: {str(e)}")
        
        elif analyze_button and not url_input:
            st.warning("⚠️ Silakan masukkan URL terlebih dahulu")
    
    with tab2:
        st.subheader("Analisis Multiple URL")
        
        # Multiple URL input
        st.markdown("Masukkan beberapa URL (satu per baris):")
        urls_text = st.text_area(
            "URLs:",
            height=150,
            placeholder="https://www.youtube.com/watch?v=...\nhttps://www.tiktok.com/@user/video/...\nhttps://www.facebook.com/watch/?v=..."
        )
        
        if st.button("🚀 Analisis Semua", type="primary"):
            if urls_text.strip():
                urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
                
                if urls:
                    with st.spinner(f"Menganalisis {len(urls)} URL... Mohon tunggu..."):
                        try:
                            results = st.session_state.crew_service.analyze_multiple_urls(urls)
                            
                            # Display total views summary first
                            display_total_views_summary(results['individual_results'])
                            
                            # Display individual results
                            st.subheader("📊 Hasil Individual")
                            for i, result in enumerate(results['individual_results'], 1):
                                with st.expander(f"URL {i}: {result['url'][:50]}..."):
                                    display_analysis_results(result, chart_key=f"multi_chart_{i}")
                            
                            # Display comparative analysis
                            if 'comparative_analysis' in results:
                                st.subheader("🔄 Analisis Perbandingan")
                                st.markdown(results['comparative_analysis'])
                            
                            # Summary
                            st.subheader("📋 Ringkasan")
                            st.info(f"Total URL dianalisis: {results['total_analyzed']} | "
                                   f"Berhasil: {results['successful_analyses']} | "
                                   f"Gagal: {results['total_analyzed'] - results['successful_analyses']}")
                            
                        except Exception as e:
                            st.error(f"Error during multiple analysis: {str(e)}")
                else:
                    st.warning("⚠️ Tidak ada URL valid yang ditemukan")
            else:
                st.warning("⚠️ Silakan masukkan URL terlebih dahulu")
    
    with tab3:
        st.subheader("📈 Riwayat Analisis")
        
        if st.session_state.analysis_results:
            # Display total views summary from all history
            display_total_views_summary(st.session_state.analysis_results)
            
            # Display summary statistics
            total_analyses = len(st.session_state.analysis_results)
            successful_analyses = len([r for r in st.session_state.analysis_results if r.get('success', False)])
            
            st.subheader("📈 Statistik Riwayat")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Analisis", total_analyses)
            with col2:
                st.metric("Berhasil", successful_analyses)
            with col3:
                st.metric("Tingkat Keberhasilan", f"{(successful_analyses/total_analyses*100):.1f}%")
            
            st.markdown("---")
            
            # Display history
            for i, result in enumerate(reversed(st.session_state.analysis_results), 1):
                with st.expander(f"Analisis #{len(st.session_state.analysis_results)-i+1} - {result.get('timestamp', 'Unknown time')}"):
                    display_analysis_results(result, chart_key=f"history_chart_{i}")
            
            # Clear history button
            if st.button("🗑️ Hapus Riwayat"):
                st.session_state.analysis_results = []
                st.success("✅ Riwayat berhasil dihapus")
                st.rerun()
        else:
            st.info("📝 Belum ada riwayat analisis. Mulai dengan menganalisis URL di tab 'Analisis Tunggal'.")

if __name__ == "__main__":
    main()