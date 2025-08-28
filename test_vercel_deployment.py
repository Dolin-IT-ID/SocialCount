#!/usr/bin/env python3
"""
Test script untuk memverifikasi konfigurasi deployment Vercel
"""

import os
import sys
import json
from pathlib import Path

def test_vercel_config():
    """Test konfigurasi Vercel"""
    print("🔍 Testing Vercel configuration...")
    
    # Check vercel.json
    vercel_json = Path("vercel.json")
    if not vercel_json.exists():
        print("❌ vercel.json not found")
        return False
    
    try:
        with open(vercel_json) as f:
            config = json.load(f)
        print("✅ vercel.json is valid JSON")
    except json.JSONDecodeError as e:
        print(f"❌ vercel.json invalid: {e}")
        return False
    
    # Check required files
    required_files = [
        "api/index.py",
        "requirements-vercel.txt", 
        "runtime.txt",
        "streamlit_video_extractor.py"
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"❌ {file_path} not found")
            return False
        else:
            print(f"✅ {file_path} exists")
    
    return True

def test_dependencies():
    """Test dependencies untuk Vercel"""
    print("\n📦 Testing Vercel dependencies...")
    
    try:
        # Test import dependencies yang diperlukan
        import streamlit
        import pandas
        import plotly
        import requests
        import json
        
        print("✅ Core dependencies available")
        
        # Check versions
        print(f"   - Streamlit: {streamlit.__version__}")
        print(f"   - Pandas: {pandas.__version__}")
        print(f"   - Plotly: {plotly.__version__}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def test_app_import():
    """Test import aplikasi utama"""
    print("\n🎬 Testing main app import...")
    
    try:
        # Add current directory to path
        sys.path.insert(0, ".")
        
        # Test import without running
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "streamlit_video_extractor", 
            "streamlit_video_extractor.py"
        )
        module = importlib.util.module_from_spec(spec)
        
        print("✅ Main app can be imported")
        return True
        
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

def test_vercel_handler():
    """Test Vercel handler"""
    print("\n🔧 Testing Vercel handler...")
    
    try:
        sys.path.insert(0, "api")
        import index
        
        # Test handler function exists
        if hasattr(index, 'handler'):
            print("✅ Handler function exists")
        else:
            print("❌ Handler function not found")
            return False
            
        if hasattr(index, 'app'):
            print("✅ App export exists")
        else:
            print("❌ App export not found")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Handler test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Vercel Deployment Test")
    print("=" * 50)
    
    tests = [
        test_vercel_config,
        test_dependencies,
        test_app_import,
        test_vercel_handler
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for Vercel deployment.")
        print("\n📝 Next steps:")
        print("   1. vercel login")
        print("   2. vercel --prod")
    else:
        print("⚠️  Some tests failed. Please fix issues before deployment.")
        
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)