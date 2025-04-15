# Toko Pintar Technical Architecture

## Directory Structure
```
/tokopintar/
├── app.py                 # Main application entry point
├── requirements.txt       # Dependencies
├── data/                  # Data storage
│   ├── game_data.json     # Game configuration
│   └── user_data.db       # SQLite database for user progress
├── assets/                # Static assets
│   ├── images/            # Game and UI images
│   ├── i18n/              # Internationalization files
│   └── styles/            # CSS styles
├── components/            # Reusable UI components
│   ├── navigation.py      # Navigation components
│   ├── scoreboard.py      # Scoring components
│   └── shop_display.py    # Shop visualization
├── games/                 # Game modules
│   ├── __init__.py        # Game registry
│   ├── inventory_game.py  # Inventory counting game
│   ├── change_making.py   # Change making game
│   ├── margin_calc.py     # Margin calculator game
│   ├── customer_service.py # Customer service game
│   └── cash_reconciliation.py # Cash reconciliation game
└── utils/                 # Utility functions
    ├── db.py              # Database operations
    ├── achievements.py    # Achievement system
    ├── skills.py          # Skill progression
    └── config.py          # Configuration management
```

## Data Model

### User Profile
- `user_id`: Unique identifier
- `name`: Player name
- `total_score`: Cumulative score
- `shop_level`: Current shop level
- `created_at`: Account creation date
- `last_active`: Last session timestamp

### Skills
- `user_id`: User reference
- `inventory_management`: Skill level (0-5)
- `cash_handling`: Skill level (0-5)
- `pricing_strategy`: Skill level (0-5)
- `customer_relations`: Skill level (0-5)
- `bookkeeping`: Skill level (0-5)

### Game History
- `id`: Entry identifier
- `user_id`: User reference
- `game_id`: Game identifier
- `score`: Points earned
- `timestamp`: When played
- `details`: JSON of game-specific data

### Achievements
- `id`: Achievement identifier
- `user_id`: User reference
- `achievement_id`: Achievement type
- `earned_at`: When achieved
- `shown`: Whether revealed to user

## Key Components

### State Management
- Session state for game-in-progress
- SQLite for persistent storage
- JSON for configuration and game content

### Internationalization
- Text resource files for English and Bahasa Indonesia
- Language selector in UI
- Culturally relevant content variations

### Progression System
- XP-based skill advancement
- Level-gated content
- Achievement triggers tied to gameplay milestones

### Educational Integration
- Just-in-time learning prompts
- Post-game educational summaries
- Real-world application suggestions