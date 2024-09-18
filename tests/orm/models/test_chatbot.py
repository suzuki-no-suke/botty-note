import unittest

from src.orm.models.chatbot import ChatBot

class ChatBotTest(unittest.TestCase):
    def test_init(self):
        obj = ChatBot()
        print(str(obj))


