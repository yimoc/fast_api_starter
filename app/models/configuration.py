import uuid

from sqlalchemy import Column, String

from app.core.sqlalchemy.typedecorator import GUID
from app.core.sqlalchemy.database import Base


class Configuration(Base):
    __tablename__ = "configuration"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    key = Column(String(20), unique=True, index=True)
    value = Column(String(255), nullable=False)
    description = Column(String(100))

    def __repr__(self):
        return str(self.__dict__)
