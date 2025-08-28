# Internationalization (i18n) system for bilingual support
# Sistem internasionalisasi untuk dukungan dwibahasa

import streamlit as st
from locales.id import LANGUAGE_CONFIG as ID_CONFIG
from locales.zh import LANGUAGE_CONFIG as ZH_CONFIG

# Available languages
LANGUAGES = {
    'id': ID_CONFIG,
    'zh': ZH_CONFIG
}

def get_available_languages():
    """Get list of available languages with their display names and flags"""
    return {
        code: {
            'name': config['language_name'],
            'flag': config['flag'],
            'display': f"{config['flag']} {config['language_name']}"
        }
        for code, config in LANGUAGES.items()
    }

def init_language():
    """Initialize language settings in session state"""
    if 'language' not in st.session_state:
        st.session_state.language = 'id'  # Default to Indonesian
    
    if 'language_config' not in st.session_state:
        st.session_state.language_config = LANGUAGES[st.session_state.language]

def set_language(language_code):
    """Set the current language"""
    if language_code in LANGUAGES:
        st.session_state.language = language_code
        st.session_state.language_config = LANGUAGES[language_code]
        # Force rerun to update UI
        st.rerun()
    else:
        st.error(f"Language '{language_code}' not supported")

def get_text(key, default=None, **kwargs):
    """Get translated text for the current language"""
    if 'language_config' not in st.session_state:
        init_language()
    
    config = st.session_state.language_config
    text = config.get(key, default or key)
    
    # Handle string formatting if kwargs provided
    if kwargs and isinstance(text, str):
        try:
            text = text.format(**kwargs)
        except (KeyError, ValueError):
            pass  # Return unformatted text if formatting fails
    
    return text

def get_current_language():
    """Get current language code"""
    return st.session_state.get('language', 'id')

def get_current_language_name():
    """Get current language display name"""
    if 'language_config' not in st.session_state:
        init_language()
    return st.session_state.language_config.get('language_name', 'Bahasa Indonesia')

def create_language_switcher():
    """Create language switcher component for sidebar"""
    init_language()
    
    available_langs = get_available_languages()
    current_lang = get_current_language()
    
    # Create selectbox with language options
    selected_display = available_langs[current_lang]['display']
    
    # Get all display options
    display_options = [lang_info['display'] for lang_info in available_langs.values()]
    
    # Create mapping from display to code
    display_to_code = {
        lang_info['display']: code 
        for code, lang_info in available_langs.items()
    }
    
    # Language selector
    with st.sidebar:
        st.markdown("---")
        selected_display = st.selectbox(
            get_text('language_selector'),
            options=display_options,
            index=display_options.index(selected_display),
            key="language_selector"
        )
        
        # Update language if changed
        selected_code = display_to_code[selected_display]
        if selected_code != current_lang:
            set_language(selected_code)

def t(key, default=None, **kwargs):
    """Shorthand function for get_text"""
    return get_text(key, default, **kwargs)

# Helper functions for common UI patterns
def get_tab_names():
    """Get translated tab names"""
    return [
        get_text('tab_extract'),
        get_text('tab_batch'),
        get_text('tab_history'),
        get_text('tab_database')
    ]

def get_platform_features(platform):
    """Get translated platform features list"""
    key = f"{platform.lower()}_features"
    return get_text(key, [])

def get_usage_steps():
    """Get translated usage steps"""
    return get_text('usage_steps', [])

def get_vlm_features():
    """Get translated VLM features"""
    return get_text('vlm_features', [])

def show_success_message(key, **kwargs):
    """Show success message in current language"""
    st.success(get_text(key, **kwargs))

def show_error_message(key, **kwargs):
    """Show error message in current language"""
    st.error(get_text(key, **kwargs))

def show_warning_message(key, **kwargs):
    """Show warning message in current language"""
    st.warning(get_text(key, **kwargs))

def show_info_message(key, **kwargs):
    """Show info message in current language"""
    st.info(get_text(key, **kwargs))