import responses
from app import pokeapi


class TestGetPokemon:
    @responses.activate
    def test_getpokemon(self):
        # TODO@slifland37
        mock_response_payload = {
            "id": 1,
            "name": "bulbasaur",
            "base_experience": 15,
            "height": 10,
            "weight": 100,
            "moves": [
                {"move": {"name": "tackle", "url": "foo"}, "version_group_details": []}
            ],
        }

        responses.add(
            method=responses.GET,
            url="https://pokeapi.co/api/v2/pokemon/bulbasaur",
            json=mock_response_payload,
        )

        response = pokeapi.get_pokemon("bulbasaur")
        assert response.name == "bulbasaur"
        assert response.base_experience == 15
