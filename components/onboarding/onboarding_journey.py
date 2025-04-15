"""
Guided Onboarding Journey components for Toko Pintar.
This module provides a step-by-step onboarding experience for new users.
"""
import streamlit as st
import uuid
from utils.config import get_config, get_translation
from datetime import datetime
from utils.i18n import tr

def show_onboarding_journey():
    """
    Main function to display the onboarding journey.
    Controls the flow between different onboarding steps.
    """
    # Clear out any previous styles and add only what we need
    st.markdown("""
    <style>
    /* Apply orange style to ALL buttons by default */
    button, .stButton>button {
        background-color: #FF7043 !important;
        color: white !important;
        border: none !important;
        font-weight: 500 !important;
        box-shadow: 0 0 0 2px rgba(255, 112, 67, 0.3) !important;
        animation: pulse-border 2s infinite !important;
    }
    
    /* Hover state for ALL buttons */
    button:hover, .stButton>button:hover {
        background-color: #E64A19 !important;
        box-shadow: 0 4px 8px rgba(255, 112, 67, 0.3), 0 0 0 2px rgba(255, 112, 67, 0.5) !important;
        transform: translateY(-2px) !important;
    }
    
    /* ONLY the back buttons get default styling - OVERRIDE with !important */
    div[data-testid="stHorizontalBlock"] div:nth-child(1) button,
    button[kind="secondary"],
    button:contains("Back") {
        background-color: #f0f2f6 !important; 
        color: #262730 !important;
        border: none !important;
        animation: none !important;
        box-shadow: none !important;
        transform: none !important;
    }
    
    /* Hover for back buttons */
    div[data-testid="stHorizontalBlock"] div:nth-child(1) button:hover,
    button[kind="secondary"]:hover,
    button:contains("Back"):hover {
        background-color: #e0e2e6 !important;
        box-shadow: none !important;
        transform: none !important;
    }
    
    /* Pulse animation for accent border */
    @keyframes pulse-border {
        0% { box-shadow: 0 0 0 0px rgba(255, 112, 67, 0.3), 0 2px 4px rgba(0,0,0,0.1); }
        70% { box-shadow: 0 0 0 6px rgba(255, 112, 67, 0), 0 2px 4px rgba(0,0,0,0.1); }
        100% { box-shadow: 0 0 0 0px rgba(255, 112, 67, 0), 0 2px 4px rgba(0,0,0,0.1); }
    }
    </style>
    """, unsafe_allow_html=True)
    # Add direct hide CSS for hamburger menu - much more aggressive approach
    st.markdown("""
    <style>
    /* Extremely aggressive style to completely hide hamburger menu and sidebar controls in onboarding */
    #custom-hamburger-btn,
    .hamburger-menu-button,
    [id*="hamburger"],
    [class*="hamburger"],
    [data-testid="collapsedControl"],
    .stButton button[aria-label*="menu"],
    button[data-testid*="sidebar"],
    button[aria-label*="sidebar"],
    button[data-baseweb="button"][aria-expanded],
    .css-fblp2m {
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
    </style>
    
    <script>
    // When page loads, add necessary classes to body
    document.addEventListener('DOMContentLoaded', function() {
        // Mark body as in onboarding mode to hide hamburger menu
        document.body.classList.add('onboarding-active');
        
        // Also handle mobile detection
        if (window.matchMedia("(max-width: 768px)").matches) {
            document.body.classList.add('mobile-view');
            // Try to find any potential step connectors and hide them
            setTimeout(function() {
                const stepElements = document.querySelectorAll('.step-connector, .onboarding-steps-mobile-hide');
                stepElements.forEach(function(element) {
                    element.style.display = 'none';
                    element.style.height = '0';
                    element.style.margin = '0';
                    element.style.padding = '0';
                });
            }, 100);
        }
        
        // Also directly hide all hamburger-related elements
        const hideElements = [
            document.querySelector('#custom-hamburger-btn'),
            document.querySelector('.hamburger-menu-button'),
            document.querySelector('[data-testid="collapsedControl"]'),
            ...document.querySelectorAll('[id*="hamburger"]'),
            ...document.querySelectorAll('[class*="hamburger"]'),
            ...document.querySelectorAll('button[aria-label*="menu"]'),
            ...document.querySelectorAll('button[data-testid*="sidebar"]'),
            ...document.querySelectorAll('button[aria-label*="sidebar"]')
        ];
        
        hideElements.forEach(element => {
            if (element) {
                element.style.display = 'none';
                element.style.visibility = 'hidden';
                element.style.opacity = '0';
                element.style.pointerEvents = 'none';
                element.style.position = 'absolute';
                element.style.left = '-9999px';
            }
        });
        
        // Do it again after a delay to catch dynamically added elements
        setTimeout(() => {
            const hideElementsAgain = [
                document.querySelector('#custom-hamburger-btn'),
                document.querySelector('.hamburger-menu-button'),
                document.querySelector('[data-testid="collapsedControl"]'),
                ...document.querySelectorAll('[id*="hamburger"]'),
                ...document.querySelectorAll('[class*="hamburger"]'),
                ...document.querySelectorAll('button[aria-label*="menu"]'),
                ...document.querySelectorAll('button[data-testid*="sidebar"]'),
                ...document.querySelectorAll('button[aria-label*="sidebar"]')
            ];
            
            hideElementsAgain.forEach(element => {
                if (element) {
                    element.style.display = 'none';
                    element.style.visibility = 'hidden';
                    element.style.opacity = '0';
                    element.style.pointerEvents = 'none';
                    element.style.position = 'absolute';
                    element.style.left = '-9999px';
                }
            });
        }, 500);
    });
    </script>
    """, unsafe_allow_html=True)
    
    # Add necessary CSS for animations and layout - with mobile responsiveness
    st.markdown("""
    <style>
    /* Special styles for mobile view */
    body.mobile-view .step-connector,
    body.mobile-view .step-progress-indicator,
    body.mobile-view .step-progress-label,
    body.mobile-view .onboarding-steps-mobile-hide {
        display: none !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        opacity: 0 !important;
        visibility: hidden !important;
        position: absolute !important;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    /* Force flex display for our progress container */
    .steps-container {
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        align-items: center !important;
        width: 100% !important;
    }
    
    .step-item {
        flex: 1 !important;
        text-align: center !important;
        position: relative !important;
    }
    
    .step-connector {
        flex: 0.5 !important;
        height: 3px !important;
    }
    
    /* Mobile-specific styles */
    @media (max-width: 768px) {
        /* Hide step indicators and connections on mobile devices */
        .step-progress-indicator, .step-progress-label, .step-connector {
            display: none !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Add specific class for mobile step hiding */
        .onboarding-steps-mobile-hide {
            display: none !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            opacity: 0 !important;
            visibility: hidden !important;
        }
        
        /* Force hide all elements in the step container */
        .onboarding-steps-mobile-hide * {
            display: none !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize onboarding state if not exists
    if 'onboarding_step' not in st.session_state:
        st.session_state.onboarding_step = 1
    
    # Get current step here from session state
    current_step = st.session_state.onboarding_step
    
    # Create a container for consistent styling
    st.markdown('<div class="onboarding-container" style="margin-top: 0;">', unsafe_allow_html=True)
    
    # Display the current step content (moved to top)
    if current_step == 1:
        show_onboarding_welcome()
    elif current_step == 2:
        show_onboarding_skills_intro()
    elif current_step == 3:
        show_onboarding_games_intro()
    elif current_step == 4:
        show_onboarding_complete()
    else:
        # Onboarding complete, reset state and redirect to main menu
        st.session_state.onboarding_completed = True
        st.session_state.onboarding_step = 0
        st.rerun()
    
    # Display progress indicator (current_step already defined above)
    total_steps = 4
    
    # Create a simpler horizontal progress indicator using st.columns 
    # First, render a message to ensure HTML is properly parsed
    st.markdown('<div style="display:none">Force HTML parsing</div>', unsafe_allow_html=True)
    
    # Special empty container for mobile that takes zero space
    st.markdown("""
    <style>
    /* Desktop-only element to hide completely on mobile without taking any space */
    @media (max-width: 768px) {
        .desktop-only-element {
            display: none !important;
            height: 0 !important;
            width: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            position: absolute !important;
            opacity: 0 !important;
            overflow: hidden !important;
            visibility: hidden !important;
        }
    }
    </style>
    <div class="desktop-only-element"><!-- This will be hidden on mobile without creating space --></div>
    """, unsafe_allow_html=True)
    
    # Add this inside a conditional statement only for desktop
    # Using session state to track if we're viewing on mobile
    if 'is_mobile' not in st.session_state:
        # Default assumption is desktop
        st.session_state.is_mobile = False
    
    # We'll wrap the desktop-only step indicators in a try/except block
    # If mobile, this will simply not create any step indicators
    try:
        # Conditionally create these elements only for desktop
        if not st.session_state.is_mobile:
            # We use HTML for our container which will be easier to hide
            st.markdown('<div class="desktop-only-element">', unsafe_allow_html=True)
            
            # Create column containers only for desktop
            cols = st.columns(2*total_steps - 1)  # Twice as many columns to account for connectors
            
            # Add steps to columns - only on desktop
            for step in range(1, total_steps + 1):
                status = "active" if step == current_step else "complete" if step < current_step else ""
                step_info = get_step_info(step)
                
                # Calculate colors based on status
                bg_color = "#FF7043" if status == "active" else "#4CAF50" if status == "complete" else "#E0E0E0"
                text_color = "white" if status in ["active", "complete"] else "#757575"
                
                # Create the step indicator in the appropriate column
                with cols[2*(step-1)]:  # Use even-indexed columns for steps
                    # Add indicator with styling
                    indicator_style = (
                        f"width:60px;height:60px;border-radius:50%;background-color:{bg_color};"
                        f"color:{text_color};display:flex;align-items:center;justify-content:center;"
                        f"font-size:1.8rem;margin:0 auto 10px auto;box-shadow:0 2px 5px rgba(0,0,0,0.1);"
                    )
                    
                    # Add animation for active step
                    if status == "active":
                        indicator_style += "animation:pulse 1.5s infinite;"
                    
                    # Create styled step indicator
                    st.markdown(f'<div class="step-progress-indicator" style="{indicator_style}">{step_info["icon"]}</div>', unsafe_allow_html=True)
                    
                    # Add label
                    label_style = f"text-align:center;font-weight:{500 if status != 'active' else 600};color:{bg_color};font-size:1.1rem;"
                    st.markdown(f'<div class="step-progress-label" style="{label_style}">{step_info["title"]}</div>', unsafe_allow_html=True)
                
                # Add connecting line between steps (except after the last step)
                if step < total_steps:
                    with cols[2*(step-1) + 1]:  # Use odd-indexed columns for connectors
                        line_color = "#4CAF50" if step < current_step else "#E0E0E0"
                        st.markdown(f'<div class="step-connector" style="height:3px;background-color:{line_color};margin:30px 0;"></div>', unsafe_allow_html=True)
            
            # Close the container div
            st.markdown('</div>', unsafe_allow_html=True)
    except Exception:
        # On mobile, we'll end up here if there's an issue with columns
        # Just add some invisible content to avoid errors
        st.markdown('<div style="display:none"></div>', unsafe_allow_html=True)
    
    
    # Add onboarding steps as a footer bar for mobile only
    total_steps = 4
    current_step = st.session_state.onboarding_step
    
    # Create the active class strings for each step
    step1_class = "active" if current_step == 1 else ""
    step2_class = "active" if current_step == 2 else ""
    step3_class = "active" if current_step == 3 else ""
    step4_class = "active" if current_step == 4 else ""
    
    # Use CSS to construct the mobile footer dynamically to avoid showing raw HTML
    mobile_footer_css = f"""
    <style>
    /* Create the mobile steps footer using ::before and ::after */
    .onboarding-container::after {{
        content: '';
        display: block;
        margin-top: 30px;
        border-top: 1px solid #eee;
        padding-top: 15px;
    }}
    
    /* Only show on mobile devices */
    @media (max-width: 768px) {{
        /* Footer title text */
        .onboarding-container::after {{
            content: '{tr('onboarding_title')}';
            display: block;
            text-align: center;
            font-size: 1.2rem;
            font-weight: bold;
            margin-top: 30px;
            border-top: 1px solid #eee;
            padding-top: 15px;
        }}
        
        /* No footer subtitle in onboarding - removed to prevent duplication */
        
        /* Create step indicators using fixed positioning */
        .step-indicator-1, .step-indicator-2, .step-indicator-3, .step-indicator-4 {{
            position: fixed;
            bottom: 30px;
            text-align: center;
            width: 25%;
            opacity: 0.5;
        }}
        
        .step-indicator-1 {{ left: 0%; }}
        .step-indicator-2 {{ left: 25%; }}
        .step-indicator-3 {{ left: 50%; }}
        .step-indicator-4 {{ left: 75%; }}
        
        /* Active step indicator */
        .step-indicator-{current_step} {{ 
            opacity: 1;
        }}
        
        /* Step icons */
        .step-indicator-1::before {{ content: '👋'; display: block; font-size: 1.5rem; }}
        .step-indicator-2::before {{ content: '🎯'; display: block; font-size: 1.5rem; }}
        .step-indicator-3::before {{ content: '🎮'; display: block; font-size: 1.5rem; }}
        .step-indicator-4::before {{ content: '🚀'; display: block; font-size: 1.5rem; }}
        
        /* Step labels */
        .step-indicator-1::after {{ 
            content: '{tr('onboarding_step_1')}'; 
            display: block; 
            font-size: 0.7rem; 
            color: {('#FF7043' if current_step == 1 else '#666')};
            font-weight: {('bold' if current_step == 1 else 'normal')};
        }}
        
        .step-indicator-2::after {{ 
            content: '{tr('onboarding_step_2')}'; 
            display: block; 
            font-size: 0.7rem; 
            color: {('#FF7043' if current_step == 2 else '#666')};
            font-weight: {('bold' if current_step == 2 else 'normal')};
        }}
        
        .step-indicator-3::after {{ 
            content: '{tr('onboarding_step_3')}'; 
            display: block; 
            font-size: 0.7rem; 
            color: {('#FF7043' if current_step == 3 else '#666')};
            font-weight: {('bold' if current_step == 3 else 'normal')};
        }}
        
        .step-indicator-4::after {{ 
            content: '{tr('onboarding_step_4')}'; 
            display: block; 
            font-size: 0.7rem; 
            color: {('#FF7043' if current_step == 4 else '#666')};
            font-weight: {('bold' if current_step == 4 else 'normal')};
        }}
    }}
    </style>
    
    <!-- Add empty divs for the steps -->
    <div class="step-indicator-1"></div>
    <div class="step-indicator-2"></div>
    <div class="step-indicator-3"></div>
    <div class="step-indicator-4"></div>
    """
    
    # Use markdown to add the CSS and placeholder divs
    st.markdown(mobile_footer_css, unsafe_allow_html=True)
    
    # Close the container
    st.markdown('</div>', unsafe_allow_html=True)

def get_step_info(step):
    """Get the title and icon for a specific onboarding step."""
    lang = get_config("app.default_language") or "en"
    
    step_info = {
        1: {
            "title": tr('onboarding_step_1'),
            "icon": "👋"
        },
        2: {
            "title": tr('onboarding_step_2'),
            "icon": "🎯"
        },
        3: {
            "title": tr('onboarding_step_3'),
            "icon": "🎮"
        },
        4: {
            "title": tr('onboarding_step_4'),
            "icon": "🚀"
        }
    }
    
    return step_info.get(step, {"title": tr('unknown_step'), "icon": "❓"})

def show_onboarding_welcome():
    """Display the welcome screen of the onboarding journey."""
    lang = get_config("app.default_language") or "en"
    
    # Header with animation - with proper translations
    header_title = tr('onboarding_title')
    header_subtitle = tr('onboarding_subtitle')
    
    st.markdown(f"""
    <div class="onboarding-header">
        <h2>{header_title}</h2>
        <p>{header_subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add language selector at the top of the welcome screen
    st.markdown("### 🌐 " + tr('language_selector'))
    languages = {"en": "English", "id": "Bahasa Indonesia"}
    current_lang = get_config("app.default_language") or "en"
    
    # Create a styled language selector directly in the main content
    selected_lang = st.selectbox(
        tr('select_language'),
        options=list(languages.keys()),
        format_func=lambda x: languages[x],
        index=list(languages.keys()).index(current_lang),
        key="welcome_page_language_selector"
    )
    
    # Update language if changed
    if selected_lang != current_lang:
        from utils.config import set_config
        set_config("app.default_language", selected_lang)
        st.rerun()
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Translate all welcome content
        journey_title = tr('journey_title')
        journey_intro = tr('journey_intro')
        activities_intro = tr('activities_intro')
        
        # Skills translations
        inventory = tr('inventory_management')
        cash = tr('cash_handling')
        pricing = tr('pricing_strategy')
        customer = tr('customer_relations')
        bookkeeping = tr('bookkeeping')
        
        st.markdown(f"""
        <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px;">
            <h3 style="color: var(--color-primary); margin-bottom: 15px;">{journey_title}</h3>
            <p>{journey_intro}</p>
            <p>{activities_intro}</p>
            <ul style="margin-left: 20px; margin-bottom: 10px;">
                <li>{inventory}</li>
                <li>{cash}</li>
                <li>{pricing}</li>
                <li>{customer}</li>
                <li>{bookkeeping}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        # Character input section - translated
        shopkeeper_title = tr('shopkeeper_title')
        
        st.markdown(f"""
        <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h3 style="color: var(--color-primary); margin-bottom: 15px;">{shopkeeper_title}</h3>
        """, unsafe_allow_html=True)
        
        # Name input
        name_label = tr('name_label')
        player_name = st.text_input(name_label, key="onboarding_name_input")
        
        # Shop name input
        shop_label = tr('shop_label')
        shop_name = st.text_input(shop_label, key="onboarding_shop_input")
        
        # Add the Next button directly in the same card for better alignment
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)  # Spacing
        
        next_text = tr('next_button')
        
        # Regular Streamlit button but with custom styling
        next_clicked = st.button(next_text, key="welcome_next", use_container_width=True)
        
        # Add CSS to style the button with accent highlight and pulse animation
        # This CSS is now defined globally at the top of the function
        
        if next_clicked:
            # Save user info
            if player_name:
                st.session_state.player_name = player_name
            if shop_name:
                st.session_state.shop_name = shop_name
            
            # Proceed to next step
            st.session_state.onboarding_step = 2
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

def show_onboarding_skills_intro():
    """Display the skills introduction screen."""
    lang = get_config("app.default_language") or "en"
    
    # Header with translations
    skills_title = tr('skills_title')
    skills_subtitle = tr('skills_subtitle')
    
    st.markdown(f"""
    <div class="onboarding-header">
        <h2>{skills_title}</h2>
        <p>{skills_subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Skills grid
    st.container()
    
    # First row
    col1, col2 = st.columns(2)
    
    # Translations for skill titles and descriptions
    inventory_title = tr('inventory_management')
    inventory_desc = tr('inventory_description')
    cash_title = tr('cash_handling')
    cash_desc = tr('cash_description')
    pricing_title = tr('pricing_strategy')
    pricing_desc = tr('pricing_description')
    bookkeeping_title = tr('bookkeeping')
    bookkeeping_desc = tr('bookkeeping_description')
    
    with col1:
        show_skill_card(
            icon="📦",
            title=inventory_title, 
            description=inventory_desc
        )
    
    with col2:
        show_skill_card(
            icon="💰",
            title=cash_title, 
            description=cash_desc
        )
    
    # Second row
    col1, col2 = st.columns(2)
    
    with col1:
        show_skill_card(
            icon="🏷️",
            title=pricing_title, 
            description=pricing_desc
        )
    
    with col2:
        show_skill_card(
            icon="📝",
            title=bookkeeping_title, 
            description=bookkeeping_desc
        )
    
    # Shop level progress with translations
    grow_title = tr('shop_growth_title')
    grow_desc = tr('shop_growth_description')
    
    st.markdown(f"""
    <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin: 20px 0;">
        <h3 style="color: #FF7043; margin-bottom: 15px;">{grow_title}</h3>
        <p>{grow_desc}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add Streamlit native progress components with translations
    shop_growth = tr('shop_growth')
    level_text = tr('level_text')
    st.write(f"**{shop_growth}** - {level_text} 1/5")
    st.progress(0.2)  # 20% progress for Level 1
    
    # Navigation buttons
    st.container().markdown("<br>", unsafe_allow_html=True)
    
    back_text = tr('back_button')
    next_text = tr('next_button_skills')
    
    col1, col2, col3 = st.columns([1, 2, 2])
    
    with col1:
        if st.button(back_text, key="skills_back", use_container_width=True, type="secondary"):
            st.session_state.onboarding_step = 1
            st.rerun()
    
    with col3:
        if st.button(next_text, key="skills_next", use_container_width=True):
            st.session_state.onboarding_step = 3
            st.rerun()

def show_skill_card(icon, title, description):
    """Display a skill card with an icon, title, and description."""
    st.markdown(f"""
    <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 15px; display: flex; align-items: flex-start;">
        <div style="font-size: 2.5rem; margin-right: 15px;">{icon}</div>
        <div>
            <h4 style="color: #FF7043; margin: 0 0 8px 0;">{title}</h4>
            <p style="margin: 0;">{description}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_onboarding_games_intro():
    """Display the games introduction screen."""
    lang = get_config("app.default_language") or "en"
    
    # Header with translations
    header_title = tr('games_title')
    header_subtitle = tr('games_subtitle')
    
    st.markdown(f"""
    <div class="onboarding-header">
        <h2>{header_title}</h2>
        <p>{header_subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Games showcase with translations
    show_game_preview(
        title=tr('game_1_title'),
        description=tr('game_1_description'),
        icon="📦",
        skill=tr('inventory_management'),
        difficulty=tr('game_1_difficulty')
    )
    
    show_game_preview(
        title=tr('game_2_title'),
        description=tr('game_2_description'),
        icon="💰",
        skill=tr('cash_handling'),
        difficulty=tr('game_2_difficulty')
    )
    
    show_game_preview(
        title=tr('game_3_title'),
        description=tr('game_3_description'),
        icon="🏷️",
        skill=tr('pricing_strategy'),
        difficulty=tr('game_3_difficulty')
    )
    
    # Navigation buttons
    st.container().markdown("<br>", unsafe_allow_html=True)
    
    back_text = tr('back_button')
    next_text = tr('next_button_games')
    
    col1, col2, col3 = st.columns([1, 2, 2])
    
    with col1:
        if st.button(back_text, key="games_back", use_container_width=True, type="secondary"):
            st.session_state.onboarding_step = 2
            st.rerun()
    
    with col3:
        if st.button(next_text, key="games_next", use_container_width=True):
            st.session_state.onboarding_step = 4
            st.rerun()

def show_game_preview(title, description, icon, skill, difficulty):
    """Display a game preview card with language support."""
    # Get current language
    lang = get_config("app.default_language") or "en"
    
    # Translate the "Difficulty" label
    difficulty_label = tr('difficulty_label')
    
    st.markdown(f"""
    <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 15px; display: flex; align-items: flex-start;">
        <div style="font-size: 2.5rem; margin-right: 15px;">{icon}</div>
        <div style="flex: 1;">
            <h4 style="color: #FF7043; margin: 0 0 8px 0;">{title}</h4>
            <p style="margin: 0 0 12px 0;">{description}</p>
            <div style="display: flex; justify-content: space-between;">
                <span style="background-color: #FFAB91; color: #E64A19; padding: 3px 10px; border-radius: 12px; font-size: 0.85rem;">{skill}</span>
                <span style="background-color: #80DEEA; color: #00ACC1; padding: 3px 10px; border-radius: 12px; font-size: 0.85rem;">{difficulty_label}: {difficulty}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_onboarding_complete():
    """Display the onboarding completion screen."""
    lang = get_config("app.default_language") or "en"
    
    # Header with celebration animation - translated
    ready_title = tr('onboarding_complete_title')
    ready_subtitle = tr('onboarding_complete_subtitle')
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 30px;">
        <div style="font-size: 4rem; margin-bottom: 15px; animation: bounce 1.5s infinite;">🎉</div>
        <h2>{ready_title}</h2>
        <p style="color: #757575;">{ready_subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Shop and player summary
    player_name = st.session_state.player_name or "Shopkeeper"
    shop_name = getattr(st.session_state, 'shop_name', "My Shop")
    
    st.markdown(f"""
    <div style="background-color: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px; text-align: center;">
        <h3 style="color: #FF7043; margin-bottom: 15px;">{shop_name}</h3>
        <p>Owned by: <strong>{player_name}</strong></p>
        <p>Founded: {datetime.now().strftime('%B %d, %Y')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Use Streamlit native progress component
    st.write(tr('shop_level') + ": 1/5")
    st.progress(0.2)  # 20% progress for Level 1
    
    # First tasks suggestions with translations
    tasks_title = tr('first_tasks_title')
    tasks_intro = tr('first_tasks_intro')
    
    st.markdown(f"""
    <div style="background-color: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 30px;">
        <h3 style="color: #FF7043; margin-bottom: 15px;">{tasks_title}</h3>
        <p>{tasks_intro}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Set up translations for tasks
    task1_title = tr('task_1_title')
    task1_desc = tr('task_1_description')
    task2_title = tr('task_2_title')
    task2_desc = tr('task_2_description')
    task3_title = tr('task_3_title')
    task3_desc = tr('task_3_description')
    
    # Task 1
    col1, col2 = st.columns([1, 20])
    with col1:
        st.write("1️⃣")
    with col2:
        st.markdown(f"**{task1_title}**")
        st.markdown(f"<span style='color: #757575; font-size: 0.9rem;'>{task1_desc}</span>", unsafe_allow_html=True)
    
    # Task 2
    col1, col2 = st.columns([1, 20])
    with col1:
        st.write("2️⃣")
    with col2:
        st.markdown(f"**{task2_title}**")
        st.markdown(f"<span style='color: #757575; font-size: 0.9rem;'>{task2_desc}</span>", unsafe_allow_html=True)
    
    # Task 3
    col1, col2 = st.columns([1, 20])
    with col1:
        st.write("3️⃣")
    with col2:
        st.markdown(f"**{task3_title}**")
        st.markdown(f"<span style='color: #757575; font-size: 0.9rem;'>{task3_desc}</span>", unsafe_allow_html=True)
    
    # Complete button
    st.container().markdown("<br>", unsafe_allow_html=True)
    
    start_text = tr('start_button')
    
    if st.button(start_text, key="complete_button", use_container_width=True):
        try:
            # Create user in database if needed
            from utils.db import db
            
            # Make sure player name is set
            player_name = st.session_state.player_name
            if not player_name:
                player_name = "Shopkeeper"
                st.session_state.player_name = player_name
            
            # Simplify the metadata - just use shop name string
            shop_name = getattr(st.session_state, 'shop_name', "My Shop")
            
            # Debug message
            st.info(f"Creating user for {player_name} with shop '{shop_name}'...")
            
            # Basic initialization without database for now
            st.session_state.user_id = str(uuid.uuid4())  # Generate a random ID
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
            
            # Mark onboarding as completed
            st.session_state.onboarding_completed = True
            st.session_state.onboarding_step = 0
            
            # Try to create the user in the database
            try:
                user_id = db.create_user(player_name, {"shop_name": shop_name})
                if user_id:
                    st.session_state.user_id = user_id
                    st.success(tr('user_created'))
            except Exception as e:
                st.warning(f"Notice: Could not create user in database: {str(e)}")
                st.write(tr('continuing_without_database'))
                
            # Add a simple first achievement directly
            st.session_state.achievements.append({
                "id": "first_steps",
                "name": tr('first_steps_achievement'),
                "description": f"{tr('started_journey')} {shop_name}",
                "earned_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # Skip the additional button click and go directly to the main app flow
            st.success(tr('shop_ready'))
            
            # Make sure sidebar starts collapsed
            if 'sidebar_expanded' in st.session_state:
                st.session_state.sidebar_expanded = False
            
            # Clear any game state
            st.session_state.current_game = None
            
            # Add additional flags to ensure proper state on reload
            st.session_state.first_main_menu_load = True
            
            # Add JavaScript to remove onboarding-active class when transitioning to main menu
            st.markdown("""
            <script>
            // Remove onboarding-active class when going to main menu
            document.addEventListener('DOMContentLoaded', function() {
                document.body.classList.remove('onboarding-active');
            });
            </script>
            """, unsafe_allow_html=True)
            
            # A brief delay to show the success message
            import time
            time.sleep(1)
            
            # Trigger reload
            st.rerun()
                
        except Exception as e:
            # Display any errors
            st.error(f"{tr('error_setting_up_shop')}: {str(e)}")
            st.info(tr('try_again'))