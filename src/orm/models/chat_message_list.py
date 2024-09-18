from ..Base import Base

from sqlalchemy.schema import Column
from sqlalchemy.types import String, DateTime

class ChatMessageList(Base):
    __tablename__ = 'chat_message_list'

    history_id = Column(String, primary_key=True)
    message_id = Column(String, primary_key=True)
    time = Column(DateTime(timezone=False))

    def __str__(self) -> str:
        return f"ChatMessageList - {self.history_id} {self.message_id} @ {self.time.isoformat()}"
