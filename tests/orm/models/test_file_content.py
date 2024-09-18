import unittest

from src.orm.models.file_content import FileContent

class FileContentTest(unittest.TestCase):
    def test_init(self):
        obj = FileContent()
        print(str(obj))


