import unittest
import os
import shutil

from src.md.FixedFilesHandler import FixedFileHandler

class TestFixedFileHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixed_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '../fixture/respawn/from'))
        cls.respawn_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '../fixture/respawn/to'))
        # cleanup
        for f in cls.respawn_dir:
            fullpath = os.path.join(cls.respawn_dir, f)
            if f != ".gitignore" and os.path.exists(fullpath):
                os.remove(fullpath)

    @classmethod
    def tearDownClass(cls):
        # cleanup
        for f in cls.respawn_dir:
            fullpath = os.path.join(cls.respawn_dir, f)
            if f != ".gitignore" and os.path.exists(fullpath):
                os.remove(fullpath)

    def setUp(self):
        self.handler = FixedFileHandler(self.fixed_dir, self.respawn_dir)

    def test_respawn_index(self):
        # テスト用の index.md を respawn_dir に作成
        self.handler.respawn_index()
        self.assertTrue(os.path.isfile(os.path.join(self.fixed_dir, 'index.md')))

    def test_respawn_leftmenu(self):
        # テスト用の leftmenu.md を respawn_dir に作成
        self.handler.respawn_leftmenu()
        self.assertTrue(os.path.isfile(os.path.join(self.fixed_dir, 'leftmenu.md')))

    def test_respawn_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            self.handler.common_respawn_file("nonexistent.md")

