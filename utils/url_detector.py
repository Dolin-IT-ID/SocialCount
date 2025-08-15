import re
import validators
from urllib.parse import urlparse

class URLDetector:
    """Utility class to detect social media platform from URL"""
    
    PLATFORM_PATTERNS = {
        'youtube': [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([\w-]+)',
            r'youtube\.com/.*[?&]v=([\w-]+)',
        ],
        'tiktok': [
            r'tiktok\.com/@[\w.-]+/video/(\d+)',
            r'vm\.tiktok\.com/([\w-]+)',
            r'tiktok\.com/t/([\w-]+)',
        ],
        'facebook': [
            r'facebook\.com/.*/(?:posts|videos)/(\d+)',
            r'fb\.watch/([\w-]+)',
            r'facebook\.com/watch/\?v=(\d+)',
            r'facebook\.com/share/v/([\w-]+)',
        ]
    }
    
    @classmethod
    def detect_platform(cls, url: str) -> str:
        """Detect social media platform from URL"""
        if not validators.url(url):
            raise ValueError("Invalid URL format")
        
        url_lower = url.lower()
        
        for platform, patterns in cls.PLATFORM_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, url_lower):
                    return platform
        
        raise ValueError("Unsupported social media platform")
    
    @classmethod
    def extract_video_id(cls, url: str, platform: str) -> str:
        """Extract video/post ID from URL"""
        patterns = cls.PLATFORM_PATTERNS.get(platform, [])
        
        for pattern in patterns:
            match = re.search(pattern, url.lower())
            if match:
                return match.group(1)
        
        raise ValueError(f"Could not extract ID from {platform} URL")
    
    @classmethod
    def validate_url(cls, url: str) -> dict:
        """Validate URL and return platform info"""
        try:
            platform = cls.detect_platform(url)
            video_id = cls.extract_video_id(url, platform)
            
            return {
                'valid': True,
                'platform': platform,
                'video_id': video_id,
                'original_url': url
            }
        except Exception as e:
            return {
                'valid': False,
                'error': str(e),
                'original_url': url
            }
    
    @classmethod
    def get_canonical_url(cls, url: str, platform: str, video_id: str) -> str:
        """Get canonical URL for the platform"""
        canonical_urls = {
            'youtube': f'https://www.youtube.com/watch?v={video_id}',
            'tiktok': f'https://www.tiktok.com/video/{video_id}',
            'facebook': f'https://www.facebook.com/watch/?v={video_id}'
        }
        
        return canonical_urls.get(platform, url)