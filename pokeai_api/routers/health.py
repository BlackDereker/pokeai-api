from pokeai_api.resources.health import Health
from pokeai_api.routers import ResourceRouter

router = ResourceRouter(prefix="/health", tags=["health"])

router.add_resource(Health, "/")
