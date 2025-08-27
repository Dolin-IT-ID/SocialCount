#!/usr/bin/env python3
"""
Script untuk menguji dan memvalidasi ekstraksi tanggal unggah video
dari berbagai platform media sosial.

Script ini akan:
1. Menguji ekstraksi tanggal unggah dari URL yang diberikan
2. Menampilkan detail lengkap metadata video
3. Memvalidasi akurasi informasi yang diperoleh
4. Memberikan saran perbaikan jika diperlukan
"""

import sys
import os
import json
from datetime import datetime
from urllib.parse import urlparse

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers import ScraperFactory

def detect_platform(url: str) -> str:
    """Deteksi platform berdasarkan URL"""
    parsed_url = urlparse(url.lower())
    domain = parsed_url.netloc.replace('www.', '')
    
    if 'youtube.com' in domain or 'youtu.be' in domain:
        return 'youtube'
    elif 'tiktok.com' in domain:
        return 'tiktok'
    elif 'facebook.com' in domain or 'fb.com' in domain:
        return 'facebook'
    else:
        raise ValueError(f"Platform tidak didukung untuk URL: {url}")

def format_upload_date(date_str: str) -> dict:
    """Format dan validasi tanggal unggah"""
    if not date_str:
        return {
            'raw': None,
            'formatted': None,
            'is_valid': False,
            'error': 'Tanggal unggah tidak ditemukan'
        }
    
    result = {
        'raw': date_str,
        'formatted': None,
        'is_valid': False,
        'error': None
    }
    
    try:
        # Coba berbagai format tanggal yang umum
        date_formats = [
            '%Y-%m-%d',
            '%d/%m/%Y',
            '%m/%d/%Y',
            '%B %d, %Y',
            '%d %B %Y',
            '%Y-%m-%d %H:%M:%S',
            '%d-%m-%Y'
        ]
        
        # Bersihkan string tanggal
        clean_date = date_str.strip()
        
        # Coba parsing dengan berbagai format
        parsed_date = None
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(clean_date, fmt)
                break
            except ValueError:
                continue
        
        if parsed_date:
            result['formatted'] = parsed_date.strftime('%d %B %Y')
            result['is_valid'] = True
        else:
            # Jika tidak bisa diparse, tetap simpan sebagai string
            result['formatted'] = clean_date
            result['is_valid'] = False
            result['error'] = 'Format tanggal tidak dapat diparse'
            
    except Exception as e:
        result['error'] = f'Error memproses tanggal: {str(e)}'
    
    return result

def validate_metadata(stats) -> dict:
    """Validasi kelengkapan dan akurasi metadata"""
    validation = {
        'completeness_score': 0,
        'total_fields': 8,
        'missing_fields': [],
        'present_fields': [],
        'recommendations': []
    }
    
    # Daftar field yang harus ada
    required_fields = {
        'title': stats.title,
        'author': stats.author,
        'views': stats.views,
        'likes': stats.likes,
        'comments': stats.comments,
        'shares': stats.shares,
        'upload_date': stats.upload_date,
        'error': stats.error
    }
    
    # Hitung skor kelengkapan
    for field, value in required_fields.items():
        if value is not None and value != '':
            validation['present_fields'].append(field)
            validation['completeness_score'] += 1
        else:
            validation['missing_fields'].append(field)
    
    # Berikan rekomendasi
    if 'upload_date' in validation['missing_fields']:
        validation['recommendations'].append(
            "Tanggal unggah tidak ditemukan. Periksa selector CSS untuk platform ini."
        )
    
    if 'title' in validation['missing_fields']:
        validation['recommendations'].append(
            "Judul video tidak ditemukan. Mungkin halaman belum sepenuhnya dimuat."
        )
    
    if 'author' in validation['missing_fields']:
        validation['recommendations'].append(
            "Nama author/channel tidak ditemukan. Periksa selector untuk nama channel."
        )
    
    if validation['completeness_score'] < 4:
        validation['recommendations'].append(
            "Skor kelengkapan rendah. Pertimbangkan untuk meningkatkan waktu tunggu atau memperbaiki selector."
        )
    
    return validation

def test_upload_date_extraction(url: str, verbose: bool = True) -> dict:
    """Menguji ekstraksi tanggal unggah dari URL yang diberikan"""
    
    print(f"\n{'='*60}")
    print(f"MENGUJI EKSTRAKSI TANGGAL UNGGAH")
    print(f"{'='*60}")
    print(f"URL: {url}")
    
    try:
        # Deteksi platform
        platform = detect_platform(url)
        print(f"Platform: {platform.upper()}")
        
        # Buat scraper
        print(f"\nMemulai scraping...")
        with ScraperFactory.create_scraper(platform, headless=False) as scraper:
            stats = scraper.scrape(url)
        
        # Format hasil
        result = {
            'url': url,
            'platform': platform,
            'timestamp': datetime.now().isoformat(),
            'metadata': stats.to_dict(),
            'upload_date_analysis': format_upload_date(stats.upload_date),
            'validation': validate_metadata(stats)
        }
        
        # Tampilkan hasil detail
        if verbose:
            print(f"\n{'='*60}")
            print(f"HASIL EKSTRAKSI METADATA")
            print(f"{'='*60}")
            
            print(f"\n📹 INFORMASI VIDEO:")
            print(f"   Judul: {stats.title or 'Tidak ditemukan'}")
            print(f"   Author: {stats.author or 'Tidak ditemukan'}")
            print(f"   Platform: {stats.platform.upper()}")
            
            print(f"\n📊 STATISTIK:")
            print(f"   Views: {stats.views:,} views" if stats.views else "   Views: Tidak ditemukan")
            print(f"   Likes: {stats.likes:,} likes" if stats.likes else "   Likes: Tidak ditemukan")
            print(f"   Comments: {stats.comments:,} comments" if stats.comments else "   Comments: Tidak ditemukan")
            print(f"   Shares: {stats.shares:,} shares" if stats.shares else "   Shares: Tidak ditemukan")
            
            print(f"\n📅 TANGGAL UNGGAH:")
            upload_analysis = result['upload_date_analysis']
            print(f"   Raw Data: {upload_analysis['raw'] or 'Tidak ditemukan'}")
            print(f"   Formatted: {upload_analysis['formatted'] or 'Tidak dapat diformat'}")
            print(f"   Valid: {'✅ Ya' if upload_analysis['is_valid'] else '❌ Tidak'}")
            if upload_analysis['error']:
                print(f"   Error: {upload_analysis['error']}")
            
            print(f"\n📋 VALIDASI METADATA:")
            validation = result['validation']
            print(f"   Skor Kelengkapan: {validation['completeness_score']}/{validation['total_fields']} ({validation['completeness_score']/validation['total_fields']*100:.1f}%)")
            print(f"   Field Tersedia: {', '.join(validation['present_fields']) if validation['present_fields'] else 'Tidak ada'}")
            print(f"   Field Hilang: {', '.join(validation['missing_fields']) if validation['missing_fields'] else 'Tidak ada'}")
            
            if validation['recommendations']:
                print(f"\n💡 REKOMENDASI:")
                for i, rec in enumerate(validation['recommendations'], 1):
                    print(f"   {i}. {rec}")
            
            if stats.error:
                print(f"\n❌ ERROR: {stats.error}")
        
        return result
        
    except Exception as e:
        error_result = {
            'url': url,
            'platform': None,
            'timestamp': datetime.now().isoformat(),
            'error': str(e),
            'metadata': None,
            'upload_date_analysis': None,
            'validation': None
        }
        
        if verbose:
            print(f"\n❌ ERROR: {str(e)}")
        
        return error_result

def save_results(results: dict, filename: str = None):
    """Simpan hasil ke file JSON"""
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'upload_date_test_results_{timestamp}.json'
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Hasil disimpan ke: {filename}")

def main():
    """Fungsi utama untuk menjalankan tes"""
    print("🔍 TESTER EKSTRAKSI TANGGAL UNGGAH VIDEO")
    print("Masukkan URL video untuk menguji ekstraksi tanggal unggah dan metadata lengkap.")
    print("Platform yang didukung: YouTube, TikTok, Facebook")
    print("Ketik 'quit' untuk keluar.\n")
    
    results = []
    
    while True:
        try:
            url = input("Masukkan URL video: ").strip()
            
            if url.lower() in ['quit', 'exit', 'q']:
                break
            
            if not url:
                print("URL tidak boleh kosong!")
                continue
            
            # Test ekstraksi
            result = test_upload_date_extraction(url)
            results.append(result)
            
            # Tanya apakah ingin menyimpan hasil
            save_choice = input("\nSimpan hasil ke file JSON? (y/n): ").strip().lower()
            if save_choice in ['y', 'yes']:
                save_results(result)
            
            print("\n" + "="*60)
            
        except KeyboardInterrupt:
            print("\n\nTes dihentikan oleh user.")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
    
    if results:
        print(f"\n📊 RINGKASAN TES:")
        print(f"Total URL yang diuji: {len(results)}")
        successful = len([r for r in results if r.get('metadata') and not r.get('error')])
        print(f"Berhasil: {successful}/{len(results)} ({successful/len(results)*100:.1f}%)")
        
        # Simpan semua hasil
        if len(results) > 1:
            save_choice = input("\nSimpan semua hasil ke file JSON? (y/n): ").strip().lower()
            if save_choice in ['y', 'yes']:
                save_results(results, 'all_upload_date_test_results.json')

if __name__ == "__main__":
    main()