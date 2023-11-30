import http
import logging

from fastapi.utils import is_body_allowed_for_status_code
from fastapi.encoders import jsonable_encoder
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.core.exception.exception_response_dto import ExceptionResponseDto
from app.core.exception.exceptions import SodaflowResponseError, SodaflowError
from app.core.web.response_base import Result, Meta

logger = logging.getLogger()

async def default_exception_handler(request, err):
    logging.critical(err, exc_info=True)
    base_error_message = f"Failed to execute: {request.method}: {request.url}"

    result = Result(code='Undefined Error', message=f"{base_error_message}. Detail: {err}")
    meta = Meta(version='v1')
    response = ExceptionResponseDto(result=result, meta=meta, data=dict())
    return JSONResponse(
        status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(response)
    )

async def sodaflow_default_exception_handler(request, err: SodaflowError):
    logging.critical(err, exc_info=True)
    base_error_message = f"Failed to execute: {request.method}: {request.url}"

    result = Result(code=err.code, message=err.message)
    meta = Meta(version='v1')
    response = ExceptionResponseDto(result=result, meta=meta, data=dict())
    return JSONResponse(
        status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(response)
    )


async def sodaflow_soda_reponse_exception_handler(request: Request, exc: SodaflowResponseError) -> Response:
    logging.critical(exc, exc_info=True)
    headers = getattr(exc, "headers", None)
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    meta = Meta(version='v1')
    result = Result(code=exc.code, message=f"{exc.message}.")
    response = ExceptionResponseDto(result=result, meta=meta, data=dict())
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(response)
    )





# https://fastapi.tiangolo.com/tutorial/handling-errors/