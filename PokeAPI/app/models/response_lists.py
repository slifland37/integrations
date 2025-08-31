from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel


class UnnamedResource(BaseModel):
    url: str


class NamedResource(UnnamedResource):
    name: str


T = TypeVar("T", bound=UnnamedResource)


class ResourceList(BaseModel, Generic[T]):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[T]
