from pydantic import BaseModel
from typing import Literal


class Health(BaseModel):
    status: Literal["ok"]
    message: str

    class Config:
        schema_extra = {
            "example": {
                "status": "ok",
                "message": "PokeAI API is running",
            }
        }
