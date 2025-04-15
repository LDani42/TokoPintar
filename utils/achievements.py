"""
Achievement system for Toko Pintar application.
"""
import streamlit as st
from datetime import datetime
from utils.db import db

# Achievement definitions
ACHIEVEMENTS = [
    {
        "id": "first_steps",
        "name": "First Steps",
        "name_id": "Langkah Pertama",
        "description": "Complete the onboarding process",
        "description_id": "Menyelesaikan proses orientasi",
        "check": lambda: hasattr(st.session_state, 'onboarding_completed') and st.session_state.onboarding_completed
    },
    {
        "id": "first_game",
        "name": "Game Beginner",
        "name_id": "Pemula Permainan",
        "description": "Play your first mini-game",
        "description_id": "Memainkan permainan mini pertama Anda",
        "check": lambda: len(st.session_state.game_history) >= 1
    },
    {
        "id": "inventory_master",
        "name": "Inventory Master",
        "name_id": "Ahli Inventaris",
        "description": "Reach level 3 in inventory management",
        "description_id": "Mencapai level 3 dalam manajemen inventaris",
        "check": lambda: st.session_state.skill_levels["inventory_management"] >= 3
    },
    {
        "id": "math_whiz",
        "name": "Math Whiz", 
        "name_id": "Ahli Matematika",
        "description": "Score perfectly in 3 math-related games in a row",
        "description_id": "Skor sempurna dalam 3 permainan matematika berturut-turut",
        "check": lambda: check_math_whiz()
    },
    {
        "id": "shop_upgrade",
        "name": "Shop Upgrade",
        "name_id": "Peningkatan Toko",
        "description": "Reach shop level 2",
        "description_id": "Mencapai level toko 2",
        "check": lambda: st.session_state.shop_level >= 2
    },
    {
        "id": "financial_guru",
        "name": "Financial Guru",
        "name_id": "Guru Keuangan",
        "description": "Score over 30 points in margin calculator game",
        "description_id": "Skor lebih dari 30 poin dalam permainan kalkulator margin",
        "check": lambda: any(g["game_id"] == "margin_calculator" and g["score"] >= 30 for g in st.session_state.game_history)
    },
    {
        "id": "consistent_player",
        "name": "Consistent Player",
        "name_id": "Pemain Konsisten",
        "description": "Play at least 10 games total",
        "description_id": "Mainkan setidaknya 10 permainan total",
        "check": lambda: len(st.session_state.game_history) >= 10
    },
    {
        "id": "cash_expert",
        "name": "Cash Expert",
        "name_id": "Ahli Kas",
        "description": "Reach level 3 in cash handling",
        "description_id": "Mencapai level 3 dalam penanganan uang tunai",
        "check": lambda: st.session_state.skill_levels["cash_handling"] >= 3
    },
    {
        "id": "pricing_pro",
        "name": "Pricing Pro",
        "name_id": "Ahli Penetapan Harga",
        "description": "Reach level 3 in pricing strategy",
        "description_id": "Mencapai level 3 dalam strategi penetapan harga",
        "check": lambda: st.session_state.skill_levels["pricing_strategy"] >= 3
    }
]

def check_math_whiz():
    """Helper function to check the Math Whiz achievement."""
    if len(st.session_state.game_history) < 3:
        return False
    
    # Get the last 3 games
    last_3_games = st.session_state.game_history[-3:]
    
    # Check if they are all math games with perfect scores
    math_games = ["change_making", "margin_calculator"]
    all_math_games = all(g["game_id"] in math_games for g in last_3_games)
    
    # Define perfect scores for each game
    perfect_scores = {
        "change_making": 30,
        "margin_calculator": 30
    }
    
    all_perfect = all(g["score"] >= perfect_scores.get(g["game_id"], 0) for g in last_3_games)
    
    return all_math_games and all_perfect

def check_achievements():
    """Check for and award any earned achievements.
    
    Returns:
        list: Newly earned achievements
    """
    new_achievements = []
    
    # Check achievements in session state
    achieved_ids = set()
    if hasattr(st.session_state, 'achievements'):
        for achievement in st.session_state.achievements:
            # The session state uses "id" while the database uses "achievement_type"
            if "id" in achievement:
                achieved_ids.add(achievement["id"])
            elif "achievement_type" in achievement:
                achieved_ids.add(achievement["achievement_type"])
    
    # Check each achievement
    for achievement in ACHIEVEMENTS:
        # Skip already earned achievements
        if achievement["id"] in achieved_ids:
            continue
        
        # Check if achievement should be earned
        if achievement["check"]():
            # Add to database
            if hasattr(st.session_state, 'user_id'):
                db.add_achievement(st.session_state.user_id, achievement["id"])
            
            # Add to session state for immediate display
            new_achievement = {
                "id": achievement["id"],
                "name": achievement["name"],
                "description": achievement["description"],
                "earned_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            if not hasattr(st.session_state, 'achievements'):
                st.session_state.achievements = []
                
            st.session_state.achievements.append(new_achievement)
            new_achievements.append(new_achievement)
    
    return new_achievements

def display_achievement(achievement):
    """Display an achievement notification."""
    st.balloons()
    st.success(f"🏆 Achievement Unlocked: **{achievement['name']}**")
    st.info(achievement['description'])

def get_achievement_details(achievement_id):
    """Get the details of an achievement by ID."""
    for achievement in ACHIEVEMENTS:
        if achievement["id"] == achievement_id:
            return achievement
    return None

def add_achievement(achievement_id, custom_description=None):
    """Manually add an achievement to the user's profile.
    
    Args:
        achievement_id (str): The ID of the achievement to add
        custom_description (str, optional): Optional custom description
    
    Returns:
        dict: The added achievement, or None if not found
    """
    # Get achievement details
    achievement_details = get_achievement_details(achievement_id)
    if not achievement_details:
        return None
    
    # Check if already earned
    achieved_ids = set()
    if hasattr(st.session_state, 'achievements'):
        for achievement in st.session_state.achievements:
            if "id" in achievement:
                achieved_ids.add(achievement["id"])
            elif "achievement_type" in achievement:
                achieved_ids.add(achievement["achievement_type"])
    
    if achievement_id in achieved_ids:
        return None  # Already earned
    
    # Add to database
    if hasattr(st.session_state, 'user_id'):
        db.add_achievement(st.session_state.user_id, achievement_id)
    
    # Use custom description if provided
    description = custom_description if custom_description else achievement_details["description"]
    
    # Add to session state for immediate display
    new_achievement = {
        "id": achievement_id,
        "name": achievement_details["name"],
        "description": description,
        "earned_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if not hasattr(st.session_state, 'achievements'):
        st.session_state.achievements = []
    
    st.session_state.achievements.append(new_achievement)
    return new_achievement