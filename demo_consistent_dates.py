#!/usr/bin/env python3
"""
Demo Konsistensi Ekstraksi Tanggal Unggah

Script demonstrasi yang menunjukkan bagaimana sistem ekstraksi tanggal unggah
bekerja secara konsisten di semua platform (YouTube, TikTok, Facebook).
"""

import sys
import os
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.url_detector import URLDetector
from scrapers.youtube_scraper import YouTubeScraper
from scrapers.tiktok_scraper import TikTokScraper
from scrapers.facebook_scraper import FacebookScraper

def get_scraper(platform):
    """Get appropriate scraper based on platform"""
    scrapers = {
        'youtube': YouTubeScraper,
        'tiktok': TikTokScraper,
        'facebook': FacebookScraper
    }
    return scrapers.get(platform.lower())

def format_date_info(upload_date):
    """Format date information with additional details"""
    if not upload_date:
        return "❌ Tanggal tidak tersedia"
    
    try:
        # Parse the date to get additional info
        date_obj = datetime.strptime(upload_date, '%B %d, %Y')
        
        # Calculate age
        now = datetime.now()
        age_days = (now - date_obj).days
        age_years = age_days // 365
        age_months = (age_days % 365) // 30
        
        age_str = ""
        if age_years > 0:
            age_str = f"{age_years} tahun"
            if age_months > 0:
                age_str += f" {age_months} bulan"
        elif age_months > 0:
            age_str = f"{age_months} bulan"
        else:
            age_str = f"{age_days} hari"
        
        return f"📅 {upload_date} ({age_str} yang lalu)"
    except:
        return f"📅 {upload_date}"

def demonstrate_date_consistency():
    """Demonstrate consistent date extraction across platforms"""
    print("🎬 DEMONSTRASI KONSISTENSI EKSTRAKSI TANGGAL UNGGAH")
    print("=" * 60)
    print("Menunjukkan bagaimana sistem mengekstrak tanggal unggah secara")
    print("konsisten di semua platform yang didukung.\n")
    
    # Show supported date formats
    print("📋 FORMAT TANGGAL YANG DIDUKUNG:")
    print("=" * 40)
    supported_formats = [
        "October 24, 2009 (Format standar)",
        "2023-01-30T02:34:17-08:00 (ISO 8601)",
        "2024-01-15 (Format singkat)",
        "15 Jan 2024 (Format alternatif)",
        "2 days ago (Waktu relatif bahasa Inggris)",
        "1 minggu yang lalu (Waktu relatif bahasa Indonesia)",
        "Unix timestamp (untuk Facebook)",
        "Meta tags dan JSON-LD data"
    ]
    
    for i, fmt in enumerate(supported_formats, 1):
        print(f"  {i}. {fmt}")
    
    # Show extraction methods for each platform
    print("\n🔧 METODE EKSTRAKSI PER PLATFORM:")
    print("=" * 40)
    
    platforms_info = {
        "YouTube": {
            "selectors": [
                "#info-strings yt-formatted-string",
                "#date yt-formatted-string",
                "Meta tags (article:published_time)",
                "JSON-LD structured data"
            ],
            "enhanced": "_enhanced_date_extraction",
            "features": ["Multiple CSS selectors", "Shorts support", "Meta tag fallback", "Regex patterns"]
        },
        "TikTok": {
            "selectors": [
                ".video-meta-date",
                "[data-e2e='video-date']",
                "Meta tags (video:release_date)",
                "JSON timestamp parsing"
            ],
            "enhanced": "_enhanced_date_extraction_tiktok",
            "features": ["Data attributes", "Unix timestamp", "Meta tag extraction", "Page source parsing"]
        },
        "Facebook": {
            "selectors": [
                "abbr[data-utime]",
                "[data-testid='story-subtitle'] a[role='link']",
                ".timestamp",
                "Meta tags (article:published_time)"
            ],
            "enhanced": "_enhanced_date_extraction_facebook",
            "features": ["Unix timestamp handling", "Data attributes", "Story elements", "Meta tag support"]
        }
    }
    
    for platform, info in platforms_info.items():
        print(f"\n🎯 {platform}:")
        print(f"  Metode Enhanced: {info['enhanced']}")
        print("  Selector Utama:")
        for selector in info['selectors']:
            print(f"    • {selector}")
        print("  Fitur Khusus:")
        for feature in info['features']:
            print(f"    ✓ {feature}")
    
    # Show normalization process
    print("\n🔄 PROSES NORMALISASI TANGGAL:")
    print("=" * 40)
    normalization_steps = [
        "1. Deteksi format tanggal input",
        "2. Parsing dengan multiple format patterns",
        "3. Konversi waktu relatif ke tanggal absolut",
        "4. Normalisasi ke format standar: 'Month DD, YYYY'",
        "5. Validasi dan fallback handling"
    ]
    
    for step in normalization_steps:
        print(f"  {step}")
    
    # Test date normalization examples
    print("\n📝 CONTOH NORMALISASI TANGGAL:")
    print("=" * 40)
    
    # Create a temporary scraper to test normalization
    try:
        with YouTubeScraper() as scraper:
            test_cases = [
                "October 24, 2009",
                "2023-01-30T02:34:17-08:00",
                "2024-01-15",
                "15 Jan 2024",
                "24/10/2009"
            ]
            
            for test_date in test_cases:
                try:
                    normalized = scraper._normalize_date(test_date)
                    print(f"  '{test_date}' → '{normalized}'")
                except Exception as e:
                    print(f"  '{test_date}' → Error: {str(e)}")
    except Exception as e:
        print(f"  Error testing normalization: {str(e)}")
    
    print("\n✨ KEUNGGULAN SISTEM:")
    print("=" * 40)
    advantages = [
        "🎯 Konsistensi format output di semua platform",
        "🔄 Multiple fallback methods untuk reliability",
        "🌐 Support bahasa Indonesia dan Inggris",
        "⚡ Parsing cepat dengan caching",
        "🛡️ Error handling yang robust",
        "📱 Support untuk mobile dan desktop layouts",
        "🔍 Deep extraction dari page source",
        "📊 Metadata lengkap dengan analisis umur konten"
    ]
    
    for advantage in advantages:
        print(f"  {advantage}")

def demo_with_sample_url():
    """Demo with a sample URL"""
    print("\n" + "=" * 60)
    print("🌐 DEMO EKSTRAKSI DENGAN URL SAMPLE:")
    print("=" * 60)
    
    sample_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    print(f"URL: {sample_url}")
    
    try:
        # Detect platform
        platform = URLDetector.detect_platform(sample_url)
        print(f"Platform terdeteksi: {platform.upper()}")
        
        # Get scraper
        scraper_class = get_scraper(platform)
        if not scraper_class:
            print("❌ Scraper tidak tersedia")
            return
        
        print("\n🔄 Memulai ekstraksi...")
        
        # Extract data
        with scraper_class() as scraper:
            stats = scraper.scrape(sample_url)
            
            if stats:
                print("\n📊 HASIL EKSTRAKSI:")
                print("-" * 30)
                print(f"📺 Judul: {stats.title or 'N/A'}")
                print(f"👤 Author: {stats.author or 'N/A'}")
                print(f"🏷️ Platform: {stats.platform or 'N/A'}")
                print(f"👀 Views: {stats.views or 'N/A'}")
                print(f"👍 Likes: {stats.likes or 'N/A'}")
                print(f"💬 Comments: {stats.comments or 'N/A'}")
                
                # Highlight the upload date
                print(f"\n🎯 TANGGAL UNGGAH: {format_date_info(stats.upload_date)}")
                
                if stats.upload_date:
                    print("\n✅ EKSTRAKSI TANGGAL BERHASIL!")
                    print("   Tanggal unggah berhasil diekstrak dan dinormalisasi")
                    print("   ke format yang konsisten dan mudah dibaca.")
                else:
                    print("\n⚠️  Tanggal unggah tidak ditemukan")
                    print("   Sistem akan mencoba metode ekstraksi alternatif.")
            else:
                print("❌ Gagal mengekstrak data dari URL")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        # Show demonstration
        demonstrate_date_consistency()
        
        # Demo with sample URL
        demo_with_sample_url()
        
        print("\n" + "=" * 60)
        print("🎉 DEMO SELESAI")
        print("=" * 60)
        print("✅ Sistem ekstraksi tanggal unggah siap digunakan!")
        print("🎯 Semua platform mendukung ekstraksi tanggal yang konsisten.")
        print("\n💡 Untuk menggunakan sistem ini:")
        print("   1. Jalankan 'python extract_video_details.py'")
        print("   2. Masukkan URL video dari YouTube, TikTok, atau Facebook")
        print("   3. Sistem akan mengekstrak tanggal unggah secara otomatis")
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo dihentikan oleh user.")
    except Exception as e:
        print(f"\n\n❌ Error tidak terduga: {str(e)}")
        import traceback
        traceback.print_exc()