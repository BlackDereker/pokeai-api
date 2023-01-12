from pokeai_api.resources import PokemonList, PokemonDetail
from pokeai_api.routers import ResourceRouter

router = ResourceRouter(prefix="/pokemon", tags=["pokemon"])

router.add_resource(PokemonList, "/")
router.add_resource(PokemonDetail, "/{pokedex_number}")
