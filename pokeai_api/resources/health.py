from fastapi_restful import Resource

from pokeai_api.schemas import Health


class Health(Resource):
    def get(self) -> Health:
        return Health(status="ok", message="PokeAI API is running")
