from ..Base import Base

from sqlalchemy.schema import Column, Identity
from sqlalchemy.types import Integer, String

class FileContent(Base):
    __tablename__ = 'file_content'

    pk = Column(Integer, Identity(), primary_key=True)
    id = Column(String, nullable=False)
    extension = Column(String(10), default='')
    original_filename = Column(String, nullable=False)

    def __str__(self) -> str:
        return f"FileContent - {self.pk} {self.id}.{self.extension} ({self.original_filename})"
