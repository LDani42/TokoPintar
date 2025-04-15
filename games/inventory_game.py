"""
Inventory Counting mini-game for Toko Pintar application.
"""
import streamlit as st
import random
import time
from utils.config import get_config, SAMPLE_PRODUCTS
from utils.skills import update_skills
from components.scoreboard import display_educational_tip
from utils.db import db
from utils.tooltips import show_mechanics_tooltip_button, add_tooltips_to_page
import os
from games.breadcrumb import show_game_breadcrumb

def generate_widget_key(*args):
    """Generate a unique widget key by joining all arguments with underscores."""
    return "_".join(str(arg) for arg in args)

def get_game_products(level=1):
    """Get products for the game based on level.
    
    Args:
        level (int): Game difficulty level
    
    Returns:
        list: List of product dictionaries
    """
    # Get products from database
    all_products = db.get_products()
    if not all_products:
        # Fall back to sample products if database is empty
        all_products = SAMPLE_PRODUCTS
    
    # Select products based on level
    if level == 1:
        # Level 1: 3 simple products (no similar items)
        # Group products by category to avoid similar items
        products_by_category = {}
        for product in all_products:
            category = product.get('category', 'Uncategorized')
            if category not in products_by_category:
                products_by_category[category] = []
            products_by_category[category].append(product)
        
        # Select one product from each of the three most distinct categories
        selected_products = []
        for category in list(products_by_category.keys())[:3]:
            if products_by_category[category]:
                selected_products.append(random.choice(products_by_category[category]))
        
        # If we have fewer than 3 categories, fill with random products
        while len(selected_products) < 3 and all_products:
            product = random.choice(all_products)
            if product not in selected_products:
                selected_products.append(product)
                
        return selected_products
    
    elif level == 2:
        # Level 2: 5 products including similar items that must be correctly categorized
        # Ensure some similar products are included
        categories = set(p.get('category', 'Uncategorized') for p in all_products)
        selected_products = []
        
        # Choose 2-3 categories
        selected_categories = random.sample(list(categories), min(3, len(categories)))
        
        # For each selected category, add 1-2 products
        for category in selected_categories:
            category_products = [p for p in all_products if p.get('category', 'Uncategorized') == category]
            num_to_select = min(2, len(category_products))
            selected_products.extend(random.sample(category_products, num_to_select))
        
        # If we still need more products, add random ones
        while len(selected_products) < 5 and len(selected_products) < len(all_products):
            product = random.choice(all_products)
            if product not in selected_products:
                selected_products.append(product)
                
        return selected_products[:5]  # Ensure we return exactly 5 products
    
    elif level == 3:
        # Level 3: 7 random products with time pressure
        return random.sample(all_products, min(7, len(all_products)))
    
    elif level == 4:
        # Level 4: 9 products with some "damaged" or "misplaced" items
        products = random.sample(all_products, min(9, len(all_products)))
        
        # Mark some products as "damaged" or "misplaced"
        # This will be used to display them differently and provide educational content
        for i in range(min(3, len(products))):
            issue_type = random.choice(["damaged", "misplaced"])
            products[i]["issue"] = issue_type
            
        return products
    
    else:
        # Level 5: Many products across multiple categories
        num_products = min(12, len(all_products))
        return random.sample(all_products, num_products)

def initialize_game_state(level=1):
    """Initialize the inventory game state.
    
    Args:
        level (int): Game difficulty level
    """
    # Select products for this game
    products = get_game_products(level)
    
    # Set actual counts (with randomization based on level)
    game_items = []
    for item in products:
        stock = item.get("stock", random.randint(5, 25))
        
        # Variation complexity increases with level
        if level == 1:
            # Level 1: Very small variations for beginners
            variation = random.randint(-1, 1)
        elif level == 2:
            # Level 2: Slightly more variation
            variation = random.randint(-2, 2)
        elif level == 3:
            # Level 3: Moderate variation with time pressure
            variation = random.randint(-3, 3)
        elif level == 4:
            # Level 4: Higher variation and potential issues
            variation = random.randint(-4, 4)
            
            # Apply additional adjustments for damaged/misplaced items
            if "issue" in item:
                if item["issue"] == "damaged":
                    # Damaged items might need to be excluded from count
                    damage_amount = random.randint(1, max(1, int(stock * 0.2)))  # Up to 20% damaged
                    stock -= damage_amount
                    item["damage_amount"] = damage_amount
                elif item["issue"] == "misplaced":
                    # Misplaced items might be in wrong category
                    item["original_category"] = item.get("category", "Uncategorized")
                    item["current_category"] = random.choice(["Shelf A", "Shelf B", "Back Room", "Display"])
        else:
            # Level 5: Maximum complexity
            variation = random.randint(-5, 5)
        
        actual_count = max(0, stock + variation)
        
        game_item = {
            "id": item.get("product_id", str(random.randint(1000, 9999))),
            "name": item["name"],
            "name_id": item.get("name_id", item["name"]),
            "stock": stock,
            "actual_count": actual_count,
            "user_count": 0
        }
        
        # Copy any issue-related fields
        if "issue" in item:
            game_item["issue"] = item["issue"]
        if "damage_amount" in item:
            game_item["damage_amount"] = item["damage_amount"]
        if "original_category" in item:
            game_item["original_category"] = item["original_category"]
            game_item["current_category"] = item["current_category"]
        
        game_items.append(game_item)
    
    # Set time limit based on level
    time_limits = {
        1: None,          # Level 1: No time limit for beginners
        2: None,          # Level 2: No time limit for categorization learning
        3: 90,            # Level 3: Moderate time limit
        4: 75,            # Level 4: Tighter time limit
        5: 60             # Level 5: Challenging time limit
    }
    
    # Store in session state
    st.session_state.inventory_game = {
        "level": level,
        "items": game_items,
        "start_time": time.time(),
        "time_limit": time_limits.get(level),
        "level_description": get_level_description(level),
        "level_tips": get_level_tips(level)
    }

def get_level_description(level):
    """Get description text for each level.
    
    Args:
        level (int): Game difficulty level
        
    Returns:
        dict: Descriptions in English and Indonesian
    """
    descriptions = {
        1: {
            "en": "Basic counting of distinct items. Count each product type accurately.",
            "id": "Penghitungan dasar untuk jenis barang yang berbeda. Hitung setiap jenis produk dengan tepat."
        },
        2: {
            "en": "Similar items categorization. Pay attention to similar-looking products.",
            "id": "Kategorisasi barang yang mirip. Perhatikan produk yang tampak serupa."
        },
        3: {
            "en": "Time pressure inventory. Count accurately while racing against the clock.",
            "id": "Inventaris dengan tekanan waktu. Hitung dengan tepat sambil berlomba dengan waktu."
        },
        4: {
            "en": "Identify discrepancies. Some items may be damaged or misplaced.",
            "id": "Identifikasi perbedaan. Beberapa barang mungkin rusak atau salah tempat."
        },
        5: {
            "en": "Full inventory audit. Handle multiple categories with time pressure.",
            "id": "Audit inventaris lengkap. Tangani berbagai kategori dengan tekanan waktu."
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
            "en": "Take your time and count one item at a time. This builds basic counting skills.",
            "id": "Luangkan waktu dan hitung satu item pada satu waktu. Ini membangun keterampilan menghitung dasar."
        },
        2: {
            "en": "Group similar items and count by category. Note subtle differences between products.",
            "id": "Kelompokkan item serupa dan hitung berdasarkan kategori. Perhatikan perbedaan halus antar produk."
        },
        3: {
            "en": "Use grouping strategies to count quickly. Try counting in groups of 5 or 10.",
            "id": "Gunakan strategi pengelompokan untuk menghitung dengan cepat. Coba hitung dalam kelompok 5 atau 10."
        },
        4: {
            "en": "Look for damaged or misplaced items. In real inventory, these create discrepancies.",
            "id": "Cari barang yang rusak atau salah tempat. Dalam inventaris nyata, ini menciptakan perbedaan."
        },
        5: {
            "en": "Combine speed and accuracy. Use systematic counting patterns to handle complex inventory.",
            "id": "Gabungkan kecepatan dan akurasi. Gunakan pola penghitungan sistematis untuk menangani inventaris kompleks."
        }
    }
    
    return tips.get(level, tips[1])

def generate_visual_inventory(product, actual_count, level=1):
    """Generate a visual representation of products to count (one icon per item, no count shown)."""
    from utils.config import get_product_emoji
    product_emoji = get_product_emoji(product)
    product_name = product.get("name_id") or product.get("name", "")
    html = "<div class='inventory-card'>"
    html += "<div class='inventory-card-emoji-row'>"
    for _ in range(actual_count):
        html += f"<span class='inventory-card-emoji'>{product_emoji}</span>"
    html += "</div>"
    html += f"<div class='inventory-card-name'>{product_name}</div>"
    html += "</div>"
    return html

def inventory_game():
    """Inventory counting mini-game implementation."""
    # Get language preference
    lang = get_config("app.default_language") or "en"
    
    # Force initialization at the start of the game function
    # This must happen before any other code that uses the session state
    if "inventory_game" not in st.session_state:
        st.info("Initializing inventory game...")
        initialize_game_state(1)
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
    title = "Inventory Counting Game" if lang == "en" else "Permainan Menghitung Inventaris"
    description = "Count the items shown for each product and enter the correct numbers." if lang == "en" else "Hitung item yang ditampilkan untuk setiap produk dan masukkan angka yang benar."
    
    st.markdown(f'<p class="game-title">{title}</p>', unsafe_allow_html=True)
    st.write(description)
    
    # Display educational tip
    display_educational_tip("inventory")
    
    # Add game mechanics tooltip button
    col1, col2 = st.columns([3, 1])
    with col2:
        show_mechanics_tooltip_button("inventory_counting", game_id="inventory_game")
    
    # Add tooltips JavaScript
    add_tooltips_to_page()
    
    # Set up level selection
    if "inventory_game" not in st.session_state:
        # Determine available levels based on player's skill
        skill_level = st.session_state.skill_levels.get("inventory_management", 0) if hasattr(st.session_state, "skill_levels") else 0
        max_available_level = min(5, max(1, int(skill_level) + 1))
        
        # Display level selection UI
        st.markdown("### Select Difficulty Level")
        
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
                    <div style="padding: 10px; border-radius: 8px; border: 2px solid #4CAF50; text-align: center; margin-bottom: 10px; cursor: pointer; height: 120px;">
                        <h4 style="margin: 0;">{level_title}</h4>
                        <p style="font-size: 0.8em; margin: 5px 0; height: 40px;">{level_desc}</p>
                        <div style="margin-top: 5px; color: #4CAF50;">Unlocked ✓</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Button to select this level
                    if st.button(f"Select Level {level_num}", key=generate_widget_key("button", f"select_level_{level_num}")):
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
            initialize_game_state(level_selected)
    
    # Get game state - we've already initialized it at the top of the function
    game = st.session_state.inventory_game
    level = game["level"]
    items = game["items"]
    
    # Check if there's a time limit
    if game.get("time_limit"):
        elapsed_time = time.time() - game["start_time"]
        remaining_time = max(0, game["time_limit"] - elapsed_time)
        
        # Display timer
        st.progress(remaining_time / game["time_limit"])
        st.write(f"Time remaining: {int(remaining_time)} seconds")
        
        # Auto-submit if time is up
        if remaining_time <= 0 and not game.get("submitted"):
            st.warning("Time's up! Your count has been submitted.")
            game["submitted"] = True
            st.rerun()
    
    # Display difficulty level with its description
    level_text = f"Level {level}" if lang == "en" else f"Level {level}"
    
    # Get level description and tips
    level_desc = game.get("level_description", {}).get(lang, "")
    level_tips = game.get("level_tips", {}).get(lang, "")
    
    # Display level header with colorful badge based on level
    level_colors = {
        1: "#4CAF50",  # Green for beginner
        2: "#2196F3",  # Blue for easy
        3: "#FF9800",  # Orange for medium
        4: "#9C27B0",  # Purple for hard
        5: "#F44336"   # Red for expert
    }
    
    level_color = level_colors.get(level, "#7E57C2")
    
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 15px;">
        <div style="background-color: {level_color}; color: white; padding: 5px 10px; border-radius: 15px; font-weight: bold; margin-right: 10px;">
            {level_text}
        </div>
        <div style="font-size: 1.1em;">{level_desc}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display tips in an info box
    st.info(f"💡 **Tip:** {level_tips}")
    
    # Display each product with visual counting area and input field
    for i, item in enumerate(items):
        # Use localized name if available and language is Indonesian
        display_name = item["name_id"] if lang == "id" and "name_id" in item else item["name"]
        
        # Create a container for this product
        st.markdown(f"<div class='inventory-item'><strong>{display_name}</strong></div>", unsafe_allow_html=True)
        
        # Generate and display the visual inventory to count
        visual_inventory = generate_visual_inventory(item, item["actual_count"], level)
        st.markdown(visual_inventory, unsafe_allow_html=True)
        
        # Input field for user's count
        count_label = "Your count" if lang == "en" else "Hitungan Anda"
        user_count = st.number_input(
            count_label, 
            min_value=0,
            max_value=100,
            value=items[i]["user_count"],
            key=generate_widget_key("number_input", f"inventory_{i}")
        )
        items[i]["user_count"] = user_count
        
        # Add a separator between products
        st.markdown("---")
    
    # Submit button
    submit_text = "Submit Inventory Count" if lang == "en" else "Kirim Hitungan Inventaris"
    if st.button(submit_text, key=generate_widget_key("button", "submit_inventory")) or game.get("submitted"):
        game["submitted"] = True
        
        score = 0
        results = []
        
        # Check each count
        for item in items:
            display_name = item["name_id"] if lang == "id" and "name_id" in item else item["name"]
            is_correct = item["user_count"] == item["actual_count"]
            
            if is_correct:
                score += 10
                correct_text = "Correct" if lang == "en" else "Benar"
                you_counted = "You counted" if lang == "en" else "Anda menghitung"
                results.append(f"✅ **{display_name}**: {correct_text}! {you_counted} {item['user_count']}")
            else:
                you_counted = "You counted" if lang == "en" else "Anda menghitung"
                actual_count = "actual count was" if lang == "en" else "jumlah sebenarnya adalah"
                results.append(f"❌ **{display_name}**: {you_counted} {item['user_count']}, {actual_count} {item['actual_count']}")
        
        # Calculate bonuses based on level
        time_bonus = 0
        level_bonus = 0
        accuracy_bonus = 0
        total_bonus = 0
        
        # Time bonus for timed levels
        if game.get("time_limit"):
            elapsed_time = time.time() - game["start_time"]
            if elapsed_time < game["time_limit"]:
                # Bonus points for finishing quickly - higher bonus for higher levels
                time_factor = 1 - (elapsed_time / game["time_limit"])
                time_bonus = int((10 + (level * 2)) * time_factor)  # More bonus points at higher levels
                score += time_bonus
                total_bonus += time_bonus
        
        # Level-specific bonuses
        level_bonus = level * 5  # 5 points per level
        score += level_bonus
        total_bonus += level_bonus
        
        # Accuracy bonus
        correct_count = sum(1 for item in items if item["user_count"] == item["actual_count"])
        accuracy = (correct_count / len(items)) * 100
        
        if accuracy == 100:
            # Perfect accuracy bonus increases with level
            accuracy_bonus = 10 * level  # 10 points per level for perfect accuracy
            score += accuracy_bonus
            total_bonus += accuracy_bonus
        
        # Display results
        results_text = "Results" if lang == "en" else "Hasil"
        st.markdown(f"### {results_text}:")
        
        # Group results by category (correct/incorrect) for better readability
        correct_results = []
        incorrect_results = []
        
        for result in results:
            if result.startswith("✅"):
                correct_results.append(result)
            else:
                incorrect_results.append(result)
        
        # Show results in expandable sections
        if correct_results:
            correct_text = "Correct Items" if lang == "en" else "Item Benar"
            with st.expander(f"{correct_text} ({len(correct_results)}/{len(items)})", expanded=True):
                for result in correct_results:
                    st.markdown(result)
        
        if incorrect_results:
            incorrect_text = "Incorrect Items" if lang == "en" else "Item Salah"
            with st.expander(f"{incorrect_text} ({len(incorrect_results)}/{len(items)})", expanded=True):
                for result in incorrect_results:
                    st.markdown(result)
        
        # Show detailed score breakdown
        st.markdown("### Score Breakdown")
        
        # Base score
        base_score_text = "Base Score" if lang == "en" else "Skor Dasar"
        st.markdown(f"**{base_score_text}:** {10 * correct_count} points ({correct_count} correct items × 10)")
        
        # Bonuses
        if time_bonus > 0:
            time_bonus_text = "Time Bonus" if lang == "en" else "Bonus Waktu"
            st.markdown(f"**{time_bonus_text}:** +{time_bonus} points")
        
        if level_bonus > 0:
            level_bonus_text = "Level Bonus" if lang == "en" else "Bonus Level"
            st.markdown(f"**{level_bonus_text}:** +{level_bonus} points")
        
        if accuracy_bonus > 0:
            accuracy_bonus_text = "Perfect Accuracy Bonus" if lang == "en" else "Bonus Akurasi Sempurna"
            st.markdown(f"**{accuracy_bonus_text}:** +{accuracy_bonus} points")
        
        # Total score with animation for emphasis
        score_text = "Total Score" if lang == "en" else "Skor Total"
        
        st.markdown(f"""
        <div style="margin: 15px 0; padding: 10px; background-color: #E8F5E9; border-radius: 8px; border-left: 4px solid #4CAF50;">
            <h3 style="margin: 0; color: #2E7D32;">{score_text}: {score} points</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Show achievement and celebration based on performance and level
        if accuracy == 100:
            st.balloons()
            if level >= 4:
                # Special celebration for perfect score at high levels
                st.markdown(f"""
                <div style="padding: 20px; text-align: center; background-color: #FFF9C4; border-radius: 10px; margin: 20px 0;">
                    <h2 style="color: #FF9800; margin-bottom: 10px;">🏆 {level_text} Master! 🏆</h2>
                    <p style="font-size: 1.2em;">Perfect inventory management at this advanced level is remarkable!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                perfect_score = "Perfect Score" if lang == "en" else "Skor Sempurna"
                skills_excellent = "Your inventory management skills are excellent" if lang == "en" else "Keterampilan manajemen inventaris Anda sangat baik"
                st.success(f"{perfect_score}! {skills_excellent}!")
        elif accuracy >= 80:
            good_job = "Great Job" if lang == "en" else "Kerja Bagus"
            st.success(f"{good_job}! {int(accuracy)}% accuracy is very good!")
        
        # Update player progress
        results = update_skills("inventory_game", score)
        
        # Show detailed feedback based on performance
        st.markdown("### Learning Insights")
        
        # Calculate accuracy percentage
        correct_count = sum(1 for item in items if item["user_count"] == item["actual_count"])
        accuracy = (correct_count / len(items)) * 100
        
        # Display accuracy gauge
        st.markdown(f"""
        <div style="margin: 20px 0;">
            <p style="margin-bottom: 5px;">Accuracy</p>
            <div style="height: 10px; background-color: #EEEEEE; border-radius: 5px;">
                <div style="height: 100%; width: {accuracy}%; background-color: {'#4CAF50' if accuracy >= 70 else '#FFC107' if accuracy >= 40 else '#F44336'}; border-radius: 5px;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                <span>0%</span>
                <span>{accuracy:.0f}%</span>
                <span>100%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Personalized feedback based on performance
        if accuracy == 100:
            st.success("Excellent work! You counted every item correctly. This level of accuracy is essential for proper inventory management.")
            
            # Suggest moving to a harder level
            if level < 5:
                next_level_text = "Try the next level" if lang == "en" else "Coba level berikutnya"
                st.info(f"{next_level_text} for a greater challenge!")
        elif accuracy >= 80:
            st.success("Great job! You're very accurate with your counting. Small errors can still affect inventory management over time.")
            
            # Provide a specific tip for improvement
            if level >= 3:
                st.markdown("""
                <div style="background-color: #FFF3E0; border-left: 4px solid #FF9800; padding: 15px; margin: 15px 0; border-radius: 4px;">
                    <strong>Improvement Tip:</strong> Try counting in groups (like 2s or 5s) for even faster accuracy with large quantities.
                </div>
                """, unsafe_allow_html=True)
        elif accuracy >= 50:
            st.warning("Not bad, but there's room for improvement. Accurate inventory counts prevent stockouts and overstocking.")
            
            # Specific advice based on level
            if level <= 2:
                st.markdown("""
                <div style="background-color: #FFF3E0; border-left: 4px solid #FF9800; padding: 15px; margin: 15px 0; border-radius: 4px;">
                    <strong>Improvement Tip:</strong> Try counting each item once, then verify with a second count.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background-color: #FFF3E0; border-left: 4px solid #FF9800; padding: 15px; margin: 15px 0; border-radius: 4px;">
                    <strong>Improvement Tip:</strong> Group items visually when counting larger quantities to avoid losing your place.
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("Your accuracy needs improvement. Incorrect inventory counts can lead to business losses.")
            
            # Basic advice for struggling players
            st.markdown("""
            <div style="background-color: #FFF3E0; border-left: 4px solid #FF9800; padding: 15px; margin: 15px 0; border-radius: 4px;">
                <strong>Improvement Tip:</strong> Start by organizing items into rows of 5 or 10 to make counting easier.
            </div>
            """, unsafe_allow_html=True)
        
        # Show real-world application
        from components.learning.real_world_tips import get_real_world_applications
        applications = get_real_world_applications("inventory_management", 1)
        if applications and lang in applications:
            with st.expander("See Real-World Examples"):
                st.markdown(applications[lang])
        
        # Learning path suggestion
        st.markdown("""
        <div style="background-color: #E8F5E9; border: 1px solid #66BB6A; border-radius: 8px; padding: 15px; margin-top: 20px;">
            <h4 style="color: #2E7D32; margin-top: 0;">Continue Your Learning</h4>
            <p>Explore the Inventory Management learning path to master more advanced techniques.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Learning path button
        path_text = "Go to Learning Path" if lang == "en" else "Buka Jalur Pembelajaran"
        if st.button(path_text, key=generate_widget_key("button", "go_to_learning_path")):
            st.session_state.current_game = None
            st.session_state.selected_learning_path = "inventory"
            st.rerun()
        
        # Continue button
        continue_text = "Continue to Main Menu" if lang == "en" else "Lanjutkan ke Menu Utama"
        if st.button(continue_text, key=generate_widget_key("button", "continue_main_menu")):
            # Clean up game state
            if "inventory_game" in st.session_state:
                del st.session_state.inventory_game
            
            st.session_state.current_game = None
            st.rerun()
            
        # Removed the automatic return to main menu
        # The user will now need to click a button to continue

# Helper function to provide game information
def get_game_info():
    """Get information about the inventory game.
    
    Returns:
        dict: Game information
    """
    return {
        "id": "inventory_game",
        "name": {
            "en": "Inventory Counting",
            "id": "Menghitung Inventaris"
        },
        "title": "Inventory Counting Game",
        "description": {
            "en": "Keep track of your stock accurately",
            "id": "Catat persediaan Anda dengan akurat"
        },
        "primary_skill": "inventory_management",
        "levels": 5,
        "level_descriptions": {
            1: {
                "en": "Basic counting of distinct items",
                "id": "Penghitungan dasar untuk jenis barang yang berbeda"
            },
            2: {
                "en": "Similar items categorization",
                "id": "Kategorisasi barang yang mirip"
            },
            3: {
                "en": "Time pressure inventory counting",
                "id": "Penghitungan inventaris dengan tekanan waktu"
            },
            4: {
                "en": "Identifying damaged and misplaced items",
                "id": "Mengidentifikasi barang rusak dan salah tempat"
            },
            5: {
                "en": "Full inventory audit with multiple categories",
                "id": "Audit inventaris lengkap dengan beberapa kategori"
            }
        },
        "time_limit": {
            1: None,
            2: None,
            3: 90,
            4: 75,
            5: 60
        },
        "max_score": {
            1: 50,   # Base: 30 + Level bonus: 5 + Perfect bonus: 10 + Time bonus: 5 (no time limit)
            2: 85,   # Base: 50 + Level bonus: 10 + Perfect bonus: 20 + Time bonus: 5 (no time limit)
            3: 150,  # Base: 70 + Level bonus: 15 + Perfect bonus: 30 + Time bonus: 35
            4: 205,  # Base: 90 + Level bonus: 20 + Perfect bonus: 40 + Time bonus: 55
            5: 275   # Base: 120 + Level bonus: 25 + Perfect bonus: 50 + Time bonus: 80
        },
        "educational_objectives": {
            1: {
                "en": "Basic counting skills and stock awareness",
                "id": "Keterampilan menghitung dasar dan kesadaran stok"
            },
            2: {
                "en": "Product categorization and differentiation",
                "id": "Kategorisasi dan pembedaan produk"
            },
            3: {
                "en": "Speed and accuracy balance in inventory management",
                "id": "Keseimbangan kecepatan dan akurasi dalam manajemen inventaris"
            },
            4: {
                "en": "Identifying inventory discrepancies and their causes",
                "id": "Mengidentifikasi perbedaan inventaris dan penyebabnya"
            },
            5: {
                "en": "Comprehensive inventory management under pressure",
                "id": "Manajemen inventaris komprehensif di bawah tekanan"
            }
        }
    }