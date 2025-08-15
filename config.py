import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Ollama Configuration
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama2')
    
    # CrewAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Social Media APIs (if available)
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')
    FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN', '')
    TIKTOK_API_KEY = os.getenv('TIKTOK_API_KEY', '')
    
    # Selenium Configuration
    SELENIUM_TIMEOUT = 30
    HEADLESS_BROWSER = True
    
    # Rate Limiting
    REQUEST_DELAY = 2  # seconds between requests
    MAX_RETRIES = 3
    
    # Supported Platforms
    SUPPORTED_PLATFORMS = ['youtube', 'tiktok', 'facebook']
    
    @classmethod
    def validate_config(cls):
        """Validate essential configuration"""
        if not cls.OLLAMA_BASE_URL:
            raise ValueError("OLLAMA_BASE_URL is required")
        return True