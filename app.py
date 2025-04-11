# app.py - Main Streamlit application for Toko Pintar
import streamlit as st
import random
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Toko Pintar - Financial Literacy Game",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
    }
    .game-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #1E88E5;
    }
    .score-text {
        font-size: 1.5rem;
        font-weight: bold;
        color: #4CAF50;
    }
    .achievement-card {
        background-color: #FFF9C4;
        border-radius: 5px;
        padding: 10px;
        margin: 5px 0;
        border-left: 5px solid #FFC107;
    }
    .game-title {
        font-weight: bold;
        color: #1E88E5;
    }
    .shop-level {
        font-size: 1.2rem;
        color: #7E57C2;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Sample product data
SAMPLE_PRODUCTS = [
    {"name": "Indomie", "buy_price": 2500, "sell_price": 3500, "stock": 24, "category": "Food"},
    {"name": "Teh Botol", "buy_price": 3000, "sell_price": 4000, "stock": 15, "category": "Beverage"},
    {"name": "Sabun Mandi", "buy_price": 3500, "sell_price": 5000, "stock": 10, "category": "Hygiene"},
    {"name": "Gula 1kg", "buy_price": 15000, "sell_price": 18000, "stock": 5, "category": "Grocery"},
    {"name": "Minyak Goreng 1L", "buy_price": 20000, "sell_price": 23000, "stock": 3, "category": "Grocery"},
    {"name": "Kopi Sachet", "buy_price": 1500, "sell_price": 2000, "stock": 30, "category": "Beverage"},
    {"name": "Beras 1kg", "buy_price": 12000, "sell_price": 13500, "stock": 8, "category": "Grocery"},
    {"name": "Telur (per butir)", "buy_price": 2000, "sell_price": 2500, "stock": 20, "category": "Food"},
    {"name": "Pasta Gigi", "buy_price": 10000, "sell_price": 12000, "stock": 6, "category": "Hygiene"},
    {"name": "Air Mineral", "buy_price": 2000, "sell_price": 3000, "stock": 24, "category": "Beverage"}
]

# Initialize session state variables
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.player_name = ""
    st.session_state.total_score = 0
    st.session_state.current_game = None
    st.session_state.game_history = []
    st.session_state.skill_levels = {
        "inventory_management": 0,
        "cash_handling": 0,
        "pricing_strategy": 0,
        "customer_relations": 0,
        "bookkeeping": 0
    }
    st.session_state.achievements = []
    st.session_state.shop_level = 1

# Helper functions
def update_skills(game_id, score):
    """Update player skills based on the game played and score earned"""
    # Map games to skills
    skill_mapping = {
        "inventory_game": "inventory_management",
        "change_making": "cash_handling",
        "margin_calculator": "pricing_strategy",
        "customer_service": "customer_relations",
        "simple_accounting": "bookkeeping",
        "cash_reconciliation": "cash_handling"
    }
    
    # Update relevant skill
    if game_id in skill_mapping:
        skill_name = skill_mapping[game_id]
        # Increase skill by 0.2 if they scored points, max level is 5
        if score > 0:
            st.session_state.skill_levels[skill_name] = min(5, st.session_state.skill_levels[skill_name] + 0.2)
    
    # Update total score
    st.session_state.total_score += score
    
    # Record game in history
    st.session_state.game_history.append({
        "game_id": game_id,
        "score": score,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # Update shop level (average of all skills, rounded down)
    skill_values = list(st.session_state.skill_levels.values())
    avg_skill = sum(skill_values) / len(skill_values)
    st.session_state.shop_level = max(1, int(avg_skill) + 1)  # Shop levels start at 1
    
    # Check for achievements
    check_achievements()

def check_achievements():
    """Check for and award any earned achievements"""
    # Example achievements
    possible_achievements = [
        {
            "id": "first_game",
            "name": "First Steps",
            "description": "Play your first mini-game",
            "check": lambda: len(st.session_state.game_history) >= 1
        },
        {
            "id": "inventory_master",
            "name": "Inventory Master",
            "description": "Reach level 3 in inventory management",
            "check": lambda: st.session_state.skill_levels["inventory_management"] >= 3
        },
        {
            "id": "math_whiz",
            "name": "Math Whiz", 
            "description": "Score perfectly in 3 math-related games in a row",
            "check": lambda: check_math_whiz()
        },
        {
            "id": "shop_upgrade",
            "name": "Shop Upgrade",
            "description": "Reach shop level 2",
            "check": lambda: st.session_state.shop_level >= 2
        },
        {
            "id": "financial_guru",
            "name": "Financial Guru",
            "description": "Score over 30 points in margin calculator game",
            "check": lambda: any(g["game_id"] == "margin_calculator" and g["score"] >= 30 for g in st.session_state.game_history)
        }
    ]
    
    # Check each achievement
    for achievement in possible_achievements:
        # Skip already earned achievements
        if any(a["id"] == achievement["id"] for a in st.session_state.achievements):
            continue
        
        # Check if achievement should be earned
        if achievement["check"]():
            st.session_state.achievements.append({
                "id": achievement["id"],
                "name": achievement["name"],
                "description": achievement["description"],
                "earned_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

def check_math_whiz():
    """Helper function to check the Math Whiz achievement"""
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

# Game implementations
def inventory_game():
    """Inventory counting mini-game"""
    st.markdown('<p class="game-title">Inventory Counting Game</p>', unsafe_allow_html=True)
    st.write("Count your products accurately to maintain proper stock records.")
    
    # Initialize game state if needed
    if "inventory_items" not in st.session_state:
        # Select 3 random products
        st.session_state.inventory_items = random.sample(SAMPLE_PRODUCTS, 3)
        # Set actual counts (with slight randomization from recorded stock)
        for item in st.session_state.inventory_items:
            variation = random.randint(-2, 2)
            item["actual_count"] = max(0, item["stock"] + variation)
            item["user_count"] = 0
    
    # Display instructions
    st.info("Your task is to count the actual stock and enter the correct numbers below.")
    
    # Display each product with input field
    for i, item in enumerate(st.session_state.inventory_items):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{item['name']}** (Recorded stock: {item['stock']})")
        with col2:
            st.session_state.inventory_items[i]["user_count"] = st.number_input(
                f"Actual count", 
                min_value=0,
                max_value=100,
                value=st.session_state.inventory_items[i]["user_count"],
                key=f"inventory_{i}"
            )
    
    # Submit button
    if st.button("Submit Inventory Count"):
        score = 0
        results = []
        
        # Check each count
        for item in st.session_state.inventory_items:
            is_correct = item["user_count"] == item["actual_count"]
            if is_correct:
                score += 10
                results.append(f"✅ **{item['name']}**: Correct! You counted {item['user_count']}")
            else:
                results.append(f"❌ **{item['name']}**: You counted {item['user_count']}, actual count was {item['actual_count']}")
        
        # Display results
        st.markdown("### Results:")
        for result in results:
            st.markdown(result)
        
        st.markdown(f"**Score:** {score} points")
        
        # Show achievement if perfect score
        if score == 30:
            st.balloons()
            st.success("Perfect score! Your inventory management skills are excellent!")
        
        # Update player progress
        update_skills("inventory_game", score)
        
        # Reset game state
        del st.session_state.inventory_items
        
        # Add a slight delay before returning to main menu
        time.sleep(2)
        st.session_state.current_game = None
        st.experimental_rerun()

def change_making_game():
    """Change making mini-game"""
    st.markdown('<p class="game-title">Change Making Challenge</p>', unsafe_allow_html=True)
    st.write("Calculate change quickly and accurately.")
    
    # Initialize game state if needed
    if "transaction" not in st.session_state:
        # Generate a random purchase
        items_bought = random.sample(SAMPLE_PRODUCTS, random.randint(1, 3))
        total_price = sum(item["sell_price"] for item in items_bought)
        
        # Indonesian Rupiah denominations
        denominations = [100000, 50000, 20000, 10000, 5000, 2000, 1000, 500, 200, 100]
        
        # Generate payment amount (ensure it's larger than total price)
        payment_idx = min(3, len(denominations) - 1)  # Use larger denominations
        payment_amount = denominations[random.randint(0, payment_idx)]
        
        while payment_amount <= total_price:
            payment_amount += denominations[random.randint(0, payment_idx)]
        
        # Store transaction details
        st.session_state.transaction = {
            "items": items_bought,
            "total_price": total_price,
            "payment": payment_amount,
            "correct_change": payment_amount - total_price,
            "user_change": 0
        }
    
    # Display transaction
    st.markdown("### Customer Purchase:")
    
    # Create a table to show purchased items
    items_data = []
    for item in st.session_state.transaction["items"]:
        items_data.append({
            "Product": item["name"],
            "Price": f"Rp {item['sell_price']:,}"
        })
    
    items_df = pd.DataFrame(items_data)
    st.table(items_df)
    
    # Show total and payment
    st.markdown(f"**Total Price:** Rp {st.session_state.transaction['total_price']:,}")
    st.markdown(f"**Customer Payment:** Rp {st.session_state.transaction['payment']:,}")
    
    # Input for change calculation
    st.session_state.transaction["user_change"] = st.number_input(
        "How much change should you give back to the customer?",
        min_value=0,
        max_value=1000000,
        value=st.session_state.transaction["user_change"],
        step=100
    )
    
    # Submit button
    if st.button("Check My Answer"):
        correct_change = st.session_state.transaction["correct_change"]
        user_change = st.session_state.transaction["user_change"]
        
        if user_change == correct_change:
            st.success(f"Correct! The change is Rp {correct_change:,}")
            score = 10
            if "time_bonus" in st.session_state.transaction:
                score += st.session_state.transaction["time_bonus"]
                st.write(f"Time bonus: +{st.session_state.transaction['time_bonus']} points")
        else:
            st.error(f"That's not right. The correct change is Rp {correct_change:,}")
            score = 0
        
        # Update player progress
        update_skills("change_making", score)
        
        # Reset game state
        del st.session_state.transaction
        
        # Add a slight delay before returning to main menu
        time.sleep(2)
        st.session_state.current_game = None
        st.experimental_rerun()

def margin_calculator_game():
    """Margin calculation mini-game"""
    st.markdown('<p class="game-title">Margin Calculator Challenge</p>', unsafe_allow_html=True)
    st.write("Calculate prices, margins, and profits to boost your business.")
    
    # Initialize game state if needed
    if "margin_challenge" not in st.session_state:
        # Select a random product
        product = random.choice(SAMPLE_PRODUCTS)
        
        # Choose one of three challenge types
        challenge_type = random.choice(["find_sell_price", "find_margin_percent", "find_profit"])
        
        st.session_state.margin_challenge = {
            "product": product,
            "type": challenge_type,
            "user_answer": 0
        }
        
        # Set up specific challenge parameters
        if challenge_type == "find_sell_price":
            # Choose a target margin
            target_margin = random.randint(15, 45)
            correct_sell_price = round(product["buy_price"] * (1 + target_margin/100), -2)  # Round to nearest 100
            
            st.session_state.margin_challenge["target_margin"] = target_margin
            st.session_state.margin_challenge["correct_answer"] = correct_sell_price
            
        elif challenge_type == "find_margin_percent":
            # Calculate the correct margin
            correct_margin = round(((product["sell_price"] - product["buy_price"]) / product["buy_price"]) * 100)
            
            st.session_state.margin_challenge["correct_answer"] = correct_margin
            
        else:  # find_profit
            # Choose random quantity sold
            quantity = random.randint(5, 15)
            correct_profit = (product["sell_price"] - product["buy_price"]) * quantity
            
            st.session_state.margin_challenge["quantity"] = quantity
            st.session_state.margin_challenge["correct_answer"] = correct_profit
    
    # Display the challenge
    product = st.session_state.margin_challenge["product"]
    challenge_type = st.session_state.margin_challenge["type"]
    
    st.markdown(f"### Product: {product['name']}")
    
    if challenge_type == "find_sell_price":
        target_margin = st.session_state.margin_challenge["target_margin"]
        
        st.write(f"**Buy price:** Rp {product['buy_price']:,}")
        st.write(f"**Target margin:** {target_margin}%")
        
        st.warning("You need to set a selling price that achieves the target margin. Round to the nearest 100 Rupiah.")
        
        # Input for sell price
        answer = st.number_input(
            "What selling price will give you this margin?",
            min_value=0,
            max_value=1000000,
            value=st.session_state.margin_challenge["user_answer"],
            step=100
        )
        st.session_state.margin_challenge["user_answer"] = answer
        
    elif challenge_type == "find_margin_percent":
        st.write(f"**Buy price:** Rp {product['buy_price']:,}")
        st.write(f"**Sell price:** Rp {product['sell_price']:,}")
        
        st.warning("Calculate the margin percentage. Round to the nearest whole number.")
        
        # Input for margin percentage
        answer = st.number_input(
            "What is the margin percentage?",
            min_value=0,
            max_value=100,
            value=st.session_state.margin_challenge["user_answer"],
            step=1
        )
        st.session_state.margin_challenge["user_answer"] = answer
        
    else:  # find_profit
        quantity = st.session_state.margin_challenge["quantity"]
        
        st.write(f"**Buy price:** Rp {product['buy_price']:,}")
        st.write(f"**Sell price:** Rp {product['sell_price']:,}")
        st.write(f"**Quantity sold:** {quantity}")
        
        st.warning("Calculate the total profit from this sale.")
        
        # Input for profit
        answer = st.number_input(
            "What is the total profit?",
            min_value=0,
            max_value=1000000,
            value=st.session_state.margin_challenge["user_answer"],
            step=1000
        )
        st.session_state.margin_challenge["user_answer"] = answer
    
    # Submit button
    if st.button("Check My Answer"):
        correct_answer = st.session_state.margin_challenge["correct_answer"]
        user_answer = st.session_state.margin_challenge["user_answer"]
        
        # Allow for some margin of error
        tolerance = 0
        if challenge_type == "find_sell_price":
            tolerance = 100  # 100 Rp difference allowed
        elif challenge_type == "find_margin_percent":
            tolerance = 1    # 1% difference allowed
        elif challenge_type == "find_profit":
            tolerance = 1000  # 1000 Rp difference allowed
        
        if abs(user_answer - correct_answer) <= tolerance:
            st.success(f"Correct! The answer is {correct_answer:,}")
            score = 15
        else:
            st.error(f"Incorrect. The correct answer is {correct_answer:,}")
            score = 0
        
        # Provide educational explanation
        if challenge_type == "find_sell_price":
            st.info(f"To calculate the selling price with a {st.session_state.margin_challenge['target_margin']}% margin:\n"
                   f"Selling Price = Buy Price × (1 + Margin %)\n"
                   f"Selling Price = {product['buy_price']:,} × (1 + {st.session_state.margin_challenge['target_margin']}/100)\n"
                   f"Selling Price = {product['buy_price']:,} × {1 + st.session_state.margin_challenge['target_margin']/100}\n"
                   f"Selling Price = {correct_answer:,} (rounded to nearest 100)")
        
        elif challenge_type == "find_margin_percent":
            st.info(f"To calculate the margin percentage:\n"
                   f"Margin % = ((Sell Price - Buy Price) ÷ Buy Price) × 100\n"
                   f"Margin % = (({product['sell_price']:,} - {product['buy_price']:,}) ÷ {product['buy_price']:,}) × 100\n"
                   f"Margin % = ({product['sell_price'] - product['buy_price']:,} ÷ {product['buy_price']:,}) × 100\n"
                   f"Margin % = {correct_answer}%")
        
        else:  # find_profit
            quantity = st.session_state.margin_challenge["quantity"]
            st.info(f"To calculate the total profit:\n"
                   f"Profit per item = Sell Price - Buy Price\n"
                   f"Profit per item = {product['sell_price']:,} - {product['buy_price']:,} = {product['sell_price'] - product['buy_price']:,}\n"
                   f"Total Profit = Profit per item × Quantity\n"
                   f"Total Profit = {product['sell_price'] - product['buy_price']:,} × {quantity} = {correct_answer:,}")
        
        # Update player progress
        update_skills("margin_calculator", score)
        
        # Reset game state after delay
        time.sleep(5)  # Give time to read the explanation
        del st.session_state.margin_challenge
        
        # Return to main menu
        st.session_state.current_game = None
        st.experimental_rerun()

# Main menu display
def show_main_menu():
    st.markdown('<h1 class="main-header">Toko Pintar</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem;">Financial Literacy Game for Small Retailers</p>', unsafe_allow_html=True)
    
    # First-time setup
    if not st.session_state.player_name:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### Welcome to Toko Pintar!")
            st.write("Learn financial and operational skills while running your own small shop.")
            st.session_state.player_name = st.text_input("What's your name?")
            
            if st.button("Start Game") and st.session_state.player_name:
                st.success(f"Welcome, {st.session_state.player_name}! Let's get started.")
                st.experimental_rerun()
    else:
        # Player dashboard
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### Welcome to your shop, {st.session_state.player_name}!")
            
            # Shop level visualization
            st.markdown(f'<p class="shop-level">Shop Level: {st.session_state.shop_level}</p>', unsafe_allow_html=True)
            
            # Show visual representation of shop based on level
            if st.session_state.shop_level == 1:
                st.image("https://via.placeholder.com/600x200.png?text=Small+Shop+Level+1", caption="Your small warung is just starting out.")
            elif st.session_state.shop_level == 2:
                st.image("https://via.placeholder.com/600x200.png?text=Improved+Shop+Level+2", caption="Your shop has some basic improvements.")
            else:
                st.image("https://via.placeholder.com/600x200.png?text=Advanced+Shop+Level+3+", caption="Your shop is growing nicely!")
            
            # Display available mini-games
            st.markdown("### Mini-Games")
            st.write("Choose a game to practice your retail skills:")
            
            # Create game cards with 3 columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown('<div class="game-card">', unsafe_allow_html=True)
                st.markdown("**Inventory Counting**")
                st.write("Keep track of your stock accurately")
                st.progress(min(1.0, st.session_state.skill_levels["inventory_management"] / 5))
                if st.button("Play Inventory Game"):
                    st.session_state.current_game = "inventory_game"
                    st.experimental_rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="game-card">', unsafe_allow_html=True)
                st.markdown("**Change Making**")
                st.write("Calculate change quickly and accurately")
                st.progress(min(1.0, st.session_state.skill_levels["cash_handling"] / 5))
                if st.button("Play Change Making"):
                    st.session_state.current_game = "change_making"
                    st.experimental_rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="game-card">', unsafe_allow_html=True)
                st.markdown("**Margin Calculator**")
                st.write("Set prices and calculate profits")
                st.progress(min(1.0, st.session_state.skill_levels["pricing_strategy"] / 5))
                if st.button("Play Margin Calculator"):
                    st.session_state.current_game = "margin_calculator"
                    st.experimental_rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Player stats
            st.markdown('<p class="score-text">Score: {:,}</p>'.format(st.session_state.total_score), unsafe_allow_html=True)
            
            # Skill levels
            st.markdown("### Your Skills")
            for skill, level in st.session_state.skill_levels.items():
                # Format skill name for display
                display_name = " ".join(word.capitalize() for word in skill.split("_"))
                st.write(f"{display_name}:")
                st.progress(min(1.0, level / 5))
            
            # Achievements
            if st.session_state.achievements:
                st.markdown("### Achievements")
                for achievement in st.session_state.achievements:
                    st.markdown(f"""
                    <div class="achievement-card">
                        <strong>{achievement["name"]}</strong><br>
                        {achievement["description"]}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Recent activity
            if st.session_state.game_history:
                st.markdown("### Recent Activity")
                
                # Convert to DataFrame for easy display
                history_df = pd.DataFrame(st.session_state.game_history[-5:])  # Last 5 games
                
                # Format game names
                game_name_map = {
                    "inventory_game": "Inventory Counting",
                    "change_making": "Change Making",
                    "margin_calculator": "Margin Calculator"
                }
                
                # Clean up the display
                display_df = pd.DataFrame({
                    "Game": [game_name_map.get(g, g) for g in history_df["game_id"]],
                    "Score": history_df["score"],
                    "Date": [ts.split()[0] for ts in history_df["timestamp"]]
                })
                
                st.table(display_df)

# Main app flow
def main():
    # App routing based on current state
    if st.session_state.current_game == "inventory_game":
        inventory_game()
    elif st.session_state.current_game == "change_making":
        change_making_game()
    elif st.session_state.current_game == "margin_calculator":
        margin_calculator_game()
    else:
        show_main_menu()

if __name__ == "__main__":
    main()
