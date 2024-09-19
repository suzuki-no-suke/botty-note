import shutil
import os

class FixedFileHandler:
    def __init__(self, fixed_dir, respawn_dir):
        self.fixed_dir = fixed_dir
        self.respawn_dir = respawn_dir

    def common_respawn_file(self, filename):
        respawn_fullpath = os.path.abspath(
                os.path.join(self.fixed_dir, filename)
            )
        if not os.path.isfile(respawn_fullpath):
            from_fullpath = os.path.abspath(
                os.path.join(self.respawn_dir, filename)
            )
            if os.path.isfile(from_fullpath):
                shutil.copy(from_fullpath, respawn_fullpath)
            else:
                raise FileNotFoundError(f"fixed {filename} not found")

    def respawn_index(self):
        self.common_respawn_file("index.md")

    def respawn_leftmenu(self):
        self.common_respawn_file("leftmenu.md")
