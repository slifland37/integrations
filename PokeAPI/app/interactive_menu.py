import os
from typing import List

from models.pokemon import Pokemon

from pokeapi import PokeAPI


class PokemonExplorer:
    def __init__(self):
        self.api = PokeAPI()
        self.favorites: List[str] = []
        self.search_history: List[str] = []
        self.current_page = 1
        self.items_per_page = 20

    def clear_screen(self):
        """Clear the console screen using a more reliable method"""
        # Print multiple newlines to clear the visible area
        print("\n" * 100)

        # For Windows, also try the cls command as backup
        if os.name == "nt":
            os.system("cls")

    def print_header(self):
        """Print the application header"""
        print("=" * 50)
        print("           POKEMON EXPLORER")
        print("=" * 50)
        print()

    def print_menu(self):
        """Display the main menu"""
        self.clear_screen()
        self.print_header()
        print("Main Menu:")
        print("1. Search Pokemon")
        print("2. Browse by Type")
        print("3. Browse by Generation")
        print("4. Random Pokemon")
        print("5. My Favorites")
        print("6. Pokemon Quiz")
        print("7. Settings")
        print("8. Exit")
        print()

    def get_user_choice(self, min_choice: int, max_choice: int) -> int:
        """Get and validate user input"""
        while True:
            try:
                choice = input(
                    f"Enter your choice ({min_choice}-{max_choice}): "
                ).strip()
                choice_num = int(choice)
                if min_choice <= choice_num <= max_choice:
                    return choice_num
                else:
                    print(
                        f"Please enter a number between {min_choice} and {max_choice}"
                    )
            except ValueError:
                print("Please enter a valid number")

    def search_pokemon_menu(self):
        """Handle Pokemon search functionality"""
        while True:
            self.clear_screen()
            self.print_header()
            print("Search Pokemon:")
            print("1. Search by Name")
            print("2. Search by Type")
            print("3. Search by Generation")
            print("4. Back to Main Menu")
            print()

            choice = self.get_user_choice(1, 4)

            if choice == 1:
                self.search_by_name()
            elif choice == 2:
                self.search_by_type()
            elif choice == 3:
                self.search_by_generation()
            elif choice == 4:
                break

    def search_by_name(self):
        """Search Pokemon by name"""
        self.clear_screen()
        self.print_header()
        print("Search Pokemon by Name")
        print("-" * 30)

        name = input("Enter Pokemon name (or partial name): ").strip().lower()
        if not name:
            input("Name cannot be empty. Press Enter to continue...")
            return

        try:
            # Add to search history
            if name not in self.search_history:
                self.search_history.insert(0, name)
                if len(self.search_history) > 10:  # Keep only last 10 searches
                    self.search_history.pop()

            # Search for Pokemon
            pokemon = self.api.get_pokemon(name)
            self.display_pokemon_details(pokemon)

        except Exception as e:
            print(f"Error searching for Pokemon: {e}")
            input("Press Enter to continue...")

    def search_by_type(self):
        """Search Pokemon by type"""
        self.clear_screen()
        self.print_header()
        print("Search Pokemon by Type")
        print("-" * 30)

        # Common Pokemon types
        types = [
            "normal",
            "fire",
            "water",
            "electric",
            "grass",
            "ice",
            "fighting",
            "poison",
            "ground",
            "flying",
            "psychic",
            "bug",
            "rock",
            "ghost",
            "dragon",
            "dark",
            "steel",
            "fairy",
        ]

        print("Available types:")
        for i, type_name in enumerate(types, 1):
            print(f"{i:2d}. {type_name.title()}")
        print()

        try:
            choice = self.get_user_choice(1, len(types))
            selected_type = types[choice - 1]

            print(f"\nSearching for {selected_type.title()} type Pokemon...")
            # This would need to be implemented in the API client
            # For now, we'll show a placeholder
            print(
                f"Feature coming soon: Browse Pokemon by {selected_type.title()} type"
            )

        except Exception as e:
            print(f"Error: {e}")

        input("Press Enter to continue...")

    def search_by_generation(self):
        """Search Pokemon by generation"""
        self.clear_screen()
        self.print_header()
        print("Search Pokemon by Generation")
        print("-" * 30)

        generations = [
            "Generation I (Red/Blue)",
            "Generation II (Gold/Silver)",
            "Generation III (Ruby/Sapphire)",
            "Generation IV (Diamond/Pearl)",
            "Generation V (Black/White)",
            "Generation VI (X/Y)",
            "Generation VII (Sun/Moon)",
            "Generation VIII (Sword/Shield)",
            "Generation IX (Scarlet/Violet)",
        ]

        print("Available generations:")
        for i, gen in enumerate(generations, 1):
            print(f"{i}. {gen}")
        print()

        try:
            choice = self.get_user_choice(1, len(generations))
            selected_gen = generations[choice - 1]

            print(f"\nSearching for Pokemon from {selected_gen}...")
            # This would need to be implemented in the API client
            print(f"Feature coming soon: Browse Pokemon by {selected_gen}")

        except Exception as e:
            print(f"Error: {e}")

        input("Press Enter to continue...")

    def display_pokemon_details(self, pokemon: Pokemon):
        """Display detailed Pokemon information"""
        while True:
            self.clear_screen()
            self.print_header()

            # Pokemon header
            print(f"Pokemon: {pokemon.name.title()} (ID: {pokemon.id})")
            print("=" * 40)

            # Basic info
            print(f"Height: {pokemon.height/10}m")
            print(f"Weight: {pokemon.weight/10}kg")
            print(f"Base Experience: {pokemon.base_experience}")

            # Types
            if hasattr(pokemon, "types") and pokemon.types:
                type_names = [t["type"]["name"].title() for t in pokemon.types]
                print(f"Types: {', '.join(type_names)}")

            # Stats
            if hasattr(pokemon, "stats") and pokemon.stats:
                print("\nBase Stats:")
                for stat in pokemon.stats:
                    stat_name = stat.stat.name.replace("-", " ").title()
                    print(f"  {stat_name}: {stat.base_stat}")

            # Abilities
            if hasattr(pokemon, "abilities") and pokemon.abilities:
                print("\nAbilities:")
                for ability in pokemon.abilities:
                    hidden = " (Hidden)" if ability.is_hidden else ""
                    print(f"  {ability.ability.name.title()}{hidden}")

            # Moves count
            if hasattr(pokemon, "moves") and pokemon.moves:
                print(f"\nTotal Moves: {len(pokemon.moves)}")

            print("\n" + "=" * 40)
            print("1. View Moves")
            print("2. View Evolution")
            print("3. Add to Favorites")
            print("4. Back to Search")
            print("5. Back to Main Menu")
            print()

            choice = self.get_user_choice(1, 5)

            if choice == 1:
                self.display_pokemon_moves(pokemon)
            elif choice == 2:
                self.display_pokemon_evolution(pokemon)
            elif choice == 3:
                self.add_to_favorites(pokemon.name)
            elif choice == 4:
                break
            elif choice == 5:
                return

    def display_pokemon_moves(self, pokemon: Pokemon):
        """Display Pokemon moves"""
        self.clear_screen()
        self.print_header()
        print(f"Moves for {pokemon.name.title()}")
        print("=" * 40)

        if not hasattr(pokemon, "moves") or not pokemon.moves:
            print("No moves available for this Pokemon.")
            input("Press Enter to continue...")
            return

        # Show first 20 moves with pagination
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        moves_to_show = pokemon.moves[start_idx:end_idx]

        for i, move_wrapper in enumerate(moves_to_show, start_idx + 1):
            move_name = move_wrapper.move.name.replace("-", " ").title()
            print(f"{i:3d}. {move_name}")

        # Pagination controls
        total_pages = (
            len(pokemon.moves) + self.items_per_page - 1
        ) // self.items_per_page
        if total_pages > 1:
            print(f"\nPage {self.current_page} of {total_pages}")
            print("n: Next page, p: Previous page, q: Quit")

            while True:
                nav = input("Navigation: ").strip().lower()
                if nav == "n" and self.current_page < total_pages:
                    self.current_page += 1
                    break
                elif nav == "p" and self.current_page > 1:
                    self.current_page -= 1
                    break
                elif nav == "q":
                    break
                else:
                    print("Invalid navigation. Use n/p/q")

        input("Press Enter to continue...")

    def display_pokemon_evolution(self, pokemon: Pokemon):
        """Display Pokemon evolution information"""
        self.clear_screen()
        self.print_header()
        print(f"Evolution for {pokemon.name.title()}")
        print("=" * 40)

        # This would need to be implemented in the API client
        print("Evolution information coming soon!")
        print("This feature will show the evolution chain for this Pokemon.")

        input("Press Enter to continue...")

    def add_to_favorites(self, pokemon_name: str):
        """Add Pokemon to favorites"""
        if pokemon_name not in self.favorites:
            self.favorites.append(pokemon_name)
            print(f"{pokemon_name.title()} added to favorites!")
        else:
            print(f"{pokemon_name.title()} is already in your favorites!")

        input("Press Enter to continue...")

    def browse_by_type_menu(self):
        """Browse Pokemon by type"""
        self.clear_screen()
        self.print_header()
        print("Browse Pokemon by Type")
        print("-" * 30)
        print("Feature coming soon!")
        print("This will allow you to browse all Pokemon of a specific type.")
        input("Press Enter to continue...")

    def browse_by_generation_menu(self):
        """Browse Pokemon by generation"""
        self.clear_screen()
        self.print_header()
        print("Browse Pokemon by Generation")
        print("-" * 30)
        print("Feature coming soon!")
        print("This will allow you to browse Pokemon by game generation.")
        input("Press Enter to continue...")

    def random_pokemon_menu(self):
        """Show random Pokemon"""
        self.clear_screen()
        self.print_header()
        print("Random Pokemon")
        print("-" * 30)
        print("Feature coming soon!")
        print("This will show you a random Pokemon to discover.")
        input("Press Enter to continue...")

    def favorites_menu(self):
        """Manage favorites"""
        while True:
            self.clear_screen()
            self.print_header()
            print("My Favorites")
            print("-" * 30)

            if not self.favorites:
                print("You haven't added any Pokemon to favorites yet.")
                print("Search for Pokemon and add them to see them here!")
            else:
                print("Your favorite Pokemon:")
                for i, pokemon_name in enumerate(self.favorites, 1):
                    print(f"{i}. {pokemon_name.title()}")

                print(f"\nTotal favorites: {len(self.favorites)}")

            print("\n1. View Pokemon Details")
            print("2. Remove from Favorites")
            print("3. Clear All Favorites")
            print("4. Back to Main Menu")
            print()

            choice = self.get_user_choice(1, 4)

            if choice == 1 and self.favorites:
                self.view_favorite_details()
            elif choice == 2 and self.favorites:
                self.remove_from_favorites()
            elif choice == 3:
                self.clear_favorites()
            elif choice == 4:
                break

    def view_favorite_details(self):
        """View details of a favorite Pokemon"""
        print("\nEnter the number of the Pokemon to view:")
        try:
            choice = self.get_user_choice(1, len(self.favorites))
            pokemon_name = self.favorites[choice - 1]
            pokemon = self.api.get_pokemon(pokemon_name)
            self.display_pokemon_details(pokemon)
        except Exception as e:
            print(f"Error loading Pokemon: {e}")
            input("Press Enter to continue...")

    def remove_from_favorites(self):
        """Remove a Pokemon from favorites"""
        print("\nEnter the number of the Pokemon to remove:")
        try:
            choice = self.get_user_choice(1, len(self.favorites))
            pokemon_name = self.favorites[choice - 1]
            self.favorites.pop(choice - 1)
            print(f"{pokemon_name.title()} removed from favorites!")
            input("Press Enter to continue...")
        except Exception as e:
            print(f"Error: {e}")
            input("Press Enter to continue...")

    def clear_favorites(self):
        """Clear all favorites"""
        confirm = (
            input("Are you sure you want to clear all favorites? (y/N): ")
            .strip()
            .lower()
        )
        if confirm == "y":
            self.favorites.clear()
            print("All favorites cleared!")
        input("Press Enter to continue...")

    def quiz_menu(self):
        """Pokemon quiz system"""
        self.clear_screen()
        self.print_header()
        print("Pokemon Quiz")
        print("-" * 30)
        print("Feature coming soon!")
        print("This will include interactive quizzes about Pokemon.")
        input("Press Enter to continue...")

    def settings_menu(self):
        """Application settings"""
        while True:
            self.clear_screen()
            self.print_header()
            print("Settings")
            print("-" * 30)
            print(f"Items per page: {self.items_per_page}")
            print(f"Search history entries: {len(self.search_history)}")
            print(f"Favorites count: {len(self.favorites)}")
            print()
            print("1. Change items per page")
            print("2. Clear search history")
            print("3. Back to Main Menu")
            print()

            choice = self.get_user_choice(1, 3)

            if choice == 1:
                self.change_items_per_page()
            elif choice == 2:
                self.clear_search_history()
            elif choice == 3:
                break

    def change_items_per_page(self):
        """Change the number of items displayed per page"""
        print(f"\nCurrent items per page: {self.items_per_page}")
        try:
            new_count = int(input("Enter new items per page (5-50): "))
            if 5 <= new_count <= 50:
                self.items_per_page = new_count
                print(f"Items per page changed to {new_count}")
            else:
                print("Please enter a number between 5 and 50")
        except ValueError:
            print("Please enter a valid number")
        input("Press Enter to continue...")

    def clear_search_history(self):
        """Clear search history"""
        confirm = (
            input("Are you sure you want to clear search history? (y/N): ")
            .strip()
            .lower()
        )
        if confirm == "y":
            self.search_history.clear()
            print("Search history cleared!")
        input("Press Enter to continue...")

    def run(self):
        """Main application loop"""
        while True:
            self.print_menu()
            choice = self.get_user_choice(1, 8)

            if choice == 1:
                self.search_pokemon_menu()
            elif choice == 2:
                self.browse_by_type_menu()
            elif choice == 3:
                self.browse_by_generation_menu()
            elif choice == 4:
                self.random_pokemon_menu()
            elif choice == 5:
                self.favorites_menu()
            elif choice == 6:
                self.quiz_menu()
            elif choice == 7:
                self.settings_menu()
            elif choice == 8:
                print("\nThank you for using Pokemon Explorer!")
                break


if __name__ == "__main__":
    explorer = PokemonExplorer()
    try:
        explorer.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        input("Press Enter to exit...")
