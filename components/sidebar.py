"""
Collapsible sidebar component for Toko Pintar application.
"""
import streamlit as st
from utils.config import get_config, generate_widget_key

def init_sidebar_state():
    """Initialize sidebar state if not present."""
    # Always start with sidebar collapsed on mobile
    if 'sidebar_expanded' not in st.session_state:
        st.session_state.sidebar_expanded = False  # Start collapsed by default
    
    # Add enhanced mobile sidebar styling
    st.markdown("""
    <style>
    /* Base sidebar styles - for both desktop and mobile */
    [data-testid="stSidebar"] {
        background-color: white !important;
        box-shadow: 2px 0 5px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease-in-out !important;
    }
    
    /* When sidebar is closed - completely hide it, but don't shift main content */
    [data-testid="stSidebar"][aria-expanded="false"] {
        width: 0 !important;
        visibility: hidden !important;
        position: fixed !important;
        z-index: 999 !important;
        opacity: 0 !important;
        transition: all 0.3s ease-in-out;
    }
    
    /* When sidebar is open - standard width on desktop, full width on mobile */
    [data-testid="stSidebar"][aria-expanded="true"] {
        visibility: visible !important;
        position: fixed !important;
        z-index: 999 !important;
        width: 21rem !important; 
        opacity: 1 !important;
        transition: all 0.3s ease-in-out;
    }
    
    /* Prevent main content from shifting */
    .main .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    
    /* Better padding */
    [data-testid="stSidebarUserContent"] {
        padding: 1rem 1rem !important;
    }
    
    /* Add close button to sidebar */
    [data-testid="stSidebar"][aria-expanded="true"]::after {
        content: "×";
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 28px;
        font-weight: bold;
        color: #888;
        cursor: pointer;
        z-index: 1000;
    }
    
    /* Mobile responsive sidebar improvements */
    @media (max-width: 768px) {
        /* Full-width sidebar that slides in */
        [data-testid="stSidebar"][aria-expanded="true"] {
            width: 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
            height: 100vh !important;
            position: fixed !important;
            z-index: 999 !important;
            overflow-y: auto !important;
        }
        
        /* Improved buttons for mobile */
        [data-testid="stSidebar"] button {
            width: 100% !important;
            margin-bottom: 10px !important;
            min-height: 48px !important; /* Better touch target */
            font-size: 16px !important; /* Larger text for mobile */
            border-radius: 8px !important;
        }
        
        /* Make scrolling smooth */
        section[data-testid="stSidebar"] {
            max-height: 100vh !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
        }
        
        /* Don't hide collapse control - need it for our hamburger menu to work */
        /* We'll use CSS to visually hide it but keep it functional */
        [data-testid="collapsedControl"] {
            opacity: 0 !important;
            position: absolute !important;
            left: -9999px !important;
            pointer-events: auto !important;
        }
        
        /* When sidebar is closed on mobile, make sure it's completely hidden */
        [data-testid="stSidebar"][aria-expanded="false"] {
            transform: translateX(-100%) !important;
            width: 0 !important;
            height: 100vh !important;
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            opacity: 0 !important;
            visibility: hidden !important;
            transition: all 0.3s ease-in-out !important;
        }
        
        /* Better styling for close button on mobile */
        [data-testid="stSidebar"][aria-expanded="true"]::after {
            font-size: 36px;
            top: 15px;
            right: 20px;
        }
    }
    
    /* Add click handler to the close button */
    </style>
    
    <script>
    // Function to add click handler to the sidebar close button
    function setupSidebarCloseButton() {
        // Wait for the sidebar to be visible
        const checkForSidebar = setInterval(function() {
            const sidebar = document.querySelector('[data-testid="stSidebar"][aria-expanded="true"]');
            if (sidebar) {
                clearInterval(checkForSidebar);
                
                // Add click handler to the sidebar
                sidebar.addEventListener('click', function(e) {
                    // Check if the click was on the close button (the ::after element)
                    // We approximate this by checking if the click is in the top-right corner
                    const rect = sidebar.getBoundingClientRect();
                    if (e.clientX > rect.right - 50 && e.clientY < rect.top + 50) {
                        // Find and click Streamlit's sidebar toggle button
                        const sidebarBtn = document.querySelector('[data-testid="collapsedControl"] button');
                        if (sidebarBtn) {
                            sidebarBtn.click();
                        }
                    }
                });
            }
        }, 100);
    }
    
    // On page load
    document.addEventListener('DOMContentLoaded', setupSidebarCloseButton);
    
    // Also track sidebar changes to re-add handler when needed
    const sidebarObserver = new MutationObserver(function(mutations) {
        setupSidebarCloseButton();
    });
    
    // Start observing when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        sidebarObserver.observe(document.body, { 
            childList: true, 
            subtree: true,
            attributes: true,
            attributeFilter: ['aria-expanded']
        });
    });
    </script>
    """, unsafe_allow_html=True)
    
    # No additional content needed
        
    # Initialize settings panel expanded state if not present
    if 'settings_expanded' not in st.session_state:
        # Settings section should be open by default
        st.session_state.settings_expanded = True
        
def show_language_selector():
    """Display a language selector in the sidebar.
    
    This function can be used both during the initial setup and after login.
    """
    # Get language preference
    lang = get_config("app.default_language") or "en"
    
    # Language options
    languages = {"en": "English", "id": "Bahasa Indonesia"}
    current_lang = get_config("app.default_language") or "en"
    
    # Create a language selector with a clean title
    st.sidebar.markdown("### 🌐 Language / Bahasa")
    selected_lang = st.sidebar.selectbox(
        "Select your preferred language:",
        options=list(languages.keys()),
        format_func=lambda x: languages[x],
        index=list(languages.keys()).index(current_lang),
        key="welcome_language_selector_stable"
    )
    
    # Update language if changed
    if selected_lang != current_lang:
        from utils.config import set_config
        set_config("app.default_language", selected_lang)
        st.rerun()

def toggle_sidebar():
    """Toggle sidebar expansion state."""
    # This function is kept for backward compatibility
    pass

def add_sidebar_toggle():
    """Add a toggle button for the sidebar."""
    # Simplified version without JavaScript that might cause conflicts
    pass

def collapsible_sidebar(content_function=None):
    """Create a collapsible sidebar layout.
    
    Args:
        content_function: Function that populates the sidebar content
    """
    # Initialize sidebar state
    init_sidebar_state()
    
    # Create a container for content - simplified approach
    if content_function:
        with st.sidebar:
            content_function()

def toggle_settings():
    """Toggle settings section expansion state."""
    st.session_state.settings_expanded = not st.session_state.settings_expanded

def sidebar_quick_navigation():
    """Display quick navigation links in the sidebar."""
    lang = get_config("app.default_language") or "en"
    
    st.sidebar.title("Toko Pintar")
    
    # Use the centralized language selector at the top
    show_language_selector()
    
    # Quick Navigation section - always expanded by default
    quick_nav_text = "Quick Navigation" if lang == "en" else "Navigasi Cepat"
    
    # Create an expander that's open by default with a cleaner title (no ### markdown)
    with st.sidebar.expander(quick_nav_text, expanded=True):
        # Game links section
        games_header = "Games" if lang == "en" else "Permainan"
        st.markdown(f"### {games_header}")
        
        # Game buttons - each with language-specific text and a unique key
        inventory_text = "🎮 " + ("Inventory Game" if lang == "en" else "Permainan Inventaris")
        if st.button(inventory_text, key=generate_widget_key("button", "sidebar_inventory_game")):
            st.session_state.current_game = "inventory_game"
            st.rerun()
            
        change_text = "💵 " + ("Change Making" if lang == "en" else "Membuat Kembalian")
        if st.button(change_text, key=generate_widget_key("button", "sidebar_change_making")):
            st.session_state.current_game = "change_making"
            st.rerun()
            
        margin_text = "📊 " + ("Margin Calculator" if lang == "en" else "Kalkulator Margin")
        if st.button(margin_text, key=generate_widget_key("button", "sidebar_margin_calculator")):
            st.session_state.current_game = "margin_calculator"
            st.rerun()
        
        # Skills section
        skills_header = "Skills" if lang == "en" else "Keahlian"
        st.markdown(f"### {skills_header}")
        
        # Define skills with translations
        skills = [
            ("inventory_management", "📦 " + ("Inventory" if lang == "en" else "Inventaris")),
            ("cash_handling", "💰 " + ("Cash Handling" if lang == "en" else "Penanganan Kas")),
            ("pricing_strategy", "💹 " + ("Pricing" if lang == "en" else "Penetapan Harga")),
            ("customer_relations", "🤝 " + ("Customer" if lang == "en" else "Pelanggan")),
            ("bookkeeping", "📒 " + ("Bookkeeping" if lang == "en" else "Pembukuan"))
        ]
        
        # Display each skill with unique keys
        for skill_id, skill_name in skills:
            if st.button(skill_name, key=generate_widget_key("button", f"sidebar_skill_{skill_id}")):
                st.session_state.current_section = "Skills" if lang == "en" else "Keahlian"
                st.session_state.selected_skill = skill_id
                st.rerun()
        
        # Shop section
        shop_header = "My Shop" if lang == "en" else "Toko Saya"
        st.markdown(f"### {shop_header}")
        
        shop_button_text = "🏪 " + ("View Shop" if lang == "en" else "Lihat Toko")
        if st.button(shop_button_text, key=generate_widget_key("button", "sidebar_view_shop")):
            st.session_state.current_section = "My Shop" if lang == "en" else "Toko Saya"
            st.rerun()
    
    # Settings section
    settings_text = "Settings" if lang == "en" else "Pengaturan"
    
    # Add a header for the settings section
    st.sidebar.markdown(f"### ⚙️ {settings_text}")
    
    # Add more settings options
    debug_mode = get_config("debug.enabled")
    debug_label = "Debug Mode" if lang == "en" else "Mode Debug"
    debug_enabled = st.sidebar.checkbox(debug_label, value=debug_mode, key=generate_widget_key("checkbox", "debug_mode_toggle"))
    
    if debug_enabled != debug_mode:
        from utils.config import set_config
        set_config("debug.enabled", debug_enabled)
        st.rerun()