import streamlit as st

# Game registry with lazy imports to avoid circular dependencies

def get_game_function(game_id):
    if game_id == "inventory_game":
        from games.inventory_game import inventory_game
        return inventory_game
    elif game_id == "change_making":
        from games.change_making import change_making_game
        return change_making_game
    elif game_id == "margin_calculator":
        from games.margin_calculator import margin_calculator_game
        return margin_calculator_game
    elif game_id == "simple_calculator":
        from games.simple_calculator import simple_calculator_game
        return simple_calculator_game
    return None

def get_game_info(game_id):
    if game_id == "inventory_game":
        from games.inventory_game import get_game_info as info
        return info()
    elif game_id == "change_making":
        from games.change_making import get_game_info as info
        return info()
    elif game_id == "margin_calculator":
        from games.margin_calculator import get_game_info as info
        return info()
    elif game_id == "simple_calculator":
        from games.simple_calculator import get_game_info as info
        return info()
    return None

def get_all_games():
    return {
        "inventory_game": get_game_info("inventory_game"),
        "change_making": get_game_info("change_making"),
        "margin_calculator": get_game_info("margin_calculator"),
        "simple_calculator": get_game_info("simple_calculator"),
    }
