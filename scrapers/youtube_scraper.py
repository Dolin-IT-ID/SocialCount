import time
import re
import json
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .base_scraper import BaseScraper, SocialMediaStats

# Constants for better maintainability
class YouTubeSelectors:
    """CSS selectors for YouTube elements"""
    
    # Regular YouTube video selectors
    REGULAR_TITLE = 'h1.ytd-watch-metadata yt-formatted-string, h1.title.style-scope.ytd-video-primary-info-renderer'
    REGULAR_AUTHOR = '#owner #channel-name a, .ytd-channel-name a'
    REGULAR_VIEWS = [
        'span.yt-core-attributed-string:contains("views")',
        '.yt-core-attributed-string',
        '.view-count', 
        '#info-contents #count .view-count', 
        '.ytd-video-view-count-renderer', 
        'span.view-count'
    ]
    REGULAR_LIKES = [
        'button[aria-label*="like"] span',
        'button[aria-label*="suka"] span',
        '#top-level-buttons-computed button[aria-label*="like"] #text', 
        '.ytd-toggle-button-renderer #text', 
        'ytd-segmented-like-dislike-button-renderer button span',
        '#segmented-like-button button span'
    ]
    REGULAR_COMMENTS = ['#count .count-text', '.ytd-comments-header-renderer #count', '#comments #count span']
    
    # YouTube Shorts selectors
    SHORTS_TITLE = ['h1.ytd-reel-video-in-sequence-renderer', '.ytd-reel-video-in-sequence-renderer h1', 'h1[class*="reel"]', 'meta[property="og:title"]']
    SHORTS_AUTHOR = ['ytd-reel-player-header-renderer #channel-name a', '.reel-player-header-renderer #channel-name a', 
                     'ytd-reel-player-header-renderer .ytd-channel-name a', '.ytd-reel-video-in-sequence-renderer #channel-name a',
                     '.ytd-reel-video-in-sequence-renderer .ytd-channel-name a', 'a[class*="channel-name"]',
                     '[data-e2e="browse-username"]', 'meta[name="author"]', 'meta[property="og:video:tag"]']
    SHORTS_VIEWS = ['ytd-reel-player-header-renderer .view-count', '.reel-player-header-renderer .view-count',
                    'ytd-reel-video-in-sequence-renderer .view-count', '.ytd-reel-video-in-sequence-renderer .view-count',
                    'span[class*="view-count"]', '.view-count']
    SHORTS_NUMBERS = 'span.yt-core-attributed-string'
    
    # Common selectors
    UPLOAD_DATE = '#info-strings yt-formatted-string, .ytd-video-secondary-info-renderer #date'
    SHORTS_CONTAINER = 'ytd-reel-video-in-sequence-renderer, ytd-reel-player-header-renderer'
    
    # Upload date selectors
    REGULAR_UPLOAD_DATE = ['#info-strings yt-formatted-string', '.ytd-video-secondary-info-renderer #date']
    SHORTS_UPLOAD_DATE = ['.ytd-reel-player-header-renderer .published-time-text', '.reel-player-header-renderer .published-time-text', 'span[class*="published-time"]', '.published-time-text']

# Timing constants
class YouTubeTiming:
    """Timing constants for YouTube scraping"""
    PAGE_LOAD_WAIT = 5
    SHORTS_LOAD_WAIT = 8
    SHORTS_FALLBACK_WAIT = 2
    COMMENTS_SCROLL_WAIT = 2
    ELEMENT_TIMEOUT = 10
    SHORTS_ELEMENT_TIMEOUT = 5

class YouTubeScraper(BaseScraper):
    """YouTube video statistics scraper with enhanced maintainability"""
    
    def _extract_with_selectors(self, selectors, is_meta=False, attribute='content'):
        """Helper method to extract data using multiple selectors"""
        if isinstance(selectors, str):
            selectors = [selectors]
            
        for selector in selectors:
            try:
                if is_meta and selector.startswith('meta'):
                    element = self.safe_find_element(By.CSS_SELECTOR, selector)
                    if element:
                        content = element.get_attribute(attribute)
                        if content and content.strip():
                            return content.strip()
                else:
                    element = self.safe_find_element(By.CSS_SELECTOR, selector)
                    if element and element.text and element.text.strip():
                        return element.text.strip()
            except Exception as e:
                continue
        return None
    
    def _extract_shorts_numbers(self):
        """Extract likes and comments from YouTube Shorts number spans"""
        likes, comments = None, None
        try:
            spans = self.driver.find_elements(By.CSS_SELECTOR, YouTubeSelectors.SHORTS_NUMBERS)
            for span in spans:
                text = span.text.strip()
                if text and ('K' in text or 'M' in text) and any(char.isdigit() for char in text):
                    if not likes:  # First number as likes
                        likes = self.extract_number(text)
                    elif not comments:  # Second number as comments
                        comments = self.extract_number(text)
                        break
        except:
            pass
        return likes, comments
    
    def _wait_for_shorts_load(self):
        """Optimized waiting for YouTube Shorts to load"""
        time.sleep(YouTubeTiming.SHORTS_LOAD_WAIT)
        try:
            self.wait_for_element(By.CSS_SELECTOR, YouTubeSelectors.SHORTS_CONTAINER, timeout=YouTubeTiming.SHORTS_ELEMENT_TIMEOUT)
        except:
            time.sleep(YouTubeTiming.SHORTS_FALLBACK_WAIT)
    
    def scrape(self, url: str) -> SocialMediaStats:
        """Scrape YouTube video statistics"""
        stats = SocialMediaStats(platform='youtube', url=url)
        
        try:
            self.driver.get(url)
            time.sleep(YouTubeTiming.PAGE_LOAD_WAIT)
            
            # Check if this is a YouTube Shorts URL
            is_shorts = '/shorts/' in url
            
            if is_shorts:
                self._wait_for_shorts_load()
            else:
                # Wait for regular video player to load
                self.wait_for_element(By.ID, 'movie_player', timeout=YouTubeTiming.ELEMENT_TIMEOUT)
            
            # Extract title
            try:
                if is_shorts:
                    stats.title = self._extract_with_selectors(YouTubeSelectors.SHORTS_TITLE, is_meta=True)
                else:
                    # Regular YouTube video title
                    title_element = self.wait_for_element(
                        By.CSS_SELECTOR, 
                        YouTubeSelectors.REGULAR_TITLE,
                        timeout=5
                    )
                    stats.title = title_element.text.strip()
            except:
                pass
            
            # Extract author/channel name
            try:
                if is_shorts:
                    stats.author = self._extract_with_selectors(YouTubeSelectors.SHORTS_AUTHOR, is_meta=True)
                else:
                    # Regular YouTube video author
                    stats.author = self._extract_with_selectors([YouTubeSelectors.REGULAR_AUTHOR])
            except:
                pass
            
            # Extract view count
            try:
                if is_shorts:
                    view_text = self._extract_with_selectors(YouTubeSelectors.SHORTS_VIEWS)
                    if view_text and 'view' in view_text.lower():
                        stats.views = self.extract_number(view_text)
                else:
                    # Regular YouTube video views - try multiple approaches
                    view_text = None
                    
                    # First try: Look for main video views in metadata area
                    try:
                        # Look for views in metadata area first (most accurate)
                        metadata_views = self.driver.find_elements(By.XPATH, '//div[contains(@class, "metadata")]//span[contains(text(), "views") or contains(text(), "ditonton")]')
                        if metadata_views:
                            view_text = metadata_views[0].text.strip()
                        else:
                            # Fallback: Look for any views with yt-core-attributed-string class
                            core_views = self.driver.find_elements(By.XPATH, '//span[contains(@class, "yt-core-attributed-string") and (contains(text(), "views") or contains(text(), "ditonton"))]')
                            if core_views:
                                # Get the first one that looks like main video views (usually has higher count)
                                for element in core_views:
                                    text = element.text.strip()
                                    if text:
                                        # Extract number to check if it's reasonable for main video
                                        number = self.extract_number(text)
                                        if number and number > 1000:  # Main videos usually have >1K views
                                            view_text = text
                                            break
                                # If no high-count views found, use the first one
                                if not view_text and core_views:
                                    view_text = core_views[0].text.strip()
                    except:
                        pass
                    
                    # Second try: Use CSS selectors
                    if not view_text:
                        view_text = self._extract_with_selectors(YouTubeSelectors.REGULAR_VIEWS)
                    
                    # Third try: Look for yt-core-attributed-string elements
                    if not view_text:
                        try:
                            core_elements = self.driver.find_elements(By.CSS_SELECTOR, '.yt-core-attributed-string')
                            for element in core_elements:
                                text = element.text.strip()
                                if text and ('view' in text.lower() or 'ditonton' in text.lower()):
                                    # Check if this is in the main video metadata area
                                    try:
                                        parent = element.find_element(By.XPATH, '../..')
                                        parent_classes = parent.get_attribute('class') or ''
                                        if 'metadata' in parent_classes.lower() or 'primary' in parent_classes.lower():
                                            view_text = text
                                            break
                                    except:
                                        # If we can't check parent, use the first views text we find
                                        if not view_text:
                                            view_text = text
                        except:
                            pass
                    
                    if view_text:
                        stats.views = self.extract_number(view_text)
            except:
                pass
            
            # Extract likes and comments
            try:
                if is_shorts:
                    # For YouTube Shorts, use helper method
                    likes, comments = self._extract_shorts_numbers()
                    stats.likes = likes
                    stats.comments = comments
                else:
                    # Regular YouTube video likes - try multiple approaches
                    like_text = None
                    
                    # First try: Look for like buttons and extract from aria-label or button text
                    try:
                        like_buttons = self.driver.find_elements(By.XPATH, '//button[contains(@aria-label, "like") or contains(@aria-label, "suka")]')
                        for button in like_buttons:
                            try:
                                # First check button text directly
                                button_text = button.text.strip()
                                if button_text and any(c.isdigit() for c in button_text):
                                    like_text = button_text
                                    break
                                
                                # Then check aria-label for like count
                                aria_label = button.get_attribute('aria-label') or ''
                                if 'like' in aria_label.lower() and any(c.isdigit() for c in aria_label):
                                    # Extract number from aria-label like "like this video along with 608 other people"
                                    import re
                                    numbers = re.findall(r'\d+', aria_label)
                                    if numbers:
                                        like_text = numbers[0]  # Take the first number found
                                        break
                                
                                # Finally check span elements within the button
                                spans = button.find_elements(By.TAG_NAME, 'span')
                                for span in spans:
                                    text = span.text.strip()
                                    if text and any(c.isdigit() for c in text):
                                        like_text = text
                                        break
                                if like_text:
                                    break
                            except:
                                continue
                    except:
                        pass
                    
                    # Second try: Use CSS selectors
                    if not like_text:
                        like_text = self._extract_with_selectors(YouTubeSelectors.REGULAR_LIKES)
                    
                    # Third try: Look for segmented like button
                    if not like_text:
                        try:
                            segmented_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'ytd-segmented-like-dislike-button-renderer button')
                            for button in segmented_buttons:
                                aria_label = button.get_attribute('aria-label') or ''
                                if 'like' in aria_label.lower() or 'suka' in aria_label.lower():
                                    spans = button.find_elements(By.TAG_NAME, 'span')
                                    for span in spans:
                                        text = span.text.strip()
                                        if text and any(c.isdigit() for c in text):
                                            like_text = text
                                            break
                                    if like_text:
                                        break
                        except:
                            pass
                    
                    if like_text:
                        stats.likes = self.extract_number(like_text)
                    
                    # Scroll down to load comments section for regular videos
                    self.driver.execute_script("window.scrollTo(0, 1000);")
                    time.sleep(YouTubeTiming.COMMENTS_SCROLL_WAIT)
                    
                    # Regular YouTube video comments
                    comment_text = self._extract_with_selectors(YouTubeSelectors.REGULAR_COMMENTS)
                    if comment_text:
                        stats.comments = self.extract_number(comment_text)
            except:
                pass
            
            # YouTube doesn't have direct share count, set to None
            stats.shares = None
            
            # Extract upload date with enhanced extraction
            try:
                if is_shorts:
                    stats.upload_date = self._extract_with_selectors(YouTubeSelectors.SHORTS_UPLOAD_DATE)
                else:
                    # Regular YouTube video upload date
                    stats.upload_date = self._extract_with_selectors(YouTubeSelectors.REGULAR_UPLOAD_DATE)
                
                # If standard extraction failed, try enhanced extraction
                if not stats.upload_date:
                    stats.upload_date = self._enhanced_date_extraction()
            except:
                pass
                
        except TimeoutException:
            stats.error = "Timeout: Page took too long to load"
        except Exception as e:
            import traceback
            stats.error = f"Error scraping YouTube: {str(e)}\nTraceback: {traceback.format_exc()}"
        
        return stats
    
    def _enhanced_date_extraction(self):
        """Enhanced date extraction with multiple strategies"""
        # Enhanced selectors for YouTube date extraction
        enhanced_selectors = [
            # Meta tags
            'meta[property="video:release_date"]',
            'meta[property="article:published_time"]',
            'meta[name="uploadDate"]',
            'meta[itemprop="uploadDate"]',
            
            # JSON-LD structured data
            'script[type="application/ld+json"]',
            
            # Additional selectors
            '.ytd-video-meta-block span',
            '#info-text span',
            '.ytd-video-secondary-info-renderer span',
            '#upload-info span',
            '.upload-date',
            '.publish-date'
        ]
        
        # Try enhanced selectors
        for selector in enhanced_selectors:
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
                            data = json.loads(script.get_attribute('innerHTML'))
                            if isinstance(data, dict) and 'uploadDate' in data:
                                return self._normalize_date(data['uploadDate'])
                            elif isinstance(data, list):
                                for item in data:
                                    if isinstance(item, dict) and 'uploadDate' in item:
                                        return self._normalize_date(item['uploadDate'])
                        except:
                            continue
                else:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element and element.text:
                        date_text = element.text.strip()
                        if self._is_date_like(date_text):
                            return self._normalize_date(date_text)
            except:
                continue
        
        # Search in page source for date patterns
        return self._extract_from_page_source()
    
    def _is_date_like(self, text):
        """Check if text looks like a date"""
        if not text or len(text) < 4:
            return False
        
        # Check for common date patterns
        date_patterns = [
            r'\d{4}',  # Year
            r'\w+\s+\d{1,2}',  # Month Day
            r'\d{1,2}\s+\w+',  # Day Month
            r'\d+\s+(day|week|month|year|hari|minggu|bulan|tahun)s?\s+(ago|lalu)',  # Relative time
        ]
        
        for pattern in date_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def _extract_from_page_source(self):
        """Extract date from page source using regex patterns"""
        try:
            page_source = self.driver.page_source
            
            # Date patterns to search for
            date_patterns = [
                r'"uploadDate"\s*:\s*"([^"]+)"',
                r'"publishedTimeText"\s*:\s*{[^}]*"simpleText"\s*:\s*"([^"]+)"',
                r'"dateText"\s*:\s*{[^}]*"simpleText"\s*:\s*"([^"]+)"',
                r'(\w+\s+\d{1,2},\s+\d{4})',  # Jan 15, 2024
                r'(\d{1,2}\s+\w+\s+\d{4})',   # 15 Jan 2024
                r'(\d{4}-\d{2}-\d{2})',       # 2024-01-15
                r'(\d+)\s+(day|week|month|year)s?\s+ago',  # Relative time
                r'(\d+)\s+(hari|minggu|bulan|tahun)\s+yang\s+lalu',  # Indonesian relative time
            ]
            
            for pattern in date_patterns:
                matches = re.findall(pattern, page_source, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0] if match[0] else ' '.join(match)
                    
                    normalized = self._normalize_date(match)
                    if normalized and normalized != match:  # Only return if successfully normalized
                        return normalized
        except:
            pass
        
        return None
    
    def _normalize_date(self, date_str):
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
        
        # Handle ISO 8601 format with timezone (e.g., "2023-01-30T02:34:17-08:00")
        iso_match = re.match(r'(\d{4}-\d{2}-\d{2})T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}', date_str)
        if iso_match:
            try:
                # Extract just the date part and parse it
                date_part = iso_match.group(1)
                parsed_date = datetime.strptime(date_part, '%Y-%m-%d')
                return parsed_date.strftime('%B %d, %Y')
            except ValueError:
                pass
        
        # Try to parse various date formats
        date_formats = [
            '%Y-%m-%d',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%dT%H:%M:%S%z',  # With timezone
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
        
        # If all else fails, return the original string if it looks like a date
        if self._is_date_like(date_str):
            return date_str
        
        return None
    
    def _convert_relative_time(self, amount, unit):
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
    
    def _convert_relative_time_indonesian(self, amount, unit):
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

    def extract_number(self, text: str) -> int:
        """Override to handle YouTube specific number formats"""
        if not text:
            return None
        
        # YouTube specific patterns
        text = text.lower().replace('views', '').replace('likes', '').replace('comments', '')
        text = re.sub(r'[^0-9kmb.,]', '', text)
        
        return super().extract_number(text)