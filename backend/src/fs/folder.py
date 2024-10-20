import os
import shutil

class Folder:
    @classmethod
    def create_folder(cls, path):
        """指定されたパスにフォルダを作成します。"""
        os.makedirs(path, exist_ok=True)
        print(f"フォルダ '{path}' を作成しました。")

    @classmethod
    def move_folder(cls, src, dest):
        """フォルダを指定されたソースからデスティネーションに移動します。"""
        shutil.move(src, dest)
        print(f"フォルダ '{src}' を '{dest}' に移動しました。")

    @classmethod
    def delete_folder(cls, path):
        """指定されたパスのフォルダを削除します。"""
        shutil.rmtree(path)
        print(f"フォルダ '{path}' を削除しました。")
