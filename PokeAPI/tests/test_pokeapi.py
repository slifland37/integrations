from app import pokeapi
import responses

class TestGetPokemon:
    @responses.activate
    def test_getpokemon(self):
        responses.add(
            method=responses.GET,
            url='https://pokeapi.co/api/v2/pokemon/bulbasaur',
            json={'id':1, 'name':'bulbasaur'}
        )

        response = pokeapi.get_pokemon('bulbasaur')
        print(response)
        assert response.json() == {'id':1, 'name':'bulbasaur'}



