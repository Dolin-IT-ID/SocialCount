#!/usr/bin/env python3
"""
VLM Metrics Analyzer - Analisis Visual untuk Akurasi Metrics Video
Menggunakan Vision-Language Model untuk memverifikasi dan meningkatkan akurasi
pencatatan jumlah like, komentar, view, dan share dari screenshot halaman video.

Author: Social Media Scraper
Date: 2024
"""

import base64
import json
import re
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime
import logging
from dataclasses import dataclass

# Import services
from services.ollama_service import OllamaService

# Setup logging with more detailed configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Set specific log levels for different components
logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('requests').setLevel(logging.WARNING)

@dataclass
class MetricAnalysis:
    """Data class untuk hasil analisis metric"""
    metric_name: str
    scraped_value: Optional[int]
    vlm_detected_value: Optional[int]
    confidence_score: float
    is_verified: bool
    discrepancy_ratio: Optional[float]
    final_value: Optional[int]
    notes: str

@dataclass
class VLMAnalysisResult:
    """Data class untuk hasil lengkap analisis VLM"""
    screenshot_taken: bool
    analysis_successful: bool
    metrics: Dict[str, MetricAnalysis]
    overall_confidence: float
    platform_detected: str
    timestamp: str
    error_message: Optional[str] = None

class VLMMetricsAnalyzer:
    """Analyzer untuk metrics video menggunakan VLM"""
    
    def __init__(self):
        self.ollama_service = None
        self.setup_vlm_service()
        
        # Threshold untuk confidence scoring
        self.confidence_thresholds = {
            'high': 0.8,
            'medium': 0.6,
            'low': 0.4
        }
        
        # Pattern untuk ekstraksi angka dari teks VLM
        self.number_patterns = [
            r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?[KMBkmb]?)',  # Format dengan koma
            r'(\d+(?:\.\d+)?[KMBkmb])',  # Format dengan K/M/B
            r'(\d+)',  # Angka biasa
        ]
    
    def setup_vlm_service(self) -> bool:
        """Setup VLM service"""
        try:
            self.ollama_service = OllamaService()
            health = self.ollama_service.health_check()
            return health.get('service_available', False)
        except Exception as e:
            logger.error(f"Error setting up VLM service: {e}")
            return False
    
    def capture_screenshot_with_playwright(self, url: str) -> Optional[str]:
        """Capture screenshot menggunakan Selenium sebagai fallback"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            import base64
            import time
            
            # Setup Chrome options
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1280,720')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--allow-running-insecure-content')
            
            # Setup driver service
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            try:
                # Navigate to URL
                driver.get(url)
                
                # Wait for page to load
                time.sleep(3)
                
                # Take screenshot
                screenshot_base64 = driver.get_screenshot_as_base64()
                
                logger.info(f"Screenshot captured successfully for {url}")
                return screenshot_base64
                
            finally:
                driver.quit()
                
        except Exception as e:
            logger.error(f"Error capturing screenshot with Selenium: {e}")
            # Fallback: return None untuk disable VLM analysis
            logger.warning("VLM screenshot capture disabled due to browser compatibility issues")
            return None
    
    def analyze_metrics_from_screenshot(self, screenshot_base64: str, platform: str) -> Dict[str, Any]:
        """Analisis metrics dari screenshot menggunakan VLM"""
        logger.info(f"Starting VLM analysis for platform: {platform}")
        
        if not self.ollama_service:
            logger.error("VLM service not available")
            return {'error': 'VLM service not available'}
        
        try:
            # Buat prompt khusus untuk analisis metrics
            logger.info("Creating metrics analysis prompt")
            prompt = self._create_metrics_analysis_prompt(platform)
            logger.debug(f"Prompt created with length: {len(prompt)} characters")
            
            # Panggil VLM dengan screenshot
            logger.info("Calling Ollama VLM service for image analysis")
            logger.debug(f"Screenshot size: {len(screenshot_base64)} characters (base64)")
            
            response = self.ollama_service.analyze_image_with_text(
                image_base64=screenshot_base64,
                prompt=prompt
            )
            
            logger.info("Received response from VLM service")
            
            if response:
                logger.info("Parsing VLM response")
                logger.debug(f"VLM response length: {len(response)} characters")
                parsed_result = self._parse_vlm_metrics_response(response)
                logger.info(f"VLM analysis completed successfully. Detected metrics: {list(parsed_result.keys())}")
                return parsed_result
            else:
                logger.warning("No response received from VLM")
                return {'error': 'No response from VLM'}
                
        except Exception as e:
            logger.error(f"Error analyzing screenshot with VLM: {e}")
            logger.exception("Full exception details:")
            return {'error': str(e)}
    
    def _create_metrics_analysis_prompt(self, platform: str) -> str:
        """Buat prompt khusus untuk analisis metrics berdasarkan platform"""
        base_prompt = """
        Analisis screenshot halaman video ini dan ekstrak metrics berikut dengan sangat akurat:
        
        TUGAS:
        1. Identifikasi dan baca angka untuk setiap metric berikut:
           - Views (jumlah penayangan)
           - Likes (jumlah suka)
           - Comments (jumlah komentar)
           - Shares (jumlah berbagi)
        
        2. Berikan confidence level (0-100%) untuk setiap angka yang ditemukan
        
        3. Jika ada format singkatan (K, M, B), konversi ke angka penuh
        
        PLATFORM: {platform}
        
        FORMAT RESPONS (JSON):
        {{
            "views": {{
                "value": [angka atau null],
                "confidence": [0-100],
                "location": "[deskripsi lokasi di halaman]",
                "format_detected": "[format asli yang terdeteksi]"
            }},
            "likes": {{
                "value": [angka atau null],
                "confidence": [0-100],
                "location": "[deskripsi lokasi di halaman]",
                "format_detected": "[format asli yang terdeteksi]"
            }},
            "comments": {{
                "value": [angka atau null],
                "confidence": [0-100],
                "location": "[deskripsi lokasi di halaman]",
                "format_detected": "[format asli yang terdeteksi]"
            }},
            "shares": {{
                "value": [angka atau null],
                "confidence": [0-100],
                "location": "[deskripsi lokasi di halaman]",
                "format_detected": "[format asli yang terdeteksi]"
            }},
            "platform_confirmed": "[platform yang terdeteksi]",
            "overall_confidence": [0-100],
            "notes": "[catatan tambahan]"
        }}
        
        PENTING:
        - Hanya berikan angka yang benar-benar terlihat jelas
        - Jika tidak yakin, set confidence rendah
        - Jika tidak menemukan metric tertentu, set value ke null
        - Berikan respons dalam format JSON yang valid
        """.format(platform=platform.upper())
        
        # Tambahan prompt khusus per platform
        platform_specific = {
            'youtube': """
            
            KHUSUS YOUTUBE:
            - Views biasanya di bawah judul video
            - Likes di bagian bawah video player
            - Comments di section komentar
            - Shares mungkin tidak selalu terlihat
            """,
            'tiktok': """
            
            KHUSUS TIKTOK:
            - Metrics biasanya di sisi kanan video
            - Icon heart untuk likes
            - Icon comment bubble untuk comments
            - Icon share untuk shares
            - Views mungkin tidak selalu terlihat
            """,
            'facebook': """
            
            KHUSUS FACEBOOK:
            - Likes di bawah video
            - Comments dan shares di bagian interaksi
            - Views mungkin di pojok video
            """
        }
        
        return base_prompt + platform_specific.get(platform.lower(), "")
    
    def _parse_vlm_metrics_response(self, response: str) -> Dict[str, Any]:
        """Parse respons VLM untuk ekstrak metrics"""
        try:
            # Coba parse sebagai JSON
            if '{' in response and '}' in response:
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            
            # Fallback: ekstrak menggunakan regex
            return self._extract_metrics_with_regex(response)
            
        except json.JSONDecodeError:
            logger.warning("Failed to parse VLM response as JSON, using regex fallback")
            return self._extract_metrics_with_regex(response)
        except Exception as e:
            logger.error(f"Error parsing VLM response: {e}")
            return {'error': f'Parse error: {str(e)}'}
    
    def _extract_metrics_with_regex(self, text: str) -> Dict[str, Any]:
        """Ekstrak metrics menggunakan regex sebagai fallback"""
        metrics = {
            'views': {'value': None, 'confidence': 50},
            'likes': {'value': None, 'confidence': 50},
            'comments': {'value': None, 'confidence': 50},
            'shares': {'value': None, 'confidence': 50}
        }
        
        # Pattern untuk mencari metrics dalam teks
        patterns = {
            'views': [r'views?[:\s]*(\d+(?:,\d{3})*(?:\.\d+)?[KMBkmb]?)', r'penayangan[:\s]*(\d+(?:,\d{3})*(?:\.\d+)?[KMBkmb]?)'],
            'likes': [r'likes?[:\s]*(\d+(?:,\d{3})*(?:\.\d+)?[KMBkmb]?)', r'suka[:\s]*(\d+(?:,\d{3})*(?:\.\d+)?[KMBkmb]?)'],
            'comments': [r'comments?[:\s]*(\d+(?:,\d{3})*(?:\.\d+)?[KMBkmb]?)', r'komentar[:\s]*(\d+(?:,\d{3})*(?:\.\d+)?[KMBkmb]?)'],
            'shares': [r'shares?[:\s]*(\d+(?:,\d{3})*(?:\.\d+)?[KMBkmb]?)', r'berbagi[:\s]*(\d+(?:,\d{3})*(?:\.\d+)?[KMBkmb]?)']
        }
        
        for metric, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    raw_value = match.group(1)
                    converted_value = self._convert_number_format(raw_value)
                    if converted_value is not None:
                        metrics[metric]['value'] = converted_value
                        metrics[metric]['confidence'] = 70  # Medium confidence for regex
                        break
        
        return metrics
    
    def _convert_number_format(self, value_str: str) -> Optional[int]:
        """Konversi format angka (K, M, B) ke integer"""
        if not value_str:
            return None
        
        try:
            # Remove commas
            clean_str = value_str.replace(',', '')
            
            # Check for K, M, B suffixes
            multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000, 'k': 1000, 'm': 1000000, 'b': 1000000000}
            
            for suffix, multiplier in multipliers.items():
                if clean_str.endswith(suffix):
                    number_part = clean_str[:-1]
                    return int(float(number_part) * multiplier)
            
            # Regular number
            return int(float(clean_str))
            
        except (ValueError, TypeError):
            return None
    
    def cross_validate_metrics(self, scraped_data: Dict[str, Any], vlm_data: Dict[str, Any]) -> Dict[str, MetricAnalysis]:
        """Cross-validate antara data scraping dan VLM analysis"""
        logger.info("Starting cross-validation of metrics")
        logger.debug(f"Scraped data: {scraped_data}")
        logger.debug(f"VLM data keys: {list(vlm_data.keys())}")
        
        metrics_analysis = {}
        
        metric_names = ['views', 'likes', 'comments', 'shares']
        logger.info(f"Processing {len(metric_names)} metrics: {metric_names}")
        
        for i, metric in enumerate(metric_names, 1):
            logger.info(f"Processing metric {i}/{len(metric_names)}: {metric}")
            
            scraped_value = scraped_data.get(metric)
            vlm_result = vlm_data.get(metric, {})
            vlm_value = vlm_result.get('value')
            vlm_confidence = vlm_result.get('confidence', 0) / 100.0
            
            logger.debug(f"{metric} - Scraped: {scraped_value}, VLM: {vlm_value}, VLM confidence: {vlm_confidence:.2f}")
            
            # Calculate discrepancy ratio
            discrepancy_ratio = None
            if scraped_value and vlm_value and scraped_value > 0:
                discrepancy_ratio = abs(scraped_value - vlm_value) / scraped_value
                logger.debug(f"{metric} - Discrepancy ratio: {discrepancy_ratio:.3f} ({discrepancy_ratio*100:.1f}%)")
            else:
                logger.debug(f"{metric} - Cannot calculate discrepancy ratio (missing values)")
            
            # Determine verification status
            logger.debug(f"{metric} - Determining verification status")
            is_verified = False
            confidence_score = 0.0
            final_value = scraped_value
            notes = ""
            
            if scraped_value and vlm_value:
                logger.debug(f"{metric} - Both values available, comparing")
                if discrepancy_ratio is not None and discrepancy_ratio < 0.1:  # Less than 10% difference
                    is_verified = True
                    confidence_score = min(0.95, 0.7 + vlm_confidence * 0.3)
                    final_value = vlm_value if vlm_confidence > 0.8 else scraped_value
                    notes = "Values match closely, high confidence"
                    logger.debug(f"{metric} - High match (< 10% diff), verified=True, confidence={confidence_score:.2f}")
                elif discrepancy_ratio is not None and discrepancy_ratio < 0.3:  # Less than 30% difference
                    is_verified = True
                    confidence_score = 0.6 + vlm_confidence * 0.2
                    final_value = max(scraped_value, vlm_value)  # Use higher value
                    notes = "Moderate discrepancy, using higher value"
                    logger.debug(f"{metric} - Moderate match (< 30% diff), verified=True, confidence={confidence_score:.2f}")
                else:
                    is_verified = False
                    confidence_score = 0.3
                    final_value = scraped_value  # Default to scraped
                    notes = "High discrepancy, using scraped value"
                    logger.debug(f"{metric} - High discrepancy (>= 30% diff), verified=False, confidence={confidence_score:.2f}")
            elif scraped_value and not vlm_value:
                confidence_score = 0.5
                notes = "Only scraped value available"
                logger.debug(f"{metric} - Only scraped value available, confidence={confidence_score:.2f}")
            elif vlm_value and not scraped_value:
                confidence_score = vlm_confidence * 0.7
                final_value = vlm_value
                notes = "Only VLM value available"
                logger.debug(f"{metric} - Only VLM value available, confidence={confidence_score:.2f}")
            else:
                confidence_score = 0.0
                notes = "No values detected"
                logger.debug(f"{metric} - No values detected, confidence={confidence_score:.2f}")
            
            metrics_analysis[metric] = MetricAnalysis(
                metric_name=metric,
                scraped_value=scraped_value,
                vlm_detected_value=vlm_value,
                confidence_score=confidence_score,
                is_verified=is_verified,
                discrepancy_ratio=discrepancy_ratio,
                final_value=final_value,
                notes=notes
            )
            
            logger.info(f"{metric} validation complete - Final: {final_value}, Verified: {is_verified}, Confidence: {confidence_score:.2f}")
        
        verified_count = sum(1 for analysis in metrics_analysis.values() if analysis.is_verified)
        logger.info(f"Cross-validation completed. {verified_count}/{len(metric_names)} metrics verified")
        
        return metrics_analysis
    
    def analyze_video_metrics(self, url: str, scraped_data: Dict[str, Any], platform: str) -> VLMAnalysisResult:
        """Analisis lengkap metrics video dengan VLM"""
        start_time = datetime.now()
        timestamp = start_time.isoformat()
        
        logger.info(f"=== Starting VLM metrics analysis ===")
        logger.info(f"URL: {url}")
        logger.info(f"Platform: {platform}")
        logger.info(f"Scraped data keys: {list(scraped_data.keys())}")
        
        try:
            # Step 1: Capture screenshot
            logger.info("STEP 1: Capturing screenshot")
            step1_start = datetime.now()
            screenshot_base64 = self.capture_screenshot_with_playwright(url)
            step1_duration = (datetime.now() - step1_start).total_seconds()
            logger.info(f"Screenshot capture completed in {step1_duration:.2f} seconds")
            
            if not screenshot_base64:
                logger.error("Screenshot capture failed")
                return VLMAnalysisResult(
                    screenshot_taken=False,
                    analysis_successful=False,
                    metrics={},
                    overall_confidence=0.0,
                    platform_detected=platform,
                    timestamp=timestamp,
                    error_message="Failed to capture screenshot"
                )
            
            logger.info("Screenshot captured successfully")
            
            # Step 2: Analyze with VLM
            logger.info("STEP 2: VLM Analysis")
            step2_start = datetime.now()
            vlm_data = self.analyze_metrics_from_screenshot(screenshot_base64, platform)
            step2_duration = (datetime.now() - step2_start).total_seconds()
            logger.info(f"VLM analysis completed in {step2_duration:.2f} seconds")
            
            if 'error' in vlm_data:
                logger.error(f"VLM analysis failed: {vlm_data['error']}")
                return VLMAnalysisResult(
                    screenshot_taken=True,
                    analysis_successful=False,
                    metrics={},
                    overall_confidence=0.0,
                    platform_detected=platform,
                    timestamp=timestamp,
                    error_message=vlm_data['error']
                )
            
            logger.info("VLM analysis successful")
            
            # Step 3: Cross-validate
            logger.info("STEP 3: Cross-validation")
            step3_start = datetime.now()
            metrics_analysis = self.cross_validate_metrics(scraped_data, vlm_data)
            step3_duration = (datetime.now() - step3_start).total_seconds()
            logger.info(f"Cross-validation completed in {step3_duration:.2f} seconds")
            
            # Calculate overall confidence
            logger.info("STEP 4: Calculating overall confidence")
            confidence_scores = [analysis.confidence_score for analysis in metrics_analysis.values()]
            overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
            
            total_duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"=== VLM analysis completed successfully in {total_duration:.2f} seconds ===")
            logger.info(f"Overall confidence: {overall_confidence:.2f}")
            
            return VLMAnalysisResult(
                screenshot_taken=True,
                analysis_successful=True,
                metrics=metrics_analysis,
                overall_confidence=overall_confidence,
                platform_detected=vlm_data.get('platform_confirmed', platform),
                timestamp=timestamp
            )
            
        except Exception as e:
            total_duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"=== VLM analysis failed after {total_duration:.2f} seconds ===")
            logger.error(f"Error in VLM analysis: {e}")
            logger.exception("Full exception details:")
            return VLMAnalysisResult(
                screenshot_taken=False,
                analysis_successful=False,
                metrics={},
                overall_confidence=0.0,
                platform_detected=platform,
                timestamp=timestamp,
                error_message=str(e)
            )
    
    def get_confidence_level_text(self, confidence: float) -> str:
        """Get confidence level description"""
        if confidence >= self.confidence_thresholds['high']:
            return "Tinggi"
        elif confidence >= self.confidence_thresholds['medium']:
            return "Sedang"
        elif confidence >= self.confidence_thresholds['low']:
            return "Rendah"
        else:
            return "Sangat Rendah"
    
    def format_analysis_summary(self, result: VLMAnalysisResult) -> str:
        """Format summary hasil analisis untuk display"""
        if not result.analysis_successful:
            return f"❌ Analisis VLM gagal: {result.error_message or 'Unknown error'}"
        
        summary = f"🤖 **Analisis VLM Selesai**\n\n"
        summary += f"📊 **Confidence Keseluruhan:** {result.overall_confidence:.1%} ({self.get_confidence_level_text(result.overall_confidence)})\n\n"
        
        summary += "📈 **Detail Metrics:**\n"
        for metric_name, analysis in result.metrics.items():
            icon = {'views': '👀', 'likes': '👍', 'comments': '💬', 'shares': '📤'}.get(metric_name, '📊')
            
            summary += f"\n{icon} **{metric_name.title()}:**\n"
            summary += f"  • Scraped: {analysis.scraped_value:,} " if analysis.scraped_value else "  • Scraped: N/A\n"
            summary += f"  • VLM: {analysis.vlm_detected_value:,} " if analysis.vlm_detected_value else "  • VLM: N/A\n"
            summary += f"  • Final: {analysis.final_value:,} " if analysis.final_value else "  • Final: N/A\n"
            summary += f"  • Confidence: {analysis.confidence_score:.1%}\n"
            summary += f"  • Status: {'✅ Verified' if analysis.is_verified else '⚠️ Unverified'}\n"
            summary += f"  • Notes: {analysis.notes}\n"
        
        return summary

# Global instance
vlm_analyzer = VLMMetricsAnalyzer()

def analyze_video_with_vlm(url: str, scraped_data: Dict[str, Any], platform: str) -> VLMAnalysisResult:
    """Function wrapper untuk analisis VLM"""
    return vlm_analyzer.analyze_video_metrics(url, scraped_data, platform)

if __name__ == "__main__":
    # Test the analyzer
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    test_data = {'views': 1000000, 'likes': 50000, 'comments': 5000, 'shares': 1000}
    
    result = analyze_video_with_vlm(test_url, test_data, "youtube")
    print(vlm_analyzer.format_analysis_summary(result))