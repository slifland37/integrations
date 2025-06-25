from pydantic import BaseModel
from typing import Optional, List

class NamedResource(BaseModel):
    name: str
    url: str

class UnnamedResource(BaseModel):
    url: str

class NamedResourceList(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[NamedResource]

class UnnamedResourceList(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[UnnamedResource]