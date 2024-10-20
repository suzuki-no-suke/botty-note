from ..Base import Base
from sqlalchemy import Column, Text, TIMESTAMP, Enum
from sqlalchemy.types import TIMESTAMP

import enum

class EntryType(enum.Enum):
    FILE = 'file'
    DIRECTORY = 'directory'

class FileSystemMeta(Base):
    __tablename__  = 'file_system_meta'

    file_path = Column(Text, primary_key=True)
    entry_type = Column(Enum(EntryType), nullable=False)
    content_type = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    tag = Column(Text)
    unique_id = Column(Text)
    wikiname = Column(Text)

    def __str__(self):
        return f"FileSystemMeta(file_path={self.file_path}, entry_type={self.entry_type}, content_type={self.content_type}, created_at={self.created_at}, updated_at={self.updated_at}, tag={self.tag}, unique_id={self.unique_id}, wikiname={self.wikiname})"
