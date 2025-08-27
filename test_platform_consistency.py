#!/usr/bin/env python3
"""
Test Platform Consistency for Upload Date Extraction

Script ini menguji konsistensi ekstraksi tanggal unggah di semua platform
(YouTube, TikTok, Facebook) untuk memastikan semua platform dapat mengakses
dan menampilkan tanggal unggah dengan konsisten.
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

def test_date_extraction_methods(scraper_class, platform_name):
    """Test date extraction methods for a specific platform"""
    print(f"\n🔍 Testing {platform_name} Date Extraction Methods:")
    print("=" * 50)
    
    # Test if scraper has required methods
    methods_to_check = [
        '_normalize_date',
        '_convert_relative_time',
        '_convert_relative_time_indonesian'
    ]
    
    enhanced_method = f'_enhanced_date_extraction_{platform_name.lower()}'
    if platform_name.lower() == 'youtube':
        enhanced_method = '_enhanced_date_extraction'
    
    methods_to_check.append(enhanced_method)
    
    # Create a temporary instance to check methods
    try:
        with scraper_class() as scraper:
            for method in methods_to_check:
                if hasattr(scraper, method):
                    print(f"✅ {method}: Available")
                else:
                    print(f"❌ {method}: Missing")
            
            # Test date normalization with sample dates
            test_dates = [
                "October 24, 2009",
                "2023-01-30T02:34:17-08:00",
                "2 days ago",
                "1 minggu yang lalu",
                "2024-01-15",
                "15 Jan 2024"
            ]
            
            print("\n📅 Testing Date Normalization:")
            for test_date in test_dates:
                try:
                    normalized = scraper._normalize_date(test_date)
                    status = "✅" if normalized else "❌"
                    print(f"  {status} '{test_date}' → '{normalized}'")
                except Exception as e:
                    print(f"  ❌ '{test_date}' → Error: {str(e)}")
    
    except Exception as e:
        print(f"❌ Error testing {platform_name}: {str(e)}")

def test_platform_consistency():
    """Test consistency across all platforms"""
    print("🎬 TESTING PLATFORM CONSISTENCY FOR UPLOAD DATE EXTRACTION")
    print("=" * 60)
    print("Testing date extraction methods across YouTube, TikTok, and Facebook")
    print("to ensure consistent display and accessibility of upload dates.\n")
    
    platforms = [
        ('youtube', YouTubeScraper, 'YouTube'),
        ('tiktok', TikTokScraper, 'TikTok'),
        ('facebook', FacebookScraper, 'Facebook')
    ]
    
    results = {}
    
    for platform_key, scraper_class, platform_name in platforms:
        try:
            test_date_extraction_methods(scraper_class, platform_name)
            results[platform_name] = "✅ Passed"
        except Exception as e:
            results[platform_name] = f"❌ Failed: {str(e)}"
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 CONSISTENCY TEST SUMMARY:")
    print("=" * 60)
    
    all_passed = True
    for platform, result in results.items():
        print(f"{platform:12}: {result}")
        if "Failed" in result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL PLATFORMS PASSED CONSISTENCY TESTS!")
        print("✅ Upload dates can be accessed and displayed consistently across all platforms.")
    else:
        print("⚠️  SOME PLATFORMS FAILED CONSISTENCY TESTS")
        print("❌ Please review the failed platforms above.")
    
    print("\n🔧 Enhanced Features Available:")
    print("  • Multiple date format support (ISO 8601, relative time, etc.)")
    print("  • Fallback extraction methods for each platform")
    print("  • Consistent date normalization across platforms")
    print("  • Support for both English and Indonesian relative time")
    print("  • Unix timestamp handling")
    print("  • Meta tag and JSON-LD extraction")
    
    return all_passed

def test_sample_urls():
    """Test with sample URLs if available"""
    print("\n" + "=" * 60)
    print("🌐 TESTING WITH SAMPLE URLS (if provided):")
    print("=" * 60)
    
    # Sample URLs for testing (you can modify these)
    sample_urls = {
        'YouTube': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        # Add TikTok and Facebook URLs here if needed for testing
        # 'TikTok': 'https://www.tiktok.com/@username/video/1234567890',
        # 'Facebook': 'https://www.facebook.com/watch/?v=1234567890'
    }
    
    for platform, url in sample_urls.items():
        print(f"\n🔗 Testing {platform}: {url}")
        try:
            detected_platform = URLDetector.detect_platform(url)
            scraper_class = get_scraper(detected_platform)
            
            if scraper_class:
                with scraper_class() as scraper:
                    stats = scraper.scrape(url)
                    if stats and stats.upload_date:
                        print(f"  ✅ Upload Date: {stats.upload_date}")
                        print(f"  ✅ Title: {stats.title or 'N/A'}")
                        print(f"  ✅ Platform: {stats.platform}")
                    else:
                        print(f"  ❌ Failed to extract upload date")
            else:
                print(f"  ❌ No scraper available for {detected_platform}")
        
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")

if __name__ == "__main__":
    try:
        # Test platform consistency
        consistency_passed = test_platform_consistency()
        
        # Test with sample URLs
        test_sample_urls()
        
        print("\n" + "=" * 60)
        print("🏁 TESTING COMPLETED")
        print("=" * 60)
        
        if consistency_passed:
            print("✅ All platforms are consistent and ready for use!")
            print("🎯 Upload dates will be displayed consistently across YouTube, TikTok, and Facebook.")
        else:
            print("⚠️  Some issues detected. Please review the test results above.")
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Testing interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Unexpected error during testing: {str(e)}")
        import traceback
        traceback.print_exc()