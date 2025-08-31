import argparse
from dataclasses import dataclass
from typing import Callable, Final, List
from urllib.parse import urljoin

import requests
from app.models.pokemon import Move, Pokemon
from app.models.request_params import PaginationParams
from app.models.response_lists import NamedResource, ResourceList
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

BASE_URL: Final = "https://pokeapi.co/api/v2/"


@dataclass(frozen=True)
class Endpoints:
    get_pokemon: Callable[[str], str]
    list_pokemon: str


ENDPOINTS: Final = Endpoints(
    get_pokemon=lambda name: f"pokemon/{name}", list_pokemon="pokemon"
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
    # pokemon = client.get_pokemon(name)
    # if pokemon:
    #     move = client.get_move(pokemon)
    pokemon_list = client.list_pokemon(5)
    for p in pokemon_list:
        print(f"Name: {p.name}; URL: {p.url}")
