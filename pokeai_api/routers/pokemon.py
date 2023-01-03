from pokeai_api.resources import PokemonDetail
from pokeai_api.routers import ResourceRouter

router = ResourceRouter(prefix="/pokemon/{pokedex_number}", tags=["pokemon"])

router.add_resource(PokemonDetail, "/")
