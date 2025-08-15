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
            try:
                date_element = self.safe_find_element(
                    By.CSS_SELECTOR,
                    '.video-meta-date, [data-e2e="video-date"]'
                )
                if date_element:
                    stats.upload_date = date_element.text.strip()
            except:
                pass
                
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