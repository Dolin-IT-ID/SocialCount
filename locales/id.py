# Indonesian language configuration
# Konfigurasi bahasa Indonesia

LANGUAGE_CONFIG = {
    "language_name": "Bahasa Indonesia",
    "language_code": "id",
    "flag": "🇮🇩",
    
    # Header and Title
    "app_title": "🎬 Ekstraksi Detail Video Multi-Platform",
    "app_subtitle": "Analisis mendalam video dari YouTube, TikTok, dan Facebook dengan teknologi AI",
    
    # Navigation Tabs
    "tab_extract": "🎬 Ekstrak Video",
    "tab_batch": "📊 Analisis Batch",
    "tab_history": "📚 Riwayat",
    "tab_database": "🗄️ Database & Ekspor",
    
    # Main Form Labels
    "creator_name": "👤 Nama Pembuat Video:",
    "creator_placeholder": "Masukkan nama pembuat/kreator video",
    "creator_help": "Nama pembuat atau kreator video",
    
    "calculation_date": "📅 Tanggal Penghitungan:",
    "calculation_time": "⏰ Jam Penghitungan:",
    "date_help": "Tanggal saat melakukan penghitungan/analisis video",
    "time_help": "Jam saat melakukan penghitungan/analisis video",
    
    "video_url": "🔗 Masukkan URL Video:",
    "url_placeholder": "https://www.youtube.com/watch?v=... atau https://www.tiktok.com/@user/video/... atau https://www.facebook.com/watch/?v=...",
    "url_help": "Mendukung URL dari YouTube, TikTok, dan Facebook",
    
    "account_name": "📱 Nama Akun:",
    "account_placeholder": "@username",
    "account_help": "Nama akun/username dari platform",
    
    # Buttons
    "extract_button": "🚀 Ekstrak Detail",
    "vlm_analysis": "🤖 Analisis VLM",
    "save_data": "💾 Simpan Data",
    "add_to_database": "💾 Tambahkan ke Database",
    "extract_all": "🚀 Ekstrak Semua",
    "load_data": "📊 Muat Data",
    
    # Messages
    "url_required": "⚠️ Silakan masukkan URL video terlebih dahulu",
    "invalid_platform": "Platform tidak dapat dideteksi. Pastikan URL dari YouTube, TikTok, atau Facebook",
    "empty_url": "URL tidak boleh kosong",
    "extraction_success": "✅ Ekstraksi berhasil!",
    "extraction_failed": "❌ Ekstraksi gagal",
    "save_success": "✅ Data berhasil disimpan ke database MongoDB!",
    "save_failed": "❌ Gagal menyimpan data ke database",
    "fill_required_fields": "⚠️ Harap isi Nama Pembuat Video dan Nama Akun sebelum menyimpan ke database",
    
    # Sidebar
    "sidebar_title": "🎯 Platform yang Didukung",
    "sidebar_vlm": "🧠 Fitur VLM",
    "sidebar_usage": "📋 Cara Penggunaan",
    
    # Platform Features
    "youtube_features": [
        "📊 Views, likes, comments",
        "📅 Tanggal upload",
        "⏱️ Durasi video",
        "👤 Channel info",
        "📝 Deskripsi lengkap"
    ],
    "tiktok_features": [
        "❤️ Likes dan shares",
        "💬 Jumlah komentar",
        "👀 View count",
        "🎵 Info musik",
        "#️⃣ Hashtags"
    ],
    "facebook_features": [
        "👍 Reactions",
        "💬 Comments",
        "🔄 Shares",
        "📊 Engagement metrics",
        "📅 Post date"
    ],
    
    # Tab content
    'tab_extract': '🎬 Ekstraksi Detail Video Tunggal',
    'creator_name': '👤 Nama Pembuat Video:',
    'creator_placeholder': 'Masukkan nama pembuat/kreator video',
    'creator_help': 'Nama pembuat atau kreator video',
    'calculation_date': '📅 Tanggal Penghitungan:',
    'date_help': 'Tanggal saat melakukan penghitungan/analisis video',
    'calculation_time': '⏰ Jam Penghitungan:',
    'time_help': 'Jam saat melakukan penghitungan/analisis video',
    'url_input': '🔗 Masukkan URL Video:',
    'url_placeholder': 'https://www.youtube.com/watch?v=... atau https://www.tiktok.com/@user/video/... atau https://www.facebook.com/watch/?v=...',
    'url_help': 'Mendukung URL dari YouTube, TikTok, dan Facebook',
    'extract_button': '🚀 Ekstrak Detail',
    
    # Batch Analysis
    'tab_batch': '📊 Analisis Batch Multiple URL',
    'batch_info': 'Fitur ini memungkinkan Anda menganalisis beberapa video sekaligus',
    'batch_urls': '📝 Masukkan URL (satu per baris):',
    'batch_placeholder': 'https://www.youtube.com/watch?v=...\nhttps://www.tiktok.com/@user/video/...\nhttps://www.facebook.com/watch/?v=...',
    'batch_extract': '🚀 Ekstrak Semua',
    'batch_vlm': '🤖 Analisis VLM Batch',
    
    # History Tab
    'history_empty': '📝 Belum ada riwayat ekstraksi. Mulai dengan mengekstrak video pertama Anda!',
    'history_title': '📚 Riwayat Ekstraksi',
    'video_count': 'video',
    'total_videos': '📊 Total Video',
    'total_views': '👀 Total Views',
    'total_likes': '👍 Total Likes',
    'title_label': 'Judul',
    'platform_label': 'Platform',
    'clear_history': '🗑️ Hapus Riwayat',
    
    # Database Tab
    'tab_database': '🗄️ Database & Ekspor Data',
    'check_db_connection': '🔄 Cek Koneksi Database',
    'checking_mongodb': 'Mengecek koneksi MongoDB...',
    'mongodb_success': '✅ Koneksi MongoDB berhasil!',
    'mongodb_failed': '❌ Gagal terhubung ke MongoDB',
    'total_db_videos': '📊 Total video dalam database',
    'tips_label': 'Tips',
    'mongodb_tips': 'Pastikan MongoDB berjalan di sistem Anda',
    'filter_data': '🔍 Filter Data',
    'start_date': '📅 Tanggal Mulai:',
    'start_date_help': 'Pilih tanggal mulai untuk filter data',
    'end_date': '📅 Tanggal Akhir:',
    'end_date_help': 'Pilih tanggal akhir untuk filter data',
    'load_data': '📊 Muat Data',
    'loading_data': '📥 Memuat data dari database...',
    'data_summary': '📈 Ringkasan Data',
    'data_preview': '👀 Preview Data',
    'show_data_table': '📋 Tampilkan Data dalam Tabel',
    'select_columns': 'Pilih kolom untuk ditampilkan:',
    'select_min_column': '⚠️ Pilih minimal satu kolom untuk ditampilkan',
    'no_data_display': '📭 Tidak ada data untuk ditampilkan',
    'export_data': '📥 Ekspor Data',
    'export_format': 'Format Ekspor',
    'select_export_format': 'Pilih format ekspor:',
    'export_format_help': 'Excel Detail: Data lengkap per video\nExcel Ringkasan: Format statistik sesuai referensi Vietnam/Chinese',
    'format_preview': 'Preview Format',
    'summary_format_info': '📊 Format ringkasan statistik per kreator dengan header Vietnam/Chinese sesuai file referensi',
    'detail_format_info': '📋 Format detail lengkap per video dengan header Indonesia',
    'csv_format_info': '📄 Format CSV standar untuk data mentah',
    'export_failed': '❌ Gagal membuat file ekspor',
    'no_data_range': '📭 Tidak ada data dalam rentang tanggal yang dipilih',
    'click_load_data': '👆 Klik \'Muat Data\' untuk menampilkan data dari database',
    
    # Status Messages
    'vlm_active': '✅ VLM: Aktif',
    'ai_ready': '🧠 Siap untuk analisis AI',
    'vlm_inactive': '❌ VLM: Tidak aktif',
    'ai_unavailable': '⚠️ Analisis AI tidak tersedia',
    'stats_unavailable': 'Data statistik tidak tersedia',
    'history_cleared': '✅ Riwayat berhasil dihapus!',
    'extraction_success': '🎉 Ekstraksi berhasil!',
    'fill_creator_warning': '⚠️ Harap isi Nama Pembuat Video dan Nama Akun sebelum menyimpan ke database',
    'data_saved_success': '✅ Data berhasil disimpan ke database MongoDB!',
    'data_save_failed': '❌ Gagal menyimpan data ke database',
    'enter_url_warning': '⚠️ Silakan masukkan URL video terlebih dahulu',
    'no_valid_urls': '⚠️ Tidak ada URL valid yang ditemukan',
    'enter_urls_first': '⚠️ Silakan masukkan URL terlebih dahulu',
    
    # VLM Features
    "vlm_features": [
        "📊 Analisis engagement",
        "📈 Prediksi performa",
        "🎯 Rekomendasi konten",
        "📝 Ringkasan otomatis",
        "🔍 Insight mendalam"
    ],
    
    # Usage Instructions
    "usage_steps": [
        "📝 Masukkan URL video",
        "🚀 Klik tombol 'Ekstrak Detail'",
        "⏳ Tunggu proses ekstraksi",
        "📊 Lihat hasil dan analisis",
        "🤖 Dapatkan insight AI (jika VLM aktif)",
        "💾 Simpan hasil jika diperlukan"
    ],
    
    # Batch Analysis
    "batch_title": "📊 Analisis Batch Multiple URL",
    "batch_info": "💡 Fitur ini memungkinkan Anda menganalisis beberapa video sekaligus",
    "batch_input": "📝 Masukkan URL (satu per baris):",
    "batch_placeholder": "https://www.youtube.com/watch?v=...\nhttps://www.tiktok.com/@user/video/...\nhttps://www.facebook.com/watch/?v=...",
    
    # Database & Export
    "database_title": "🗄️ Database & Ekspor Data",
    "filter_data": "🔍 Filter Data",
    "start_date": "📅 Tanggal Mulai:",
    "end_date": "📅 Tanggal Akhir:",
    "start_date_help": "Pilih tanggal mulai untuk filter data",
    "end_date_help": "Pilih tanggal akhir untuk filter data",
    
    "data_summary": "📈 Ringkasan Data",
    "data_preview": "👀 Preview Data",
    "show_table": "📋 Tampilkan Data dalam Tabel",
    "select_columns": "Pilih kolom untuk ditampilkan:",
    "min_one_column": "⚠️ Pilih minimal satu kolom untuk ditampilkan",
    "no_data": "📭 Tidak ada data untuk ditampilkan",
    
    "export_data": "📥 Ekspor Data",
    "export_format": "**Format Ekspor:**",
    "export_preview": "**Preview Format:**",
    "export_action": "**Aksi Ekspor:**",
    
    "format_csv": "CSV",
    "format_excel_detail": "Excel Detail",
    "format_excel_summary": "Excel Ringkasan",
    
    "format_help": "Excel Detail: Data lengkap per video\nExcel Ringkasan: Format statistik sesuai referensi Vietnam/Chinese",
    
    "preview_summary": "📊 Format ringkasan statistik per kreator dengan header Vietnam/Chinese sesuai file referensi",
    "preview_detail": "📋 Format detail lengkap per video dengan header Indonesia",
    "preview_csv": "📄 Format CSV standar untuk data mentah",
    
    "export_button": "📥 Ekspor ke {}",
    "preparing_file": "📦 Menyiapkan file {}...",
    "file_ready": "✅ File {} siap untuk diunduh!",
    "export_failed": "❌ Gagal membuat file ekspor",
    "export_error": "❌ Error saat ekspor: {}",
    
    "platform_stats": "📊 Statistik Platform",
    
    # Loading and Status Messages
    "loading_data": "📥 Memuat data dari database...",
    "saving_data": "💾 Menyimpan ke database...",
    "extracting": "🔄 Mengekstrak data video...",
    "analyzing": "🤖 Menganalisis dengan VLM...",
    
    # Error Messages
    "vlm_unavailable": "VLM tidak tersedia untuk analisis",
    "connection_error": "❌ Error koneksi",
    "processing_error": "❌ Error saat memproses",
    
    # Data Fields
    "video_title": "Judul Video",
    "video_description": "Deskripsi",
    "views": "Views",
    "likes": "Likes",
    "comments": "Comments",
    "shares": "Shares",
    "duration": "Durasi",
    "upload_date": "Tanggal Upload",
    "platform": "Platform",
    "created_at": "Dibuat Pada",
    "updated_at": "Diperbarui Pada",
    
    # Download
    "download_data": "💾 Download Data",
    "download_json": "📥 Download Data JSON",
    
    # Language Switcher
    "language_selector": "🌐 Bahasa / Language",
    "select_language": "Pilih Bahasa",
    
    # Status and notification messages
    'export_format_excel_detail': 'File Excel dengan detail lengkap setiap video',
    'export_format_csv': 'File CSV yang dapat dibuka dengan Excel atau aplikasi spreadsheet lainnya',
    'no_data_in_range': 'Tidak ada data dalam rentang tanggal yang dipilih',
    'load_data_first': 'Silakan muat data terlebih dahulu',
    'vlm_status_active': 'VLM Aktif',
    'vlm_status_inactive': 'VLM Tidak Aktif',
    'statistics_unavailable': 'Statistik tidak tersedia',
    'warning_missing_creator': 'Peringatan: Nama pembuat video kosong. Silakan isi sebelum menyimpan ke database.',
    'warning_missing_account': 'Peringatan: Nama akun kosong. Silakan isi sebelum menyimpan ke database.',
    'batch_no_valid_urls': 'Tidak ada URL yang valid ditemukan',
    'batch_enter_urls': 'Silakan masukkan URL terlebih dahulu',
    
    # Export headers
    'export_id': 'ID',
    'export_creator_name': 'Nama Pembuat Video',
    'export_account_name': 'Nama Akun',
    'export_video_url': 'URL Video',
    'export_platform': 'Platform',
    'export_video_title': 'Judul Video',
    'export_description': 'Deskripsi',
    'export_views': 'Views',
    'export_likes': 'Likes',
    'export_comments': 'Comments',
    'export_shares': 'Shares',
    'export_duration': 'Duration',
    'export_upload_date': 'Upload Date',
    'export_calculation_time': 'Waktu Penghitungan',
    'export_created_at': 'Created At',
    'export_updated_at': 'Updated At',
    
    # Summary export headers
    'summary_creator_name': 'Nama Pembuat',
    'summary_fb_post': 'FB Post',
    'summary_fb_view': 'FB View',
    'summary_fb_like': 'FB Like',
    'summary_fb_comment': 'FB Comment',
    'summary_fb_share': 'FB Share',
    'summary_zalo_post': 'Zalo Post',
    'summary_zalo_view': 'Zalo View',
    'summary_zalo_like': 'Zalo Like',
    'summary_zalo_comment': 'Zalo Comment',
    'summary_zalo_share': 'Zalo Share',
    'summary_yt_post': 'YT Post',
    'summary_yt_view': 'YT View',
    'summary_yt_like': 'YT Like',
    'summary_yt_comment': 'YT Comment',
    'summary_yt_share': 'YT Share',
    'summary_total_post': 'Total Post',
    'summary_total_view': 'Total View',
    'summary_total_like': 'Total Like',
    'summary_total_comment': 'Total Comment',
    'summary_total_share': 'Total Share',
    
    # Summary export labels
    'summary_main_header': 'STATISTIK INTERAKSI MEDIA SOSIAL',
    'summary_export_date': 'Tanggal ekspor: {date}',
    'summary_date_label': 'Tanggal Pembuatan',
    'summary_time_label': 'Waktu',
    'summary_total': 'Total',
    'summary_post': 'Post',
    'summary_view': 'View',
    'summary_like': 'Like',
    'summary_comment': 'Comment',
    'summary_share': 'Share',
    
    # Export summary display
    'export_no_data': '📭 Tidak ada data untuk diekspor',
    'export_total_videos': 'Total Video',
    'export_platforms': 'Platform',
    'export_date_range': 'Rentang Tanggal',
    'export_days_format': '{days} hari',
    'export_available_platforms': 'Platform yang tersedia',
    'export_data_period': 'Periode data'
}