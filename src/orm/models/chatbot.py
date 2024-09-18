from ..Base import Base

from sqlalchemy.schema import Column, Identity
from sqlalchemy.types import Integer, String

class ChatBot(Base):
    __tablename__ = 'chatbot'

    pk = Column(Integer, Identity(), primary_key=True)
    botname = Column(String(255), nullable=False)
    module_filename = Column(String)
    classname = Column(String)

    def __str__(self) -> str:
        return f"ChatBot - {self.pk} {self.botname} (module {self.module_filename} class {self.classname})"
