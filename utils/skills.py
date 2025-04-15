"""
Skills progression system for Toko Pintar application.
"""
import streamlit as st
from datetime import datetime
from utils.db import db
from utils.config import get_config
from utils.achievements import check_achievements

# Skill definitions with display names
SKILL_DEFINITIONS = {
    "inventory_management": {
        "name": "Inventory Management",
        "name_id": "Manajemen Inventaris",
        "description": "Ability to track and manage product stock",
        "description_id": "Kemampuan melacak dan mengelola stok produk",
        "icon": "📦"
    },
    "cash_handling": {
        "name": "Cash Handling", 
        "name_id": "Penanganan Uang Tunai",
        "description": "Ability to handle money transactions accurately",
        "description_id": "Kemampuan menangani transaksi uang secara akurat",
        "icon": "💰"
    },
    "pricing_strategy": {
        "name": "Pricing Strategy",
        "name_id": "Strategi Penetapan Harga",
        "description": "Ability to set prices for optimal profit",
        "description_id": "Kemampuan menetapkan harga untuk keuntungan optimal",
        "icon": "📊"
    },
    "customer_relations": {
        "name": "Customer Relations",
        "name_id": "Hubungan Pelanggan",
        "description": "Ability to build customer loyalty",
        "description_id": "Kemampuan membangun loyalitas pelanggan",
        "icon": "🤝"
    },
    "bookkeeping": {
        "name": "Bookkeeping",
        "name_id": "Pembukuan",
        "description": "Ability to maintain financial records",
        "description_id": "Kemampuan memelihara catatan keuangan",
        "icon": "📒"
    }
}

# Map games to primary and secondary skills they affect
GAME_SKILL_MAPPING = {
    "inventory_game": {
        "primary": "inventory_management",
        "secondary": None
    },
    "change_making": {
        "primary": "cash_handling",
        "secondary": None
    },
    "margin_calculator": {
        "primary": "pricing_strategy",
        "secondary": "bookkeeping"
    },
    "customer_service": {
        "primary": "customer_relations",
        "secondary": None
    },
    "cash_reconciliation": {
        "primary": "cash_handling",
        "secondary": "bookkeeping"
    },
    "simple_accounting": {
        "primary": "bookkeeping",
        "secondary": None
    }
}

def initialize_skills():
    """Initialize skill levels in session state if not present."""
    if 'skill_levels' not in st.session_state:
        st.session_state.skill_levels = {
            "inventory_management": 0,
            "cash_handling": 0,
            "pricing_strategy": 0,
            "customer_relations": 0,
            "bookkeeping": 0
        }

def update_skills(game_id, score):
    """Update player skills based on the game played and score earned.
    
    Args:
        game_id (str): Identifier of the game played
        score (int): Score earned in the game
        
    Returns:
        dict: Updated skills information
    """
    initialize_skills()
    
    # Get skill increase amount from config
    skill_increase = get_config("gameplay.skill_increase_amount") or 0.2
    max_skill_level = get_config("gameplay.max_skill_level") or 5
    
    # Update relevant skills
    updated_skills = {}
    
    if game_id in GAME_SKILL_MAPPING:
        # Update primary skill
        primary_skill = GAME_SKILL_MAPPING[game_id]["primary"]
        if score > 0:
            # Calculate skill increase based on score
            # Higher scores give more skill points
            score_factor = min(1.0, score / 30)  # Normalize to max of 1.0
            increase_amount = skill_increase * score_factor
            
            # Update the skill
            current_level = st.session_state.skill_levels[primary_skill]
            new_level = min(max_skill_level, current_level + increase_amount)
            st.session_state.skill_levels[primary_skill] = new_level
            
            updated_skills[primary_skill] = {
                "old_level": current_level,
                "new_level": new_level,
                "increased": new_level > current_level
            }
            
            # Update in database if user is logged in
            if hasattr(st.session_state, 'user_id'):
                db.update_skill(st.session_state.user_id, primary_skill, new_level)
        
        # Update secondary skill if present
        secondary_skill = GAME_SKILL_MAPPING[game_id]["secondary"]
        if secondary_skill and score > 0:
            # Secondary skills increase at half the rate
            increase_amount = (skill_increase * 0.5) * min(1.0, score / 30)
            
            current_level = st.session_state.skill_levels[secondary_skill]
            new_level = min(max_skill_level, current_level + increase_amount)
            st.session_state.skill_levels[secondary_skill] = new_level
            
            updated_skills[secondary_skill] = {
                "old_level": current_level,
                "new_level": new_level,
                "increased": new_level > current_level
            }
            
            # Update in database if user is logged in
            if hasattr(st.session_state, 'user_id'):
                db.update_skill(st.session_state.user_id, secondary_skill, new_level)
    
    # Update total score
    if 'total_score' not in st.session_state:
        st.session_state.total_score = 0
    st.session_state.total_score += score
    
    # Update in database if user is logged in
    if hasattr(st.session_state, 'user_id'):
        db.update_total_score(st.session_state.user_id, st.session_state.total_score)
    
    # Record game in history
    if 'game_history' not in st.session_state:
        st.session_state.game_history = []
        
    game_entry = {
        "game_id": game_id,
        "score": score,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    st.session_state.game_history.append(game_entry)
    
    # Add to database if user is logged in
    if hasattr(st.session_state, 'user_id'):
        db.add_game_history(st.session_state.user_id, game_id, score)
    
    # Update shop level
    update_shop_level()
    
    # Check for achievements
    new_achievements = check_achievements()
    
    return {
        "updated_skills": updated_skills,
        "new_achievements": new_achievements,
        "score": score,
        "total_score": st.session_state.total_score,
        "shop_level": st.session_state.shop_level
    }

def update_shop_level():
    """Update shop level based on skill levels.
    
    Returns:
        bool: True if shop level changed, False otherwise
    """
    if 'skill_levels' not in st.session_state:
        return False
    
    # Get threshold from config
    threshold = get_config("gameplay.shop_level_threshold") or 1.0
    
    # Calculate average skill level
    skill_values = list(st.session_state.skill_levels.values())
    avg_skill = sum(skill_values) / len(skill_values)
    
    # Shop levels start at 1, max at 5
    old_level = st.session_state.shop_level if 'shop_level' in st.session_state else 1
    new_level = max(1, min(5, int(avg_skill / threshold) + 1))
    
    # Update session state if changed
    if new_level != old_level:
        st.session_state.shop_level = new_level
        
        # Update in database if user is logged in
        if hasattr(st.session_state, 'user_id'):
            db.update_shop_level(st.session_state.user_id, new_level)
        
        return True
    
    # Ensure shop_level exists in session state
    if 'shop_level' not in st.session_state:
        st.session_state.shop_level = new_level
    
    return False

def get_skill_name(skill_id, language='en'):
    """Get the display name for a skill."""
    if skill_id in SKILL_DEFINITIONS:
        if language == 'id':
            return SKILL_DEFINITIONS[skill_id]["name_id"]
        return SKILL_DEFINITIONS[skill_id]["name"]
    return skill_id

def get_skill_icon(skill_id):
    """Get the icon for a skill."""
    if skill_id in SKILL_DEFINITIONS:
        return SKILL_DEFINITIONS[skill_id]["icon"]
    return "📝"

def get_skill_description(skill_id, language='en'):
    """Get the description for a skill."""
    if skill_id in SKILL_DEFINITIONS:
        if language == 'id':
            return SKILL_DEFINITIONS[skill_id]["description_id"]
        return SKILL_DEFINITIONS[skill_id]["description"]
    return ""