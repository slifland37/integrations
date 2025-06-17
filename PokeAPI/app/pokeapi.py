import requests
from dotenv import load_dotenv
from urllib.parse import urljoin
from types import MappingProxyType
from dataclasses import dataclass
from typing import Final, Callable

load_dotenv()

BASE_URL: Final = "https://pokeapi.co/api/v2/"

@dataclass(frozen=True)
class Endpoints:
    pokemon: Callable[[str], str]
    moves: Callable[[str], str]

ENDPOINTS: Final = Endpoints(
    pokemon=lambda name: f"pokemon/{name}",
    moves=lambda name: f"move/{name}"
)

def get_pokemon(name):
    url = urljoin(BASE_URL, ENDPOINTS.pokemon(name))
    print(url)
    response = requests.get(
        url=url
    )
    return response

if __name__ == "__main__":
    get_pokemon("bulbasaur")