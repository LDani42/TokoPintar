"""
Database operations for Toko Pintar application.
"""
import os
import sqlite3
import json
import uuid
from datetime import datetime
import streamlit as st
import threading

# Ensure data directory exists
data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
os.makedirs(data_dir, exist_ok=True)

# Thread-local storage for database connections
thread_local = threading.local()

class DatabaseManager:
    def __init__(self, db_path=None):
        if db_path is None:
            self.db_path = os.path.join(data_dir, 'user_data.db')
        else:
            self.db_path = db_path
        
        # Make sure tables exist
        self.ensure_tables_exist()
    
    def get_connection(self):
        """Get or create SQLite connection for the current thread."""
        if not hasattr(thread_local, 'conn') or thread_local.conn is None:
            thread_local.conn = sqlite3.connect(self.db_path)
            thread_local.conn.row_factory = sqlite3.Row
        return thread_local.conn
    
    def close_connection(self):
        """Close the database connection for the current thread."""
        if hasattr(thread_local, 'conn') and thread_local.conn:
            thread_local.conn.close()
            thread_local.conn = None
    
    def ensure_tables_exist(self):
        """Create tables if they don't exist."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            total_score INTEGER DEFAULT 0,
            shop_level INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create skills table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            inventory_management REAL DEFAULT 0,
            cash_handling REAL DEFAULT 0,
            pricing_strategy REAL DEFAULT 0,
            customer_relations REAL DEFAULT 0,
            bookkeeping REAL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        ''')
        
        # Create game_history table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_history (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            game_id TEXT NOT NULL,
            score INTEGER NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            details TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        ''')
        
        # Create achievements table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS achievements (
            achievement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            achievement_type TEXT NOT NULL,
            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            shown BOOLEAN DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        ''')
        
        # Create game_configs table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_configs (
            config_id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id TEXT NOT NULL,
            level INTEGER NOT NULL,
            config_data TEXT NOT NULL,
            UNIQUE(game_id, level)
        )
        ''')
        
        # Create products table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            name_id TEXT,
            buy_price INTEGER NOT NULL,
            sell_price INTEGER NOT NULL,
            category TEXT NOT NULL,
            image_path TEXT,
            stock INTEGER DEFAULT 0
        )
        ''')
        
        conn.commit()
        self.close_connection()
    
    # User methods
    def create_user(self, name, extra_data=None):
        """Create a new user and return the user_id.
        
        Args:
            name (str): User's name
            extra_data (dict, optional): Additional data to store as user metadata
        
        Returns:
            str: User ID or None if error
        """
        user_id = str(uuid.uuid4())
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if we need to alter the users table to add a metadata column
        try:
            cursor.execute("PRAGMA table_info(users)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'metadata' not in columns:
                cursor.execute("ALTER TABLE users ADD COLUMN metadata TEXT")
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error checking/adding metadata column: {e}")
        
        try:
            # Prepare metadata JSON if provided
            metadata_json = None
            if extra_data:
                metadata_json = json.dumps(extra_data)
            
            cursor.execute(
                "INSERT INTO users (user_id, name, metadata) VALUES (?, ?, ?)",
                (user_id, name, metadata_json)
            )
            cursor.execute(
                "INSERT INTO skills (user_id) VALUES (?)",
                (user_id,)
            )
            conn.commit()
            return user_id
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Database error: {e}")
            return None
        finally:
            self.close_connection()
    
    def get_user(self, user_id):
        """Get user by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
        finally:
            self.close_connection()
    
    def get_user_by_name_and_shop(self, name, shop_name):
        """Get user by name and shop name (from metadata)."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM users WHERE name = ?",
                (name,)
            )
            users = cursor.fetchall()
            for user in users:
                # Check metadata for shop name
                metadata = user["metadata"] if "metadata" in user.keys() else None
                if metadata:
                    try:
                        meta_dict = json.loads(metadata)
                        if meta_dict.get("shop_name", "").strip().lower() == shop_name.strip().lower():
                            return dict(user)
                    except Exception:
                        continue
            return None
        finally:
            self.close_connection()
    
    def update_last_active(self, user_id):
        """Update user's last active timestamp."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "UPDATE users SET last_active = ? WHERE user_id = ?",
                (now, user_id)
            )
            conn.commit()
        finally:
            self.close_connection()
    
    def update_total_score(self, user_id, new_score):
        """Update user's total score."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE users SET total_score = ? WHERE user_id = ?",
                (new_score, user_id)
            )
            conn.commit()
        finally:
            self.close_connection()
    
    def update_shop_level(self, user_id, new_level):
        """Update user's shop level."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE users SET shop_level = ? WHERE user_id = ?",
                (new_level, user_id)
            )
            conn.commit()
        finally:
            self.close_connection()
    
    # Skills methods
    def update_skill(self, user_id, skill_name, new_value):
        """Update a single skill value."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"UPDATE skills SET {skill_name} = ? WHERE user_id = ?",
                (new_value, user_id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Database error updating skill: {e}")
            return False
        finally:
            self.close_connection()
    
    def get_skills(self, user_id):
        """Get all skills for a user."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM skills WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
        finally:
            self.close_connection()
    
    # Game history methods
    def add_game_history(self, user_id, game_id, score, details=None):
        """Add a game history entry."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO game_history (user_id, game_id, score, details) VALUES (?, ?, ?, ?)",
                (user_id, game_id, score, json.dumps(details) if details else None)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Database error adding game history: {e}")
            return False
        finally:
            self.close_connection()
    
    def get_game_history(self, user_id, limit=10):
        """Get recent game history for a user."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM game_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
                (user_id, limit)
            )
            return [dict(row) for row in cursor.fetchall()]
        finally:
            self.close_connection()
    
    # Achievement methods
    def add_achievement(self, user_id, achievement_type):
        """Add a new achievement."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Check if achievement already exists
            cursor.execute(
                "SELECT COUNT(*) FROM achievements WHERE user_id = ? AND achievement_type = ?",
                (user_id, achievement_type)
            )
            if cursor.fetchone()[0] > 0:
                return False  # Achievement already exists
                
            cursor.execute(
                "INSERT INTO achievements (user_id, achievement_type) VALUES (?, ?)",
                (user_id, achievement_type)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Database error adding achievement: {e}")
            return False
        finally:
            self.close_connection()
    
    def get_achievements(self, user_id):
        """Get all achievements for a user."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM achievements WHERE user_id = ? ORDER BY earned_at DESC",
                (user_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
        finally:
            self.close_connection()
    
    def mark_achievement_shown(self, achievement_id):
        """Mark an achievement as shown to the user."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE achievements SET shown = 1 WHERE achievement_id = ?",
                (achievement_id,)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Database error marking achievement shown: {e}")
            return False
        finally:
            self.close_connection()
    
    # Product methods
    def add_product(self, name, buy_price, sell_price, category, name_id=None, image_path=None, stock=0):
        """Add a new product."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO products (name, name_id, buy_price, sell_price, category, image_path, stock) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (name, name_id, buy_price, sell_price, category, image_path, stock)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Database error adding product: {e}")
            return None
        finally:
            self.close_connection()
    
    def get_products(self, category=None):
        """Get all products, optionally filtered by category."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if category:
                cursor.execute("SELECT * FROM products WHERE category = ?", (category,))
            else:
                cursor.execute("SELECT * FROM products")
            return [dict(row) for row in cursor.fetchall()]
        finally:
            self.close_connection()
    
    def get_product(self, product_id):
        """Get a product by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
        finally:
            self.close_connection()

# Create a singleton instance for use in Streamlit
db = DatabaseManager()

# Helper function to initialize session from database
def initialize_session_from_db(user_id):
    """Initialize Streamlit session state from database for a user."""
    user = db.get_user(user_id)
    if not user:
        return False
    
    skills = db.get_skills(user_id)
    achievements_db = db.get_achievements(user_id)
    game_history = db.get_game_history(user_id)
    
    # Update session state
    st.session_state.user_id = user_id
    st.session_state.player_name = user['name']
    st.session_state.total_score = user['total_score']
    st.session_state.shop_level = user['shop_level']
    
    # Parse metadata JSON if exists
    if 'metadata' in user and user['metadata']:
        try:
            metadata = json.loads(user['metadata'])
            # Add each metadata key to session state
            for key, value in metadata.items():
                st.session_state[key] = value
        except json.JSONDecodeError:
            print(f"Error parsing user metadata JSON")
    
    # Update skill levels
    st.session_state.skill_levels = {
        "inventory_management": skills['inventory_management'],
        "cash_handling": skills['cash_handling'],
        "pricing_strategy": skills['pricing_strategy'],
        "customer_relations": skills['customer_relations'],
        "bookkeeping": skills['bookkeeping']
    }
    
    # Update achievements - convert database format to session format
    from utils.achievements import get_achievement_details
    
    st.session_state.achievements = []
    for achievement_db in achievements_db:
        achievement_id = achievement_db.get('achievement_type')
        achievement_details = get_achievement_details(achievement_id)
        
        if achievement_details:
            # Create consistent achievement format for session state
            st.session_state.achievements.append({
                "id": achievement_id,
                "name": achievement_details["name"],
                "description": achievement_details["description"],
                "earned_at": achievement_db.get('earned_at', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            })
    
    # Update game history
    st.session_state.game_history = game_history
    
    # Mark user as active
    db.update_last_active(user_id)
    
    return True

# Helper function to save session state to database
def save_session_state_to_db():
    """Save current session state to database."""
    if 'user_id' not in st.session_state:
        return False
    
    user_id = st.session_state.user_id
    
    # Update user record
    db.update_total_score(user_id, st.session_state.total_score)
    db.update_shop_level(user_id, st.session_state.shop_level)
    db.update_last_active(user_id)
    
    # Update skills
    for skill_name, level in st.session_state.skill_levels.items():
        db.update_skill(user_id, skill_name, level)
    
    return True