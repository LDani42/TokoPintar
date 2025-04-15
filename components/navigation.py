"""
Navigation components for Toko Pintar application.
"""
import streamlit as st
import time
from utils.config import get_config, set_config, get_translation, generate_widget_key
from components.progress_dashboard import show_progress_dashboard
from components.transitions import slide_transition, section_transition
from utils.i18n import tr

def inject_custom_css():
    """Inject custom CSS into the Streamlit app."""
    import os
    import glob
    
    # Get base directory
    base_dir = os.path.dirname(os.path.dirname(__file__))
    css_files = []
    
    # ORDER MATTERS HERE:
    # 1. Theme variables (must be first so other CSS can use the variables)
    # 2. Component CSS files
    # 3. Main CSS (for overrides and global styles)
    
    # 1. Add theme.css first - CRITICAL for CSS variables
    theme_css_path = os.path.join(base_dir, 'assets', 'styles', 'theme.css')
    if os.path.exists(theme_css_path):
        with open(theme_css_path) as f:
            theme_css = f.read()
            # Inject theme variables immediately to ensure they're available
            st.markdown(f'<style>{theme_css}</style>', unsafe_allow_html=True)
    
    # 2. Add all component CSS files
    component_css_path = os.path.join(base_dir, 'assets', 'styles', 'components', '*.css')
    component_files = sorted(glob.glob(component_css_path))
    
    # 3. Add main.css last for overrides
    main_css_path = os.path.join(base_dir, 'assets', 'styles', 'main.css')
    if os.path.exists(main_css_path):
        component_files.append(main_css_path)
    
    # Read and combine all component CSS files and main.css
    combined_css = ""
    for css_file in component_files:
        try:
            with open(css_file) as f:
                combined_css += f.read() + "\n\n"
        except Exception as e:
            st.warning(f"Error loading CSS file {css_file}: {e}")
    
    # Add JavaScript to completely remove all toolbar elements
    # This is the most aggressive approach but should solve the issue
    toolbar_js = """
    <script>
    // Run immediately and after a delay to ensure it catches dynamically added elements
    function removeToolbars() {
        // Find and remove all toolbar-like elements
        const toolbars = document.querySelectorAll('[data-testid="stToolbar"], [data-testid="baseToolbar"], header[data-testid="stHeader"]');
        toolbars.forEach(function(toolbar) {
            if (toolbar && toolbar.parentNode) {
                toolbar.parentNode.removeChild(toolbar);
            }
        });
        
        // Also try to find any containers that might hold these elements
        const containers = document.querySelectorAll('.stToolbar');
        containers.forEach(function(container) {
            if (container && container.parentNode) {
                container.style.display = 'none';
                container.style.height = '0';
                container.style.margin = '0';
                container.style.padding = '0';
            }
        });
    }
    
    // Run immediately
    removeToolbars();
    
    // And after a short delay to catch any that might appear later
    setTimeout(removeToolbars, 100);
    setTimeout(removeToolbars, 500);
    setTimeout(removeToolbars, 1000);
    
    // Also watch for DOM changes to catch any toolbars added later
    const observer = new MutationObserver(function(mutations) {
        removeToolbars();
    });
    
    // Start observing
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """
    
    # Add the JavaScript
    st.markdown(toolbar_js, unsafe_allow_html=True)
    
    # Add responsive styles to hide header and step progress on mobile
    mobile_css = """
    /* Mobile-specific styles - more aggressive approach */
    @media (max-width: 768px) {
        /* Hide main header and subtitle on mobile */
        .main-header, .sub-header {
            display: none !important;
            margin: 0 !important;
            padding: 0 !important;
            height: 0 !important;
        }
        
        /* Hide step progress indicators on mobile */
        .onboarding-steps-mobile-hide {
            display: none !important;
            margin: 0 !important;
            padding: 0 !important;
            height: 0 !important;
        }
        
        /* Remove any margin/padding from containers that would create white space */
        .onboarding-container > div:empty,
        .onboarding-container > div:first-child {
            margin: 0 !important;
            padding: 0 !important;
            height: 0 !important;
        }
        
        /* Make column containers take full width on mobile */
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
        
        /* Improve fitting for mobile screens */
        .block-container {
            padding-top: 0 !important;
            max-width: 100% !important;
            padding-left: 10px !important;
            padding-right: 10px !important;
        }
        
        /* Remove the three grey lines at the top */
        [data-testid="stToolbar"], [data-testid="baseToolbar"] {
            display: none !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            opacity: 0 !important;
            visibility: hidden !important;
            position: absolute !important;
        }
        
        /* Fix header toolbar and menu */
        header[data-testid="stHeader"], div[data-testid="stHeader"] {
            display: none !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            opacity: 0 !important;
            visibility: hidden !important;
            position: absolute !important;
        }
        
        /* Special extreme measures to remove all toolbar-like elements */
        div:has(> [data-testid="stToolbar"]),
        div:has(> [data-testid="baseToolbar"]) {
            display: none !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove top margin - this pushes everything up */
        .main .element-container:first-child {
            margin-top: 0 !important;
        }
        
        /* Game Card improvements for mobile */
        .game-card {
            padding: 10px !important;
            margin-bottom: 10px !important;
        }
        
        /* Remove excess margin from streamlit containers */
        [data-testid="stVerticalBlock"] > div {
            gap: 10px !important;
        }
        
        /* Improve stApp container */
        .main .stApp {
            max-width: 100vw !important;
            padding-top: 0 !important;
        }
        
        /* Remove sidebar toggle button whitespace */
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        
        /* Adjust font sizes for mobile */
        h1 {
            font-size: 1.5rem !important;
        }
        
        h2 {
            font-size: 1.3rem !important;
        }
        
        h3 {
            font-size: 1.1rem !important;
        }
        
        p, div {
            font-size: 0.9rem !important;
        }
        
        /* Progress dashboard adjustments for mobile */
        .progress-dashboard {
            padding: 10px !important;
            margin-bottom: 10px !important;
        }
        
        .progress-dashboard-title {
            font-size: 1rem !important;
        }
        
        .progress-category {
            margin-bottom: 8px !important;
        }
        
        /* Fix breadcrumbs on mobile */
        .breadcrumb {
            padding: 5px 0 !important;
            font-size: 0.8rem !important;
            margin-bottom: 5px !important;
        }
        
        /* Remove top padding - important for vertical space */
        section[data-testid="stSectionContainer"] {
            padding-top: 0 !important;
        }
        
        /* Fix for extra divs that might cause spacing issues */
        div[data-testid="stDecoration"], 
        div[data-testid="stStatusWidget"] {
            display: none !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }
    }
    """
    
    # Combine all CSS
    combined_css += mobile_css
    
    # Inject the combined CSS
    if combined_css:
        st.markdown(f'<style>{combined_css}</style>', unsafe_allow_html=True)
    else:
        st.warning("Could not load component CSS files")

def set_page_config():
    """Set Streamlit page configuration."""
    # Always use collapsed as the initial sidebar state
    sidebar_state = "collapsed"
    
    # Set the page config with the determined sidebar state
    st.set_page_config(
        page_title=get_config("app.title") or "Toko Pintar - Financial Literacy Game",
        page_icon="🏪",
        layout="wide",
        initial_sidebar_state=sidebar_state
    )
    
    # Add mobile-friendly hamburger menu styling with animation
    st.markdown("""
    <style>
    /* Style for our custom hamburger menu button */
    .hamburger-menu {
        position: fixed;
        top: 10px;
        left: 10px;
        width: 45px;
        height: 45px;
        background-color: #FF7043;
        border-radius: 50%;
        z-index: 9999;
        box-shadow: 0 3px 6px rgba(0,0,0,0.2);
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
        transition: all 0.3s ease;
    }
    
    .hamburger-menu:hover {
        background-color: #E64A19;
        transform: scale(1.05);
    }
    
    .hamburger-menu:active {
        transform: scale(0.95);
    }
    
    /* Animated hamburger icon */
    .hamburger-lines {
        width: 22px;
        height: 20px;
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .hamburger-line {
        display: block;
        height: 3px;
        width: 100%;
        background-color: white;
        border-radius: 3px;
        transition: all 0.3s ease;
    }
    
    /* When sidebar is open, change hamburger to X */
    .hamburger-menu.active .hamburger-line:nth-child(1) {
        transform: translateY(8px) rotate(45deg);
    }
    
    .hamburger-menu.active .hamburger-line:nth-child(2) {
        opacity: 0;
    }
    
    .hamburger-menu.active .hamburger-line:nth-child(3) {
        transform: translateY(-8px) rotate(-45deg);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a dedicated Streamlit component that will toggle the sidebar correctly
    st.markdown("""
    <style>
    /* Style for the hamburger button as a div without link functionality */
    #streamlit-sidebar-toggle-btn {
        position: fixed;
        top: 10px;
        left: 10px;
        width: 45px;
        height: 45px;
        background-color: #FF7043;
        border-radius: 50%;
        z-index: 9999;
        box-shadow: 0 3px 6px rgba(0,0,0,0.2);
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
        transition: all 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add the hamburger menu button to the top-left corner
    st.markdown("""
    <style>
    .hamburger-menu-button {
        position: fixed;
        top: 60px; /* Moved lower from 10px to 60px */
        left: 10px;
        width: 45px;
        height: 45px;
        background-color: #FF7043;
        border-radius: 50%;
        z-index: 9999;
        box-shadow: 0 3px 6px rgba(0,0,0,0.2);
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
        transition: all 0.3s ease;
    }
    
    .hamburger-menu-button:hover {
        background-color: #E64A19;
        transform: scale(1.05);
    }
    
    .hamburger-menu-button:active {
        transform: scale(0.95);
    }
    
    .hamburger-lines {
        width: 22px;
        height: 16px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
    }
    
    .hamburger-line {
        display: block;
        height: 3px;
        width: 100%;
        background-color: white;
        border-radius: 3px;
        transition: all 0.3s ease;
    }
    
    /* Animated X when menu is open */
    .hamburger-menu-button.open .hamburger-line:nth-child(1) {
        transform: translateY(6px) rotate(45deg);
        background-color: white;
    }
    
    .hamburger-menu-button.open .hamburger-line:nth-child(2) {
        opacity: 0;
        background-color: white;
    }
    
    .hamburger-menu-button.open .hamburger-line:nth-child(3) {
        transform: translateY(-6px) rotate(-45deg);
        background-color: white;
    }
    
    /* Make sure lines are properly spaced */
    .hamburger-lines {
        height: 18px;
    }
    
    /* Override any conflicting styles */
    .hamburger-menu-button, .hamburger-lines, .hamburger-line {
        box-sizing: border-box !important;
    }
    
    /* Keep Streamlit's default hamburger button functional but visually hidden */
    [data-testid="collapsedControl"] {
        opacity: 0 !important;
        position: absolute !important;
        left: -9999px !important;
        pointer-events: auto !important; /* Ensure it can still be clicked by our JS */
    }
    </style>
    
    <!-- Improved Streamlit-friendly hamburger button -->
    <div class="hamburger-menu-button" id="custom-hamburger-btn">
        <div class="hamburger-lines">
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
        </div>
    </div>
    
    <!-- Add CSS to hide hamburger more aggressively during onboarding -->
    <style>
    /* Very aggressive styles to hide hamburger menu during onboarding */
    body.onboarding-active #custom-hamburger-btn,
    body.onboarding-active .hamburger-menu-button,
    body.onboarding-active [id*="hamburger"],
    body.onboarding-active [class*="hamburger"],
    body.onboarding-active [data-testid="collapsedControl"],
    body.onboarding-active .stSidebar > div:first-child {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        position: absolute !important;
        left: -9999px !important;
        height: 0 !important;
        width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        overflow: hidden !important;
    }
    
    /* Completely hide sidebar without affecting main content layout */
    [data-testid="stSidebar"][aria-expanded="false"] {
        visibility: hidden !important;
        width: 0 !important;
        position: fixed !important;
        z-index: 999 !important;
        opacity: 0 !important;
        transition: all 0.3s ease-in-out;
    }
        
    /* Sidebar overlay when expanded */
    [data-testid="stSidebar"][aria-expanded="true"] {
        visibility: visible !important;
        position: fixed !important;
        z-index: 999 !important;
        width: 21rem !important;
        opacity: 1 !important;
        transition: all 0.3s ease-in-out;
    }
    
    /* Ensure main content uses full width */
    .main .block-container {
        max-width: calc(100% - 1rem) !important;
        padding-left: 1rem !important;
        padding-right: 0 !important; 
    }
    
    /* Mobile-specific sidebar styling - full width */
    @media (max-width: 768px) {
        [data-testid="stSidebar"][aria-expanded="true"] {
            width: 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
            margin-left: 0 !important;
            z-index: 1000 !important;
            background-color: rgba(255, 255, 255, 0.98) !important;
        }
        
        /* Ensure content layout for mobile */
        .main .block-container {
            max-width: 100% !important;
            padding-left: 10px !important;
            padding-right: 10px !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        
        /* Make hamburger button more prominent on mobile */
        .hamburger-menu-button {
            width: 50px !important;
            height: 50px !important;
            box-shadow: 0 3px 10px rgba(0,0,0,0.2) !important;
        }
    }
    </style>
    
    <script>
    // Function to track sidebar state and update hamburger appearance
    function updateHamburgerState() {
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        const hamburger = document.getElementById('custom-hamburger-btn');
        
        if (sidebar && hamburger) {
            // Check if sidebar is expanded
            const isExpanded = sidebar.getAttribute('aria-expanded') === 'true';
            
            // Update hamburger appearance
            if (isExpanded) {
                hamburger.classList.add('open');
            } else {
                hamburger.classList.remove('open');
            }
        }
    }
    
    // Function to add event listener with improved state tracking
    function setupHamburgerMenu() {
        // Find our custom button
        const btn = document.getElementById('custom-hamburger-btn');
        if (btn) {
            // Remove any existing listeners first to avoid duplicates
            btn.replaceWith(btn.cloneNode(true));
            
            // Get the fresh reference
            const newBtn = document.getElementById('custom-hamburger-btn');
            
            if (newBtn) {
                // Add the click handler
                newBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Find and click Streamlit's sidebar toggle button
                    const sidebarBtn = document.querySelector('[data-testid="collapsedControl"] button');
                    if (sidebarBtn) {
                        sidebarBtn.click();
                        
                        // Update the hamburger state after a brief delay to allow Streamlit to update
                        setTimeout(updateHamburgerState, 100);
                    }
                    
                    return false;
                });
            }
        }
        
        // Initial state update
        updateHamburgerState();
    }
    
    // Try immediately on load
    document.addEventListener('DOMContentLoaded', setupHamburgerMenu);
    
    // Also try after a short delay (for dynamic loading)
    setTimeout(setupHamburgerMenu, 500);
    
    // And try again after a longer delay (for slower connections)
    setTimeout(setupHamburgerMenu, 2000);
    
    // Set up MutationObserver to detect DOM changes and update state
    const observer = new MutationObserver(function(mutations) {
        setupHamburgerMenu();
        updateHamburgerState();
    });
    
    // Start observing once DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        observer.observe(document.body, { 
            childList: true, 
            subtree: true,
            attributes: true,
            attributeFilter: ['aria-expanded']
        });
    });
    </script>
    """, unsafe_allow_html=True)

def language_selector():
    """Display a language selector in the sidebar."""
    languages = {
        "en": "English",
        "id": "Bahasa Indonesia"
    }
    
    current_lang = get_config("app.default_language") or "en"
    
    st.sidebar.title("Settings")
    selected_lang = st.sidebar.selectbox(
        "Language / Bahasa",
        options=list(languages.keys()),
        format_func=lambda x: languages[x],
        index=list(languages.keys()).index(current_lang),
        key="navigation_language_selector_stable"
    )
    
    if selected_lang != current_lang:
        set_config("app.default_language", selected_lang)
        st.rerun()

def show_header():
    """Display the application header."""
    # First insert a placeholder div that can be targeted by CSS
    # This will help make sure we can completely hide this on mobile
    st.markdown('<div id="app-header-container" class="app-header-container">', unsafe_allow_html=True)
    
    lang = get_config("app.default_language") or "en"
    title = "Toko Pintar" if lang == "en" else "Toko Pintar"
    subtitle = "Financial Literacy Game for Small Retailers" if lang == "en" else "Game Literasi Keuangan untuk Pedagang Kecil"
    
    # Add the actual header content with classes for styling and make it clickable
    st.markdown(f'<h1 class="main-header" style="cursor: pointer;" id="clickable-header">{title}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="center-text sub-header" style="cursor: pointer;" id="clickable-header-subtitle">{subtitle}</p>', unsafe_allow_html=True)
    
    # Add JavaScript to handle the click events
    js_code = """
    <script>
    // JavaScript to handle header click
    document.addEventListener('DOMContentLoaded', function() {
        const header = document.getElementById('clickable-header');
        const subtitle = document.getElementById('clickable-header-subtitle');
        
        function handleHeaderClick() {
            // Clear current game and return to main menu
            window.parent.postMessage({
                type: "streamlit:setComponentValue",
                value: true,
                dataType: "bool",
                key: "return_to_main_menu"
            }, "*");
        }
        
        if (header) {
            header.addEventListener('click', handleHeaderClick);
        }
        
        if (subtitle) {
            subtitle.addEventListener('click', handleHeaderClick);
        }
    });
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)
    
    # Close the container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add a footer version of the header for mobile only - also make it clickable
    st.markdown(f"""
    <div class="mobile-footer-header" id="mobile-clickable-header" style="cursor: pointer;">
        <h2>{title}</h2>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add JavaScript to handle mobile header click
    mobile_js = """
    <script>
    // JavaScript to handle mobile header click
    document.addEventListener('DOMContentLoaded', function() {
        const mobileHeader = document.getElementById('mobile-clickable-header');
        if (mobileHeader) {
            mobileHeader.addEventListener('click', function() {
                // Use same handler as desktop header
                window.parent.postMessage({
                    type: "streamlit:setComponentValue",
                    value: true,
                    dataType: "bool",
                    key: "return_to_main_menu"
                }, "*");
            });
        }
    });
    </script>
    """
    st.markdown(mobile_js, unsafe_allow_html=True)
    
    # Add the mobile footer header styles
    style_html = """
    <style>
    .mobile-footer-header {
        display: none;
        text-align: center;
        padding: 15px 0;
        margin-top: 30px;
        border-top: 1px solid #eee;
    }
    
    @media (max-width: 768px) {
        .mobile-footer-header {
            display: block;
        }
        .app-header-container {
            display: none !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }
    }
    </style>
    """
    st.markdown(style_html, unsafe_allow_html=True)

def show_game_card(title, description, button_text, game_id, skill_key):
    """Display a game card with progress bar.
    
    Args:
        title (str): Game title
        description (str): Game description
        button_text (str): Text for the play button
        game_id (str): ID of the game
        skill_key (str): Key of the skill this game improves
    
    Returns:
        bool: True if the game button was clicked
    """
    # Create a unique container ID for this game card
    container_id = f"game-card-{game_id}"
    st.markdown(f'<div class="game-card" id="{container_id}">', unsafe_allow_html=True)
    st.markdown(f'<p class="game-title">{title}</p>', unsafe_allow_html=True)
    st.write(description)
    
    # Display skill progress
    if 'skill_levels' in st.session_state and skill_key in st.session_state.skill_levels:
        skill_level = st.session_state.skill_levels[skill_key]
        max_level = get_config("gameplay.max_skill_level") or 5
        progress = min(1.0, skill_level / max_level)
        st.progress(progress)
    else:
        st.progress(0)
    
    # Create a unique button key
    button_key = f"main_tab_play_{game_id}_{skill_key}"
    
    # Play button with guaranteed unique key
    clicked = st.button(button_text, key=button_key)
    
    # Close the game card container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Debug information in case of click
    if clicked:
        # Add a confirmation that will be visible to the user
        st.success(f"Starting game: {game_id}")
        
        # Set session state variables
        st.session_state.current_game = game_id
        st.session_state.current_subsection = title
        
        # Force an immediate rerun to activate the game
        st.rerun()
    
    return clicked

def show_achievement(achievement):
    """Display an achievement card.
    
    Args:
        achievement (dict): Achievement data
    """
    # Determine badge type based on achievement ID
    badge_type = "inventory"
    if "cash" in achievement["id"] or "math" in achievement["id"]:
        badge_type = "cash"
    elif "price" in achievement["id"] or "margin" in achievement["id"] or "financial" in achievement["id"]:
        badge_type = "pricing"
    elif "customer" in achievement["id"]:
        badge_type = "customer"
    elif "book" in achievement["id"] or "accounting" in achievement["id"]:
        badge_type = "bookkeeping"
    
    # Determine icon based on achievement
    icon = "🏆"
    if "inventory" in achievement["id"]:
        icon = "📦"
    elif "cash" in achievement["id"] or "math" in achievement["id"]:
        icon = "💰"
    elif "margin" in achievement["id"] or "financial" in achievement["id"]:
        icon = "📊"
    elif "customer" in achievement["id"]:
        icon = "🤝"
    elif "book" in achievement["id"]:
        icon = "📒"
    elif "first" in achievement["id"]:
        icon = "🎯"
    elif "player" in achievement["id"]:
        icon = "🎮"
    elif "shop" in achievement["id"]:
        icon = "🏪"
    
    # Check if this is a new achievement (earned in the past day)
    is_new = False
    if "earned_at" in achievement:
        from datetime import datetime, timedelta
        try:
            earned_at = datetime.strptime(achievement["earned_at"], "%Y-%m-%d %H:%M:%S")
            is_new = (datetime.now() - earned_at) < timedelta(days=1)
        except:
            pass
    
    # Generate the badge HTML
    new_class = "achievement-badge-new" if is_new else ""
    
    st.markdown(f"""
    <div class="achievement-card">
        <div class="achievement-badge achievement-badge-{badge_type} {new_class}">
            {icon}
            <div class="achievement-badge-tooltip">{achievement['name']}</div>
        </div>
        <div class="achievement-details">
            <span class="achievement-name">{achievement['name']}</span>
            <p class="achievement-description">{achievement['description']}</p>
            <span class="achievement-date">Earned: {achievement.get('earned_at', 'N/A')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_main_menu_tabs():
    """Display tabs for the main menu.
    
    Returns:
        str: Selected tab
    """
    lang = get_config("app.default_language") or "en"
    
    # Show breadcrumbs for navigation - but avoid circular imports
    # Import directly inside the function to avoid circular imports
    if 'current_section' in st.session_state and 'current_subsection' in st.session_state:
        main_section = st.session_state.current_section
        sub_section = st.session_state.current_subsection
        
        breadcrumb_items = [
            ("Home", main_section is None),
            (main_section, sub_section is None),
            (sub_section, True)
        ]
        
        # Filter out None values
        breadcrumb_items = [(item, active) for item, active in breadcrumb_items if item]
        
        # Display breadcrumb navigation - implement directly to avoid import issues
        breadcrumb_html = '<nav aria-label="breadcrumb"><ol class="breadcrumb">'
        
        for i, (name, is_active) in enumerate(breadcrumb_items):
            if is_active:
                breadcrumb_html += f'<li class="breadcrumb-item active">{name}</li>'
            else:
                # Use anchor with javascript void to avoid page reload but make it look clickable
                breadcrumb_html += f'<li class="breadcrumb-item"><a href="javascript:void(0);">{name}</a></li>'
        
        breadcrumb_html += '</ol></nav>'
        st.markdown(breadcrumb_html, unsafe_allow_html=True)
    
    # Add custom tab styling
    st.markdown("""
    <style>
    /* Improve tab styling for better visibility */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #f2f2f2;
        border-radius: 4px;
        padding: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FF7043 !important;
        color: white !important;
    }
    
    @media (max-width: 768px) {
        /* Smaller tabs on mobile */
        .stTabs [data-baseweb="tab"] {
            padding: 6px 10px;
            font-size: 0.9rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    tabs = {
        "games": tr('games'),
        "learning": tr('learning_paths'),
        "shop": tr('my_shop'),
        "skills": tr('skills'),
        "achievements": tr('achievements')
    }
    
    # Create tabs with language-specific labels
    tab_values = list(tabs.values())
    tab1, tab2, tab3, tab4, tab5 = st.tabs(tab_values)
    
    # Track current section in session state for breadcrumb navigation
    if 'current_section' not in st.session_state:
        st.session_state.current_section = list(tabs.values())[0]
        st.session_state.current_subsection = None
    
    # Get previous section for animation direction
    prev_section = st.session_state.get('current_section', None)
    
    with tab1:
        new_section = list(tabs.values())[0]
        st.session_state.current_section = new_section
        # Determine animation direction
        direction = section_transition(prev_section, new_section)
        # Wrap content in slide transition
        slide_transition(direction, show_games_tab)
    
    with tab2:
        new_section = list(tabs.values())[1]
        st.session_state.current_section = new_section
        # Determine animation direction
        direction = section_transition(prev_section, new_section)
        # Wrap content in slide transition
        slide_transition(direction, show_learning_paths_tab)
    
    with tab3:
        new_section = list(tabs.values())[2]
        st.session_state.current_section = new_section
        # Determine animation direction
        direction = section_transition(prev_section, new_section)
        # Wrap content in slide transition
        slide_transition(direction, show_shop_tab)
    
    with tab4:
        new_section = list(tabs.values())[3]
        st.session_state.current_section = new_section
        # Determine animation direction
        direction = section_transition(prev_section, new_section)
        # Wrap content in slide transition
        slide_transition(direction, show_skills_tab)
    
    with tab5:
        new_section = list(tabs.values())[4]
        st.session_state.current_section = new_section
        # Determine animation direction
        direction = section_transition(prev_section, new_section)
        # Wrap content in slide transition
        slide_transition(direction, show_achievements_tab)

def show_games_tab():
    """Display the games tab content."""
    st.markdown(f"### {tr('available_games')}")
    st.write(tr('choose_game'))
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        show_game_card(
            tr('inventory_counting'),
            tr('inventory_counting_desc'),
            tr('play_inventory_game'),
            "inventory_game",
            "inventory_management"
        )
    
    with col2:
        show_game_card(
            tr('change_making'),
            tr('change_making_desc'),
            tr('play_change_making'),
            "change_making",
            "cash_handling"
        )
    
    with col3:
        show_game_card(
            tr('margin_calculator'),
            tr('margin_calculator_desc'),
            tr('play_margin_calculator'),
            "margin_calculator",
            "pricing_strategy"
        )
    
    with col4:
        show_game_card(
            tr('simple_calculator'),
            tr('simple_calculator_desc'),
            tr('play_simple_calculator'),
            "simple_calculator",
            "pricing_strategy"
        )

def show_shop_tab():
    """Display the shop tab content."""
    if 'shop_level' not in st.session_state:
        st.session_state.shop_level = 1
    
    # Shop level display
    st.markdown(f'<p class="shop-level">{tr("shop_level")} {st.session_state.shop_level}</p>', unsafe_allow_html=True)
    
    # Show shop image based on level
    import os
    from utils.config import ROOT_DIR
    
    # Use local image paths
    shop_images = {
        1: os.path.join(ROOT_DIR, "assets", "images", "shop", "shop_level_1.png"),
        2: os.path.join(ROOT_DIR, "assets", "images", "shop", "shop_level_2.png"),
        3: os.path.join(ROOT_DIR, "assets", "images", "shop", "shop_level_3.png")
    }
    
    # Create placeholder images if they don't exist
    for level, image_path in shop_images.items():
        if not os.path.exists(image_path):
            # Generate a colored rectangle with text as placeholder
            import numpy as np
            from PIL import Image, ImageDraw, ImageFont
            
            # Create a blank image with a color based on level
            colors = {1: (200, 230, 255), 2: (220, 255, 220), 3: (255, 240, 200)}
            img = Image.new('RGB', (600, 200), colors.get(level, (240, 240, 240)))
            draw = ImageDraw.Draw(img)
            
            # Add text
            try:
                # Try to load a font, fall back to default if not available
                font = ImageFont.truetype("Arial", 24)
            except:
                font = ImageFont.load_default()
                
            level_text = f"{tr('shop_level')} {level}"
            # Different PIL versions have different methods
            try:
                text_width = draw.textlength(level_text, font=font)
            except AttributeError:
                # Fall back for older PIL versions
                text_width = font.getsize(level_text)[0]
            draw.text(((600-text_width)/2, 80), level_text, fill=(0, 0, 0), font=font)
            
            # Save the image
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            img.save(image_path)
    
    # Display the appropriate image
    level = min(3, max(1, st.session_state.shop_level))
    
    # Modified approach to use in-memory generated image
    captions = {
        1: tr('shop_level_1_caption'),
        2: tr('shop_level_2_caption'),
        3: tr('shop_level_3_caption')
    }
    
    # Generate image in memory to avoid file path issues
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    import io
    import base64
    
    # Create a blank image with a color based on level
    colors = {1: (200, 230, 255), 2: (220, 255, 220), 3: (255, 240, 200)}
    img = Image.new('RGB', (600, 200), colors.get(level, (240, 240, 240)))
    draw = ImageDraw.Draw(img)
    
    # Add text
    try:
        # Try to load a font, fall back to default if not available
        font = ImageFont.truetype("Arial", 24)
    except:
        font = ImageFont.load_default()
    
    level_text = f"{tr('shop_level')} {level}"
    # Different PIL versions have different methods
    try:
        text_width = draw.textlength(level_text, font=font)
    except AttributeError:
        # Fall back for older PIL versions
        try:
            text_width = font.getsize(level_text)[0]
        except:
            text_width = 100  # Fallback fixed width
    
    draw.text(((600-text_width)/2, 80), level_text, fill=(0, 0, 0), font=font)
    
    # Convert to bytes and display directly
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    byte_im = buf.getvalue()
    
    # Display using st.image with bytes
    st.image(byte_im, caption=captions[level])
    
    # Shop stats
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### {tr('shop_statistics')}")
        
        total_games = len(st.session_state.game_history) if hasattr(st.session_state, 'game_history') else 0
        avg_score = sum(g["score"] for g in st.session_state.game_history) / max(1, total_games) if hasattr(st.session_state, 'game_history') else 0
        total_score = st.session_state.total_score if hasattr(st.session_state, 'total_score') else 0
        
        st.markdown(f"""
        <div class="shop-stats">
            <p><strong>{tr('total_score')}:</strong> {total_score}</p>
            <p><strong>{tr('games_played')}:</strong> {total_games}</p>
            <p><strong>{tr('average_score')}:</strong> {avg_score:.1f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if hasattr(st.session_state, 'game_history') and st.session_state.game_history:
            st.markdown("### {tr('recent_activity')}")
            
            # Get game name mapping
            game_name_map = {
                "inventory_game": tr('inventory_counting'),
                "change_making": tr('change_making'),
                "margin_calculator": tr('margin_calculator'),
                "customer_service": tr('customer_service'),
                "cash_reconciliation": tr('cash_reconciliation'),
                "simple_accounting": tr('simple_accounting')
            }
            
            # Show latest games
            for game in list(reversed(st.session_state.game_history))[:5]:
                st.markdown(f"""
                <div style="padding: 5px; margin-bottom: 5px; border-bottom: 1px solid #eee;">
                    <strong>{game_name_map.get(game['game_id'], game['game_id'])}</strong>: 
                    Score {game['score']} | {game['timestamp']}
                </div>
                """, unsafe_allow_html=True)

def show_skills_tab():
    """Display the skills tab content."""
    st.markdown("### {tr('your_skills')}")
    
    from utils.skills import SKILL_DEFINITIONS, get_skill_name, get_skill_icon, get_skill_description
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    # Split skills into two groups
    skills = list(SKILL_DEFINITIONS.keys())
    first_half = skills[:len(skills)//2 + len(skills)%2]
    second_half = skills[len(skills)//2 + len(skills)%2:]
    
    # Display skills in first column
    with col1:
        for skill in first_half:
            show_skill_details(skill)
    
    # Display skills in second column
    with col2:
        for skill in second_half:
            show_skill_details(skill)

def show_skill_details(skill_id):
    """Display detailed information about a skill."""
    from utils.skills import get_skill_name, get_skill_icon, get_skill_description
    
    lang = get_config("app.default_language") or "en"
    skill_name = get_skill_name(skill_id, lang)
    skill_icon = get_skill_icon(skill_id)
    skill_desc = get_skill_description(skill_id, lang)
    
    # Get skill level and calculate stars
    skill_level = st.session_state.skill_levels.get(skill_id, 0) if hasattr(st.session_state, 'skill_levels') else 0
    max_level = get_config("gameplay.max_skill_level") or 5
    full_stars = int(skill_level)
    partial_star = skill_level - full_stars > 0
    empty_stars = max_level - full_stars - (1 if partial_star else 0)
    
    # Create star display
    star_display = "★" * full_stars
    if partial_star:
        star_display += "⭒"
    star_display += "☆" * empty_stars
    
    # Display skill information
    st.markdown(f"""
    <div style="padding: 10px; margin-bottom: 15px; background-color: #f7f7f7; border-radius: 5px;">
        <span style="font-size: 1.2rem; font-weight: bold; color: #1E88E5;">
            {skill_icon} {skill_name}
        </span><br>
        <span style="font-size: 1.1rem; color: #FFC107;">{star_display}</span>
        <div style="margin-top: 5px; font-size: 0.9rem;">
            {skill_desc}
        </div>
        <div style="margin-top: 5px;">
            <strong>{tr('level')}:</strong> {skill_level:.1f}/{max_level}
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_learning_paths_tab():
    """Display the learning paths tab content."""
    # Import the learning paths component
    from components.learning import show_learning_paths
    
    # Show learning paths
    show_learning_paths()

def show_achievements_tab():
    """Display the achievements tab content."""
    # Check if we should show certificates instead
    if "selected_certificate" in st.session_state and st.session_state.selected_certificate:
        from components.learning.certificates import show_certificate_details
        show_certificate_details(st.session_state.selected_certificate)
        return
    
    # First show certificates if any
    from components.learning.certificates import show_certificates_tab
    show_certificates_tab()
    
    # Then show achievements
    st.markdown(f"### {tr('your_achievements')}")
    
    # Get language
    lang = get_config("app.default_language") or "en"
    
    # Get all achievements from the achievements system
    from utils.achievements import ACHIEVEMENTS
    
    # Get earned achievement IDs
    earned_ids = set()
    if hasattr(st.session_state, 'achievements') and st.session_state.achievements:
        for achievement in st.session_state.achievements:
            if "id" in achievement:
                earned_ids.add(achievement["id"])
            elif "achievement_type" in achievement:
                earned_ids.add(achievement["achievement_type"])
    
    # If no achievements yet, show a message
    if not earned_ids:
        st.info(tr('no_achievements_yet'))
    
    # Create a container for earned achievements
    st.markdown("#### {tr('earned_achievements')}")
    earned_container = st.container()
    
    # Create a container for locked achievements
    st.markdown("#### {tr('locked_achievements')}")
    locked_container = st.container()
    
    # Display earned achievements
    with earned_container:
        if not earned_ids:
            st.write(tr('no_achievements_earned'))
        else:
            # Display all earned achievements
            for achievement in st.session_state.achievements:
                show_achievement(achievement)
    
    # Display locked achievements
    with locked_container:
        locked_count = 0
        for achievement in ACHIEVEMENTS:
            if achievement["id"] not in earned_ids:
                locked_count += 1
                # Create a simplified achievement dict for display
                achievement_data = {
                    "id": achievement["id"],
                    "name": achievement["name"] if lang == "en" else achievement["name_id"],
                    "description": achievement["description"] if lang == "en" else achievement["description_id"]
                }
                show_locked_achievement(achievement_data)
        
        if locked_count == 0:
            st.success(tr('all_achievements_unlocked'))

def show_locked_achievement(achievement):
    """Display a locked achievement.
    
    Args:
        achievement (dict): Achievement data
    """
    # Determine badge type based on achievement ID
    badge_type = "inventory"
    if "cash" in achievement["id"] or "math" in achievement["id"]:
        badge_type = "cash"
    elif "price" in achievement["id"] or "margin" in achievement["id"] or "financial" in achievement["id"]:
        badge_type = "pricing"
    elif "customer" in achievement["id"]:
        badge_type = "customer"
    elif "book" in achievement["id"] or "accounting" in achievement["id"]:
        badge_type = "bookkeeping"
    
    # Determine icon based on achievement
    icon = "🏆"
    if "inventory" in achievement["id"]:
        icon = "📦"
    elif "cash" in achievement["id"] or "math" in achievement["id"]:
        icon = "💰"
    elif "margin" in achievement["id"] or "financial" in achievement["id"]:
        icon = "📊"
    elif "customer" in achievement["id"]:
        icon = "🤝"
    elif "book" in achievement["id"]:
        icon = "📒"
    elif "first" in achievement["id"]:
        icon = "🎯"
    elif "player" in achievement["id"]:
        icon = "🎮"
    elif "shop" in achievement["id"]:
        icon = "🏪"
    
    # Generate the badge HTML
    st.markdown(f"""
    <div class="achievement-card">
        <div class="achievement-badge achievement-badge-{badge_type} achievement-badge-locked">
            {icon}
            <div class="achievement-badge-tooltip">{achievement['name']}</div>
        </div>
        <div class="achievement-details">
            <span class="achievement-name">{achievement['name']}</span>
            <p class="achievement-description">{achievement['description']}</p>
            <span class="achievement-date">{tr('locked_achievement')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_welcome_screen():
    """Show the welcome screen for first-time users."""
    # Check if we should show the new onboarding experience
    onboarding_enabled = get_config("app.enable_onboarding") or True
    
    if onboarding_enabled:
        # Import and show the guided onboarding journey
        from components.onboarding import show_onboarding_journey
        show_onboarding_journey()
    else:
        # Fall back to simple welcome screen if onboarding is disabled
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            lang = get_config("app.default_language") or "en"
            welcome_text = tr('welcome_text')
            desc_text = tr('welcome_description')
            name_label = tr('name_label')
            button_text = tr('start_game')
            
            st.markdown(f"### {welcome_text}")
            st.write(desc_text)
            
            # Name input
            st.session_state.player_name = st.text_input(name_label, key=generate_widget_key("text_input", "player_name"))
            
            # Start button
            if st.button(button_text, key=generate_widget_key("button", "start_game")) and st.session_state.player_name:
                # Create user in database if needed
                from utils.db import db
                user_id = db.create_user(st.session_state.player_name)
                if user_id:
                    st.session_state.user_id = user_id
                    # Initialize other state variables
                    st.session_state.total_score = 0
                    st.session_state.skill_levels = {
                        "inventory_management": 0,
                        "cash_handling": 0,
                        "pricing_strategy": 0,
                        "customer_relations": 0,
                        "bookkeeping": 0
                    }
                    st.session_state.achievements = []
                    st.session_state.game_history = []
                    st.session_state.shop_level = 1
                    
                    st.success(f"{tr('welcome_success')} {st.session_state.player_name}!")
                    st.rerun()