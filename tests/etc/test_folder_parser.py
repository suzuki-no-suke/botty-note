import unittest
import os

from src.etc.FolderParser import FolderParser, ContentType

"""
Expected test data structure

  * /dummy_dir (folder/4)
    * /dir2 (folder/1)
    * /emptydir (folder/0)
      * .gitignore (file/0)
    * /somedir (folder/2)
      * /depthlimit (folder/2)   # limit
        * /moredepth (folder/1) # ignored
          * /deeper (folder/1)  # ignored
            * template.md (file/1)  # ignored
        * template.md (file/0)  # ignored
      * template.md (file/0)
    * somefile.md (file/0)
"""

class TestFolderParser_ListDir(unittest.TestCase):
    def setUp(self):
        self.test_target = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "../fixture/dummy_dir"))
        #print(f"test target -> {self.test_target}")

    def test_list_dir_with_ignore(self):
        parser = FolderParser(self.test_target) # default ignore
        result = parser.sorted_ignored_listdir(self.test_target)
        #print(f"listed -> {result}")
        self.assertEqual(result[0], 'dir2')
        self.assertEqual(result[3], 'somefile.md')

    def test_list_dir_disable_ignore(self):
        parser = FolderParser(self.test_target, [])
        result = parser.sorted_ignored_listdir(self.test_target)
        self.assertEqual(result[1], 'emptydir')
        result2 = parser.sorted_ignored_listdir(os.path.join(self.test_target, result[1]))
        self.assertEqual(result2[0], '.gitignore')


class TestFolderParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_target = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "../fixture/dummy_dir"))
        cls.parser = FolderParser(cls.test_target)
        cls.parsed = cls.parser.parse(depth=3)

    def test_root_dir(self):
        p = self.parsed
        self.assertEqual(p['name'], 'dummy_dir')
        self.assertEqual(p['type'], ContentType.Folder)
        self.assertEqual(p['children'], 4)
        self.assertEqual(len(p['folder']), 4)


    def test_deepest_folder(self):
        p = self.parsed
        # NOTE : expect folder order consistency
        deepest = p['folder'][2]['folder'][0]
        self.assertEqual(deepest['name'], 'depthlimit')
        self.assertEqual(deepest['type'], ContentType.Folder)
        self.assertEqual(deepest['children'], 2)
        self.assertEqual(deepest['folder'], []) # must empty list





