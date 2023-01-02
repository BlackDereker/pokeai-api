from typing import Type
from fastapi_restful import Resource
from fastapi_restful.cbv import _cbv
from fastapi_restful.inferring_router import InferringRouter


class ResourceRouter(InferringRouter):
    def add_resource(self, resource: Type[Resource], *urls: str) -> None:
        _cbv(self, resource, *urls, instance=resource())
