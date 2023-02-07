from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException, Path, Query, Body
from fastapi_restful import Resource
from pymongo.errors import DuplicateKeyError

from pokeai_api.schemas import (
    Pokemon,
    PokemonPost,
    PokemonUpdate,
    PokemonDeleteResponse,
)
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

        return pokemon_orms

    async def post(
        self,
        pokemon: PokemonPost,
    ) -> Pokemon:
        """Create a Pokémon
        If a Pokémon with the same Pokédex number already exists, a 409 Conflict
        response will be returned.

        For user defined pokémon, the Pokédex number should be greater or equal
        than 1000.
        """

        if pokemon.pokedex_number < 1000:
            raise HTTPException(
                status_code=403,
                detail="Pokédex number must be greater or equal than 1000",
            )

        pokemon_data: dict[str, Any] = pokemon.dict()

        pokemon_data["metadata"] = {
            "custom": True,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }

        try:
            pokemon_odm: PokemonODM = await PokemonODM(**pokemon_data).save()
        except DuplicateKeyError as e:
            raise HTTPException(
                status_code=409,
                detail="Pokémon already exists with that Pokédex number",
            ) from e

        return pokemon_odm


class PokemonDetail(Resource):
    """Resource for getting, updating, and deleting Pokémon"""

    async def get(
        self,
        pokedex_number: int = Path(
            ...,
            description="The number of the Pokémon in the Pokédex",
            example=1,
            gt=0,
        ),
    ) -> Pokemon:
        """Get a Pokémon by its Pokédex number"""
        pokemon_odm: PokemonODM = await PokemonODM.find_one(
            {"pokedex_number": pokedex_number}
        )

        if not pokemon_odm:
            raise PokemonNotFound(pokedex_number)

        return pokemon_odm

    async def put(
        self,
        pokedex_number: int = Path(
            ...,
            description="The number of the Pokémon in the Pokédex",
            example=1,
            gt=0,
        ),
        pokemon: PokemonUpdate = Body(
            ...,
            description="The Pokémon to fully update",
        ),
    ) -> Pokemon:
        """Fully Update a Pokémon by its Pokédex number"""

        if pokedex_number < 1000:
            raise HTTPException(
                status_code=403,
                detail="Pokédex number must be greater or equal than 1000",
            )

        pokemon_odm: PokemonODM = await PokemonODM.find_one(
            {"pokedex_number": pokedex_number}
        )

        if not pokemon_odm:
            raise PokemonNotFound(pokedex_number)

        pokemon_data: dict[str, Any] = pokemon.dict()

        pokemon_data["metadata"] = {
            "custom": True,
            "created_at": pokemon_odm.metadata.created_at,
            "updated_at": datetime.now(timezone.utc),
        }

        updated_pokemon: Pokemon = await pokemon_odm.update(**pokemon_data)

        return updated_pokemon

    async def patch(
        self,
        pokedex_number: int = Path(
            ...,
            description="The number of the Pokémon in the Pokédex",
            example=1,
            gt=0,
        ),
        pokemon: Pokemon = Body(
            ...,
            description="The Pokémon to partially update",
        ),
    ) -> Pokemon:
        """Partially Update a Pokémon by its Pokédex number"""

        if pokedex_number < 1000:
            raise HTTPException(
                status_code=403,
                detail="Pokédex number must be greater or equal than 1000",
            )

        pokemon_odm: PokemonODM = await PokemonODM.find_one(
            {"pokedex_number": pokedex_number}
        )

        if not pokemon_odm:
            raise PokemonNotFound(pokedex_number)

        pokemon_data: dict[str, Any] = pokemon.dict()

        pokemon_data["metadata"] = {
            "custom": True,
            "created_at": pokemon_odm.metadata.created_at,
            "updated_at": datetime.now(timezone.utc),
        }

        updated_pokemon: Pokemon = await pokemon_odm.update(
            **pokemon_data(exclude_unset=True)
        )

        return updated_pokemon

    async def delete(
        self,
        pokedex_number: int = Path(
            ...,
            description="The number of the Pokémon in the Pokédex",
            example=1,
            gt=0,
        ),
    ) -> PokemonDeleteResponse:
        """Delete a Pokémon by its Pokédex number"""

        if pokedex_number < 1000:
            raise HTTPException(
                status_code=403,
                detail="Pokédex number must be greater or equal than 1000",
            )

        pokemon_odm: PokemonODM = await PokemonODM.find_one(
            {"pokedex_number": pokedex_number}
        )

        if not pokemon_odm:
            raise PokemonNotFound(pokedex_number)

        await pokemon_odm.delete()

        return PokemonDeleteResponse(
            deleted=True,
        )
