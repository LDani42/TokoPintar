"""
Margin Calculator mini-game for Toko Pintar application.
"""
import streamlit as st
import random
import time
from utils.config import get_config
from utils.skills import update_skills
from components.scoreboard import display_educational_tip
from utils.db import db
from utils.i18n import tr

def initialize_margin_challenge(level=1):
    """Initialize a margin calculation challenge based on level.
    
    Args:
        level (int): Game difficulty level
    """
    # Get products from database
    all_products = db.get_products()
    if not all_products:
        # Fall back to sample products if database is empty
        from utils.config import SAMPLE_PRODUCTS
        all_products = SAMPLE_PRODUCTS
    
    # Select a random product
    product = random.choice(all_products)
    
    # Choose challenge type based on level
    if level == 1:
        # Level 1: Find selling price given buy price and margin (simple)
        challenge_type = "find_sell_price"
        target_margin = random.randint(20, 40)  # Simple margins
        # Round to nearest 100
        correct_sell_price = round(product["buy_price"] * (1 + target_margin/100), -2)
        
        challenge = {
            "level": level,
            "product": product,
            "type": challenge_type,
            "target_margin": target_margin,
            "correct_answer": correct_sell_price,
            "user_answer": 0
        }
    
    elif level == 2:
        # Level 2: Find margin percentage given buy and sell price
        challenge_type = "find_margin_percent"
        # Calculate the correct margin
        correct_margin = round(((product["sell_price"] - product["buy_price"]) / product["buy_price"]) * 100)
        
        challenge = {
            "level": level,
            "product": product,
            "type": challenge_type,
            "correct_answer": correct_margin,
            "user_answer": 0
        }
    
    elif level == 3:
        # Level 3: Find profit given buy price, sell price, and quantity
        challenge_type = "find_profit"
        quantity = random.randint(5, 15)
        correct_profit = (product["sell_price"] - product["buy_price"]) * quantity
        
        challenge = {
            "level": level,
            "product": product,
            "type": challenge_type,
            "quantity": quantity,
            "correct_answer": correct_profit,
            "user_answer": 0
        }
    
    elif level == 4:
        # Level 4: Find break-even point given fixed costs and margins
        challenge_type = "find_breakeven"
        fixed_cost = random.randint(1, 5) * 100000  # Between 100K and 500K
        margin_per_unit = product["sell_price"] - product["buy_price"]
        correct_units = round(fixed_cost / margin_per_unit)
        
        challenge = {
            "level": level,
            "product": product,
            "type": challenge_type,
            "fixed_cost": fixed_cost,
            "correct_answer": correct_units,
            "user_answer": 0
        }
    
    else:
        # Level 5: Find optimal price given elasticity
        challenge_type = "find_optimal_price"
        current_price = product["sell_price"]
        current_demand = random.randint(50, 200)
        elasticity = round(random.uniform(0.8, 2.0), 1)  # Price elasticity of demand
        
        # Current revenue
        current_revenue = current_price * current_demand
        
        # Optimal price given elasticity
        if elasticity != 1:
            optimal_markup = 1 / (elasticity - 1)
            optimal_price = round(product["buy_price"] * (1 + optimal_markup), -2)
        else:
            # Special case for unit elasticity
            optimal_price = current_price
        
        challenge = {
            "level": level,
            "product": product,
            "type": challenge_type,
            "current_demand": current_demand,
            "elasticity": elasticity,
            "correct_answer": optimal_price,
            "user_answer": 0
        }
    
    # Set time limit based on level
    time_limits = {
        1: None,          # Level 1: No time limit for beginners
        2: None,          # Level 2: No time limit for percentage learning
        3: 60,            # Level 3: Moderate time limit
        4: 60,            # Level 4: Challenging time limit
        5: 60             # Level 5: Challenging time limit with complex calculation
    }
    
    # Add time tracking and level information
    challenge["start_time"] = time.time()
    challenge["time_limit"] = time_limits.get(level)
    challenge["level_description"] = get_level_description(level)
    challenge["level_tips"] = get_level_tips(level)
    
    # Store in session state
    st.session_state.margin_calculator = challenge

def get_level_description(level):
    """Get description text for each level.
    
    Args:
        level (int): Game difficulty level
        
    Returns:
        dict: Descriptions in English and Indonesian
    """
    descriptions = {
        1: {
            "en": "Simple selling price calculation. Find the right price based on cost and target margin.",
            "id": "Perhitungan harga jual sederhana. Temukan harga yang tepat berdasarkan biaya dan target margin."
        },
        2: {
            "en": "Margin percentage calculation. Calculate the margin based on selling and buying prices.",
            "id": "Perhitungan persentase margin. Hitung margin berdasarkan harga jual dan harga beli."
        },
        3: {
            "en": "Profit calculation with quantity. Find total profit from multiple sales with time pressure.",
            "id": "Perhitungan keuntungan dengan kuantitas. Temukan total keuntungan dari beberapa penjualan dengan tekanan waktu."
        },
        4: {
            "en": "Break-even point analysis. Calculate how many units you need to sell to cover fixed costs.",
            "id": "Analisis titik impas. Hitung berapa unit yang perlu Anda jual untuk menutupi biaya tetap."
        },
        5: {
            "en": "Advanced pricing strategy with elasticity. Find optimal price for maximum profit.",
            "id": "Strategi penetapan harga lanjutan dengan elastisitas. Temukan harga optimal untuk keuntungan maksimal."
        }
    }
    
    return descriptions.get(level, descriptions[1])

def get_level_tips(level):
    """Get tips specific to each level.
    
    Args:
        level (int): Game difficulty level
        
    Returns:
        dict: Tips in English and Indonesian
    """
    tips = {
        1: {
            "en": "Remember to use the formula: Selling Price = Buy Price × (1 + Margin%/100)",
            "id": "Ingat untuk menggunakan rumus: Harga Jual = Harga Beli × (1 + Margin%/100)"
        },
        2: {
            "en": "To find margin percentage: ((Sell Price - Buy Price) ÷ Buy Price) × 100",
            "id": "Untuk menemukan persentase margin: ((Harga Jual - Harga Beli) ÷ Harga Beli) × 100"
        },
        3: {
            "en": "Calculate profit per item first, then multiply by quantity. Work quickly under time pressure.",
            "id": "Hitung keuntungan per item terlebih dahulu, lalu kalikan dengan jumlah. Bekerja cepat di bawah tekanan waktu."
        },
        4: {
            "en": "Break-even point = Fixed Costs ÷ (Selling Price - Buy Price)",
            "id": "Titik impas = Biaya Tetap ÷ (Harga Jual - Harga Beli)"
        },
        5: {
            "en": "When elasticity > 1, demand is elastic. When elasticity < 1, demand is inelastic. This affects optimal pricing.",
            "id": "Ketika elastisitas > 1, permintaan bersifat elastis. Ketika elastisitas < 1, permintaan bersifat inelastis. Ini memengaruhi penetapan harga optimal."
        }
    }
    
    return tips.get(level, tips[1])

def margin_calculator_game():
    """Margin calculator mini-game implementation."""
    # Get language preference
    lang = get_config("app.default_language") or "en"
    
    # Force initialization at the start of the game function
    # This must happen before any other code that uses the session state
    if "margin_calculator" not in st.session_state:
        st.info(tr('margin_game_initializing'))
        initialize_margin_challenge(1)
        st.rerun()
        return
    
    # Add JavaScript to disable mousewheel on number inputs
    st.markdown("""
    <script>
    // Disable mousewheel on number inputs
    document.addEventListener('DOMContentLoaded', function() {
        // Initial application
        disableMouseWheelForNumberInputs();
        
        // Set up a mutation observer to watch for new inputs that might be added
        const observer = new MutationObserver(function(mutations) {
            disableMouseWheelForNumberInputs();
        });
        
        // Start observing the document body for DOM changes
        observer.observe(document.body, { 
            childList: true,
            subtree: true
        });
        
        function disableMouseWheelForNumberInputs() {
            // Get all number input elements
            const numberInputs = document.querySelectorAll('input[type="number"]');
            
            // Add wheel event listener to each one
            numberInputs.forEach(function(input) {
                // Only add the listener once
                if (!input.dataset.wheelDisabled) {
                    input.addEventListener('wheel', function(e) {
                        // Prevent the default wheel behavior
                        e.preventDefault();
                    });
                    // Mark this input as having the wheel disabled
                    input.dataset.wheelDisabled = 'true';
                }
            });
        }
    });
    </script>
    """, unsafe_allow_html=True)
    
    # Game title
    st.markdown(f'<p class="game-title">{tr("margin_calculator_title")}</p>', unsafe_allow_html=True)
    st.write(tr("margin_calculator_description"))
    
    # Display educational tip
    display_educational_tip("pricing")
    
    # Add game mechanics tooltip button
    try:
        from utils.tooltips import show_mechanics_tooltip_button, add_tooltips_to_page
        col1, col2 = st.columns([3, 1])
        with col2:
            show_mechanics_tooltip_button("margin_calculator", game_id="margin_calculator")
        
        # Add tooltips JavaScript
        add_tooltips_to_page()
    except ImportError:
        # Tooltips module not available, skip
        pass
    
    # Set up level selection or start game
    if "margin_calculator" not in st.session_state:
        # Determine available levels based on player's skill
        skill_level = st.session_state.skill_levels.get("pricing_strategy", 0) if hasattr(st.session_state, "skill_levels") else 0
        max_available_level = min(5, max(1, int(skill_level) + 1))
        
        # Display level selection UI
        st.markdown(f"### {tr('select_difficulty_level')}")
        
        # Create level selection cards
        cols = st.columns(5)
        level_selected = None
        
        for i, col in enumerate(cols):
            level_num = i + 1
            is_unlocked = level_num <= max_available_level
            
            with col:
                level_title = f"Level {level_num}"
                
                # Get short description
                desc_key = "en" if lang == "en" else "id"
                level_desc = get_level_description(level_num)[desc_key].split('.')[0]
                
                # Create a card for each level with appropriate styling
                if is_unlocked:
                    st.markdown(f"""
                    <div style="padding: 10px; border-radius: 8px; border: 2px solid #7E57C2; text-align: center; margin-bottom: 10px; cursor: pointer; height: 120px;">
                        <h4 style="margin: 0;">{level_title}</h4>
                        <p style="font-size: 0.8em; margin: 5px 0; height: 40px;">{level_desc}</p>
                        <div style="margin-top: 5px; color: #7E57C2;">Unlocked ✓</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Button to select this level
                    if st.button(f"Select Level {level_num}", key=f"select_margin_level_{level_num}"):
                        level_selected = level_num
                else:
                    # Locked level
                    st.markdown(f"""
                    <div style="padding: 10px; border-radius: 8px; border: 2px solid #ccc; text-align: center; margin-bottom: 10px; opacity: 0.7; height: 120px;">
                        <h4 style="margin: 0;">{level_title}</h4>
                        <p style="font-size: 0.8em; margin: 5px 0; height: 40px;">{level_desc}</p>
                        <div style="margin-top: 5px; color: #888;">🔒 Locked</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Initialize game if a level was selected
        if level_selected:
            initialize_margin_challenge(level_selected)
    
    # Get game state - we've already initialized it at the top of the function
    challenge = st.session_state.margin_calculator
    level = challenge["level"]
    product = challenge["product"]
    challenge_type = challenge["type"]
    
    # Check if there's a time limit
    if challenge.get("time_limit"):
        elapsed_time = time.time() - challenge["start_time"]
        remaining_time = max(0, challenge["time_limit"] - elapsed_time)
        
        # Display timer with color-coded progress based on remaining time percentage
        time_percentage = remaining_time / challenge["time_limit"]
        timer_color = "#4CAF50" if time_percentage > 0.6 else "#FF9800" if time_percentage > 0.3 else "#F44336"
        
        st.markdown(f"""
        <div style="margin-bottom: 15px;">
            <div style="height: 8px; background-color: #e0e0e0; border-radius: 4px; width: 100%;">
                <div style="height: 100%; width: {time_percentage * 100}%; background-color: {timer_color}; border-radius: 4px;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                <span style="font-size: 0.8em; color: #757575;">0s</span>
                <span style="font-size: 0.9em; font-weight: bold; color: {timer_color};">
                    {int(remaining_time)} {'seconds' if lang == 'en' else 'detik'}
                </span>
                <span style="font-size: 0.8em; color: #757575;">{challenge["time_limit"]}s</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Auto-submit if time is up
        if remaining_time <= 0 and not challenge.get("submitted"):
            times_up = "Time's up" if lang == "en" else "Waktu habis"
            st.warning(f"{times_up}! Your answer has been submitted.")
            challenge["submitted"] = True
            st.rerun()
    
    # Level badge and description
    level_colors = {
        1: "#4CAF50",
        2: "#2196F3",
        3: "#FF9800",
        4: "#9C27B0",
        5: "#F44336"
    }
    level_color = level_colors.get(level, "#7E57C2")
    level_desc = challenge.get("level_description", {}).get(lang, "")
    level_tips = challenge.get("level_tips", {}).get(lang, "")
    st.markdown(f"""
    <div style='display: flex; align-items: center; margin-bottom: 15px;'>
        <div style='background-color: {level_color}; color: white; padding: 5px 10px; border-radius: 15px; font-weight: bold; margin-right: 10px;'>
            {tr('level')} {level}
        </div>
        <div style='font-size: 1.1em;'>{level_desc}</div>
    </div>
    """, unsafe_allow_html=True)
    st.info(f"💡 **{tr('tip')}:** {level_tips}")
    
    # Display the challenge in a more visual way
    from utils.config import get_product_emoji
    product_emoji = get_product_emoji(product)
    
    product_name = product["name_id"] if lang == "id" and "name_id" in product else product["name"]
    
    # Create product card
    st.markdown(f"""
    <div style='background-color: #f5f5f5; padding: 15px; border-radius: 10px; margin-bottom: 20px; 
         border-left: 5px solid #1E88E5;'>
        <h3 style='margin-top: 0;'>{product_emoji} {product_name}</h3>
    """, unsafe_allow_html=True)
    
    if challenge_type == "find_sell_price":
        target_margin = challenge["target_margin"]
        buy_price = product['buy_price']
        
        # Calculate expected answer for verification
        expected_answer = buy_price * (1 + target_margin/100)
        rounded_answer = round(expected_answer, -2)
        
        # Display debug info if needed
        if get_config("debug.enabled"):
            st.write(f"Debug - Buy price: {buy_price}, Margin: {target_margin}%, Expected: {expected_answer}, Rounded: {rounded_answer}")
        
        buy_price_text = tr('buy_price')
        target_margin_text = tr('target_margin')
        
        # Display product info in product card
        st.markdown(f"""
        <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
            <span style='font-weight: bold;'>{buy_price_text}:</span>
            <span class='cash-amount'>Rp {product['buy_price']:,}</span>
        </div>
        <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
            <span style='font-weight: bold;'>{target_margin_text}:</span>
            <span>{target_margin}%</span>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Challenge description
        task_text = tr('set_selling_price_task')
        
        # Show formula guidance for lower levels
        if level <= 2:
            calculated_value = buy_price * (1 + target_margin/100)
            rounded_value = round(calculated_value, -2)
            
            st.markdown(f"""
            <div style='background-color: #e3f2fd; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
                <p style='font-weight: bold;'>Formula:</p>
                <div class='math-formula'>
                    Selling Price = Buy Price × (1 + Margin%/100)
                </div>
                <div class='math-formula'>
                    Selling Price = {buy_price:,} × (1 + {target_margin}/100) = {buy_price:,} × {1 + target_margin/100:.2f}
                </div>
                <div class='math-formula'>
                    Selling Price = {calculated_value:.0f} ≈ {rounded_value:,.0f} (rounded to nearest 100 Rp)
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.warning(task_text)
        
        # Visual calculator-style input
        st.markdown("<div style='background-color: #f1f8e9; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)
        
        input_label = tr('selling_price_input_label')
        st.markdown(f"<h4>{input_label}</h4>", unsafe_allow_html=True)
        
        # --- Quick Calculator: placed directly below the input label ---
        with st.expander("Quick Calculator", expanded=True):
            expr = st.text_input("Enter calculation (e.g., 123*1.2+50):", key="margin_calc_input")
            if expr:
                try:
                    result = eval(expr, {"__builtins__": {}})
                    st.success(f"Result: {result}")
                except Exception:
                    st.error("Invalid expression.")
        
        # Calculator input with Rp prefix
        col1, col2 = st.columns([1, 4])
        
        with col1:
            st.markdown("<div style='background-color: #e0e0e0; height: 38px; border-radius: 5px 0 0 5px; display: flex; align-items: center; justify-content: center; font-weight: bold;'>Rp</div>", unsafe_allow_html=True)
        
        with col2:
            answer = st.number_input(
                "Price",
                min_value=0,
                max_value=1000000,
                value=int(challenge["user_answer"]),
                step=100,
                label_visibility="collapsed"
            )
            challenge["user_answer"] = answer
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif challenge_type == "find_margin_percent":
        buy_price = product['buy_price']
        sell_price = product['sell_price']
        
        # Calculate expected answer for verification
        diff = sell_price - buy_price
        expected_margin = (diff / buy_price) * 100
        rounded_margin = round(expected_margin)
        
        # Display debug info if needed
        if get_config("debug.enabled"):
            st.write(f"Debug - Buy: {buy_price}, Sell: {sell_price}, Diff: {diff}, Margin: {expected_margin}%, Rounded: {rounded_margin}%")
        
        buy_price_text = tr('buy_price')
        sell_price_text = tr('sell_price')
        
        # Display product info in product card
        st.markdown(f"""
        <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
            <span style='font-weight: bold;'>{buy_price_text}:</span>
            <span class='cash-amount'>Rp {buy_price:,}</span>
        </div>
        <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
            <span style='font-weight: bold;'>{sell_price_text}:</span>
            <span class='cash-amount'>Rp {sell_price:,}</span>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        task_text = tr('margin_percent_task')
        
        # Show formula guidance for lower levels
        if level <= 2:
                # Calculate step by step for educational purposes
                price_diff = sell_price - buy_price
                division_result = price_diff / buy_price
                percentage = division_result * 100
                rounded = round(percentage)
                
                st.markdown(f"""
                <div style='background-color: #e3f2fd; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
                    <p style='font-weight: bold;'>Formula:</p>
                    <div class='math-formula'>
                        Margin % = ((Sell Price - Buy Price) ÷ Buy Price) × 100
                    </div>
                    <div class='math-formula'>
                        Margin % = (({sell_price:,} - {buy_price:,}) ÷ {buy_price:,}) × 100
                    </div>
                    <div class='math-formula'>
                        Margin % = ({price_diff:,} ÷ {buy_price:,}) × 100 = {division_result:.4f} × 100 = {percentage:.2f}% ≈ {rounded}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
        st.warning(task_text)
        
        # Visual percentage slider
        st.markdown("<div style='background-color: #f1f8e9; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)
        
        input_label = tr('margin_percent_input_label')
        st.markdown(f"<h4>{input_label}</h4>", unsafe_allow_html=True)
        
        # Use slider for more intuitive percentage selection
        answer = st.slider(
            "Margin %",
            min_value=0,
            max_value=100,
            value=int(challenge["user_answer"]),
            step=1,
            label_visibility="collapsed"
        )
        challenge["user_answer"] = answer
        
        # Visual percentage display
        st.markdown(f"""
        <div style='background-color: white; padding: 15px; border-radius: 5px; 
                 border: 1px solid #ccc; margin: 10px 0; text-align: center;'>
            <span style='font-size: 24px; font-weight: bold; color: #5C6BC0;'>
                {answer}%
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif challenge_type == "find_profit":
        quantity = challenge["quantity"]
        buy_price = product['buy_price']
        sell_price = product['sell_price']
        
        # Calculate expected answer for verification
        profit_per_item = sell_price - buy_price
        expected_profit = profit_per_item * quantity
        
        # Display debug info if needed
        if get_config("debug.enabled"):
            st.write(f"Debug - Buy: {buy_price}, Sell: {sell_price}, Profit per item: {profit_per_item}, Quantity: {quantity}, Total profit: {expected_profit}")
        
        buy_price_text = tr('buy_price')
        sell_price_text = tr('sell_price')
        quantity_text = tr('quantity_sold')
        
        # Display product info in product card with quantity visualization
        st.markdown(f"""
        <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
            <span style='font-weight: bold;'>{buy_price_text}:</span>
            <span class='cash-amount'>Rp {buy_price:,}</span>
        </div>
        <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
            <span style='font-weight: bold;'>{sell_price_text}:</span>
            <span class='cash-amount'>Rp {sell_price:,}</span>
        </div>
        <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
            <span style='font-weight: bold;'>{quantity_text}:</span>
            <span>{quantity}</span>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Visual quantity representation
        st.markdown("<div style='margin: 15px 0;'>", unsafe_allow_html=True)
        
        # Display items with product-specific emoji
        emoji = product_emoji  # Reuse the product emoji
        
        # Create a visual grid of items
        item_html = f"""
        <div style='display: flex; flex-wrap: wrap; justify-content: center; margin-bottom: 20px; background-color: #f9fbe7; padding: 10px; border-radius: 5px;'>
        """
        
        for i in range(min(quantity, 30)):  # Limit to 30 items max for display
            item_html += f"<div style='font-size: 24px; margin: 5px;'>{emoji}</div>"
        
        if quantity > 30:
            item_html += f"<div style='font-size: 16px; margin: 5px;'>+{quantity - 30} more</div>"
            
        item_html += "</div>"
        
        st.markdown(item_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        task_text = tr('profit_task')
        
        # Show formula guidance for lower levels
        if level <= 2:
            st.markdown(f"""
            <div style='background-color: #e3f2fd; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
                <p style='font-weight: bold;'>Formula:</p>
                <div class='math-formula'>
                    Profit per item = Sell Price - Buy Price
                </div>
                <div class='math-formula'>
                    Profit per item = {sell_price:,} - {buy_price:,} = {profit_per_item:,}
                </div>
                <div class='math-formula'>
                    Total Profit = Profit per item × Quantity
                </div>
                <div class='math-formula'>
                    Total Profit = {profit_per_item:,} × {quantity} = {expected_profit:,}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.warning(task_text)
        
        # Visual calculator-style input
        st.markdown("<div style='background-color: #f1f8e9; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)
        
        input_label = tr('profit_input_label')
        st.markdown(f"<h4>{input_label}</h4>", unsafe_allow_html=True)
        
        # Calculator input with Rp prefix
        col1, col2 = st.columns([1, 4])
        
        with col1:
            st.markdown("<div style='background-color: #e0e0e0; height: 38px; border-radius: 5px 0 0 5px; display: flex; align-items: center; justify-content: center; font-weight: bold;'>Rp</div>", unsafe_allow_html=True)
        
        with col2:
            answer = st.number_input(
                "Profit",
                min_value=0,
                max_value=1000000,
                value=int(challenge["user_answer"]),
                step=1000,
                label_visibility="collapsed"
            )
            challenge["user_answer"] = answer
            
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif challenge_type == "find_breakeven":
        fixed_cost = challenge["fixed_cost"]
        
        buy_price_text = tr('buy_price')
        sell_price_text = tr('sell_price')
        fixed_cost_text = tr('fixed_cost')
        
        st.write(f"**{buy_price_text}:** Rp {product['buy_price']:,}")
        st.write(f"**{sell_price_text}:** Rp {product['sell_price']:,}")
        st.write(f"**{fixed_cost_text}:** Rp {fixed_cost:,}")
        
        task_text = tr('breakeven_task')
        
        st.warning(task_text)
        
        # Input for break-even units
        input_label = tr('breakeven_input_label')
        answer = st.number_input(
            input_label,
            min_value=0,
            max_value=10000,
            value=int(challenge["user_answer"]),
            step=1
        )
        challenge["user_answer"] = answer
    
    elif challenge_type == "find_optimal_price":
        current_demand = challenge["current_demand"]
        elasticity = challenge["elasticity"]
        
        buy_price_text = tr('buy_price')
        current_price_text = tr('current_price')
        current_demand_text = tr('current_monthly_demand')
        elasticity_text = tr('price_elasticity')
        
        st.write(f"**{buy_price_text}:** Rp {product['buy_price']:,}")
        st.write(f"**{current_price_text}:** Rp {product['sell_price']:,}")
        st.write(f"**{current_demand_text}:** {current_demand} units")
        st.write(f"**{elasticity_text}:** {elasticity}")
        
        # Add explanation for elasticity
        elasticity_explanation = """
        *Price elasticity measures how demand changes when price changes:*
        - *Elasticity > 1: Demand is elastic, price increases reduce total revenue*
        - *Elasticity < 1: Demand is inelastic, price increases raise total revenue*
        """
        st.info(elasticity_explanation)
        
        task_text = tr('optimal_price_task')
        
        st.warning(task_text)
        
        # Input for optimal price
        input_label = tr('optimal_price_input_label')
        answer = st.number_input(
            input_label,
            min_value=product["buy_price"],
            max_value=product["buy_price"] * 5,
            value=int(challenge["user_answer"] or product["sell_price"]),
            step=100
        )
        challenge["user_answer"] = answer
    
    # Submit button with enhanced styling
    submit_text = tr('submit_button')
    check_button_clicked = st.button(
        submit_text,
        key="check_margin_answer",
        type="primary",
    )
    
    if check_button_clicked or challenge.get("submitted"):
        challenge["submitted"] = True
        
        correct_answer = challenge["correct_answer"]
        user_answer = challenge["user_answer"]
        
        # Allow for some margin of error based on challenge type
        tolerance = 0
        if challenge_type == "find_sell_price":
            tolerance = 100  # 100 Rp difference allowed
        elif challenge_type == "find_margin_percent":
            tolerance = 1    # 1% difference allowed
        elif challenge_type == "find_profit":
            tolerance = 1000  # 1000 Rp difference allowed
        elif challenge_type == "find_breakeven":
            tolerance = 1    # 1 unit difference allowed
        elif challenge_type == "find_optimal_price":
            tolerance = 500  # 500 Rp difference allowed
        
        is_correct = abs(user_answer - correct_answer) <= tolerance
        
        # Calculate end time and elapsed time
        end_time = time.time()
        elapsed_time = end_time - challenge["start_time"]
        
        # Calculate score components
        # Base scores increase with level difficulty
        base_scores = {
            1: 10,  # Level 1: Basic score
            2: 15,  # Level 2: Slightly higher
            3: 20,  # Level 3: Moderate
            4: 25,  # Level 4: Challenging
            5: 30   # Level 5: Expert
        }
        
        base_score = base_scores.get(level, 15)
        level_bonus = level * 2  # 2 points per level
        time_bonus = 0
        accuracy_bonus = 0
        
        # Calculate score
        if is_correct:
            # Base and level bonus
            score = base_score + level_bonus
            
            # Time bonus for quick answers on timed levels
            if challenge.get("time_limit"):
                if elapsed_time < challenge["time_limit"]:
                    # More time bonus for higher levels and quicker answers
                    time_factor = 1 - (elapsed_time / challenge["time_limit"])
                    time_bonus = int(15 * time_factor * (level / 3))  # Scale with level
                    score += time_bonus
            
            # Accuracy bonus for exact answers
            if abs(user_answer - correct_answer) < (tolerance / 2):
                accuracy_bonus = 5 * level  # Higher accuracy bonus for higher levels
                score += accuracy_bonus
        else:
            # No points for incorrect answers
            score = 0
            
        # Display results in a visually appealing container
        st.markdown("<div style='background-color: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px 0;'>", unsafe_allow_html=True)
        
        # Results header
        results_title = "Results" if lang == "en" else "Hasil"
        st.markdown(f"<h3 style='margin-top: 0;'>{results_title}</h3>", unsafe_allow_html=True)
        
        # Display different results based on correctness
        if is_correct:
            # Celebration for correct answer
            correct_text = tr('correct_feedback')
            answer_text = "The correct answer is" if lang == "en" else "Jawaban yang benar adalah"
            
            # Format answer based on challenge type
            if challenge_type in ["find_sell_price", "find_profit", "find_optimal_price"]:
                formatted_answer = f"Rp {correct_answer:,}"
            elif challenge_type == "find_margin_percent":
                formatted_answer = f"{correct_answer}%"
            else:
                formatted_answer = f"{correct_answer}"
            
            # Display success message with animation
            st.markdown(f"""
            <div style="background-color: #E8F5E9; border-left: 4px solid #4CAF50; padding: 15px; margin-bottom: 20px; border-radius: 4px;">
                <h4 style="color: #2E7D32; margin-top: 0;">✅ {correct_text}!</h4>
                <p style="margin-bottom: 5px;">{answer_text}: <strong>{formatted_answer}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show score breakdown
            st.markdown("<h4>Score Breakdown</h4>", unsafe_allow_html=True)
            
            # Create score breakdown table
            score_table = f"""
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 15px;">
                <tr style="background-color: #f0f0f0;">
                    <th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Component</th>
                    <th style="padding: 8px; text-align: right; border: 1px solid #ddd;">Points</th>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd;">Base Score (Level {level})</td>
                    <td style="padding: 8px; text-align: right; border: 1px solid #ddd;">+{base_score}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd;">Difficulty Bonus</td>
                    <td style="padding: 8px; text-align: right; border: 1px solid #ddd;">+{level_bonus}</td>
                </tr>
            """
            
            if time_bonus > 0:
                time_bonus_text = "Time Bonus" if lang == "en" else "Bonus Waktu"
                score_table += f"""
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd;">{time_bonus_text} ({int(challenge["time_limit"] - elapsed_time)}s saved)</td>
                    <td style="padding: 8px; text-align: right; border: 1px solid #ddd;">+{time_bonus}</td>
                </tr>
                """
                
            if accuracy_bonus > 0:
                accuracy_text = "Perfect Accuracy Bonus" if lang == "en" else "Bonus Akurasi Sempurna"
                score_table += f"""
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd;">{accuracy_text}</td>
                    <td style="padding: 8px; text-align: right; border: 1px solid #ddd;">+{accuracy_bonus}</td>
                </tr>
                """
            
            # Add total score row
            total_text = "Total Score" if lang == "en" else "Skor Total"
            score_table += f"""
                <tr style="font-weight: bold; background-color: #E8F5E9;">
                    <td style="padding: 8px; border: 1px solid #ddd;">{total_text}</td>
                    <td style="padding: 8px; text-align: right; border: 1px solid #ddd;">{score}</td>
                </tr>
            </table>
            """
            
            st.markdown(score_table, unsafe_allow_html=True)
            
            # Add visual celebration for perfect score
            if accuracy_bonus > 0 and level >= 4:
                st.balloons()
                st.markdown(f"""
                <div style="padding: 20px; text-align: center; background-color: #FFF9C4; border-radius: 10px; margin: 20px 0;">
                    <h2 style="color: #FF9800; margin-bottom: 10px;">🏆 {level_text} Master! 🏆</h2>
                    <p style="font-size: 1.2em;">Perfect price calculation at this advanced level is exceptional!</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Display incorrect answer message
            incorrect_text = tr('incorrect_feedback')
            correct_text = "The correct answer is" if lang == "en" else "Jawaban yang benar adalah"
            
            # Format answers based on challenge type
            if challenge_type in ["find_sell_price", "find_profit", "find_optimal_price"]:
                formatted_correct = f"Rp {correct_answer:,}"
                formatted_user = f"Rp {user_answer:,}"
            elif challenge_type == "find_margin_percent":
                formatted_correct = f"{correct_answer}%"
                formatted_user = f"{user_answer}%"
            else:
                formatted_correct = f"{correct_answer}"
                formatted_user = f"{user_answer}"
            
            your_answer = "Your answer" if lang == "en" else "Jawaban Anda"
            
            st.markdown(f"""
            <div style="background-color: #FFEBEE; border-left: 4px solid #F44336; padding: 15px; margin-bottom: 20px; border-radius: 4px;">
                <h4 style="color: #C62828; margin-top: 0;">❌ {incorrect_text}</h4>
                <p style="margin-bottom: 5px;">{your_answer}: <span style="text-decoration: line-through;">{formatted_user}</span></p>
                <p style="margin-bottom: 0;">{correct_text}: <strong>{formatted_correct}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show that no points were earned
            no_points = "No points earned for incorrect answers" if lang == "en" else "Tidak ada poin yang didapat untuk jawaban yang salah"
            st.markdown(f"<p><i>{no_points}</i></p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Provide educational explanation
        if challenge_type == "find_sell_price":
            target_margin = challenge["target_margin"]
            
            explanation = f"""
            <div class="edu-tip">
                <strong>To calculate the selling price with a {target_margin}% margin:</strong><br>
                Selling Price = Buy Price × (1 + Margin %)<br>
                Selling Price = {product['buy_price']:,} × (1 + {target_margin}/100)<br>
                Selling Price = {product['buy_price']:,} × {1 + target_margin/100}<br>
                Selling Price = {correct_answer:,} (rounded to nearest 100)
            </div>
            """
            st.markdown(explanation, unsafe_allow_html=True)
        
        elif challenge_type == "find_margin_percent":
            explanation = f"""
            <div class="edu-tip">
                <strong>To calculate the margin percentage:</strong><br>
                Margin % = ((Sell Price - Buy Price) ÷ Buy Price) × 100<br>
                Margin % = (({product['sell_price']:,} - {product['buy_price']:,}) ÷ {product['buy_price']:,}) × 100<br>
                Margin % = ({product['sell_price'] - product['buy_price']:,} ÷ {product['buy_price']:,}) × 100<br>
                Margin % = {correct_answer}%
            </div>
            """
            st.markdown(explanation, unsafe_allow_html=True)
        
        elif challenge_type == "find_profit":
            quantity = challenge["quantity"]
            
            explanation = f"""
            <div class="edu-tip">
                <strong>To calculate the total profit:</strong><br>
                Profit per item = Sell Price - Buy Price<br>
                Profit per item = {product['sell_price']:,} - {product['buy_price']:,} = {product['sell_price'] - product['buy_price']:,}<br>
                Total Profit = Profit per item × Quantity<br>
                Total Profit = {product['sell_price'] - product['buy_price']:,} × {quantity} = {correct_answer:,}
            </div>
            """
            st.markdown(explanation, unsafe_allow_html=True)
        
        elif challenge_type == "find_breakeven":
            fixed_cost = challenge["fixed_cost"]
            margin_per_unit = product["sell_price"] - product["buy_price"]
            
            explanation = f"""
            <div class="edu-tip">
                <strong>To calculate the break-even point:</strong><br>
                Profit per unit = Sell Price - Buy Price<br>
                Profit per unit = {product['sell_price']:,} - {product['buy_price']:,} = {margin_per_unit:,}<br>
                Break-even Units = Fixed Costs ÷ Profit per unit<br>
                Break-even Units = {fixed_cost:,} ÷ {margin_per_unit:,} = {correct_answer} units
            </div>
            """
            st.markdown(explanation, unsafe_allow_html=True)
        
        elif challenge_type == "find_optimal_price":
            elasticity = challenge["elasticity"]
            current_demand = challenge["current_demand"]
            
            if elasticity != 1:
                optimal_markup = 1 / (elasticity - 1)
                
                explanation = f"""
                <div class="edu-tip">
                    <strong>To calculate the optimal price with elasticity {elasticity}:</strong><br>
                    For profit maximization with constant elasticity:<br>
                    Optimal Markup = 1 ÷ (Elasticity - 1)<br>
                    Optimal Markup = 1 ÷ ({elasticity} - 1) = {optimal_markup:.2f}<br>
                    Optimal Price = Buy Price × (1 + Optimal Markup)<br>
                    Optimal Price = {product['buy_price']:,} × (1 + {optimal_markup:.2f}) = {correct_answer:,}
                </div>
                """
            else:
                explanation = f"""
                <div class="edu-tip">
                    <strong>With unit elasticity (elasticity = 1):</strong><br>
                    When elasticity is exactly 1, revenue remains constant regardless of price.<br>
                    The optimal price equals the current price, assuming costs don't change.
                </div>
                """
                
            st.markdown(explanation, unsafe_allow_html=True)
        
        # Add learning insights section
        st.markdown("<h3>Learning Insights</h3>", unsafe_allow_html=True)
        
        # Display level-specific educational content based on challenge type
        pricing_tips = {
            "find_sell_price": {
                "en": "Setting the right price is crucial for profitability. The margin percentage directly impacts how much profit you make on each sale.",
                "id": "Menetapkan harga yang tepat sangat penting untuk profitabilitas. Persentase margin secara langsung memengaruhi seberapa banyak keuntungan yang Anda dapatkan pada setiap penjualan."
            },
            "find_margin_percent": {
                "en": "Calculating margin percentages helps you compare profitability across different products, regardless of their absolute prices.",
                "id": "Menghitung persentase margin membantu Anda membandingkan profitabilitas di berbagai produk, terlepas dari harga absolut mereka."
            },
            "find_profit": {
                "en": "Total profit calculations help you understand how volume affects your business. Higher sales volume can sometimes compensate for lower margins.",
                "id": "Perhitungan total keuntungan membantu Anda memahami bagaimana volume memengaruhi bisnis Anda. Volume penjualan yang lebih tinggi terkadang dapat mengimbangi margin yang lebih rendah."
            },
            "find_breakeven": {
                "en": "Break-even analysis helps you understand how many units you need to sell to cover fixed costs. It's essential for setting sales targets.",
                "id": "Analisis titik impas membantu Anda memahami berapa banyak unit yang perlu Anda jual untuk menutupi biaya tetap. Ini penting untuk menetapkan target penjualan."
            },
            "find_optimal_price": {
                "en": "Elasticity-based pricing maximizes profits by finding the optimal balance between price and demand. It's an advanced concept used by larger businesses.",
                "id": "Penetapan harga berbasis elastisitas memaksimalkan keuntungan dengan menemukan keseimbangan optimal antara harga dan permintaan. Ini adalah konsep lanjutan yang digunakan oleh bisnis yang lebih besar."
            }
        }
        
        if challenge_type in pricing_tips:
            pricing_tip = pricing_tips[challenge_type][lang]
            st.markdown(f"""
            <div style="background-color: #E3F2FD; border-left: 4px solid #2196F3; padding: 15px; margin: 15px 0; border-radius: 4px;">
                <strong>Key Insight:</strong> {pricing_tip}
            </div>
            """, unsafe_allow_html=True)
        
        # Display real-world application example
        real_world_examples = {
            1: {
                "en": "Small retail shops often use simple margin calculations to ensure they make a profit on each item sold.",
                "id": "Toko ritel kecil sering menggunakan perhitungan margin sederhana untuk memastikan mereka mendapatkan keuntungan pada setiap barang yang dijual."
            },
            2: {
                "en": "Grocery stores compare margin percentages across products to identify which items are most profitable.",
                "id": "Toko kelontong membandingkan persentase margin di seluruh produk untuk mengidentifikasi produk mana yang paling menguntungkan."
            },
            3: {
                "en": "Wholesalers focus on total profit calculations since they typically operate with lower margins but higher volumes.",
                "id": "Pedagang grosir fokus pada perhitungan total keuntungan karena mereka biasanya beroperasi dengan margin lebih rendah tetapi volume lebih tinggi."
            },
            4: {
                "en": "New businesses use break-even analysis to determine how long it will take to become profitable.",
                "id": "Bisnis baru menggunakan analisis titik impas untuk menentukan berapa lama waktu yang dibutuhkan untuk menjadi menguntungkan."
            },
            5: {
                "en": "Large retailers use elasticity-based pricing models to optimize their pricing strategy across thousands of products.",
                "id": "Pengecer besar menggunakan model penetapan harga berbasis elastisitas untuk mengoptimalkan strategi penetapan harga mereka di ribuan produk."
            }
        }
        
        real_world_title = "Real-World Application" if lang == "en" else "Aplikasi Dunia Nyata"
        with st.expander(real_world_title):
            if level in real_world_examples:
                st.markdown(f"**{real_world_title}:** {real_world_examples[level][lang]}")
                
            # Add a level-specific case study for higher levels
            if level >= 3:
                case_study_title = "Case Study" if lang == "en" else "Studi Kasus"
                case_study = {
                    3: {
                        "en": """
                        **Mini Market Volume Strategy**
                        
                        A mini market owner noticed that while her snack items had a 40% margin, she only sold about 20 units per day.
                        Meanwhile, her bottled drinks had just a 25% margin, but she sold over 100 units daily.
                        
                        Despite the lower margin, the drinks generated more total profit:
                        - Snacks: 20 units × Rp 2,000 profit per unit = Rp 40,000 daily
                        - Drinks: 100 units × Rp 1,500 profit per unit = Rp 150,000 daily
                        
                        This insight led her to allocate more shelf space to drinks, boosting overall store profitability.
                        """,
                        "id": """
                        **Strategi Volume Mini Market**
                        
                        Seorang pemilik mini market memperhatikan bahwa sementara produk makanan ringannya memiliki margin 40%, dia hanya menjual sekitar 20 unit per hari.
                        Sementara itu, minuman botolnya hanya memiliki margin 25%, tetapi dia menjual lebih dari 100 unit setiap hari.
                        
                        Meskipun marginnya lebih rendah, minuman menghasilkan total keuntungan lebih banyak:
                        - Makanan ringan: 20 unit × Rp 2.000 keuntungan per unit = Rp 40.000 per hari
                        - Minuman: 100 unit × Rp 1.500 keuntungan per unit = Rp 150.000 per hari
                        
                        Wawasan ini membawanya untuk mengalokasikan lebih banyak ruang rak untuk minuman, meningkatkan profitabilitas toko secara keseluruhan.
                        """
                    },
                    4: {
                        "en": """
                        **Warung Break-Even Analysis**
                        
                        A new warung (small food stall) had monthly fixed costs of Rp 3,000,000 (rent, utilities, staff).
                        Their average meal generated Rp 15,000 in profit (after food costs).
                        
                        The owner calculated their break-even point:
                        - Rp 3,000,000 ÷ Rp 15,000 = 200 meals per month
                        
                        This meant they needed to sell at least 7 meals per day to cover fixed costs.
                        This insight helped them set realistic daily sales targets and track their path to profitability.
                        """,
                        "id": """
                        **Analisis Titik Impas Warung**
                        
                        Sebuah warung baru memiliki biaya tetap bulanan sebesar Rp 3.000.000 (sewa, utilitas, staf).
                        Rata-rata makanan mereka menghasilkan Rp 15.000 keuntungan (setelah biaya makanan).
                        
                        Pemilik menghitung titik impas mereka:
                        - Rp 3.000.000 ÷ Rp 15.000 = 200 porsi makanan per bulan
                        
                        Ini berarti mereka perlu menjual setidaknya 7 porsi makanan per hari untuk menutupi biaya tetap.
                        Wawasan ini membantu mereka menetapkan target penjualan harian yang realistis dan melacak jalur menuju profitabilitas.
                        """
                    },
                    5: {
                        "en": """
                        **Elasticity Pricing Strategy**
                        
                        A clothing store found that their basic t-shirts had high elasticity (1.8) while their premium jeans had low elasticity (0.6).
                        
                        For the t-shirts (elastic demand):
                        - When they raised prices by 10%, sales dropped by 18%
                        - They calculated the optimal markup as 1/(1.8-1) = 1.25, setting prices 125% above cost
                        
                        For the jeans (inelastic demand):
                        - When they raised prices by 10%, sales only dropped by 6%
                        - They calculated the optimal markup as 1/(0.6-1) = -2.5, which being negative meant they should maximize markup
                        
                        This data-driven approach allowed them to optimize each product category's pricing independently.
                        """,
                        "id": """
                        **Strategi Penetapan Harga Elastisitas**
                        
                        Sebuah toko pakaian menemukan bahwa kaos polos mereka memiliki elastisitas tinggi (1,8) sementara jeans premium mereka memiliki elastisitas rendah (0,6).
                        
                        Untuk kaos (permintaan elastis):
                        - Ketika mereka menaikkan harga sebesar 10%, penjualan turun sebesar 18%
                        - Mereka menghitung markup optimal sebagai 1/(1,8-1) = 1,25, menetapkan harga 125% di atas biaya
                        
                        Untuk jeans (permintaan inelastis):
                        - Ketika mereka menaikkan harga sebesar 10%, penjualan hanya turun sebesar 6%
                        - Mereka menghitung markup optimal sebagai 1/(0,6-1) = -2,5, yang karena negatif berarti mereka harus memaksimalkan markup
                        
                        Pendekatan berbasis data ini memungkinkan mereka untuk mengoptimalkan penetapan harga setiap kategori produk secara independen.
                        """
                    }
                }
                
                if level in case_study:
                    st.markdown(f"### {case_study_title}")
                    st.markdown(case_study[level][lang])
        
        # Add learning recommendations based on performance
        next_steps_title = "Recommended Next Steps" if lang == "en" else "Langkah Selanjutnya yang Direkomendasikan"
        st.markdown(f"<h4>{next_steps_title}</h4>", unsafe_allow_html=True)
        
        if is_correct:
            if level < 5:
                next_level_text = "Try the next difficulty level" if lang == "en" else "Coba tingkat kesulitan berikutnya"
                st.markdown(f"✅ **{next_level_text}** - You're ready for more advanced pricing challenges!")
            else:
                mastery_text = "You've mastered pricing calculations" if lang == "en" else "Anda telah menguasai perhitungan penetapan harga"
                try_other_games = "Try applying these skills in other mini-games" if lang == "en" else "Coba terapkan keterampilan ini di mini-game lain"
                st.markdown(f"🏆 **{mastery_text}!** {try_other_games}.")
        else:
            practice_text = "Practice this level again" if lang == "en" else "Berlatih level ini lagi"
            review_text = "Review the formulas and concepts" if lang == "en" else "Tinjau rumus dan konsep"
            st.markdown(f"📝 **{practice_text}** - {review_text}.")
        
        # Update player progress
        results = update_skills("margin_calculator", score)
        print("DEBUG: Current skill levels after margin_calculator:", st.session_state.get("skills", {}))
        
        # Continue or try again buttons
        col1, col2 = st.columns(2)
        
        if is_correct and level < 5:
            with col1:
                next_level_button = "Next Level" if lang == "en" else "Level Berikutnya"
                if st.button(next_level_button, key="margin_next_level", type="primary"):
                    # Initialize the next level
                    initialize_margin_challenge(level + 1)
                    st.rerun()
        
        with col1 if (not is_correct or level >= 5) else col2:
            retry_text = "Try Again" if not is_correct else "Practice This Level Again"
            retry_text = retry_text if lang == "en" else "Coba Lagi" if not is_correct else "Berlatih Level Ini Lagi"
            if st.button(retry_text, key="margin_retry"):
                # Reinitialize the same level
                initialize_margin_challenge(level)
                st.rerun()
        
        with col2 if (not is_correct or level >= 5) else col1:
            main_menu_text = "Return to Main Menu" if lang == "en" else "Kembali ke Menu Utama"
            if st.button(main_menu_text, key="margin_main_menu"):
                # Clean up game state
                if "margin_calculator" in st.session_state:
                    del st.session_state.margin_calculator
                
                st.session_state.current_game = None
                st.rerun()

# Helper function to provide game information
def get_game_info():
    """Get information about the margin calculator game.
    
    Returns:
        dict: Game information
    """
    return {
        "id": "margin_calculator",
        "name": {
            "en": "Margin Calculator",
            "id": "Kalkulator Margin"
        },
        "title": "Margin Calculator Challenge",
        "description": {
            "en": "Set prices and calculate profits",
            "id": "Tetapkan harga dan hitung keuntungan"
        },
        "primary_skill": "pricing_strategy",
        "secondary_skill": "bookkeeping",
        "levels": 5,
        "level_descriptions": {
            1: {
                "en": "Simple selling price calculation",
                "id": "Perhitungan harga jual sederhana"
            },
            2: {
                "en": "Margin percentage calculation",
                "id": "Perhitungan persentase margin"
            },
            3: {
                "en": "Profit calculation with quantity",
                "id": "Perhitungan keuntungan dengan kuantitas"
            },
            4: {
                "en": "Break-even point analysis",
                "id": "Analisis titik impas"
            },
            5: {
                "en": "Advanced pricing strategy with elasticity",
                "id": "Strategi penetapan harga lanjutan dengan elastisitas"
            }
        },
        "time_limit": {
            1: None,
            2: None,
            3: 60,
            4: 60,
            5: 60
        },
        "max_score": {
            1: 20,   # Base: 10 + Level bonus: 2 + Perfect bonus: 5 + Time bonus: 3 (no time limit)
            2: 30,   # Base: 15 + Level bonus: 4 + Perfect bonus: 10 + Time bonus: 1 (no time limit)
            3: 60,   # Base: 20 + Level bonus: 6 + Perfect bonus: 15 + Time bonus: 19
            4: 75,   # Base: 25 + Level bonus: 8 + Perfect bonus: 20 + Time bonus: 22
            5: 90    # Base: 30 + Level bonus: 10 + Perfect bonus: 25 + Time bonus: 25
        },
        "educational_objectives": {
            1: {
                "en": "Basic price setting using margins",
                "id": "Penetapan harga dasar menggunakan margin"
            },
            2: {
                "en": "Understanding profit percentage calculation",
                "id": "Memahami perhitungan persentase keuntungan"
            },
            3: {
                "en": "Evaluating total profit for multiple items",
                "id": "Mengevaluasi total keuntungan untuk beberapa item"
            },
            4: {
                "en": "Calculating sales required to cover fixed costs",
                "id": "Menghitung penjualan yang diperlukan untuk menutupi biaya tetap"
            },
            5: {
                "en": "Advanced pricing strategies using demand elasticity",
                "id": "Strategi penetapan harga lanjutan menggunakan elastisitas permintaan"
            }
        },
        "challenge_types": {
            1: "find_sell_price",
            2: "find_margin_percent",
            3: "find_profit",
            4: "find_breakeven",
            5: "find_optimal_price"
        }
    }