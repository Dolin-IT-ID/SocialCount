#!/usr/bin/env python3
"""
Debug script untuk menguji TikTok scraper dengan analisis HTML
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.tiktok_scraper import TikTokScraper
from utils.url_detector import URLDetector
from selenium.webdriver.common.by import By

def debug_tiktok_html(url):
    """Debug TikTok scraper dengan analisis HTML detail"""
    print(f"\n=== DEBUG TIKTOK HTML ANALYSIS ===")
    print(f"URL: {url}")
    
    # Validasi URL
    url_info = URLDetector.validate_url(url)
    print(f"URL Valid: {url_info['valid']}")
    print(f"Platform: {url_info.get('platform', 'unknown')}")
    
    if not url_info['valid']:
        print(f"Error: {url_info['error']}")
        return
    
    # Test scraper dengan analisis HTML
    print("\n=== MEMULAI ANALISIS HTML ===")
    try:
        scraper = TikTokScraper(headless=True)  # Headless untuk speed
        scraper.setup_driver()
        
        print("Loading page...")
        scraper.driver.get(url)
        time.sleep(10)  # Wait for page to load
        
        print("\n=== MENCARI ELEMEN STATISTIK ===")
        
        # Cari semua elemen yang mungkin berisi angka
        print("\n--- MENCARI ELEMEN DENGAN ANGKA ---")
        elements_with_numbers = scraper.driver.find_elements(By.XPATH, "//*[contains(text(), 'K') or contains(text(), 'M') or contains(text(), 'B') or contains(text(), '1') or contains(text(), '2') or contains(text(), '3') or contains(text(), '4') or contains(text(), '5') or contains(text(), '6') or contains(text(), '7') or contains(text(), '8') or contains(text(), '9') or contains(text(), '0')]")
        
        for i, elem in enumerate(elements_with_numbers[:20]):  # Limit to first 20
            try:
                text = elem.text.strip()
                if text and any(char.isdigit() for char in text):
                    tag_name = elem.tag_name
                    class_attr = elem.get_attribute('class') or 'no-class'
                    data_e2e = elem.get_attribute('data-e2e') or 'no-data-e2e'
                    print(f"{i+1}. Tag: {tag_name}, Class: {class_attr}, Data-e2e: {data_e2e}, Text: '{text}'")
            except:
                continue
        
        print("\n--- MENCARI ELEMEN DENGAN DATA-E2E ---")
        data_e2e_elements = scraper.driver.find_elements(By.XPATH, "//*[@data-e2e]")
        for i, elem in enumerate(data_e2e_elements[:15]):  # Limit to first 15
            try:
                data_e2e = elem.get_attribute('data-e2e')
                text = elem.text.strip()
                if text:
                    print(f"{i+1}. Data-e2e: {data_e2e}, Text: '{text}'")
            except:
                continue
        
        print("\n--- MENCARI ELEMEN DENGAN CLASS YANG MENGANDUNG 'count' ---")
        count_elements = scraper.driver.find_elements(By.XPATH, "//*[contains(@class, 'count')]")
        for i, elem in enumerate(count_elements[:10]):
            try:
                class_attr = elem.get_attribute('class')
                text = elem.text.strip()
                print(f"{i+1}. Class: {class_attr}, Text: '{text}'")
            except:
                continue
        
        print("\n--- TESTING CURRENT SELECTORS ---")
        # Test current selectors
        selectors_to_test = {
            'likes': ['[data-e2e="like-count"]', '[data-e2e="video-like-count"]', '.like-count', 'strong[data-e2e="like-count"]'],
            'comments': ['[data-e2e="comment-count"]', '[data-e2e="video-comment-count"]', '.comment-count', 'strong[data-e2e="comment-count"]'],
            'shares': ['[data-e2e="share-count"]', '[data-e2e="video-share-count"]', '.share-count', 'strong[data-e2e="share-count"]'],
            'views': ['[data-e2e="video-views"]', '.video-count', '.playback-count'],
            'title': ['[data-e2e="video-desc"]', '.video-meta-caption', '.tt-video-meta-caption', 'h1[data-e2e="video-desc"]'],
            'author': ['[data-e2e="video-author-uniqueid"]', '.author-uniqueid', 'h3[data-e2e="video-author-uniqueid"]', '.username']
        }
        
        for metric, selectors in selectors_to_test.items():
            print(f"\n{metric.upper()}:")
            for selector in selectors:
                try:
                    element = scraper.driver.find_element(By.CSS_SELECTOR, selector)
                    if element:
                        text = element.text.strip()
                        print(f"  ✓ {selector}: '{text}'")
                        break
                except:
                    print(f"  ✗ {selector}: Not found")
        
        # Test scraper normal
        print("\n=== HASIL SCRAPER NORMAL ===")
        stats = scraper.scrape(url)
        print(f"Views: {stats.views}")
        print(f"Likes: {stats.likes}")
        print(f"Shares: {stats.shares}")
        print(f"Comments: {stats.comments}")
        print(f"Title: {stats.title}")
        print(f"Author: {stats.author}")
        
        scraper.close_driver()
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # URL TikTok dari screenshot
    test_url = "https://www.tiktok.com/@upnewsnet/video/7522432585037827346"
    debug_tiktok_html(test_url)