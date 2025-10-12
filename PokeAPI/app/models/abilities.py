from typing import List

from pydantic import BaseModel


class AbilityRef(BaseModel):
    name: str
    url: str


class AbilityEffect(BaseModel):
    effect: str
    language: dict


class Ability(BaseModel):
    id: int
    name: str
    effect_entries: List[AbilityEffect]
    pokemon: List[dict]  # Pokemon that have this ability
