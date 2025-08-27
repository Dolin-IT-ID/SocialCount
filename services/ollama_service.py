import requests
import json
from typing import Dict, Any, Optional
from config import Config

class OllamaService:
    """Service for interacting with Ollama and Llama2 model"""
    
    def __init__(self, base_url: str = None, model: str = None):
        self.base_url = base_url or Config.OLLAMA_BASE_URL
        self.model = model or Config.OLLAMA_MODEL
        self.session = requests.Session()
    
    def is_available(self) -> bool:
        """Check if Ollama service is available"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self) -> list:
        """List available models"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                return response.json().get('models', [])
            return []
        except:
            return []
    
    def generate_response(self, prompt: str, context: str = None) -> str:
        """Generate response using Llama2 model"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            
            if context:
                payload["context"] = context
            
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def analyze_social_media_data(self, stats_data: Dict[str, Any]) -> str:
        """Analyze social media statistics using Llama2"""
        prompt = f"""
Analyze the following social media statistics and provide insights:

Platform: {stats_data.get('platform', 'Unknown')}
Title: {stats_data.get('title', 'N/A')}
Author: {stats_data.get('author', 'N/A')}
Views: {stats_data.get('views', 'N/A')}
Likes: {stats_data.get('likes', 'N/A')}
Shares: {stats_data.get('shares', 'N/A')}
Comments: {stats_data.get('comments', 'N/A')}
Upload Date: {stats_data.get('upload_date', 'N/A')}

Please provide:
1. Performance analysis (engagement rate, reach assessment)
2. Content insights based on the metrics
3. Recommendations for improvement
4. Comparison with typical performance for this platform

Keep the analysis concise and actionable.
"""
        
        return self.generate_response(prompt)
    
    def compare_platforms(self, stats_list: list) -> str:
        """Compare statistics across multiple platforms"""
        if len(stats_list) < 2:
            return "Need at least 2 platforms to compare"
        
        comparison_data = ""
        for i, stats in enumerate(stats_list, 1):
            comparison_data += f"""
Platform {i}: {stats.get('platform', 'Unknown')}
- Views: {stats.get('views', 'N/A')}
- Likes: {stats.get('likes', 'N/A')}
- Shares: {stats.get('shares', 'N/A')}
- Comments: {stats.get('comments', 'N/A')}

"""
        
        prompt = f"""
Compare the following social media performance across platforms:

{comparison_data}

Please provide:
1. Which platform performed best and why
2. Engagement patterns across platforms
3. Platform-specific insights
4. Recommendations for cross-platform strategy

Keep the comparison concise and actionable.
"""
        
        return self.generate_response(prompt)
    
    def generate_content_suggestions(self, stats_data: Dict[str, Any]) -> str:
        """Generate content suggestions based on performance data"""
        prompt = f"""
Based on this social media post performance:

Platform: {stats_data.get('platform', 'Unknown')}
Title/Content: {stats_data.get('title', 'N/A')}
Views: {stats_data.get('views', 'N/A')}
Likes: {stats_data.get('likes', 'N/A')}
Shares: {stats_data.get('shares', 'N/A')}
Comments: {stats_data.get('comments', 'N/A')}

Generate 5 content improvement suggestions:
1. Title/Caption optimization
2. Posting time recommendations
3. Content format suggestions
4. Engagement tactics
5. Hashtag/keyword recommendations

Make suggestions specific to the {stats_data.get('platform', 'platform')} platform.
"""
        
        return self.generate_response(prompt)
    
    def analyze_image_with_text(self, image_base64: str, prompt: str) -> str:
        """Analyze image with text using vision-capable model"""
        try:
            # Check if we have a vision-capable model
            vision_models = ['llava', 'llava:latest', 'bakllava', 'moondream']
            available_models = [m.get('name', '') for m in self.list_models()]
            
            # Find a suitable vision model
            vision_model = None
            for model in vision_models:
                if model in available_models:
                    vision_model = model
                    break
            
            if not vision_model:
                return "Error: No vision-capable model available. Please install llava or similar model."
            
            payload = {
                "model": vision_model,
                "prompt": prompt,
                "images": [image_base64],
                "stream": False
            }
            
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60  # Longer timeout for vision analysis
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error analyzing image: {str(e)}"
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check on Ollama service"""
        result = {
            'service_available': False,
            'model_loaded': False,
            'models_available': [],
            'error': None
        }
        
        try:
            # Check service availability
            result['service_available'] = self.is_available()
            
            if result['service_available']:
                # Check available models
                models = self.list_models()
                result['models_available'] = [m.get('name', '') for m in models]
                result['model_loaded'] = self.model in result['models_available']
                
                if not result['model_loaded']:
                    result['error'] = f"Model '{self.model}' not found. Available models: {result['models_available']}"
            else:
                result['error'] = "Ollama service is not available"
                
        except Exception as e:
            result['error'] = str(e)
        
        return result