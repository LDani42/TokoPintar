"""
Learning paths for Toko Pintar application.
Organizes game-based learning into structured paths for skill development.
"""
import streamlit as st
from datetime import datetime
from utils.config import get_config
from utils.skills import get_skill_name, get_skill_icon, get_skill_description
from components.learning.real_world_tips import get_tips_for_skill, get_real_world_applications, display_pro_tip
from utils.i18n import tr

# Define learning paths with their milestones and games
LEARNING_PATHS = {
    "inventory": {
        "name": {
            "en": "Inventory Management",
            "id": "Manajemen Inventaris"
        },
        "description": {
            "en": "Learn to track and manage your shop's products efficiently",
            "id": "Pelajari cara melacak dan mengelola produk toko Anda secara efisien"
        },
        "icon": "📦",
        "skill_key": "inventory_management",
        "milestones": [
            {
                "level": 1,
                "name": {
                    "en": "Basics of Counting",
                    "id": "Dasar-dasar Penghitungan"
                },
                "games": ["inventory_game"],
                "min_score": 10
            },
            {
                "level": 2,
                "name": {
                    "en": "Stock Tracking",
                    "id": "Pelacakan Stok"
                },
                "games": ["inventory_game"],
                "min_score": 20
            },
            {
                "level": 3,
                "name": {
                    "en": "Inventory Optimization",
                    "id": "Optimasi Inventaris"
                },
                "games": ["inventory_game"],
                "min_score": 30
            },
            {
                "level": 4,
                "name": {
                    "en": "Inventory Planning",
                    "id": "Perencanaan Inventaris"
                },
                "info": {
                    "en": "Learn to predict stock needs based on sales patterns",
                    "id": "Pelajari cara memprediksi kebutuhan stok berdasarkan pola penjualan"
                },
                "games": ["inventory_game"],
                "min_score": 40
            },
            {
                "level": 5,
                "name": {
                    "en": "Advanced Inventory Management",
                    "id": "Manajemen Inventaris Lanjutan"
                },
                "certificate": True,
                "games": ["inventory_game"],
                "min_score": 50
            }
        ]
    },
    "cash": {
        "name": {
            "en": "Cash Handling",
            "id": "Penanganan Uang Tunai"
        },
        "description": {
            "en": "Master managing money transactions accurately and quickly",
            "id": "Kuasai pengelolaan transaksi uang secara akurat dan cepat"
        },
        "icon": "💰",
        "skill_key": "cash_handling",
        "milestones": [
            {
                "level": 1,
                "name": {
                    "en": "Basic Change Making",
                    "id": "Dasar-dasar Memberikan Kembalian"
                },
                "games": ["change_making"],
                "min_score": 10
            },
            {
                "level": 2,
                "name": {
                    "en": "Quick Calculations",
                    "id": "Perhitungan Cepat"
                },
                "games": ["change_making"],
                "min_score": 20
            },
            {
                "level": 3,
                "name": {
                    "en": "Daily Cash Management",
                    "id": "Pengelolaan Kas Harian"
                },
                "games": ["change_making"],
                "min_score": 30
            },
            {
                "level": 4,
                "name": {
                    "en": "Cash Security",
                    "id": "Keamanan Kas"
                },
                "games": ["change_making"],
                "min_score": 40
            },
            {
                "level": 5,
                "name": {
                    "en": "Advanced Cash Operations",
                    "id": "Operasi Kas Lanjutan"
                },
                "certificate": True,
                "games": ["change_making"],
                "min_score": 50
            }
        ]
    },
    "pricing": {
        "name": {
            "en": "Pricing Strategy",
            "id": "Strategi Penetapan Harga"
        },
        "description": {
            "en": "Learn to set prices for optimal profit and competitiveness",
            "id": "Pelajari cara menetapkan harga untuk keuntungan dan daya saing yang optimal"
        },
        "icon": "🏷️",
        "skill_key": "pricing_strategy",
        "milestones": [
            {
                "level": 1,
                "name": {
                    "en": "Basic Margin Calculation",
                    "id": "Perhitungan Margin Dasar"
                },
                "games": ["margin_calculator"],
                "min_score": 10
            },
            {
                "level": 2,
                "name": {
                    "en": "Profit Optimization",
                    "id": "Optimasi Keuntungan"
                },
                "games": ["margin_calculator"],
                "min_score": 20
            },
            {
                "level": 3,
                "name": {
                    "en": "Competitive Pricing",
                    "id": "Penetapan Harga Kompetitif"
                },
                "games": ["margin_calculator"],
                "min_score": 30
            },
            {
                "level": 4,
                "name": {
                    "en": "Seasonal Pricing",
                    "id": "Penetapan Harga Musiman"
                },
                "games": ["margin_calculator"],
                "min_score": 40
            },
            {
                "level": 5,
                "name": {
                    "en": "Strategic Pricing Master",
                    "id": "Ahli Strategi Penetapan Harga"
                },
                "certificate": True,
                "games": ["margin_calculator"],
                "min_score": 50
            }
        ]
    }
}

def get_available_paths():
    """Get all available learning paths.
    
    Returns:
        dict: All learning paths
    """
    return LEARNING_PATHS

def get_path_progress(path_id):
    """Get progress on a specific learning path.
    
    Args:
        path_id (str): Identifier for the learning path
    
    Returns:
        dict: Progress information
    """
    if path_id not in LEARNING_PATHS:
        return None
    
    path = LEARNING_PATHS[path_id]
    skill_key = path["skill_key"]
    
    # Get current skill level
    current_level = 0
    if hasattr(st.session_state, 'skill_levels') and skill_key in st.session_state.skill_levels:
        current_level = st.session_state.skill_levels[skill_key]
    
    # Calculate milestone progress
    milestones = path["milestones"]
    milestones_count = len(milestones)
    completed_milestones = 0
    
    for milestone in milestones:
        if current_level >= milestone["level"]:
            completed_milestones += 1
    
    # Get current milestone
    current_milestone_idx = min(int(current_level), milestones_count - 1)
    current_milestone = milestones[current_milestone_idx]
    
    # Check if all games for current milestone have been completed
    games_completed = True
    if hasattr(st.session_state, 'game_history'):
        for game_id in current_milestone["games"]:
            # Get highest score for this game
            highest_score = 0
            for game in st.session_state.game_history:
                if game["game_id"] == game_id and game["score"] > highest_score:
                    highest_score = game["score"]
            
            if highest_score < current_milestone.get("min_score", 0):
                games_completed = False
                break
    else:
        games_completed = False
    
    # Get next milestone if applicable
    next_milestone = None
    if current_milestone_idx < milestones_count - 1:
        next_milestone = milestones[current_milestone_idx + 1]
    
    return {
        "path_id": path_id,
        "skill_key": skill_key,
        "current_level": current_level,
        "milestones_count": milestones_count,
        "completed_milestones": completed_milestones,
        "current_milestone": current_milestone,
        "next_milestone": next_milestone,
        "games_completed": games_completed,
        "progress_percent": (completed_milestones / milestones_count) * 100
    }

def show_learning_module(path_id, milestone_level=None):
    """Show a specific learning module with educational content and game links.
    
    Args:
        path_id (str): Identifier for the learning path
        milestone_level (int, optional): Level of milestone to show, defaults to current
    """
    if path_id not in LEARNING_PATHS:
        st.error(tr("learning_path_not_found"))
        return
    
    # Get path info and progress
    path = LEARNING_PATHS[path_id]
    progress = get_path_progress(path_id)
    
    lang = get_config("app.default_language") or "en"
    
    # Determine which milestone to show
    if milestone_level is None:
        milestone_level = int(progress["current_level"])
    
    milestone_idx = min(milestone_level, len(path["milestones"]) - 1)
    milestone = path["milestones"][milestone_idx]
    
    # Show module header
    path_name = path["name"][lang]
    milestone_name = milestone["name"][lang]
    
    st.markdown(f"""
    <div style="background-color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
        <h2 style="color: var(--color-primary); margin-bottom: 10px;">
            {path["icon"]} {path_name}: {milestone_name}
        </h2>
        <div style="height: 8px; background-color: #EEEEEE; border-radius: 4px; margin: 15px 0;">
            <div style="height: 100%; width: {progress['progress_percent']}%; 
                 background-color: var(--color-primary); border-radius: 4px;"></div>
        </div>
        <p style="color: var(--color-text-secondary);">
            {milestone_level}/{len(path['milestones'])} {tr('milestones_completed')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show educational content based on milestone
    st.markdown(f"""
    <div style="background-color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
        <h3 style="color: var(--color-primary); margin-bottom: 15px;">{tr('learning_material')}</h3>
    """, unsafe_allow_html=True)
    
    # Create tabs for different types of learning content
    ed_tabs = st.tabs([
        tr("concepts_tab"),
        tr("pro_tips_tab"),
        tr("real_world_examples_tab"),
        tr("interactive_practice_tab")
    ])
    
    with ed_tabs[0]:  # Concepts tab
        # Show info if available, otherwise show skill description
        if "info" in milestone and lang in milestone["info"]:
            st.write(milestone["info"][lang])
        else:
            st.write(get_skill_description(path["skill_key"], lang))
            
        # Add visual learning aids based on skill type
        if path["skill_key"] == "inventory_management":
            st.markdown("#### Key Inventory Management Principles")
            st.markdown("""
            1. **FIFO (First In, First Out)**: Oldest inventory is sold first
            2. **ABC Analysis**: Categorize items by value and importance
            3. **Par Levels**: Set minimum quantities for automatic reordering
            4. **Cycle Counting**: Count a portion of inventory regularly instead of all at once
            5. **Turnover Ratio**: How quickly inventory is sold and replaced
            """)
            
            # Add a simple inventory tracking template example
            st.markdown("#### Sample Inventory Tracking Sheet")
            
            # Display a sample inventory tracking template
            import pandas as pd
            import numpy as np
            
            # Create sample data
            data = {
                'Product': ['Rice 1kg', 'Cooking Oil 1L', 'Sugar 500g', 'Instant Noodles', 'Soap Bar'],
                'Beginning Count': [25, 15, 20, 30, 12],
                'Received': [10, 5, 0, 24, 0],
                'Sold': [12, 7, 8, 22, 5],
                'Ending Count': [23, 13, 12, 32, 7],
                'Minimum Level': [10, 5, 8, 15, 5]
            }
            
            # Create and display the DataFrame
            df = pd.DataFrame(data)
            st.dataframe(df)
            
        elif path["skill_key"] == "cash_handling":
            st.markdown("#### Cash Handling Best Practices")
            st.markdown("""
            1. **Count Twice**: Always count cash twice before finalizing transactions
            2. **Denominations**: Organize bills by denomination in your cash drawer
            3. **Cash Limits**: Keep minimal cash in registers, deposit excess regularly
            4. **Verification**: Have two people verify large amounts
            5. **Reconciliation**: Balance your cash drawer at the start and end of each day
            """)
            
            # Add visual for cash balancing
            st.markdown("#### Daily Cash Balance Template")
            
            cash_data = {
                'Category': ['Starting Cash', 'Cash Sales', 'Card Sales', 'Total Sales', 'Expected Cash', 'Actual Cash', 'Difference'],
                'Amount (Rp)': ['500,000', '2,345,000', '1,870,000', '4,215,000', '2,845,000', '2,835,000', '-10,000']
            }
            
            cash_df = pd.DataFrame(cash_data)
            st.dataframe(cash_df)
            
        elif path["skill_key"] == "pricing_strategy":
            st.markdown("#### Key Pricing Formulas")
            st.markdown("""
            1. **Markup**: (Selling Price - Cost) ÷ Cost × 100%
            2. **Margin**: (Selling Price - Cost) ÷ Selling Price × 100%
            3. **Setting Price for Target Margin**: Cost ÷ (1 - Desired Margin)
            4. **Break-Even Quantity**: Fixed Costs ÷ Contribution Margin per Unit
            5. **Price Elasticity**: % Change in Quantity ÷ % Change in Price
            """)
            
            # Add visual pricing examples
            st.markdown("#### Margin vs. Markup Comparison")
            
            # Display a sample pricing comparison
            pricing_data = {
                'Cost (Rp)': [10000, 10000, 10000, 10000],
                'Sell Price (Rp)': [12500, 15000, 18000, 20000],
                'Markup %': ['25%', '50%', '80%', '100%'],
                'Margin %': ['20%', '33%', '44%', '50%']
            }
            
            pricing_df = pd.DataFrame(pricing_data)
            st.dataframe(pricing_df)
    
    with ed_tabs[1]:  # Pro Tips tab
        # Show pro tips for this skill level
        tips = get_tips_for_skill(path["skill_key"], milestone_level)
        if tips:
            for tip in tips:
                display_pro_tip(tip)
        else:
            st.info(tr("no_pro_tips_available"))
    
    with ed_tabs[2]:  # Real-World Examples tab
        # Show real-world applications
        applications = get_real_world_applications(path["skill_key"], milestone_level)
        if applications and lang in applications:
            st.markdown(applications[lang])
        else:
            st.info(tr("no_real_world_examples_available"))
    
    with ed_tabs[3]:  # Interactive Practice tab
        # Show interactive practice exercises
        from components.learning.interactive_exercises import show_exercise_set
        show_exercise_set(path["skill_key"])
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Show practice games section
    st.markdown(f"""
    <div style="background-color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
        <h3 style="color: var(--color-primary); margin-bottom: 15px;">{tr('practice_games')}</h3>
        <p>{tr('practice_games_instruction')}</p>
    """, unsafe_allow_html=True)
    
    # List games for this milestone
    for game_id in milestone["games"]:
        # Get game info
        from games import get_game_info
        game_info = get_game_info(game_id)
        
        if game_info:
            game_name = game_info["name"][lang] if lang in game_info["name"] else game_info["name"]["en"]
            game_desc = game_info["description"][lang] if lang in game_info["description"] else game_info["description"]["en"]
            
            # Display game card
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 15px; 
                 background-color: #F8F9FA; padding: 15px; border-radius: 8px;">
                <div style="margin-right: 15px; font-size: 2rem;">{path["icon"]}</div>
                <div style="flex: 1;">
                    <h4 style="margin: 0 0 5px 0;">{game_name}</h4>
                    <p style="margin: 0 0 10px 0; color: var(--color-text-secondary);">{game_desc}</p>
                    <p style="margin: 0;">{tr('target_score')}: {milestone.get("min_score", 0)}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Play button with unique key including path and milestone info
            play_text = tr("play_game")
            unique_key = f"learning_path_{path_id}_milestone_{milestone_level}_play_{game_id}"
            if st.button(play_text, key=unique_key):
                st.session_state.current_game = game_id
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Show certificate section if this milestone offers one
    if milestone.get("certificate", False):
        st.markdown(f"""
        <div style="background-color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: var(--color-primary); margin-bottom: 15px;">{tr('skill_certificate')}</h3>
            <p>{tr('skill_certificate_instruction')}</p>
        """, unsafe_allow_html=True)
        
        # Check if certificate is already earned
        certificate_earned = False
        if progress["current_level"] >= milestone_level:
            certificate_earned = True
            
            # Show certificate preview
            from components.learning.certificates import display_certificate_preview
            display_certificate_preview(path_id, milestone_level)
        else:
            # Show certificate requirements
            requirements_text = tr("requirements")
            st.markdown(f"#### {requirements_text}")
            
            # List games and required scores
            for game_id in milestone["games"]:
                game_info = get_game_info(game_id)
                if game_info:
                    game_name = game_info["name"][lang] if lang in game_info["name"] else game_info["name"]["en"]
                    st.markdown(f"- {game_name}: {tr('score_at_least')} {milestone.get('min_score', 0)} {tr('points')}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Navigation buttons
    st.markdown("<div style='display: flex; justify-content: space-between;'>", unsafe_allow_html=True)
    
    # Back button
    back_text = tr("back_to_learning_paths")
    if st.button(back_text, key="back_to_paths"):
        st.session_state.selected_learning_path = None
        st.session_state.selected_milestone = None
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_learning_paths():
    """Show available learning paths and allow selection."""
    lang = get_config("app.default_language") or "en"
    
    # Check if a path is already selected
    if "selected_learning_path" in st.session_state and st.session_state.selected_learning_path:
        # Show specific learning path module
        path_id = st.session_state.selected_learning_path
        milestone = st.session_state.selected_milestone if "selected_milestone" in st.session_state else None
        show_learning_module(path_id, milestone)
        return
    
    # Show paths overview
    st.markdown(f"""
    <div style="background-color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
        <h2 style="color: var(--color-primary); margin-bottom: 10px;">{tr('learning_paths_title')}</h2>
        <p>{tr('choose_learning_path_instruction')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # List all available paths
    paths = get_available_paths()
    
    # Using 2-column layout
    col1, col2 = st.columns(2)
    
    for i, (path_id, path) in enumerate(paths.items()):
        # Alternate between columns
        col = col1 if i % 2 == 0 else col2
        
        with col:
            # Get progress for this path
            progress = get_path_progress(path_id)
            
            # Get path details
            path_name = path["name"][lang]
            path_desc = path["description"][lang]
            path_icon = path["icon"]
            
            # Create card for this path
            st.markdown(f"""
            <div style="background-color: white; padding: 20px; border-radius: 8px; 
                 margin-bottom: 20px; border-left: 4px solid var(--color-primary);">
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <div style="font-size: 2rem; margin-right: 15px;">{path_icon}</div>
                    <div>
                        <h3 style="margin: 0;">{path_name}</h3>
                        <p style="color: var(--color-text-secondary); margin: 5px 0 0 0;">
                            {tr('level_label')} {int(progress["current_level"]) + 1}/5
                        </p>
                    </div>
                </div>
                <p style="margin-bottom: 15px;">{path_desc}</p>
                <div style="height: 8px; background-color: #EEEEEE; border-radius: 4px; margin-bottom: 15px;">
                    <div style="height: 100%; width: {progress['progress_percent']}%; 
                         background-color: var(--color-primary); border-radius: 4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Continue button
            continue_text = tr("continue_learning")
            if st.button(continue_text, key=f"continue_{path_id}"):
                st.session_state.selected_learning_path = path_id
                st.session_state.selected_milestone = None
                st.rerun()