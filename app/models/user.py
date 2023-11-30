import uuid
from typing import List

from sqlalchemy import Column, String, Boolean, Table, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, relationship

from app.core.sqlalchemy.typedecorator import GUID
from app.core.sqlalchemy.database import Base
from app.models.auth import Scope

# user - scope ( n to n )
user_scope_table = Table(
    "user_scope",
    Base.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("scope_id", ForeignKey("scope.id")),
)

class User(Base):
    __tablename__ = 'user'
    __mapper_args__ = {'eager_defaults': True}  #https://stackoverflow.com/questions/64838259/reading-datetime-column-gives-detachedinstanceerror-after-session-is-closed

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    #userid = Column(String(32), unique=True, nullable=True)
    name = Column(String(64), unique=True, nullable=True)
    email = Column(String(128), unique=True)
    hashed_password = Column(String(1024), nullable=False)
    is_active = Column(Boolean, nullable=False)
    scopes: Mapped[List[Scope]] = relationship(secondary=user_scope_table, lazy='subquery',)
    created_at = Column(DateTime(), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(), onupdate=func.now(), nullable=True)

    def __repr__(self):
        return str(self.__dict__)



