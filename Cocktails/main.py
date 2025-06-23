import requests
from urllib.parse import urljoin
from models.drink import Drink, DrinkList


API_KEY = '1' # dev API key
SEARCH_URL = f"https://www.thecocktaildb.com/api/json/v1/{API_KEY}/search.php"
FILTER_URL = f"https://www.thecocktaildb.com/api/json/v1/{API_KEY}/filter.php"
def search_cocktail_by_name(name):
    response = requests.get(
        url=SEARCH_URL,
        params={
            's': name
        }
    )
    r_dict = response.json()
    d_list = DrinkList(**r_dict)
    for d in d_list.drinks:
        print(f"Mmm... a tasty {d.name}.")

def search_by_ingredient(ingredient_name):
    response = requests.get(
        url=FILTER_URL,
        params={
            'i':ingredient_name
        }
    )
    r_dict = response.json()
    d_list = DrinkList(**r_dict)
    for d in d_list.drinks[:5]:
        print(f"I love me a {d.name}")

if __name__ == "__main__":
    # search_cocktail_by_name("manhattan")
    search_by_ingredient('Gin')