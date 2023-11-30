import sqlalchemy
from sqlalchemy import Column, Integer, String

from app.core.sqlalchemy.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(40), index=True)
    price = Column(sqlalchemy.Float)
    description = Column(String(50))

    def __repr__(self):
        return str(self.__dict__)
