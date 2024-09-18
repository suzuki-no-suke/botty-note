import unittest

from src.orm.models.chat_history import ChatHistory

class ChatHistoryTest(unittest.TestCase):
    def test_init(self):
        obj = ChatHistory()
        print(str(obj))


