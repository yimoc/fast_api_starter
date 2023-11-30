from sqlalchemy import Column, String, Integer

from app.core.sqlalchemy.database import Base

class Scope(Base):
    __tablename__ = 'scope'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    permission = Column(String(128), index=True, unique=True, nullable=False)
    description = Column(String(1024), nullable=False)

    def __repr__(self):
        return str(self.__dict__)