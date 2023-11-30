from sqlalchemy.ext.asyncio import AsyncAttrs

from app.core.db.connector import AsyncDatabaseConnector
from sqlalchemy.orm import declarative_base, DeclarativeBase

class Base(AsyncAttrs, DeclarativeBase):
    pass

db_connector = AsyncDatabaseConnector()

async def create_db_and_tables():
    async with db_connector.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_tables():
    async with db_connector.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)