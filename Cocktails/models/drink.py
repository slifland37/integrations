from typing import Annotated, List, Optional

from pydantic import BaseModel, Field


class Drink(BaseModel):
    id: Annotated[str, Field(alias="idDrink")]
    name: Annotated[str, Field(alias="strDrink")]
    tags: Annotated[Optional[str], Field(alias="strTags")] = None
    glass: Annotated[Optional[str], Field(alias="strGlass")] = None


class DrinkList(BaseModel):
    drinks: List[Drink]
