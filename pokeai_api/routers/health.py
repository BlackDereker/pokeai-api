from pokeai_api.resources import HealthResource
from pokeai_api.routers import ResourceRouter

router = ResourceRouter(prefix="/health", tags=["health"])

router.add_resource(HealthResource, "/")
