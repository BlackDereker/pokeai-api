from fastapi import HTTPException, Path, Query, Body
from fastapi_restful import Resource
from pymongo.errors import DuplicateKeyError

from pokeai_api.schemas import Pokemon
from pokeai_api.models import PokemonODM
from pokeai_api.resources.exceptions import PokemonNotFound


class PokemonList(Resource):
    """Resource for listing and creating Pokémon"""

    async def get(
        self,
        skip: int = Query(
            0,
            description="The number of Pokémon to skip",
            ge=0,
            example=0,
        ),
        limit: int
        | None = Query(
            20,
            description="The maximum number of Pokémon to return",
            gt=0,
            example=20,
        ),
    ) -> list[Pokemon]:
        """List all Pokémon"""
        pokemon_orms: list[PokemonODM] = await PokemonODM.find_all(
            skip=skip,
            limit=limit,
        ).to_list()

        return [Pokemon.from_orm(pokemon_orm) for pokemon_orm in pokemon_orms]

    async def post(
        self,
        pokemon: Pokemon,
    ) -> Pokemon:
        """Create a Pokémon"""
        try:
            pokemon_orm: PokemonODM = await PokemonODM(**pokemon.dict()).save()
        except DuplicateKeyError:
            raise HTTPException(
                status_code=409,
                detail="Pokémon already exists with that Pokédex number",
            )

        return Pokemon.from_orm(pokemon_orm)


class PokemonDetail(Resource):
    """Resource for getting, updating, and deleting Pokémon"""

    async def get(
        self,
        pokedex_number: int = Path(
            ...,
            description="The number of the Pokémon in the Pokédex",
            example=1,
            gt=0,
            lt=803,
        ),
    ) -> Pokemon:
        """Get a Pokémon by its Pokédex number"""
        pokemon_odm: PokemonODM = await PokemonODM.find_one(
            {"pokedex_number": pokedex_number}
        )

        if not pokemon_odm:
            raise PokemonNotFound(pokedex_number)

        return Pokemon.from_orm(pokemon_odm)

    async def put(
        self,
        pokedex_number: int = Path(
            ...,
            description="The number of the Pokémon in the Pokédex",
            example=1,
            gt=0,
            lt=803,
        ),
        pokemon: Pokemon = Body(
            ...,
            description="The Pokémon to fully update",
        ),
    ) -> Pokemon:
        """Fully Update a Pokémon by its Pokédex number"""
        pokemon_odm: PokemonODM = await PokemonODM.find_one(
            {"pokedex_number": pokedex_number}
        )

        if not pokemon_odm:
            raise PokemonNotFound(pokedex_number)

        updated_pokemon: Pokemon = await pokemon_odm.update(**pokemon.dict())

        return Pokemon.from_orm(updated_pokemon)

    async def patch(
        self,
        pokedex_number: int = Path(
            ...,
            description="The number of the Pokémon in the Pokédex",
            example=1,
            gt=0,
            lt=803,
        ),
        pokemon: Pokemon = Body(
            ...,
            description="The Pokémon to partially update",
        ),
    ) -> Pokemon:
        """Partially Update a Pokémon by its Pokédex number"""
        pokemon_odm: PokemonODM = await PokemonODM.find_one(
            {"pokedex_number": pokedex_number}
        )

        if not pokemon_odm:
            raise PokemonNotFound(pokedex_number)

        updated_pokemon: Pokemon = await pokemon_odm.update(
            **pokemon.dict(exclude_unset=True)
        )

        return Pokemon.from_orm(updated_pokemon)

    async def delete(
        self,
        pokedex_number: int = Path(
            ...,
            description="The number of the Pokémon in the Pokédex",
            example=1,
            gt=0,
            lt=803,
        ),
    ) -> Pokemon:
        """Delete a Pokémon by its Pokédex number"""
        pokemon_odm: PokemonODM = await PokemonODM.find_one(
            {"pokedex_number": pokedex_number}
        )

        if not pokemon_odm:
            raise PokemonNotFound(pokedex_number)

        await pokemon_odm.delete()

        return {"message": "Pokémon deleted successfully"}
