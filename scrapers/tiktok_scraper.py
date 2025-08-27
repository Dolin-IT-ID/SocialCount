import time
import re
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .base_scraper import BaseScraper, SocialMediaStats

class TikTokScraper(BaseScraper):
    """TikTok video statistics scraper"""
    
    def setup_driver(self):
        """Setup Selenium WebDriver with TikTok-specific optimizations"""
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium import webdriver
        
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        
        # TikTok-specific optimizations
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Additional performance optimizations
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.set_page_load_timeout(45)  # Increased timeout for TikTok
        
        # Execute script to remove webdriver property
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    def scrape(self, url: str) -> SocialMediaStats:
        """Scrape TikTok video statistics"""
        stats = SocialMediaStats(platform='tiktok', url=url)
        
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                self.driver.get(url)
                time.sleep(8)  # Increased initial wait time
                
                # Wait for video container to load with increased timeout
                # Try multiple selectors for better compatibility
                video_selectors = [
                    '[data-e2e="video-player"]',
                    '.video-player',
                    '[data-e2e="browse-video"]',
                    '.browse-video',
                    'video',
                    '.video-card'
                ]
                
                element_found = False
                for selector in video_selectors:
                    try:
                        self.wait_for_element(By.CSS_SELECTOR, selector, timeout=10)
                        element_found = True
                        break
                    except TimeoutException:
                        continue
                
                if element_found:
                    break  # Success, exit retry loop
                else:
                    raise TimeoutException("No video elements found")
                
            except TimeoutException:
                retry_count += 1
                if retry_count >= max_retries:
                    stats.error = f"Timeout: TikTok page took too long to load after {max_retries} attempts"
                    return stats
                time.sleep(3)  # Wait before retry
                continue
        
        try:
            
            # Extract title/description
            try:
                title_selectors = [
                    '[data-e2e="video-desc"]',
                    '.video-meta-caption',
                    '.tt-video-meta-caption',
                    'h1[data-e2e="video-desc"]'
                ]
                
                for selector in title_selectors:
                    title_element = self.safe_find_element(By.CSS_SELECTOR, selector)
                    if title_element and title_element.text:
                        stats.title = title_element.text.strip()
                        break
            except:
                pass
            
            # Extract author/username
            try:
                author_selectors = [
                    '[data-e2e="video-author-uniqueid"]',
                    '.author-uniqueid',
                    'h3[data-e2e="video-author-uniqueid"]',
                    '.username'
                ]
                
                for selector in author_selectors:
                    author_element = self.safe_find_element(By.CSS_SELECTOR, selector)
                    if author_element and author_element.text:
                        stats.author = author_element.text.strip().replace('@', '')
                        break
            except:
                pass
            
            # Extract view count
            try:
                # First try to extract from page source (most reliable for TikTok)
                page_source = self.driver.page_source
                import re
                
                # Look for playCount in JSON data
                play_count_patterns = [
                    r'"playCount":\s*"?(\d+)"?',
                    r'"stats":\s*{[^}]*"playCount":\s*(\d+)',
                    r'"viewCount":\s*"?(\d+)"?'
                ]
                
                for pattern in play_count_patterns:
                    matches = re.findall(pattern, page_source)
                    if matches:
                        try:
                            stats.views = int(matches[0])
                            break
                        except (ValueError, IndexError):
                            continue
                
                # Fallback to DOM selectors if page source extraction fails
                if stats.views is None:
                    view_selectors = [
                        '[data-e2e="video-views"]',
                        '.video-count',
                        '.playback-count'
                    ]
                    
                    for selector in view_selectors:
                        view_element = self.safe_find_element(By.CSS_SELECTOR, selector)
                        if view_element and view_element.text:
                            view_text = view_element.text
                            stats.views = self.extract_number(view_text)
                            break
            except:
                pass
            
            # Extract likes
            try:
                like_selectors = [
                    '[data-e2e="like-count"]',
                    '[data-e2e="video-like-count"]',
                    '.like-count',
                    'strong[data-e2e="like-count"]'
                ]
                
                for selector in like_selectors:
                    like_element = self.safe_find_element(By.CSS_SELECTOR, selector)
                    if like_element and like_element.text:
                        like_text = like_element.text
                        stats.likes = self.extract_number(like_text)
                        break
            except:
                pass
            
            # Extract shares
            try:
                share_selectors = [
                    '[data-e2e="share-count"]',
                    '[data-e2e="video-share-count"]',
                    '.share-count',
                    'strong[data-e2e="share-count"]'
                ]
                
                for selector in share_selectors:
                    share_element = self.safe_find_element(By.CSS_SELECTOR, selector)
                    if share_element and share_element.text:
                        share_text = share_element.text
                        stats.shares = self.extract_number(share_text)
                        break
            except:
                pass
            
            # Extract comments
            try:
                comment_selectors = [
                    '[data-e2e="comment-count"]',
                    '[data-e2e="video-comment-count"]',
                    '.comment-count',
                    'strong[data-e2e="comment-count"]'
                ]
                
                for selector in comment_selectors:
                    comment_element = self.safe_find_element(By.CSS_SELECTOR, selector)
                    if comment_element and comment_element.text:
                        comment_text = comment_element.text
                        stats.comments = self.extract_number(comment_text)
                        break
            except:
                pass
            
            # Extract upload date (if available)
            upload_date = None
            date_selectors = ['.video-meta-date', '[data-e2e="video-date"]']
            for selector in date_selectors:
                try:
                    date_element = self.safe_find_element(By.CSS_SELECTOR, selector)
                    if date_element:
                        date_text = date_element.text.strip()
                        if date_text:
                            upload_date = self._normalize_date(date_text)
                            if upload_date:
                                break
                except Exception as e:
                    continue
            
            # Fallback to enhanced date extraction if standard extraction fails
            if not upload_date:
                upload_date = self._enhanced_date_extraction_tiktok()
            
            stats.upload_date = upload_date
                
        except TimeoutException:
            stats.error = "Timeout: TikTok page took too long to load"
        except Exception as e:
            stats.error = f"Error scraping TikTok: {str(e)}"
        
        return stats
    
    def extract_number(self, text: str) -> int:
        """Override to handle TikTok specific number formats"""
        if not text:
            return None
        
        # TikTok specific cleaning
        text = text.lower().replace('views', '').replace('likes', '').replace('shares', '').replace('comments', '')
        text = re.sub(r'[^0-9kmb.,]', '', text)
        
        return super().extract_number(text)
    
    def _enhanced_date_extraction_tiktok(self):
        """Enhanced date extraction for TikTok with multiple strategies"""
        import re
        from datetime import datetime
        
        # Enhanced selectors for TikTok date extraction
        enhanced_selectors = [
            # Meta tags
            'meta[property="video:release_date"]',
            'meta[property="article:published_time"]',
            'meta[name="publish_date"]',
            
            # TikTok specific selectors
            '[data-e2e="video-date"]',
            '.video-meta-date',
            '[data-e2e="video-desc"] span[data-e2e="video-published-date"]',
            '.video-info-detail span[data-e2e="video-published-date"]',
            '.video-card-big-info span[data-e2e="video-published-date"]',
            '.video-feed-item-wrapper span[data-e2e="video-published-date"]',
            '.video-meta-info .date',
            '.video-card .date',
            'time[datetime]'
        ]
        
        # Try enhanced selectors
        for selector in enhanced_selectors:
            try:
                if selector.startswith('meta'):
                    element = self.safe_find_element(By.CSS_SELECTOR, selector)
                    if element:
                        date_value = element.get_attribute('content')
                        if date_value:
                            return self._normalize_date(date_value)
                elif selector == 'time[datetime]':
                    element = self.safe_find_element(By.CSS_SELECTOR, selector)
                    if element:
                        datetime_value = element.get_attribute('datetime')
                        if datetime_value:
                            return self._normalize_date(datetime_value)
                else:
                    element = self.safe_find_element(By.CSS_SELECTOR, selector)
                    if element:
                        date_text = element.text.strip()
                        if date_text:
                            return self._normalize_date(date_text)
            except:
                continue
        
        # Search in page source for date patterns
        try:
            page_source = self.driver.page_source
            
            # Date patterns to search for
            date_patterns = [
                r'"createTime"\s*:\s*(\d+)',  # Unix timestamp
                r'"publishTime"\s*:\s*(\d+)',  # Unix timestamp
                r'"uploadDate"\s*:\s*"([^"]+)"',
                r'"datePublished"\s*:\s*"([^"]+)"',
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
                    
                    # Handle Unix timestamp
                    if (pattern.startswith(r'"createTime"') or pattern.startswith(r'"publishTime"')) and match.isdigit():
                        try:
                            timestamp = int(match)
                            date_obj = datetime.fromtimestamp(timestamp)
                            return date_obj.strftime('%B %d, %Y')
                        except:
                            continue
                    
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
        
        import re
        from datetime import datetime, timedelta
        
        date_str = date_str.strip()
        
        # Handle ISO 8601 format with timezone (e.g., "2023-01-30T02:34:17-08:00")
        if 'T' in date_str and (':' in date_str[-6:] or date_str.endswith('Z')):
            try:
                # Extract just the date part and parse it
                date_part = date_str.split('T')[0]
                date_obj = datetime.strptime(date_part, '%Y-%m-%d')
                return date_obj.strftime('%B %d, %Y')
            except:
                pass
        
        # Try various date formats
        date_formats = [
            '%B %d, %Y',      # October 24, 2009
            '%d %B %Y',       # 24 October 2009
            '%Y-%m-%d',       # 2009-10-24
            '%d/%m/%Y',       # 24/10/2009
            '%m/%d/%Y',       # 10/24/2009
            '%Y-%m-%dT%H:%M:%S%z',  # ISO 8601 with timezone
            '%Y-%m-%dT%H:%M:%SZ',   # ISO 8601 UTC
            '%Y-%m-%dT%H:%M:%S',    # ISO 8601 without timezone
        ]
        
        for fmt in date_formats:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime('%B %d, %Y')
            except ValueError:
                continue
        
        # Handle relative time (e.g., "2 days ago", "1 week ago")
        relative_match = re.match(r'(\d+)\s+(second|minute|hour|day|week|month|year)s?\s+ago', date_str, re.IGNORECASE)
        if relative_match:
            return self._convert_relative_time(relative_match.group(1), relative_match.group(2))
        
        # Handle Indonesian relative time
        indonesian_match = re.match(r'(\d+)\s+(detik|menit|jam|hari|minggu|bulan|tahun)\s+yang\s+lalu', date_str, re.IGNORECASE)
        if indonesian_match:
            return self._convert_relative_time_indonesian(indonesian_match.group(1), indonesian_match.group(2))
        
        return date_str  # Return original if no format matches
    
    def _convert_relative_time(self, amount, unit):
        """Convert relative time to absolute date"""
        try:
            from datetime import datetime, timedelta
            amount = int(amount)
            now = datetime.now()
            
            if unit.lower().startswith('second'):
                date_obj = now - timedelta(seconds=amount)
            elif unit.lower().startswith('minute'):
                date_obj = now - timedelta(minutes=amount)
            elif unit.lower().startswith('hour'):
                date_obj = now - timedelta(hours=amount)
            elif unit.lower().startswith('day'):
                date_obj = now - timedelta(days=amount)
            elif unit.lower().startswith('week'):
                date_obj = now - timedelta(weeks=amount)
            elif unit.lower().startswith('month'):
                date_obj = now - timedelta(days=amount * 30)  # Approximate
            elif unit.lower().startswith('year'):
                date_obj = now - timedelta(days=amount * 365)  # Approximate
            else:
                return None
            
            return date_obj.strftime('%B %d, %Y')
        except:
            return None
    
    def _convert_relative_time_indonesian(self, amount, unit):
        """Convert Indonesian relative time to absolute date"""
        try:
            from datetime import datetime, timedelta
            amount = int(amount)
            now = datetime.now()
            
            unit_mapping = {
                'detik': 'seconds',
                'menit': 'minutes', 
                'jam': 'hours',
                'hari': 'days',
                'minggu': 'weeks',
                'bulan': 'months',
                'tahun': 'years'
            }
            
            english_unit = unit_mapping.get(unit.lower())
            if english_unit:
                return self._convert_relative_time(str(amount), english_unit)
            
            return None
        except:
            return None