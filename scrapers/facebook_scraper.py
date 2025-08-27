import time
import re
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .base_scraper import BaseScraper, SocialMediaStats

class FacebookScraper(BaseScraper):
    """Facebook post/video statistics scraper"""
    
    def scrape(self, url: str) -> SocialMediaStats:
        """Scrape Facebook post/video statistics"""
        stats = SocialMediaStats(platform='facebook', url=url)
        
        try:
            self.driver.get(url)
            time.sleep(5)  # Wait for Facebook to load
            
            # Handle Facebook login redirect or content loading
            try:
                # Wait for main content to load
                self.wait_for_element(By.CSS_SELECTOR, '[role="main"], .story_body_container', timeout=10)
            except:
                # If login required, try to find public content
                pass
            
            # Extract title/post content
            try:
                title_selectors = [
                    '[data-testid="post_message"]',
                    '.userContent',
                    '[data-ad-preview="message"]',
                    '.story_body_container p',
                    'div[data-testid="post_message"] span'
                ]
                
                for selector in title_selectors:
                    title_element = self.safe_find_element(By.CSS_SELECTOR, selector)
                    if title_element and title_element.text:
                        stats.title = title_element.text.strip()[:200]  # Limit length
                        break
            except:
                pass
            
            # Extract author/page name
            try:
                author_selectors = [
                    'h3 a[role="link"]',
                    '.actor a',
                    '[data-testid="story-subtitle"] a',
                    'strong a[role="link"]'
                ]
                
                for selector in author_selectors:
                    author_element = self.safe_find_element(By.CSS_SELECTOR, selector)
                    if author_element and author_element.text:
                        stats.author = author_element.text.strip()
                        break
            except:
                pass
            
            # Get page source once for both views and likes extraction
            import re
            page_source = self.driver.page_source
            
            # Extract view count (for videos)
            try:
                # First try to extract from visible text (user-facing display)
                # Look for elements containing view count in visible text
                all_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'view') or contains(text(), 'View')]") 
                
                for element in all_elements:
                    try:
                        text = element.text.strip()
                        # Look for pattern like "25 views" or "25 view"
                        view_match = re.search(r'(\d+)\s*views?', text, re.IGNORECASE)
                        if view_match:
                            stats.views = int(view_match.group(1))
                            break
                    except:
                        continue
                
                # Fallback to page source JSON data if visible text extraction fails
                if stats.views is None:
                    # Look for video view count in JSON data
                    view_patterns = [
                        r'"video_view_count":\s*(\d+)',
                        r'"view_count":\s*(\d+)',
                        r'"playCount":\s*(\d+)'
                    ]
                    
                    for pattern in view_patterns:
                        matches = re.findall(pattern, page_source)
                        if matches:
                            try:
                                stats.views = int(matches[0])
                                break
                            except (ValueError, IndexError):
                                continue
                
                # Final fallback to DOM selectors
                if stats.views is None:
                    view_selectors = [
                        '[data-testid="video_view_count"]',
                        '.video-view-count',
                        'span[aria-label*="view"]'
                    ]
                    
                    for selector in view_selectors:
                        view_element = self.safe_find_element(By.CSS_SELECTOR, selector)
                        if view_element:
                            view_text = view_element.get_attribute('aria-label') or view_element.text
                            if view_text:
                                stats.views = self.extract_number(view_text)
                                break
            except:
                pass
            
            # Extract likes/reactions
            try:
                # First try to extract from page source (most reliable for Facebook)
                # Look for reaction count in JSON data
                like_patterns = [
                    r'"reaction_count":\s*(\d+)',
                    r'"like_count":\s*(\d+)',
                    r'"likes":\s*(\d+)',
                    r'reaction_count["\']?:\s*(\d+)'
                ]
                
                for pattern in like_patterns:
                    matches = re.findall(pattern, page_source)
                    if matches:
                        try:
                            stats.likes = int(matches[0])
                            break
                        except (ValueError, IndexError):
                            continue
                
                # Fallback to DOM selectors if page source extraction fails
                if stats.likes is None:
                    like_selectors = [
                        '[data-testid="like_count"]',
                        'span[data-testid="like_count"]',
                        '.reaction-count',
                        'span[aria-label*="reaction"]'
                    ]
                    
                    for selector in like_selectors:
                        like_element = self.safe_find_element(By.CSS_SELECTOR, selector)
                        if like_element:
                            like_text = like_element.get_attribute('aria-label') or like_element.text
                            if like_text:
                                stats.likes = self.extract_number(like_text)
                                break
            except:
                pass
            
            # Extract shares
            try:
                share_selectors = [
                    '[data-testid="share_count"]',
                    'span[data-testid="share_count"]',
                    '.share-count',
                    'span[aria-label*="share"]'
                ]
                
                for selector in share_selectors:
                    share_element = self.safe_find_element(By.CSS_SELECTOR, selector)
                    if share_element:
                        share_text = share_element.get_attribute('aria-label') or share_element.text
                        if share_text:
                            stats.shares = self.extract_number(share_text)
                            break
            except:
                pass
            
            # Extract comments
            try:
                comment_selectors = [
                    '[data-testid="comment_count"]',
                    'span[data-testid="comment_count"]',
                    '.comment-count',
                    'span[aria-label*="comment"]'
                ]
                
                for selector in comment_selectors:
                    comment_element = self.safe_find_element(By.CSS_SELECTOR, selector)
                    if comment_element:
                        comment_text = comment_element.get_attribute('aria-label') or comment_element.text
                        if comment_text:
                            stats.comments = self.extract_number(comment_text)
                            break
            except:
                pass
            
            # Extract upload date with enhanced extraction
            try:
                # Try standard selectors first
                date_selectors = [
                    'abbr[data-utime]',
                    '[data-testid="story-subtitle"] a[role="link"]',
                    '.timestamp'
                ]
                
                upload_date = None
                for selector in date_selectors:
                    date_element = self.safe_find_element(By.CSS_SELECTOR, selector)
                    if date_element:
                        # Try data-utime attribute first (Unix timestamp)
                        if selector == 'abbr[data-utime]':
                            utime = date_element.get_attribute('data-utime')
                            if utime and utime.isdigit():
                                from datetime import datetime
                                timestamp = int(utime)
                                date_obj = datetime.fromtimestamp(timestamp)
                                upload_date = date_obj.strftime('%B %d, %Y')
                                break
                        
                        # Try title attribute or text
                        date_text = date_element.get_attribute('title') or date_element.text
                        if date_text:
                            upload_date = self._normalize_date(date_text.strip())
                            if upload_date:
                                break
                
                # If standard extraction failed, try enhanced extraction
                if not upload_date:
                    upload_date = self._enhanced_date_extraction_facebook()
                
                stats.upload_date = upload_date
            except:
                pass
                
        except TimeoutException:
            stats.error = "Timeout: Facebook page took too long to load"
        except Exception as e:
            stats.error = f"Error scraping Facebook: {str(e)}"
        
        return stats
    
    def extract_number(self, text: str) -> int:
        """Override to handle Facebook specific number formats"""
        if not text:
            return None
        
        # Facebook specific cleaning
        text = text.lower()
        text = re.sub(r'(views?|likes?|shares?|comments?|reactions?)', '', text)
        text = re.sub(r'[^0-9kmb.,]', '', text)
        
        return super().extract_number(text)
    
    def _enhanced_date_extraction_facebook(self):
        """Enhanced date extraction for Facebook with multiple strategies"""
        import re
        from datetime import datetime
        
        # Enhanced selectors for Facebook date extraction
        enhanced_selectors = [
            # Meta tags
            'meta[property="article:published_time"]',
            'meta[property="og:updated_time"]',
            'meta[name="publish_date"]',
            
            # Additional selectors
            'abbr[title]',
            '[data-testid="story-subtitle"] abbr',
            '.story_body_container abbr',
            '[data-testid="feed-story-ring"] abbr',
            '.userContentWrapper abbr',
            '.timestampContent',
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
                        # Try title attribute first, then text
                        date_text = element.get_attribute('title') or element.text
                        if date_text:
                            return self._normalize_date(date_text.strip())
            except:
                continue
        
        # Search in page source for date patterns
        try:
            page_source = self.driver.page_source
            
            # Date patterns to search for
            date_patterns = [
                r'"publish_time"\s*:\s*(\d+)',  # Unix timestamp
                r'"created_time"\s*:\s*"([^"]+)"',
                r'"updated_time"\s*:\s*"([^"]+)"',
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
                    if pattern.startswith(r'"publish_time"') and match.isdigit():
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