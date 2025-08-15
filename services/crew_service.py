from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool
from typing import Dict, Any, List
import json
from .ollama_service import OllamaService
from scrapers import ScraperFactory, SocialMediaStats
from utils import URLDetector
from config import Config

class SocialMediaScrapingTool(BaseTool):
    """Custom tool for scraping social media data"""
    name: str = "social_media_scraper"
    description: str = "Scrapes social media statistics from YouTube, TikTok, and Facebook URLs"
    
    def _run(self, url: str) -> str:
        """Execute the scraping tool"""
        try:
            # Detect platform
            url_info = URLDetector.validate_url(url)
            if not url_info['valid']:
                return f"Error: {url_info['error']}"
            
            platform = url_info['platform']
            
            # Create scraper and scrape data
            with ScraperFactory.create_scraper(platform, headless=True) as scraper:
                stats = scraper.scrape(url)
                return json.dumps(stats.to_dict(), indent=2)
                
        except Exception as e:
            return f"Error scraping {url}: {str(e)}"

class SocialMediaAnalysisTool(BaseTool):
    """Custom tool for analyzing social media data using Ollama"""
    name: str = "social_media_analyzer"
    description: str = "Analyzes social media statistics and provides insights using Llama2"
    
    def _run(self, stats_json: str) -> str:
        """Execute the analysis tool"""
        try:
            ollama_service = OllamaService()
            stats_data = json.loads(stats_json)
            return ollama_service.analyze_social_media_data(stats_data)
        except Exception as e:
            return f"Error analyzing data: {str(e)}"

class CrewService:
    """Service for managing CrewAI agents and tasks"""
    
    def __init__(self):
        self.ollama_service = OllamaService()
        self.scraping_tool = SocialMediaScrapingTool()
        self.analysis_tool = SocialMediaAnalysisTool()
        
        # Configure Ollama LLM for CrewAI
        self.llm = LLM(
            model=f"ollama/{Config.OLLAMA_MODEL}",
            base_url="http://localhost:11434"
        )
        
        # Initialize agents
        self.data_collector = self._create_data_collector_agent()
        self.data_analyst = self._create_data_analyst_agent()
        self.insights_generator = self._create_insights_generator_agent()
    
    def _create_data_collector_agent(self) -> Agent:
        """Create agent responsible for collecting social media data"""
        return Agent(
            role='Social Media Data Collector',
            goal='Collect accurate and comprehensive social media statistics from various platforms',
            backstory="""You are an expert data collector specializing in social media analytics. 
            You have extensive experience in gathering metrics from YouTube, TikTok, and Facebook. 
            You ensure data accuracy and handle various edge cases in social media scraping.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def _create_data_analyst_agent(self) -> Agent:
        """Create agent responsible for analyzing collected data"""
        return Agent(
            role='Social Media Data Analyst',
            goal='Analyze social media metrics and identify patterns, trends, and performance indicators',
            backstory="""You are a skilled data analyst with deep expertise in social media metrics. 
            You can interpret engagement rates, reach metrics, and performance indicators across 
            different platforms. You provide actionable insights based on quantitative analysis.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def _create_insights_generator_agent(self) -> Agent:
        """Create agent responsible for generating insights and recommendations"""
        return Agent(
            role='Social Media Insights Generator',
            goal='Generate actionable insights and recommendations for social media optimization',
            backstory="""You are a social media strategist with years of experience in content 
            optimization and audience engagement. You can translate data analysis into practical 
            recommendations for improving social media performance across platforms.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def create_data_collection_task(self, url: str) -> Task:
        """Create task for collecting social media data"""
        return Task(
            description=f"""Collect comprehensive social media statistics from the following URL: {url}
            
            Requirements:
            1. Extract all available metrics (views, likes, shares, comments)
            2. Gather metadata (title, author, upload date)
            3. Handle any errors gracefully
            4. Return data in structured JSON format
            
            The output should include platform identification and all relevant metrics.""",
            agent=self.data_collector,
            expected_output="Structured JSON data containing all social media metrics and metadata"
        )
    
    def create_analysis_task(self, collected_data: str) -> Task:
        """Create task for analyzing collected data"""
        return Task(
            description=f"""Analyze the following social media data and provide comprehensive insights:
            
            Data: {collected_data}
            
            Requirements:
            1. Calculate engagement rates and performance metrics
            2. Assess content performance relative to platform benchmarks
            3. Identify strengths and areas for improvement
            4. Provide platform-specific analysis
            
            Focus on actionable insights that can help improve future content performance.""",
            agent=self.data_analyst,
            expected_output="Detailed analysis report with performance metrics and insights"
        )
    
    def create_insights_task(self, analysis_results: str) -> Task:
        """Create task for generating actionable insights"""
        return Task(
            description=f"""Based on the following analysis, generate actionable recommendations:
            
            Analysis: {analysis_results}
            
            Requirements:
            1. Provide specific, actionable recommendations
            2. Suggest content optimization strategies
            3. Recommend posting time and frequency improvements
            4. Propose engagement enhancement tactics
            5. Include platform-specific best practices
            
            Make recommendations practical and implementable.""",
            agent=self.insights_generator,
            expected_output="Comprehensive list of actionable recommendations for social media optimization"
        )
    
    def analyze_single_url(self, url: str) -> Dict[str, Any]:
        """Analyze a single social media URL using direct scraping and Ollama analysis"""
        try:
            # Direct data collection using scraper
            url_info = URLDetector.validate_url(url)
            if not url_info['valid']:
                return {
                'success': False,
                'error': f"Invalid URL: {url_info['error']}",
                'stats': None,
                'analysis': None,
                'insights': None
            }
            
            platform = url_info['platform']
            with ScraperFactory.create_scraper(platform, headless=True) as scraper:
                stats = scraper.scrape(url)
                stats_data = stats.to_dict()
            
            # Use OllamaService directly for analysis instead of CrewAI
            analysis_result = self.ollama_service.analyze_social_media_data(stats_data)
            
            return {
                'success': True,
                'error': None,
                'stats': stats_data,
                'analysis': analysis_result,
                'insights': analysis_result  # Using same analysis as insights for now
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'stats': None,
                'analysis': None,
                'insights': None
            }
    
    def analyze_multiple_urls(self, urls: List[str]) -> Dict[str, Any]:
        """Analyze multiple social media URLs and provide comparative insights"""
        results = []
        
        for url in urls:
            result = self.analyze_single_url(url)
            results.append(result)
        
        # Generate comparative analysis if multiple successful results
        successful_results = [r for r in results if r.get('success', False)]
        
        if len(successful_results) > 1:
            stats_list = [r['stats'] for r in successful_results if 'stats' in r]
            comparative_analysis = self.ollama_service.compare_platforms(stats_list)
            
            return {
                'individual_results': results,
                'comparative_analysis': comparative_analysis,
                'total_analyzed': len(urls),
                'successful_analyses': len(successful_results)
            }
        
        return {
            'individual_results': results,
            'total_analyzed': len(urls),
            'successful_analyses': len(successful_results)
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check on all services"""
        return {
            'ollama_service': self.ollama_service.health_check(),
            'crew_agents_ready': True,
            'tools_available': {
                'scraping_tool': self.scraping_tool.name,
                'analysis_tool': self.analysis_tool.name
            }
        }