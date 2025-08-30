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


class Pokemon(BaseModel):
    id: int
    name: str
    base_experience: int
    height: int
    weight: int
    moves: List[MoveRefWrapper]


class Move(BaseModel):
    id: int
    name: str
    accuracy: Annotated[int, Field(ge=0, le=100)]
    pp: int
    priority: int
    power: int
