"""
Tooltips and educational popover utilities for Toko Pintar application.
Provides reusable tooltip components for explaining game mechanics.
"""
import streamlit as st
from utils.config import get_config

# Dictionary of tooltips for different game mechanics
GAME_MECHANICS = {
    "inventory_counting": {
        "en": "Count the items shown and enter the correct total. Be careful with similar-looking items.",
        "id": "Hitung item yang ditampilkan dan masukkan total yang benar. Hati-hati dengan item yang terlihat mirip."
    },
    "change_making": {
        "en": "Calculate the correct change using Indonesian Rupiah denominations. Aim for speed and accuracy.",
        "id": "Hitung kembalian yang benar menggunakan denominasi Rupiah Indonesia. Usahakan kecepatan dan akurasi."
    },
    "margin_calculator": {
        "en": "Set prices to achieve target profit margins. Consider both costs and market competition.",
        "id": "Tetapkan harga untuk mencapai margin keuntungan target. Pertimbangkan biaya dan persaingan pasar."
    },
    "inventory_management": {
        "en": "Track stock levels accurately to prevent stockouts and excess inventory.",
        "id": "Lacak tingkat stok secara akurat untuk mencegah kehabisan stok dan kelebihan inventaris."
    },
    "cash_handling": {
        "en": "Manage cash transactions accurately to maintain proper financial records.",
        "id": "Kelola transaksi tunai secara akurat untuk mempertahankan catatan keuangan yang tepat."
    },
    "pricing_strategy": {
        "en": "Set optimal prices that balance profitability and competitive positioning.",
        "id": "Tetapkan harga optimal yang menyeimbangkan profitabilitas dan posisi kompetitif."
    },
    "shop_level": {
        "en": "Your shop level increases as you improve your skills. Higher levels unlock new features.",
        "id": "Level toko Anda meningkat seiring peningkatan keterampilan Anda. Level lebih tinggi membuka fitur baru."
    },
    "achievement": {
        "en": "Complete specific goals to earn achievements and track your progress.",
        "id": "Selesaikan tujuan tertentu untuk mendapatkan prestasi dan melacak kemajuan Anda."
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
    title_html = f'<div style="font-weight: bold; margin-bottom: 5px;">{title}</div>' if title else ''
    
    html = f"""
    <div class="tooltip-container">
        <span style="cursor: help; border-bottom: 1px dotted #666; margin: 0 5px;">?</span>
        <div class="tooltip tooltip-{place} tooltip-educational">
            {title_html}{text}
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
    if st.button(button_text, key=f"btn_{key}"):
        st.session_state[key] = not st.session_state[key]
    
    # Show tooltip if enabled
    if st.session_state[key]:
        st.info(f"💡 {tooltip_text}")
        
        # Add a close button
        close_text = "Close" if lang == "en" else "Tutup"
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
    return f"{text} {tooltip_html}"

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