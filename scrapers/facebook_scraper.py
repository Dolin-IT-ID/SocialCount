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
            
            # Extract upload date
            try:
                date_selectors = [
                    'abbr[data-utime]',
                    '[data-testid="story-subtitle"] a[role="link"]',
                    '.timestamp'
                ]
                
                for selector in date_selectors:
                    date_element = self.safe_find_element(By.CSS_SELECTOR, selector)
                    if date_element:
                        date_text = date_element.get_attribute('title') or date_element.text
                        if date_text:
                            stats.upload_date = date_text.strip()
                            break
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