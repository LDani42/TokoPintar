# Database Schema for Toko Pintar

## SQLite Schema Design

```sql
-- User profile table
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    total_score INTEGER DEFAULT 0,
    shop_level INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Skills progression table
CREATE TABLE skills (
    skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    inventory_management REAL DEFAULT 0,
    cash_handling REAL DEFAULT 0,
    pricing_strategy REAL DEFAULT 0,
    customer_relations REAL DEFAULT 0,
    bookkeeping REAL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Game history
CREATE TABLE game_history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    game_id TEXT NOT NULL,
    score INTEGER NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details TEXT, -- JSON string of game-specific data
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Achievements 
CREATE TABLE achievements (
    achievement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    achievement_type TEXT NOT NULL,
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    shown BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Game configurations
CREATE TABLE game_configs (
    config_id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id TEXT NOT NULL,
    level INTEGER NOT NULL,
    config_data TEXT NOT NULL, -- JSON string of game configuration
    UNIQUE(game_id, level)
);

-- Products database
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    name_id TEXT, -- Indonesian name
    buy_price INTEGER NOT NULL,
    sell_price INTEGER NOT NULL,
    category TEXT NOT NULL,
    image_path TEXT
);
```

## Data Access Layer Implementation

```python
import sqlite3
import json
import uuid
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="data/user_data.db"):
        self.db_path = db_path
        self.conn = None
        self.ensure_tables_exist()
    
    def get_connection(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def ensure_tables_exist(self):
        # Implementation of table creation if not exists
        pass
    
    # User methods
    def create_user(self, name):
        user_id = str(uuid.uuid4())
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (user_id, name) VALUES (?, ?)",
            (user_id, name)
        )
        cursor.execute(
            "INSERT INTO skills (user_id) VALUES (?)",
            (user_id,)
        )
        conn.commit()
        return user_id
    
    def get_user(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone()
    
    # Skills methods
    def update_skill(self, user_id, skill_name, new_value):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE skills SET {skill_name} = ? WHERE user_id = ?",
            (new_value, user_id)
        )
        conn.commit()
    
    def get_skills(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM skills WHERE user_id = ?", (user_id,))
        return cursor.fetchone()
    
    # Game history methods
    def add_game_history(self, user_id, game_id, score, details=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO game_history (user_id, game_id, score, details) VALUES (?, ?, ?, ?)",
            (user_id, game_id, score, json.dumps(details) if details else None)
        )
        conn.commit()
    
    def get_game_history(self, user_id, limit=10):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM game_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
            (user_id, limit)
        )
        return cursor.fetchall()
    
    # Achievement methods
    def add_achievement(self, user_id, achievement_type):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO achievements (user_id, achievement_type) VALUES (?, ?)",
            (user_id, achievement_type)
        )
        conn.commit()
    
    def get_achievements(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM achievements WHERE user_id = ? ORDER BY earned_at DESC",
            (user_id,)
        )
        return cursor.fetchall()
```