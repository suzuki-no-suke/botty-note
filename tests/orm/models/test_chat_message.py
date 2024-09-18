import unittest

from src.orm.models.chat_message import ChatType, ChatMessage

import datetime

class ChatMessageTest(unittest.TestCase):
    def test_init(self):
        obj = ChatMessage()
        obj.type = ChatType.Chatbot
        obj.content = "this is a test"
        obj.time = datetime.datetime.now()
        print(str(obj))

