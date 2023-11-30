from pydantic import BaseModel
from typing import Union


class ItemDto(BaseModel):
    id : int
    name: str
    price: float
    description: Union[str, None] = None

    class Config:
        from_attributes = True

# https://fastapi.tiangolo.com/tutorial/sql-databases/
# Usage
# dict -> Model
# MyModel.parse_obj(my_dict)
# Model -> dict : https://pydantic-docs.helpmanual.io/usage/exporting_models/
# MyModel.dict()

