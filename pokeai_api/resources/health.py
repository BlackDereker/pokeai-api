from fastapi_restful import Resource


class Health(Resource):
    def post(self):
        return {"status": "OK"}

    def get(self):
        return {"status": "OK"}
