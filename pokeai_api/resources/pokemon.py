from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException, Path, Query
from fastapi_restful import Resource
from pymongo.errors import DuplicateKeyError
from pymongo.results import DeleteResult

from pokeai_api.schemas import (
    Pokemon,
    PokemonBody,
    PokemonUpdateResponse,
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
        pokemon: PokemonBody,
    ) -> Pokemon:
        """Create a Pokémon."""

        pokemon_data: dict[str, Any] = pokemon.dict()

        last_pokemon: PokemonODM = await PokemonODM.find_one(
            sort=[("pokedex_number", -1)]
        )

        pokedex_number: int = (
            last_pokemon.pokedex_number + 1
            if last_pokemon.pokedex_number >= 1000
            else 1000
        )

        pokemon_data["pokedex_number"] = pokedex_number

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
        pokemon: PokemonBody,
        pokedex_number: int = Path(
            ...,
            description="The number of the Pokémon in the Pokédex",
            example=1,
            gt=0,
        ),
    ) -> PokemonUpdateResponse:
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

        await pokemon_odm.set(pokemon_data)

        return PokemonUpdateResponse(updated=True)

    async def patch(
        self,
        pokemon: dict[str, Any],
        pokedex_number: int = Path(
            ...,
            description="The number of the Pokémon in the Pokédex",
            example=1,
            gt=0,
        ),
    ) -> PokemonUpdateResponse:
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

        pokemon.pop("pokedex_number", None)

        pokemon["metadata"] = {
            "custom": True,
            "created_at": pokemon_odm.metadata.created_at,
            "updated_at": datetime.now(timezone.utc),
        }

        await pokemon_odm.set(pokemon)

        return PokemonUpdateResponse(updated=True)

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

        result: DeleteResult | None = await pokemon_odm.delete()

        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to delete Pokémon",
            )

        return PokemonDeleteResponse(
            deleted=result.deleted_count == 1,
        )
