from typing import Annotated, List, Optional

from pydantic import BaseModel, Field


class VersionGroupRef(BaseModel):
    name: str
    url: str


class MoveVersionGroupDetails(BaseModel):
    level_learned_at: int
    order: Optional[int] = None  # Allow null/missing values
    version_group: VersionGroupRef


class MoveRef(BaseModel):
    name: str
    url: str


class MoveRefWrapper(BaseModel):
    move: MoveRef
    version_group_details: List[MoveVersionGroupDetails]


class TypeRef(BaseModel):
    name: str
    url: str


class AbilityRef(BaseModel):
    name: str
    url: str


class AbilityWrapper(BaseModel):
    ability: AbilityRef
    is_hidden: bool
    slot: int


class StatRef(BaseModel):
    name: str
    url: str


class Stat(BaseModel):
    base_stat: int
    effort: int
    stat: StatRef


class Pokemon(BaseModel):
    id: int
    name: str
    base_experience: int
    height: int
    weight: int
    types: List[dict]  # Will contain type information
    abilities: List[AbilityWrapper]
    stats: List[Stat]
    moves: List[MoveRefWrapper]
    sprites: dict  # Will contain sprite URLs


class Move(BaseModel):
    id: int
    name: str
    accuracy: Annotated[int, Field(ge=0, le=100)]
    pp: int
    priority: int
    power: int
    type: TypeRef
    damage_class: dict
    effect_entries: List[dict]
