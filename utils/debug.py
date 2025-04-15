"""
Debug utilities for Toko Pintar application.
This module provides debugging tools and information display.
"""
import streamlit as st
import json
import os
import sys
import traceback
from utils.config import get_config, set_config, generate_widget_key

def show_debug_page():
    """Show debugging information page."""
    st.title("Toko Pintar Debug Page")
    
    # Add exit button
    if st.button("Exit Debug Mode", key=generate_widget_key("button", "exit_debug")):
        st.session_state.show_debug_page = False
        st.rerun()
    
    # Get app version
    version = get_config("app.version") or "Unknown"
    st.write(f"Application Version: {version}")
    
    # System information
    st.header("System Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"Python Version: {sys.version.split()[0]}")
        st.write(f"Streamlit Version: {st.__version__}")
        st.write(f"Operating System: {os.name.upper()}")
    
    with col2:
        st.write(f"Language: {get_config('app.default_language')}")
        st.write(f"Debug Mode: {get_config('debug.enabled')}")
    
    # Session state information
    st.header("Session State")
    
    # Create a function to filter sensitive data
    def filter_sensitive_data(key, value):
        sensitive_keys = ["password", "token", "secret", "key", "auth"]
        if any(s in key.lower() for s in sensitive_keys):
            return "********"
        return value
    
    # Filter session state for display
    filtered_state = {}
    for key, value in st.session_state.items():
        filtered_state[key] = filter_sensitive_data(key, value)
    
    # Display session state
    with st.expander("Session State Variables", expanded=False):
        st.json(filtered_state)
    
    # Widget key tester
    st.header("Widget Key Generator")
    st.write("Test creating unique widget keys to avoid duplications")
    
    col1, col2 = st.columns(2)
    
    with col1:
        prefix = st.text_input("Prefix", value="button", key=generate_widget_key("text_input", "debug_prefix"))
        identifier = st.text_input("Identifier", value="test", key=generate_widget_key("text_input", "debug_identifier"))
    
    with col2:
        key1 = generate_widget_key(prefix, identifier)
        key2 = generate_widget_key(prefix, identifier)
        
        st.write(f"Generated Key 1: `{key1}`")
        st.write(f"Generated Key 2: `{key2}`")
        
        if key1 == key2:
            st.error("WARNING: Generated keys are identical! This indicates a problem with the key generation.")
        else:
            st.success("Keys are unique as expected.")
    
    # Error logging
    st.header("Error Logging")
    with st.expander("Recent Errors"):
        try:
            with open("error_log.txt", "r") as f:
                errors = f.read()
                if errors:
                    st.text(errors)
                else:
                    st.info("No errors have been logged.")
        except FileNotFoundError:
            st.info("No error log found.")
    
    # Configuration viewer/editor
    st.header("Configuration")
    with st.expander("Current Configuration"):
        config = get_config()
        st.json(config)
    
    # Tools
    st.header("Tools")
    
    # Clear session state
    if st.button("Clear Session State", key=generate_widget_key("button", "clear_session_state")):
        # Keep a few core items
        keep_keys = ["app_config"]
        preserved = {k: st.session_state[k] for k in keep_keys if k in st.session_state}
        
        # Clear session state
        for key in list(st.session_state.keys()):
            if key not in keep_keys:
                del st.session_state[key]
        
        # Restore preserved keys
        for key, value in preserved.items():
            st.session_state[key] = value
        
        st.success("Session state cleared (except for core configuration).")
        st.rerun()

def log_error(error, context=None):
    """Log an error to the error log file.
    
    Args:
        error (Exception): The error to log
        context (str, optional): Additional context. Defaults to None.
    """
    try:
        with open("error_log.txt", "a") as f:
            f.write(f"--- ERROR at {__import__('datetime').datetime.now()} ---\n")
            if context:
                f.write(f"Context: {context}\n")
            f.write(f"Error: {str(error)}\n")
            f.write(traceback.format_exc())
            f.write("\n\n")
    except Exception as e:
        print(f"Error logging error: {e}")