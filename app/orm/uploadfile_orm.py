import logging
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.status import HTTP_404_NOT_FOUND

from app.core.exception.exceptions import SodaflowResponseError
from app.models.file import UploadedFile
from app.schemas.uploadfile_dto import UploadFileCreate

logger = logging.getLogger(__name__)

async def selects(session: AsyncSession) -> list:
    result = await session.execute(select(UploadedFile))
    return result.scalars().all()

async def select_by_id(session: AsyncSession, id: str) -> UploadedFile:
    template = await session.get(UploadedFile, id)
    return template


async def insert(session: AsyncSession, uploadfile: UploadedFile):
    session.add(uploadfile)
    await session.commit()
    logger.debug(f"added ={uploadfile.id}")
    return uploadfile


async def delete(session: AsyncSession, id: str) -> bool:
    template = await session.get(UploadedFile, id)
    if template:
        await session.delete(template)
        return True
    else:
        raise SodaflowResponseError(
            status_code=HTTP_404_NOT_FOUND,
            code = "NotFound",
            message = f"Not found Id = {id}"
        )




