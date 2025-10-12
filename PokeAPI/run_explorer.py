#!/usr/bin/env python3
"""
Pokemon Explorer Launcher
Run this script to start the interactive Pokemon exploration interface.
"""

import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

try:
    from interactive_menu import PokemonExplorer

    print("Starting Pokemon Explorer...")
    print("Loading interactive interface...")

    explorer = PokemonExplorer()
    explorer.run()

except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Make sure you're running this from the PokeAPI directory")
    print("and that all required dependencies are installed.")
    input("Press Enter to exit...")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    input("Press Enter to exit...")
