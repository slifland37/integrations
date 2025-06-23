import requests
from dotenv import load_dotenv
from urllib.parse import urljoin
from dataclasses import dataclass
from typing import Final, Callable
import argparse
from models.pokemon import Pokemon, Move

load_dotenv()

BASE_URL: Final = "https://pokeapi.co/api/v2/"

@dataclass(frozen=True)
class Endpoints:
    pokemon: Callable[[str], str]

ENDPOINTS: Final = Endpoints(
    pokemon=lambda name: f"pokemon/{name}",
)

def get_pokemon(name):
    url = urljoin(BASE_URL, ENDPOINTS.pokemon(name))
    print(url)
    response = requests.get(
        url=url
    )
    response_dict = response.json()
    pokemon = Pokemon(**response_dict)
    print(f"Fetched pokemon: {pokemon.name}, ({pokemon.id:03})")
    print(f"Getting move...")
    get_move(pokemon)

def get_move(pokemon: Pokemon):
    url = pokemon.moves[0].move.url
    print(f"move_url: {url}")
    response = requests.get(url=url)
    move = Move(**response.json())
    print(f"Fetched move: {move.name} ({move.id})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Get a pokemon, along with a list of their moves")
    parser.add_argument("name", help="Provide the name of a pokemon")

    args = parser.parse_args()
    name = args.name
    get_pokemon(name)