"""
Educational content utilities for Toko Pintar application.
Provides standardized display of educational content across games.
"""
import streamlit as st
from utils.config import get_config

def display_learning_insight(text, insight_type="info", lang="en"):
    """Display an educational insight with consistent styling.
    
    Args:
        text (str): The insight text content
        insight_type (str): Type of insight (info, success, warning, error)
        lang (str): Language code
    """
    style_map = {
        "info": {
            "bg_color": "#E3F2FD", 
            "border_color": "#2196F3", 
            "icon": "💡",
            "title": "Key Insight" if lang == "en" else "Wawasan Kunci"
        },
        "success": {
            "bg_color": "#E8F5E9", 
            "border_color": "#4CAF50", 
            "icon": "✅",
            "title": "Success Tip" if lang == "en" else "Tip Sukses"
        },
        "warning": {
            "bg_color": "#FFF3E0", 
            "border_color": "#FF9800", 
            "icon": "⚠️",
            "title": "Important Note" if lang == "en" else "Catatan Penting"
        },
        "error": {
            "bg_color": "#FFEBEE", 
            "border_color": "#F44336", 
            "icon": "❌",
            "title": "Common Mistake" if lang == "en" else "Kesalahan Umum"
        }
    }
    
    style = style_map.get(insight_type, style_map["info"])
    
    st.markdown(f"""
    <div style="background-color: {style['bg_color']}; border-left: 4px solid {style['border_color']}; padding: 15px; margin: 15px 0; border-radius: 4px;">
        <strong>{style['icon']} {style['title']}:</strong> {text}
    </div>
    """, unsafe_allow_html=True)

def display_formula_explanation(formula_text, step_by_step_values=None, lang="en"):
    """Display a mathematical formula with explanation.
    
    Args:
        formula_text (str): The formula as text
        step_by_step_values (list, optional): List of steps showing calculation with values
        lang (str): Language code
    """
    formula_title = "Formula" if lang == "en" else "Rumus"
    
    html = f"""
    <div style='background-color: #e3f2fd; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
        <p style='font-weight: bold;'>{formula_title}:</p>
        <div class='math-formula'>
            {formula_text}
        </div>
    """
    
    if step_by_step_values:
        for step in step_by_step_values:
            html += f"""
            <div class='math-formula'>
                {step}
            </div>
            """
    
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

def display_real_world_application(application_text, image_url=None, case_study=None, lang="en"):
    """Display a real-world application of a concept.
    
    Args:
        application_text (str): The application text
        image_url (str, optional): URL to an illustrative image
        case_study (dict, optional): More detailed case study with title and content
        lang (str): Language code
    """
    real_world_title = "Real-World Application" if lang == "en" else "Aplikasi Dunia Nyata"
    
    with st.expander(real_world_title):
        st.markdown(f"**{real_world_title}:** {application_text}")
        
        if image_url:
            st.image(image_url)
        
        if case_study:
            case_study_title = case_study.get("title", "Case Study" if lang == "en" else "Studi Kasus")
            case_study_content = case_study.get("content", "")
            
            st.markdown(f"### {case_study_title}")
            st.markdown(case_study_content)

def display_educational_summary(skill_key, level, content_type="game_result", lang="en"):
    """Display a summary of educational content for a skill and level.
    
    Args:
        skill_key (str): The skill identifier
        level (int): Skill level
        content_type (str): Type of content to show (game_result, learning_path)
        lang (str): Language code
    """
    # Import components only when needed to avoid circular imports
    from components.learning.real_world_tips import get_real_world_applications, get_tips_for_skill
    
    # Titles based on content type
    titles = {
        "game_result": "Learning Insights" if lang == "en" else "Wawasan Pembelajaran",
        "learning_path": "Key Concepts" if lang == "en" else "Konsep Kunci"
    }
    
    st.markdown(f"### {titles.get(content_type, titles['game_result'])}")
    
    # Show skill-specific educational content
    if skill_key == "inventory_management":
        if level == 1:
            display_learning_insight(
                "Accurate inventory counting is the foundation of inventory management. It helps prevent stockouts and overstocking.", 
                "info", 
                lang
            )
        elif level == 2:
            display_learning_insight(
                "Organizing similar items in categories makes inventory management more efficient and reduces counting errors.", 
                "info", 
                lang
            )
        elif level >= 3:
            display_learning_insight(
                "Regular inventory counts help identify discrepancies early and maintain accurate stock levels.", 
                "info", 
                lang
            )
    
    elif skill_key == "cash_handling":
        if level == 1:
            display_learning_insight(
                "Counting cash twice before finalizing a transaction is a best practice that reduces errors.", 
                "info", 
                lang
            )
        elif level == 2:
            display_learning_insight(
                "Organizing your cash drawer by denomination makes transactions faster and more accurate.", 
                "info", 
                lang
            )
        elif level >= 3:
            display_learning_insight(
                "Regular cash reconciliation ensures that your actual cash matches your sales records.", 
                "info", 
                lang
            )
    
    elif skill_key == "pricing_strategy":
        if level == 1:
            display_learning_insight(
                "Setting the right price is crucial for profitability. The margin percentage directly impacts how much profit you make on each sale.", 
                "info", 
                lang
            )
        elif level == 2:
            display_learning_insight(
                "Calculating margin percentages helps you compare profitability across different products, regardless of their absolute prices.", 
                "info", 
                lang
            )
        elif level >= 3:
            display_learning_insight(
                "Understanding price elasticity helps you set optimal prices that maximize your total profit.", 
                "info", 
                lang
            )
    
    # Show real-world applications if available
    applications = get_real_world_applications(skill_key, level)
    if applications and lang in applications:
        real_world_title = "Real-World Examples" if lang == "en" else "Contoh Dunia Nyata"
        with st.expander(real_world_title):
            st.markdown(applications[lang])
    
    # Show tips if available
    tips = get_tips_for_skill(skill_key, level)
    if tips:
        tips_title = "Pro Tips" if lang == "en" else "Tips Pro"
        with st.expander(tips_title):
            for tip in tips:
                from components.learning.real_world_tips import display_pro_tip
                display_pro_tip(tip)