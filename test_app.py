#!/usr/bin/env python3
"""
SocialCount Test Suite
Basic tests for application components
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.url_detector import URLDetector
from scrapers.base_scraper import SocialMediaStats
from services.ollama_service import OllamaService
from config import Config

class TestURLDetector(unittest.TestCase):
    """Test URL detection and validation"""
    
    def test_youtube_url_detection(self):
        """Test YouTube URL detection"""
        test_urls = [
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'https://youtu.be/dQw4w9WgXcQ',
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=10s'
        ]
        
        for url in test_urls:
            with self.subTest(url=url):
                platform = URLDetector.detect_platform(url)
                self.assertEqual(platform, 'youtube')
    
    def test_tiktok_url_detection(self):
        """Test TikTok URL detection"""
        test_urls = [
            'https://www.tiktok.com/@user/video/1234567890123456789',
            'https://vm.tiktok.com/ZMexample/',
        ]
        
        for url in test_urls:
            with self.subTest(url=url):
                platform = URLDetector.detect_platform(url)
                self.assertEqual(platform, 'tiktok')
    
    def test_facebook_url_detection(self):
        """Test Facebook URL detection"""
        test_urls = [
            'https://www.facebook.com/watch/?v=1234567890123456',
            'https://fb.watch/example123/',
        ]
        
        for url in test_urls:
            with self.subTest(url=url):
                platform = URLDetector.detect_platform(url)
                self.assertEqual(platform, 'facebook')
    
    def test_invalid_url(self):
        """Test invalid URL handling"""
        invalid_urls = [
            'not-a-url',
            'https://example.com',
            'https://twitter.com/status/123',
            ''
        ]
        
        for url in invalid_urls:
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    URLDetector.detect_platform(url)
    
    def test_url_validation(self):
        """Test URL validation function"""
        valid_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        result = URLDetector.validate_url(valid_url)
        
        self.assertTrue(result['valid'])
        self.assertEqual(result['platform'], 'youtube')
        self.assertEqual(result['video_id'], 'dQw4w9WgXcQ')
        
        invalid_url = 'not-a-url'
        result = URLDetector.validate_url(invalid_url)
        
        self.assertFalse(result['valid'])
        self.assertIn('error', result)

class TestSocialMediaStats(unittest.TestCase):
    """Test SocialMediaStats data class"""
    
    def test_stats_creation(self):
        """Test creating stats object"""
        stats = SocialMediaStats(
            platform='youtube',
            url='https://example.com',
            views=1000,
            likes=100,
            comments=50
        )
        
        self.assertEqual(stats.platform, 'youtube')
        self.assertEqual(stats.views, 1000)
        self.assertEqual(stats.likes, 100)
        self.assertEqual(stats.comments, 50)
    
    def test_stats_to_dict(self):
        """Test converting stats to dictionary"""
        stats = SocialMediaStats(
            platform='youtube',
            url='https://example.com',
            views=1000
        )
        
        result = stats.to_dict()
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['platform'], 'youtube')
        self.assertEqual(result['views'], 1000)
        self.assertIn('url', result)

class TestOllamaService(unittest.TestCase):
    """Test Ollama service integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.service = OllamaService()
    
    @patch('requests.Session.get')
    def test_is_available_success(self, mock_get):
        """Test service availability check - success"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = self.service.is_available()
        self.assertTrue(result)
    
    @patch('requests.Session.get')
    def test_is_available_failure(self, mock_get):
        """Test service availability check - failure"""
        mock_get.side_effect = Exception("Connection error")
        
        result = self.service.is_available()
        self.assertFalse(result)
    
    @patch('requests.Session.get')
    def test_list_models(self, mock_get):
        """Test listing available models"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'models': [{'name': 'llama2'}, {'name': 'codellama'}]
        }
        mock_get.return_value = mock_response
        
        result = self.service.list_models()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'llama2')
    
    @patch('requests.Session.post')
    def test_generate_response(self, mock_post):
        """Test generating AI response"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'response': 'This is a test response'
        }
        mock_post.return_value = mock_response
        
        result = self.service.generate_response("Test prompt")
        self.assertEqual(result, 'This is a test response')
    
    def test_analyze_social_media_data(self):
        """Test social media data analysis"""
        with patch.object(self.service, 'generate_response') as mock_generate:
            mock_generate.return_value = "Analysis result"
            
            stats_data = {
                'platform': 'youtube',
                'views': 1000,
                'likes': 100
            }
            
            result = self.service.analyze_social_media_data(stats_data)
            self.assertEqual(result, "Analysis result")
            mock_generate.assert_called_once()

class TestConfig(unittest.TestCase):
    """Test configuration settings"""
    
    def test_config_attributes(self):
        """Test configuration attributes exist"""
        self.assertTrue(hasattr(Config, 'OLLAMA_BASE_URL'))
        self.assertTrue(hasattr(Config, 'OLLAMA_MODEL'))
        self.assertTrue(hasattr(Config, 'SUPPORTED_PLATFORMS'))
    
    def test_supported_platforms(self):
        """Test supported platforms list"""
        expected_platforms = ['youtube', 'tiktok', 'facebook']
        self.assertEqual(Config.SUPPORTED_PLATFORMS, expected_platforms)
    
    def test_validate_config(self):
        """Test configuration validation"""
        # Should not raise exception with default config
        try:
            Config.validate_config()
        except ValueError:
            self.fail("validate_config raised ValueError unexpectedly")

class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_url_to_platform_flow(self):
        """Test complete flow from URL to platform detection"""
        url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        
        # Validate URL
        url_info = URLDetector.validate_url(url)
        self.assertTrue(url_info['valid'])
        
        # Check platform
        platform = url_info['platform']
        self.assertIn(platform, Config.SUPPORTED_PLATFORMS)
    
    @patch('services.ollama_service.requests.Session')
    def test_service_health_check(self, mock_session):
        """Test service health check integration"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'models': [{'name': 'llama2'}]
        }
        
        mock_session_instance = Mock()
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance
        
        service = OllamaService()
        health = service.health_check()
        
        self.assertIn('service_available', health)
        self.assertIn('model_loaded', health)
        self.assertIn('models_available', health)

def run_tests():
    """Run all tests"""
    print("🧪 Running SocialCount Test Suite...\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestURLDetector,
        TestSocialMediaStats,
        TestOllamaService,
        TestConfig,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n📊 Test Results:")
    print(f"  • Tests run: {result.testsRun}")
    print(f"  • Failures: {len(result.failures)}")
    print(f"  • Errors: {len(result.errors)}")
    print(f"  • Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  • {test}: {traceback.split('AssertionError: ')[-1].split('\n')[0]}")
    
    if result.errors:
        print(f"\n🚨 Errors:")
        for test, traceback in result.errors:
            print(f"  • {test}: {traceback.split('\n')[-2]}")
    
    return len(result.failures) == 0 and len(result.errors) == 0

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)