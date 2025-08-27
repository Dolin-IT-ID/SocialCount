#!/usr/bin/env python3
"""
Enhanced Date Extractor untuk meningkatkan akurasi ekstraksi tanggal unggah
dari berbagai platform media sosial.

Script ini menyediakan:
1. Selector CSS yang lebih komprehensif untuk setiap platform
2. Parser tanggal yang lebih robust
3. Fallback methods untuk ekstraksi tanggal
4. Validasi dan normalisasi format tanggal
"""

import re
import time
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class EnhancedDateExtractor:
    """Enhanced date extractor dengan multiple strategies"""
    
    # Comprehensive selectors untuk setiap platform
    YOUTUBE_DATE_SELECTORS = [
        # Regular video selectors
        '#info-strings yt-formatted-string',
        '.ytd-video-secondary-info-renderer #date',
        '#date yt-formatted-string',
        '.ytd-video-secondary-info-renderer .ytd-video-meta-block #date',
        '#info #date yt-formatted-string',
        '.ytd-video-meta-block #date',
        
        # Shorts selectors
        '.ytd-reel-player-header-renderer .published-time-text',
        '.reel-player-header-renderer .published-time-text',
        'span[class*="published-time"]',
        '.published-time-text',
        '.ytd-reel-video-in-sequence-renderer .published-time-text',
        
        # Meta tags fallback
        'meta[property="video:release_date"]',
        'meta[property="article:published_time"]',
        'meta[name="uploadDate"]',
        
        # JSON-LD structured data
        'script[type="application/ld+json"]'
    ]
    
    FACEBOOK_DATE_SELECTORS = [
        # Primary selectors
        'abbr[data-utime]',
        '[data-testid="story-subtitle"] a[role="link"]',
        '.timestamp',
        
        # Additional selectors
        'abbr[title]',
        '[data-testid="story-subtitle"] abbr',
        '.story_body_container abbr',
        '[data-testid="feed-story-ring"] abbr',
        '.userContentWrapper abbr',
        
        # Time elements
        'time[datetime]',
        '[data-tooltip-content]',
        '.timestampContent',
        
        # Meta tags
        'meta[property="article:published_time"]',
        'meta[property="og:updated_time"]'
    ]
    
    TIKTOK_DATE_SELECTORS = [
        # Primary selectors
        '.video-meta-date',
        '[data-e2e="video-date"]',
        
        # Additional selectors
        '.video-info-detail time',
        '.video-card-info time',
        '[data-e2e="browse-video-desc"] time',
        '.video-meta-info time',
        
        # Fallback selectors
        'time[datetime]',
        '.upload-time',
        '.publish-time',
        
        # Meta tags
        'meta[property="video:release_date"]',
        'meta[name="uploadDate"]'
    ]
    
    # Date patterns untuk parsing
    DATE_PATTERNS = [
        # English patterns
        r'(\w+ \d{1,2}, \d{4})',  # Jan 15, 2024
        r'(\d{1,2} \w+ \d{4})',   # 15 Jan 2024
        r'(\d{4}-\d{2}-\d{2})',   # 2024-01-15
        r'(\d{1,2}/\d{1,2}/\d{4})', # 01/15/2024
        r'(\d{1,2}-\d{1,2}-\d{4})', # 01-15-2024
        
        # Relative time patterns
        r'(\d+)\s+(second|minute|hour|day|week|month|year)s?\s+ago',
        r'(\d+)\s+(detik|menit|jam|hari|minggu|bulan|tahun)\s+(yang\s+)?lalu',
        
        # Indonesian patterns
        r'(\d{1,2}\s+\w+\s+\d{4})',  # 15 Januari 2024
        
        # ISO format
        r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})',
    ]
    
    # Month mappings
    MONTH_MAPPINGS = {
        # English
        'jan': 1, 'january': 1, 'feb': 2, 'february': 2, 'mar': 3, 'march': 3,
        'apr': 4, 'april': 4, 'may': 5, 'jun': 6, 'june': 6,
        'jul': 7, 'july': 7, 'aug': 8, 'august': 8, 'sep': 9, 'september': 9,
        'oct': 10, 'october': 10, 'nov': 11, 'november': 11, 'dec': 12, 'december': 12,
        
        # Indonesian
        'januari': 1, 'februari': 2, 'maret': 3, 'april': 4, 'mei': 5, 'juni': 6,
        'juli': 7, 'agustus': 8, 'september': 9, 'oktober': 10, 'november': 11, 'desember': 12
    }
    
    def __init__(self, driver):
        self.driver = driver
    
    def extract_date_youtube(self) -> Optional[str]:
        """Extract upload date from YouTube with multiple strategies"""
        
        # Strategy 1: Try standard selectors
        for selector in self.YOUTUBE_DATE_SELECTORS:
            try:
                if selector.startswith('meta'):
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    date_value = element.get_attribute('content')
                    if date_value:
                        return self._normalize_date(date_value)
                elif selector.startswith('script'):
                    # Parse JSON-LD structured data
                    scripts = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for script in scripts:
                        try:
                            import json
                            data = json.loads(script.get_attribute('innerHTML'))
                            if isinstance(data, dict) and 'uploadDate' in data:
                                return self._normalize_date(data['uploadDate'])
                        except:
                            continue
                else:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element and element.text:
                        date_text = element.text.strip()
                        if date_text:
                            return self._normalize_date(date_text)
            except:
                continue
        
        # Strategy 2: Search in page source for date patterns
        return self._extract_from_page_source()
    
    def extract_date_facebook(self) -> Optional[str]:
        """Extract upload date from Facebook with multiple strategies"""
        
        # Strategy 1: Try data-utime attribute (Unix timestamp)
        try:
            utime_elements = self.driver.find_elements(By.CSS_SELECTOR, 'abbr[data-utime]')
            for element in utime_elements:
                utime = element.get_attribute('data-utime')
                if utime and utime.isdigit():
                    timestamp = int(utime)
                    date_obj = datetime.fromtimestamp(timestamp)
                    return date_obj.strftime('%B %d, %Y')
        except:
            pass
        
        # Strategy 2: Try standard selectors
        for selector in self.FACEBOOK_DATE_SELECTORS:
            try:
                if selector.startswith('meta'):
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    date_value = element.get_attribute('content')
                    if date_value:
                        return self._normalize_date(date_value)
                else:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element:
                        # Try title attribute first, then text
                        date_text = element.get_attribute('title') or element.text
                        if date_text:
                            return self._normalize_date(date_text.strip())
            except:
                continue
        
        # Strategy 3: Search in page source
        return self._extract_from_page_source()
    
    def extract_date_tiktok(self) -> Optional[str]:
        """Extract upload date from TikTok with multiple strategies"""
        
        # Strategy 1: Try standard selectors
        for selector in self.TIKTOK_DATE_SELECTORS:
            try:
                if selector.startswith('meta'):
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    date_value = element.get_attribute('content')
                    if date_value:
                        return self._normalize_date(date_value)
                else:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element:
                        # Try datetime attribute first, then text
                        date_text = element.get_attribute('datetime') or element.text
                        if date_text:
                            return self._normalize_date(date_text.strip())
            except:
                continue
        
        # Strategy 2: Search in page source
        return self._extract_from_page_source()
    
    def _extract_from_page_source(self) -> Optional[str]:
        """Extract date from page source using regex patterns"""
        try:
            page_source = self.driver.page_source
            
            # Try each date pattern
            for pattern in self.DATE_PATTERNS:
                matches = re.findall(pattern, page_source, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0] if match[0] else ' '.join(match)
                    
                    normalized = self._normalize_date(match)
                    if normalized:
                        return normalized
        except:
            pass
        
        return None
    
    def _normalize_date(self, date_str: str) -> Optional[str]:
        """Normalize date string to consistent format"""
        if not date_str:
            return None
        
        date_str = date_str.strip()
        
        # Handle relative time (e.g., "2 days ago")
        relative_match = re.search(r'(\d+)\s+(second|minute|hour|day|week|month|year)s?\s+ago', date_str, re.IGNORECASE)
        if relative_match:
            return self._convert_relative_time(relative_match.group(1), relative_match.group(2))
        
        # Handle Indonesian relative time
        relative_match_id = re.search(r'(\d+)\s+(detik|menit|jam|hari|minggu|bulan|tahun)\s+(yang\s+)?lalu', date_str, re.IGNORECASE)
        if relative_match_id:
            return self._convert_relative_time_indonesian(relative_match_id.group(1), relative_match_id.group(2))
        
        # Try to parse various date formats
        date_formats = [
            '%Y-%m-%d',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%Y-%m-%dT%H:%M:%SZ',
            '%B %d, %Y',
            '%b %d, %Y',
            '%d %B %Y',
            '%d %b %Y',
            '%m/%d/%Y',
            '%d/%m/%Y',
            '%m-%d-%Y',
            '%d-%m-%Y'
        ]
        
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                return parsed_date.strftime('%B %d, %Y')
            except ValueError:
                continue
        
        # Try manual parsing for mixed formats
        try:
            return self._manual_date_parse(date_str)
        except:
            pass
        
        # If all else fails, return the original string
        return date_str
    
    def _convert_relative_time(self, amount: str, unit: str) -> str:
        """Convert relative time to actual date"""
        try:
            amount = int(amount)
            now = datetime.now()
            
            if unit.lower().startswith('second'):
                target_date = now - timedelta(seconds=amount)
            elif unit.lower().startswith('minute'):
                target_date = now - timedelta(minutes=amount)
            elif unit.lower().startswith('hour'):
                target_date = now - timedelta(hours=amount)
            elif unit.lower().startswith('day'):
                target_date = now - timedelta(days=amount)
            elif unit.lower().startswith('week'):
                target_date = now - timedelta(weeks=amount)
            elif unit.lower().startswith('month'):
                target_date = now - timedelta(days=amount*30)  # Approximate
            elif unit.lower().startswith('year'):
                target_date = now - timedelta(days=amount*365)  # Approximate
            else:
                return None
            
            return target_date.strftime('%B %d, %Y')
        except:
            return None
    
    def _convert_relative_time_indonesian(self, amount: str, unit: str) -> str:
        """Convert Indonesian relative time to actual date"""
        unit_mapping = {
            'detik': 'second',
            'menit': 'minute', 
            'jam': 'hour',
            'hari': 'day',
            'minggu': 'week',
            'bulan': 'month',
            'tahun': 'year'
        }
        
        english_unit = unit_mapping.get(unit.lower())
        if english_unit:
            return self._convert_relative_time(amount, english_unit)
        
        return None
    
    def _manual_date_parse(self, date_str: str) -> Optional[str]:
        """Manual parsing for complex date formats"""
        # Remove common prefixes/suffixes
        date_str = re.sub(r'^(published|uploaded|posted)\s+', '', date_str, flags=re.IGNORECASE)
        date_str = re.sub(r'\s+(ago|lalu)$', '', date_str, flags=re.IGNORECASE)
        
        # Try to extract date components
        # Pattern: "15 Januari 2024" or "January 15, 2024"
        month_day_year = re.search(r'(\d{1,2})\s+(\w+)\s+(\d{4})', date_str)
        if month_day_year:
            day, month_str, year = month_day_year.groups()
            month_num = self.MONTH_MAPPINGS.get(month_str.lower())
            if month_num:
                try:
                    parsed_date = datetime(int(year), month_num, int(day))
                    return parsed_date.strftime('%B %d, %Y')
                except ValueError:
                    pass
        
        # Pattern: "January 15, 2024" or "Jan 15, 2024"
        month_day_year2 = re.search(r'(\w+)\s+(\d{1,2}),?\s+(\d{4})', date_str)
        if month_day_year2:
            month_str, day, year = month_day_year2.groups()
            month_num = self.MONTH_MAPPINGS.get(month_str.lower())
            if month_num:
                try:
                    parsed_date = datetime(int(year), month_num, int(day))
                    return parsed_date.strftime('%B %d, %Y')
                except ValueError:
                    pass
        
        return None

def enhance_scraper_date_extraction():
    """Function to patch existing scrapers with enhanced date extraction"""
    
    def enhanced_youtube_date_extraction(scraper_instance):
        """Enhanced date extraction for YouTube scraper"""
        extractor = EnhancedDateExtractor(scraper_instance.driver)
        return extractor.extract_date_youtube()
    
    def enhanced_facebook_date_extraction(scraper_instance):
        """Enhanced date extraction for Facebook scraper"""
        extractor = EnhancedDateExtractor(scraper_instance.driver)
        return extractor.extract_date_facebook()
    
    def enhanced_tiktok_date_extraction(scraper_instance):
        """Enhanced date extraction for TikTok scraper"""
        extractor = EnhancedDateExtractor(scraper_instance.driver)
        return extractor.extract_date_tiktok()
    
    return {
        'youtube': enhanced_youtube_date_extraction,
        'facebook': enhanced_facebook_date_extraction,
        'tiktok': enhanced_tiktok_date_extraction
    }

if __name__ == "__main__":
    print("Enhanced Date Extractor - Library untuk meningkatkan akurasi ekstraksi tanggal unggah")
    print("Gunakan fungsi enhance_scraper_date_extraction() untuk mengintegrasikan dengan scraper yang ada.")