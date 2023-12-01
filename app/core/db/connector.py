import logging
from asyncio import current_task
from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from app.core.db.transaction import Transactional, SqlAlchemyTransaction



class AsyncDatabaseConnector:
    def __init__(self, **kwargs):
        self._scoped_session = None
        self._engine = None
        self._session_local = None
        self._transaction = None
        # self.init_app(**kwargs)

    def init_app(self, **kwargs):
        database_url = kwargs.get("DB_URL")
        pool_recycle = kwargs.setdefault("DB_POOL_RECYCLE", 900)
        echo = kwargs.setdefault("DB_ECHO", False)
        connect_args = kwargs.get("connect_args", {})
        future = kwargs.get("future", True)
        pool_size = kwargs.get("pool_size", 20)
        max_overflow = kwargs.get("max_overflow", 40)

        self._engine = create_async_engine(
            url=database_url,
            echo=echo,
            future=future,
            pool_recycle=pool_recycle,
            connect_args=connect_args,
            pool_pre_ping=True,
            #pool_size=pool_size,
            #max_overflow=max_overflow
        )
        self._session_local = async_sessionmaker(bind=self._engine, autocommit=False, autoflush=False,
                                           class_=AsyncSession,
                                           expire_on_commit=False)

        self._scoped_session = async_scoped_session(
            session_factory=self._session_local,
            scopefunc=current_task
        )

    async def get_session(self):
        if self._session_local is None:
            raise Exception("must be called 'init_app'")
        db_session = None
        try:
            async with self._session_local() as session:
                yield session
        finally:
            await db_session.close()

    # get_session와 별도 분리 수정 확인
    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        if self._session_local is None:
            raise Exception("must be called 'init_app'")
        # try:
        async with self._session_local() as session:
            yield session
           # await session.close()
        # finally:
        #     print(session)
        #     print(type(session))
        #     # await session.close()

    def get_tx(self):
        return Transactional(self._session_local)

    @property
    def scoped_session(self):
        return self._scoped_session

    @property
    def session(self):
        #return self.get_session
        return self.get_async_session

    @property
    def engine(self):
        return self._engine

    @property
    def transaction(self):
        return self.get_tx


class DatabaseConnector:
    def __init__(self, **kwargs):
        self._engine = None
        self._session_local = None
        self._transaction = None

    def init_app(self, **kwargs):
        database_url = kwargs.get("DB_URL")
        pool_recycle = kwargs.setdefault("DB_POOL_RECYCLE", 900)
        echo = kwargs.setdefault("DB_ECHO", False)
        connect_args = kwargs.get("connect_args", {})

        self._engine = create_engine(
            database_url,
            echo=echo,
            pool_recycle=pool_recycle,
            pool_pre_ping=True,
            connect_args=connect_args,
        )
        self._session_local = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)


    def get_session(self):
        if self._session_local is None:
            raise Exception("must be called 'init_app'")
        db_session = None
        try:
            db_session = self._session_local()
            yield db_session
        finally:
            db_session.close()

    @property
    def session(self):
        return self.get_session

    @property
    def engine(self):
        return self._engine

    @property
    def transaction(self):
        return SqlAlchemyTransaction(self._session_local)

