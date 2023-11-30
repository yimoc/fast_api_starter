import logging

from fastapi import APIRouter

from app.core.web.response_base import Result, Meta, SodaflowResponseBase

from app.api.api_router import api_router
from fastapi import status


logger = logging.getLogger(__name__)

root_router = APIRouter()

@root_router.get("/health",
             status_code=status.HTTP_200_OK,
             response_model=SodaflowResponseBase, include_in_schema=True)
def request_health():
    data = dict(result = 'healthy')
    result = Result()
    meta = Meta(version='v1')
    response_data = SodaflowResponseBase[dict](data=data, result=result, meta=meta)
    return response_data


root_router.include_router(api_router, prefix="/api")
