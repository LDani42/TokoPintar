"""
Game level utilities for Toko Pintar application.
Provides standardized level management across different games.
"""
import streamlit as st
from utils.config import get_config
from utils.i18n import tr

def display_level_selection(game_id, level_descriptions, get_level_limits=None, on_level_select=None):
    """Display a standardized level selection UI.
    
    Args:
        game_id (str): Game identifier
        level_descriptions (dict): Dictionary of level descriptions keyed by level number
        get_level_limits (callable, optional): Function to get time limits for levels
        on_level_select (callable, optional): Function to call when level is selected
    """
    # Get language preference
    lang = get_config("app.default_language") or "en"
    
    # Determine available levels based on player's skill
    skill_level = 0
    
    # Get the primary skill for this game
    from games import get_game_info
    game_info = get_game_info(game_id)
    if game_info and "primary_skill" in game_info:
        primary_skill = game_info["primary_skill"]
        if hasattr(st.session_state, "skill_levels") and primary_skill in st.session_state.skill_levels:
            skill_level = st.session_state.skill_levels[primary_skill]
    
    max_available_level = min(5, max(1, int(skill_level) + 1))
    
    # Display level selection UI
    st.markdown(tr('level_selection_header'))
    
    # Create level selection cards
    cols = st.columns(5)
    level_selected = None
    
    for i, col in enumerate(cols):
        level_num = i + 1
        is_unlocked = level_num <= max_available_level
        
        with col:
            level_title = tr('level_title', level_num=level_num)
            
            # Get short description for this level
            desc_key = "en" if lang == "en" else "id"
            level_desc = ""
            if level_num in level_descriptions:
                level_desc_data = level_descriptions[level_num]
                if isinstance(level_desc_data, dict) and desc_key in level_desc_data:
                    level_desc = level_desc_data[desc_key].split('.')[0]
                elif isinstance(level_desc_data, str):
                    level_desc = level_desc_data.split('.')[0]
            
            # Get color for game type
            game_colors = {
                "inventory_game": "#4CAF50",  # Green for inventory
                "change_making": "#FF9800",   # Orange for cash
                "margin_calculator": "#7E57C2" # Purple for pricing
            }
            color = game_colors.get(game_id, "#2196F3")  # Default to blue
            
            # Display time limit if available
            time_info = ""
            if get_level_limits:
                time_limit = get_level_limits(level_num)
                if time_limit:
                    time_text = tr('time_text')
                    time_info = f"⏱️ {time_limit} {time_text}"
            
            # Create a card for each level with appropriate styling
            if is_unlocked:
                st.markdown(f"""
                <div style="padding: 10px; border-radius: 8px; border: 2px solid {color}; text-align: center; margin-bottom: 10px; cursor: pointer; height: 120px;">
                    <h4 style="margin: 0;">{level_title}</h4>
                    <p style="font-size: 0.8em; margin: 5px 0; height: 40px;">{level_desc}</p>
                    <div style="margin-top: 5px; font-size: 0.8em;">{time_info}</div>
                    <div style="margin-top: 5px; color: {color};">{tr('unlocked_text')}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Button to select this level
                if st.button(tr('select_level_button', level_num=level_num), key=f"select_{game_id}_level_{level_num}"):
                    level_selected = level_num
            else:
                # Locked level
                st.markdown(f"""
                <div style="padding: 10px; border-radius: 8px; border: 2px solid #ccc; text-align: center; margin-bottom: 10px; opacity: 0.7; height: 120px;">
                    <h4 style="margin: 0;">{level_title}</h4>
                    <p style="font-size: 0.8em; margin: 5px 0; height: 40px;">{level_desc}</p>
                    <div style="margin-top: 5px; font-size: 0.8em;">{time_info}</div>
                    <div style="margin-top: 5px; color: #888;">{tr('locked_text')}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Return selected level, or call the provided callback
    if level_selected and on_level_select:
        on_level_select(level_selected)
    
    return level_selected

def display_level_header(level, descriptions, tips=None):
    """Display a standardized level header with description and tips.
    
    Args:
        level (int): Current level number
        descriptions (dict): Dictionary of level descriptions
        tips (dict, optional): Dictionary of tips for each level
    """
    # Get language preference
    lang = get_config("app.default_language") or "en"
    
    # Level colors based on difficulty
    level_colors = {
        1: "#4CAF50",  # Green for beginner
        2: "#2196F3",  # Blue for easy
        3: "#FF9800",  # Orange for medium
        4: "#E91E63",  # Pink for hard
        5: "#9C27B0"   # Purple for expert
    }
    
    # Level text translation (with formatting)
    level_text = tr('level_text', level=level)
    # Defensive: descriptions should be a dict of lang -> level -> desc
    if isinstance(descriptions, dict) and lang in descriptions:
        level_descs = descriptions[lang]
    else:
        level_descs = descriptions.get('en', {})
    level_desc = level_descs.get(level, "")
    
    st.markdown(f"""
    <div style="background-color: {level_colors.get(level, '#2196F3')}; color: white; padding: 12px 20px; border-radius: 8px; margin-bottom: 15px;">
        <div style="font-size: 1.2em; font-weight: bold;">
            {level_text}
        </div>
        <div style="font-size: 1.1em;">{level_desc}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display tips in an info box if provided
    if tips and level in tips:
        tip_text = ""
        if isinstance(tips[level], dict) and lang in tips[level]:
            tip_text = tips[level][lang]
        elif isinstance(tips[level], str):
            tip_text = tips[level]
            
        if tip_text:
            st.info(tr('tip_text', tip=tip_text))

def display_timer(start_time, time_limit):
    """Display a timer for timed levels.
    
    Args:
        start_time (float): Start time from time.time()
        time_limit (int): Time limit in seconds
        
    Returns:
        float: Remaining time in seconds
    """
    import time
    
    # Get language preference
    lang = get_config("app.default_language") or "en"
    
    # Calculate remaining time
    elapsed_time = time.time() - start_time
    remaining_time = max(0, time_limit - elapsed_time)
    
    # Calculate progress percentage for color coding
    time_percentage = remaining_time / time_limit
    timer_color = "#4CAF50" if time_percentage > 0.6 else "#FF9800" if time_percentage > 0.3 else "#F44336"
    
    # Display timer with color-coded progress
    st.markdown(f"""
    <div style="margin-bottom: 15px;">
        <div style="height: 8px; background-color: #e0e0e0; border-radius: 4px; width: 100%;">
            <div style="height: 100%; width: {time_percentage * 100}%; background-color: {timer_color}; border-radius: 4px;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 5px;">
            <span style="font-size: 0.8em; color: #757575;">0s</span>
            <span style="font-size: 0.9em; font-weight: bold; color: {timer_color};">
                {int(remaining_time)} {tr('seconds_text', seconds=remaining_time)}
            </span>
            <span style="font-size: 0.8em; color: #757575;">{time_limit}s</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    return remaining_time

def display_score_breakdown(base_score, level_bonus=0, time_bonus=0, accuracy_bonus=0, lang="en"):
    """Display a standardized score breakdown.
    
    Args:
        base_score (int): Base score
        level_bonus (int): Bonus for level difficulty
        time_bonus (int): Bonus for quick completion
        accuracy_bonus (int): Bonus for accuracy
        lang (str): Language code
    
    Returns:
        int: Total score
    """
    total_score = base_score + level_bonus + time_bonus + accuracy_bonus
    
    # Translations
    score_breakdown = tr('score_breakdown_text')
    base_score_text = tr('base_score_text')
    level_bonus_text = tr('level_bonus_text')
    time_bonus_text = tr('time_bonus_text')
    accuracy_bonus_text = tr('accuracy_bonus_text')
    total_score_text = tr('total_score_text')
    points = tr('points_text')
    
    # Create score breakdown table
    st.markdown(f"### {score_breakdown}")
    
    score_table = f"""
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 15px;">
        <tr style="background-color: #f0f0f0;">
            <th style="padding: 8px; text-align: left; border: 1px solid #ddd;">{tr('component_text')}</th>
            <th style="padding: 8px; text-align: right; border: 1px solid #ddd;">{tr('points_text')}</th>
        </tr>
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;">{base_score_text}</td>
            <td style="padding: 8px; text-align: right; border: 1px solid #ddd;">+{base_score}</td>
        </tr>
    """
    
    if level_bonus > 0:
        score_table += f"""
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;">{level_bonus_text}</td>
            <td style="padding: 8px; text-align: right; border: 1px solid #ddd;">+{level_bonus}</td>
        </tr>
        """
    
    if time_bonus > 0:
        score_table += f"""
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;">{time_bonus_text}</td>
            <td style="padding: 8px; text-align: right; border: 1px solid #ddd;">+{time_bonus}</td>
        </tr>
        """
    
    if accuracy_bonus > 0:
        score_table += f"""
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;">{accuracy_bonus_text}</td>
            <td style="padding: 8px; text-align: right; border: 1px solid #ddd;">+{accuracy_bonus}</td>
        </tr>
        """
    
    # Add total score row
    score_table += f"""
        <tr style="font-weight: bold; background-color: #E8F5E9;">
            <td style="padding: 8px; border: 1px solid #ddd;">{total_score_text}</td>
            <td style="padding: 8px; text-align: right; border: 1px solid #ddd;">{total_score}</td>
        </tr>
    </table>
    """
    
    st.markdown(score_table, unsafe_allow_html=True)
    
    return total_score

def display_game_end_buttons(level, accuracy, lang="en"):
    """Display standardized buttons at the end of a game.
    
    Args:
        level (int): Current level
        accuracy (float): Accuracy percentage
        lang (str): Language code
        
    Returns:
        tuple: (next_level, retry, main_menu) button clicked states
    """
    col1, col2 = st.columns(2)
    next_level_clicked = False
    retry_clicked = False
    main_menu_clicked = False
    
    if accuracy >= 80 and level < 5:
        with col1:
            next_level_text = tr('next_level_button')
            next_level_clicked = st.button(next_level_text, key="next_level_button", type="primary")
    
    with col1 if (accuracy < 80 or level >= 5) else col2:
        retry_text = tr('retry_button', accuracy=accuracy)
        retry_clicked = st.button(retry_text, key="retry_button")
    
    with col2 if (accuracy < 80 or level >= 5) else col1:
        main_menu_text = tr('main_menu_button')
        main_menu_clicked = st.button(main_menu_text, key="main_menu_button")
        
    return next_level_clicked, retry_clicked, main_menu_clicked