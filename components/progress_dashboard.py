"""
Progress dashboard component for Toko Pintar application.
Provides a persistent progress indicator showing completion status across all sections.
"""
import streamlit as st
from utils.skills import SKILL_DEFINITIONS, get_skill_name, get_skill_icon
from utils.config import get_config

def display_breadcrumb_navigation(items):
    """Display breadcrumb navigation.
    
    Args:
        items (list): List of (name, is_active) tuples for breadcrumb items
    """
    breadcrumb_html = '<nav aria-label="breadcrumb"><ol class="breadcrumb">'
    
    for i, (name, is_active) in enumerate(items):
        if is_active:
            breadcrumb_html += f'<li class="breadcrumb-item active">{name}</li>'
        else:
            # Use anchor with javascript void to avoid page reload but make it look clickable
            breadcrumb_html += f'<li class="breadcrumb-item"><a href="javascript:void(0);">{name}</a></li>'
    
    breadcrumb_html += '</ol></nav>'
    st.markdown(breadcrumb_html, unsafe_allow_html=True)

def display_progress_indicator():
    """Display a persistent progress indicator showing skills and completion status."""
    # Ensure skills are initialized
    if 'skill_levels' not in st.session_state:
        from utils.skills import initialize_skills
        initialize_skills()
    
    # Get language
    lang = get_config("app.default_language") or "en"
    
    # Progress dashboard title based on language
    progress_title = "My Shop Progress" if lang == "en" else "Kemajuan Toko Saya"
    
    # Start the dashboard
    st.markdown(f"""
    <div class="progress-dashboard">
        <div class="progress-dashboard-title">
            <span class="icon">📊</span> {progress_title}
        </div>
    """, unsafe_allow_html=True)
    
    # Calculate total progress
    max_level = get_config("gameplay.max_skill_level") or 5
    total_possible = len(SKILL_DEFINITIONS) * max_level
    current_total = sum(st.session_state.skill_levels.values())
    overall_progress = int((current_total / total_possible) * 100)
    
    # Display overall progress
    overall_label = "Overall Progress" if lang == "en" else "Kemajuan Keseluruhan"
    st.markdown(f"""
        <div class="progress-category">
            <div class="progress-category-header">
                <div class="progress-category-name">
                    <span class="icon">🏆</span> {overall_label}
                </div>
                <div class="progress-category-value">{overall_progress}%</div>
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar" style="width: {overall_progress}%;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Display each skill category
    for skill_id, skill_info in SKILL_DEFINITIONS.items():
        # Get skill level
        skill_level = st.session_state.skill_levels.get(skill_id, 0)
        
        # Calculate percentage
        percentage = int((skill_level / max_level) * 100)
        
        # Get skill name in proper language
        skill_name = get_skill_name(skill_id, lang)
        
        # Get skill icon
        skill_icon = get_skill_icon(skill_id)
        
        # Determine CSS class for color coding
        css_class = f"progress-{skill_id.split('_')[0]}"  # Use the first part of the skill ID
        
        # Achievement badges
        achievement_badge = ""
        if skill_level >= 3:  # Example threshold for showing a badge
            achievement_badge = '<span class="achievement-indicator">✓</span>'
        
        # Output HTML for the skill progress
        st.markdown(f"""
            <div class="progress-category {css_class}">
                <div class="progress-category-header">
                    <div class="progress-category-name">
                        <span class="icon">{skill_icon}</span> {skill_name} {achievement_badge}
                    </div>
                    <div class="progress-category-value">{percentage}%</div>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-bar" style="width: {percentage}%;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Close the dashboard
    st.markdown("</div>", unsafe_allow_html=True)

def display_shop_growth_visualization():
    """Display a visual representation of shop growth levels."""
    # Get current shop level
    current_level = st.session_state.shop_level if 'shop_level' in st.session_state else 1
    
    # Get language
    lang = get_config("app.default_language") or "en"
    
    # Header text based on language
    growth_title = "Shop Growth Journey" if lang == "en" else "Perjalanan Pertumbuhan Toko"
    
    # Start the visualization with just the title
    st.markdown(f"""
    <div class="progress-dashboard">
        <div class="progress-dashboard-title">
            <span class="icon">🏪</span> {growth_title}
        </div>
    """, unsafe_allow_html=True)
    
    # Shop level icons
    icons = ["🏪", "🏬", "🏢", "🏙️", "🌆"]
    level_names = [
        "Small Shop" if lang == "en" else "Toko Kecil", 
        "Growing Shop" if lang == "en" else "Toko Berkembang", 
        "Established" if lang == "en" else "Mapan",
        "Thriving" if lang == "en" else "Berkembang Pesat", 
        "Successful" if lang == "en" else "Sukses"
    ]
    
    # Use Streamlit's columns to ensure horizontal layout
    cols = st.columns(5)
    
    # Add class for mobile responsiveness
    st.markdown("""
    <style>
    /* Mobile responsiveness for shop growth visualization */
    @media (max-width: 768px) {
        .shop-level-indicator {
            padding: 5px !important;
        }
        
        .shop-level-icon {
            font-size: 1.8rem !important;
            margin-bottom: 4px !important;
        }
        
        .shop-level-name {
            font-size: 0.7rem !important;
            margin-bottom: 2px !important;
        }
        
        .shop-level-bar {
            height: 3px !important;
            margin: 4px auto !important;
        }
        
        .shop-level-label {
            font-size: 0.7rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display each level in its own column
    for i in range(5):
        level_num = i + 1
        level_class = ""
        
        if level_num < current_level:
            color = "#4CAF50"  # Completed (green)
            text_color = "#4CAF50"
            transform = "scale(1.0)"
        elif level_num == current_level:
            color = "#FF7043"  # Active (orange)
            text_color = "#FF7043"
            transform = "scale(1.2)"
        else:
            color = "#E0E0E0"  # Upcoming (gray)
            text_color = "#9E9E9E"
            transform = "scale(1.0)"
        
        # Create the level indicator in a column
        with cols[i]:
            st.markdown(f"""
                <div class="shop-level-indicator" style="text-align:center; padding:10px;">
                    <div class="shop-level-icon" style="font-size:2.5rem; margin-bottom:8px; transform:{transform}; transition:transform 0.3s ease;">{icons[i]}</div>
                    <div class="shop-level-name" style="font-weight:600; color:{text_color}; margin-bottom:5px;">Level {level_num}</div>
                    <div class="shop-level-bar" style="height:4px; background-color:{color}; width:70%; margin:8px auto;"></div>
                    <div class="shop-level-label" style="font-size:0.9rem; color:{text_color};">{level_names[i]}</div>
                </div>
            """, unsafe_allow_html=True)
    
    # Close the visualization container
    st.markdown("</div>", unsafe_allow_html=True)

def show_breadcrumb_navigation():
    """Display just the breadcrumb navigation."""
    # Create a single column for breadcrumb navigation
    col1 = st.columns([1])[0]
    
    # Breadcrumb navigation
    with col1:
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
            
            display_breadcrumb_navigation(breadcrumb_items)

def show_save_progress_button():
    """Display just the Save Progress button."""
    # Get language
    lang = get_config("app.default_language") or "en"
    save_text = "Save Progress" if lang == "en" else "Simpan Kemajuan"
    
    # Only show the button if user is logged in
    if hasattr(st.session_state, 'user_id'):
        # Add proper Streamlit button styling for alignment
        st.markdown("""
        <style>
        /* Center align the save button container */
        [data-testid="element-container"]:has(button[key="save_progress_button"]) {
            text-align: center;
        }
        
        /* Style the save button */
        button[key="save_progress_button"] {
            background-color: #FF7043 !important;
            color: white !important;
            font-weight: 500 !important;
            border: none !important;
            padding: 0.5rem 1rem !important;
            border-radius: 4px !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
            width: auto !important;
            margin: 1rem auto !important;
        }
        
        button[key="save_progress_button"]:hover {
            background-color: #E64A19 !important;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2) !important;
            transform: translateY(-1px) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Use only a single Streamlit button for functionality
        if st.button(save_text, key="save_progress_button"):
            # Save progress to database
            from utils.db import save_session_state_to_db
            save_session_state_to_db()
            
            # Show confirmation
            st.success("Progress saved successfully!")

def show_progress_dashboard():
    """Display the complete progress dashboard including breadcrumbs, progress indicators, and shop growth."""
    # Only display breadcrumb navigation
    show_breadcrumb_navigation()
    
    # Note: We don't display progress sections here anymore
    # They will be displayed separately in the app.py file
    # in the order specified by the user
    pass