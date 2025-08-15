#!/usr/bin/env python3
"""
SocialCount - Social Media Analytics Tool
Main CLI interface for the application
"""

import argparse
import json
import sys
from typing import List
from services import CrewService, OllamaService
from utils import URLDetector
from config import Config

def print_banner():
    """Print application banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                        📊 SocialCount                        ║
║              Social Media Analytics with AI                  ║
║                                                              ║
║    Supported Platforms: YouTube 🎥 | TikTok 🎵 | Facebook 👥  ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_services():
    """Check if required services are available"""
    print("🔍 Checking services...")
    
    try:
        ollama_service = OllamaService()
        health_status = ollama_service.health_check()
        
        print(f"\n📊 Service Status:")
        print(f"  • Ollama Service: {'✅ Available' if health_status['service_available'] else '❌ Not Available'}")
        
        if health_status['service_available']:
            print(f"  • Model ({Config.OLLAMA_MODEL}): {'✅ Loaded' if health_status['model_loaded'] else '❌ Not Loaded'}")
            if health_status['models_available']:
                print(f"  • Available Models: {', '.join(health_status['models_available'])}")
        
        if health_status['error']:
            print(f"  • Error: {health_status['error']}")
        
        return health_status['service_available'] and health_status['model_loaded']
        
    except Exception as e:
        print(f"❌ Error checking services: {str(e)}")
        return False

def analyze_url(url: str, verbose: bool = False) -> dict:
    """Analyze a single URL"""
    print(f"\n🔍 Analyzing URL: {url}")
    
    # Validate URL
    url_info = URLDetector.validate_url(url)
    if not url_info['valid']:
        print(f"❌ Invalid URL: {url_info['error']}")
        return {'success': False, 'error': url_info['error']}
    
    platform = url_info['platform']
    platform_icons = {'youtube': '🎥', 'tiktok': '🎵', 'facebook': '👥'}
    icon = platform_icons.get(platform, '📱')
    
    print(f"✅ Platform detected: {icon} {platform.title()}")
    
    try:
        # Initialize CrewAI service
        print("🤖 Initializing AI agents...")
        crew_service = CrewService()
        
        # Perform analysis
        print("📊 Performing analysis...")
        result = crew_service.analyze_single_url(url)
        
        if result['success']:
            print("✅ Analysis completed successfully!")
            display_results(result, verbose)
        else:
            print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
        
        return result
        
    except Exception as e:
        error_msg = f"Error during analysis: {str(e)}"
        print(f"❌ {error_msg}")
        return {'success': False, 'error': error_msg}

def analyze_multiple_urls(urls: List[str], verbose: bool = False) -> dict:
    """Analyze multiple URLs"""
    print(f"\n🔍 Analyzing {len(urls)} URLs...")
    
    try:
        # Initialize CrewAI service
        print("🤖 Initializing AI agents...")
        crew_service = CrewService()
        
        # Perform analysis
        print("📊 Performing batch analysis...")
        results = crew_service.analyze_multiple_urls(urls)
        
        print(f"\n📋 Analysis Summary:")
        print(f"  • Total URLs: {results['total_analyzed']}")
        print(f"  • Successful: {results['successful_analyses']}")
        print(f"  • Failed: {results['total_analyzed'] - results['successful_analyses']}")
        
        # Display individual results
        for i, result in enumerate(results['individual_results'], 1):
            print(f"\n--- URL {i} ---")
            if result['success']:
                display_results(result, verbose)
            else:
                print(f"❌ Failed: {result.get('error', 'Unknown error')}")
        
        # Display comparative analysis
        if 'comparative_analysis' in results:
            print("\n🔄 Comparative Analysis:")
            print(results['comparative_analysis'])
        
        return results
        
    except Exception as e:
        error_msg = f"Error during batch analysis: {str(e)}"
        print(f"❌ {error_msg}")
        return {'success': False, 'error': error_msg}

def display_results(result: dict, verbose: bool = False):
    """Display analysis results"""
    if not result.get('success', False):
        return
    
    stats = result.get('stats', {})
    
    if stats.get('error'):
        print(f"❌ Scraping error: {stats['error']}")
        return
    
    # Basic info
    print(f"\n📋 Basic Information:")
    if stats.get('platform'):
        platform_icons = {'youtube': '🎥', 'tiktok': '🎵', 'facebook': '👥'}
        icon = platform_icons.get(stats['platform'], '📱')
        print(f"  • Platform: {icon} {stats['platform'].title()}")
    
    if stats.get('title'):
        title = stats['title'][:80] + '...' if len(stats['title']) > 80 else stats['title']
        print(f"  • Title: {title}")
    
    if stats.get('author'):
        print(f"  • Author: {stats['author']}")
    
    if stats.get('upload_date'):
        print(f"  • Upload Date: {stats['upload_date']}")
    
    # Statistics
    print(f"\n📊 Statistics:")
    metrics = [
        ('Views', stats.get('views'), '👁️'),
        ('Likes', stats.get('likes'), '👍'),
        ('Shares', stats.get('shares'), '🔄'),
        ('Comments', stats.get('comments'), '💬')
    ]
    
    for label, value, icon in metrics:
        if value is not None:
            formatted_value = f"{value:,}" if isinstance(value, int) else str(value)
            print(f"  • {icon} {label}: {formatted_value}")
    
    # AI Analysis
    if 'analysis' in result and result['analysis'] and verbose:
        print(f"\n🤖 AI Analysis:")
        print(result['analysis'])
    
    # JSON output for verbose mode
    if verbose:
        print(f"\n📄 Raw Data (JSON):")
        print(json.dumps(stats, indent=2, ensure_ascii=False))

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description='SocialCount - Social Media Analytics Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --check                                    # Check services
  python main.py --url "https://youtube.com/watch?v=..."    # Analyze single URL
  python main.py --file urls.txt                           # Analyze URLs from file
  python main.py --url "..." --verbose                     # Detailed output
  python main.py --web                                     # Launch web interface
        """
    )
    
    parser.add_argument('--url', '-u', type=str, help='Single URL to analyze')
    parser.add_argument('--file', '-f', type=str, help='File containing URLs (one per line)')
    parser.add_argument('--check', '-c', action='store_true', help='Check service status')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--web', '-w', action='store_true', help='Launch web interface')
    parser.add_argument('--output', '-o', type=str, help='Output file for results (JSON)')
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Check services if requested
    if args.check:
        services_ok = check_services()
        sys.exit(0 if services_ok else 1)
    
    # Launch web interface
    if args.web:
        print("🚀 Launching web interface...")
        import subprocess
        try:
            subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to launch web interface: {e}")
            sys.exit(1)
        return
    
    # Check services before analysis
    if not check_services():
        print("\n❌ Services are not ready. Please check your Ollama installation and ensure Llama2 model is available.")
        print("\nTo install Ollama and Llama2:")
        print("1. Install Ollama: https://ollama.ai/")
        print("2. Run: ollama pull llama2")
        sys.exit(1)
    
    results = None
    
    # Analyze single URL
    if args.url:
        results = analyze_url(args.url, args.verbose)
    
    # Analyze URLs from file
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip()]
            
            if not urls:
                print(f"❌ No URLs found in file: {args.file}")
                sys.exit(1)
            
            results = analyze_multiple_urls(urls, args.verbose)
            
        except FileNotFoundError:
            print(f"❌ File not found: {args.file}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error reading file: {str(e)}")
            sys.exit(1)
    
    else:
        # Interactive mode
        print("\n🔗 Enter URL to analyze (or 'quit' to exit):")
        while True:
            try:
                url = input("> ").strip()
                if url.lower() in ['quit', 'exit', 'q']:
                    break
                if url:
                    analyze_url(url, args.verbose)
                    print("\n" + "="*60)
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                break
    
    # Save results to file if requested
    if args.output and results:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Results saved to: {args.output}")
        except Exception as e:
            print(f"❌ Error saving results: {str(e)}")

if __name__ == '__main__':
    main()