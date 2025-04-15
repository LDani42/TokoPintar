import os
import json
import streamlit as st

TRANSLATION_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'i18n', 'app_translations.json')

# Cache translations in memory
_translations = None

def load_translations():
    global _translations
    if _translations is None:
        with open(TRANSLATION_PATH, encoding='utf-8') as f:
            _translations = json.load(f)
    return _translations

def tr(key, **kwargs):
    translations = load_translations()
    lang = st.session_state.get('language', 'English')
    lang_code = 'id' if lang == 'Bahasa Indonesia' else 'en'
    value = translations.get(lang_code, {}).get(key, key)
    if kwargs:
        return value.format(**kwargs)
    return value
