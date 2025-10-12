import argparse
from dataclasses import dataclass
from typing import Callable, Final, List
from urllib.parse import urljoin

import requests
from app.models.abilities import Ability
from app.models.pokemon import Move, Pokemon
from app.models.request_params import PaginationParams
from app.models.response_lists import NamedResource, ResourceList
from app.models.types import Type
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

BASE_URL: Final = "https://pokeapi.co/api/v2/"


@dataclass(frozen=True)
class Endpoints:
    get_pokemon: Callable[[str], str]
    list_pokemon: str
    get_type: Callable[[str], str]
    get_ability: Callable[[str], str]
    get_evolution_chain: Callable[[str], str]
    get_pokemon_species: Callable[[str], str]


ENDPOINTS: Final = Endpoints(
    get_pokemon=lambda name: f"pokemon/{name}",
    list_pokemon="pokemon",
    get_type=lambda name: f"type/{name}",
    get_ability=lambda name: f"ability/{name}",
    get_evolution_chain=lambda name: f"evolution-chain/{name}",
    get_pokemon_species=lambda name: f"pokemon-species/{name}",
)


class PokeAPI:
    def __init__(self):
        pass

    def get_pokemon(self, name) -> Pokemon:
        url = urljoin(BASE_URL, ENDPOINTS.get_pokemon(name))
        response_dict = self._make_get_request(url)
        pokemon = Pokemon(**response_dict)
        return pokemon

    def get_move(self, pokemon: Pokemon) -> Move:
        url = pokemon.moves[0].move.url
        response_dict = self._make_get_request(url)
        move = Move(**response_dict)
        return move

    def get_type(self, name: str) -> Type:
        """Get type information including effectiveness"""
        url = urljoin(BASE_URL, ENDPOINTS.get_type(name))
        response_dict = self._make_get_request(url)
        type_data = Type(**response_dict)
        return type_data

    def get_ability(self, name: str) -> Ability:
        """Get ability information including effects"""
        url = urljoin(BASE_URL, ENDPOINTS.get_ability(name))
        response_dict = self._make_get_request(url)
        ability = Ability(**response_dict)
        return ability

    def get_evolution_chain(self, chain_id: str):
        """Get evolution chain information"""
        url = urljoin(BASE_URL, ENDPOINTS.get_evolution_chain(chain_id))
        response_dict = self._make_get_request(url)
        return response_dict

    def get_pokemon_species(self, name: str):
        """Get Pokemon species information including evolution details"""
        url = urljoin(BASE_URL, ENDPOINTS.get_pokemon_species(name))
        response_dict = self._make_get_request(url)
        return response_dict

    def list_pokemon(self, count: int = 20) -> List:
        """
        Returns the first n pokemon
        """
        url = urljoin(BASE_URL, ENDPOINTS.list_pokemon)
        params = PaginationParams(limit=count)
        results = []

        while url and len(results) < count:
            response_dict = self._make_get_request(url, params)
            pokemon_list = ResourceList[NamedResource](**response_dict)
            url = pokemon_list.next
            results += pokemon_list.results
            params = None  # Only needed for first request

        return results

    def search_pokemon_by_type(self, type_name: str, limit: int = 20) -> List:
        """Search Pokemon by type"""
        try:
            type_data = self.get_type(type_name)
            pokemon_list = type_data.pokemon[:limit]
            return pokemon_list
        except Exception as e:
            print(f"Error searching Pokemon by type: {e}")
            return []

    def get_random_pokemon(self) -> Pokemon:
        """Get a random Pokemon"""
        import random

        # Get a random ID between 1 and 1000 (most Pokemon are in this range)
        random_id = random.randint(1, 1000)
        try:
            return self.get_pokemon(str(random_id))
        except Exception as e:
            print(f"Error getting random Pokemon: {e}")
            # Fallback to a known Pokemon
            return self.get_pokemon("1")

    def _make_get_request(self, url: str, params: dict | BaseModel = None) -> dict:
        if isinstance(params, BaseModel):
            params = params.model_dump(exclude_none=True)

        try:
            response = requests.get(url=url, params=params)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            print(f"HTTP request failed: {url}")
            raise

        try:
            response_dict = response.json()
        except ValueError:
            print(f"Failed to parse response JSON: {response.text}")
            raise

        return response_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Get a pokemon, along with a list of their moves")
    parser.add_argument("name", help="Provide the name of a pokemon")

    args = parser.parse_args()
    name = args.name
    client = PokeAPI()

    try:
        pokemon = client.get_pokemon(name)
        if pokemon:
            print(f"Found Pokemon: {pokemon.name.title()} (ID: {pokemon.id})")
            print(f"Height: {pokemon.height/10}m")
            print(f"Weight: {pokemon.weight/10}kg")
            print(f"Base Experience: {pokemon.base_experience}")

            # Show types if available
            if hasattr(pokemon, "types") and pokemon.types:
                type_names = [t["type"]["name"].title() for t in pokemon.types]
                print(f"Types: {', '.join(type_names)}")

            # Show stats if available
            if hasattr(pokemon, "stats") and pokemon.stats:
                print("\nBase Stats:")
                for stat in pokemon.stats:
                    stat_name = stat.stat.name.replace("-", " ").title()
                    print(f"  {stat_name}: {stat.base_stat}")

            print(f"\nTotal Moves: {len(pokemon.moves)}")

    except Exception as e:
        print(f"Error: {e}")
        print(
            "Try running the interactive menu instead: python app/interactive_menu.py"
        )
