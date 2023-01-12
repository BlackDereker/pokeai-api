from fastapi_restful.api_model import APIModel
from pydantic import BaseModel, Field


class Against(BaseModel):
    bug: float = Field(
        default=1.0,
        description="The effectiveness of Bug-type moves",
        example=1.0,
        ge=0.0,
    )
    dark: float = Field(
        default=1.0,
        description="The effectiveness of Dark-type moves",
        example=1.0,
        ge=0.0,
    )
    dragon: float = Field(
        default=1.0,
        description="The effectiveness of Dragon-type moves",
        example=1.0,
        ge=0.0,
    )
    electric: float = Field(
        default=1.0,
        description="The effectiveness of Electric-type moves",
        example=1.0,
        ge=0.0,
    )
    fairy: float = Field(
        default=1.0,
        description="The effectiveness of Fairy-type moves",
        example=1.0,
        ge=0.0,
    )
    fight: float = Field(
        default=1.0,
        description="The effectiveness of Fighting-type moves",
        example=1.0,
        ge=0.0,
    )
    fire: float = Field(
        default=1.0,
        description="The effectiveness of Fire-type moves",
        example=1.0,
        ge=0.0,
    )
    flying: float = Field(
        default=1.0,
        description="The effectiveness of Flying-type moves",
        example=1.0,
        ge=0.0,
    )
    ghost: float = Field(
        default=1.0,
        description="The effectiveness of Ghost-type moves",
        example=1.0,
        ge=0.0,
    )
    grass: float = Field(
        default=1.0,
        description="The effectiveness of Grass-type moves",
        example=1.0,
        ge=0.0,
    )
    ground: float = Field(
        default=1.0,
        description="The effectiveness of Ground-type moves",
        example=1.0,
        ge=0.0,
    )
    ice: float = Field(
        default=1.0,
        description="The effectiveness of Ice-type moves",
        example=1.0,
        ge=0.0,
    )
    normal: float = Field(
        default=1.0,
        description="The effectiveness of Normal-type moves",
        example=1.0,
        ge=0.0,
    )
    poison: float = Field(
        default=1.0,
        description="The effectiveness of Poison-type moves",
        example=1.0,
        ge=0.0,
    )
    psychic: float = Field(
        default=1.0,
        description="The effectiveness of Psychic-type moves",
        example=1.0,
        ge=0.0,
    )
    rock: float = Field(
        default=1.0,
        description="The effectiveness of Rock-type moves",
        example=1.0,
        ge=0.0,
    )
    steel: float = Field(
        default=1.0,
        description="The effectiveness of Steel-type moves",
        example=1.0,
        ge=0.0,
    )
    water: float = Field(
        default=1.0,
        description="The effectiveness of Water-type moves",
        example=1.0,
        ge=0.0,
    )


class Attributes(BaseModel):
    hp: int = Field(
        ...,
        description="The base HP of the Pokémon",
        example=45,
        ge=1,
    )
    attack: int = Field(
        ...,
        description="The base Attack of the Pokémon",
        example=49,
        ge=0,
    )
    defense: int = Field(
        ...,
        description="The base Defense of the Pokémon",
        example=49,
        ge=0,
    )
    sp_attack: int = Field(
        ...,
        description="The base Special Attack of the Pokémon",
        example=65,
        ge=0,
    )
    sp_defense: int = Field(
        ...,
        description="The base Special Defense of the Pokémon",
        example=65,
        ge=0,
    )
    speed: int = Field(
        ...,
        description="The base Speed of the Pokémon",
        example=45,
        ge=0,
    )


class Pokemon(APIModel):
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
    type2: str | None = Field(
        ..., description="The secondary type of the Pokémon", example="Poison"
    )
    classification: str = Field(
        ..., description="The classification of the Pokémon", example="Seed Pokémon"
    )
    height_m: float | None = Field(
        ..., description="The height of the Pokémon in meters", example=0.7
    )
    weight_kg: float | None = Field(
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
    abilities: list[str] = Field(
        ...,
        description="The abilities of the Pokémon",
        example=["Overgrow", "Chlorophyll"],
    )
    experience_growth: int = Field(
        ..., description="The experience growth of the Pokémon", example=1059860
    )
    base_happiness: int = Field(
        ..., description="The base happiness of the Pokémon", example=70
    )
    against: Against = Field(
        ...,
        description="The effectiveness of the Pokémon against other types",
        example={
            "normal": 1.0,
            "fight": 1.0,
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
    attributes: Attributes = Field(
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
