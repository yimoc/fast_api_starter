from datetime import datetime
from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel
from strenum import StrEnum

#Response code
class ResponseResult(StrEnum):
    OK = "ok"
    FAIL = "fail"

# Reponse Data
DataType = TypeVar("DataType")

# Response Meta Data
class Meta(BaseModel):
    version: str = None

# Reponse result
class Result(BaseModel):
    code: str = ResponseResult.OK    # 'ok | fail'
    message : str = "success"


class SodaflowResponseBase(BaseModel, Generic[DataType]):
    result : Result
    meta : Optional[Meta]
    data: Optional[DataType]

    class Config:
        json_encoders = {
            datetime: lambda v: v.replace(microsecond=0).isoformat(' ')
        }


# https://pydantic-docs.helpmanual.io/usage/models/#generic-models
# https://stackoverflow.com/questions/73136859/decorate-response-model-of-a-fastapi-route-with-another-model
# https://stackoverflow.com/questions/69507122/fastapi-custom-response-model