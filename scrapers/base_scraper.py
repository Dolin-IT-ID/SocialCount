from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

@dataclass
class SocialMediaStats:
    """Data class for social media statistics"""
    platform: str
    url: str
    views: Optional[int] = None
    likes: Optional[int] = None
    shares: Optional[int] = None
    comments: Optional[int] = None
    title: Optional[str] = None
    author: Optional[str] = None
    upload_date: Optional[str] = None
    error: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            'platform': self.platform,
            'url': self.url,
            'views': self.views,
            'likes': self.likes,
            'shares': self.shares,
            'comments': self.comments,
            'title': self.title,
            'author': self.author,
            'upload_date': self.upload_date,
            'error': self.error
        }

class BaseScraper(ABC):
    """Base class for social media scrapers"""
    
    def __init__(self, headless: bool = True, timeout: int = 30):
        self.headless = headless
        self.timeout = timeout
        self.driver = None
    
    def setup_driver(self):
        """Setup Selenium WebDriver with optimized performance settings"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        
        # Performance optimizations
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')  # Faster loading
        # Note: JavaScript is required for YouTube, so not disabling it
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.set_page_load_timeout(self.timeout)
    
    def close_driver(self):
        """Close WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def wait_for_element(self, by, value, timeout=None):
        """Wait for element to be present"""
        timeout = timeout or self.timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    
    def safe_find_element(self, by, value):
        """Safely find element without throwing exception"""
        try:
            return self.driver.find_element(by, value)
        except:
            return None
    
    def extract_number(self, text: str) -> Optional[int]:
        """Extract number from text (handles K, M, B suffixes)"""
        if not text:
            return None
        
        # Remove non-numeric characters except K, M, B
        import re
        text = re.sub(r'[^0-9KMBkmb.,]', '', text.upper())
        
        if not text:
            return None
        
        try:
            # Handle suffixes
            multiplier = 1
            if 'K' in text:
                multiplier = 1000
                text = text.replace('K', '')
            elif 'M' in text:
                multiplier = 1000000
                text = text.replace('M', '')
            elif 'B' in text:
                multiplier = 1000000000
                text = text.replace('B', '')
            
            # Remove commas and convert to float
            number = float(text.replace(',', ''))
            return int(number * multiplier)
        except:
            return None
    
    @abstractmethod
    def scrape(self, url: str) -> SocialMediaStats:
        """Abstract method to scrape social media stats"""
        pass
    
    def __enter__(self):
        self.setup_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_driver()