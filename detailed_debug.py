#!/usr/bin/env python3
"""
Detailed debug script untuk TikTok - mencari elemen dengan angka spesifik
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.tiktok_scraper import TikTokScraper
from selenium.webdriver.common.by import By

def detailed_debug():
    """Detailed debug untuk mencari elemen dengan angka 32K dan 12K"""
    url = "https://www.tiktok.com/@upnewsnet/video/7522432585037827346"
    print(f"Testing URL: {url}")
    
    try:
        scraper = TikTokScraper(headless=True)
        scraper.setup_driver()
        
        print("Loading page...")
        scraper.driver.get(url)
        time.sleep(15)  # Wait longer
        
        print("\n=== LOOKING FOR ELEMENTS WITH 32K OR 12K ===")
        # Look specifically for 32K and 12K
        try:
            elements_32k = scraper.driver.find_elements(By.XPATH, "//*[contains(text(), '32K') or contains(text(), '32k') or contains(text(), '32.') or contains(text(), '32')]")
            print(f"Found {len(elements_32k)} elements with '32'")
            
            for i, elem in enumerate(elements_32k):
                try:
                    text = elem.text.strip()
                    tag_name = elem.tag_name
                    class_attr = elem.get_attribute('class') or 'no-class'
                    data_e2e = elem.get_attribute('data-e2e') or 'no-data-e2e'
                    parent_class = elem.find_element(By.XPATH, '..'). get_attribute('class') if elem.find_element(By.XPATH, '..') else 'no-parent'
                    print(f"{i+1}. Tag: {tag_name}, Class: {class_attr}, Data-e2e: {data_e2e}, Parent: {parent_class}, Text: '{text}'")
                except Exception as e:
                    print(f"{i+1}. Error: {e}")
            
            elements_12k = scraper.driver.find_elements(By.XPATH, "//*[contains(text(), '12K') or contains(text(), '12k') or contains(text(), '12.') or contains(text(), '12')]")
            print(f"\nFound {len(elements_12k)} elements with '12'")
            
            for i, elem in enumerate(elements_12k):
                try:
                    text = elem.text.strip()
                    tag_name = elem.tag_name
                    class_attr = elem.get_attribute('class') or 'no-class'
                    data_e2e = elem.get_attribute('data-e2e') or 'no-data-e2e'
                    parent_class = elem.find_element(By.XPATH, '..'). get_attribute('class') if elem.find_element(By.XPATH, '..') else 'no-parent'
                    print(f"{i+1}. Tag: {tag_name}, Class: {class_attr}, Data-e2e: {data_e2e}, Parent: {parent_class}, Text: '{text}'")
                except Exception as e:
                    print(f"{i+1}. Error: {e}")
        except Exception as e:
            print(f"Error finding specific elements: {e}")
        
        print("\n=== LOOKING FOR ALL STRONG ELEMENTS ===")
        try:
            strong_elements = scraper.driver.find_elements(By.TAG_NAME, "strong")
            print(f"Found {len(strong_elements)} strong elements")
            
            for i, elem in enumerate(strong_elements[:20]):
                try:
                    text = elem.text.strip()
                    class_attr = elem.get_attribute('class') or 'no-class'
                    data_e2e = elem.get_attribute('data-e2e') or 'no-data-e2e'
                    if text and any(char.isdigit() for char in text):
                        print(f"{i+1}. Class: {class_attr}, Data-e2e: {data_e2e}, Text: '{text}'")
                except:
                    continue
        except Exception as e:
            print(f"Error finding strong elements: {e}")
        
        print("\n=== LOOKING FOR SPAN ELEMENTS WITH NUMBERS ===")
        try:
            span_elements = scraper.driver.find_elements(By.TAG_NAME, "span")
            print(f"Found {len(span_elements)} span elements")
            
            for i, elem in enumerate(span_elements):
                try:
                    text = elem.text.strip()
                    if text and any(char.isdigit() for char in text) and ('K' in text or 'M' in text or len(text) <= 10):
                        class_attr = elem.get_attribute('class') or 'no-class'
                        data_e2e = elem.get_attribute('data-e2e') or 'no-data-e2e'
                        print(f"{i+1}. Class: {class_attr}, Data-e2e: {data_e2e}, Text: '{text}'")
                        if i >= 15:  # Limit output
                            break
                except:
                    continue
        except Exception as e:
            print(f"Error finding span elements: {e}")
        
        print("\n=== TESTING ALTERNATIVE SELECTORS ===")
        alternative_selectors = {
            'likes_alt1': 'strong[data-e2e="like-count"]',
            'likes_alt2': 'span[data-e2e="like-count"]',
            'comments_alt1': 'strong[data-e2e="comment-count"]',
            'comments_alt2': 'span[data-e2e="comment-count"]',
            'shares_alt1': 'strong[data-e2e="share-count"]',
            'shares_alt2': 'span[data-e2e="share-count"]'
        }
        
        for name, selector in alternative_selectors.items():
            try:
                element = scraper.driver.find_element(By.CSS_SELECTOR, selector)
                text = element.text.strip()
                print(f"{name}: '{text}'")
            except:
                print(f"{name}: NOT FOUND")
        
        scraper.close_driver()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    detailed_debug()