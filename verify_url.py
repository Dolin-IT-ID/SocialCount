#!/usr/bin/env python3
"""
Verify URL and check if we're getting the right video
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.tiktok_scraper import TikTokScraper
from selenium.webdriver.common.by import By

def verify_video():
    """Verify we're getting the right video"""
    url = "https://www.tiktok.com/@upnewsnet/video/7522432585037827346"
    print(f"Testing URL: {url}")
    
    try:
        scraper = TikTokScraper(headless=False)  # Non-headless to see what's happening
        scraper.setup_driver()
        
        print("Loading page...")
        scraper.driver.get(url)
        time.sleep(20)  # Wait longer to see the page
        
        print("\n=== PAGE INFO ===")
        print(f"Page title: {scraper.driver.title}")
        print(f"Current URL: {scraper.driver.current_url}")
        
        # Check if we can find the video description
        try:
            desc_element = scraper.driver.find_element(By.CSS_SELECTOR, '[data-e2e="video-desc"]')
            print(f"Video description: {desc_element.text}")
        except:
            print("Video description not found")
        
        # Check author
        try:
            author_element = scraper.driver.find_element(By.CSS_SELECTOR, '[data-e2e="video-author-uniqueid"]')
            print(f"Author: {author_element.text}")
        except:
            print("Author not found")
        
        # Get all stats
        print("\n=== CURRENT STATS ===")
        try:
            likes_elem = scraper.driver.find_element(By.CSS_SELECTOR, '[data-e2e="like-count"]')
            print(f"Likes: {likes_elem.text}")
        except:
            print("Likes not found")
        
        try:
            comments_elem = scraper.driver.find_element(By.CSS_SELECTOR, '[data-e2e="comment-count"]')
            print(f"Comments: {comments_elem.text}")
        except:
            print("Comments not found")
        
        try:
            shares_elem = scraper.driver.find_element(By.CSS_SELECTOR, '[data-e2e="share-count"]')
            print(f"Shares: {shares_elem.text}")
        except:
            print("Shares not found")
        
        # Wait for user to see the page
        print("\n=== BROWSER OPENED ===")
        print("Browser window is open. Check if this is the correct video.")
        print("Press Enter to continue...")
        input()
        
        scraper.close_driver()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_video()