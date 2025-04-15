"""
Game UI utilities for Toko Pintar application.
Provides standardized UI components across games.
"""
import streamlit as st
import random
from utils.config import get_config, get_product_emoji

def display_product_card(product, lang="en"):
    """Display a product card with consistent styling.
    
    Args:
        product (dict): Product information
        lang (str): Language code
        
    Returns:
        str: Generated HTML for the product card
    """
    # Get emoji and name
    product_emoji = get_product_emoji(product)
    product_name = product.get("name_id", product.get("name", "")) if lang == "id" and "name_id" in product else product.get("name", "")
    
    # Create product card HTML
    html = f"""
    <div style='background-color: #f5f5f5; padding: 15px; border-radius: 10px; margin-bottom: 20px; 
         border-left: 5px solid #1E88E5;'>
        <h3 style='margin-top: 0;'>{product_emoji} {product_name}</h3>
    """
    
    # Add additional product details if available
    if "buy_price" in product:
        buy_price_text = "Buy price" if lang == "en" else "Harga beli"
        html += f"""
        <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
            <span style='font-weight: bold;'>{buy_price_text}:</span>
            <span class='cash-amount'>Rp {product['buy_price']:,}</span>
        </div>
        """
    
    if "sell_price" in product:
        sell_price_text = "Sell price" if lang == "en" else "Harga jual"
        html += f"""
        <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
            <span style='font-weight: bold;'>{sell_price_text}:</span>
            <span class='cash-amount'>Rp {product['sell_price']:,}</span>
        </div>
        """
    
    if "stock" in product:
        stock_text = "Stock" if lang == "en" else "Stok"
        html += f"""
        <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
            <span style='font-weight: bold;'>{stock_text}:</span>
            <span>{product['stock']}</span>
        </div>
        """
    
    html += "</div>"
    return html

def display_calculator_input(label, min_value=0, max_value=1000000, step=100, prefix="Rp", 
                        with_calculator=False, lang="en"):
    """Display a calculator-style input with consistent styling.
    
    Args:
        label (str): Input label
        min_value (int): Minimum value allowed
        max_value (int): Maximum value allowed
        step (int): Step size for the input
        prefix (str): Currency prefix (e.g., "Rp")
        with_calculator (bool): Whether to show a calculator widget
        lang (str): Language code
        
    Returns:
        int: The input value
    """
    st.markdown("<div style='background-color: #f1f8e9; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)
    
    st.markdown(f"<h4>{label}</h4>", unsafe_allow_html=True)
    
    # Calculator input with currency prefix
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.markdown(f"<div style='background-color: #e0e0e0; height: 38px; border-radius: 5px 0 0 5px; display: flex; align-items: center; justify-content: center; font-weight: bold;'>{prefix}</div>", unsafe_allow_html=True)
    
    with col2:
        value = st.number_input(
            "Value",
            min_value=min_value,
            max_value=max_value,
            value=0,
            step=step,
            label_visibility="collapsed"
        )
    
    # Add calculator widget if requested
    if with_calculator:
        from components.scoreboard import display_simple_calculator
        display_simple_calculator()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    return value

def display_result_container(is_correct, correct_answer, user_answer, format_type="currency", lang="en"):
    """Display a result container with correct/incorrect styling.
    
    Args:
        is_correct (bool): Whether the answer is correct
        correct_answer (any): The correct answer
        user_answer (any): The user's answer
        format_type (str): How to format the answers (currency, percent, number)
        lang (str): Language code
    """
    if is_correct:
        # Celebration for correct answer
        correct_text = "Correct" if lang == "en" else "Benar"
        answer_text = "The correct answer is" if lang == "en" else "Jawaban yang benar adalah"
        
        # Format answer based on format_type
        if format_type == "currency":
            formatted_answer = f"Rp {correct_answer:,}"
        elif format_type == "percent":
            formatted_answer = f"{correct_answer}%"
        else:
            formatted_answer = f"{correct_answer}"
            
        # Display success message
        st.markdown(f"""
        <div style="background-color: #E8F5E9; border-left: 4px solid #4CAF50; padding: 15px; margin-bottom: 20px; border-radius: 4px;">
            <h4 style="color: #2E7D32; margin-top: 0;">✅ {correct_text}!</h4>
            <p style="margin-bottom: 5px;">{answer_text}: <strong>{formatted_answer}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        # Display incorrect answer message
        incorrect_text = "Incorrect" if lang == "en" else "Salah"
        correct_text = "The correct answer is" if lang == "en" else "Jawaban yang benar adalah"
        
        # Format answers based on format_type
        if format_type == "currency":
            formatted_correct = f"Rp {correct_answer:,}"
            formatted_user = f"Rp {user_answer:,}"
        elif format_type == "percent":
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

def display_accuracy_gauge(accuracy, lang="en"):
    """Display an accuracy gauge with color-coding.
    
    Args:
        accuracy (float): Accuracy percentage (0-100)
        lang (str): Language code
    """
    accuracy_text = "Accuracy" if lang == "en" else "Akurasi"
    
    st.markdown(f"""
    <div style="margin: 20px 0;">
        <p style="margin-bottom: 5px;">{accuracy_text}</p>
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

def generate_visualization(items, count, style="default", level=1):
    """Generate a visual representation of items.
    
    Args:
        items (str): Emoji or identifier of items to show
        count (int): Number of items to display
        style (str): Visual style to use (default, random, grid, etc.)
        level (int): Game difficulty level
        
    Returns:
        str: HTML string for the visualization
    """
    # Start container
    container_style = "display: flex; flex-wrap: wrap; margin-bottom: 10px; padding: 10px; border-radius: 5px;"
    html = f"<div style='{container_style}'>"
    
    # Apply different visualization styles
    if style == "random":
        # Random arrangement with varied spacing
        for i in range(count):
            margin = f"{random.randint(2, 10)}px"
            size = f"{random.randint(24, 32)}px"
            html += f"<div style='font-size: {size}; margin: {margin}; display: inline-block;'>{items}</div>"
    
    elif style == "grid":
        # Organized grid arrangement
        for i in range(count):
            html += f"<div style='font-size: 28px; margin: 4px; display: inline-block;'>{items}</div>"
            if (i + 1) % 5 == 0 and i < count - 1:
                html += "</div><div style='{container_style}'>"
    
    elif style == "dynamic":
        # Size, opacity and position vary based on level
        indices = list(range(count))
        random.shuffle(indices)
        
        for i in range(count):
            # Randomize size, spacing, and opacity based on level
            size_variance = 8 + (level * 2)  # More variance at higher levels
            size = f"{random.randint(28 - size_variance//2, 28 + size_variance//2)}px"
            margin = f"{random.randint(2, 4 + level)}px"
            opacity = random.uniform(0.8, 1.0) if level >= 4 else 1.0
            
            html += f"<div style='font-size: {size}; margin: {margin}; opacity: {opacity}; display: inline-block;'>{items}</div>"
    
    else:
        # Default display
        for i in range(count):
            html += f"<div style='font-size: 28px; margin: 4px; display: inline-block;'>{items}</div>"
    
    html += "</div>"
    return html