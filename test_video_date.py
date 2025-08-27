#!/usr/bin/env python3
"""
Script untuk menguji ekstraksi tanggal unggah video
"""

import sys
import os
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.youtube_scraper import YouTubeScraper
from scrapers.tiktok_scraper import TikTokScraper
from scrapers.facebook_scraper import FacebookScraper

def detect_platform(url):
    """Detect platform from URL"""
    if 'youtube.com' in url or 'youtu.be' in url:
        return 'youtube'
    elif 'tiktok.com' in url:
        return 'tiktok'
    elif 'facebook.com' in url or 'fb.watch' in url:
        return 'facebook'
    else:
        return 'unknown'

def format_date_info(upload_date):
    """Format upload date information"""
    if not upload_date:
        return "❌ Tidak ditemukan"
    
    # Check if it's a valid formatted date
    try:
        # Try to parse common formats
        for fmt in ['%B %d, %Y', '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']:
            try:
                parsed = datetime.strptime(upload_date, fmt)
                return f"✅ {upload_date} (Valid)"
            except ValueError:
                continue
        
        # If no format matches but we have a date string
        return f"⚠️ {upload_date} (Format tidak standar)"
    except:
        return f"❌ {upload_date} (Error parsing)"

def test_video_extraction(url):
    """Test video metadata extraction"""
    print(f"\n🔍 Menguji URL: {url}")
    print("=" * 60)
    
    platform = detect_platform(url)
    print(f"Platform: {platform.upper()}")
    
    # Select appropriate scraper
    if platform == 'youtube':
        scraper = YouTubeScraper()
    elif platform == 'tiktok':
        scraper = TikTokScraper()
    elif platform == 'facebook':
        scraper = FacebookScraper()
    else:
        print("❌ Platform tidak didukung")
        return None
    
    try:
        print("\n⏳ Mengekstrak metadata...")
        with scraper:
            stats = scraper.scrape(url)
        
        if stats:
            print("\n📹 INFORMASI VIDEO:")
            print(f"   Judul: {stats.title or 'Tidak ditemukan'}")
            print(f"   Author: {stats.author or 'Tidak ditemukan'}")
            print(f"   Platform: {stats.platform or 'Tidak ditemukan'}")
            
            print("\n📊 STATISTIK:")
            print(f"   Views: {stats.views or 'Tidak ditemukan'}")
            print(f"   Likes: {stats.likes or 'Tidak ditemukan'}")
            print(f"   Comments: {stats.comments or 'Tidak ditemukan'}")
            print(f"   Shares: {stats.shares or 'Tidak ditemukan'}")
            
            print("\n📅 TANGGAL UNGGAH:")
            date_info = format_date_info(stats.upload_date)
            print(f"   Status: {date_info}")
            if stats.upload_date:
                print(f"   Raw Data: {stats.upload_date}")
            
            # Calculate completeness score
            fields = [stats.title, stats.author, stats.views, stats.likes, 
                     stats.comments, stats.shares, stats.upload_date]
            available_fields = sum(1 for field in fields if field is not None)
            completeness = (available_fields / len(fields)) * 100
            
            print(f"\n📋 SKOR KELENGKAPAN: {available_fields}/{len(fields)} ({completeness:.1f}%)")
            
            if stats.error:
                print(f"\n⚠️ ERROR: {stats.error}")
            
            return stats
        else:
            print("❌ Gagal mengekstrak metadata")
            return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def main():
    """Main function"""
    print("🎬 TES EKSTRAKSI TANGGAL UNGGAH VIDEO")
    print("=" * 60)
    
    # Test URLs - you can modify these
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Example YouTube URL
        # Add more URLs here for testing
    ]
    
    results = []
    
    # Test predefined URLs
    for url in test_urls:
        result = test_video_extraction(url)
        if result:
            results.append(result)
    
    # Interactive testing
    while True:
        print("\n" + "=" * 60)
        url = input("\nMasukkan URL video (atau 'quit' untuk keluar): ").strip()
        
        if url.lower() in ['quit', 'exit', 'q']:
            break
        
        if not url:
            continue
            
        result = test_video_extraction(url)
        if result:
            results.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 RINGKASAN TES:")
    print(f"Total video yang diuji: {len(results)}")
    
    if results:
        successful_dates = sum(1 for r in results if r.upload_date)
        print(f"Tanggal berhasil diekstrak: {successful_dates}/{len(results)} ({(successful_dates/len(results)*100):.1f}%)")
        
        # Show date extraction results
        print("\n📅 HASIL EKSTRAKSI TANGGAL:")
        for i, result in enumerate(results, 1):
            title = result.title[:50] + "..." if result.title and len(result.title) > 50 else result.title
            date_status = format_date_info(result.upload_date)
            print(f"   {i}. {title or 'Tanpa judul'}: {date_status}")

if __name__ == "__main__":
    main()