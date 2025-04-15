"""
Tooltips and educational popover utilities for Toko Pintar application.
Provides reusable tooltip components for explaining game mechanics.
"""
import streamlit as st
from utils.config import get_config
from utils.i18n import tr

# Dictionary of tooltips for different game mechanics
GAME_MECHANICS = {
    "inventory_counting": {
        "en": tr("tooltip_inventory_counting"),
        "id": tr("tooltip_inventory_counting_id")
    },
    "change_making": {
        "en": tr("tooltip_change_making"),
        "id": tr("tooltip_change_making_id")
    },
    "margin_calculator": {
        "en": tr("tooltip_margin_calculator"),
        "id": tr("tooltip_margin_calculator_id")
    },
    "inventory_management": {
        "en": tr("tooltip_inventory_management"),
        "id": tr("tooltip_inventory_management_id")
    },
    "cash_handling": {
        "en": tr("tooltip_cash_handling"),
        "id": tr("tooltip_cash_handling_id")
    },
    "pricing_strategy": {
        "en": tr("tooltip_pricing_strategy"),
        "id": tr("tooltip_pricing_strategy_id")
    },
    "shop_level": {
        "en": tr("tooltip_shop_level"),
        "id": tr("tooltip_shop_level_id")
    },
    "achievement": {
        "en": tr("tooltip_achievement"),
        "id": tr("tooltip_achievement_id")
    }
}

def show_tooltip(mechanic_id, place="top"):
    """Generate HTML for a tooltip explaining a game mechanic.
    
    Args:
        mechanic_id (str): The ID of the game mechanic to explain
        place (str): Tooltip placement (top, bottom, left, right)
        
    Returns:
        str: HTML for the tooltip
    """
    lang = get_config("app.default_language") or "en"
    tooltip_text = GAME_MECHANICS.get(mechanic_id, {}).get(lang)
    
    if not tooltip_text:
        return ""
    
    html = f"""
    <div class="tooltip-container">
        <span style="cursor: help; border-bottom: 1px dotted #666;">?</span>
        <div class="tooltip tooltip-{place} tooltip-educational">
            {tooltip_text}
        </div>
    </div>
    """
    return html

def show_educational_tooltip(text, title=None, place="top"):
    """Generate HTML for a custom educational tooltip.
    
    Args:
        text (str): The tooltip content
        title (str, optional): Optional title for the tooltip
        place (str): Tooltip placement (top, bottom, left, right)
        
    Returns:
        str: HTML for the tooltip
    """
    title_html = f'<div style="font-weight: bold; margin-bottom: 5px;">{tr(title)}</div>' if title else ''
    
    html = f"""
    <div class="tooltip-container">
        <span style="cursor: help; border-bottom: 1px dotted #666; margin: 0 5px;">?</span>
        <div class="tooltip tooltip-{place} tooltip-educational">
            {title_html}{tr(text)}
        </div>
    </div>
    """
    return html

def show_mechanics_tooltip_button(mechanic_id, button_text="How to Play", game_id=None):
    """Display a button that shows a tooltip explaining game mechanics.
    
    Args:
        mechanic_id (str): The ID of the game mechanic to explain
        button_text (str): Text to display on the button
        game_id (str, optional): The game ID to make the key more unique
    """
    lang = get_config("app.default_language") or "en"
    tooltip_text = GAME_MECHANICS.get(mechanic_id, {}).get(lang)
    
    if not tooltip_text:
        return
    
    # Create a unique key for this tooltip
    key_suffix = f"_{game_id}" if game_id else ""
    key = f"tooltip_{mechanic_id}{key_suffix}"
    
    # Initialize in session state if not present
    if key not in st.session_state:
        st.session_state[key] = False
    
    # Create button to toggle tooltip
    if st.button(tr(button_text), key=f"btn_{key}"):
        st.session_state[key] = not st.session_state[key]
    
    # Show tooltip if enabled
    if st.session_state[key]:
        st.info(f"💡 {tooltip_text}")
        
        # Add a close button
        close_text = tr("Close") if lang == "en" else tr("Tutup")
        if st.button(close_text, key=f"close_{key}"):
            st.session_state[key] = False

def add_inline_tooltip(text, mechanic_id):
    """Add an inline tooltip to text.
    
    Args:
        text (str): The text to add the tooltip to
        mechanic_id (str): The ID of the game mechanic to explain
        
    Returns:
        str: HTML with the text and tooltip
    """
    tooltip_html = show_tooltip(mechanic_id)
    return f"{tr(text)} {tooltip_html}"

# Function to add educational tooltips to Streamlit elements using JavaScript
def add_tooltips_to_page():
    """Add JavaScript to the page to enable tooltip functionality."""
    js = """
    <script>
    // Initialize tooltips on page load
    document.addEventListener('DOMContentLoaded', function() {
        // Find all tooltip containers
        const tooltipContainers = document.querySelectorAll('.tooltip-container');
        
        tooltipContainers.forEach(container => {
            const tooltipTrigger = container.querySelector('span');
            const tooltip = container.querySelector('.tooltip');
            
            // Show tooltip on hover
            tooltipTrigger.addEventListener('mouseenter', function() {
                tooltip.style.opacity = '1';
                tooltip.style.transform = 'translateX(-50%) translateY(0)';
            });
            
            // Hide tooltip when mouse leaves
            tooltipTrigger.addEventListener('mouseleave', function() {
                tooltip.style.opacity = '0';
                tooltip.style.transform = 'translateX(-50%) translateY(-5px)';
            });
        });
    });
    </script>
    """
    st.markdown(js, unsafe_allow_html=True)