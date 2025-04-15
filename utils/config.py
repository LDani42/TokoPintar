"""
Configuration management for Toko Pintar application.
"""
import os
import json
import uuid
import streamlit as st

# Define paths
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
ASSET_DIR = os.path.join(ROOT_DIR, 'assets')
IMAGE_DIR = os.path.join(ASSET_DIR, 'images')
I18N_DIR = os.path.join(ASSET_DIR, 'i18n')

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(I18N_DIR, exist_ok=True)

# Default configuration
DEFAULT_CONFIG = {
    "app": {
        "title": "Toko Pintar - Financial Literacy Game",
        "version": "0.3.0",
        "default_language": "en"
    },
    "gameplay": {
        "max_skill_level": 5,
        "skill_increase_amount": 0.2,
        "shop_level_threshold": 1.0
    },
    "debug": {
        "enabled": True,  # Enable debug mode to verify calculations
        "log_level": "INFO"
    }
}

# Path to config file
CONFIG_FILE = os.path.join(DATA_DIR, 'config.json')

def load_config():
    """Load configuration from file or create default if not exists."""
    if not os.path.exists(CONFIG_FILE):
        # Create default config
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        return DEFAULT_CONFIG

def save_config(config):
    """Save configuration to file."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def get_config(key=None):
    """Get configuration value by key path (dot notation) or entire config."""
    if not hasattr(st.session_state, 'app_config'):
        st.session_state.app_config = load_config()
    
    if key is None:
        return st.session_state.app_config
    
    # Handle dot notation (e.g., "app.title")
    keys = key.split('.')
    value = st.session_state.app_config
    for k in keys:
        if k in value:
            value = value[k]
        else:
            return None
    
    return value

def set_config(key, value):
    """Set configuration value by key path (dot notation)."""
    if not hasattr(st.session_state, 'app_config'):
        st.session_state.app_config = load_config()
    
    # Handle dot notation (e.g., "app.title")
    keys = key.split('.')
    config = st.session_state.app_config
    
    # Navigate to the correct level
    current = config
    for i, k in enumerate(keys[:-1]):
        if k not in current:
            current[k] = {}
        current = current[k]
    
    # Set the value
    current[keys[-1]] = value
    
    # Save to file
    save_config(config)
    return True

# Product-specific emoji mappings
PRODUCT_EMOJI_MAP = {
    # Foods
    "Indomie": "🍜",
    "Instant Noodles": "🍜",
    "Bread": "🍞",
    "Rice": "🍚",
    "Eggs": "🥚",
    "Egg": "🥚",
    "Egg (each)": "🥚",
    "Telur": "🥚",
    "Telur (per butir)": "🥚",
    "Flour": "🌾",
    "Sugar": "🧂",
    "Salt": "🧂",
    "Cooking Oil": "🫙",
    "Milk": "🥛",
    "Chocolate": "🍫",
    "Candy": "🍬",
    "Biscuits": "🍪",
    "Crackers": "🍘",
    "Snacks": "🍿",
    
    # Beverages
    "Bottled Tea": "🧃",
    "Teh Botol": "🧃",
    "Tea": "🫖",
    "Coffee": "☕",
    "Coffee Sachet": "☕",
    "Juice": "🧃",
    "Soda": "🥤",
    "Mineral Water": "💧",
    "Water": "💧",
    "Energy Drink": "🥤",
    
    # Hygiene
    "Soap": "🧼",
    "Shampoo": "🧴",
    "Toothpaste": "🧴",
    "Toilet Paper": "🧻",
    "Detergent": "🧼",
    "Dishwashing Liquid": "🧴",
    
    # Grocery
    "Rice 1kg": "🍚",
    "Beras 1kg": "🍚",
    "Sugar 1kg": "🧂",
    "Gula 1kg": "🧂",
    "Cooking Oil 1L": "🫙",
    "Minyak Goreng 1L": "🫙",
    "Salt": "🧂",
    
    # Fallbacks by category
    "_category_Food": "🍲",
    "_category_Beverage": "🥤",
    "_category_Hygiene": "🧼",
    "_category_Grocery": "🛒",
    "_category_Default": "📦"
}

# Sample product data (will be moved to database later)
SAMPLE_PRODUCTS = [
    {"name": "Indomie", "name_id": "Indomie", "buy_price": 2500, "sell_price": 3500, "stock": 24, "category": "Food"},
    {"name": "Bottled Tea", "name_id": "Teh Botol", "buy_price": 3000, "sell_price": 4000, "stock": 15, "category": "Beverage"},
    {"name": "Soap", "name_id": "Sabun Mandi", "buy_price": 3500, "sell_price": 5000, "stock": 10, "category": "Hygiene"},
    {"name": "Sugar 1kg", "name_id": "Gula 1kg", "buy_price": 15000, "sell_price": 18000, "stock": 5, "category": "Grocery"},
    {"name": "Cooking Oil 1L", "name_id": "Minyak Goreng 1L", "buy_price": 20000, "sell_price": 23000, "stock": 3, "category": "Grocery"},
    {"name": "Coffee Sachet", "name_id": "Kopi Sachet", "buy_price": 1500, "sell_price": 2000, "stock": 30, "category": "Beverage"},
    {"name": "Rice 1kg", "name_id": "Beras 1kg", "buy_price": 12000, "sell_price": 13500, "stock": 8, "category": "Grocery"},
    {"name": "Egg (each)", "name_id": "Telur (per butir)", "buy_price": 2000, "sell_price": 2500, "stock": 20, "category": "Food"},
    {"name": "Toothpaste", "name_id": "Pasta Gigi", "buy_price": 10000, "sell_price": 12000, "stock": 6, "category": "Hygiene"},
    {"name": "Mineral Water", "name_id": "Air Mineral", "buy_price": 2000, "sell_price": 3000, "stock": 24, "category": "Beverage"}
]

def initialize_product_database():
    """Initialize product database with sample data."""
    from utils.db import db
    
    try:
        # Check if products already exist
        products = db.get_products()
        if products:
            return
        
        # Add sample products
        for product in SAMPLE_PRODUCTS:
            db.add_product(
                name=product["name"],
                name_id=product.get("name_id", product["name"]),
                buy_price=product["buy_price"],
                sell_price=product["sell_price"],
                category=product["category"],
                stock=product.get("stock", 0)
            )
    except Exception as e:
        print(f"Error initializing product database: {e}")

def get_translation(key, language=None):
    """Get a translated string for the given key and language."""
    if language is None:
        language = get_config('app.default_language')
    
    # Load translation file
    translation_file = os.path.join(I18N_DIR, f"{language}.json")
    if not os.path.exists(translation_file):
        # Create empty translation file
        with open(translation_file, 'w') as f:
            json.dump({}, f, indent=4)
        return key
    
    try:
        with open(translation_file, 'r') as f:
            translations = json.load(f)
            
        if key in translations:
            return translations[key]
        else:
            # Key not found, return the key itself
            return key
    except Exception as e:
        print(f"Error loading translation: {e}")
        return key
        
def generate_widget_key(prefix, identifier="", stable=False):
    """Generate a unique widget key with a prefix and optional identifier.
    
    Args:
        prefix (str): A prefix for the key (e.g., 'button', 'input')
        identifier (str, optional): An additional identifier. Defaults to "".
        stable (bool, optional): If True, return a stable key without random UUID. 
                                Use this only for widgets that need persistence.
        
    Returns:
        str: A unique widget key
    """
    # Get the language from session state
    lang = get_config("app.default_language") or "en"
    
    # For stable keys (like language selectors), skip the random UUID
    if stable:
        if identifier:
            return f"{prefix}__{identifier}__{lang}__stable"
        else:
            return f"{prefix}__{lang}__stable"
    
    # For normal widgets, add a unique ID to prevent duplication
    unique_id = str(uuid.uuid4())[:8]
    
    # Combine all parts to make a unique key
    if identifier:
        return f"{prefix}__{identifier}__{lang}__{unique_id}"
    else:
        return f"{prefix}__{lang}__{unique_id}"

def get_product_emoji(product):
    """Get an appropriate emoji for a given product.
    
    Args:
        product (dict or str): Either a product dict or product name
        
    Returns:
        str: Emoji representing the product
    """
    # Handle both product objects and strings
    if isinstance(product, dict):
        product_name = product.get("name", "")
        product_id_name = product.get("name_id", "")
        category = product.get("category", "Default")
    else:
        product_name = product
        product_id_name = ""
        category = "Default"
    
    # Try to find a direct match for the name
    if product_name in PRODUCT_EMOJI_MAP:
        return PRODUCT_EMOJI_MAP[product_name]
    
    # Try the localized name if available
    if product_id_name and product_id_name in PRODUCT_EMOJI_MAP:
        return PRODUCT_EMOJI_MAP[product_id_name]
    
    # Fall back to category
    category_key = f"_category_{category}"
    if category_key in PRODUCT_EMOJI_MAP:
        return PRODUCT_EMOJI_MAP[category_key]
    
    # Ultimate fallback
    return PRODUCT_EMOJI_MAP["_category_Default"]