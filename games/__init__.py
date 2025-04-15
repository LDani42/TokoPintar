"""
Game registry for Toko Pintar application.
"""
import streamlit as st
from games.inventory_game import inventory_game, get_game_info as get_inventory_game_info
from games.change_making import change_making_game, get_game_info as get_change_making_info
from games.margin_calculator import margin_calculator_game, get_game_info as get_margin_calculator_info
from games.simple_calculator import simple_calculator_game, get_game_info as get_simple_calculator_info

# Game registry
GAMES = {
    "inventory_game": {
        "function": inventory_game,
        "info": get_inventory_game_info()
    },
    "change_making": {
        "function": change_making_game,
        "info": get_change_making_info()
    },
    "margin_calculator": {
        "function": margin_calculator_game,
        "info": get_margin_calculator_info()
    },
    "simple_calculator": {
        "function": simple_calculator_game,
        "info": get_simple_calculator_info()
    }
}

def get_game_function(game_id):
    """Get the game function for a given game ID.
    
    Args:
        game_id (str): The game identifier
        
    Returns:
        function: The game function, or None if not found
    """
    if game_id in GAMES:
        return GAMES[game_id]["function"]
    return None

def get_game_info(game_id):
    """Get information about a game.
    
    Args:
        game_id (str): The game identifier
        
    Returns:
        dict: Game information, or None if not found
    """
    if game_id in GAMES:
        return GAMES[game_id]["info"]
    return None

def get_all_games():
    """Get all registered games.
    
    Returns:
        dict: Dict of game_id -> game_info pairs
    """
    return {game_id: data["info"] for game_id, data in GAMES.items()}