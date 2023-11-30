import logging
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.web.response_base import Meta, Result, SodaflowResponseBase
from starlette import status

from app.core.sqlalchemy.database import db_connector
from app.schemas.configurationdto import ConfigurationCreate, ConfigurationUpdate, ConfigurationResponse
from app.services.configuration_service import read_configurations, read_configuration, \
    create_configuration, update_configuration, delete_configuration

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase[List[ConfigurationResponse]])
async def request_configurations(
        key: str = None, 
        db: AsyncSession = Depends(db_connector.session)):
    logger.debug(f'key : {key}')
    configurations = await read_configurations(db, key)
    result = Result()
    meta = Meta(version='v1')
    response_data = SodaflowResponseBase[List[ConfigurationResponse]](data=configurations, result=result, meta=meta)
    return response_data


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase[ConfigurationResponse])
async def request_configuration(
        id: str,
        db: AsyncSession = Depends(db_connector.session)):
    logger.debug(f"id : {id}")
    configuration = await read_configuration(db, id)
    result = Result()
    meta = Meta(version='v1')
    configuration_rsp = ConfigurationResponse.model_validate(configuration.__dict__)
    response_data = SodaflowResponseBase[ConfigurationResponse](data=configuration_rsp, result=result, meta=meta)
    return response_data


@router.post("", status_code=status.HTTP_201_CREATED, response_model=SodaflowResponseBase[ConfigurationResponse])
async def request_create_configuration(
        configuration: ConfigurationCreate,
        session: AsyncSession = Depends(db_connector.session)
    ):
    logger.info(f"configuration : {configuration}")
    configuration = await create_configuration(session, configuration)
    result = Result()
    meta = Meta(version='v1')
    response_data = SodaflowResponseBase[ConfigurationResponse](data=configuration, result=result, meta=meta)
    return response_data


@router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase[ConfigurationResponse])
async def request_update_configuration(
        id: str,
        configuration: ConfigurationUpdate,
        session: AsyncSession = Depends(db_connector.session)):
    logger.info(f"configuration : {configuration}")
    updated_configuration = await update_configuration(session, id, configuration)
    meta = Meta(version='v1')
    response_data = SodaflowResponseBase[ConfigurationResponse](data=updated_configuration, result=Result(), meta=meta)
    return response_data


@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase)
async def request_delete_configuration(
        id: str,
        session: AsyncSession = Depends(db_connector.session)):
    bool_result = await delete_configuration(session, id)
    data = dict(bool= bool_result)
    meta = Meta(version='v1')
    response_data = SodaflowResponseBase[dict](data=data, result=Result(), meta=meta)
    return response_data
