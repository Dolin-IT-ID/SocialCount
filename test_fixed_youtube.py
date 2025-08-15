#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.youtube_scraper import YouTubeScraper

def test_youtube_shorts():
    """Test the fixed YouTube scraper with the provided Shorts URL"""
    
    url = "https://www.youtube.com/shorts/MaZWPkjuE-o"
    print(f"Testing YouTube Shorts URL: {url}")
    print("=" * 60)
    
    scraper = YouTubeScraper(headless=False)  # Use non-headless for debugging
    scraper.setup_driver()  # Setup the driver
    
    try:
        stats = scraper.scrape(url)
        
        print("\n=== EXTRACTION RESULTS ===")
        print(f"Title: {stats.title}")
        print(f"Author: {stats.author}")
        print(f"Views: {stats.views}")
        print(f"Likes: {stats.likes}")
        print(f"Comments: {stats.comments}")
        print(f"Shares: {stats.shares}")
        print(f"Upload Date: {stats.upload_date}")
        print(f"Error: {stats.error}")
        
        print("\n=== VALIDATION ===")
        # Expected values from user's screenshot: 32K likes, 12K comments
        if stats.likes:
            print(f"✓ Likes extracted: {stats.likes}")
            if stats.likes >= 30000:  # 32K should be around 32000
                print("✓ Likes count seems reasonable (≥30K)")
            else:
                print(f"⚠ Likes count ({stats.likes}) seems low compared to expected 32K")
        else:
            print("✗ No likes extracted")
            
        if stats.comments:
            print(f"✓ Comments extracted: {stats.comments}")
            if stats.comments >= 10000:  # 12K should be around 12000
                print("✓ Comments count seems reasonable (≥10K)")
            else:
                print(f"⚠ Comments count ({stats.comments}) seems low compared to expected 12K")
        else:
            print("✗ No comments extracted")
            
        if stats.title:
            print(f"✓ Title extracted: {stats.title[:50]}...")
        else:
            print("✗ No title extracted")
            
        if stats.author:
            print(f"✓ Author extracted: {stats.author}")
        else:
            print("✗ No author extracted")
        
    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        scraper.close_driver()

if __name__ == "__main__":
    test_youtube_shorts()