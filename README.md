# Toko Pintar

Toko Pintar is an educational game designed to teach financial literacy and operational skills to small retail shop owners in Indonesia through interactive mini-games.

## Features

- **Interactive Mini-Games**: Learn practical skills through gameplay
- **Skill Progression System**: Track improvement in different retail skills
- **Shop Visualization**: Visual representation of shop improvements as skills develop
- **Achievement System**: Earn achievements for reaching skill milestones
- **Educational Content**: Learn practical business concepts through gameplay
- **Bilingual Support**: Available in English and Bahasa Indonesia

## Mini-Games

1. **Inventory Counting**: Practice accurate stock-taking and reconciliation
2. **Change Making**: Calculate change quickly and accurately
3. **Margin Calculator**: Set prices and understand profit margins
4. **Customer Service**: (Coming soon) Learn how to handle customer interactions
5. **Cash Reconciliation**: (Coming soon) Balance your cash register at day's end

## Installation

1. Ensure you have Python 3.7+ installed
2. Clone this repository:
   ```
   git clone https://github.com/yourusername/toko-pintar.git
   cd toko-pintar
   ```
3. Run the setup script:
   ```
   # On Linux/Mac:
   ./run.sh
   
   # On Windows:
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   streamlit run app.py
   ```

## Project Structure

- `/app.py` - Main application entry point
- `/games/` - Mini-game implementations
- `/components/` - Reusable UI components
- `/utils/` - Utility functions and helpers
  - `/utils/game_levels.py` - Level management utilities
  - `/utils/game_ui.py` - UI components for games
  - `/utils/educational_content.py` - Educational content display utilities
- `/assets/` - Static assets (images, styles, etc.)
- `/data/` - Data storage and configuration

## Recent Updates

- Added standardized game level progression system across all games
- Implemented comprehensive educational content delivery system
- Created unified UI components for consistent user experience
- Improved bilingual support throughout the application
- Added real-world application examples for skills taught in games
- Optimized code to reduce duplication and improve maintainability

## Contributing

Contributions are welcome! Here's how you can help:

1. Report bugs or suggest features by opening an issue
2. Improve documentation or translations
3. Submit pull requests for new features or bug fixes

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Developed to support financial education in Indonesian small businesses
- Built with Streamlit, Python, and SQLite
- Open-source educational project