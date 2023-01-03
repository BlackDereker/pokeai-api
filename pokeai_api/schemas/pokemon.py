from pydantic import BaseModel, Field
from pydantic_factories import ModelFactory


class Pokemon(BaseModel):
    name: str = Field(
        ..., description="The English name of the Pokémon", example="Bulbasaur"
    )
    japanese_name: str = Field(
        ..., description="The Japanese name of the Pokémon", example="フシギダネ"
    )
    pokedex_number: int = Field(
        ..., description="The number of the Pokémon in the Pokédex", example=1
    )
    percentage_male: float = Field(
        ...,
        description=(
            "The percentage of the Pokémon that are males. "
            "Null if the Pokémon is genderless."
        ),
        example=88.1,
    )
    type1: str = Field(
        ..., description="The primary type of the Pokémon", example="Grass"
    )
    type2: str = Field(
        ..., description="The secondary type of the Pokémon", example="Poison"
    )
    classification: str = Field(
        ..., description="The classification of the Pokémon", example="Seed Pokémon"
    )
    height_m: float = Field(
        ..., description="The height of the Pokémon in meters", example=0.7
    )
    weight_kg: float = Field(
        ..., description="The weight of the Pokémon in kilograms", example=6.9
    )
    capture_rate: int = Field(
        ..., description="The base capture rate of the Pokémon", example=45
    )
    base_egg_steps: int = Field(
        ...,
        description=(
            "The base number of steps required to hatch an egg of the Pokémon"
        ),
        example=5120,
    )
    abilities: str = Field(
        ...,
        description="The abilities of the Pokémon",
        example='["Overgrow", "Chlorophyll"]',
    )
    experience_growth: int = Field(
        ..., description="The experience growth of the Pokémon", example=1059860
    )
    base_happiness: int = Field(
        ..., description="The base happiness of the Pokémon", example=70
    )
    against: dict[str, float] = Field(
        ...,
        description="The effectiveness of the Pokémon against other types",
        example={
            "normal": 1.0,
            "fighting": 1.0,
            "flying": 1.0,
            "poison": 1.0,
            "ground": 1.0,
            "rock": 1.0,
            "bug": 1.0,
            "ghost": 1.0,
            "steel": 1.0,
            "fire": 1.0,
            "water": 1.0,
            "grass": 1.0,
            "electric": 1.0,
            "psychic": 1.0,
            "ice": 1.0,
            "dragon": 1.0,
            "dark": 1.0,
            "fairy": 1.0,
        },
    )
    attributes: dict[str, int] = Field(
        ...,
        description="The base attributes of the Pokémon",
        example={
            "hp": 45,
            "attack": 49,
            "defense": 49,
            "sp_attack": 65,
            "sp_defense": 65,
            "speed": 45,
        },
    )
    generation: int = Field(..., description="The generation of the Pokémon", example=1)
    is_legendary: bool = Field(
        ..., description="Whether the Pokémon is legendary", example=False
    )


class PokemonFactory(ModelFactory):
    __model__ = Pokemon
