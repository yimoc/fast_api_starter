from datetime import datetime
from typing import Optional, Generic, TypeVar

from pydantic import BaseModel

from app.core.web.response_base import Meta, Result

DataType = TypeVar("DataType")


class ExceptionResponseDto(BaseModel, Generic[DataType]):
    result: Result
    meta: Optional[Meta]
    data: Optional[DataType]

    class Config:
        json_encoders = {
            datetime: lambda v: v.replace(microsecond=0).isoformat(' ')
        }
