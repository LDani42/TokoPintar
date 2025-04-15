# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build/Test/Lint Commands
- Run app: `streamlit run app.py`
- Install dependencies: `pip install -r requirements.txt`
- Format code: `black app.py`
- Lint: `flake8 app.py`
- Type check: `mypy app.py`

## Code Style Guidelines
- Formatting: Use Black for Python code
- Imports: Group standard library, third-party, and local imports
- Project Structure: Streamlit app structure with session state management
- Naming: snake_case for variables/functions, PascalCase for classes
- Error handling: Use try/except with specific error types
- Comments: Docstrings for functions, inline comments for complex logic
- UI Elements: Organized into sections with consistent styling
- Game Mechanics: Follow patterns in existing mini-games when adding new ones
- State Management: Use st.session_state for persistent game data

## Utility Modules
When implementing new features, use the following utility modules:

### Game UI (utils/game_ui.py)
- For displaying product cards: `display_product_card(product, lang)`
- For displaying results: `display_result_container(is_correct, correct_answer, user_answer, format_type, lang)`
- For displaying accuracy gauges: `display_accuracy_gauge(accuracy, lang)`
- For generating visual representations: `generate_visualization(items, count, style, level)`

### Game Levels (utils/game_levels.py)
- For displaying level selection: `display_level_selection(game_id, level_descriptions, get_level_limits, on_level_select)`
- For displaying level headers: `display_level_header(level, descriptions, tips)`
- For displaying timers: `display_timer(start_time, time_limit)`
- For displaying score breakdowns: `display_score_breakdown(base_score, level_bonus, time_bonus, accuracy_bonus, lang)`
- For displaying end-of-game buttons: `display_game_end_buttons(level, accuracy, lang)`

### Educational Content (utils/educational_content.py)
- For displaying insights: `display_learning_insight(text, insight_type, lang)`
- For displaying formulas: `display_formula_explanation(formula_text, step_by_step_values, lang)`
- For displaying real-world applications: `display_real_world_application(application_text, image_url, case_study, lang)`
- For displaying educational summaries: `display_educational_summary(skill_key, level, content_type, lang)`

## Game Implementation Pattern
When creating or updating games, follow this consistent structure:
1. Define `get_level_description(level)` and `get_level_tips(level)` functions
2. Create an `initialize_[game]_challenge(level)` function to set up game state
3. Implement the main game function with these sections:
   - Header and navigation
   - Level selection (using display_level_selection)
   - Game UI (specific to the game)
   - Answer submission and verification
   - Results display (using display_result_container)
   - Educational content (using educational_content utils)
   - Navigation buttons for next steps
4. Implement a `get_game_info()` function for game registration