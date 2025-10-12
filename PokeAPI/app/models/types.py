from typing import List

from pydantic import BaseModel


class TypeRef(BaseModel):
    name: str
    url: str


class TypeEffectiveness(BaseModel):
    double_damage_to: List[TypeRef]
    double_damage_from: List[TypeRef]
    half_damage_to: List[TypeRef]
    half_damage_from: List[TypeRef]
    no_damage_to: List[TypeRef]
    no_damage_from: List[TypeRef]


class Type(BaseModel):
    id: int
    name: str
    damage_relations: TypeEffectiveness
    pokemon: List[dict]  # Pokemon that have this type
