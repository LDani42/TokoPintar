"""
Change Making mini-game for Toko Pintar application.
"""
import streamlit as st
import random
import time
import pandas as pd
from utils.config import get_config, get_product_emoji
from utils.skills import update_skills
from components.scoreboard import display_educational_tip
from utils.db import db
from utils.tooltips import show_mechanics_tooltip_button, add_tooltips_to_page
from utils.game_levels import display_level_selection, display_level_header, display_timer, display_score_breakdown
from utils.game_ui import display_product_card, display_result_container, display_accuracy_gauge
from utils.educational_content import display_learning_insight, display_formula_explanation
from games.breadcrumb import show_game_breadcrumb

def get_level_description(level):
    """Get description text for each level.
    
    Args:
        level (int): Game difficulty level
        
    Returns:
        dict: Descriptions in English and Indonesian
    """
    descriptions = {
        1: {
            "en": "Simple change calculations with round numbers. Great for beginners!",
            "id": "Perhitungan kembalian sederhana dengan angka bulat. Cocok untuk pemula!"
        },
        2: {
            "en": "More complex calculations with odd amounts. Pay attention to smaller denominations.",
            "id": "Perhitungan lebih kompleks dengan jumlah ganjil. Perhatikan denominasi yang lebih kecil."
        },
        3: {
            "en": "Multiple items with varied prices. Calculate change with precision.",
            "id": "Beberapa barang dengan harga bervariasi. Hitung kembalian dengan tepat."
        },
        4: {
            "en": "Time pressure and optimal denomination selection. Speed and efficiency matter!",
            "id": "Tekanan waktu dan pemilihan denominasi optimal. Kecepatan dan efisiensi penting!"
        },
        5: {
            "en": "Find the optimal change combination with fewest bills/coins under tight time pressure.",
            "id": "Temukan kombinasi kembalian optimal dengan uang kertas/koin paling sedikit dengan tekanan waktu ketat."
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
            "en": "Start with the formula: Change = Payment - Total Price. With round numbers, this is easy!",
            "id": "Mulai dengan rumus: Kembalian = Pembayaran - Total Harga. Dengan angka bulat, ini mudah!"
        },
        2: {
            "en": "Break down the calculation: first calculate the main difference, then handle smaller denominations.",
            "id": "Uraikan perhitungan: pertama hitung perbedaan utama, lalu tangani denominasi yang lebih kecil."
        },
        3: {
            "en": "Add all prices first, then subtract from the payment. Check your math carefully!",
            "id": "Tambahkan semua harga terlebih dahulu, lalu kurangi dari pembayaran. Periksa perhitungan Anda dengan hati-hati!"
        },
        4: {
            "en": "Try to use the fewest bills and coins possible. Larger denominations first, then smaller ones.",
            "id": "Cobalah untuk menggunakan uang kertas dan koin sesedikit mungkin. Denominasi lebih besar dahulu, lalu yang lebih kecil."
        },
        5: {
            "en": "Speed is critical! Practice mental math shortcuts and quick denomination selection.",
            "id": "Kecepatan sangat penting! Latih jalan pintas matematika mental dan pemilihan denominasi yang cepat."
        }
    }
    
    return tips.get(level, tips[1])

def initialize_transaction(level=1):
    """Initialize a transaction for the game based on level.
    
    Args:
        level (int): Game difficulty level
    """
    # Get products from database
    all_products = db.get_products()
    if not all_products:
        # Fall back to sample products if database is empty
        from utils.config import SAMPLE_PRODUCTS
        all_products = SAMPLE_PRODUCTS
    
    # Determine number of items based on level
    if level == 1:
        num_items = 1  # Single item for beginners
    elif level == 2:
        num_items = 2  # Two items for level 2
    elif level == 3:
        num_items = 3  # Three items for level 3
    else:
        num_items = random.randint(3, 5)  # Multiple items for advanced levels
    
    # Generate a random purchase
    items_bought = random.sample(all_products, min(num_items, len(all_products)))
    
    # Calculate total price based on level
    if level == 1:
        # Level 1: Use actual price, do not round
        total_price = sum(item["sell_price"] for item in items_bought)
    elif level == 2:
        # Level 2: Round to nearest 500 for slightly more complex calculation
        total_price = round(sum(item["sell_price"] for item in items_bought) / 500) * 500
    else:
        # Higher levels: Use exact prices
        total_price = sum(item["sell_price"] for item in items_bought)
    
    # Indonesian Rupiah denominations
    denominations = [100000, 50000, 20000, 10000, 5000, 2000, 1000, 500, 200, 100]
    
    # Generate payment amount (ensure it's larger than total price)
    payment_amount = 0
    
    if level == 1:
        # Level 1: Payment is a single large bill for easier calculation
        for denom in denominations:
            if denom > total_price and denom <= 50000:  # Limit to 50k for beginners
                payment_amount = denom
                break
        
        # If no suitable denomination found, use 50000
        if payment_amount == 0:
            payment_amount = 50000
    
    elif level == 2:
        # Level 2: Payment is 1-2 notes with simpler change calculation
        # Use top 4 denominations for level 2
        payment_options = denominations[:4]  
        payment_amount = payment_options[random.randint(0, len(payment_options) - 1)]
        
        while payment_amount <= total_price:
            payment_amount += payment_options[random.randint(0, len(payment_options) - 1)]
    
    elif level == 3:
        # Level 3: More complex payment with multiple denominations
        num_notes = random.randint(1, 2)
        for _ in range(num_notes):
            payment_amount += denominations[random.randint(0, 6)]  # Use first 7 denominations
        
        while payment_amount <= total_price:
            payment_amount += denominations[random.randint(0, 6)]
    
    elif level == 4:
        # Level 4: Complex payment with time pressure
        num_notes = random.randint(2, 3)
        for _ in range(num_notes):
            payment_amount += denominations[random.randint(0, 7)]  # Use first 8 denominations
        
        while payment_amount <= total_price:
            payment_amount += denominations[random.randint(0, 7)]
    
    else:
        # Level 5: Maximum complexity
        num_notes = random.randint(2, 4)
        for _ in range(num_notes):
            payment_amount += denominations[random.randint(0, 9)]  # Use all denominations
        
        while payment_amount <= total_price:
            payment_amount += denominations[random.randint(0, 9)]
    
    # Set time limit based on level
    time_limits = {
        1: None,          # Level 1: No time limit for beginners
        2: None,          # Level 2: No time limit for learning
        3: None,          # Level 3: No time limit but more complex
        4: 45,            # Level 4: Moderate time limit
        5: 30             # Level 5: Tight time limit
    }
    
    # Store transaction details
    st.session_state.change_making = {
        "level": level,
        "items": items_bought,
        "total_price": total_price,
        "payment": payment_amount,
        "correct_change": payment_amount - total_price,
        "user_change": 0,
        "start_time": time.time(),
        "time_limit": time_limits.get(level),
        "level_description": get_level_description(level),
        "level_tips": get_level_tips(level)
    }

def change_making_game():
    """Change making mini-game implementation (UI Overhaul)."""
    lang = get_config("app.default_language") or "en"
    
    # --- HEADER ---
    st.markdown(f"""
        <div style='text-align:center;margin-bottom:10px;'>
            <span style='font-size:2.2rem;font-weight:bold;color:#2E7D32;'>
                {'💵 ' if lang=='en' else '💴 '}{'Change Making Challenge' if lang=='en' else 'Tantangan Memberi Kembalian'}
            </span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center;color:#444;margin-bottom:20px;'>{'Calculate change quickly and accurately.' if lang=='en' else 'Hitung kembalian dengan cepat dan akurat.'}</div>", unsafe_allow_html=True)
    
    display_educational_tip("cash")
    col1, col2 = st.columns([3, 1])
    with col2:
        show_mechanics_tooltip_button("cash_handling", game_id="change_making")
    add_tooltips_to_page()
    
    # --- GAME STATE ---
    game = st.session_state.change_making
    level = game["level"]
    items = game["items"]
    total_price = game["total_price"]
    payment = game["payment"]
    
    # --- TIMER ---
    if game.get("time_limit"):
        remaining_time = display_timer(game["start_time"], game["time_limit"])
        if remaining_time <= 0 and not game.get("submitted"):
            st.warning(("Time's up!" if lang=="en" else "Waktu habis!") + " Your answer has been submitted.")
            game["submitted"] = True
            st.rerun()
    
    # --- LEVEL HEADER ---
    display_level_header(level, game["level_description"], game["level_tips"])
    
    # --- MAIN LAYOUT ---
    st.markdown("""
        <div style='max-width:600px;margin:0 auto;'>
    """, unsafe_allow_html=True)
    # Product purchase section
    st.markdown("""
        <div style='background:#f5f5f5;padding:18px 18px 10px 18px;border-radius:10px;box-shadow:0 2px 8px #eee;margin-bottom:18px;'>
            <span style='font-size:1.2rem;font-weight:bold;'>🛒 {}</span>
    """.format("Customer Purchase" if lang=="en" else "Pembelian Pelanggan"), unsafe_allow_html=True)
    for item in items:
        name = item["name_id"] if lang == "id" and "name_id" in item else item["name"]
        price = item["sell_price"]
        emoji = get_product_emoji(item)
        st.markdown(f"<div style='display:flex;justify-content:space-between;margin:8px 0;'><span style='font-size:1.1rem;'>{emoji} <b>{name}</b></span><span class='cash-amount'>Rp {price:,}</span></div>", unsafe_allow_html=True)
    st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)
    st.markdown(f"<div style='display:flex;justify-content:space-between;font-weight:bold;font-size:1.1rem;'><span>Total</span><span class='cash-amount'>Rp {total_price:,}</span></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    # Payment section
    st.markdown("""
        <div style='background:#e8f5e9;padding:15px 15px 8px 15px;border-radius:10px;box-shadow:0 2px 8px #eee;margin-bottom:18px;'>
            <span style='font-size:1.1rem;font-weight:bold;'>💰 {}</span>
    """.format("Customer Pays With" if lang=="en" else "Pelanggan Membayar Dengan"), unsafe_allow_html=True)
    denominations = [100000, 50000, 20000, 10000, 5000, 2000, 1000, 500, 200, 100]
    payment_left = payment
    for denom in denominations:
        count = payment_left // denom
        if count > 0:
            st.markdown(f"<div style='display:inline-block;background:#5DADE2;color:white;width:68px;height:38px;margin:3px 3px 8px 0;text-align:center;border-radius:5px;line-height:38px;font-weight:bold;'>Rp {denom:,}</div>", unsafe_allow_html=True)
            payment_left %= denom
    st.markdown(f"<div style='margin-top:6px;font-weight:bold;'>Total Payment: <span class='cash-amount'>Rp {payment:,}</span></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # --- CHANGE INPUT AREA ---
    change_label = "How much change should you give back to the customer?" if lang=="en" else "Berapa kembalian yang harus Anda berikan kepada pelanggan?"
    correct_change = game["correct_change"]
    
    if level >= 4 and not game.get("submitted"):
        # Denomination selection UI
        if "selected_denominations" not in game:
            game["selected_denominations"] = {denom: 0 for denom in denominations}
        st.markdown("<div style='margin-bottom:10px;'><b>Select bills/coins to give as change:</b></div>", unsafe_allow_html=True)
        denom_cols = st.columns(len(denominations))
        for i, denom in enumerate(denominations):
            with denom_cols[i]:
                st.markdown(f"<div style='background:#BB8FCE;color:white;width:50px;height:30px;margin:0 auto 5px auto;text-align:center;border-radius:5px;line-height:30px;font-weight:bold;'>Rp {denom:,}</div>", unsafe_allow_html=True)
                minus, count_disp, plus = st.columns([1,1,1])
                with minus:
                    if st.button("-", key=f"minus_{denom}", disabled=game["selected_denominations"][denom] <= 0):
                        game["selected_denominations"][denom] = max(0, game["selected_denominations"][denom] - 1)
                with count_disp:
                    st.markdown(f"<div style='text-align:center;font-weight:bold;'>{game['selected_denominations'][denom]}</div>", unsafe_allow_html=True)
                with plus:
                    if st.button("+", key=f"plus_{denom}"):
                        game["selected_denominations"][denom] += 1
        selected_total = sum(denom * count for denom, count in game["selected_denominations"].items())
        game["user_change"] = selected_total
        st.markdown(f"<div style='margin-top:10px;font-weight:bold;'>Your selected change: <span class='cash-amount'>Rp {selected_total:,}</span></div>", unsafe_allow_html=True)
        if any(count > 0 for count in game["selected_denominations"].values()):
            selected_notes = [f"{count} x Rp {denom:,}" for denom, count in game["selected_denominations"].items() if count > 0]
            st.markdown(f"<div style='margin-bottom:8px;'>You're giving: {', '.join(selected_notes)}</div>", unsafe_allow_html=True)
    elif level < 4 and not game.get("submitted"):
        st.markdown(f"<h3 style='margin-bottom:12px;'>{change_label}</h3>", unsafe_allow_html=True)
        # Only allow answer selection from provided options, not free number input
        options = [correct_change, correct_change + 1000, max(100, correct_change - 1000)]
        options = sorted(set(options))
        btn_cols = st.columns(len(options))
        for i, amount in enumerate(options):
            with btn_cols[i]:
                if st.button(f"Rp {amount:,}", key=f"amount_{amount}"):
                    game["user_change"] = amount
                    st.session_state["change_option_selected"] = True
                    st.rerun()
        # Display the user's current selection if any
        if game.get("user_change", 0) > 0:
            st.markdown(f"<div style='background:white;padding:12px 0 8px 0;border-radius:7px;border:1px solid #b3c7e6;margin:10px 0 0 0;text-align:right;'><span style='font-size:1.4rem;font-family:monospace;color:#2E7D32;'>Rp {game['user_change']:,}</span></div>", unsafe_allow_html=True)
    
    # --- SUBMIT BUTTON ---
    check_text = "Check My Answer" if lang == "en" else "Periksa Jawaban Saya"
    if st.button(check_text) or game.get("submitted"):
        game["submitted"] = True
        user_change = game["user_change"]
        base_score = 0
        if user_change == correct_change:
            base_score = 10 * level
            display_result_container(True, correct_change, user_change, "currency", lang)
        else:
            display_result_container(False, correct_change, user_change, "currency", lang)
        # Score, feedback, and progress update
        results = update_skills("change_making", base_score)
        st.write("DEBUG: Skill levels after update", st.session_state.skill_levels)
        # Show educational summary and next steps
        display_educational_tip("cash")
        col1, col2 = st.columns(2)
        with col1:
            path_text = "Go to Learning Path" if lang == "en" else "Buka Jalur Pembelajaran"
            if st.button(path_text, key="go_to_cash_learning_path"):
                st.session_state.current_game = None
                st.session_state.selected_learning_path = "cash"
                st.rerun()
        with col2:
            continue_text = "Continue to Main Menu" if lang == "en" else "Lanjutkan ke Menu Utama"
            if st.button(continue_text, key="continue_cash_main_menu"):
                if "change_making" in st.session_state:
                    del st.session_state.change_making
                st.session_state.current_game = None
                st.rerun()

def is_optimal_change(selected_denominations, amount):
    """Check if the selected denominations represent an optimal change solution.
    
    Args:
        selected_denominations (dict): Dict of denomination: count pairs
        amount (int): The change amount
    
    Returns:
        bool: True if the solution is optimal (minimum number of bills/coins)
    """
    # Get the optimal solution
    optimal = get_optimal_denominations(amount)
    
    # Count total pieces in selected solution
    selected_count = sum(selected_denominations.values())
    
    # Count total pieces in optimal solution
    optimal_count = sum(optimal.values())
    
    # Selected is optimal if it uses the same or fewer pieces
    return selected_count <= optimal_count + 1  # Allow 1 extra piece for flexibility

def get_optimal_denominations(amount):
    """Get the optimal denomination combination for a given amount.
    
    Args:
        amount (int): The amount to make change for
    
    Returns:
        dict: Dict of denomination: count pairs
    """
    # Indonesian Rupiah denominations
    denominations = [100000, 50000, 20000, 10000, 5000, 2000, 1000, 500, 200, 100]
    
    # Initialize result
    result = {denom: 0 for denom in denominations}
    
    # Greedy algorithm for change-making
    remaining = amount
    for denom in denominations:
        if remaining >= denom:
            count = remaining // denom
            result[denom] = count
            remaining -= count * denom
    
    return result

# Helper function to provide game information
def get_game_info():
    """Get information about the change making game.
    
    Returns:
        dict: Game information
    """
    return {
        "id": "change_making",
        "name": {
            "en": "Change Making",
            "id": "Memberi Kembalian"
        },
        "description": {
            "en": "Calculate change quickly and accurately",
            "id": "Hitung kembalian dengan cepat dan akurat"
        },
        "primary_skill": "cash_handling",
        "levels": 5,
        "time_limit": {
            1: None,
            2: None,
            3: None,
            4: 30,
            5: 20
        }
    }