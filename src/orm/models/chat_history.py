from ..Base import Base

import sqlalchemy
from sqlalchemy.schema import Column, Identity
from sqlalchemy.types import Integer, String

import enum

class ChatStatus(enum.Enum):
    Waiting = 'waiting'
    InProgress = 'in_progress'
    Failed = 'failed'
    Completed = 'completed'

class ChatHistory(Base):
    __tablename__ = 'chat_history'

    pk = Column(Integer, Identity(), primary_key=True)
    id = Column(String, nullable=False)
    status = Column(sqlalchemy.Enum(ChatStatus), nullable=False)
    botname = Column(String(255), nullable=False)

    def __str__(self) -> str:
        return f"ChatHistory - {self.pk} {self.id} {self.botname} ({self.status})"
