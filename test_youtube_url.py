#!/usr/bin/env python3
"""
Test YouTube scraper dengan URL yang benar dari screenshot
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.youtube_scraper import YouTubeScraper
from utils.url_detector import URLDetector

def test_youtube_url():
    """Test YouTube scraper dengan URL dari screenshot"""
    url = "https://www.youtube.com/shorts/MaZWPkjuE-o"
    print(f"Testing YouTube URL: {url}")
    
    # Validasi URL
    url_info = URLDetector.validate_url(url)
    print(f"URL Valid: {url_info['valid']}")
    print(f"Platform: {url_info.get('platform', 'unknown')}")
    
    if not url_info['valid']:
        print(f"Error: {url_info['error']}")
        return
    
    # Test scraper
    print("\n=== MEMULAI SCRAPING YOUTUBE ===")
    try:
        with YouTubeScraper(headless=True) as scraper:
            stats = scraper.scrape(url)
            
            print("\n=== HASIL SCRAPING ===")
            print(f"Platform: {stats.platform}")
            print(f"Title: {stats.title}")
            print(f"Author: {stats.author}")
            print(f"Views: {stats.views}")
            print(f"Likes: {stats.likes}")
            print(f"Shares: {stats.shares}")
            print(f"Comments: {stats.comments}")
            print(f"Upload Date: {stats.upload_date}")
            print(f"Error: {stats.error}")
            
            print("\n=== DICTIONARY OUTPUT ===")
            print(stats.to_dict())
            
            # Cek apakah data sesuai dengan screenshot (32K likes, 12K comments)
            print("\n=== VERIFIKASI DATA ===")
            if stats.likes:
                print(f"Likes found: {stats.likes}")
                if '32' in str(stats.likes) or '32K' in str(stats.likes):
                    print("✓ Likes sesuai dengan screenshot (32K)")
                else:
                    print("⚠ Likes tidak sesuai dengan screenshot")
            
            if stats.comments:
                print(f"Comments found: {stats.comments}")
                if '12' in str(stats.comments) or '12K' in str(stats.comments):
                    print("✓ Comments sesuai dengan screenshot (12K)")
                else:
                    print("⚠ Comments tidak sesuai dengan screenshot")
            
    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_youtube_url()