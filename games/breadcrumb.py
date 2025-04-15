import streamlit as st
import time
import random
from games.game_registry import get_game_info

def show_game_breadcrumb(game_id):
    """Show a breadcrumb navigation for a game.
    
    Args:
        game_id (str): The game identifier
    """
    # Get game info for display name
    game_info = get_game_info(game_id)
    game_name = game_info.get("title", game_id) if game_info else game_id
    
    # Set up breadcrumb items
    breadcrumb_items = [
        ("Home", False),
        ("Games", False),
        (game_name, True)
    ]
    
    # Show breadcrumb - directly implemented to avoid import issues
    breadcrumb_html = '<nav aria-label="breadcrumb"><ol class="breadcrumb">'
    
    for i, (name, is_active) in enumerate(breadcrumb_items):
        if is_active:
            breadcrumb_html += f'<li class="breadcrumb-item active">{name}</li>'
        else:
            # Use anchor with javascript void to avoid page reload but make it look clickable
            breadcrumb_html += f'<li class="breadcrumb-item"><a href="javascript:void(0);">{name}</a></li>'
    
    breadcrumb_html += '</ol></nav>'
    st.markdown(breadcrumb_html, unsafe_allow_html=True)
    
    # Add a back button with a stable key
    col1, col2 = st.columns([1, 3])
    with col1:
        back_button_key = f"back_from_{game_id}"
        if st.button("\u2190 Back to Games", key=back_button_key):
            st.session_state.current_game = None
            st.session_state.current_subsection = None
            st.rerun()
