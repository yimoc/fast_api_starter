import uuid

from sqlalchemy import Column, String, Integer, DateTime, func

from app.core.sqlalchemy.typedecorator import GUID
from app.core.sqlalchemy.database import Base

class UploadedFile(Base):
    __tablename__ = 'uploadfile'
    __mapper_args__ = {'eager_defaults': True}  #https://stackoverflow.com/questions/64838259/reading-datetime-column-gives-detachedinstanceerror-after-session-is-closed

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(256))
    size = Column(Integer, nullable=False)
    path = Column(String(512), nullable=False)
    created_at = Column(DateTime(), server_default=func.now(), nullable=False)

    def __repr__(self):
        return str(self.__dict__)