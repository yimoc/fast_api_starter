import logging
import traceback
from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSessionTransaction, AsyncSession

from app.core.unit_of_work import AbstractUnitOfWork
logger = logging.getLogger()

class SqlAlchemyTransaction(AbstractUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.session = self.session_factory()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            print("- [commit ] :")
            self.commit()
        else:
            print("- [rollback ] ")
            self.rollback()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


# Async Transaction decorators.
def Transactional(fn=None):
    def decorator(func):
        @wraps(func)
        async def wrapper(session: AsyncSession, *args, **kwargs):
            async with session as session:
                async with AsyncSessionTransaction(session=session):
                    try:
                        logger.info(f"Start Transaction {func.__name__}")
                        result = await func(session, *args, **kwargs)
                        await session.commit()
                    except Exception:
                        traceback.print_exc()
                        logger.error("Transactional Annotation failed. Roll_back database")
                        await session.rollback()
                        raise
                    finally:
                        await session.close()
                        logger.info(f"Transaction {func.__name__} finished.")
            return result
        return wrapper

    if fn is None:
        return decorator
    else:
        return decorator(fn)


def Class_Transactional(fn=None):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            try:
                logger.info(f"Start Transaction {func.__name__}")
                result = await func(self, *args, **kwargs)
                await self.session.commit()
            except Exception:
                logger.error("Class Transactional Annotation failed. Roll_back database")
                await self.session.rollback()
                raise
            finally:
                await self.session.remove()
                logger.info(f"Transaction {func.__name__} finished.")
            return result
        return wrapper

    if fn is None:
        return decorator
    else:
        return decorator(fn)