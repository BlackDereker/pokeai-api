from beanie import Document, Indexed
from pydantic import BaseModel


class Against(BaseModel):
    type: str
    value: float


class Attributes(BaseModel):
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int


class PokemonORM(Document):
    name: str
    japanese_name: str
    pokedex_number: Indexed(int)
    percentage_male: float
    type1: str
    type2: str | None
    classification: str
    height_m: float
    weight_kg: float
    capture_rate: int
    base_egg_steps: int
    abilities: list[str]
    experience_growth: int
    base_happiness: int
    against: Against
    attributes: Attributes
    generation: int
    is_legendary: bool
