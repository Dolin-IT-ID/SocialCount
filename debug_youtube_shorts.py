#!/usr/bin/env python3
"""
Debug script khusus untuk YouTube Shorts
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.youtube_scraper import YouTubeScraper
from selenium.webdriver.common.by import By

def debug_youtube_shorts():
    """Debug YouTube Shorts untuk mencari selector yang tepat"""
    url = "https://www.youtube.com/shorts/MaZWPkjuE-o"
    print(f"Testing YouTube Shorts URL: {url}")
    
    try:
        scraper = YouTubeScraper(headless=True)
        scraper.setup_driver()
        
        print("Loading page...")
        scraper.driver.get(url)
        time.sleep(15)  # Wait longer for Shorts to load
        
        print("\n=== PAGE INFO ===")
        print(f"Page title: {scraper.driver.title}")
        print(f"Current URL: {scraper.driver.current_url}")
        
        print("\n=== LOOKING FOR NUMBERS (32K, 12K) ===")
        # Look for elements containing 32K or 12K
        try:
            elements_32k = scraper.driver.find_elements(By.XPATH, "//*[contains(text(), '32K') or contains(text(), '32k') or contains(text(), '32.') or contains(text(), '32')]")
            print(f"Found {len(elements_32k)} elements with '32'")
            
            for i, elem in enumerate(elements_32k[:10]):
                try:
                    text = elem.text.strip()
                    tag_name = elem.tag_name
                    class_attr = elem.get_attribute('class') or 'no-class'
                    aria_label = elem.get_attribute('aria-label') or 'no-aria-label'
                    print(f"{i+1}. Tag: {tag_name}, Class: {class_attr}, Aria-label: {aria_label}, Text: '{text}'")
                except Exception as e:
                    print(f"{i+1}. Error: {e}")
            
            elements_12k = scraper.driver.find_elements(By.XPATH, "//*[contains(text(), '12K') or contains(text(), '12k') or contains(text(), '12.') or contains(text(), '12')]")
            print(f"\nFound {len(elements_12k)} elements with '12'")
            
            for i, elem in enumerate(elements_12k[:10]):
                try:
                    text = elem.text.strip()
                    tag_name = elem.tag_name
                    class_attr = elem.get_attribute('class') or 'no-class'
                    aria_label = elem.get_attribute('aria-label') or 'no-aria-label'
                    print(f"{i+1}. Tag: {tag_name}, Class: {class_attr}, Aria-label: {aria_label}, Text: '{text}'")
                except Exception as e:
                    print(f"{i+1}. Error: {e}")
        except Exception as e:
            print(f"Error finding specific numbers: {e}")
        
        print("\n=== LOOKING FOR BUTTONS WITH ARIA-LABELS ===")
        try:
            buttons = scraper.driver.find_elements(By.TAG_NAME, "button")
            print(f"Found {len(buttons)} buttons")
            
            for i, button in enumerate(buttons[:20]):
                try:
                    aria_label = button.get_attribute('aria-label') or ''
                    text = button.text.strip()
                    if 'like' in aria_label.lower() or 'comment' in aria_label.lower() or any(char.isdigit() for char in aria_label):
                        print(f"{i+1}. Aria-label: '{aria_label}', Text: '{text}'")
                except:
                    continue
        except Exception as e:
            print(f"Error finding buttons: {e}")
        
        print("\n=== LOOKING FOR SPANS WITH NUMBERS ===")
        try:
            spans = scraper.driver.find_elements(By.TAG_NAME, "span")
            print(f"Found {len(spans)} spans")
            
            for i, span in enumerate(spans):
                try:
                    text = span.text.strip()
                    if text and any(char.isdigit() for char in text) and ('K' in text or 'M' in text or len(text) <= 10):
                        class_attr = span.get_attribute('class') or 'no-class'
                        print(f"{i+1}. Class: {class_attr}, Text: '{text}'")
                        if i >= 15:  # Limit output
                            break
                except:
                    continue
        except Exception as e:
            print(f"Error finding spans: {e}")
        
        print("\n=== TESTING SHORTS-SPECIFIC SELECTORS ===")
        shorts_selectors = {
            'likes_shorts1': 'button[aria-label*="like"] span',
            'likes_shorts2': '#like-button span',
            'likes_shorts3': '.YtLikeButtonViewModelHost span',
            'comments_shorts1': 'button[aria-label*="comment"] span',
            'comments_shorts2': '#comment-button span',
            'comments_shorts3': '.YtCommentButtonViewModelHost span',
            'title_shorts': 'h2.ytd-reel-video-renderer',
            'author_shorts': '.ytd-reel-player-header-renderer .yt-simple-endpoint'
        }
        
        for name, selector in shorts_selectors.items():
            try:
                element = scraper.driver.find_element(By.CSS_SELECTOR, selector)
                text = element.text.strip()
                aria_label = element.get_attribute('aria-label') or ''
                print(f"{name}: Text='{text}', Aria-label='{aria_label}'")
            except:
                print(f"{name}: NOT FOUND")
        
        scraper.close_driver()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_youtube_shorts()