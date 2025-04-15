"""
Scoreboard and progress display components for Toko Pintar application.
"""
import streamlit as st
import pandas as pd
from utils.config import get_config
from utils.i18n import tr

def display_score_sidebar():
    """Display the player's score and stats in the sidebar."""
    # Player name and score
    st.sidebar.markdown(f"### {st.session_state.player_name}'s Stats")
    
    total_score = st.session_state.total_score if hasattr(st.session_state, 'total_score') else 0
    st.sidebar.markdown(f'<p class="score-text">{tr("score")}: {total_score:,}</p>', unsafe_allow_html=True)
    
    # Shop level
    shop_level = st.session_state.shop_level if hasattr(st.session_state, 'shop_level') else 1
    max_level = 5
    st.sidebar.markdown(f"**{tr('shop_level')}:** {shop_level}/{max_level}")
    st.sidebar.progress(shop_level / max_level)
    
    # Show skill levels
    if hasattr(st.session_state, 'skill_levels'):
        st.sidebar.markdown("---")
        st.sidebar.markdown("### {tr('skills_overview')}")
        
        from utils.skills import get_skill_name, get_skill_icon
        
        lang = get_config("app.default_language") or "en"
        max_skill_level = get_config("gameplay.max_skill_level") or 5
        
        for skill, level in st.session_state.skill_levels.items():
            # Format skill name for display
            display_name = get_skill_name(skill, lang)
            icon = get_skill_icon(skill)
            
            st.sidebar.write(f"{icon} {display_name}:")
            st.sidebar.progress(min(1.0, level / max_skill_level))

def display_game_results(results):
    """Display game results in a structured format.
    
    Args:
        results (dict): Game results including score, skill updates, etc.
    """
    st.markdown(f"### {tr('game_results')}")
    
    # Show score
    st.markdown(f'<p class="score-text">{tr("score")}: {results["score"]} {tr("points")}</p>', unsafe_allow_html=True)
    
    # Show skill improvements
    if "updated_skills" in results and results["updated_skills"]:
        st.markdown(f"#### {tr('skill_improvements')}")
        
        from utils.skills import get_skill_name, get_skill_icon
        lang = get_config("app.default_language") or "en"
        
        for skill, info in results["updated_skills"].items():
            if info["increased"]:
                name = get_skill_name(skill, lang)
                icon = get_skill_icon(skill)
                st.markdown(f"{icon} **{name}**: {info['old_level']:.1f} → {info['new_level']:.1f}")
    
    # Show new achievements
    if "new_achievements" in results and results["new_achievements"]:
        st.markdown(f"#### {tr('new_achievements')}")
        st.balloons()
        
        for achievement in results["new_achievements"]:
            st.markdown(f"""
            <div class="achievement-card">
                <span class="achievement-name">🏆 {achievement['name']}</span><br>
                {achievement['description']}
            </div>
            """, unsafe_allow_html=True)
    
    # Show total score
    st.markdown(f"**{tr('total_score')}: {results['total_score']:,}")
    
    # Shop level update
    if "old_shop_level" in results and results["old_shop_level"] != results["shop_level"]:
        st.success(tr('shop_upgraded', shop_level=results['shop_level']))

def display_game_history_table():
    """Display game history in a table format."""
    if not hasattr(st.session_state, 'game_history') or not st.session_state.game_history:
        st.info(tr('no_game_history'))
        return
    
    # Game name mapping
    game_name_map = {
        "inventory_game": tr('inventory_game'),
        "change_making": tr('change_making'),
        "margin_calculator": tr('margin_calculator'),
        "customer_service": tr('customer_service'),
        "cash_reconciliation": tr('cash_reconciliation'),
        "simple_accounting": tr('simple_accounting')
    }
    
    # Create DataFrame for display
    history = st.session_state.game_history[-10:]  # Last 10 games
    
    # Format game names
    display_data = []
    for game in history:
        display_data.append({
            tr('game'): game_name_map.get(game["game_id"], game["game_id"]),
            tr('score'): game["score"],
            tr('date'): game["timestamp"].split()[0],
            tr('time'): game["timestamp"].split()[1]
        })
    
    # Create and display the table
    df = pd.DataFrame(display_data)
    st.table(df)

def display_skill_progress_chart():
    """Display a chart showing skill progress over time."""
    import matplotlib.pyplot as plt
    
    if not hasattr(st.session_state, 'game_history') or len(st.session_state.game_history) < 2:
        st.info(tr('play_more_games'))
        return
    
    # Get skill level snapshots from game history
    # This would require storing skill levels with each game history entry
    # For now, we'll just show current skills
    
    # Set up the chart
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Data for the chart
    skills = list(st.session_state.skill_levels.keys())
    values = list(st.session_state.skill_levels.values())
    
    # Create labels with proper formatting
    from utils.skills import get_skill_name
    lang = get_config("app.default_language") or "en"
    labels = [get_skill_name(skill, lang) for skill in skills]
    
    # Create the bar chart
    bars = ax.bar(labels, values, color='#1E88E5')
    
    # Add some styling
    ax.set_ylabel(tr('skill_level'))
    ax.set_title(tr('your_current_skills'))
    ax.set_ylim(0, 5)  # Assuming max skill level is 5
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height:.1f}', ha='center', va='bottom')
    
    # Display the chart
    st.pyplot(fig)

def display_educational_tip(category):
    """Display an educational tip based on category.
    
    Args:
        category (str): Tip category (inventory, cash, pricing, etc.)
    """
    # Use the more comprehensive tips from the learning module if possible
    from components.learning.real_world_tips import get_tips_for_skill, display_pro_tip
    
    # Map game categories to skill keys
    skill_map = {
        "inventory": "inventory_management",
        "cash": "cash_handling",
        "pricing": "pricing_strategy",
        "customer": "customer_relations",
        "bookkeeping": "bookkeeping"
    }
    
    # Determine player's current level in this skill
    skill_key = skill_map.get(category)
    level = 1
    if skill_key and hasattr(st.session_state, 'skill_levels') and skill_key in st.session_state.skill_levels:
        level = max(1, int(st.session_state.skill_levels[skill_key]) + 1)
    
    # Get tips for this skill and level
    if skill_key:
        tips = get_tips_for_skill(skill_key, level)
        if tips:
            # Display a random tip
            import random
            tip = random.choice(tips)
            display_pro_tip(tip)
            return
    
    # Fallback to simple tips if no advanced tips available
    simple_tips = {
        "inventory": [
            tr('inventory_tip1'),
            tr('inventory_tip2'),
            tr('inventory_tip3')
        ],
        "cash": [
            tr('cash_tip1'),
            tr('cash_tip2'),
            tr('cash_tip3')
        ],
        "pricing": [
            tr('pricing_tip1'),
            tr('pricing_tip2'),
            tr('pricing_tip3')
        ],
        "customer": [
            tr('customer_tip1'),
            tr('customer_tip2'),
            tr('customer_tip3')
        ],
        "bookkeeping": [
            tr('bookkeeping_tip1'),
            tr('bookkeeping_tip2'),
            tr('bookkeeping_tip3')
        ]
    }
    
    # Select a random tip from the category
    import random
    if category in simple_tips and simple_tips[category]:
        tip_content = random.choice(simple_tips[category])
        st.markdown(f"""
        <div style="background-color: #E3F2FD; border-left: 4px solid #42A5F5; 
             padding: 15px; margin: 15px 0; border-radius: 4px;">
            <strong>{tr('tip')}:</strong> {tip_content}
        </div>
        """, unsafe_allow_html=True)
        
def display_simple_calculator():
    """Display a simple calculator for basic operations."""
    with st.expander(tr('simple_calculator')):
        st.markdown("""
        <style>
        .calculator {
            background-color: #f5f5f5;
            border-radius: 10px;
            padding: 15px;
            width: 100%;
        }
        .calc-display {
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
            font-family: monospace;
            font-size: 18px;
            text-align: right;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Initialize calculator state if needed
        if 'calc_num1' not in st.session_state:
            st.session_state.calc_num1 = ""
            st.session_state.calc_num2 = ""
            st.session_state.calc_op = ""
            st.session_state.calc_result = ""
            st.session_state.calc_display = "0"
            
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Current calculation display
            st.markdown(f"""
            <div class="calculator">
                <div class="calc-display">{st.session_state.calc_display}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            # Clear button
            if st.button(tr('clear'), key="calc_clear"):
                st.session_state.calc_num1 = ""
                st.session_state.calc_num2 = ""
                st.session_state.calc_op = ""
                st.session_state.calc_result = ""
                st.session_state.calc_display = "0"
                st.rerun()
                
        # Number entry and operations
        col1, col2, col3 = st.columns(3)
        
        # Function to handle number input
        def on_number_click(num):
            if st.session_state.calc_op == "":
                # First number
                if st.session_state.calc_num1 == "" and num == "0":
                    st.session_state.calc_num1 = "0"
                elif st.session_state.calc_num1 == "0" and num != ".":
                    st.session_state.calc_num1 = num
                else:
                    # Check if we're adding a decimal point
                    if num == "." and "." in st.session_state.calc_num1:
                        pass  # Don't add another decimal
                    else:
                        st.session_state.calc_num1 += num
                st.session_state.calc_display = st.session_state.calc_num1
            else:
                # Second number
                if st.session_state.calc_num2 == "" and num == "0":
                    st.session_state.calc_num2 = "0"
                elif st.session_state.calc_num2 == "0" and num != ".":
                    st.session_state.calc_num2 = num
                else:
                    # Check if we're adding a decimal point
                    if num == "." and "." in st.session_state.calc_num2:
                        pass  # Don't add another decimal
                    else:
                        st.session_state.calc_num2 += num
                st.session_state.calc_display = f"{st.session_state.calc_num1} {st.session_state.calc_op} {st.session_state.calc_num2}"
                
        # Function to handle operation
        def on_op_click(op):
            if st.session_state.calc_num1 == "":
                # Handle operations on empty calculator
                return
                
            if st.session_state.calc_num2 != "":
                # Calculate previous operation first
                calculate_result()
                st.session_state.calc_num1 = st.session_state.calc_result
                st.session_state.calc_num2 = ""
                
            st.session_state.calc_op = op
            st.session_state.calc_display = f"{st.session_state.calc_num1} {op}"
                
        # Function to calculate result
        def calculate_result():
            try:
                num1 = float(st.session_state.calc_num1)
                num2 = float(st.session_state.calc_num2)
                
                if st.session_state.calc_op == "+":
                    st.session_state.calc_result = str(num1 + num2)
                elif st.session_state.calc_op == "-":
                    st.session_state.calc_result = str(num1 - num2)
                elif st.session_state.calc_op == "×":
                    st.session_state.calc_result = str(num1 * num2)
                elif st.session_state.calc_op == "÷":
                    if num2 == 0:
                        st.session_state.calc_result = "Error"
                    else:
                        st.session_state.calc_result = str(num1 / num2)
                else:
                    return
                    
                # Format result for display
                try:
                    result_float = float(st.session_state.calc_result)
                    if result_float.is_integer():
                        st.session_state.calc_result = str(int(result_float))
                    else:
                        # Limit decimal places for cleaner display
                        st.session_state.calc_result = str(round(result_float, 4))
                except:
                    pass  # Keep as is if formatting fails
                
                # Update display
                st.session_state.calc_display = f"{st.session_state.calc_num1} {st.session_state.calc_op} {st.session_state.calc_num2} = {st.session_state.calc_result}"
                
            except ValueError:
                st.session_state.calc_result = "Error"
                st.session_state.calc_display = "Error"
                
        # Number buttons
        number_grid = [
            ["7", "8", "9"], 
            ["4", "5", "6"],
            ["1", "2", "3"],
            ["0", ".", "="]
        ]
        
        # Create number pad
        for row in number_grid:
            cols = st.columns(3)
            for i, num in enumerate(row):
                if num == "=":
                    if cols[i].button("=", key=f"calc_{num}"):
                        if st.session_state.calc_num1 != "" and st.session_state.calc_num2 != "" and st.session_state.calc_op != "":
                            calculate_result()
                            # Reset for new calculation but keep result as first number
                            st.session_state.calc_num1 = st.session_state.calc_result
                            st.session_state.calc_num2 = ""
                            st.session_state.calc_op = ""
                            st.rerun()
                else:
                    if cols[i].button(num, key=f"calc_{num}"):
                        on_number_click(num)
                        st.rerun()
                        
        # Operation buttons
        ops = ["+", "-", "×", "÷"]
        op_cols = st.columns(4)
        for i, op in enumerate(ops):
            if op_cols[i].button(op, key=f"calc_{op}"):
                on_op_click(op)
                st.rerun()