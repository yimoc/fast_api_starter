import logging
import uuid
from typing import Union

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.status import HTTP_404_NOT_FOUND

from app.core.exception.exceptions import SodaflowResponseError
from app.models.configuration import Configuration
from app.schemas.configurationdto import ConfigurationCreate, ConfigurationUpdate, ConfigurationResponse

logger = logging.getLogger(__name__)


async def selects(session: AsyncSession, key: str=None) -> list:
    if not key:
        result = await session.execute(select(Configuration))
    else:
        result = await session.execute(select(Configuration).filter(Configuration.key == key))

    return result.scalars().all()


async def select_by_id(session: AsyncSession, id: str) -> Configuration:
    result = await session.execute(select(Configuration).filter(Configuration.id == id))
    return result.scalars().first()


async def select_by_key(session: AsyncSession, key: str) -> Configuration:
    result = await session.execute(select(Configuration).filter(Configuration.key == key))
    return result.scalars().first()
    

async def insert(session: AsyncSession, configuration: ConfigurationCreate) -> Configuration:
    configuration_record = Configuration(**configuration.model_dump(), id=uuid.uuid4())
    session.add(configuration_record)
    await session.commit()
    return configuration_record


async def update(session: AsyncSession, id, configuration: ConfigurationUpdate) -> Configuration:
    selected_configuration = await select_by_id(session, id)
    if selected_configuration:
        for column in Configuration.__table__.columns:
            value = getattr(configuration, column.name, None)
            if value:
                setattr(selected_configuration, column.name, value)
    return selected_configuration


async def delete(session: AsyncSession, id: str) -> bool:
    configuration = await session.get(Configuration, id)
    if configuration:
        await session.delete(configuration)
        return True
    else:
        raise SodaflowResponseError(
            status_code=HTTP_404_NOT_FOUND,
            code = "NotFound",
            message = f"Not found Id = {configuration.id}"
        )




