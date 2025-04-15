"""
Toko Pintar - Financial Literacy Game for Small Retailers.
Main Streamlit application file.
"""
import streamlit as st
import time
import os

# Import utilities
from utils.config import get_config, set_config, initialize_product_database
from utils.db import db, initialize_session_from_db, save_session_state_to_db
from utils.skills import initialize_skills, update_shop_level

# Import components
from components.navigation import (
    set_page_config, 
    inject_custom_css, 
    language_selector, 
    show_header, 
    show_welcome_screen,
    show_main_menu_tabs
)
from components.scoreboard import display_score_sidebar
from components.shop_display import display_shop_upgrade_animation
from components.sidebar import collapsible_sidebar, sidebar_quick_navigation, init_sidebar_state
from components.user_login import show_user_login
from games.breadcrumb import show_game_breadcrumb

# Import games with explicit imports to avoid circular references
import games
from games import get_game_function, get_all_games

# Initialize app
def init_app():
    """Initialize the application."""
    # Set page config - this must be called first
    set_page_config()
    
    # Inject custom CSS
    assets_path = os.path.join(os.path.dirname(__file__), 'assets', 'styles')
    if os.path.exists(assets_path):
        inject_custom_css()
    
    # Initialize product database if needed
    initialize_product_database()
    
    # Initialize session state variables if needed
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.player_name = ""
        st.session_state.total_score = 0
        st.session_state.current_game = None
        st.session_state.game_history = []
        st.session_state.achievements = []
        st.session_state.shop_level = 1
        
        # Initialize skills
        initialize_skills()

# Main app flow
def main():
    """Main application entry point."""
    # Initialize the app
    init_app()

    # --- USER LOGIN/REGISTRATION ---
    if "user_id" not in st.session_state:
        show_user_login()
        st.stop()
    # --- END USER LOGIN/REGISTRATION ---

    # Inject inventory game CSS after page config
    import os
    css_path = os.path.join('assets', 'styles', 'components', 'inventory_game.css')
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Handle header click to return to main menu
    if st.session_state.get('return_to_main_menu', False):
        # Clear any current game state
        st.session_state.current_game = None
        # Reset the flag
        st.session_state.return_to_main_menu = False
        # Force rerun to show main menu
        st.rerun()
    
    # Add a header click listener to capture click events
    st.markdown("""
    <script>
    // Handle return_to_main_menu message from header click
    window.addEventListener('message', function(event) {
        if (event.data.type === 'streamlit:setComponentValue' && event.data.key === 'return_to_main_menu') {
            // This will get picked up by Streamlit to set session state
        }
    });
    </script>
    """, unsafe_allow_html=True)
    
    # The hamburger menu is loaded via set_page_config() but hidden during onboarding using CSS
    
    # --- DEBUG: Show current navigation state ---
    st.write("DEBUG: current_game =", st.session_state.get("current_game"))

    # --- Always render sidebar for logged-in users ---
    if st.session_state.get("player_name"):
        init_sidebar_state()  # Ensure sidebar state is initialized and CSS injected
        collapsible_sidebar(sidebar_quick_navigation)

    # --- Main navigation logic ---
    if st.session_state.get("current_game") is None:
        # Show main menu
        show_header()
        show_main_menu_tabs()
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        from components.progress_dashboard import (
            display_progress_indicator, 
            display_shop_growth_visualization,
            show_save_progress_button
        )
        display_progress_indicator()
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        display_shop_growth_visualization()
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        show_save_progress_button()
    else:
        # Show breadcrumb and game
        show_game_breadcrumb(st.session_state.current_game)
        st.markdown("---")
        game_function = get_game_function(st.session_state.current_game)
        if game_function:
            try:
                game_id = st.session_state.current_game
                if game_id == "inventory_game" and "inventory_game" not in st.session_state:
                    from games.inventory_game import initialize_game_state
                    initialize_game_state(1)
                elif game_id == "change_making" and "change_making" not in st.session_state:
                    from games.change_making import initialize_transaction
                    initialize_transaction(1)
                elif game_id == "margin_calculator" and "margin_calculator" not in st.session_state:
                    from games.margin_calculator import initialize_margin_challenge
                    initialize_margin_challenge(1)
                game_function()
            except Exception as e:
                st.error(f"Error running game: {e}")
                import traceback
                st.code(traceback.format_exc())
        else:
            st.error(f"Game '{st.session_state.current_game}' not found!")
            st.session_state.current_game = None
            st.button("Return to Main Menu", on_click=lambda: st.rerun())

    # Show debug page if debug mode is enabled
    if get_config("debug.enabled"):
        from utils.debug import show_debug_page
        from utils.config import generate_widget_key
        if st.sidebar.button("Debug Page", key=generate_widget_key("button", "debug_page")):
            st.session_state.show_debug_page = True
        
        if st.session_state.get("show_debug_page", False):
            show_debug_page()
    
    # Save session state periodically
    if hasattr(st.session_state, 'user_id'):
        save_session_state_to_db()

# Run the app
if __name__ == "__main__":
    main()