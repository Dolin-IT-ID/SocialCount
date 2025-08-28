#!/usr/bin/env python3
"""
Vercel handler for Streamlit app
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set environment variables for Streamlit
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'
os.environ['STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION'] = 'false'

def handler(request):
    """Vercel serverless handler for Streamlit"""
    try:
        # Import Streamlit components
        import streamlit as st
        from streamlit.web import bootstrap
        
        # Configure Streamlit for serverless deployment
        st.set_option('server.headless', True)
        st.set_option('server.enableCORS', False)
        st.set_option('server.enableXsrfProtection', False)
        
        # Set up the Streamlit app path
        app_path = str(project_root / 'streamlit_video_extractor.py')
        
        # Bootstrap the Streamlit app
        bootstrap.run(app_path, '', [], {})
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html',
                'Access-Control-Allow-Origin': '*'
            },
            'body': 'Streamlit app is running'
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': '{"error": "Failed to start Streamlit app: ' + str(e) + '"}'
        }

# For Vercel compatibility
app = handler