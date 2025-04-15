"""
Animated transitions for Toko Pintar application.
Provides smooth transitions between different app sections.
"""
import streamlit as st
import time

def fade_in_section(content_function, key=None, duration=0.3):
    """Display a section with fade-in animation.
    
    Args:
        content_function: Function that generates the content to display
        key (str, optional): Unique key for this transition
        duration (float): Duration of the animation in seconds
    """
    if key is None:
        key = "fade_in_" + str(hash(content_function))
    
    # Generate a unique container
    container = st.empty()
    
    # Add CSS for the animation
    animation_css = f"""
    <style>
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    .fade-in-section {{
        animation: fadeIn {duration}s ease-in-out forwards;
    }}
    </style>
    """
    st.markdown(animation_css, unsafe_allow_html=True)
    
    # Wrap the content in a div with the animation class
    with container:
        st.markdown('<div class="fade-in-section">', unsafe_allow_html=True)
        content_function()
        st.markdown('</div>', unsafe_allow_html=True)

def slide_transition(direction="right", content_function=None):
    """Create a sliding transition effect.
    
    Args:
        direction (str): Direction to slide from ("left", "right", "up", "down")
        content_function: Function that generates the content to display
    """
    # Determine the CSS transform based on direction
    transform = {
        "left": "translateX(-100%)",
        "right": "translateX(100%)",
        "up": "translateY(-100%)",
        "down": "translateY(100%)"
    }.get(direction, "translateX(100%)")
    
    # Create the animation CSS
    animation_css = f"""
    <style>
    @keyframes slideIn {{
        from {{ transform: {transform}; opacity: 0; }}
        to {{ transform: translateX(0) translateY(0); opacity: 1; }}
    }}
    
    .slide-in-section {{
        animation: slideIn 0.5s ease-out forwards;
    }}
    </style>
    """
    st.markdown(animation_css, unsafe_allow_html=True)
    
    # Wrap the content in a div with the animation class
    st.markdown('<div class="slide-in-section">', unsafe_allow_html=True)
    if content_function:
        content_function()
    st.markdown('</div>', unsafe_allow_html=True)

def pulse_animation(element_selector):
    """Add pulse animation to specific elements via JavaScript.
    
    Args:
        element_selector (str): CSS selector for elements to animate
    """
    js = f"""
    <script>
    // Function to add pulse animation
    function addPulseAnimation() {{
        const elements = document.querySelectorAll('{element_selector}');
        elements.forEach(el => {{
            el.classList.add('animate-pulse');
        }});
    }}
    
    // Execute when DOM is fully loaded
    document.addEventListener('DOMContentLoaded', addPulseAnimation);
    </script>
    """
    st.markdown(js, unsafe_allow_html=True)

def highlight_element(element_selector, duration=2):
    """Temporarily highlight an element on the page.
    
    Args:
        element_selector (str): CSS selector for element to highlight
        duration (int): Duration of highlight in seconds
    """
    highlight_css = f"""
    <style>
    @keyframes highlight {{
        0% {{ background-color: transparent; }}
        50% {{ background-color: rgba(255, 215, 0, 0.3); }}
        100% {{ background-color: transparent; }}
    }}
    
    .highlighted {{
        animation: highlight {duration}s ease-out;
    }}
    </style>
    """
    
    highlight_js = f"""
    <script>
    // Function to highlight element
    function highlightElement() {{
        const elements = document.querySelectorAll('{element_selector}');
        elements.forEach(el => {{
            el.classList.add('highlighted');
            setTimeout(() => el.classList.remove('highlighted'), {duration * 1000});
        }});
    }}
    
    // Execute when DOM is fully loaded
    document.addEventListener('DOMContentLoaded', highlightElement);
    </script>
    """
    
    st.markdown(highlight_css + highlight_js, unsafe_allow_html=True)

def animated_progress_bar(percent, label=None):
    """Display an animated progress bar.
    
    Args:
        percent (float): Percentage completion (0-100)
        label (str, optional): Label to display with the progress bar
    """
    # First show the progress bar at 0%
    progress_container = st.empty()
    label_container = st.empty()
    
    if label:
        label_container.markdown(f"**{label}**")
    
    # Create a placeholder for the progress bar
    progress_placeholder = progress_container.progress(0)
    
    # Animate from 0 to the target percentage
    step = max(1, int(percent / 10))
    for i in range(0, int(percent) + step, step):
        current = min(i, percent)
        progress_placeholder.progress(min(100, current))
        time.sleep(0.05)  # Short delay between updates

def section_transition(old_section, new_section):
    """Handle transition between main sections with animation.
    
    Args:
        old_section (str): Previous section name
        new_section (str): New section name
    """
    # Store the transition in session state
    if 'last_section' not in st.session_state:
        st.session_state.last_section = None
    
    # Determine direction based on section order
    sections_order = ["Games", "Learning Paths", "My Shop", "Skills", "Achievements"]
    
    try:
        old_index = sections_order.index(old_section) if old_section in sections_order else -1
        new_index = sections_order.index(new_section) if new_section in sections_order else -1
        
        if old_index < new_index:
            direction = "right"
        else:
            direction = "left"
    except (ValueError, IndexError):
        direction = "right"
    
    # Update the last section
    st.session_state.last_section = new_section
    
    # Return the direction for use in a slide transition
    return direction