from beanie import Document, Indexed

from pokeai_api.schemas.pokemon import Against, Attributes


class PokemonODM(Document):
    """ODM for Pokémon"""

    name: str
    japanese_name: str
    pokedex_number: Indexed(int, unique=True)
    percentage_male: float
    type1: str
    type2: str | None
    classification: str
    height_m: float | None
    weight_kg: float | None
    capture_rate: int
    base_egg_steps: int
    abilities: list[str]
    experience_growth: int
    base_happiness: int
    against: Against
    attributes: Attributes
    generation: int
    is_legendary: bool

    class Settings:
        name = "pokemons"
