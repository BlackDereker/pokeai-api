from fastapi_restful import Resource

from pokeai_api.schemas import Pokemon
from pokeai_api.schemas.pokemon import PokemonFactory  # TODO temporary


class PokemonDetail(Resource):
    def get(self, pokedex_number: int) -> Pokemon:
        pokemon: Pokemon = PokemonFactory.build()
        pokemon.pokedex_number = pokedex_number
        return pokemon
