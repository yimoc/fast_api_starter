import logging

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT

from app.core.db.transaction import Transactional
from app.core.exception.exceptions import SodaflowResponseError
from app.models.configuration import Configuration
from app.orm import configuration_orm
from app.schemas.configurationdto import ConfigurationCreate, ConfigurationUpdate, ConfigurationResponse

logger = logging.getLogger(__name__)


async def read_configurations(session: AsyncSession, key: str = None) -> list:
    result = await configuration_orm.selects(session, key)
    return result


async def read_configuration(session: AsyncSession, id: str) -> ConfigurationResponse:
    result = await configuration_orm.select_by_id(session, id)
    if not result:
        raise SodaflowResponseError(
            status_code=HTTP_404_NOT_FOUND,
            code="NotFound",
            message=f"Not found Id = {id}"
        )
    return result


async def create_configuration(session: AsyncSession, configuration: ConfigurationCreate) -> ConfigurationResponse:
    await check_duplicate_key(session, configuration.key)

    result = await configuration_orm.insert(session, configuration)
    return result


@Transactional
async def update_configuration(session: AsyncSession, id: str, configuration: ConfigurationUpdate):
    updated_configuration = await configuration_orm.update(session, id, configuration)
    return updated_configuration


@Transactional
async def delete_configuration(session: AsyncSession, id: str) -> bool:
    deleted_bool = await configuration_orm.delete(session, id)
    return deleted_bool


async def check_duplicate_key(session: AsyncSession, key):
    dupliated_key = await configuration_orm.select_by_key(session, key)
    if dupliated_key:
        raise SodaflowResponseError(
            status_code=HTTP_409_CONFLICT,
            code="DuplicatedKey",
            message=f"Duplicated Key = {key}"
        )