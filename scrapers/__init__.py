from .base_scraper import BaseScraper, SocialMediaStats
from .youtube_scraper import YouTubeScraper
from .tiktok_scraper import TikTokScraper
from .facebook_scraper import FacebookScraper

class ScraperFactory:
    """Factory class to create appropriate scraper based on platform"""
    
    SCRAPERS = {
        'youtube': YouTubeScraper,
        'tiktok': TikTokScraper,
        'facebook': FacebookScraper
    }
    
    @classmethod
    def create_scraper(cls, platform: str, **kwargs) -> BaseScraper:
        """Create scraper instance for the given platform"""
        if platform not in cls.SCRAPERS:
            raise ValueError(f"Unsupported platform: {platform}")
        
        scraper_class = cls.SCRAPERS[platform]
        return scraper_class(**kwargs)
    
    @classmethod
    def get_supported_platforms(cls):
        """Get list of supported platforms"""
        return list(cls.SCRAPERS.keys())

__all__ = [
    'BaseScraper',
    'SocialMediaStats', 
    'YouTubeScraper',
    'TikTokScraper',
    'FacebookScraper',
    'ScraperFactory'
]