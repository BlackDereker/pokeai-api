from fastapi import HTTPException


class PokemonNotFound(HTTPException):
    def __init__(self, pokedex_number: int):
        super().__init__(
            status_code=404,
            detail=f"Pokémon with Pokédex number {pokedex_number} not found",
        )
