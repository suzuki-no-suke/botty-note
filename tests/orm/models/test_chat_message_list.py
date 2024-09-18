import unittest

from src.orm.models.chat_message_list import ChatMessageList

import datetime

class ChatMessageListTest(unittest.TestCase):
    def test_init(self):
        obj = ChatMessageList()
        obj.time = datetime.datetime.now()
        print(str(obj))


