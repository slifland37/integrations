# Pokemon Explorer - Interactive Interface

A console-based interactive application for exploring Pokemon data using the PokeAPI.

## Features

### Phase 1 (Current Implementation)
- ✅ **Interactive Menu System** - User-friendly console interface
- ✅ **Pokemon Search** - Search Pokemon by name with detailed information
- ✅ **Enhanced Pokemon Display** - View stats, types, abilities, and moves
- ✅ **Favorites System** - Save and manage your favorite Pokemon
- ✅ **Search History** - Track your recent searches
- ✅ **Settings Management** - Customize your experience

### Coming Soon (Phase 2-4)
- 🔄 **Type & Generation Browsing** - Browse Pokemon by type or generation
- 🔄 **Random Pokemon Discovery** - Discover new Pokemon randomly
- 🔄 **Evolution Chains** - View Pokemon evolution information
- 🔄 **Pokemon Quiz System** - Interactive quizzes about Pokemon
- 🔄 **Advanced Search Filters** - More sophisticated search options

## Installation

1. **Navigate to the PokeAPI directory:**
   ```bash
   cd PokeAPI
   ```

2. **Set up virtual environment (recommended):**
   ```bash
   # On Windows:
   .venv\Scripts\activate
   
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Quick Start
Run the interactive interface:
```bash
python run_explorer.py
```

### Alternative Methods
- **Direct execution:**
  ```bash
  python app/interactive_menu.py
  ```
  
- **Original script (still available):**
  ```bash
  python app/pokeapi.py pikachu
  ```

## Interactive Interface Guide

### Main Menu
```
┌─────────────────────────────────────┐
│         POKEMON EXPLORER            │
├─────────────────────────────────────┤
│ 1. Search Pokemon                   │
│ 2. Browse by Type                   │
│ 3. Browse by Generation             │
│ 4. Random Pokemon                   │
│ 5. My Favorites                     │
│ 6. Pokemon Quiz                     │
│ 7. Settings                         │
│ 8. Exit                             │
└─────────────────────────────────────┘
```

### Navigation
- **Enter numbers** to select menu options
- **Press Enter** to confirm selections
- **Use n/p/q** for pagination in move lists
- **Press Enter** to return to previous menus

### Key Features

#### 1. Search Pokemon
- **Search by Name**: Find Pokemon by exact or partial name
- **Search by Type**: Browse Pokemon by type (coming soon)
- **Search by Generation**: Browse by game generation (coming soon)

#### 2. Pokemon Details
- **Basic Info**: Height, weight, base experience
- **Types**: Pokemon type(s) with effectiveness
- **Stats**: Base stats (HP, Attack, Defense, etc.)
- **Abilities**: Pokemon abilities and hidden abilities
- **Moves**: Complete move list with pagination

#### 3. Favorites System
- **Add Pokemon**: Save Pokemon to your favorites
- **View Favorites**: Browse your saved Pokemon
- **Remove Favorites**: Remove Pokemon from your list
- **Clear All**: Reset your favorites list

#### 4. Settings
- **Items per Page**: Customize how many items display per page
- **Search History**: View and clear your search history
- **Favorites Count**: See how many Pokemon you've favorited

## Examples

### Search for a Pokemon
1. Select "1. Search Pokemon" from main menu
2. Select "1. Search by Name"
3. Enter "pikachu" (or any Pokemon name)
4. View detailed information
5. Add to favorites or explore moves

### Manage Favorites
1. Select "5. My Favorites" from main menu
2. View your saved Pokemon
3. Select a Pokemon to view details
4. Remove Pokemon or clear all favorites

### Customize Settings
1. Select "7. Settings" from main menu
2. Change items per page (5-50)
3. Clear search history
4. View current settings

## Technical Details

### Data Models
- **Enhanced Pokemon Model**: Includes types, abilities, stats, and sprites
- **Type Model**: Type information and effectiveness relationships
- **Ability Model**: Ability details and effects
- **Move Model**: Complete move information

### API Integration
- **Extended PokeAPI Client**: New endpoints for types, abilities, evolution
- **Error Handling**: Graceful fallbacks for API failures
- **Rate Limiting**: Respects PokeAPI rate limits

### Performance
- **Efficient Data Loading**: Loads only necessary information
- **Pagination**: Handles large move lists efficiently
- **Local State**: Maintains user preferences and favorites

## Troubleshooting

### Common Issues

**Import Errors:**
- Make sure you're in the PokeAPI directory
- Activate your virtual environment
- Install dependencies with `pip install -r requirements.txt`

**API Errors:**
- Check your internet connection
- The PokeAPI may be temporarily unavailable
- Some Pokemon names might not exist

**Display Issues:**
- Ensure your terminal supports the characters used
- Try adjusting your terminal window size
- Some terminals may not support screen clearing

### Getting Help
- Check that all dependencies are installed
- Verify you're running from the correct directory
- Try the original script first: `python app/pokeapi.py pikachu`

## Development

### Project Structure
```
PokeAPI/
├── app/
│   ├── models/          # Data models
│   ├── interactive_menu.py  # Main interface
│   └── pokeapi.py       # API client
├── run_explorer.py      # Launcher script
├── requirements.txt     # Dependencies
└── README.md           # This file
```

### Adding New Features
1. **Extend Data Models**: Add new fields to existing models
2. **Update API Client**: Add new endpoints and methods
3. **Enhance Interface**: Add new menu options and functionality
4. **Test Thoroughly**: Ensure new features work correctly

## License

This project uses the PokeAPI which is free to use. Please respect their rate limits and terms of service.

## Contributing

Feel free to enhance the interface, add new features, or improve the user experience. The modular design makes it easy to extend functionality.
