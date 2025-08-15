#!/usr/bin/env python3
"""
SocialCount Setup Script
Automatic setup and installation script
"""

import os
import sys
import subprocess
import platform
import requests
from pathlib import Path

def print_banner():
    """Print setup banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    📊 SocialCount Setup                      ║
║              Automatic Installation Script                   ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def install_requirements():
    """Install Python requirements"""
    print("\n📦 Installing Python dependencies...")
    
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                      check=True, capture_output=True)
        
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True)
        
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_ollama_installation():
    """Check if Ollama is installed and running"""
    print("\n🤖 Checking Ollama installation...")
    
    # Check if Ollama is installed
    try:
        result = subprocess.run(['ollama', '--version'], 
                               capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Ollama installed: {result.stdout.strip()}")
        else:
            print("❌ Ollama not found in PATH")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Ollama not installed")
        return False
    
    # Check if Ollama service is running
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            print("✅ Ollama service is running")
            return True
        else:
            print("❌ Ollama service not responding")
            return False
    except requests.RequestException:
        print("❌ Ollama service not running")
        return False

def install_ollama():
    """Install Ollama based on platform"""
    print("\n🔧 Installing Ollama...")
    
    system = platform.system().lower()
    
    if system == 'windows':
        print("📥 Please download and install Ollama manually:")
        print("   1. Go to https://ollama.ai/")
        print("   2. Download Ollama for Windows")
        print("   3. Run the installer")
        print("   4. Restart this setup script")
        return False
    
    elif system == 'darwin':  # macOS
        try:
            subprocess.run(['brew', 'install', 'ollama'], check=True)
            print("✅ Ollama installed via Homebrew")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Failed to install via Homebrew")
            print("📥 Please install manually from https://ollama.ai/")
            return False
    
    elif system == 'linux':
        try:
            # Install via curl script
            subprocess.run(['curl', '-fsSL', 'https://ollama.ai/install.sh'], 
                          stdout=subprocess.PIPE, check=True)
            print("✅ Ollama installed via install script")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install via script")
            print("📥 Please install manually from https://ollama.ai/")
            return False
    
    else:
        print(f"❌ Unsupported platform: {system}")
        return False

def pull_llama2_model():
    """Pull Llama2 model"""
    print("\n🦙 Pulling Llama2 model...")
    print("⏳ This may take several minutes depending on your internet connection...")
    
    try:
        process = subprocess.Popen(['ollama', 'pull', 'llama2'], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.STDOUT, 
                                  text=True, 
                                  universal_newlines=True)
        
        # Show progress
        for line in process.stdout:
            print(f"   {line.strip()}")
        
        process.wait()
        
        if process.returncode == 0:
            print("✅ Llama2 model downloaded successfully")
            return True
        else:
            print("❌ Failed to download Llama2 model")
            return False
            
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        return False

def setup_environment():
    """Setup environment file"""
    print("\n⚙️ Setting up environment...")
    
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists() and env_example.exists():
        try:
            # Copy example to .env
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print("✅ Environment file created from template")
        except Exception as e:
            print(f"❌ Failed to create environment file: {e}")
            return False
    elif env_file.exists():
        print("✅ Environment file already exists")
    else:
        print("❌ No environment template found")
        return False
    
    return True

def check_chrome_installation():
    """Check if Chrome is installed"""
    print("\n🌐 Checking Chrome installation...")
    
    system = platform.system().lower()
    chrome_paths = {
        'windows': [
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        ],
        'darwin': ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'],
        'linux': ['/usr/bin/google-chrome', '/usr/bin/chromium-browser']
    }
    
    paths = chrome_paths.get(system, [])
    
    for path in paths:
        if os.path.exists(path):
            print("✅ Chrome browser found")
            return True
    
    print("❌ Chrome browser not found")
    print("📥 Please install Google Chrome from https://www.google.com/chrome/")
    return False

def run_health_check():
    """Run application health check"""
    print("\n🏥 Running health check...")
    
    try:
        result = subprocess.run([sys.executable, 'main.py', '--check'], 
                               capture_output=True, text=True, timeout=30)
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install Python requirements
    if not install_requirements():
        print("\n❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Check Chrome
    chrome_ok = check_chrome_installation()
    
    # Check Ollama
    ollama_ok = check_ollama_installation()
    
    if not ollama_ok:
        print("\n🔧 Ollama not found. Attempting installation...")
        if not install_ollama():
            print("\n❌ Please install Ollama manually and run setup again")
            sys.exit(1)
        
        # Check again after installation
        ollama_ok = check_ollama_installation()
    
    if ollama_ok:
        # Pull Llama2 model
        if not pull_llama2_model():
            print("\n❌ Failed to download Llama2 model")
            print("   You can try manually: ollama pull llama2")
    
    # Setup environment
    if not setup_environment():
        print("\n❌ Environment setup failed")
    
    # Final health check
    print("\n" + "="*60)
    health_ok = run_health_check()
    
    # Summary
    print("\n" + "="*60)
    print("📋 Setup Summary:")
    print(f"  • Python Dependencies: ✅")
    print(f"  • Chrome Browser: {'✅' if chrome_ok else '❌'}")
    print(f"  • Ollama Service: {'✅' if ollama_ok else '❌'}")
    print(f"  • Health Check: {'✅' if health_ok else '❌'}")
    
    if health_ok:
        print("\n🎉 Setup completed successfully!")
        print("\n🚀 You can now run the application:")
        print("   • Web Interface: python main.py --web")
        print("   • CLI Interface: python main.py --url <your-url>")
    else:
        print("\n⚠️ Setup completed with issues")
        print("   Please check the error messages above")
        print("   You may need to install missing components manually")
    
    print("\n📖 For more information, see README.md")

if __name__ == '__main__':
    main()