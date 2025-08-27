#!/usr/bin/env python3
"""
Script untuk mengekstrak tanggal unggah dan detail lengkap video dari berbagai platform media sosial.
Mendukung YouTube, TikTok, dan Facebook dengan akurasi tinggi.

Author: Social Media Scraper
Date: 2024
"""

import sys
import json
from datetime import datetime
from typing import Optional, Dict, Any

from utils.url_detector import URLDetector
from scrapers.youtube_scraper import YouTubeScraper
from scrapers.tiktok_scraper import TikTokScraper
from scrapers.facebook_scraper import FacebookScraper

def get_scraper(platform: str):
    """Mendapatkan scraper yang sesuai berdasarkan platform"""
    scrapers = {
        'youtube': YouTubeScraper,
        'tiktok': TikTokScraper,
        'facebook': FacebookScraper
    }
    
    scraper_class = scrapers.get(platform.lower())
    if not scraper_class:
        raise ValueError(f"Platform '{platform}' tidak didukung. Platform yang didukung: {list(scrapers.keys())}")
    
    return scraper_class(headless=True, timeout=30)

def format_number(num: Optional[int]) -> str:
    """Format angka dengan pemisah ribuan"""
    if num is None:
        return "Tidak ditemukan"
    
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return f"{num:,}"

def validate_upload_date(date_str: Optional[str]) -> Dict[str, Any]:
    """Validasi dan analisis tanggal unggah"""
    if not date_str:
        return {
            'status': 'tidak_ditemukan',
            'message': 'Tanggal unggah tidak ditemukan',
            'is_valid': False,
            'formatted_date': None,
            'raw_date': None
        }
    
    # Coba parse berbagai format tanggal
    date_formats = [
        '%B %d, %Y',  # October 24, 2009
        '%d %B %Y',   # 24 October 2009
        '%Y-%m-%d',   # 2009-10-24
        '%d/%m/%Y',   # 24/10/2009
        '%m/%d/%Y',   # 10/24/2009
    ]
    
    parsed_date = None
    for fmt in date_formats:
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            break
        except ValueError:
            continue
    
    if parsed_date:
        # Hitung umur video
        now = datetime.now()
        age_days = (now - parsed_date).days
        age_years = age_days / 365.25
        
        return {
            'status': 'valid',
            'message': f'Tanggal valid - video berumur {age_days:,} hari ({age_years:.1f} tahun)',
            'is_valid': True,
            'formatted_date': parsed_date.strftime('%d %B %Y'),
            'raw_date': date_str,
            'age_days': age_days,
            'age_years': round(age_years, 1)
        }
    else:
        return {
            'status': 'format_tidak_dikenal',
            'message': f'Format tanggal tidak dikenal: {date_str}',
            'is_valid': False,
            'formatted_date': None,
            'raw_date': date_str
        }

def calculate_completeness_score(stats) -> Dict[str, Any]:
    """Hitung skor kelengkapan metadata"""
    fields = ['title', 'author', 'views', 'likes', 'comments', 'shares', 'upload_date']
    found_fields = []
    missing_fields = []
    
    for field in fields:
        value = getattr(stats, field, None)
        if value is not None and str(value).strip() != "":
            found_fields.append(field)
        else:
            missing_fields.append(field)
    
    score = len(found_fields) / len(fields) * 100
    
    return {
        'score': round(score, 1),
        'found_count': len(found_fields),
        'total_count': len(fields),
        'found_fields': found_fields,
        'missing_fields': missing_fields
    }

def extract_video_details(url: str, save_to_file: bool = False) -> Dict[str, Any]:
    """Ekstrak detail lengkap video dari URL"""
    print(f"\n🔍 Menganalisis URL: {url}")
    print("=" * 80)
    
    # Deteksi platform
    platform = URLDetector.detect_platform(url)
    if not platform:
        error_msg = "Platform tidak dapat dideteksi dari URL"
        print(f"❌ Error: {error_msg}")
        return {'error': error_msg, 'url': url}
    
    print(f"📱 Platform: {platform.upper()}")
    
    try:
        # Inisialisasi scraper
        scraper = get_scraper(platform)
        
        print("\n⏳ Mengekstrak metadata video...")
        with scraper:
            stats = scraper.scrape(url)
        
        if not stats:
            error_msg = "Gagal mengekstrak data dari video"
            print(f"❌ Error: {error_msg}")
            return {'error': error_msg, 'url': url, 'platform': platform}
        
        # Analisis tanggal unggah
        date_analysis = validate_upload_date(stats.upload_date)
        
        # Hitung skor kelengkapan
        completeness = calculate_completeness_score(stats)
        
        # Tampilkan hasil
        print("\n" + "=" * 80)
        print("📹 DETAIL VIDEO LENGKAP")
        print("=" * 80)
        
        print(f"\n📝 INFORMASI DASAR:")
        print(f"   🎬 Judul: {stats.title or 'Tidak ditemukan'}")
        print(f"   👤 Author: {stats.author or 'Tidak ditemukan'}")
        print(f"   🌐 Platform: {platform.upper()}")
        print(f"   🔗 URL: {url}")
        
        print(f"\n📊 STATISTIK ENGAGEMENT:")
        print(f"   👀 Views: {format_number(stats.views)}")
        print(f"   👍 Likes: {format_number(stats.likes)}")
        print(f"   💬 Comments: {format_number(stats.comments)}")
        print(f"   📤 Shares: {format_number(stats.shares)}")
        
        print(f"\n📅 INFORMASI TANGGAL UNGGAH:")
        if date_analysis['is_valid']:
            print(f"   ✅ Status: VALID")
            print(f"   📆 Tanggal: {date_analysis['formatted_date']}")
            print(f"   ⏰ Umur Video: {date_analysis['age_days']:,} hari ({date_analysis['age_years']} tahun)")
            print(f"   📋 Data Mentah: {date_analysis['raw_date']}")
        else:
            print(f"   ❌ Status: {date_analysis['status'].upper()}")
            print(f"   📝 Pesan: {date_analysis['message']}")
            if date_analysis['raw_date']:
                print(f"   📋 Data Mentah: {date_analysis['raw_date']}")
        
        print(f"\n📈 SKOR KELENGKAPAN METADATA:")
        print(f"   🎯 Skor: {completeness['found_count']}/{completeness['total_count']} ({completeness['score']}%)")
        print(f"   ✅ Ditemukan: {', '.join(completeness['found_fields'])}")
        if completeness['missing_fields']:
            print(f"   ❌ Tidak ditemukan: {', '.join(completeness['missing_fields'])}")
        
        # Rekomendasi berdasarkan skor
        if completeness['score'] >= 85:
            print(f"   🌟 Excellent! Data sangat lengkap")
        elif completeness['score'] >= 70:
            print(f"   👍 Good! Data cukup lengkap")
        elif completeness['score'] >= 50:
            print(f"   ⚠️ Fair! Beberapa data tidak ditemukan")
        else:
            print(f"   🔧 Poor! Perlu perbaikan scraper untuk platform ini")
        
        # Siapkan data untuk return
        result = {
            'success': True,
            'url': url,
            'platform': platform,
            'video_info': {
                'title': stats.title,
                'author': stats.author,
                'views': stats.views,
                'likes': stats.likes,
                'comments': stats.comments,
                'shares': stats.shares
            },
            'upload_date': date_analysis,
            'completeness': completeness,
            'extracted_at': datetime.now().isoformat()
        }
        
        # Simpan ke file jika diminta
        if save_to_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"video_details_{timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Data disimpan ke: {filename}")
        
        return result
        
    except Exception as e:
        error_msg = f"Error saat mengekstrak data: {str(e)}"
        print(f"\n❌ {error_msg}")
        return {
            'success': False,
            'error': error_msg,
            'url': url,
            'platform': platform
        }

def main():
    """Fungsi utama untuk menjalankan ekstraksi video"""
    print("🎬 EKSTRAKSI DETAIL VIDEO & TANGGAL UNGGAH")
    print("=" * 80)
    print("Mendukung: YouTube, TikTok, Facebook")
    print("Ketik 'quit' untuk keluar\n")
    
    results = []
    
    while True:
        try:
            url = input("Masukkan URL video: ").strip()
            
            if url.lower() in ['quit', 'exit', 'q']:
                break
            
            if not url:
                print("❌ URL tidak boleh kosong!\n")
                continue
            
            # Tanya apakah ingin menyimpan hasil
            save_choice = input("Simpan hasil ke file JSON? (y/n): ").strip().lower()
            save_to_file = save_choice in ['y', 'yes', 'ya']
            
            # Ekstrak detail video
            result = extract_video_details(url, save_to_file)
            results.append(result)
            
            print("\n" + "=" * 80)
            
        except KeyboardInterrupt:
            print("\n\n👋 Ekstraksi dihentikan oleh user")
            break
        except Exception as e:
            print(f"\n❌ Error tidak terduga: {str(e)}")
    
    # Tampilkan ringkasan
    if results:
        print("\n" + "=" * 80)
        print("📊 RINGKASAN EKSTRAKSI")
        print("=" * 80)
        
        successful = [r for r in results if r.get('success', False)]
        failed = [r for r in results if not r.get('success', False)]
        
        print(f"Total video diproses: {len(results)}")
        print(f"Berhasil: {len(successful)}")
        print(f"Gagal: {len(failed)}")
        
        if successful:
            print("\n✅ VIDEO BERHASIL DIEKSTRAK:")
            for i, result in enumerate(successful, 1):
                title = result['video_info'].get('title', 'Tanpa judul')[:50]
                date_status = "✅" if result['upload_date']['is_valid'] else "❌"
                upload_date = result['upload_date'].get('formatted_date', 'Tidak ditemukan')
                completeness = result['completeness']['score']
                print(f"   {i}. {title}... - {date_status} {upload_date} ({completeness}%)")
        
        if failed:
            print("\n❌ VIDEO GAGAL DIEKSTRAK:")
            for i, result in enumerate(failed, 1):
                error = result.get('error', 'Unknown error')
                print(f"   {i}. {result.get('url', 'Unknown URL')} - {error}")
    
    print("\n👋 Terima kasih telah menggunakan Video Details Extractor!")

if __name__ == "__main__":
    main()